# Task 7 — experiment 1: no trim (raw log, summarized)

Run by the learner on 2026-11-13. `qwen2.5:3b`, `CONTEXT_SIZE = 512` (num_ctx), `MAX_TOKENS = 150`.
System prompt: "You are an assistant named Nour. Always reply in simple English."
`/history` outputs and the long answers are cut here; only the numbers and the key replies are kept.

| # | user message | in / 512 | out | stop | notes |
|---|---|---:|---:|---|---|
| 1 | My name is Kareem and I work as a Laravel developer. | 40 (8%) | 27 | stop | "Hi Kareem, it's nice to meet you." |
| 2 | Explain HTTP status codes in detail. | 84 (16%) | 150 | length | cut at item 5 |
| 3 | What is the difference between SQL and NoSQL databases? Explain with examples. | 259 (51%) | 150 | length | |
| 4 | Tell me about the history of Cairo. | 427 (83%) | 150 | length | ⚠️ warning shown |
| 5 | What are the main features of Python? | **378 (74%)** | 150 | length | in **went down** although the history grew: Ollama dropped old messages. No warning. |
| 6 | What is my name and what is my job? | 373 (73%) | 40 | stop | "I don't have access to personal information like your name or job. We've been chatting about Cairo's history" |
| 7 | /hitstory (typo) | 425 (83%) | 53 | stop | sent to the model as a normal message |
| 8 | What is my name and what is my job? | 497 (97%) | 62 | stop | "I can't see any details about you." |
| 9 | What is your name? | 405 (79%) | 14 | stop | "My name is Nour." (the system message survived) |

- No error at any point.
- `/history` in the CLI still showed every message, including message 1: our list was complete, the truncation happened inside Ollama.
- `input_tokens` never went above 512 (max 497).
