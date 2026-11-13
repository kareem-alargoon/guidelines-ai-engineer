# شرح: Artificial Analysis — Methodology، و LLM Leaderboard، و API Providers Leaderboard

> **المصدر:** [Artificial Analysis](https://artificialanalysis.ai/) — snapshot يوم 2026-11-13
> **الملفات:**
> - `resources/articles/03-artificial-analysis-methodology.md` (و `.pdf`)
> - `resources/articles/03-artificial-analysis-leaderboard.md` (و `.pdf`، بس الـ PDF فيه أول 15 صف بس، فالـ `.md` هو الكامل: **288 موديل**)
> - `resources/articles/03-artificial-analysis-providers.md` (و `.pdf`، والـ `.md` فيه **525 endpoint**)
>
> **إزاي تقرا:** ابدأ بالـ methodology (التعريفات)، وبعدين الـ leaderboard، وبعدين الـ providers. ملفات الـ `.md` طويلة لأن كل خلية في الجدول في سطر لوحدها، فدوّر فيها بـ `Ctrl+F` على اسم الموديل.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

الكتاب قالك: الخطوة 2 في الـ model selection هي "استخدم المعلومات العامة (benchmarks و leaderboards) عشان **تضيّق** اللستة". Artificial Analysis (اختصاره **AA**) واحد من أشهر الأماكن اللي بتعمل ده النهارده، والميزة إنه بيحط **4 محاور جنب بعض**: **الذكاء، والسعر، والسرعة، والـ latency**. يعني بالظبط الـ **Pareto** بتاع الكتاب.

وفيه حاجة مهمة جداً: AA بيقيس **الموديل** و **الـ provider** كل واحد لوحده. وده بيوريك بالأرقام كلام الكتاب: "نفس الموديل من APIs مختلفة ممكن يختلف".

| # | الصفحة | بتجاوب على |
|:---:|---|---|
| 1 | Methodology | الأرقام دي معناها إيه بالظبط؟ |
| 2 | LLM Leaderboard | أنهي **موديل** أذكى، وأرخص، وأسرع؟ |
| 3 | API Providers Leaderboard | نفس الموديل: أنهي **provider** أرخص وأسرع وأثبت؟ |

> ⏳ **عمر المصدر:** الصفحات دي بتتحدّث **يومياً**. الأرقام هنا snapshot. واسم أي موديل هنا ممكن يبقى قديم بعد شهرين. **اتعلّم تقرا الجدول، مش تحفظه.**

---

## 1. Methodology
> 📍 `03-artificial-analysis-methodology.md`

### 1.1 Scope
**الفكرة:** AA بيعمل benchmarking لـ 4 حاجات: **intelligence** و **quality** و **performance** (السرعة) و **price**، على **الموديلات**، و **الـ API endpoints**، و **الـ systems**.

**3 جمل مهمة في الجزء ده:**
1. **Serverless:** بيعتبر الـ endpoint "serverless" لما بتدفع **على قد استخدامك** (غالباً بالـ token، وسعر الـ input غير الـ output)، مش سعر ثابت. (يعني الـ model APIs اللي في الكتاب.)
2. **الـ performance بتتقاس end-to-end زي ما العميل بيحسّها:** الأرقام **مش** "أقصى سرعة ممكنة على hardware معيّن"، دي **السرعة الحقيقية اللي هتشوفها لو اشتركت**. (يعني فيها الشبكة، والـ queue، وزحمة الـ provider.)
3. بيقيسوا **proprietary و open weights** الاتنين.

### 1.2 الـ Indexes (قايمة)
الصفحة فيها لستة بكل الحاجات اللي بيقيسوها: Language Model Intelligence، و Capability Indexes، و Small Language Model Intelligence، و **Endpoint Accuracy Index**، و Coding Agents، وصوت وصورة وفيديو، و API Performance، و System Load Test، و **Openness Index**، وغيرهم. كل واحد ليه صفحة methodology لوحده.

> ⚠️ **تفاصيل الـ Intelligence Index نفسه** (أنهي benchmarks جوّاه وبأي وزن) **في صفحة تانية مش من اللي رفعتها**. فمش هنشرح تركيبته هنا. اللي محتاج تعرفه: ده **رقم مجمّع** من benchmarks كتير بأوزان (زي ما الكتاب شرح الـ leaderboards بتعمل aggregation)، وبتطبّق عليه **كل أسئلة الكتاب**: بيقيس إيه؟ بيجمّع إزاي؟ ممكن يكون contaminated؟

### 1.3 Definitions ⭐⭐⭐
ده أهم جزء، لأنه بيعرّف كل عمود هتشوفه:

| المصطلح | معناه | ربطه باللي تعرفه |
|---|---|---|
| **Model** | الـ LLM نفسه (proprietary أو open) | |
| **Model Creator** | اللي درّب الموديل (OpenAI عملت GPT-4، و Meta عملت Llama 3) | |
| **Endpoint** | **نسخة متشغّلة** من الموديل بتوصلها بـ API. **الموديل الواحد ممكن يبقى ليه endpoints كتير عند providers مختلفين** | الـ inference service في الكتاب |
| **System** | بيئة compute مخصصة (زي VM) بتتقاس تحت ضغط | self-hosting |
| **Provider** | الشركة اللي بتشغّل الـ endpoints (OpenAI، و AWS Bedrock، و Together.ai...). وشركات كتير **creator و provider** في نفس الوقت | الـ 3 أنواع providers في الكتاب |
| **Serverless** | بتدفع بالاستخدام (بالـ token). ونكتة الصفحة: الـ serverless **لسه شغّال على servers** 😄 | |
| **Open Weights** | الـ weights متاحة. وبيقولوا "open weights" أو "open" **مش "open source"**، لأن موديلات كتير الـ license بتاعها **مش بيحقق التعريف الكامل** للـ open source | بالظبط جدل الكتاب (جزء 5.3.1) |
| **Token** | كل موديل ليه **tokenizer مختلف** | Step 02 Task 1 |
| **Native Tokens** | الـ tokens **بالـ tokenizer بتاع الموديل نفسه**. الأسعار والسرعة بتتحسب بيها | ⚠️ شوف تحت |

**ليه "Native Tokens" مهمة؟** لأن "100 token في الثانية" على موديل A **مش زي** "100 token في الثانية" على موديل B، لو الـ tokenizers مختلفين. ونفس الكلام في السعر. وده نفس تحذير Anthropic: الـ tokenizer الجديد بيطلّع **~30% tokens أكتر**. فالمقارنة الصح لازم تبقى على **المهمة**، مش على الـ token. وده بالظبط سبب المقاييس الجاية.

**Price (Input/Output):** سعر الـ provider الحالي لكل token داخل ولكل token خارج.

**Price (Blended):** عشان تقارن بسهولة برقم واحد، بيعملوا **متوسط مرجّح** بنسبة **7 : 2 : 1** (cache hit : input : output):

```
Blended = (7 × Cache Hit Price + 2 × Input Price + 1 × Output Price) / 10
```

مثال على **Claude Opus 5.5** (من أسعار Anthropic: cache hit $0.20، و input $4، و output $20):
`(7 × 0.20 + 2 × 4 + 1 × 20) / 10 = (1.4 + 8 + 20) / 10 = $2.94 لكل مليون token`

⚠️ **النسبة دي افتراض** (إن 70% من الـ tokens cache hits، وده شبه شغل الـ agents). لو تطبيقك chatbot من غير caching وبيطلّع ردود طويلة، النسبة الحقيقية مختلفة خالص، والـ blended price مش هيمثّلك. **احسب نسبتك إنت.**

**Cost per Task** ⭐: متوسط التكلفة (بالدولار) عشان الموديل **يخلّص مهمة واحدة** من مهام الـ Intelligence Index. بيضربوا عدد الـ tokens الفعلي (input، و cached، و output) × الأسعار، ويرجّحوا بنفس أوزان الـ index.
والجملة الأهم: **الموديلات اللي بتكتب ردود أطول أو بتفكّر أكتر (reasoning tokens) هيبقى cost per task بتاعها أعلى، حتى لو سعر الـ token نفسه.** يعني **ده المقياس اللي يهمك فعلاً**، مش سعر الـ token.

**Time per Task:** الوقت المتوقع لمهمة واحدة. بيحسبوه: (answer tokens + reasoning tokens) ÷ **output speed** (السرعة اللي قاسوها في آخر 5 أيام على الـ endpoint الأساسي، غالباً API صاحب الموديل). يعني **محسوب** من الـ tokens والسرعة، مش متوقّت فعلاً.

**Time to First Token (TTFT)** و **Time to First Answer Token (TTFAT)**: ⭐ فرق مهم مع الـ reasoning models:
- **TTFT**: لحد **أول token** يوصل. في موديل بيفكّر ويرجّع الـ thinking، ده ممكن يبقى **أول token من التفكير**.
- **TTFAT**: لحد **أول token من الإجابة نفسها**، يعني **بعد** ما يخلّص تفكير. وده بيقيس **انتظار المستخدم الحقيقي** بنفس الطريقة للموديلات اللي بتفكّر واللي مبتفكرش.

**ليه ده مهم؟** فاكر TTFT من Step 01؟ مع الـ reasoning models، الـ TTFT ممكن يبقى ثانية، بس المستخدم مش هيشوف إجابة غير بعد **دقيقة** تفكير. فـ TTFAT أصدق للـ UX.

**Output Speed:** عدد الـ output tokens (**ومعاهم الـ reasoning tokens**) في الثانية، **على مدة الـ request كلها** (يعني فيها الـ TTFT).

**End-to-End Time:** من إرسال الـ request لحد آخر token.

**Endpoint Error Rate:** نسبة الـ requests اللي **فشلت من ناحية الـ provider** في آخر 5 أيام. بيحسبوا: الـ rate limits بتاعة الـ provider، والـ timeouts. ومبيحسبوش: API key غلط، أو رصيد خلص، أو request أطول من الـ context، أو safety block. **ده مقياس الـ reliability** (محور الـ SLA في الكتاب).

**Cache Hit Rate:** نسبة الـ input tokens اللي اتقرت من الـ cache فعلاً في sessions الـ agents.

**تشبيه من Laravel:** المقاييس دي زي اللي بتشوفه في **APM** (New Relic / Laravel Pulse): مش بس "الـ endpoint بيرد" لكن **p50 latency**، و **error rate**، و **throughput**، و **تكلفة**. AA بيعمل كده للـ LLM providers كلهم ويحطهم جنب بعض.

---

## 2. LLM Leaderboard
> 📍 `03-artificial-analysis-leaderboard.md`

### 2.1 شكل الصفحة
- بتقارن **أكتر من 250 موديل**، وفي الـ snapshot بتاعك **288 صف**.
- فوق فيه **ملخصات**: الأذكى، والأسرع (time per task)، والأقل latency، والأرخص (cost per task)، والأكبر context.
- **Filters:** **Weights** (open/proprietary)، و **Size**، و **Price**، و **Reasoning**، و **Status** (Current).
- **الأعمدة:** Model، و Context Window، و Creator، و **Artificial Analysis Intelligence Index**، و **Cost per Task (USD)**، و **Time per Task (Minutes)**، و **First Answer Token (s)**.

### 2.2 إزاي تقرا أول الجدول
أول صفوف في الـ snapshot:

| Model | Index | Cost/Task | Time/Task (min) | TTFAT (s) |
|---|:---:|---:|---:|---:|
| Claude Fable 5.2 (max) | **65** | $26.54 | 46.8 | 267 |
| Claude Fable 5.2 (xhigh) | 62 | $14.83 | 26.2 | 87 |
| Claude Fable 5.2 (high) | 62 | $9.08 | 16.9 | 29 |
| Gemini 4 Carbon (high) | 60 | $5.48 | 28.4 | 65 |
| Claude Opus 5.5 (max) | 59 | $10.04 | 25.2 | 343 |
| Claude Opus 5.5 (high) | 52 | $3.46 | 9.5 | 24 |
| GPT-6.1 Sol (max) | 55 | $1.27 | 23.3 | 174 |
| Claude Sonnet 5.5 (max) | 55 | $10.02 | 34.1 | 240 |
| Claude Haiku 5.5 (medium) | 25 | $0.09 | 4.0 | 11 |

**4 دروس من الجدول ده:**

**1) الوحدة اللي بتتقارن هي "موديل + إعداد"، مش موديل بس.** نفس الموديل (Fable 5.2) موجود **5 مرات** بـ effort مختلف (max، و xhigh، و high، و medium، و low). فاكر الـ effort من صفحة Anthropic؟ أهو بالأرقام:
- Fable 5.2 من **high لـ max**: الـ index زاد **3 نقط بس** (62 ← 65)، والتكلفة زادت **3 مرات تقريباً** ($9 ← $26.5)، والـ TTFAT زاد **9 مرات** (29 ← 267 ثانية).
- يعني آخر شوية جودة **غاليين جداً**. ده بالظبط الـ **Pareto**: بعد نقطة معيّنة، كل تحسين صغير بيكلّف كتير.

