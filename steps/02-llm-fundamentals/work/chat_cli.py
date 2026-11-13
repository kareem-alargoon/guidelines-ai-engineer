from llm_client import chat, Role, LLMError, ChatResult

# English, because Arabic shows right-to-left reversed in the Windows terminal.
SYSTEM_PROMPT = "You are an assistant named Nour. Always reply in simple English."
CONTEXT_SIZE = 512    # sent to Ollama as num_ctx; the max tokens the model can see at once
# Cap each reply. With a small context and no cap, a long answer filled the context and
# the model kept going until our 120 s timeout. 150 also makes the history grow fast.
MAX_TOKENS = 150
WARNING_RATIO = 0.8   # warn when the prompt uses more than 80% of the context

# ---------- /summarize (compaction) ----------
# The summary is saved as a second system message that starts with this prefix.
# Ollama joins all system messages into one (checked with qwen2.5:3b), and trim_history
# keeps every system message, so the summary survives the sliding window too.
# Tested before choosing it (6 tries each, qwen2.5:3b, an HTTP turn between the summary and
# "What is my name and what is my job?"):
#   "Summary of the earlier conversation: ..."                         → 4/6 answered with the name
#   the same + "the user told you these facts ... use them" (below)    → 6/6
# Without the instruction, the 3B model often says "I don't have information about you".
SUMMARY_PREFIX = (
    "Earlier in this conversation the user told you the facts below. They are true, and you remember them. "
    "Use them when the user asks about themselves or about earlier messages.\n"
    "Summary of the earlier conversation: "
)
# "The user's name is Kareem" instead of "Kareem is a Laravel developer": with the second
# wording, the chat model did not connect "Kareem" to the person it was talking to.
# The 3B model does not always follow this (1 of 4 tries in a test), so check the summary in /history.
SUMMARY_PROMPT = """You summarize a conversation between a user and an assistant.
Every sentence must start with "The user". Never use the user's name as the subject of a sentence.

Example:
Conversation:
user: Hi, I'm Sara and I'm a nurse. What is a fever?
assistant: Hi Sara! A fever is a body temperature above normal...
Summary:
The user's name is Sara. The user works as a nurse. The user asked what a fever is.

Keep every fact the user said about themselves (name, job, preferences) and anything they asked to remember.
One short phrase per topic. At most 5 sentences. Write only the sentences, without a title like "Summary:"."""
SUMMARY_MAX_TOKENS = 120
KEEP_AFTER_SUMMARY = 2  # the last turn (question + reply) stays as it is
# The summary request is a separate call with its own window. If it used our tiny 512,
# a long history would be cut silently BEFORE the model reads it (the Task 7 lesson),
# and the oldest messages (the name!) would be lost from the summary itself.
SUMMARY_CONTEXT_SIZE = 2048


def new_context() -> list[dict[str, str]]:
    """A fresh conversation: only the system message. Used at start and by /reset."""
    return [{"role": Role.SYSTEM.value, "content": SYSTEM_PROMPT}]


def trim_history(
        messages: list[dict[str, str]],
        max_messages: int,
) -> list[dict[str, str]]:
    """Sliding window: keep every system message, plus the last `max_messages` other messages.

    - Never starts the window with an assistant reply whose user question was cut off,
      so the window can end up with max_messages - 1 messages.
    - Returns a NEW list; `messages` itself is not changed.
      (The dicts inside are shared, which is fine because we never edit them.)
    """
    system = [m for m in messages if m["role"] == Role.SYSTEM.value]
    others = [m for m in messages if m["role"] != Role.SYSTEM.value]

    window = others[-max_messages:]  # the last N, like array_slice($others, -N)
    if window and window[0]["role"] == Role.ASSISTANT.value:
        window = window[1:]  # drop the reply that lost its question

    return system + window


def is_summary(message: dict[str, str]) -> bool:
    return message["role"] == Role.SYSTEM.value and message["content"].startswith(SUMMARY_PREFIX)


