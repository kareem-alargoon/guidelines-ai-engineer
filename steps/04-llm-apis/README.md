# Step 04 — التعامل مع LLM APIs من Python

> **Branch المواد:** `step/04-llm-apis` · **Branch شغلك:** `work/04-llm-apis` · **المدة المتوقعة:** أسبوع لأسبوعين

## 🎯 بعد الخطوة دي هتقدر
- تكلّم **Claude Messages API** بإيدك (httpx) وبالـ **SDK الرسمي** (`anthropic`)، وتفهم الـ response: **content blocks**، و `stop_reason`، و `usage`.
- تشغّل **نفس كود الـ SDK** على موديل **local** (Ollama `/v1/messages`) من غير key ومن غير ما الداتا تخرج، وتعرف **إيه اللي مش هيتطابق** لما تنقل لـ Claude.
- تعرف إيه اللي **اتغيّر في الموديلات الجديدة** عن الكورسات القديمة: `temperature` اتشال، والـ prefill اتمنع، والـ thinking بيسبق النص، والـ tokenizer الجديد.
- تعمل **streaming** بـ 3 طرق (NDJSON، و SSE بإيدك، و الـ SDK)، وتقيس الـ **TTFT**، وتتعامل مع الـ stream لما يقع.
- تاخد **JSON مضمون الشكل** (structured outputs) من Ollama ومن Claude، وتعمل validation صح بـ **Pydantic**.
- تتعامل مع **errors الـ API** (أعيد ولا لأ؟)، وتكتب **retries** بـ exponential backoff، وتفهم الـ **rate limits** (RPM، و ITPM، و OTPM، و ramp limits).
- تعالج requests كتير **بالتوازي** بـ **asyncio** بـ concurrency محدود، وتعرف إمتى ده بيسرّع وإمتى لأ.
- تحسب **التكلفة الحقيقية** من الـ `usage` (cache reads و writes)، وتعرف **إمتى الـ prompt caching بيشتغل أصلاً**.
- تدير مشروع Python بـ **uv** (زي Composer).

## 📚 المصادر (بالترتيب)

