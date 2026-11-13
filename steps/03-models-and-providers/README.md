# Step 03 — الموديلات والـ Providers (Cloud vs Local)

> **Branch المواد:** `step/03-models-and-providers` · **Branch شغلك:** `work/03-models-and-providers` · **المدة المتوقعة:** أسبوع لأسبوعين

## 🎯 بعد الخطوة دي هتقدر
- تختار موديل لتطبيق **بخطوات واضحة** (الـ workflow بتاع الكتاب): تفلتر بالـ **hard attributes**، وتضيّق بالـ **leaderboards**، وتقرر بـ **eval set بتاعك**.
- تقرر **API ولا self-hosting** بالـ 7 محاور: privacy، و data lineage، و performance، و functionality، و cost، و control، و on-device.
- تقرا **model license** وتعرف إمتى يمنعك من الاستخدام التجاري (ومتفترضش إن "open" = "تعمل اللي إنت عايزه").
- تشغّل موديلات **local بـ Ollama صح**: تعرف الموديل بياخد memory قد إيه، وشغّال على GPU ولا CPU، وليه أول request بطيء، وإزاي الـ context بياكل RAM.
- تبني **abstraction للـ providers** زي drivers بتوع Laravel (`LLM_PROVIDER=ollama`)، وتستخدم **OpenAI-compatible API**.
- تقرا **Artificial Analysis** و **LMArena** صح: cost per task، و TTFAT، و confidence intervals، و rank spread، وليه الاتنين مش متفقين.
- تحسب **تكلفة تطبيق حقيقي** على Claude API (input/output، و caching، و batch، و data residency)، وتعرف **الموديل بيعيش قد إيه** قبل ما يتشال.

## 📚 المصادر (بالترتيب)