def split_for_summary(
        messages: list[dict[str, str]],
        keep_last: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Split the history into (system, to_summarize, keep). No model call, so it's easy to test.

    - system: the normal system messages (not old summaries). They stay as they are.
    - keep: the last `keep_last` user/assistant messages, never starting with an orphan reply.
    - to_summarize: any old summary + every user/assistant message that is not kept.
      An old summary goes in, so a second /summarize makes ONE new summary, not two.
    """
    system = [m for m in messages if m["role"] == Role.SYSTEM.value and not is_summary(m)]
    old_summaries = [m for m in messages if is_summary(m)]
    others = [m for m in messages if m["role"] != Role.SYSTEM.value]

    # careful: others[-0:] is the WHOLE list, not an empty one
    keep = others[-keep_last:] if keep_last > 0 else []
    if keep and keep[0]["role"] == Role.ASSISTANT.value:
        keep = keep[1:]  # its question goes to the summary, so the reply goes there too

    to_summarize = old_summaries + others[:len(others) - len(keep)]
    return system, to_summarize, keep


def format_transcript(messages: list[dict[str, str]]) -> str:
    """The messages as plain text, one per line, for the summary request."""
    return "\n".join(f"{m['role']}: {m['content']}" for m in messages)


def summarize_history(
        messages: list[dict[str, str]],
        keep_last: int,
) -> tuple[list[dict[str, str]], ChatResult | None]:
    """Compaction: replace the old messages with one summary message, right after the system message.

    Returns (new history, the ChatResult of the summary call). The result is None when there
    was nothing old enough to summarize. Like trim_history, it returns a NEW list.
    LLMError is not caught here: if the call fails, the caller keeps the old history.
    """
    system, to_summarize, keep = split_for_summary(messages, keep_last)
    if not to_summarize:
        return list(messages), None

    request = [
        {"role": Role.SYSTEM.value, "content": SUMMARY_PROMPT},
        # same "Conversation: ... Summary:" shape as the example in SUMMARY_PROMPT
        {"role": Role.USER.value, "content": "Conversation:\n" + format_transcript(to_summarize) + "\nSummary:"},
    ]
    # temperature 0: a summary should be stable, not creative
    result = chat(request, temperature=0, max_tokens=SUMMARY_MAX_TOKENS, context_size=SUMMARY_CONTEXT_SIZE)

    # the model sometimes starts with "Summary:" anyway (seen in a test run)
    text = result.text.strip().removeprefix("Summary:").strip()
    summary = {"role": Role.SYSTEM.value, "content": SUMMARY_PREFIX + text}
    return system + [summary] + keep, result


def print_history(context: list[dict[str, str]]) -> None:
    for message in context:
        print(f"{message['role']}: {message['content']}")


def print_usage(input_tokens: int, output_tokens: int, seconds: float, stop_reason: str) -> None:
    """Show how much of the context window the last request used, and warn near the limit."""
    used = input_tokens / CONTEXT_SIZE
    print(f"in: {input_tokens} / {CONTEXT_SIZE} tokens ({used:.0%}) | out: {output_tokens} tokens "
          f"| {seconds:.2f} s | stop: {stop_reason}")
    if used > WARNING_RATIO:
        print("⚠️ context is almost full: older messages may be dropped")


def parse_trim_command(inp: str) -> int | None:
    """Read N from '/trim N'. Returns None for '/trim off'. Raises ValueError if N is not a whole number >= 1."""
    parts = inp.split()
    if len(parts) != 2:
        raise ValueError("Use: /trim N (N = how many messages to keep) or /trim off")
    if parts[1] == "off":
        return None
    if not parts[1].isdigit():  # "abc" or "-2"
        raise ValueError(f"N must be a whole number, not {parts[1]!r}")
    n = int(parts[1])
    if n < 1:
        raise ValueError("N must be 1 or more")
    return n


def main() -> None:
    context = new_context()
    window_size: int | None = None  # None = no trimming (Ollama truncates on its own)

    try:
        while True:
            inp = input("Enter your message>> ").strip()
            if inp == "/reset":
                context = new_context()  # keep the system message, drop the rest
                print("context is reset")
                continue
            elif inp == "":
                print("This is empty input")
                continue
            elif inp == "/history":
                print_history(context)
                continue
            elif inp == "/exit":
                break
            elif inp.startswith("/trim"):
                try:
                    window_size = parse_trim_command(inp)
                except ValueError as e:
                    print(e)
                    continue
                if window_size is None:
                    print("trim is off")
                else:
                    context = trim_history(context, window_size)
                    print(f"trim is on: keeping the system message + the last {window_size} messages")
                continue
            elif inp == "/summarize":
                old_count = len(context)
                try:
                    new_history, summary_result = summarize_history(context, KEEP_AFTER_SUMMARY)
                except LLMError as e:
                    print(f"Summary failed, the history is unchanged: {e}")
                    continue
                if summary_result is None:
                    print("Nothing to summarize yet: the history is too short")
                    continue
                context = new_history
                print(f"summarized: {old_count} messages → {len(context)} "
                      f"(summary call: in {summary_result.input_tokens} tokens, "
                      f"out {summary_result.output_tokens} tokens, stop: {summary_result.stop_reason})")
                summary = next(m for m in context if is_summary(m))  # the first message that matches
                print(f"summary: {summary['content'].removeprefix(SUMMARY_PREFIX)}")
                continue
            elif inp.startswith("/"):
                # A typo like /hitstory used to go to the model as a normal message.
                print(f"Unknown command: {inp}. Commands: /history /reset /trim N /trim off /summarize /exit")
                continue
            else:
                context.append({"role": Role.USER.value, "content": inp})
                if window_size is not None:
                    context = trim_history(context, window_size)  # trim before every request
                try:
                    chat_result = chat(context, context_size=CONTEXT_SIZE, max_tokens=MAX_TOKENS)
                except LLMError as e:
                    print(e)
                    context.pop()
                    continue
                print("response is: ", chat_result.text)
                print_usage(chat_result.input_tokens, chat_result.output_tokens,
                            chat_result.duration_seconds, chat_result.stop_reason)
                context.append({"role": Role.ASSISTANT.value, "content": chat_result.text})
    except KeyboardInterrupt:
        print("\nExit Chat. Goodbye!")


if __name__ == "__main__":
    main()
