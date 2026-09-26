# Step 01 — مقدمة: يعني إيه AI Engineering

> **Branch المواد:** `step/01-introduction` · **Branch شغلك:** `work/01-introduction` · **المدة المتوقعة:** أسبوع تقريباً

## 🎯 بعد الخطوة دي هتقدر
- تشرح يعني إيه **foundation model** و **LLM**، وإزاي وصلنا لهنا.
- تشرح يعني إيه **AI Engineering**، وإيه الفرق بينه وبين ML Engineering و full-stack engineering.
- تعرف أشهر **use cases** للـ AI، وإزاي تقيّم فكرة: تنفع تبقى AI app ولا لأ.
- تعرف طبقات الـ **AI engineering stack**: application، model، infrastructure.
- تشرح الـ LLM بيشتغل إزاي "من برّه": ليه بيعمل **hallucination**، وليه **stateless**، وإيه مخاطره الأمنية.
- تكلّم **LLM شغّال على جهازك** (Ollama) من كود Python **كتبته بإيدك**.

## 📚 المصادر (بالترتيب)

| # | المصدر | النوع | الشرح | الوقت التقريبي |
|:---:|---|:---:|---|---|
| 1 | *AI Engineering* — Chip Huyen — **Ch.1**: *Introduction to Building AI Applications with Foundation Models* (ص 1–48، PDF ص 25–72) | 📘 | [`notes/01-chip-huyen-ch1.md`](notes/01-chip-huyen-ch1.md) ✅ | 3–4 ساعات |
| 2 | Andrej Karpathy — [*Intro to Large Language Models*](https://www.youtube.com/watch?v=zjkBMFhNj_g) | 🎥 | [`notes/02-karpathy-intro-to-llms.md`](notes/02-karpathy-intro-to-llms.md) ✅ | ساعة (+ وقف وإعادة) |
| 3 | swyx — [*The Rise of the AI Engineer*](https://www.latent.space/p/ai-engineer) | 📰 | [`notes/03-swyx-rise-of-the-ai-engineer.md`](notes/03-swyx-rise-of-the-ai-engineer.md) ✅ | نص ساعة |

✅ = الشرح جاهز · ⏳ = لسه متكتبش. بنشرح مصدر واحد في المرة، والشرح دايماً ماشي مع الأصل اللي في `resources/`، مش من الذاكرة.

### ليه المصادر دي وبالترتيب ده؟
1. **الفصل الأول من الكتاب** بيحط الإطار كله: الـ foundation models جات منين، والـ AI Engineering يعني إيه، والـ use cases، وإزاي تخطط لـ AI app. ده الأساس اللي باقي الكتاب والـ roadmap مبنيين عليه.
2. **فيديو Karpathy** (من المؤسسين بتوع OpenAI، وكان مسؤول الـ AI في Tesla) بيوريك الـ LLM من جوّه بشكل مبسّط: هو عبارة عن إيه، واتدرّب إزاي، وليه بيعمل hallucination، وإيه مخاطره الأمنية. ده بيخلّي كلام الكتاب ملموس.
3. **مقال swyx** هو المقال اللي سمّى وظيفة "AI Engineer" سنة 2023. قصير، وبيوضّح ليه الوظيفة دي ظهرت ومكانها فين بين الـ ML Engineer والـ software engineer.

## 🧭 خطة المذاكرة
1. **المصدر 1:** اقرا الفصل الأول من الكتاب section section، وافتح الشرح بتاعه جنبه.
2. **المصدر 2:** اتفرّج على الفيديو. لما تقابل جزء في الشرح، ارجع للـ timestamp بتاعه.
3. **المصدر 3:** اقرا المقال والشرح بتاعه.
4. بعد كل مصدر: جاوب **أسئلة الفهم** اللي في آخر ملف الشرح **بنفسك الأول**، وبعدين افتح الإجابات.
5. حل التاسكات في [`TASKS.md`](TASKS.md). تقدر تبدأ Task 0 و 1 و 2 من دلوقتي لأنهم مش معتمدين على الشرح.
6. افتح PR بشغلك، وأنا هراجعه سطر سطر.

## ✅ Checklist
- [ ] رفعت مصادر الخطوة في `resources/`
- [ ] قريت الفصل الأول + الشرح، وجاوبت أسئلة الفهم
- [ ] اتفرّجت على فيديو Karpathy + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت مقال swyx + الشرح
- [ ] حليت التاسكات وفتحت PR
- [ ] صلّحت ملاحظات الـ review واتعمل merge
