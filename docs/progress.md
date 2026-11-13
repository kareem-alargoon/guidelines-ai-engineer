# إحنا فين دلوقتي؟ (Progress)

> بيتحدّث بعد كل خطوة وبعد كل review.

## الحالة الحالية
- **الخطوة الحالية:** 02 — الـ LLMs من منظور المستخدم 🟡
- **آخر حاجة خلصت:** **Task 7** (chat CLI في `work/chat_cli.py`): `context_size` (`num_ctx`) في `llm_client.py`، و system message ثابت، وتنبيه عند 80%، و `trim_history` (sliding window) مع أمر `/trim N` و tests في `work/test_trim.py`. التجربة على `num_ctx=512`: من غير trim، Ollama **شال رسالة الاسم بصمت** (الـ `in` قلّ من 427 لـ 378 والمحادثة بتكبر، ومفيش error)، والموديل قال "ملقيتش المعلومة" مش "نسيت". بـ `/trim 4` الاستهلاك ثبت عند ~40%، والاسم اتنسي برضه بس بقرارنا. الـ system message فضل في الحالتين. اللوجات في `results/truncation_*.md`، والـ observations في `work/observations.md`. الـ Bonus (`/summarize`) لسه متعملش. وقبلها **Task 6** (self-consistency في `work/experiments/self_consistency.py`): 10 مسائل حساب بالعامية × 4 إعدادات (120 request). direct ×1 = **3/10**، و reasoning ×1 = **9/10** (~16× tokens)، و direct ×5 + vote = **2/10**، و reasoning ×5 + vote = **9/10** (~90× tokens). يعني التفكير هو اللي فرق، والتصويت بيصلّح الغلط العشوائي بس، مش الـ systematic (المسألة 6 غلط في كل الإعدادات). الداتا في `work/data/math_problems.json`، والنتايج في `results/self_consistency.json` و `work/observations.md`. مقارنة `qwen2.5:7b` اتسابت (مش متسطّب). وقبلها **Task 5** (structured outputs في `work/experiments/structured.py`): 3 طرق (prompt بس، وprompt + تنضيف بـ regex، وschema في `format` بتاع Ollama متولّد من `Order`)، 10 رسايل × 3 طرق × 3 مرات على T=0.7. الشكل: 93% → **100%** في الطريقتين 2 و 3. الداتا الصح: **30–33%** في التلاتة، يعني الـ schema بيضمن الشكل مش الصح. الداتا في `work/data/orders.json`، والنتايج في `results/structured.json` و `work/observations.md`. وده حل سؤال `ok: 1 items` من Task 4. قبلها Task 4 (الـ stop reasons) اتعمله commit و push (`aa5ee9d`).
- **التاسكات على `work/02-llm-fundamentals`:**

  | Task | الحالة |
  |---|:---:|
  | 0 — تجهيز الخطوة | ✅ |
  | 1 — Token counter | ✅ |
  | 2 — Sampling options و stop reason | ✅ |
  | 3 — تجربة الـ temperature والـ seed | ✅ |
  | 4 — الـ stop reasons | ✅ |
  | 5 — Structured outputs: 3 طرق ومقارنة | ✅ |
  | 6 — Self-consistency و "Models need tokens to think" | ✅ |
  | 7 — Chat CLI بيدير الـ context window | ✅ (الـ Bonus `/summarize` اختياري ولسه) |

- **مستنيين منك:** commit لـ Task 7، وإجابة سؤال التفكير بتاع Task 5 (هتتكتب في الـ PR).
- **الجاي:** تعمل push وتفتح PR لـ `work/02-llm-fundamentals` وأراجعه. وبعد الـ merge، Step 02 تبقى ✅ ونبدأ Step 03.

## سجل الخطوات
| الخطوة | المواد (notes + tasks) | شغلك (PR) | ملاحظات |
|---|:---:|:---:|---|
| 01 — مقدمة | ✅ المصادر التلاتة اتشرحوا | ✅ اتعمله merge | خلصت ✅ |
| 02 — الـ LLMs من منظور المستخدم | ✅ المصادر الأربعة اتشرحوا + التاسكات | ⬜ | التاسكات كلها على Ollama local |

## البيئة
- الأجهزة: اللاب الشخصي، ولاب الشركة (من 2026-11-09). الاتنين Windows 11 + PyCharm.
- Python: 3.13، و venv لكل خطوة في `steps/NN-name/work/.venv` (مش على الـ git، فبيتعمل على كل جهاز بـ `pip install -r requirements.txt`).
- Ollama: الموديل `qwen2.5:3b`.
