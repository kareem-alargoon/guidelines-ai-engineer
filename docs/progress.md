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
  | 0 — تجهيز الخطوة | ⬜ |
  | 1 — Model card من Ollama | ⬜ |
  | 2 — قارئ الـ leaderboard | ⬜ |
  | 3 — الوقت بيروح فين؟ (cold start و keep_alive) | ⬜ |
  | 4 — الـ context بياكل memory | ⬜ |
  | 5 — Providers زي drivers Laravel | ⬜ |
  | 6 — Mini eval: الموديل الـ local كفاية؟ | ⬜ |
  | 7 — التكلفة والقرار | ⬜ |

- **مستنيين منك:** commit و push لمواد Step 03 وتفتح PR (`step/03-models-and-providers`)، وبعد الـ merge تبدأ المذاكرة. وفي Task 0 ابعتلي مواصفات جهازك (CPU، و RAM، و GPU و VRAM).
- **الجاي:** تذاكر بخطة القعدات في `steps/03-models-and-providers/README.md`، وتحل التاسكات على `work/03-models-and-providers`.

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ✅ اتعمله merge (`dc3394f`) | خلصت ✅ (Tasks 0–7 + Bonus) |
| 03 — الموديلات والـ Providers | ✅ المصادر الخمسة اتشرحوا + التاسكات | ⬜ | التاسكات على Ollama local، و Claude API في Bonus بس |

## البيئة
- الأجهزة: اللاب الشخصي، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git، فبيتعمل على كل جهاز بـ `pip install -r requirements.txt`).
- Ollama: **0.34.4**، والموديل `qwen2.5:3b` (3.1B، و `Q4_K_M`، و 1.9GB).