**2) نفس الـ index، تكلفة مختلفة جداً.** GPT-6.1 Sol (max) و Claude Sonnet 5.5 (max) الاتنين **55**، بس واحد بـ **$1.27** والتاني بـ **$10.02** للمهمة (8 مرات). لو الـ index ده بيقيس اللي يهمك (وده "لو" كبيرة)، الفرق ده فلوس كتير.

**3) الـ latency بتاعة الـ reasoning ممكن تبقى دقايق.** Opus 5.5 (max) بياخد **343 ثانية** (حوالي 6 دقايق) لحد أول token من الإجابة! ده مقبول لـ agent بيشتغل في الخلفية، ومش مقبول خالص لـ chatbot. **الـ must-have مقابل nice-to-have** بتاع الكتاب.

**4) الأرخص مش في نفس الملعب.** Haiku 5.5 (medium) بـ **9 سنت** للمهمة و index **25**. ده **أرخص بـ 300 مرة** من Fable 5.2 (max). السؤال مش "مين أذكى"، السؤال "**مين كفاية لمهمتي** بأقل تكلفة؟".

### 2.3 الـ index رقم نسبي، مش "نسبة ذكاء"
- موديلات كتير قديمة أو صغيرة قدامها **`--`** في الـ index (يعني **مااتقيّمتش** على الـ version الحالي من الـ index)، زي Qwen3.5 9B، و gpt-oss-20b، و Gemma 4 12B.
- وفيه موديلات كانت مشهورة وقوية وقت نزولها، والنهارده رقمها **صغير جداً** (مثلاً **gpt-oss-120b (high) = 4**). ده **مش** معناه إنه "4% ذكي"، معناه إن الـ index **بقى صعب** (benchmarks أصعب بتتحط مع الوقت، زي ما الكتاب قال إن الـ benchmarks بتتشبّع فبيتعمل أصعب).
- **الدرس:** متقارنش رقم index من شهر برقم النهارده، ومتقارنش index الـ AA بـ score بتاع LMArena. كل رقم ليه **مقياسه**.

