# شرح: LMArena (arena.ai) — How it works، و Text Leaderboard

> **المصدر:** [arena.ai](https://arena.ai/) (اسمه القديم LMArena، وقبله Chatbot Arena من LMSYS) — snapshot يوم 2026-11-13 (الـ leaderboard نفسه متحدّث يوم Nov 11, 2026)
> **الملفات:**
> - `resources/articles/03-lmarena-how-it-works.pdf` (3 صفحات)
> - `resources/articles/03-lmarena-text-leaderboard.md` (و `.pdf`، بس الـ PDF فيه أول كام صف بس، والـ `.md` هو الكامل: **421 موديل**)
>
> **إزاي تقرا:** **اقرا الملحق بتاع Ch.3 في شرح الكتاب الأول** (`01-chip-huyen-ch4-model-selection.md` جزء 7: Comparative Evaluation)، لأنه بيشرح **إزاي** الترتيب ده بيتحسب، وبعدين تعالى هنا.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

Artificial Analysis بيرتّب بـ **pointwise evaluation**: كل موديل بيتقيّم لوحده على benchmarks، وبعدين رقم. LMArena بيرتّب بـ **comparative evaluation**: ناس حقيقية بتشوف ردّين من موديلين **مجهولين** وتختار الأحسن، وبعدين **Bradley–Terry** بيطلّع ترتيب. (الاتنين اتشرحوا في الكتاب.)

يعني المصدرين دول **وجهين لنفس السؤال**: "أنهي موديل أحسن؟". وهتلاقيهم **مش متفقين** في الترتيب، وده الدرس الأهم.

| # | الصفحة | بتجاوب على |
|:---:|---|---|
| 1 | How it works | الأصوات دي بتتجمع إزاي؟ وبيحصل إيه للـ prompts بتاعتك؟ |
| 2 | Text Leaderboard | الترتيب نفسه، وإزاي تقرا كل عمود |

> ⏳ **عمر المصدر:** الـ leaderboard بيتحدّث كل كام يوم، والموديلات بتنزل وتطلع. اتعلّم **تقراه**، متحفظوش.

---

## 1. How it works
> 📍 `03-lmarena-how-it-works.pdf`

### 1.1 الـ 4 خطوات (ص 1)
1. **Input your Prompt:** تكتب prompt، وتختار الأداة المناسبة (لو عايز صورة، تختار أيقونة الصور). والصفحة بتقول صراحة: الـ prompt بتاعك **بيتجمع** عشان التقييمات العامة وتطوير الموديلات.
2. **Compare Answers:** في **battle mode** بيجيلك **ردّين من موديلين مجهولين**.
3. **Vote for the Best:** تختار الرد اللي عاجبك. صوتك بيأثر على الـ leaderboard، و**جزء من الـ feedback بتاعك بيتبعت للشركات اللي عاملة الموديلات**.
4. **Discover and Repeat:** **بعد** التصويت بس، أسماء الموديلات بتظهر. تكمّل نفس المحادثة أو تبدأ جديدة.

**ليه المجهولية مهمة؟** عشان الناس متصوّتش **للاسم** ("أنا بحب Claude" أو "أنا بحب GPT"). زي **blind taste test**: لو عارف إن الكوباية دي Pepsi، ممكن ده يأثر على رأيك.

> ⚠️ **ليك بالذات (privacy):** الـ prompts اللي بتكتبها في Arena **بتتجمع، وبتتنشر في datasets عامة** (جزء 1.3)، **وجزء منها بيروح للشركات**. **متحطش أبداً داتا حساسة أو داتا شغل** في Arena. ده عكس الـ API تماماً: في Arena إنت **بتتبرّع** بالداتا بتاعتك للتقييم.

### 1.2 Transparency & Privacy (ص 1–2)
- عندهم **Terms of Use** و **Privacy Policy** و **Leaderboard Policy** (القواعد اللي بيرتّبوا بيها).
- **من مارس 2024** بيختبروا موديلات proprietary و open source من شركات كبيرة وفرق صغيرة، ومن ضمنهم **موديلات لسه مانزلتش (pre-release)**. يعني ساعات بتصوّت على موديل محدش يعرفه لسه، والـ feedback بتاعك بيأثر على شكله لما ينزل.

**ربط بالكتاب:** الكاتبة قالت (footnote 24) إن **محاولات الغش** في Arena بتزيد كل ما يشتهر. اختبار موديلات pre-release كتير من نفس الشركة واختيار الأحسن قبل ما ينزل، ده من الحاجات اللي اتناقشت كتير كـ "ميزة غير عادلة" للشركات الكبيرة. (النقاش ده مش من الصفحة. اللي في الصفحة: فيه **Leaderboard Policy** معلنة بالقواعد، وفي جزء 1.3 فيه paper عن الـ adversarial attacks على الـ leaderboards.)

### 1.3 Open Research (ص 2)
- نشروا **أكبر مجموعة "organic human preferences"** في العالم (تفضيلات حقيقية من ناس حقيقية) كـ datasets مجانية على Hugging Face.
- ولستة papers، أهمها لينا:

| Paper | ليه يهمك |
|---|---|
| **Original Chatbot Arena paper (ICML 2024)** | الطريقة الأصلية كلها |
| **LMSYS-Chat-1M** | داتا مليون محادثة حقيقية بين ناس وموديلات. (الـ 33,000 prompt اللي الكتاب جاب منهم إحصائية الـ "hello" dataset تاني أصغر، نشرته Arena في 2023.) |
| **LLM-as-a-judge (NeurIPS 2023)** | إزاي موديل يقيّم موديل تاني (Step 14) |
| **Arena-Hard (ICML 2025)** | benchmark من **الـ prompts الصعبة** بس (حل مشكلة "الـ prompts البسيطة مش بتفرّق" اللي الكتاب قالها) |
| **RouteLLM (ICLR 2025)** | إزاي تبعت كل request للموديل المناسب (رخيص للسهل، وغالي للصعب) |
| **Exploring and Mitigating Adversarial Attacks on Leaderboards (ICML 2025)** | إزاي حد يغشّ في الـ leaderboard، وإزاي يتمنع (قلق الكاتبة!) |
| **Over-Refusal Benchmarking** | الموديلات اللي بترفض أكتر من اللازم (الـ over-censoring في محور الـ control) |
| **Style Control analysis**، و **Sentiment Control analysis** | فصل "شكل" الرد عن "محتواه" (جزء 2.4) |
| **Prompt Freshness and Benchmark** (العنوان مقطوع في الـ PDF) | من العنوان: عن الـ prompts **الجديدة** مقابل القديمة في التقييم (قريب من فكرة الـ contamination في الكتاب) |

مش مطلوب تقرا الـ papers دي. الفكرة إن **كل نقد من الكتاب** (الـ prompts البسيطة، والغش، والـ style، والـ refusal) ليه **paper بيحاول يحله**.

### 1.4 Leaderboard Rankings (ص 2–3)
فيه leaderboards كتير غير الـ text: **Overall**، و **Agent**، و **Alignment Index**، و **Text**، و **WebDev**، و Image-to-WebDev، و Text to Image، و Image Edit، و Text to Video، و **Vision**، و **Document**، و **Search**. يعني "أحسن موديل" **بيختلف حسب الـ arena**.

---

## 2. Text Leaderboard
> 📍 `03-lmarena-text-leaderboard.md`

### 2.1 شكل الصفحة
**فوق:**
- **View as: Ranking أو Pareto** ⭐: الـ Pareto view بيرسم الموديلات على محورين (الجودة مقابل التكلفة)، وده **بالظبط** الـ "mapping models along the cost-performance axes" اللي الكتاب قال عليه.
- **Categories (29):** Overall، و **Expert**، و Occupational، و **Math**، و **Instruction Following**، و **Multi-Turn**، و Creative Writing، و **Coding**، و **Hard Prompts**، و Hard Prompts (English)، و "View more" (الباقي مستخبي في الملف).
- **Adjustments:** **Style Control** و **Factuality** (و None).
- **License Type:** All، أو Proprietary، أو Open Source.
- **Ranges:** للـ score (من 953 لـ 1527)، والـ input price (لحد $75)، والـ output price (لحد $150)، والـ context (من 2K لـ 2.1M).

**الـ snapshot:** Text Arena، **Overall**، يوم **Nov 11, 2026**، **9,122,174 صوت**، و **421 موديل**.

**الأعمدة:**

| العمود | معناه |
|---|---|
| **Rank** | الترتيب |
| **Rank Spread** | **أعلى وأوطى ترتيب ممكن** الموديل يكون فيه (بسبب عدم التأكد). مثلاً "1 – 3" |
| **Model** | الاسم، وتحته **Lab · License** |
| **Score** | الـ rating (Bradley–Terry متظبّط عشان يبان زي Elo، الكتاب footnote 23)، وجنبه **± (confidence interval)**، وساعات كلمة **Preliminary** |
| **Votes** | عدد الأصوات (المقارنات) اللي الموديل دخل فيها |
| **Cost/Task (P50)** | التكلفة الوسيطة (median) للرد |
| **Price $/M** | سعر الـ input / الـ output لكل مليون token |
| **Context** | الـ context window |

### 2.2 إزاي تقرا أول الجدول
أول صفوف في الـ snapshot:

| Rank | Spread | Model | License | Score | Votes | Price $/M |
|:---:|:---:|---|---|---|---:|---|
| 1 | 1–3 | Gemini 4 Carbon (High) | Proprietary | 1526 ±10 *Preliminary* | 4,273 | $2 / $10 |
| 2 | 1–3 | Gemini 4 Argon (High) | Proprietary | 1522 ±5 | 20,779 | $2 / $10 |
| 3 | 1–8 | Muse Wonder (Max) | Proprietary | 1511 ±6 | 12,696 | $4 / $20 |
| 4 | 3–10 | Claude Opus 5.5 (High) | Proprietary | 1507 ±6 | 15,793 | $4 / $20 |
| 5 | 3–10 | Claude Fable 5 (High) | Proprietary | 1504 ±4 | 45,469 | $10 / $50 |
| 6 | 3–11 | Claude Opus 4.6 (High) | Proprietary | 1503 ±3 | 84,375 | $5 / $25 |

**الدرس 1: الـ Rank Spread والـ ± أهم من الـ Rank.**
- الأول والتاني **spread بتاعهم 1–3**، يعني **إحصائياً ممكن أي واحد فيهم يبقى الأول**. الفرق بين 1526 و 1522 (4 نقط) **أصغر من الـ ±**.
- الأول عنده **4,273 صوت بس** ومكتوب **Preliminary** (أولي) و **±10**. يعني ممكن ترتيبه يتغيّر بعد أصوات أكتر. أما Claude Opus 4.6 (High) عنده **84,375 صوت** و **±3**، يعني رقمه **أثبت** بكتير.
- **تشبيه:** زي تقييم مطعم على Google Maps: 4.9 من **12 تقييم** مش زي 4.7 من **8,000 تقييم**. التاني أوثق.

**الدرس 2: الفرق في الـ score = احتمال التفضيل.**
الـ score على مقياس شبه Elo، فالفرق بين موديلين بيتحوّل لـ **احتمال الناس تفضّل واحد على التاني** تقريباً بالمعادلة:

```
P(A يكسب B) ≈ 1 / (1 + 10^((Score_B − Score_A) / 400))
```

| المقارنة | الفرق | احتمال الأعلى يكسب |
|---|:---:|:---:|
| Gemini 4 Carbon (1526) ضد Claude Opus 5.5 (1507) | 19 | **~53%** (تقريباً زي بعض!) |
| Gemma 3 4B IT (1303) ضد Llama 3.2 3B (1167) | 136 | ~69% |
| Claude Opus 5.5 (1507) ضد Llama 3.2 3B (1167) | 340 | **~88%** |

يعني الفرق بين الأول والرابع **مش ملحوظ** في أغلب المحادثات (53/47). الفرق بين موديل frontier وموديل صغير 3B **واضح جداً**. (الأرقام دي تقريبية، بس كفاية عشان تحس بالمقياس.)

### 2.3 الـ licenses في الـ leaderboard (اختبار لكلام الكتاب)
من الـ 421 موديل:
- **191 Proprietary**، والباقي licenses **كتير جداً**: Apache 2.0 (62، ومعاها 13 مكتوبة "Apache-2.0" بشكل تاني)، و **MIT** (50)، و Modified MIT (10)، و **CC-BY-NC-4.0** (10، و **NC = Non-Commercial**!)، و Llama 2 Community (10)، و Qianwen LICENSE (8)، و Gemma license (7)، و Non-commercial (7)، و Llama 3.1 Community، و OpenMDW-1.1، و NVIDIA Open Model License، وكمان licenses **خاصة بموديل واحد** زي "Kimi K3 license".
- **ده بالظبط** اللي الكاتبة قالته: "الموديلات خلّت موضوع الـ licenses أسوأ، وكتير منها نازل بـ license خاص بيه". **لازم تقرا الـ license** قبل ما تستخدم موديل في شغل تجاري.

**أعلى موديلات مش proprietary في الـ snapshot:**

| Rank | Model | License | Score |
|:---:|---|---|:---:|
| 20 | Kimi K3 (Max) | Kimi K3 license | 1487 |
| 24 | Kimi K3.1 Pro (Max) | Kimi K3.1 Pro License | 1485 |
| 28 | GLM-5.3 (Max) | **MIT** | 1482 |
| 38 | DeepSeek-V4.1-Flash (Max) | **MIT** | 1475 |

يعني أعلى موديل مفتوح **في المركز الـ 20**، وبفرق **~40 نقطة** عن الأول (يعني الناس بتفضّل الأول عليه **حوالي 56%** من المرات). الفجوة **موجودة بس صغيرة** في التفضيل البشري. وده **نفس استنتاج** Artificial Analysis تقريباً (المفتوح ورا، بس قريب).

### 2.4 ⚠️ عيلة Qwen: نفس الاسم، licenses مختلفة
ده مثال مهم جداً **ليك** (موديلك `qwen2.5:3b`):

| Model | License | Rank | Score |
|---|---|:---:|:---:|
| Qwen2.5-Max | **Proprietary** (مقفول، API بس!) | 200 | 1374 |
| Qwen2.5-Plus (1127) | **Proprietary** | 273 | 1315 |
| Qwen2.5-72B-Instruct | **Qwen** (license خاص) | 290 | 1303 |
| Qwen2.5-Coder-32B-Instruct | **Apache 2.0** | 316 | 1271 |

**نفس العيلة (Qwen2.5)** فيها موديلات **مقفولة** ومفتوحة، والمفتوحة نفسها **بـ licenses مختلفة**. يعني **"Qwen مفتوح"** جملة غلط. لازم تبص على **الموديل بالظبط** (والحجم بالظبط). والـ 3B بتاعك **مش موجود** في الـ leaderboard، فـ license بتاعه هتعرفه من `ollama show qwen2.5:3b --license` (Task 1).

### 2.5 الموديلات الصغيرة: توقعاتك من موديل 3B
موديلك (3B) مش في الـ leaderboard، بس فيه موديلات قريبة في الحجم:

| Rank | Model | License | Score |
|:---:|---|---|:---:|
| 289 | Gemma 3 4B IT | Gemma | 1303 |
| 348 | Llama 3.1 8B Instruct | Llama 3.1 Community | 1211 |
| 374 | **Llama 3.2 3B Instruct** | Llama 3.2 | **1167** |
| 403 | Llama 3.2 1B Instruct | Llama 3.2 | 1111 |

- Llama 3.2 3B في المركز **374 من 421**، و **340 نقطة** تحت Claude Opus 5.5 (يعني الناس بتفضّل Opus **~88%** من المرات).
- **بس** Gemma 3 4B (أكبر بشوية، وأحدث) **136 نقطة** فوق Llama 3.2 3B. يعني **الجيل والتدريب بيفرقوا** مش الحجم بس (زي ما Step 02 قال: Llama 3-8B غلب Llama 2-70B).
- **الدرس:** الموديلات الصغيرة local **مش في نفس الملعب** مع الـ frontier في محادثة عامة. **بس** ده مش معناه إنها مش كفاية **لمهمة محددة** (تصنيف، استخراج، تلخيص قصير). وده اللي هتقيسه بنفسك في التاسكات.

### 2.6 الـ leaderboards مش متفقة
قارن الـ snapshot ده بـ Artificial Analysis (نفس الأسبوع):
- **AA:** الأول **Claude Fable 5.2** (index 65)، و **Gemini 4 Carbon** في المركز الرابع.
- **Arena:** الأول **Gemini 4 Carbon**، و **Claude Fable 5.2 مش موجود** في الجدول أصلاً (ممكن جديد، أو لسه مااتقيّمش، أو مش متاح في الـ arena ده).
- وفي Arena: **Claude Opus 4.6 (High)** (مركز 6، 1503) **فوق** **Claude Opus 5 (High)** (مركز 16، 1490). يعني الموديل **الأحدث** مش دايماً **المفضّل** عند الناس، رغم إنه غالباً أعلى في الـ benchmarks.

**ليه؟** لأنهم **بيقيسوا حاجات مختلفة**: AA بيقيس **قدرة على benchmarks صعبة** (pointwise)، و Arena بيقيس **تفضيل ناس عاديين في محادثات عامة** (comparative). الكتاب قالها: comparative بيقيس "human preference"، ومش بيقولك الموديل **كويس كفاية لمهمتك**. **مفيش leaderboard هو "الحقيقة"**: كل واحد **منظور**، وإنت بتاخد منه **لستة مرشحين** وتقيس بنفسك.

### 2.7 Style Control و Factuality (Adjustments)
الكتاب حذّر إن الناس في Arena ممكن **تفضّل الرد اللي شكله أحلى** (أطول، فيه markdown وعناوين وbullets) حتى لو المحتوى مش أحسن، وممكن **ميعملوش fact-check**. الـ **Adjustments** دي محاولة لحل ده:
- **Style Control:** بيحاول **يفصل أثر الشكل** (الطول والتنسيق) عن الـ score، عشان الترتيب يعكس **المحتوى** أكتر.
- **Factuality:** بيحاول يضبط الترتيب حسب **صحة المعلومات**.

> ⚠️ **الصفحات اللي بتشرح الطريقتين دول بالتفصيل مش من اللي رفعتها** (فيه لينكات لـ blog posts في الصفحة). فخد الفكرة بس: **الترتيب بيتغيّر حسب الـ adjustment**، وده يأكد إن "الترتيب" نفسه **قرار منهجي**، مش حقيقة ثابتة. جرّب تغيّر الـ adjustment في الموقع وشوف الترتيب بيتحرك.

### 2.8 الـ Win-rate plot (آخر الصفحة)
تحت الجدول فيه رسمة: **"Fraction of Model A Wins in A vs. B Battles (Ties Excluded)"**: مصفوفة لأعلى الموديلات، كل خلية = **نسبة المرات اللي موديل الصف كسب فيها موديل العمود** (من غير التعادل). ده **بالظبط Table 3-6** في الكتاب (الـ win rates بين 5 موديلات)، بس بأرقام حقيقية. في الملف هتلاقي الأرقام (زي 0.55، و 0.60، و 0.63) من غير أسماء واضحة لكل خلية، فبص عليها في الموقع.

### 2.9 حجم الأصوات مقارنة بالكتاب
- **الكتاب (يناير 2024):** 57 موديل، و 244,000 مقارنة، يعني ~153 مقارنة لكل **زوج** موديلات.
- **الـ snapshot (نوفمبر 2026):** 421 موديل، و 9,122,174 صوت. عدد الأزواج = 421 × 420 / 2 = **88,410 زوج**، يعني **~103 صوت لكل زوج** في المتوسط.
- يعني رغم إن الأصوات زادت **37 مرة**، **مشكلة الـ scalability اللي الكتاب قالها لسه موجودة** (عدد الأزواج بيزيد تربيعياً). عشان كده الـ **Rank Spread** واسع لكتير من الموديلات، وعشان كده بيستخدموا **matching ذكي** و **transitivity** (الكتاب جزء 7.4).

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md) تحت "Step 03 (المصدر 5)":
**Battle Mode (Blind Pairwise Comparison)** · **Confidence Interval و Rank Spread** (ومعاه الـ Preliminary) · **Score Difference → Win Probability** · **Style Control** · **Category Leaderboards** · **Pareto View (Quality vs Cost)**

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. ليه الموديلات في Arena مجهولة لحد ما تصوّت؟</summary>

