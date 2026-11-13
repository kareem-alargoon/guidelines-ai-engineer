"""Quick checks for trim_history, parse_trim_command and split_for_summary. No Ollama needed.

Run from the work folder:  python test_trim.py
"""
import copy

from chat_cli import trim_history, parse_trim_command, split_for_summary, SUMMARY_PREFIX


def msg(role: str, content: str) -> dict[str, str]:
    return {"role": role, "content": content}


SYSTEM = msg("system", "You are Nour.")
HISTORY = [
    SYSTEM,
    msg("user", "q1"), msg("assistant", "a1"),
    msg("user", "q2"), msg("assistant", "a2"),
    msg("user", "q3"), msg("assistant", "a3"),
]


def contents(messages: list[dict[str, str]]) -> list[str]:
    return [m["content"] for m in messages]


# 1. Keeps the system message + the last N messages.
assert contents(trim_history(HISTORY, 4)) == ["You are Nour.", "q2", "a2", "q3", "a3"]

# 2. Odd N would start with an assistant reply (a2) without its question: that reply is dropped.
assert contents(trim_history(HISTORY, 3)) == ["You are Nour.", "q3", "a3"]

# 3. The window right after a new user message (the CLI trims before sending).
with_new_question = HISTORY + [msg("user", "q4")]
assert contents(trim_history(with_new_question, 3)) == ["You are Nour.", "q3", "a3", "q4"]

# 4. N bigger than the history: nothing is removed.
assert trim_history(HISTORY, 100) == HISTORY

# 5. N = 1 between turns keeps only the system message (the last message is an assistant reply).
assert contents(trim_history(HISTORY, 1)) == ["You are Nour."]

# 6. The original list is not changed.
before = copy.deepcopy(HISTORY)
result = trim_history(HISTORY, 2)
assert HISTORY == before
assert result is not HISTORY

# 7. Works without a system message too.
assert contents(trim_history(HISTORY[1:], 2)) == ["q3", "a3"]

# parse_trim_command
assert parse_trim_command("/trim 6") == 6
assert parse_trim_command("/trim off") is None
for bad in ["/trim", "/trim abc", "/trim 0", "/trim -2", "/trim 2 3"]:
    try:
        parse_trim_command(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"{bad!r} should raise ValueError")

# split_for_summary (the part of /summarize that doesn't call the model)

# 1. Keeps the last turn, summarizes the rest, the system message stays apart.
system, to_summarize, keep = split_for_summary(HISTORY, 2)
assert contents(system) == ["You are Nour."]
assert contents(to_summarize) == ["q1", "a1", "q2", "a2"]
assert contents(keep) == ["q3", "a3"]

# 2. keep_last = 0 summarizes everything (others[-0:] would have kept everything instead).
system, to_summarize, keep = split_for_summary(HISTORY, 0)
assert contents(to_summarize) == ["q1", "a1", "q2", "a2", "q3", "a3"]
assert keep == []

# 3. Odd keep_last: the orphan reply goes to the summary with its question, nothing is lost.
system, to_summarize, keep = split_for_summary(HISTORY, 3)
assert contents(to_summarize) == ["q1", "a1", "q2", "a2"]
assert contents(keep) == ["q3", "a3"]

# 4. A short history: nothing old enough to summarize.
system, to_summarize, keep = split_for_summary(HISTORY[:3], 2)
assert to_summarize == []
assert contents(keep) == ["q1", "a1"]

# 5. A second /summarize: the old summary goes INTO the new one, it is not kept next to it.
old_summary = msg("system", SUMMARY_PREFIX + "The user is Kareem.")
summarized_once = [SYSTEM, old_summary, msg("user", "q4"), msg("assistant", "a4"),
                   msg("user", "q5"), msg("assistant", "a5")]
system, to_summarize, keep = split_for_summary(summarized_once, 2)
assert contents(system) == ["You are Nour."]
assert contents(to_summarize) == [SUMMARY_PREFIX + "The user is Kareem.", "q4", "a4"]
assert contents(keep) == ["q5", "a5"]

# 6. trim_history keeps the summary, because it is a system message.
assert contents(trim_history(summarized_once, 2)) == [
    "You are Nour.", SUMMARY_PREFIX + "The user is Kareem.", "q5", "a5"]

# 7. The original list is not changed.
before = copy.deepcopy(HISTORY)
split_for_summary(HISTORY, 2)
assert HISTORY == before

print("trim and summary tests: all passed")
