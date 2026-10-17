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
| 2 | Andrej Karpathy — [*Deep Dive into LLMs like ChatGPT*](https://www.youtube.com/watch?v=7xTGNNLPyMI) | 🎥 | [`notes/02-karpathy-deep-dive-into-llms.md`](notes/02-karpathy-deep-dive-into-llms.md) ✅ | 3.5 ساعة (على 3 قعدات) |
| 3 | 3Blue1Brown — [*Large Language Models explained briefly*](https://www.youtube.com/watch?v=LPZh9BOjkQs) | 🎥 | [`notes/03-3blue1brown-llms-explained-briefly.md`](notes/03-3blue1brown-llms-explained-briefly.md) ✅ | 8 دقايق (+ وقف وإعادة) |
| 4 | Anthropic docs — [*Context windows*](https://docs.claude.com/en/docs/build-with-claude/context-windows) | 📚 | [`notes/04-anthropic-context-windows.md`](notes/04-anthropic-context-windows.md) ✅ | نص ساعة |

✅ = الشرح جاهز. كل مصادر الخطوة متشرحة، والشرح دايماً ماشي مع الأصل اللي في `resources/`، مش من الذاكرة. والتاسكات جاهزة في [`TASKS.md`](TASKS.md).

### ليه المصادر دي وبالترتيب ده؟
1. **الفصل التاني من الكتاب** هو العمود الفقري: بيمشي مع رحلة الموديل كلها (داتا ← architecture ← حجم ← post-training ← sampling). أجزاء الـ architecture والـ training **برّه نطاقنا** فبنعدّي عليها على مستوى الفكرة، وبنركّز على الـ **sampling** والـ **structured outputs** والـ **hallucination**، لأنها حاجات هتتحكم فيها بإيدك في كل تطبيق.
2. **فيديو Karpathy الطويل** بيحكي نفس الرحلة بالصورة: هتشوف الـ tokenization والـ sampling بعينك، وهيدّيك تفسير تاني للـ hallucination وإزاي الموديلات بتتعلم تقول "مش عارف". اتفرّج عليه **بعد** الفصل، هتلاقي كل حاجة قريتها بقت ملموسة.
3. **فيديو 3Blue1Brown** قصير جداً، وبيوريك فكرة الـ attention والـ next-token prediction بالرسوم المتحركة. ممتاز كمراجعة بصرية.
4. **صفحة Anthropic عن الـ context windows** بتنقلك من الكلام النظري لـ API حقيقي: إيه اللي بيتحسب في الـ context، وإزاي الـ thinking والـ tools بيستهلكوه، وبيحصل إيه لما المحادثة تطول.

## 🧭 خطة المذاكرة
**طريقة كل قعدة:** اقرا (أو اتفرّج على) الجزء في الأصل الأول، وبعدين افتح شرحه. وفي الآخر جاوب **أسئلة الفهم** بنفسك قبل ما تفتح الإجابات. والتاسكات بتتحل **وإنت ماشي**: كل تاسك مكتوب جنبها الجزء اللي لازم تكون خلّصته.

| القعدة | تذاكر إيه | الوقت | التاسكات اللي تقدر تعملها بعدها |
|:---:|---|---|---|
| 1 | Ch.2: المقدمة + *Training Data* (PDF ص 73–81) | ساعة | Task 0 (تجهيز) |
| 2 | Ch.2: *Modeling* (PDF ص 82–101): اقرا الشرح الأول، وعدّي المعادلات | ساعة | — |
| 3 | Ch.2: *Post-Training* (PDF ص 102–112) | 45 دقيقة | — |
| 4 | Karpathy: الجزء 1 (0:00–1:00) + 3Blue1Brown كله | ساعة ونص | **Task 1** (tokens) |
| 5 | Ch.2: *Sampling* لحد آخر *Test Time Compute* (PDF ص 112–123) | ساعة ونص | **Task 2، 3، 4** |
| 6 | Ch.2: *Structured Outputs* لآخر الفصل (PDF ص 123–136) | ساعة ونص | **Task 5** |
| 7 | Karpathy: الجزء 2 (1:00–2:10) | ساعة ونص | — |
| 8 | Karpathy: الجزء 3 (2:10–3:31) | ساعة ونص | **Task 6** |
| 9 | Anthropic docs: *Context windows* | نص ساعة | **Task 7** |

- القعدات 5 و 6 و 7 أهم حاجة في الخطوة، خد وقتك فيهم.
- لما تبدأ تاسك: قولّي "Task N"، وهنمشي فيها **خطوة خطوة** زي Step 01. ولو التاسك محتاجة ملف داتا، أنا اللي هكتبه.
- في الآخر: افتح PR بشغلك على `work/02-llm-fundamentals`، وأنا هراجعه سطر سطر.

## ✅ Checklist
- [x] رفعت مصادر الخطوة في `resources/`
- [ ] قريت الفصل التاني + الشرح، وجاوبت أسئلة الفهم
- [ ] اتفرّجت على فيديو Karpathy + الشرح، وجاوبت أسئلة الفهم
- [ ] اتفرّجت على فيديو 3Blue1Brown + الشرح
- [ ] قريت صفحة Anthropic عن الـ context windows + الشرح، وجاوبت أسئلة الفهم
- [ ] حليت التاسكات وفتحت PR
- [ ] صلّحت ملاحظات الـ review واتعمل merge
