# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 02 — الـ LLMs من منظور المستخدم 🟡
- **آخر حاجة خلصت:** **Task 5** (structured outputs في `work/experiments/structured.py`): 3 طرق (prompt بس، وprompt + تنضيف بـ regex، وschema في `format` بتاع Ollama متولّد من `Order`)، 10 رسايل × 3 طرق × 3 مرات على T=0.7. الشكل: 93% → **100%** في الطريقتين 2 و 3. الداتا الصح: **30–33%** في التلاتة، يعني الـ schema بيضمن الشكل مش الصح. الداتا في `work/data/orders.json`، والنتايج في `results/structured.json` و `work/observations.md`. وده حل سؤال `ok: 1 items` من Task 4. قبلها Task 4 (الـ stop reasons) اتعمله commit و push (`aa5ee9d`).
- **التاسكات على `work/02-llm-fundamentals`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Token counter | ✅ |
  | 2 — Sampling options و stop reason | ✅ |
  | 3 — تجربة الـ temperature والـ seed | ✅ |
  | 4 — الـ stop reasons | ✅ |
  | 5 — Structured outputs: 3 طرق ومقارنة | ✅ |
  | 6 — Self-consistency و "Models need tokens to think" | ⬅️ الجاي |
  | 7 | ⬜ |

- **مستنيين منك:** إجابة سؤال التفكير بتاع Task 5 (هتتكتب في الـ PR)، وبعدها Task 6.
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
