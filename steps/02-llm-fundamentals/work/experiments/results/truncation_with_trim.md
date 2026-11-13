# Task 7 — experiment 2: sliding window with `/trim 4` (raw log, summarized)

Run by the learner on 2026-11-13. Same setup as experiment 1: `qwen2.5:3b`, `CONTEXT_SIZE = 512`, `MAX_TOKENS = 150`, same system prompt, same messages.
First command: `/trim 4` → the CLI keeps the system message + the last 4 messages, and trims before every request.

| # | user message | in / 512 | out | stop | notes |
|---|---|---:|---:|---|---|
| 1 | My name is Kareem and I work as a Laravel developer. | 40 (8%) | 35 | stop | "Hi Kareem!" |
| 2 | Explain HTTP status codes in detail. | 92 (18%) | 150 | length | |
| 3 | What is the difference between SQL and NoSQL databases? Explain with examples. | 210 (41%) | 150 | length | the name turn was already trimmed here (system + HTTP turn + this question) |
| 4 | Tell me about the history of Cairo. | 210 (41%) | 150 | length | |
| 5 | What are the main features of Python? | 203 (40%) | 150 | length | |
| 6 | What is my name and what is my job? | 205 (40%) | 46 | stop | "as an AI, I don't have access to information about individuals like your name or job ... Could you please tell me" |
| 7 | What is your name? | 97 (19%) | 14 | stop | "My name is Nour." |

- No warning at any point (max 41%). Compare experiment 1: 83% → 74% → 97%.
- `/history` at the end: the system message + the last 2 turns (4 messages). This time it shows exactly what the model saw.
- What each request carried: the system message + the previous turn + the new question. After the new question is added, the last 4 messages start with an old assistant reply whose question is gone, so `trim_history` drops it (3 messages sent, not 4).
