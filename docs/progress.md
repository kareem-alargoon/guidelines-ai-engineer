# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 02 — الـ LLMs من منظور المستخدم 🟡
- **آخر حاجة خلصت:** **Task 3** (تجربة الـ temperature والـ seed في `work/experiments/temperature.py`): الـ 49 رد في `results/temperature.json`، والنتايج اتكتبت في `work/observations.md`. قبلها Task 2 اتعمله commit و push (`41991b6`)، ومواد Step 02 اتعملها merge في `main` (PR #6).
- **التاسكات على `work/02-llm-fundamentals`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Token counter | ✅ |
  | 2 — Sampling options و stop reason | ✅ |
  | 3 — تجربة الـ temperature والـ seed | ✅ |
  | 4 — الـ stop reasons | ⬅️ الجاي |
  | 5 – 7 | ⬜ |

- **مستنيين منك:** Task 4 في `work/experiments/stop_reasons.py`.
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