### 2.4 فين الموديلات المفتوحة؟ (اختبار لتوقّع الكتاب)
الكاتبة قالت: "أقوى موديل مفتوح غالباً هيفضل **ورا** أقوى موديل مقفول". الـ snapshot بتاعك (لو بصيت على عمود الـ License في صفحة الـ providers، جزء 3):
- **أعلى موديل open** في الـ snapshot: **Kimi K3.1 Pro** بـ index **46**، وترتيبه في الـ leaderboard حوالي **الـ 28**.
- أعلى موديل في الكل: **65** (proprietary).
- يعني **الفجوة لسه موجودة** (46 مقابل 65)، وتوقّع الكاتبة **لسه ماشي** في نوفمبر 2026. بس 46 ده **أعلى** من موديلات proprietary كتير، يعني لمهام كتير المفتوح **كفاية**، زي ما قالت برضه.

(هتتأكد من ده بنفسك بالـ filter بتاع **Weights** في Task 1.)

### 2.5 FAQ (في آخر الصفحة)
فيه أسئلة جاهزة (أنهي موديل الأول؟ الأسرع؟ الأرخص؟ أحسن open weights؟...)، بس الإجابات **مش ظاهرة** في الملف اللي اتحفظ (محتاجة ضغطة). مش مهم، الجدول نفسه بيجاوب.

