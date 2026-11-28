# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 04 — التعامل مع LLM APIs من Python 🟡
- **آخر حاجة خلصت:** **Step 03 ✅**: PR الكود (#9، `work/03-models-and-providers`، Tasks 0–7) اتراجع واتعمله merge على `main` (`09c886e`). أهم النتايج: `qwen2.5:3b` عدّى أرقام الـ eval (total و date 100%، و 2.85 ث للإيصال) بس الـ license `qwen-research` (non-commercial)، والقرار المبدئي **local بشرط موديل Apache 2.0** (`model_decision.md`)، والتكلفة على Claude سنتات في الشهر فمش هي اللي بتحسم. التفاصيل الكاملة في `steps/03-models-and-providers/work/observations.md`.
- **مواد Step 04 اتجهزت كلها (2026-11-28):** شرح **7 ملفات** من **23 مصدر** في `resources/articles/04-*`:
  1. الكورس *API Fundamentals* (6 notebooks)، مع تنبيه ⏳ على كل حاجة قديمة (الريبو archived، وموديلات Claude 3 اتشالت، و `temperature` والـ prefill اتمنعوا على الموديلات الجديدة).
  2. Messages API، و Streaming، و Structured outputs.
  3. Prompt caching، و Token counting.
  4. Errors، و Rate limits، و README الـ SDK.
  5. Ollama: API، و `/api/chat`، و Streaming، و Structured outputs، و **Anthropic compatibility**.
  6. uv، و Pydantic، و HTTPX Async.
  7. Real Python: asyncio.

  و `TASKS.md` فيه **9 تاسكات (0–8) + 3 Bonus**، مبنية على كود Step 03 (`llm_client.py`، و `providers.py`، و `cost.py`، و `model_eval.py`).
- **ملاحظات من تحضير Step 04:**
  - **Ollama 0.34.4 عندك بيدعم `/v1/messages` (Anthropic-compatible)**: اتجرّب بـ request عادي وبـ streaming على `qwen2.5:3b`. يعني الـ SDK الرسمي بتاع `anthropic` بيشتغل local من غير key، وده اللي التاسكات الأساسية مبنية عليه. و `/v1/messages/count_tokens` مش موجود (404)، زي ما الـ docs بتقول.
  - **`/api/chat` بيرجّع `prompt_eval_cached_count`** على 0.34.4 (اتأكدت)، و `llm_client.py` لسه مش بيقراه (Task 8).
  - **uv مش متسطّب** على الجهاز اللي اتحضّرت منه المواد. Task 0 فيها التسطيب.
  - **السؤالين اللي اتأجلوا من Step 03:**
    - **الحد الأدنى للـ caching:** 512 token لـ Haiku/Sonnet/Opus 5.5 و Fable (وأكتر للأقدم)، والأقصر مش بيتعمله cache **ومن غير error**. فالـ system prompt بتاع الإيصالات (~172 token) **مش هيتعمله cache**، وعمود الـ cache في `cost.py` مش واقعي.
    - **الفرق بين tokenizer الـ Qwen و Claude:** الـ docs مفيهاش إجابة. الـ "+30%" (اللي اتذكرت في Step 03) هي **Claude الجديد مقابل Claude القديم**، مش مقابل Qwen. والقياس الحقيقي بـ `count_tokens` (ببلاش بس محتاج key) في **Bonus B1**.
  - **`cost.py` بيفترض شكل OpenAI للـ usage** (الـ cached جزء من الـ input)، و Anthropic الـ 3 أرقام منفصلين، ومفيش حساب للـ cache writes. اتصلّح في Task 8.
- **الجاي:** commit و push لمواد الخطوة على `step/04-llm-apis`، وافتح PR، وبعد الـ merge: `work/04-llm-apis` وابدأ بـ **Task 0** (القعدة 1 في `steps/04-llm-apis/README.md`).

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ✅ اتعمله merge (`5bfdb1a`) | خلصت ✅ (Tasks 0–7 + Bonus) |
| 03 — الموديلات والـ Providers | ✅ المصادر الخمسة اتشرحوا + التاسكات | ✅ اتعمله merge (`09c886e`، PR #9) | خلصت ✅ (Tasks 0–7، والـ Bonus اتساب) |
| 04 — التعامل مع LLM APIs من Python | 🟡 المصادر السبعة اتشرحوا + التاسكات (مستني PR المواد) | ⬜ | التاسكات على Ollama (`/api/chat` و `/v1/messages`)، و Claude API في Bonus بس |

## البيئة
- الأجهزة: الـ **desktop الشخصي** (i5-14600K، و 32 GB DDR5، ومن غير GPU منفصل، شوف `steps/03-models-and-providers/work/hardware.md`)، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git). لحد Step 03 بـ `pip install -r requirements.txt`، ومن Step 04 بـ **uv** (`uv sync` من `pyproject.toml` و `uv.lock`).
- Ollama: **0.34.4**، والموديل `qwen2.5:3b` (3.1B، و `Q4_K_M`، و 1.9GB).
