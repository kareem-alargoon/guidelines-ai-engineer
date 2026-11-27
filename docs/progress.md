# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 03 — الموديلات والـ Providers (Cloud vs Local) 🟡
- **آخر حاجة خلصت:** **Step 02 ✅**: PR الكود (`work/02-llm-fundamentals`، Tasks 0–7 ومعاهم الـ Bonus `/summarize`) اتعمله merge على `main` (`dc3394f`). ومواد **Step 03** اتجهزت كلها: شرح **5 مصادر** (Ch.4 *Model Selection* + ملحق Ch.3 *Comparative Evaluation*، و 10 صفحات Ollama، و 4 صفحات Anthropic، و Artificial Analysis، و LMArena)، و `TASKS.md` فيه 8 تاسكات + 3 Bonus.
- **ملاحظات من تحضير Step 03:**
  - Ollama عندك **0.34.4**، والـ docs اللي اتحفظت فيها features من versions أحدث (مش لازم تحدّث للتاسكات الأساسية).
  - `ollama ps` على الجهاز اللي اتحضّرت منه المواد: `qwen2.5:3b` اتحمّل بـ `size_vram = 0` (يعني على الـ CPU)، و context **4096** (مش 2048 زي صفحة Modelfile). هتتأكد بنفسك في Tasks 3 و 4.
  - الـ snapshots بتاعة الـ leaderboards: AA يوم 2026-11-13 (288 موديل، و 525 endpoint)، و LMArena يوم 2026-11-11 (421 موديل، و 9.1M صوت).
- **التاسكات على `work/03-models-and-providers`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Model card من Ollama | ✅ |
  | 2 — قارئ الـ leaderboard | ⬜ |
  | 3 — الوقت بيروح فين؟ (cold start و keep_alive) | ⬜ |
  | 4 — الـ context بياكل memory | ⬜ |
  | 5 — Providers زي drivers Laravel | ⬜ |
  | 6 — Mini eval: الموديل الـ local كفاية؟ | ⬜ |
  | 7 — التكلفة والقرار | ⬜ |

- **Task 0 (2026-11-27):** فولدر `work/` اتعمل فيه `llm_client.py` (من Step 02) و venv جديد و `requirements.txt` (ASCII، و `httpx 0.29.0`، و `pydantic 2.14.4`)، و `python llm_client.py` رد من `qwen2.5:3b`. و `hardware.md` اتكتب: الـ desktop الشخصي (i5-14600K، و 32 GB DDR5، و Intel UHD 770 مدمج من غير VRAM)، يعني الموديلات هتشتغل على الـ CPU والـ RAM، والـ default context هيبقى 4K.
  - ⚠️ في PowerShell 5.1، `pip freeze > requirements.txt` بيكتب **UTF-16** (git بيشوفه binary). استخدم `pip freeze | Out-File -Encoding ascii requirements.txt`.
- **Task 1 (2026-11-27):** `work/model_card.py` بيجيب الـ card من `/api/show` (كل حاجة) و `/api/tags` (الحجم بس)، و `context_length` بـ `key.endswith(".context_length")` من غير اسم الـ architecture، وبيطبع جدول لكل الموديلات. وموديل مش موجود بيرمي `LLMError` فيها `ollama pull` (عن طريق `handle_http_errors` من `llm_client`). النتيجة لـ `qwen2.5:3b`: `qwen2`، و 3.1B، و `Q4_K_M`، و context **32,768**، و license **`qwen-research`**، و 1.93 GB.
  - **الـ license:** "FOR NON-COMMERCIAL PURPOSES ONLY"، والاستخدام التجاري محتاج license منفصل من Alibaba Cloud. يعني `qwen2.5:3b` **مينفعش** في منتج تجاري من غير إذن.
  - ⚠️ **الـ license بيختلف بين أحجام نفس العيلة:** على Hugging Face، `Qwen2.5-1.5B-Instruct` و `Qwen2.5-7B-Instruct` بـ **Apache 2.0**، و `Qwen2.5-3B-Instruct` بس هو اللي `qwen-research`. افتكرها في Task 6.
  - الموديل يقدر على **32,768** token، بس Ollama بيحجز **4096** بس by default على جهاز VRAM بتاعه أقل من 24 GiB (هتتأكد في Task 4).
  - الكود كتبه المساعد بطلب منك من خطوة 4 (dataclass وجدول)، وإنت كتبت أول خطوتين وقريت الـ JSON والـ license بنفسك.
- **مستنيين منك:** commit و push لـ Task 1 على `work/03-models-and-providers`.
- **الجاي:** Task 2 (قارئ الـ leaderboard).

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ✅ اتعمله merge (`dc3394f`) | خلصت ✅ (Tasks 0–7 + Bonus) |
| 03 — الموديلات والـ Providers | ✅ المصادر الخمسة اتشرحوا + التاسكات | ⬜ | التاسكات على Ollama local، و Claude API في Bonus بس |

## البيئة
- الأجهزة: الـ **desktop الشخصي** (i5-14600K، و 32 GB DDR5، ومن غير GPU منفصل، شوف `steps/03-models-and-providers/work/hardware.md`)، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git، فبيتعمل على كل جهاز بـ `pip install -r requirements.txt`).
- Ollama: **0.34.4**، والموديل `qwen2.5:3b` (3.1B، و `Q4_K_M`، و 1.9GB).