---

## 3. API Providers Leaderboard
> 📍 `03-artificial-analysis-providers.md`

### 3.1 شكل الصفحة
مقارنة **أكتر من 500 endpoint** (في الـ snapshot: **525**). نفس الـ filters، والأعمدة فيها زيادة:
- **API Provider** (مين بيشغّل الموديل)
- **Error Rate %** (الـ reliability)
- **License** (**Open** أو **Proprietary**)

**أول ملاحظة:** من الـ 525 endpoint، **408 open** و **117 proprietary**. ليه الـ open أكتر بكتير؟ **الكتاب جاوب** (ص 184): الموديل المفتوح **أي provider يقدر يشغّله**، فبتلاقي نفس الموديل عند 10 و 20 provider. أما الموديل المقفول، بس صاحبه والـ clouds اللي متفقين معاه.

### 3.2 نفس الموديل المقفول على 4 platforms
**Claude Opus 5.5 (max)** في الـ snapshot:

| Provider | Cost/Task | Time/Task (min) | TTFAT (s) | Error Rate |
|---|---:|---:|---:|---:|
| Anthropic | $10.04 | 25.2 | 343 | 3.2% |
| Amazon Bedrock | $10.04 | 25.9 | 336 | 6.3% |
| Google | **$21.07** | 24.7 | 297 | 3.2% |
| Microsoft Azure | $11.43 | 30.8 | 261 | **9.8%** |

