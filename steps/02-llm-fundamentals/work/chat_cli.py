from llm_client import chat, Role, LLMError

# English, because Arabic shows right-to-left reversed in the Windows terminal.
SYSTEM_PROMPT = "You are an assistant named Nour. Always reply in simple English."
CONTEXT_SIZE = 512    # sent to Ollama as num_ctx; the max tokens the model can see at once
# Cap each reply. With a small context and no cap, a long answer filled the context and
# the model kept going until our 120 s timeout. 150 also makes the history grow fast.
MAX_TOKENS = 150
WARNING_RATIO = 0.8   # warn when the prompt uses more than 80% of the context


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
            elif inp.startswith("/"):
                # A typo like /hitstory used to go to the model as a normal message.
                print(f"Unknown command: {inp}. Commands: /history /reset /trim N /trim off /exit")
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
