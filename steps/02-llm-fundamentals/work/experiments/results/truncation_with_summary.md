# Task 7 — Bonus: `/summarize` (compaction) (raw log, summarized)

Run by the learner on 2026-11-13. Same setup as experiments 1 and 2: `qwen2.5:3b`, `CONTEXT_SIZE = 512`, `MAX_TOKENS = 150`, same system prompt. `/trim` was OFF.
`/summarize` keeps the last turn as it is (`KEEP_AFTER_SUMMARY = 2`), summarizes the rest at temperature 0 with `SUMMARY_CONTEXT_SIZE = 2048`, and saves the summary as a second system message (with `SUMMARY_PREFIX`).

| # | message | in / 512 | out | stop | notes |
|---|---|---:|---:|---|---|
| 1 | My name is Kareem and I work as a Laravel developer. | 40 (8%) | 31 | stop | |
| 2 | Explain HTTP status codes in detail. | 88 (17%) | 150 | length | |
| 3 | What is the difference between SQL and NoSQL databases? Explain with examples. | 263 (51%) | 150 | length | |
| — | `/summarize` | (summary call: 364 in, 22 out) | | stop | 7 messages → 4. Summary: "User's name is Kareem. User works as a Laravel developer. User asked about HTTP status codes." |
| 4 | Tell me about the history of Cairo. | **271 (53%)** | 150 | length | experiment 1 at the same point: 427 (83%) |
| 5 | What are the main features of Python? | 439 (86%) | 150 | length | ⚠️ |
| 6 | What is my name and what is my job? | 434 (85%) | 19 | stop | ✅ "Your name is Kareem. You told me earlier that you work as a Laravel developer." in went DOWN: Ollama dropped old messages again |
| 7 | What is my name and what is my job? | 472 (92%) | 18 | stop | ✅ "Your name is Kareem and your job is that you work as a Laravel developer." |
| 8 | What is your name? | 504 (98%) | 7 | stop | ✅ "My name is Nour." |
| 9 | What is my name and what is my job? | 362 (71%) | 18 | stop | ✅ same answer. in went DOWN again: another silent truncation |

- `/history` right after `/summarize`: the system message, the summary (as a system message), and the SQL turn.
- 4 of 4 identity answers were right (3 × name/job, 1 × Nour). Experiment 1: 0 of 2 for the name. Experiment 2: 0 of 1.
- The summary used the "User's name is ..." wording this time (in earlier small tests the 3B model often wrote "Kareem is ..." instead).
- Side note: the Cairo answer had wrong facts (for example "Baybars built the Great Mosque of Muhammad Ali"; that mosque is from the 19th century).