**نفس الموديل بالظبط**، بس:
- على Google **ضعف** التكلفة.
- على Azure الـ error rate **3 أضعاف** Anthropic.
- والـ TTFAT مختلف (Azure أسرع في أول token هنا).

ده **بالأرقام** نصيحة الكتاب: "نفس الموديل ممكن يختلف من API لـ API، فاعمل tests لما تبدّل". ولو شركتك عندها عقد مع AWS، Bedrock ممكن يبقى أسهل في الـ privacy والفواتير، بس لازم تعرف إن الـ error rate في الـ snapshot ده **ضعف** الأصلي.

### 3.3 نفس الموديل المفتوح عند providers كتير
**gpt-oss-120b (high)** (موديل open weight من OpenAI بـ Apache 2.0): بالاسم ده بالظبط موجود عند **13 provider**، وفيه كمان 3 نسخ بأسماء مختلفة شوية (*Vertex* عند Google، و *Base* عند Nebius، و *Turbo* عند DeepInfra)، يعني الموديل فعلياً عند **15 provider**. الجدول ده للـ 13 اللي بالاسم ده:

| Provider | Cost/Task | Time/Task (min) | TTFAT (s) | Error Rate | Context |
|---|---:|---:|---:|---:|---|
| Cerebras | $0.76 | **0.9** | **1.8** | 0.0% | 131k |
| SambaNova | $0.49 | 3.1 | 6.1 | 0.0% | 131k |
| Groq | $0.32 | 3.3 | 4.9 | 2.9% | 131k |
| CoreWeave | **$0.07** | 12.0 | 16.3 | **13.1%** | 131k |
| DeepInfra | $0.09 | **40.7** | 65.1 | 10.6% | 131k |
| Scaleway | $0.39 | 10.8 | 17.0 | 1.0% | **128k** |
| ... (و 7 تانيين) | | | | | |