| # | المصدر | النوع | الشرح | الوقت التقريبي |
|:---:|---|:---:|---|---|
| 1 | *AI Engineering* — Chip Huyen — **Ch.4**: *Model Selection* + *Cost and Latency* (ص 159–161 و 177–200، PDF ص 183–185 و 201–224) + 📎 **Ch.3**: *Comparative Evaluation* (ص 148–156، PDF ص 172–180) | 📘 | [`notes/01-chip-huyen-ch4-model-selection.md`](notes/01-chip-huyen-ch4-model-selection.md) ✅ | 4–5 ساعات |
| 2 | [Ollama docs](https://docs.ollama.com/) — 10 صفحات (Quickstart، و Windows، و CLI، و FAQ، و Context length، و Hardware، و Modelfile، و Import، و OpenAI compatibility، و Cloud) | 📚 | [`notes/02-ollama-docs.md`](notes/02-ollama-docs.md) ✅ | 3 ساعات |
| 3 | [Anthropic docs](https://platform.claude.com/docs/en/about-claude/models/overview) — Models overview، و Choosing a model، و Pricing، و Model deprecations | 📚 | [`notes/03-anthropic-models-and-pricing.md`](notes/03-anthropic-models-and-pricing.md) ✅ | ساعتين |
| 4 | [Artificial Analysis](https://artificialanalysis.ai/) — Methodology، و LLM Leaderboard، و API Providers | 📰 | [`notes/04-artificial-analysis.md`](notes/04-artificial-analysis.md) ✅ | ساعة ونص |
| 5 | [LMArena (arena.ai)](https://arena.ai/) — How it works، و Text Leaderboard | 📰 | [`notes/05-lmarena.md`](notes/05-lmarena.md) ✅ | ساعة |

✅ = الشرح جاهز. كل مصادر الخطوة متشرحة من الملفات اللي في `resources/` (مش من الذاكرة). والتاسكات في [`TASKS.md`](TASKS.md).

### ليه المصادر دي وبالترتيب ده؟
1. **الكتاب** هو الإطار: إزاي تفكّر في الاختيار (hard/soft attributes، والـ workflow، و build vs buy، وليه متصدّقش الـ benchmarks). والملحق من Ch.3 بيشرح **الـ comparative evaluation** اللي LMArena مبني عليها. اقراه الأول، لأن كل المصادر الجاية **أمثلة حية** على كلامه.
2. **Ollama docs** = ناحية الـ **self-hosting** بالتفصيل: memory، و GPU/CPU، و cold start، و Modelfile، و OpenAI compatibility. وكمان **Ollama Cloud**، اللي بيوريك إن "cloud vs local" بقى سؤال عن **مكان الـ inference** مش عن الأداة.
3. **Anthropic docs** = ناحية الـ **API** بأرقام حقيقية: الـ tiers، والأسعار (caching، و batch، و data residency)، والـ deprecations (محور الـ control في الكتاب).
4. **Artificial Analysis** = leaderboard **pointwise**: ذكاء + سعر + سرعة + latency، ونفس الموديل عند providers مختلفين.
5. **LMArena** = leaderboard **comparative** من تفضيل الناس. آخر واحد لأنك محتاج الملحق بتاع Ch.3 والـ AA عشان تقارن.

> ⏳ **تنبيه:** مصادر 2 لـ 5 snapshot يوم **2026-11-13**. الموديلات والأسعار والترتيب بتتغيّر كل كام أسبوع. **اتعلّم شكل القرار والمقاييس، مش الأرقام.**

## 🧭 خطة المذاكرة
**طريقة كل قعدة:** اقرا الجزء في الأصل، وبعدين شرحه. وفي الآخر جاوب **أسئلة الفهم** بنفسك قبل ما تفتح الإجابات. والتاسكات بتتحل **وإنت ماشي**.

| القعدة | تذاكر إيه | الوقت | التاسكات اللي تقدر تعملها بعدها |
|:---:|---|---|---|
| 1 | Ch.4: المقدمة + *Cost and Latency* + *Model Selection* + *Workflow* (PDF ص 183–185 و 201–205) | ساعة | **Task 0** |
| 2 | Ch.4: *Build Versus Buy* لآخر Table 4-4 (PDF ص 205–215) | ساعة ونص | **Task 1** |
| 3 | Ch.4: *Navigate Public Benchmarks* لآخر الـ contamination (PDF ص 215–224) | ساعة | — |
| 4 | Ch.3 الملحق: *Comparative Evaluation* (PDF ص 172–180) | 45 دقيقة | — |
| 5 | Artificial Analysis (الـ 3 صفحات) + LMArena (الصفحتين) | ساعتين ونص | **Task 2** |
| 6 | Ollama: Quickstart، و Windows، و CLI، و FAQ (لحد 4.11 keep_alive) | ساعة ونص | **Task 3** |
| 7 | Ollama: باقي الـ FAQ، و Context length، و Hardware | ساعة | **Task 4** |
| 8 | Ollama: Modelfile، و Import، و OpenAI compatibility، و Cloud | ساعة ونص | **Task 5** |
| 9 | Anthropic: Models overview + Choosing a model | ساعة | **Task 6** |
| 10 | Anthropic: Pricing + Model deprecations | ساعة | **Task 7** |

- القعدات 2 و 5 و 6 أهم حاجة في الخطوة.
- لما تبدأ تاسك: قولّي "Task N"، وهنمشي فيها **خطوة خطوة**. ولو التاسك محتاجة ملف داتا (`receipts.json`، و `prices.json`)، أنا اللي هكتبه.
- **التاسكات كلها على `qwen2.5:3b` اللي عندك.** فيه موديلات تانية **اختيارية** في Task 6، وحجمها مكتوب جنبها. **متنزّلش حاجة قبل ما تقولّي.**
- **مفيش تاسك أساسية محتاجة Claude API key.** فيه Bonus واحد بس لو عندك key (قولّي الأول).
- في الآخر: افتح PR بشغلك على `work/03-models-and-providers`، وأنا هراجعه.

## ✅ Checklist
- [x] رفعت مصادر الخطوة في `resources/`
- [ ] قريت Ch.4 (Model Selection) + الملحق من Ch.3 + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت صفحات Ollama العشرة + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت صفحات Anthropic الأربعة + الشرح، وجاوبت أسئلة الفهم
- [ ] قريت Artificial Analysis و LMArena + الشرح، وجاوبت أسئلة الفهم
- [ ] حليت التاسكات وفتحت PR
- [ ] صلّحت ملاحظات الـ review واتعمل merge