عشان الـ **brand bias**: لو المستخدم عارف إن الرد ده من Claude أو GPT، ممكن يصوّت للاسم اللي بيحبه مش للرد الأحسن. المجهولية بتخلّي التصويت على **الرد نفسه** (زي blind taste test). وبتصعّب الغش شوية (لازم تعرف الرد ده بتاع مين عشان تصوّتله).
</details>

<details><summary>2. موديل A بـ score 1526 ±10 و 4,273 صوت و Preliminary، وموديل B بـ 1522 ±5 و 20,779 صوت. مين الأحسن؟</summary>

**مقدرش أقول.** الفرق (4 نقط) أصغر بكتير من الـ confidence intervals، والـ rank spread بتاع الاتنين **1–3**. يعني إحصائياً هما **متعادلين**. وكمان A **preliminary** بأصوات قليلة، فرقمه ممكن يتحرك أكتر. B **أثبت**. ولو حتى الفرق حقيقي، 4 نقط = تقريباً **50.6%** احتمال تفضيل، يعني مش ملحوظ عملياً. لازم أقيس على مهمتي.
</details>

<details><summary>3. حوّل فرق 340 نقطة في الـ score لاحتمال تقريبي. وإيه اللي الرقم ده مش بيقولهولك؟</summary>

`P ≈ 1 / (1 + 10^(−340/400)) ≈ 1 / (1 + 0.14) ≈ 88%`. يعني الناس بتفضّل الموديل الأعلى في **~88%** من المقارنات.
مش بيقولي: إن الموديل الأوطى **مش كفاية** لمهمتي (comparative مش absolute)، ولا إن الفرق ده هيبقى نفسه في **مهمتي المحددة** (الـ prompts في Arena عامة)، ولا إنه **يستاهل فرق السعر**.
</details>