**اللي بيقولهولك الجدول ده:**
- **التكلفة:** من **7 سنت لـ 76 سنت** للمهمة (**10 مرات** فرق).
- **السرعة:** من **أقل من دقيقة** لـ **40 دقيقة** للمهمة (**45 مرة** فرق!). فيه providers عاملين hardware مخصوص للسرعة.
- **الـ reliability:** من **0%** errors لـ **13%** (ونسخة *Vertex* عند Google وصلت **17.4%**).
- **الأرخص مش الأحسن:** CoreWeave الأرخص، بس error rate 13%. و Cerebras الأسرع بكتير، بس الأغلى.
- **حتى الـ context مختلف** (128k مقابل 131k).

ده **Pareto** حقيقي بين التكلفة والسرعة والـ reliability، **على نفس الموديل**. وده اللي الكتاب قصده لما قال إن الـ providers اللي ملهمش موديلات **بيتنافسوا على الـ API نفسه** (سعر وسرعة).

### 3.4 أمثلة تانية تستاهل تاخد بالك منها
- **DeepSeek V4.1 Flash (max)** في **25 endpoint** عند **21 provider** (فيه providers ليهم أكتر من نسخة، زي FAST و ULTRA): التكلفة من **$0.19** (DeepInfra) لـ **$14.54** (Scaleway)، يعني **75 مرة** فرق لنفس الموديل! وعند Scaleway الـ context **262k** بس، والباقيين **1M**.
- **Qwen3.8 27B** متاح بأسماء زي **(FP8)** و **(FP4)** و **(NVFP4)**: دي **نسخ quantized** عملها الـ provider عشان يسرّع ويرخّص. فاكر كلام الكتاب: "كل API ممكن يستخدم **تكنيكات optimization مختلفة**"؟ أهو مكتوب في الاسم. والـ quantization ممكن يأثر على الجودة شوية، والـ methodology فيها index منفصل اسمه **Endpoint Accuracy Index** (معمول تقريباً عشان يقيس الفرق ده بين الـ endpoints).
- لاحظ إن عمود الـ Intelligence Index **نفس الرقم** لكل providers نفس الموديل (مثلاً كل gpt-oss-120b = 4)، فغالباً ده **رقم الموديل**، مش متقاس لكل endpoint. يعني الجدول ده **مش هيقولك** إن نسخة FP4 أغبى شوية. لو ده يهمك، لازم **تختبر بنفسك**.

### 3.5 ليه ده مهم ليك حتى لو هتستخدم Ollama local؟
لأن ده **البديل التالت** بين "Claude API" و "Ollama على اللاب": موديل **open weight** (مثلاً موديل بنفس الـ license اللي يناسبك) بتستخدمه من **provider بيشغّله** (serverless، بالـ token). مميزاته:
- موديلات **أكبر بكتير** من اللي يدخل في جهازك.
- تقدر **تبدّل الـ provider** من غير ما تغيّر الموديل (وكتير منهم **OpenAI-compatible**، زي Ollama).
- ولو بعدين قررت **تـ host بنفسك**، نفس الموديل، نفس السلوك تقريباً.
- بس **الداتا بتخرج** برضه (لـ provider غالباً أصغر وأقل شهرة، فاقرا الـ terms). محور الـ privacy مش بيختفي.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md) تحت "Step 03 (المصدر 4)":
**Endpoint (مقابل Model)** · **Serverless Inference** · **Native Tokens** · **Blended Price** · **Time per Task** · **TTFAT (Time to First Answer Token)** · **Output Speed** · **Endpoint Error Rate** · **Intelligence Index (aggregated)**
(والـ **Cost per Task** متسجّل تحت المصدر 3 مع الـ tokenizer.)

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. إيه الفرق بين Model و Endpoint و Provider؟ وادّي مثال من الـ snapshot.</summary>

