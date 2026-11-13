"""Quick checks for trim_history and parse_trim_command. No Ollama needed.

Run from the work folder:  python test_trim.py
"""
import copy

from chat_cli import trim_history, parse_trim_command


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

print("trim tests: all passed")
