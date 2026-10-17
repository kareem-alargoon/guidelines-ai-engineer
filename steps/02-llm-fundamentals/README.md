# Step 02 — الـ LLMs من منظور المستخدم

> **Branch المواد:** `step/02-llm-fundamentals` · **Branch شغلك:** `work/02-llm-fundamentals` · **المدة المتوقعة:** أسبوع لأسبوعين (فيديو Karpathy لوحده 3.5 ساعة)

## 🎯 بعد الخطوة دي هتقدر
- تشرح إزاي **داتا التدريب** بتحدد الموديل شاطر في إيه ووحش في إيه، وليه العربي غالباً **أغلى وأضعف** من الإنجليزي.
- تفهم الـ **transformer** والـ **attention** على مستوى الفكرة، وتربطهم بحاجات بتأثر عليك فعلاً: الـ **prefill** والـ **decode** (يعني TTFT و TPOT)، وطول الـ context، والـ memory.
- تقرا اسم موديل زي `qwen2.5:7b` أو `30B-A3B` وتعرف هو محتاج **RAM** قد إيه تقريباً، ويعني إيه **MoE**.
- تشرح الموديل اتحوّل إزاي من "بيكمّل نص" لـ "assistant بيرد عليك" (**SFT** و **preference finetuning**).
- تتحكم في الـ output بالـ **sampling**: الـ **temperature** والـ **top-k** والـ **top-p** والـ **stop conditions**، وتعرف إمتى تستخدم كل واحد.
- تطلّع **structured outputs** (JSON) يعتمد عليها، وتعرف الفرق بين الـ prompting والـ post-processing والـ constrained sampling.
- تشرح ليه الموديل **inconsistent** وليه بيعمل **hallucination**، وإيه اللي تقدر تعمله في الحالتين.
- تفهم الـ **context window** كويس: إيه اللي بيتحسب فيه، وبيحصل إيه لما يتملي.

## 📚 المصادر (بالترتيب)

| # | المصدر | النوع | الشرح | الوقت التقريبي |
|:---:|---|:---:|---|---|
| 1 | *AI Engineering* — Chip Huyen — **Ch.2**: *Understanding Foundation Models* (ص 49–112، PDF ص 73–136) | 📘 | [`notes/01-chip-huyen-ch2.md`](notes/01-chip-huyen-ch2.md) ✅ | 5–6 ساعات |
| 2 | Andrej Karpathy — [*Deep Dive into LLMs like ChatGPT*](https://www.youtube.com/watch?v=7xTGNNLPyMI) | 🎥 | ⏳ | 3.5 ساعة (على أجزاء) |
| 3 | 3Blue1Brown — [*Large Language Models explained briefly*](https://www.youtube.com/watch?v=LPZh9BOjkQs) | 🎥 | ⏳ | 8 دقايق (+ وقف وإعادة) |
| 4 | Anthropic docs — [*Context windows*](https://docs.claude.com/en/docs/build-with-claude/context-windows) | 📚 | ⏳ | نص ساعة |

✅ = الشرح جاهز · ⏳ = لسه متكتبش. بنشرح مصدر واحد في المرة، والشرح دايماً ماشي مع الأصل اللي في `resources/`، مش من الذاكرة.

### ليه المصادر دي وبالترتيب ده؟
1. **الفصل التاني من الكتاب** هو العمود الفقري: بيمشي مع رحلة الموديل كلها (داتا ← architecture ← حجم ← post-training ← sampling). أجزاء الـ architecture والـ training **برّه نطاقنا** فبنعدّي عليها على مستوى الفكرة، وبنركّز على الـ **sampling** والـ **structured outputs** والـ **hallucination**، لأنها حاجات هتتحكم فيها بإيدك في كل تطبيق.
2. **فيديو Karpathy الطويل** بيحكي نفس الرحلة بالصورة: هتشوف الـ tokenization والـ sampling بعينك، وهيدّيك تفسير تاني للـ hallucination وإزاي الموديلات بتتعلم تقول "مش عارف". اتفرّج عليه **بعد** الفصل، هتلاقي كل حاجة قريتها بقت ملموسة.
3. **فيديو 3Blue1Brown** قصير جداً، وبيوريك فكرة الـ attention والـ next-token prediction بالرسوم المتحركة. ممتاز كمراجعة بصرية.
4. **صفحة Anthropic عن الـ context windows** بتنقلك من الكلام النظري لـ API حقيقي: إيه اللي بيتحسب في الـ context، وإزاي الـ thinking والـ tools بيستهلكوه، وبيحصل إيه لما المحادثة تطول.

## 🧭 خطة المذاكرة
1. **المصدر 1:** اقرا الفصل التاني section section، وافتح الشرح بتاعه جنبه. الجدول اللي في أول ملف الشرح بيقولك أنهي أجزاء تقراها بتركيز وأنهي تقراها بسرعة.
2. **المصدر 2:** اتفرّج على فيديو Karpathy على 3–4 قعدات. لما تقابل جزء في الشرح، ارجع للـ timestamp بتاعه.
3. **المصدر 3:** اتفرّج على فيديو 3Blue1Brown كمراجعة.
4. **المصدر 4:** اقرا صفحة Anthropic والشرح بتاعها.
5. بعد كل مصدر: جاوب **أسئلة الفهم** اللي في آخر ملف الشرح **بنفسك الأول**، وبعدين افتح الإجابات.
6. حل التاسكات في `TASKS.md` (هتتكتب بعد ما نخلّص شرح المصادر الأربعة)، وافتح PR، وأنا هراجعه سطر سطر.

## ✅ Checklist
- [x] رفعت مصادر الخطوة في `resources/`
- [ ] قريت الفصل التاني + الشرح، وجاوبت أسئلة الفهم
- [ ] اتفرّجت على فيديو Karpathy + الشرح، وجاوبت أسئلة الفهم
- [ ] اتفرّجت على فيديو 3Blue1Brown + الشرح
- [ ] قريت صفحة Anthropic عن الـ context windows + الشرح
- [ ] حليت التاسكات وفتحت PR
- [ ] صلّحت ملاحظات الـ review واتعمل merge