**Model**: الموديل نفسه (مثلاً gpt-oss-120b). **Endpoint**: نسخة متشغّلة منه بتوصلها بـ API عند provider معيّن (gpt-oss-120b على Groq، و gpt-oss-120b على Cerebras...). **Provider**: الشركة اللي بتشغّل الـ endpoints (Groq، و AWS Bedrock، و Anthropic). الموديل الواحد ممكن يبقى ليه endpoints كتير، وكل واحد بسعر وسرعة و error rate مختلف (gpt-oss-120b (high) عند 13 provider بالاسم ده بالظبط: من $0.07 لـ $0.76 للمهمة). وفيه شركات creator و provider مع بعض (Anthropic).
</details>

<details><summary>2. ليه AA بيقول "open weights" مش "open source"؟</summary>

لأن موديلات مفتوحة كتير نازلة بـ licenses **مبتحققش التعريف الكامل** للـ open source software (فيها قيود على الاستخدام التجاري أو عدد المستخدمين أو استخدام الـ outputs)، والداتا نفسها مش متاحة. وده نفس جدل الكتاب: الـ weights متاحة ≠ open source.
</details>

<details><summary>3. موديل سعر الـ token بتاعه أرخص بالنص، بس cost per task بتاعه أعلى. إزاي ده ممكن؟</summary>

عشان الـ **cost per task** بيحسب الـ tokens **الفعلية** اللي الموديل صرفها عشان يخلّص المهمة. لو الموديل الأرخص: (1) بيكتب ردود **أطول**، أو (2) بيفكّر **أكتر** (reasoning tokens بتتحسب output، والـ output أغلى)، أو (3) الـ **tokenizer** بتاعه بيطلّع tokens أكتر لنفس النص، أو (4) بيعيد المحاولة أو بيحتاج خطوات أكتر في مهام الـ agents، يبقى المجموع أكتر. عشان كده سعر الـ token لوحده مضلل.
</details>

<details><summary>4. الـ blended price بتاع AA بيفترض نسبة 7:2:1. إمتى الرقم ده هيضللك؟</summary>

لما تطبيقك نسبته مختلفة. الـ 7:2:1 بيفترض إن 70% من الـ tokens **cache hits** (شبه agents بيعيدوا نفس الـ context). لو عندك chatbot من غير caching، أو بتلخّص documents جديدة كل مرة (input كتير ومفيش cache)، أو بتولّد محتوى طويل (output كتير)، النسبة الحقيقية مختلفة. والموديل اللي الـ cache بتاعه رخيص جداً هيبان أرخص بكتير من حقيقته بالنسبة لك. الحل: أحسب الـ blended بنسبتي من الـ usage الحقيقي، أو أقيس cost per task على مهامي.
</details>

<details><summary>5. إيه الفرق بين TTFT و TTFAT؟ وأيهم يهمك في chatbot بـ reasoning model؟</summary>

**TTFT**: الوقت لحد **أول token**، وفي الـ reasoning models ممكن يكون أول token من **التفكير**. **TTFAT**: الوقت لحد أول token من **الإجابة** نفسها، يعني بعد التفكير. في chatbot، المستخدم بيستنى **الإجابة**، فـ **TTFAT** هو اللي بيعكس تجربته (إلا لو بتعرضله الـ thinking وهو بيتكتب). مثال الـ snapshot: Opus 5.5 (max) الـ TTFAT بتاعه **343 ثانية**، يعني مش مناسب لـ chat خالص بالإعداد ده.
</details>

<details><summary>6. Fable 5.2 (high) بـ index 62 وبـ $9.08، و Fable 5.2 (max) بـ 65 وبـ $26.54. تختار أنهي؟</summary>

