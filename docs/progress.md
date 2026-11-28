# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 03 — الموديلات والـ Providers (Cloud vs Local) 🟡
- **آخر حاجة خلصت:** **Step 02 ✅**: PR الكود (`work/02-llm-fundamentals`، Tasks 0–7 ومعاهم الـ Bonus `/summarize`) اتعمله merge على `main` (`5bfdb1a`). ومواد **Step 03** اتجهزت كلها: شرح **5 مصادر** (Ch.4 *Model Selection* + ملحق Ch.3 *Comparative Evaluation*، و 10 صفحات Ollama، و 4 صفحات Anthropic، و Artificial Analysis، و LMArena)، و `TASKS.md` فيه 8 تاسكات + 3 Bonus.
- **ملاحظات من تحضير Step 03:**
  - Ollama عندك **0.34.4**، والـ docs اللي اتحفظت فيها features من versions أحدث (مش لازم تحدّث للتاسكات الأساسية).
  - `ollama ps` على الجهاز اللي اتحضّرت منه المواد: `qwen2.5:3b` اتحمّل بـ `size_vram = 0` (يعني على الـ CPU)، و context **4096** (مش 2048 زي صفحة Modelfile). هتتأكد بنفسك في Tasks 3 و 4.
  - الـ snapshots بتاعة الـ leaderboards: AA يوم 2026-11-13 (288 موديل، و 525 endpoint)، و LMArena يوم 2026-11-11 (421 موديل، و 9.1M صوت).
- **التاسكات على `work/03-models-and-providers`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Model card من Ollama | ✅ |
  | 2 — قارئ الـ leaderboard | ✅ |
  | 3 — الوقت بيروح فين؟ (cold start و keep_alive) | ✅ |
  | 4 — الـ context بياكل memory | ✅ |
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
- **Task 2 (2026-11-27):** `work/leaderboard.py` بيقرا صفحة الـ providers المحفوظة من AA (**snapshot يوم 2026-11-13**): كل صف 13 سطر، و `"--"` بيبقى `None`. النتيجة **525** endpoint (**408 Open** و **117 Proprietary**). الكود كتبه المساعد بطلب منك (التاسك parsing متكرر)، والتفاصيل في `work/observations.md`.
  - **الـ provider tags:** الـ providers بيزوّدوا على اسم الموديل (`FAST`، و `FP8`، و `Vertex`...)، فـ 253 اسم طلعوا 176 موديل بس. الـ dedup بـ `base_model()` بيشيلهم، والـ reasoning effort (`max`/`high`) بيفضل موديل لوحده. واتأكدنا إن كل مجموعة اتدمجت ليها نفس الـ index ونفس الـ license.
  - **أعلى موديل:** Claude Fable 5.2 (max) = **65**. وأعلى open: Kimi K3.1 Pro = **46** (الـ 26). يعني توقّع الكاتبة لسه ماشي.
  - **نفس الموديل:** Claude Opus 5.5 (max) على 4 platforms: **2.1x** في السعر (Google ضعف Anthropic)، و Bedrock بنفس السعر بس الـ errors الضعف (6.3% مقابل 3.2%). و gpt-oss-120b (high) عند 16 endpoint: **10.5x** في السعر، و **45x** في السرعة، والـ errors من 0% لـ 17.4%. **الأرخص (CoreWeave) error rate بتاعه 13.1%.**
  - ⚠️ الأرقام دي صورة من يوم واحد (2026-11-13)، و Cost/Time per Task على benchmark بتاع AA مش على شغلك: للمقارنة بين الـ providers بس، مش لحساب الفاتورة.
  - **LMArena (اتشاف live يوم 2026-11-27، والصفحة متحدّثة Nov 22):** في Coding + Open Source، أول 3: MiMo-V2.6-Pro (1,539)، و Kimi K3 (Max) (1,537)، و Kimi K3.1 Pro (Max) (1,535)، يعني متعادلين تقريباً. **مفيش category للعربي**، وأقرب حاجة Non-English. فالعربي محتاج eval بتاعك (Task 6).