<details><summary>4. ليه AA و LMArena مش متفقين على الأول؟</summary>

لأنهم **بيقيسوا حاجات مختلفة بطرق مختلفة**: AA **pointwise** على benchmarks صعبة (reasoning، و coding، و agents...) وبيجمّعهم في index. Arena **comparative** من تفضيل ناس عاديين على prompts بيكتبوها (كتير منها بسيط، وفيه أثر للأسلوب والطول). وكمان **التغطية مختلفة**: موديل ممكن يكون في واحد ومش في التاني (Fable 5.2 في الـ snapshot). الاتنين مفيدين **للتضييق**، ولا واحد فيهم بيقرر بدالي.
</details>

<details><summary>5. ليه Claude Opus 4.6 ممكن يبقى فوق Claude Opus 5 في Arena رغم إنه أقدم؟</summary>

احتمالات: (1) Arena بيقيس **تفضيل الناس** في محادثات عامة، والموديل الأحدث ممكن يكون اتحسّن في حاجات (agents، و coding طويل، و reasoning صعب) **مبتظهرش** في prompts الناس العادية، أو أسلوبه اتغيّر بشكل الناس حبّته أقل. (2) **الفرق صغير** (1503 مقابل 1490، يعني ~52%)، والـ rank spreads متداخلة، فممكن يكون عملياً **تعادل**. ده مثال على كلام الكتاب: **نفس التحديث ممكن يحسّن حاجات ويبوّظ حاجات** (Voiceflow و GoDaddy).
</details>