بيعتمد على: (1) هل الـ 3 نقط دي **بتفرق في مهمتي أنا**؟ (الـ index عام، ومحتاج eval بتاعي). (2) الـ **latency**: max الـ TTFAT بتاعه 267 ثانية مقابل 29، والـ time per task ضعف الضعف تقريباً. (3) **حجم الاستخدام**: 3 أضعاف التكلفة على مليون مهمة فرق ضخم. غالباً أبدأ بـ high، وأستخدم max **بس** للمهام اللي الـ eval بيقول إنها محتاجاه (أو routing: المهام الصعبة بس لـ max). ده Pareto: آخر نقط الجودة أغلى حاجة.
</details>

<details><summary>7. من صفحة الـ providers: Claude Opus 5.5 على Google بضعف تكلفة Anthropic، وعلى Azure الـ error rate 9.8%. ليه شركة ممكن تختار Google أو Azure برضه؟</summary>

عشان أسباب **مش في الجدول**: (1) **privacy/compliance**: الشركة عندها عقد وثقة في cloud معيّن، والداتا متطلعش برّه حسابها (footnote 14 في الكتاب). (2) **الفواتير**: كل حاجة في فاتورة واحدة، وممكن credits أو خصومات متفاوض عليها. (3) **الـ integration** مع باقي خدماتهم (IAM، و networking، و logging). (4) **data residency** في regions معيّنة. بس لازم يعرفوا التمن (تكلفة، و reliability)، ويعملوا retries و fallback عشان الـ error rate.
</details>

<details><summary>8. نفس الموديل المفتوح عند provider بـ $0.07 للمهمة وعند تاني بـ $0.76. إيه الأسئلة اللي تسألها قبل ما تختار الأرخص؟</summary>

(1) **الـ error rate** (الأرخص في الـ snapshot كان 13%، يعني retries كتير وتجربة مستخدم وحشة). (2) **السرعة** (time per task و TTFAT: الفرق ممكن يبقى 45 مرة). (3) **الـ quantization**: الـ endpoint ده FP8 ولا FP4 ولا full precision؟ ده ممكن يأثر على الجودة، والـ index في الجدول مش بيقيسه لكل endpoint. (4) **الـ context** المسموح. (5) **الـ features** (structured outputs، و tools). (6) **الـ privacy terms** والـ data retention والـ region. (7) **الـ rate limits** والـ SLA. وفي الآخر أشغّل الـ eval set بتاعي عليه.
</details>

<details><summary>9. الكتاب توقّع إن أقوى موديل مفتوح هيفضل ورا أقوى مقفول. الـ snapshot بيقول إيه؟</summary>

التوقّع **لسه ماشي**: أعلى موديل open في الـ snapshot (Kimi K3.1 Pro) بـ index **46**، وأعلى موديل في الكل (proprietary) بـ **65**، والـ open الأول ترتيبه حوالي **الـ 28**. بس 46 أعلى من موديلات proprietary كتير، فالكلام التاني بتاع الكاتبة برضه صح: لـ use cases كتير مش محتاجة الأقوى، **المفتوح كفاية**. ولازم أتأكد من تاريخ الـ snapshot، لأن الترتيب بيتغيّر كل كام أسبوع.
</details>

<details><summary>10. ليه مينفعش تقارن الـ Intelligence Index بتاع موديل النهارده برقمه من سنة؟</summary>

لأن الـ index **بيتغيّر**: بيتضاف benchmarks أصعب وبتتشال اللي اتشبّعت (زي ما الكتاب شرح في Hugging Face). فرقم 50 النهارده مش هو 50 من سنة. وده واضح في الـ snapshot: موديلات كانت قوية وقت نزولها (gpt-oss-120b) رقمها النهارده **4**، وموديلات قديمة كتير **`--`** (مااتقيّمتش على الـ version الحالي). قارن الموديلات **جوه نفس الـ snapshot** بس.
</details>