- **Task 3 (2026-11-27، على الـ desktop الشخصي):** `ChatResult` بقى فيه `load_seconds` و `prompt_eval_seconds` و `eval_seconds` (بـ default، فالكود القديم شغّال) و `@property output_tokens_per_second` (÷ الـ eval مش الـ total)، و `chat()` بقى بياخد `keep_alive` في **body الـ request** (بـ `is not None` عشان `0` يتبعت). و `model_card.py` فيه `get_running_models()` من `/api/ps`. والتجربة `experiments/latency.py` (3 cold بـ `keep_alive=0`، و preload، و 5 warm). الكود كتبه المساعد بطلب منك، وإنت شغّلت التجارب.
  - **Cold مقابل warm:** الـ load **1.57 ث** cold و **0.00** warm، والـ TTFT (load + prompt eval) **1.81 ث** مقابل **0.08 ث**. والتوليد ثابت **~28 tok/s** في الحالتين. يعني الـ load هو أغلب الـ TTFT، بس الـ eval هو أغلب الـ total.
  - **PROCESSOR:** `100% CPU` (`size_vram = 0`)، و 2.16 GB في الـ memory (الملف 1.93 GB، والفرق KV cache)، و context 4,096.
  - **Prompt caching:** نفس الـ prompt المتكرر prompt eval بتاعه نزل من 0.23 لـ 0.04 ث، و**الرد اتغيّر** (70 ← 86 token) مع إن `temperature=0`.
  - ⚠️ **`localhost` على Windows كان بيضيّع ~2 ث في كل request** (IPv6 الأول). الـ default بقى `http://127.0.0.1:11434`. ده كان جزء من بطء Step 02.
  - التفاصيل في `work/observations.md`.
- **Task 4 (2026-11-28، على الـ desktop الشخصي):** `experiments/context_memory.py` بيعمل `unload()` مرة واحدة، وبعدها لكل `context_size` في `[None, 2048, …, 32768]` بيبعت request قصير ويقرا `/api/ps` (من غير unload بين الأحجام، وده مقصود). والنتايج في `experiments/results/context_memory.json`. إنت كتبت `measure()`، والمساعد صلّح فيها سطرين وكتب `main()` والحفظ بطلب منك.
  - **الـ default الحقيقي = 4,096:** من غير `num_ctx` الحجز طلع 4,096، ونفس حجم الـ 4,096 الصريح (2.16 GB). يعني الـ FAQ وصفحة Context length صح، وصفحة الـ Modelfile (2048) غلط.
  - **الـ memory مقابل `num_ctx`:** 2.09 GB (2K) ← 2.16 (4K) ← 2.41 (8K) ← 2.73 (16K) ← **3.37 GB (32K)**، يعني **+1.28 GB** بنفس الـ prompt القصير. الزيادة خطية (~40 MB لكل 1K) وقريبة من حساب الـ KV cache (~36 KB لكل token بـ f16).
  - **PROCESSOR:** `100% CPU` و 0 VRAM في كل الأحجام، يعني **مفيش offloading** (مفيش VRAM يتعدّى). والحد عندك هو الـ RAM، و 3.37 GB بعيدة عنه جداً. والـ tok/s ثابت ~31 (الـ context محجوز بس مش مليان).
  - **تغيير الـ `num_ctx` = reload كامل** (~1.6–1.9 ث في كل سطر). ونفس الـ `num_ctx` مرتين: 1.89 ث ← 0.002 ث. يعني ثبّت رقم واحد في تطبيقك.
  - **Agent بـ 64K:** مش بـ `qwen2.5:3b` (أقصاه 32,768). الـ RAM تكفي، بس محتاج موديل تاني، وهيبقى بطيء على الـ CPU. التفاصيل في `work/observations.md`.
- **مستنيين منك:** commit و push لـ Task 4، وإجابات أسئلة Tasks 3 و 4 في وصف الـ PR.
- **الجاي:** Task 5 (Providers زي drivers Laravel).

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ✅ اتعمله merge (`5bfdb1a`) | خلصت ✅ (Tasks 0–7 + Bonus) |
| 03 — الموديلات والـ Providers | ✅ المصادر الخمسة اتشرحوا + التاسكات | ⬜ | التاسكات على Ollama local، و Claude API في Bonus بس |

## البيئة
- الأجهزة: الـ **desktop الشخصي** (i5-14600K، و 32 GB DDR5، ومن غير GPU منفصل، شوف `steps/03-models-and-providers/work/hardware.md`)، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git، فبيتعمل على كل جهاز بـ `pip install -r requirements.txt`).
- Ollama: **0.34.4**، والموديل `qwen2.5:3b` (3.1B، و `Q4_K_M`، و 1.9GB).