| # | المصدر | النوع | الشرح | الوقت التقريبي |
|:---:|---|:---:|---|---|
| 1 | [Anthropic Courses — *API Fundamentals*](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) — 6 notebooks | 🎓 | [`notes/01-anthropic-course-api-fundamentals.md`](notes/01-anthropic-course-api-fundamentals.md) ✅ | 3 ساعات |
| 2 | Anthropic docs — [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)، و [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)، و [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | 📚 | [`notes/02-anthropic-messages-streaming-structured.md`](notes/02-anthropic-messages-streaming-structured.md) ✅ | 3 ساعات |
| 3 | Ollama docs — [API](https://docs.ollama.com/api/introduction)، و [`/api/chat`](https://docs.ollama.com/api/chat)، و [Streaming](https://docs.ollama.com/api/streaming)، و [Structured outputs](https://docs.ollama.com/capabilities/structured-outputs)، و [**Anthropic compatibility**](https://docs.ollama.com/api/anthropic-compatibility) | 📚 | [`notes/05-ollama-api-and-anthropic-compat.md`](notes/05-ollama-api-and-anthropic-compat.md) ✅ | ساعة ونص |
| 4 | Anthropic docs — [Errors](https://platform.claude.com/docs/en/api/errors)، و [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)، و [README الـ Python SDK](https://github.com/anthropics/anthropic-sdk-python) | 📚 | [`notes/04-anthropic-errors-rate-limits-sdk.md`](notes/04-anthropic-errors-rate-limits-sdk.md) ✅ | ساعتين |
| 5 | Anthropic docs — [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)، و [Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) | 📚 | [`notes/03-anthropic-prompt-caching-token-counting.md`](notes/03-anthropic-prompt-caching-token-counting.md) ✅ | ساعتين ونص |
| 6 | [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)، و [Pydantic: Models](https://pydantic.dev/docs/validation/latest/concepts/models/)، و [HTTPX: Async](https://www.python-httpx.org/async/) | 📚 | [`notes/06-httpx-pydantic-uv.md`](notes/06-httpx-pydantic-uv.md) ✅ | ساعتين |
| 7 | Real Python — [*Python's asyncio: A Hands-On Walkthrough*](https://realpython.com/async-io-python/) | 📰 | [`notes/07-realpython-asyncio.md`](notes/07-realpython-asyncio.md) ✅ | ساعة ونص |

✅ = الشرح جاهز. كل مصادر الخطوة متشرحة من الملفات اللي في `resources/` (مش من الذاكرة). والتاسكات في [`TASKS.md`](TASKS.md).
> 📌 أرقام ملفات الشرح (01–07) هي ترتيب **الكتابة**، مش ترتيب القراية. **اقرا بترتيب الجدول ده** (خطة المذاكرة تحت).

### ليه المصادر دي وبالترتيب ده؟
1. **الكورس** الأول: بيشرح **شكل** الـ API ببطء وبأمثلة (messages، و response، و parameters، و streaming). **بس قديم** (archived، وموديلات Claude 3 اللي اتشالت)، فالشرح بينبّه على كل حاجة اتغيّرت بـ ⏳.
2. **Messages/Streaming/Structured outputs docs**: **الحقيقة الحالية** لنفس المواضيع، وفيها أهم التغييرات (`temperature`، والـ prefill، والـ thinking blocks).
3. **Ollama**: المقابل الـ **local** لكل ده، و**Anthropic compatibility** اللي بتخليك تجرّب الـ SDK كله ببلاش. لازم قبل Task 1.
4. **Errors و Rate limits**: إيه اللي بيحصل لما حاجة تبوظ في API حقيقي على الإنترنت. لازم قبل Task 2 (جزء الـ exceptions) و Task 6.
5. **Prompt caching و Token counting**: أصعب صفحتين، وبيجاوبوا على **السؤالين اللي اتأجلوا من Step 03**. آخر حاجة لأنهم محتاجين كل اللي قبلهم (`usage`، والـ system، والتكلفة).
6. **أدوات Python**: كل واحدة قبل التاسك اللي محتاجاها (uv قبل Task 0، و Pydantic قبل Task 5، و HTTPX Async + asyncio قبل Task 7).

> ⏳ **تنبيه:** مصادر 2–5 snapshot يوم **2026-11-28**. أسماء الموديلات والأسعار والـ limits بتتغيّر كل كام أسبوع. **اتعلّم شكل الـ API والقرارات، مش الأرقام.** والكورس (مصدر 1) **قديم عن قصد**: قراية مصدر قديم ومعرفة إيه اللي اتغيّر فيه مهارة لوحدها في المجال ده.

## 🧭 خطة المذاكرة
**طريقة كل قعدة:** اقرا الجزء في الأصل، وبعدين شرحه. وفي الآخر جاوب **أسئلة الفهم** بنفسك قبل ما تفتح الإجابات. والتاسكات بتتحل **وإنت ماشي**.

| القعدة | تذاكر إيه | الوقت | التاسكات اللي تقدر تعملها بعدها |
|:---:|---|---|---|
| 1 | الشرح 06: الجزء الأول (uv) | 30 دقيقة | **Task 0** |
| 2 | الكورس: lessons 1 و 2 و 3 | ساعة ونص | — |
| 3 | الكورس: lesson 4 + Messages API docs (الشرح 02، الجزء الأول) | ساعة ونص | — |
| 4 | Ollama: الـ 5 صفحات (الشرح 05) | ساعة ونص | **Task 1** |
| 5 | Errors + README الـ SDK (الشرح 04، الجزء الأول والتاني) | ساعة | **Task 2** |
| 6 | الكورس: lesson 5 + Streaming docs (الشرح 02، الجزء التاني) + HTTPX streaming (الشرح 06، جزء 8) | ساعتين | **Task 3** و **Task 4** |
| 7 | Structured outputs (الشرح 02، الجزء التالت) + Pydantic (الشرح 06، الجزء التالت) | ساعتين | **Task 5** |
| 8 | Rate limits (الشرح 04، الجزء التالت) | 45 دقيقة | **Task 6** |
| 9 | Real Python asyncio (الشرح 07) + HTTPX Async (الشرح 06، جزء 7–9) | ساعتين | **Task 7** |
| 10 | Prompt caching + Token counting (الشرح 03) | ساعتين ونص | **Task 8** |
| — | الكورس: lesson 6 (Vision) | 30 دقيقة | اختياري |

- القعدات 4 و 6 و 10 أهم حاجة في الخطوة.
- لما تبدأ تاسك: قولّي "Task N"، وهنمشي فيها **خطوة خطوة**. ولو التاسك محتاجة ملف داتا، أنا اللي هكتبه.
- **التاسكات كلها على `qwen2.5:3b` اللي عندك** (native أو عن طريق `/v1/messages`). **متنزّلش حاجة.**
- **مفيش تاسك أساسية محتاجة Claude API key.** فيه Bonus (B1، و B2) لو عندك key، وقولّي الأول.
- في الآخر: افتح PR بشغلك على `work/04-llm-apis`، وأنا هراجعه.

## ❓ السؤالين اللي اتأجلوا من Step 03
1. **الحد الأدنى لطول الـ prompt عشان يتعمله cache في Claude:** **512 token** لـ Haiku 5.5 و Sonnet 5.5 و Opus 5.5 و Fable، وأكتر للموديلات الأقدم (لحد 4,096 لـ Haiku 4.5). والأقصر **مش بيتعمله cache ومن غير error**. يعني الـ system prompt بتاع الإيصالات (~172 token) **مش هيتعمله cache**، وعمود الـ cache في `cost.py` مش واقعي. التفاصيل في [الشرح 03 جزء 7](notes/03-anthropic-prompt-caching-token-counting.md)، والحساب في Task 8.
2. **الفرق بين tokenizer الـ Qwen و Claude:** **الـ docs مافيهاش إجابة.** الـ "+30%" اللي في الـ docs (واللي اتذكرت في Step 03) هي **Claude الجديد مقابل Claude القديم**، مش مقابل Qwen. والطريقة الوحيدة: `count_tokens` على Claude (ببلاش بس محتاج key)، وده **Bonus B1**. التفاصيل في [الشرح 03 جزء 13](notes/03-anthropic-prompt-caching-token-counting.md).

## ✅ Checklist
- [x] رفعت مصادر الخطوة في `resources/`
- [ ] قريت الكورس (6 notebooks) + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت Messages API و Streaming و Structured outputs + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت صفحات Ollama الخمسة + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت Errors و Rate limits و README الـ SDK + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت Prompt caching و Token counting + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت uv و Pydantic و HTTPX Async و Real Python asyncio + الشرح، وجاوبت أسئلة الفهم
- [ ] حليت التاسكات وفتحت PR
- [ ] صلّحت ملاحظات الـ review واتعمل merge