<details><summary>6. إيه اللي الـ licenses في الـ leaderboard بتقولهولك عن جملة "Qwen موديل مفتوح"؟</summary>

إنها **غلط** كتعميم. نفس العيلة (Qwen2.5) فيها **Qwen2.5-Max** و **Qwen2.5-Plus** وهما **proprietary** (API بس)، و **Qwen2.5-72B-Instruct** بـ license خاص اسمه "Qwen"، و **Qwen2.5-Coder-32B** بـ **Apache 2.0**. يعني لازم أتأكد من الـ license **للموديل والحجم بالظبط** اللي هستخدمه، مش من اسم العيلة. وده سبب `ollama show <model> --license`.
</details>

<details><summary>7. إيه فايدة الـ Style Control؟ وليه وجوده نفسه درس؟</summary>

الناس بتميل تفضّل الردود **الأطول والمتنسّقة** (عناوين، و bullets، و markdown) حتى لو المحتوى مش أحسن. الـ Style Control بيحاول يشيل أثر الشكل ده من الـ score، فالترتيب يعكس **المحتوى** أكتر.
الدرس: إن **الترتيب بيتغيّر حسب الـ methodology**. مفيش "ترتيب حقيقي واحد". كل leaderboard عامل **اختيارات** (أنهي prompts، وأنهي adjustments، وأنهي algorithm)، وكل اختيار بيغيّر النتيجة. زي ما الكتاب قال على HF و HELM.
</details>

