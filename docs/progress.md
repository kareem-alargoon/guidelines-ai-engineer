# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 02 — الـ LLMs من منظور المستخدم 🟡
- **آخر حاجة خلصت:** **Task 2** (sampling options و `stop_reason` في `llm_client.py`) اتراجع واتعمله commit و push (`41991b6`). مواد Step 02 اتعملها merge في `main` (PR #6).
- **التاسكات على `work/02-llm-fundamentals`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Token counter | ✅ |
  | 2 — Sampling options و stop reason | ✅ |
  | 3 — تجربة الـ temperature والـ seed | ⬅️ الجاي |
  | 4 – 7 | ⬜ |

- **مستنيين منك:** Task 3 في `work/experiments/temperature.py`. لما تخلص ابعت الـ JSON، وأنا أكتب `observations.md`.
- **الجاي:** بعد Task 7 تفتح PR لـ `work/02-llm-fundamentals` وأراجعه. وبعد الـ merge، Step 02 تبقى ✅ ونبدأ Step 03.

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ⬜ | التاسكات كلها على Ollama local |

## البيئة
- الأجهزة: اللاب الشخصي، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git، فبيتعمل على كل جهاز بـ `pip install -r requirements.txt`).
- Ollama: الموديل `qwen2.5:3b`.