<details><summary>8. ليه متكتبش داتا شغلك في Arena عشان تقارن الموديلات عليها؟</summary>

لأن الـ prompts في Arena **بتتجمع وبتتنشر** في datasets عامة، و**جزء منها بيروح لشركات الموديلات**. يعني داتا الشغل هتبقى **public** وممكن تدخل في تدريب موديلات (فتتسرّب بعدين، زي StarCoder اللي حافظ 8% من داتاه). لو عايز أقارن موديلات على داتا حساسة: أعمل eval set **عندي** وأشغّله على الموديلات (local بـ Ollama، أو APIs بعقود واضحة عن الـ data retention).
</details>

<details><summary>9. الـ Arena فيه 9 مليون صوت. ليه لسه فيه موديلات الـ rank spread بتاعها واسع (مثلاً 9–50)؟</summary>

لأن عدد **الأزواج** بيزيد **تربيعياً** مع عدد الموديلات: 421 موديل = 88,410 زوج، يعني ~103 صوت لكل زوج في المتوسط، وموديلات جديدة أو أقل شعبية بتاخد أصوات **أقل بكتير** (Kimi K3.1 Pro عنده 3,995 صوت بس ورتبته ممكن تبقى من 9 لـ 50). ده نفس **scalability bottleneck** اللي الكتاب شرحه، والحل الجزئي: matching ذكي (تقارن الأزواج اللي بتقلل الشك أكتر) و transitivity.
</details>

<details><summary>10. ازاي تستخدم Arena صح كـ AI Engineer بيختار موديل؟</summary>

(1) أختار **الـ category** الأقرب لمهمتي (Coding، أو Instruction Following، أو Multi-Turn، أو Hard Prompts)، مش Overall. (2) أفلتر بالـ **License Type** لو محتاج open weights. (3) أبص على **Score ± CI و Rank Spread و Votes**، مش الـ rank بس. (4) أستخدم الـ **Pareto view** عشان أشوف الجودة مقابل السعر. (5) أطلّع **2–3 مرشحين**، وأقارنهم بـ AA (منظور تاني). (6) أقيس المرشحين **على eval set بتاعي** (الخطوة 3 في الـ workflow). ومحطش داتا حساسة في Arena نفسه.
</details>
