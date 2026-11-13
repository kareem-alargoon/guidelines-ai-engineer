# شرح: Anthropic docs — Models overview، و Choosing a model، و Pricing، و Model deprecations

> **المصدر:** [Claude Platform Docs](https://platform.claude.com/docs/en/about-claude/models/overview) — النسخة اللي اتحفظت يوم 2026-11-13
> **الملفات:**
> - `resources/articles/03-anthropic-models-overview.pdf` (14 صفحة)
> - `resources/articles/03-anthropic-choosing-a-model.pdf` (5 صفحات)
> - `resources/articles/03-anthropic-pricing.pdf` (18 صفحة)
> - `resources/articles/03-anthropic-model-deprecations.pdf` (8 صفحات)
>
> **إزاي تقرا:** بالترتيب ده. الـ 📍 بيقولك الملف والصفحة.
> ⚠️ **الجداول الكبيرة اتلخبطت في الـ PDF** (الأعمدة دخلت في بعض، بالذات جدول *All models* وجدول *Model status*). لو رقم مش واضح، افتح الصفحة أونلاين وقارن. الأرقام اللي هنا متاخدة من الأجزاء اللي واضحة في الملفات.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

الكتاب ادّاك **الإطار**: hard/soft attributes، و API مقابل self-hosting، والتكلفة، وخطر إنك تفقد الموديل. Ollama ادّاك **ناحية الـ self-hosting**. الصفحات دي بتديك **ناحية الـ API** بأرقام حقيقية من provider حقيقي:
- **أنهي موديلات موجودة**، والفرق بينهم (جودة، سرعة، سعر، context).
- **Anthropic نفسها بتنصحك تختار إزاي** (وهنقارنه بنصيحة الكتاب).
- **التسعير بالتفصيل**: مش بس "سعر الـ token"، فيه caching و batch و data residency و fast mode وحاجات مستخبية.
- **الموديل بيعيش قد إيه** قبل ما يتشال (deprecation)، وده بالظبط محور الـ **control** في الكتاب.

| # | الصفحة | أهميتها |
|:---:|---|:---:|
| 1 | Models overview | ⭐⭐⭐ |
| 2 | Choosing a model | ⭐⭐⭐⭐ |
| 3 | Pricing | ⭐⭐⭐⭐ |
| 4 | Model deprecations | ⭐⭐⭐ |

> ⏳ **عمر المصدر:** أكتر صفحات بتتغيّر في المجال كله. الموديلات والأسعار دي **صح يوم 2026-11-13 بس**. بعد كام شهر هيبقى فيه موديلات تانية. **اتعلّم شكل القرار، مش الأرقام.**

---

## 1. Models overview
> 📍 `03-anthropic-models-overview.pdf`

### 1.1 الـ lineup الحالي (ص 1–3)
الصفحة بتبدأ بنصيحة صريحة: **لو مش متأكد، ابدأ بـ Claude Opus 5.5** لأغلب الشغل. واستخدم **Claude Fable 5.2** للـ reasoning الصعب والـ agents اللي بتشتغل لفترات طويلة، **أو لما الـ evals بتاعتك على Opus 5.5 بـ effort أعلى لسه مش كفاية**. (لاحظ: حتى Anthropic بتقولك القرار **بالـ evals بتاعتك**، زي الكتاب.)

وكل الموديلات الحالية بتدعم: input نص وصور، و output نص، و multilingual، و vision، و tool use.

| | **Fable 5.2** | **Opus 5.5** | **Sonnet 5.5** | **Haiku 5.5** |
|---|---|---|---|---|
| **معمول لـ** | reasoning صعب و agents طويلة | agentic coding و knowledge work | أحسن توازن سرعة وذكاء | حجم كبير و latency قليلة (classification، extraction، routing) |
| **Latency نسبية** | Moderate | Moderate | Fast | **Fastest** |
| **السعر (input / output لكل مليون token)** | $8 / $40 | $4 / $20 | $2 / $10 | من $0.10 / من $0.50 |
| **API ID** | `claude-fable-5-2` | `claude-opus-5-5` | `claude-sonnet-5-5` | `claude-haiku-5-5` |
| **Thinking** | Adaptive (دايماً شغّال) | Adaptive (دايماً شغّال) | Adaptive | Adaptive |
| **Default effort** | high | medium | high | medium |
| **Context window** | 1M | 1M | 1M | 1M |
| **Max output** | 128K | 128K | 128K | 128K |
| **Knowledge cutoff** | يونيو 2026 | يونيو 2026 | يونيو 2026 | يونيو 2026 |
| **Retirement** | مش قبل 9 نوفمبر 2027 | مش قبل 22 سبتمبر 2027 | مش قبل 28 سبتمبر 2027 | مش قبل 7 أكتوبر 2027 |

**إزاي تقرا الجدول ده بعين الكتاب:**
- **الـ tiers:** نفس الشركة بتبيع **4 مستويات**. كل ما تنزل، أسرع وأرخص وأقل قدرة. بين Fable و Haiku فرق **80 مرة** في سعر الـ input (8 مقابل 0.10). ده محور **التكلفة/الأداء** اللي الكتاب قال اختار عليه "أحسن أداء مقابل فلوسك".
- **Output أغلى من Input بـ 5 مرات** في كل الموديلات. ليه؟ عشان الـ output بيتولّد **token ورا token** (الـ decode)، أما الـ input بيتقري **مرة واحدة** (الـ prefill). فاكرهم من Step 02؟ يعني **رد طويل أغلى بكتير من prompt طويل**. وده سبب تاني (غير الـ latency) إنك تطلب ردود مختصرة.
- **Thinking و Effort:** الموديلات دي **reasoning models** (Step 02: "models need tokens to think"). والـ **effort** زرار بيتحكم الموديل يفكّر قد إيه. والـ thinking tokens **بتتحسب output**، يعني بتدفعها.
- **Knowledge cutoff:** الموديل مايعرفش حاجة بعد يونيو 2026 (Step 01).
- **Retirement:** **"مش قبل" تاريخ معيّن**، يعني الموديل ده مضمون لحد التاريخ ده **على الأقل**. (جزء 4.)

**تشبيه من Laravel:** الـ tiers دي زي **خطط الـ hosting** أو **أحجام AWS instances** (t3.micro لحد m5.4xlarge): نفس الـ provider، نفس الـ API، وإنت بتختار الحجم حسب الشغل. ومحدش بيحط cron job بسيط على أكبر سيرفر. نفس الفكرة: تصنيف tickets بسيط على Haiku، و agent بيكتب كود على Opus.

### 1.2 IDs على كل platform (ص 2–3)
نفس الموديل ليه ID على كل platform:
- **Claude API:** `claude-opus-5-5`
- **Amazon Bedrock:** `anthropic.claude-opus-5-5` (وموديلات بـ prefix `global.` زي `global.anthropic.claude-fable-5-2`)
- **Google Cloud، و Microsoft Foundry، و Claude Platform on AWS:** غالباً نفس ID بتاع Claude API.

**ربط بالكتاب:** ده بالظبط اللي الكاتبة قالته: **نفس الموديل متاح من أكتر من API**: من صاحب الموديل (Anthropic)، ومن cloud providers (AWS، و Google، و Azure). وده بيفيدك في الـ **privacy** (الشركة ممكن تثق في AWS اللي عندها حساب عليه أصلاً، footnote 14 في الكتاب)، بس لازم **تعمل tests** لو بدّلت (الـ features والـ IDs والأسعار ممكن تختلف).

### 1.3 All models (ص 3–5)
جدول بكل الموديلات اللي لسه موجودة، والجديد والقديم. الصفحة بتقول: الموديلات القديمة **ممكن** تكون لسه متاحة، بس **المفروض تبدأ بالأحدث** لو ينفع، وفيه migration guides للتنقل، وتواريخ الـ retirement في صفحة deprecations.

**حاجتين تاخد بالك منهم في الجدول** (لو مش واضح في الـ PDF، الأرقام دي نفسها في صفحة Pricing بشكل أوضح):
- **الأسعار نزلت جامد:** Opus 4.1 كان **$15 / $75**، و Opus 5.5 النهارده **$4 / $20**. يعني الموديل الأحدث والأقوى **أرخص بحوالي 4 مرات**. ده اتجاه عام في المجال كله.
- **الـ context كبر:** الموديلات الأقدم (زي Opus 4.5 و Sonnet 4.5 و Haiku 4.5) **200K**، والجديدة **1M**.
- وفيه موديلات **Mythos** بـ "limited availability" (لشركات متحققة بس عن طريق برامج verification). مش هتتعامل معاها.

**الدرس:** أي حسابات تكلفة عملتها من سنة **غالباً غلط دلوقتي**. ودي حاجة الكتاب قالها: لازم تعيد القرار مع الوقت.

### 1.4 Models API (ص 5–12)
تقدر **تسأل الـ API نفسه** عن الموديلات وقدراتها: **`GET /v1/models`**. والرد فيه لكل موديل:
- `id` و `display_name` و `created_at`
- **`max_input_tokens`** (الـ context window) و **`max_tokens`** (أقصى output)
- **`capabilities`**: object فيه لكل قدرة `supported: true/false`:
  - `batch`، و `citations`، و `image_input`، و `pdf_input`، و **`structured_outputs`**
  - **`effort`**: أنهي مستويات مدعومة (`low` و `medium` و `high` و `xhigh` و `max`)
  - **`thinking`**: أنواع الـ thinking المدعومة (`adaptive`، و `enabled`، و `disabled`، و `between_tools`)
  - `server_tools` (web search و code execution)، و `context_management`...
- **`lifecycle`**: `active` أو `deprecated` أو `retired` (جزء 4)
- **`retires_at`**: تاريخ الـ retirement المجدول
- **`line`**: العيلة (`haiku` أو `sonnet` أو `opus` أو `fable` أو `mythos`)

**نصايح الصفحة المهمة:**
- **"اقرا `line` ومتستنتجش العيلة من الـ `id`"** (ص 5، 12). يعني متعملش `if "opus" in model_id`. ولو Anthropic زوّدت lines جديدة، كودك ميبوظش.
- **`supported: true` مش معناها إن الـ request هيعدّي أكيد**: ممكن يترفض لسبب تاني (مثلاً effort level مش مسموح مع thinking مقفول، أو الـ admin قفل web search للـ organization).
- وأمثلة على إن الموديلات **مختلفة في القدرات**: Sonnet 5.5 مثلاً **مبيقبلش** `thinking: disabled` (هيرجع 400)، و Haiku 4.5 بيدعم code execution بس مبيدعمش إن الكود يكلّم tools تانية.

**ليه ده مهم؟** ده **feature detection**: بدل ما تـ hard-code "الموديل ده بيدعم كذا" في كودك، **تسأل**. وده نفس فكرة `ollama show` و `/api/show` في Ollama (اللي بيقولك الـ capabilities والـ context). وده بيحل مشكلة الكتاب "الـ features بتختلف بين APIs وموديلات" بشكل منظّم.

**تشبيه من Laravel:** زي `Schema::hasColumn('users', 'phone')` قبل ما تستخدم الـ column، أو زي ما الـ DB driver بيقولك يدعم إيه (`$connection->getDriverName()`). متفترضش، اسأل.

### 1.5 Prompt and output performance (ص 13)
كلام تسويقي في الأغلب (الموديلات ممتازة في الـ reasoning والكود واللغات...). بس فيه نقطة عملية: الموديلات دي بتحب **الردود الغنية والطويلة**، ولو عايز ردود **مختصرة**، **اطلب ده في الـ prompt**. وده بيوصلنا لكلام الكتاب: الرد الأقصر = **latency أقل وتكلفة أقل** (والـ output أغلى 5 مرات).

---

## 2. Choosing a model
> 📍 `03-anthropic-choosing-a-model.pdf`

### 2.1 Establish key criteria (ص 1)
Anthropic بتقولك قيّم 4 حاجات:
1. **Capabilities:** محتاج features أو قدرات إيه؟
2. **Speed:** محتاج الرد يوصل في قد إيه؟ وفيه **Fast mode**: لحد **2.5 مرة** أسرع في الـ output بسعر أعلى (على موديلات معيّنة).
3. **Cost:** الميزانية في التطوير **وفي الـ production**.
4. **Effort:** ⭐ النقطة الجديدة: موديلات كتير فيها **`effort` parameter** بيبدّل بين **الذكاء** و **الـ latency والتكلفة** **جوه نفس الموديل**. وبيقولوا: **ضبط الـ effort غالباً أحسن من إنك تغيّر الموديل**. ابدأ بالـ default (`high` في Fable و Sonnet 5.5، و `medium` في Opus 5.5 و Haiku 5.5) وعدّل حسب الـ evals.

**ربط بالكتاب:** الـ 3 الأولانيين هما الـ **quality / latency / cost** بتوع الكتاب (Pareto). والـ effort ده **بُعد جديد** مكانش موجود وقت الكتاب: الـ **test time compute** (Step 02) بقى **زرار** بتظبطه، بدل ما تختار موديل تاني.

**تشبيه:** الـ effort زي **`cost` factor في bcrypt** (`Hash::make($pw, ['rounds' => 12])`): نفس الـ algorithm، بس رقم أعلى = شغل أكتر = أبطأ وأقوى. ونفس الفكرة: نفس الموديل، effort أعلى = تفكير أكتر = أبطأ وأغلى وغالباً أدق.

### 2.2 Choose the best model to start with (ص 1–3) ⭐⭐
طريقتين تبدأ بيهم:

| | **Option 1: Efficiency-first** | **Option 2: Capability-first** |
|---|---|---|
| **تبدأ بـ** | **Haiku 5.5** (الأسرع والأرخص) | **Opus 5.5** (الأقوى للمهام الصعبة) |
| **الخطوات** | ابدأ بيه ← اختبر كويس ← شوف الأداء كفاية؟ ← **رقّي بس لو لازم** | ابدأ بيه ← ظبط الـ prompts ← شوف الأداء كفاية؟ ← **قلّل الـ effort أو انزل لموديل أرخص** مع الوقت ← ولو لسه مش كفاية حتى بـ effort عالي، اطلع لـ Fable 5.2 |
| **مناسب لـ** | الـ prototyping، و latency صارمة، والتكلفة حساسة، ومهام بسيطة بحجم كبير | reasoning معقد، وعلمي/رياضي، وفهم دقيق، ولما الدقة أهم من التكلفة، و agents |

**قارن بالكتاب (مهم):** الكاتبة قالت في الـ prompt engineering ابدأ **بأقوى موديل** عشان تعرف المهمة ممكنة، وبعدين ارجع لورا. ده **Option 2**. Anthropic بتدّيك الاتنين. إمتى كل واحد؟
- **Option 1** منطقي لما المهمة **واضحة إنها بسيطة** (تصنيف sentiment، استخراج email من نص)، وإنت متأكد إن موديل صغير يقدر. ساعتها البداية بالأقوى تضييع فلوس.
- **Option 2** منطقي لما **مش متأكد** المهمة ممكنة أصلاً. لو بدأت بالصغير وفشل، مش هتعرف السبب.

**ليك في التاسكات:** Ollama local هو "Option 1" بالفطرة (ببلاش وصغير). وده بالظبط ليه لو 3B فشل، **محتاج مرجع أقوى** تقارن بيه قبل ما تحكم.

**تحذير الـ breaking changes (ص 2–3):** لو كودك بيستخدم حاجات معيّنة (زي إنك تجبر الموديل يستخدم tool بـ `tool_choice`، أو تقفل الـ thinking، أو tool الـ computer use)، **اقرا الـ breaking changes قبل ما تبدّل** لـ Opus 5.5 أو Fable 5.2. يعني **حتى جوه نفس الـ provider**، تبديل الموديل ممكن يكسر الكود. (ده تأكيد لنصيحة الكتاب: اعمل tests لما تبدّل.)

### 2.3 Model selection matrix (ص 3)
"أغلب الشغل يبدأ بـ Opus 5.5":

| محتاج | ابدأ بـ | أمثلة |
|---|---|---|
| أعلى قدرة متاحة | Fable 5.2 | agent شغّال ساعات، research متعدد الخطوات، تحليل لحد document أو spreadsheet خلصان |
| كود و agents وشغل شركات يومي | Opus 5.5 | coding agents لساعات، refactoring كبير، vision كتير، computer use |
| توازن | Sonnet 5.5 | كتابة كود، تحليل داتا، كتابة محتوى، فهم صور، tool use |
| أقل latency وسعر | Haiku 5.5 | real-time، حجم كبير، تكلفة حساسة، **subagent tasks** |

### 2.4 Decide whether to upgrade or change models (ص 4) ⭐⭐⭐
ده أهم جزء في الصفحة، وهو **نفس كلام الكتاب بالظبط**:
1. **اعمل benchmark tests خاصة بالـ use case بتاعك.** والجملة المهمة: **evaluation set كويس هو أهم خطوة في العملية كلها.**
2. اختبر **بالـ prompts والداتا الحقيقية** بتاعتك.
3. قارن الموديلات في: دقة الردود، وجودتها، والتعامل مع الـ **edge cases**.
4. **وازن** الأداء والتكلفة.

يعني الكتاب (اللي محايد) والـ provider (اللي عايز يبيعلك) **متفقين**: متصدّقش الـ benchmarks العامة، قيس على داتاك.

### 2.5 Combine models (ص 4)
مش لازم موديل واحد للتطبيق كله. **Multimodel strategies**: تخلّي أغلب الـ tokens تتحاسب بالسعر الرخيص:
- **Executor + Advisor:** موديل رخيص بيشتغل، ولما يقابل **قرار صعب** يسأل موديل قوي.
- **Orchestrator + Workers:** موديل قوي بيخطط، وبيوزّع **الشغل الكتير** على موديلات رخيصة.

**تشبيه:** زي شركة فيها senior و juniors: الـ juniors (Haiku) بيعملوا أغلب الشغل، والـ senior (Opus) بيتسأل في القرارات الصعبة أو بيوزّع الشغل. محدش بيدفع مرتب senior عشان يعمل data entry. (هنبني حاجة زي كده في Step 11.)

---

## 3. Pricing
> 📍 `03-anthropic-pricing.pdf`

### 3.1 Model pricing (ص 1–2)
كل الأسعار بالدولار، **لكل مليون token (MTok)**. الجدول فيه 5 أعمدة:

| Model | Input | Output | Cache write (5m) | Cache write (1h) | Cache hit |
|---|---|---|---|---|---|
| Fable 5.2 | $8 | $40 | $10 | $16 | $0.20 |
| Opus 5.5 | $4 | $20 | $5 | $8 | $0.20 |
| Sonnet 5.5 | $2 | $10 | $2.50 | $4 | $0.10 |
| Haiku 5.5 (prompt ≤ 100K) | $0.10 | $0.50 | $0.125 | $0.20 | $0.01 |
| Haiku 5.5 (prompt > 100K) | $0.50 | $2.50 | $0.625 | $1 | $0.05 |
| *(قديم)* Opus 4.1 | $15 | $75 | $18.75 | $30 | $1.50 |
| *(قديم)* Haiku 4.5 | $1 | $5 | $1.25 | $2 | $0.10 |

(الصفوف بتاعة Haiku 5.5 متلخبطة شوية في الـ PDF. لو مش واضحة، قارن بالصفحة أونلاين.)

**مثال حساب** (هتعمل زيه في التاسكات): chatbot بيبعت 2,000 token input ويستقبل 500 token output في كل رسالة، و 10,000 رسالة في اليوم:
- input: 2,000 × 10,000 = 20M token. output: 500 × 10,000 = 5M token.
- على **Sonnet 5.5**: (20 × $2) + (5 × $10) = $40 + $50 = **$90 في اليوم** (حوالي $2,700 في الشهر).
- على **Haiku 5.5**: (20 × $0.10) + (5 × $0.50) = $2 + $2.50 = **$4.50 في اليوم**.
- يعني **20 مرة فرق**. السؤال: هل Haiku **كفاية** للمهمة؟ ده اللي الـ eval set بتاعك بيجاوبه.

### 3.2 ⚠️ ملاحظة الـ tokenizer (ص 2) ⭐⭐⭐
جملة صغيرة بس مهمة جداً: موديلات **Claude 4.7 وأحدث** بتستخدم **tokenizer جديد** بيطلّع **حوالي 30% tokens أكتر لنفس النص** (والزيادة بتختلف حسب المحتوى). والـ FAQ (ص 17) بيأكد: عدد الـ tokens **بيعتمد على الـ tokenizer واللغة ونوع المحتوى**، فعدّها بالـ token counting على الموديل المحدد.

**ليه دي مهمة جداً؟**
- **سعر الـ token لوحده مش بيقولك التكلفة الحقيقية.** موديل بـ $4 لكل مليون، بس بيقطّع نصك لـ tokens أكتر بـ 30%، تكلفته الفعلية زي موديل بـ $5.20 بالـ tokenizer القديم.
- فاكر **Task 1 في Step 02** (الـ token counter)؟ لقيت إن العربي بياخد tokens أكتر من الإنجليزي **على tokenizer الـ Qwen**. الـ tokenizer بتاع كل موديل مختلف، فالنسبة دي هتختلف من موديل لموديل.
- **الدرس:** قارن **تكلفة المهمة** (cost per task) مش سعر الـ token. وده بالظبط ليه Artificial Analysis و LMArena بقوا يعرضوا "cost to run" و "Cost/Task" (الشروحات الجاية).

### 3.3 Cloud platform pricing و data residency (ص 2–6)
- **Bedrock و Google Cloud (Google managed):** **هما** اللي بيحددوا الأسعار وبيبعتولك الفاتورة. فلازم تشوف صفحاتهم.
- **Global مقابل Regional endpoints (ص 3):** **global** = الـ request يروح لأي مكان متاح (أعلى availability). **regional** = **مضمون** إن الداتا تمشي في منطقة جغرافية معيّنة. والـ **regional أغلى بـ 10%**.
- **Claude Platform on AWS و Microsoft Foundry (ص 3–5):** الفاتورة بتيجي من الـ marketplace بتاعهم بوحدة اسمها CCU ($0.01). (تفاصيل billing، مش محتاجها.)
- **Data residency (ص 6):** لو حددت **`inference_geo: "us"`** (الـ inference يحصل في أمريكا بس)، كل الأسعار **× 1.1**. والـ default (global) بالسعر العادي.

**ربط بالكتاب (محور الـ privacy):** الكتاب قال إن فيه دول بتمنع إن الداتا تخرج برّه حدودها، والـ provider لازم يحط سيرفرات هناك. هنا شايف ده **بفلوس**: الـ data residency **ليها تمن** (10%). يعني الـ privacy مش بس "local مقابل cloud"، فيه درجات في النص، وكل درجة ليها سعر.

### 3.4 Prompt caching (ص 5–6)
لو بتبعت **نفس الجزء الكبير** من الـ prompt في كل request (system prompt طويل، أو document، أو تاريخ محادثة)، الـ API يقدر **يحفظه** ويقراه من الـ cache بسعر أقل بكتير:
- **كتابة في الـ cache:** 5 دقايق = **1.25×** سعر الـ input. ساعة = **2×**.
- **قراية من الـ cache (hit):** **0.1×** في أغلب الموديلات (و 0.05× في Opus 5.5 و Sonnet 5.5، و 0.025× في Fable 5.2).
- **بيوفّر إمتى؟** الـ 5 دقايق بيكسب **من أول قراية**. الساعة بيكسب **بعد قرايتين**.
- وطريقتين: **automatic** (`cache_control` واحد في الـ request، الموصى بيه) أو **explicit breakpoints**.

**تشبيه:** زي **Redis cache** لـ query تقيلة: أول مرة بتدفع تمن الـ query **وكمان** تمن الكتابة في الـ cache، والمرات اللي بعدها بتقرا من الـ cache ببلاش تقريباً. وله TTL. (هنطبّقه في Step 04.)

**ربط بالكتاب:** ده واحد من الحاجات اللي بتخلّي "cost per token ثابت مع الـ API" **مش دقيقة 100%**: لو تطبيقك فيه context متكرر كتير، الـ caching بيقلل التكلفة جامد.

### 3.5 Fast mode (ص 6–7)
لحد **2.5 مرة** tokens في الثانية في الـ output، **بسعر أعلى**: Opus 5.5 بـ $8 / $40 (يعني **ضعف** السعر العادي)، و Fable 5.2 بـ $16 / $80. ومش بيشتغل مع الـ Batch API.

**ربط بالكتاب:** ده الـ **latency/cost trade-off** بأرقام صريحة: **سرعة أكتر = ضعف الفلوس**. فاكر "must-have مقابل nice-to-have"؟ لو الـ latency مضايقة بس (nice-to-have)، متدفعش الضعف.

### 3.6 Batch processing (ص 7–8)
**Batch API**: تبعت requests كتير **async** (مش لازم ترد فوراً)، وتاخد **خصم 50%** على الـ input والـ output. مثال: Opus 5.5 بيبقى $2 / $10.

**إمتى؟** أي حاجة **مش مستعجلة**: تصنيف 100,000 ticket قديم، أو تلخيص documents بالليل، أو تشغيل الـ evals بتاعتك.

**تشبيه من Laravel:** ده الفرق بين إنك تعمل الحاجة **sync في الـ request** وبين إنك تعمل `dispatch(new ProcessTickets)` على **queue** تتعمل بعدين. لو المستخدم مش مستني، حطها في queue وادفع نص التمن.

### 3.7 Long context pricing (ص 9)
- موديلات **4.6 وأحدث** (ما عدا Haiku 5.5): الـ **1M context كله بنفس السعر**. request بـ 900K token بنفس سعر الـ token بتاع request بـ 9K.
- **Haiku 5.5** مختلف: لو الـ prompt **أكتر من 100K token**، الأسعار كلها أعلى (شوف الجدول). وكل request بيتحسب لوحده.

**يعني:** الـ context الكبير **متاح**، بس **مش ببلاش**: كل token بتدفعه. 900K token على Opus 5.5 = **$3.60 للـ request الواحد** (input بس). ومش كل حاجة لازم تتحط في الـ context (ده سبب الـ RAG في Step 09).

### 3.8 Tool use pricing (ص 9–14)
لما تستخدم **tools** (Step 10)، فيه **tokens مستخبية** بتدفعها:
- تعريفات الـ tools نفسها (الأسماء، والأوصاف، والـ schemas) = input tokens.
- **system prompt إضافي** الـ API بيحطه لوحده: مثلاً **286 token** في Opus 5.5 و Sonnet 5.5 و Haiku 5.5 (مع `tool_choice` auto)، و **406** لو بتجبره (`any`/`tool`). وبيختلف من موديل لموديل (Opus 4.8 مثلاً 675).
- tools جاهزة من Anthropic ليها تكلفة إضافية: **web search بـ $10 لكل 1,000 بحث** + الـ tokens بتاعة النتايج. و web fetch من غير رسوم إضافية بس المحتوى بيتحسب tokens (صفحة ويب متوسطة **~2,500 token**، و PDF بحث **~125,000 token**). و computer use و browser use بيضيفوا **آلاف** الـ tokens لكل request.

**الدرس:** التكلفة الحقيقية = **الـ tokens اللي إنت شايفها + اللي مستخبية**. ولما الـ agent يستخدم tools كتير، الـ context بيكبر بسرعة (ارجع لـ Step 02: Context windows).

### 3.9 Claude Managed Agents و worked example (ص 14–16)
خدمة agents شغّالة عند Anthropic. بتتحاسب بالـ tokens + **$0.08 لكل ساعة session**. والمثال المحسوب في الصفحة **ممتاز** كتمرين:

session ساعة على **Opus 5.5**، فيها 50,000 input و 15,000 output:
- input: 50,000 × $4 / 1,000,000 = **$0.20**
- output: 15,000 × $20 / 1,000,000 = **$0.30**
- runtime: 1 ساعة × $0.08 = **$0.08**
- **المجموع: $0.58**

ولو 40,000 من الـ input كانوا **cache hits**: الـ 10,000 الباقيين = $0.04، والـ 40,000 cached = 40,000 × $4 × 0.05 / 1,000,000 = $0.008، فالمجموع **$0.428** (يعني الـ caching وفّر حوالي 26%).

### 3.10 Cost optimization، و rate limits، و volume discounts (ص 16–17)
**نصايحهم للتوفير:** (1) **الموديل المناسب** (Haiku للبسيط، و Sonnet لأغلب الـ production، و Opus للأعقد). (2) **Prompt caching**. (3) **Batch** للحاجات اللي مش مستعجلة. (4) **راقب الاستهلاك**.

**Rate limits:** بتختلف حسب الـ **usage tier**: **Start** (للبداية)، و **Build** (للتطبيقات اللي بتكبر)، و **Scale** (للـ production). وفوق كده تكلّم الـ sales.
**ربط بالكتاب:** ده صف الـ **Scale (TPM)** في Table 4-3، ومحور الـ control ("إنت تحت rate limits بتاعتهم"). يعني مش بس "تدفع وخلاص": حسابك الجديد **مش هيستحمل** traffic كبير من أول يوم.

**تشبيه:** زي `throttle:60,1` middleware في Laravel، بس **إنت** اللي عليك الـ throttle، والـ provider هو اللي بيحدده حسب "مستواك".

**Volume discounts و enterprise:** خصومات بتتفاوض عليها، و rate limits مخصوصة، وعقود. **ربط بالكتاب (footnote 18):** الكاتبة قالت إن الشركات الكبيرة بتقدر تتفاوض على أسعار أحسن، والأكتر تضرراً من أسعار الـ API هي الشركات المتوسطة. أهو مكتوب رسمي.

### 3.11 FAQ (ص 17–18)
- **الـ tokens بتتحسب إزاي؟** بتعتمد على الـ tokenizer، واللغة، ونوع المحتوى (جزء 3.2).
- **فيه free tier؟** المستخدمين الجداد بياخدوا **free credits** يجربوا بيها.
- **الخصومات بتتجمع؟** آه، الـ Batch والـ caching مع بعض.

---

## 4. Model deprecations
> 📍 `03-anthropic-model-deprecations.pdf`

### 4.1 Overview والـ lifecycle (ص 1)
مع نزول موديلات أحدث وأأمن، Anthropic **بتشيل الموديلات القديمة بانتظام**، فتطبيقك **هيحتاج تحديث من وقت للتاني** عشان يفضل شغّال. والمتأثرين بيتبلّغوا **بالإيميل وفي الـ docs**.

**الـ lifecycle:**

| الحالة | يعني إيه |
|---|---|
| **Active** | مدعوم بالكامل وموصى بيه |
| **Legacy** | مش هياخد تحديثات، وممكن يبقى deprecated بعدين |
| **Deprecated** | لسه شغّال، بس **مش موصى بيه**، وليه بديل موصى بيه **وتاريخ retirement** |
| **Retired** | **مش متاح**. أي request ليه **بيفشل** |

وبيقولوا إن الـ deprecated **غالباً أقل reliability** من الـ active.

**التواريخ دي للـ platforms اللي Anthropic بتشغّلها** (Claude API، و Claude Platform on AWS، و Google Cloud Anthropic managed، و Foundry). أما **Bedrock و Google Cloud (Google managed)** فليهم **جداول retirement بتاعتهم**، فالموديل ممكن يعيش هناك أطول أو أقصر. (ده سبب إن صفحة Models overview مكتوب فيها "retired, except on Bedrock and Google Cloud" جنب موديلات زي Opus 4.)

**تشبيه من Laravel (دقيق جداً):** ده **support policy بتاع Laravel نفسه**: كل version ليه فترة bug fixes وفترة security fixes، وبعدها **مبيتدعمش**. الفرق: Laravel القديم **بيفضل شغّال** عندك (الكود عندك)، لكن موديل الـ API لما يبقى **retired بيبطّل يشتغل خالص**. ده بالظبط فرق "تجمّد الموديل" اللي الكتاب اتكلم عنه.

### 4.2 Migrating، و notifications، و auditing (ص 2)
- بعد الـ deprecation، **انقل كل استخدامك** للبديل **قبل** تاريخ الـ retirement، لأن الـ requests بعده **هتفشل**.
- **اختبر تطبيقك على الموديل الجديد بدري**، قبل التاريخ بكتير (عشان تقيس الأداء على مهامك).
- **الإشعار:** على الأقل **60 يوم** قبل الـ retirement للموديلات العامة.
- **Audit:** من الـ Console ← Usage ← Export، وهتاخد CSV بالاستخدام لكل API key وموديل، عشان تلاقي أي حتة في كودك لسه بتستخدم موديل deprecated.
- **Best practices:** تابع الـ docs، واختبر بدري، وحدّث للبديل في أقرب وقت، وكلّم الـ support لو محتاج.

**ربط بالكتاب:** الكاتبة قالت "الـ prompts بتاعتك ممكن تبطّل تشتغل وإنت مش عارف". هنا الحل المنظّم: **60 يوم إشعار + بديل موصى بيه + migration guide**. بس **الشغل لسه عليك**: لازم يبقى عندك **eval set** تشغّله على البديل، وإلا الـ 60 يوم مش هيفيدوك.

### 4.3 Deprecation downsides and mitigations (ص 2–3)
Anthropic بتعترف إن الـ retirement ليه **عيوب**: اللي بيحبوا موديل معيّن لازم ينقلوا، والباحثين بيخسروا موديلات بيدرسوها، وفيه مخاطر تانية (safety و "model welfare"). والتزامهم: **يحتفظوا بالـ weights** على المدى الطويل، ويتمنوا يرجّعوا الموديلات القديمة متاحة في يوم.

### 4.4 Model status (ص 3–5)
جدول بكل الموديلات وحالتها وتاريخ الـ retirement. (⚠️ **الجدول ده اتلخبط جداً في الـ PDF**، الأعمدة داخلة في بعض. افتحه أونلاين لو عايز تقرا صف معيّن.) الواضح منه: الموديلات الحالية (Fable 5.2، و Opus 5.5، و Sonnet 5.5، و Haiku 5.5) **Active**، وفيه موديلات **Retired** زي Opus 4 و Haiku 3.

### 4.5 Deprecation history (ص 5–8) ⭐
هنا تقدر تشوف **الموديل بيعيش قد إيه فعلاً**. أمثلة واضحة في الملف:

| الموديل | اتبلّغ إمتى | اتشال إمتى | البديل الموصى بيه |
|---|---|---|---|
| Claude 1 و Instant | 2024-09-04 | 2024-11-06 | `claude-haiku-4-5-20251001` |
| Claude 2 و 2.1 و Sonnet 3 | 2025-01-21 | 2025-07-21 | Opus 4.8 / Sonnet 5.5 |
| `claude-3-5-sonnet-20240620` | 2025-08-13 | 2025-10-28 | `claude-sonnet-5-5` |
| `claude-3-opus-20240229` | 2025-06-30 | 2026-01-05 | `claude-opus-4-8` |
| Opus 4 و Sonnet 4 | 2026-04-14 | 2026-06-15 | Opus 4.8 / Sonnet 5.5 |
| Opus 4.1 | 2026-06-05 | 2026-08-05 | `claude-opus-4-8` |
| **Sonnet 4.5** (`claude-sonnet-4-5-20250929`) | **2026-09-30** | **2026-11-30** | `claude-sonnet-5-5` |

**الملاحظات:**
- **الفترة بين الإشعار والـ retirement غالباً شهرين لـ 6 شهور.**
- **`claude-3-5-sonnet-20240620`** نزل يونيو 2024 واتشال أكتوبر 2025، يعني **عاش حوالي 16 شهر**. فخلّي في دماغك إن **عمر الموديل على الـ API سنة لسنتين تقريباً**.
- **Sonnet 4.5 هيتشال يوم 30 نوفمبر 2026**، يعني بعد **أسبوعين ونص** من النهارده! لو كان عندك تطبيق عليه، كنت المفروض تكون بدأت الـ migration.
- لاحظ إن الـ IDs القديمة فيها **تاريخ** (`claude-3-5-sonnet-20240620`) يعني الـ version نفسه متثبّت في الاسم. وده بيخلّي "الموديل اللي بتكلّمه" واضح، بس لما يتشال لازم **تغيّر الـ ID في الكود**. (فكرة تانية لـ `LLM_MODEL` في `.env`.)

### 4.6 API parameter deprecations (ص 8) ⭐
مش بس الموديلات اللي بتتشال، **الـ parameters كمان**:
- **`temperature` و `top_p` و `top_k`**: **اتشالوا** في API version **2026-10-21**، وبيرجّعوا **400 error**. وفي الـ versions الأقدم، بيرجّعوا error لو بعتهم بقيمة مش default على موديلات **4.7 وأحدث**.
- **البديل:** متبعتهمش، واستخدم **الـ prompting** عشان توجّه سلوك الموديل.

**ربط بـ Step 02:** فاكر في شرح Ch.2 إن "أحدث موديلات Claude شالت الـ temperature"؟ أهو الـ source الرسمي. وده **سبب** إن كل تجارب الـ sampling في Step 02 كانت على Ollama. وده كمان مثال حي على الكتاب: **"إنت محدود بالـ features اللي الـ API بيدّيها"** (محور الـ functionality). على Ollama، الـ temperature في إيدك. على Claude API، لأ.

**ودرس للكود بتاعك:** لو عملت abstraction واحد لكل الـ providers (`chat(messages, temperature=...)`)، لازم تفكر: **الـ provider مبيدعمش parameter معيّن، تعمل إيه؟** تتجاهله؟ ترمي error؟ تعمل warning؟ ده قرار تصميم هتاخده في التاسكات.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md) تحت "Step 03 (المصدر 3)":
**Model Tiers (Haiku / Sonnet / Opus / Fable)** · **Effort Parameter** · **Efficiency-first مقابل Capability-first** · **Capability Discovery (Models API)** · **Input مقابل Output Pricing (MTok)** · **Cost per Task (والـ Tokenizer)** · **Prompt Caching** · **Batch API** · **Data Residency و Regional Endpoints** · **Fast Mode** · **Hidden Token Overhead (Tools)** · **Model Lifecycle (Active / Legacy / Deprecated / Retired)** · **Parameter Deprecation** · **Multimodel Strategy (Executor/Advisor، Orchestrator/Workers)**
(والـ usage tiers متسجّلة مع **Rate Limits و TPM** تحت المصدر 1.)

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. ليه سعر الـ output token أغلى من الـ input token بـ 5 مرات تقريباً؟ وإيه تأثير ده على تصميمك؟</summary>

لأن الـ input بيتعالج **مرة واحدة** وبالتوازي (prefill)، أما الـ output بيتولّد **token ورا token** (decode)، وكل token محتاج pass كامل في الموديل، فده compute ووقت أكتر. التأثير: **الرد الطويل أغلى بكتير** من الـ prompt الطويل. فأطلب ردود مختصرة، وأحط `max_tokens`، وأطلب structured output بدل كلام كتير، ولو الموديل بيفكّر (thinking) أظبط الـ effort، لأن الـ thinking tokens بتتحسب output.
</details>

<details><summary>2. موديل A بـ $3/MTok input، وموديل B بـ $4/MTok input. أيهم أرخص؟</summary>

**مش هقدر أقول من السعر بس.** لازم أعرف: (1) كل واحد بيطلّع **كام token لنفس النص** (الـ tokenizer: Anthropic نفسها بتقول إن الـ tokenizer الجديد بيطلّع ~30% tokens أكتر، والعربي بيختلف جامد)، (2) **كام output token** بيطلّع لنفس المهمة (موديل بيرغي أكتر، أو بيفكّر أكتر، هيكلّف أكتر)، و (3) سعر الـ output. المقياس الصح هو **cost per task**: أشغّل الاتنين على نفس الـ eval set وأحسب التكلفة الفعلية من الـ `usage`.
</details>

<details><summary>3. إيه الفرق بين efficiency-first و capability-first؟ ومين فيهم الكتاب نصح بيه؟ وإمتى تختار التاني؟</summary>

**Efficiency-first:** تبدأ بأرخص/أسرع موديل (Haiku) وترقّي بس لو لازم. **Capability-first:** تبدأ بالأقوى (Opus)، تظبط الـ prompts، وبعدين تنزل (effort أقل أو موديل أرخص).
الكتاب نصح بـ **capability-first** في الـ prompt engineering، عشان تعرف المهمة ممكنة أصلاً، ويبقى عندك سقف تقارن بيه.
أختار efficiency-first لما المهمة **واضح إنها بسيطة** (تصنيف، استخراج)، وبحجم كبير، والتكلفة أو الـ latency حساسة. ولو الصغير فشل، أجرب الأقوى عشان أعرف هل المشكلة في الموديل ولا في الـ prompt.
</details>

<details><summary>4. إيه الـ effort parameter؟ وليه Anthropic بتقول إنه غالباً أحسن من تغيير الموديل؟</summary>

زرار جوه **نفس الموديل** بيحدد يفكّر قد إيه (thinking أكتر = أدق غالباً، بس أبطأ وأغلى لأن الـ thinking tokens output). أحسن من تغيير الموديل لأن: نفس الموديل = نفس السلوك والـ prompts والـ quirks، فمفيش migration ولا breaking changes، والتغيير أسهل وأسرع (parameter واحد). وتقدر تستخدم effort مختلف لكل نوع request في نفس التطبيق. ده **test time compute** (Step 02) بقى زرار.
</details>

<details><summary>5. احسب: تطبيق بيبعت 3,000 token input و 400 output لكل request، و 50,000 request في الشهر. التكلفة على Opus 5.5 وعلى Haiku 5.5؟ ولو حطيت 2,500 token من الـ input في prompt caching (hit) على Opus 5.5؟</summary>

input = 3,000 × 50,000 = 150M. output = 400 × 50,000 = 20M.
**Opus 5.5:** 150 × $4 + 20 × $20 = $600 + $400 = **$1,000**.
**Haiku 5.5** (prompt أقل من 100K): 150 × $0.10 + 20 × $0.50 = $15 + $10 = **$25**.
**Opus 5.5 مع caching:** الـ uncached input = 500 × 50,000 = 25M × $4 = $100. الـ cached = 2,500 × 50,000 = 125M × $4 × 0.05 = $25. والـ output $400. المجموع **≈ $525** (ومن غير ما نحسب تكلفة كتابة الـ cache أول مرة، ودي صغيرة لو الـ cache بيتقري كتير). يعني الـ caching قلّل حوالي النص، والـ output بقى أكبر جزء في الفاتورة.
</details>

<details><summary>6. إمتى تستخدم Batch API؟ وإمتى Fast mode؟ وإيه علاقتهم بكلام الكتاب عن الـ latency؟</summary>

**Batch:** للحاجات **اللي مش مستعجلة** (تصنيف داتا قديمة، تلخيص بالليل، تشغيل evals). خصم **50%**، والرد بييجي بعدين. **Fast mode:** لما الـ latency **must-have** (مثلاً real-time مع عميل)، وبتدفع **ضعف** السعر تقريباً لـ 2.5× سرعة.
الكتاب قال فرّق بين الـ latency الـ **must-have** والـ **nice-to-have**. الاتنين دول بيحطوا **تمن** للفرق ده: لو الـ latency مش مهمة، ادفع نص التمن (batch). لو مهمة جداً، ادفع الضعف (fast). وأغلب الحالات في النص بالسعر العادي.
</details>

<details><summary>7. شركتك عايزة الـ inference يحصل في أمريكا بس لأسباب قانونية. إيه الخيارات اللي في الصفحات دي؟ وبكام؟</summary>

على Claude API: **`inference_geo: "us"`** بـ **1.1×** على كل الأسعار (input، و output، و cache). أو على Bedrock أو Google Cloud: **regional endpoints** (أغلى بـ 10% من الـ global، وكل platform ليه أسعاره). ولو الشرط "الداتا متخرجش من الشركة خالص"، يبقى ولا واحد فيهم، وأروح لـ self-hosting. يعني الـ data residency درجة في النص بين "global API" و "local"، وليها تمن.
</details>

<details><summary>8. ليه لازم تسأل Models API عن الـ capabilities بدل ما تكتبها في الكود؟ وإيه المقابل في Ollama؟</summary>

لأن الموديلات **مختلفة** في القدرات (مثلاً Sonnet 5.5 مبيقبلش `thinking: disabled`، والـ effort levels بتختلف)، والـ capabilities **بتتغيّر** مع الموديلات الجديدة. لو hard-coded، هتبوظ أول ما تبدّل موديل. و `lifecycle` و `retires_at` بيقولولك الموديل هيتشال إمتى. وكمان "اقرا `line` ومتستنتجش من الـ `id`". المقابل في Ollama: **`ollama show`** أو **`/api/show`** (الـ capabilities، والـ context length، والـ parameters).
</details>

<details><summary>9. إيه الفرق بين deprecated و retired؟ وإيه اللي المفروض تعمله لما موديل بتستخدمه يبقى deprecated؟</summary>

**Deprecated:** لسه **شغّال**، بس مش موصى بيه، وليه بديل وتاريخ retirement. **Retired:** **مبقاش متاح**، أي request بيفشل.
لما يبقى deprecated: (1) أعرف كل الأماكن اللي بتستخدمه (الـ usage audit من الـ Console)، (2) أشغّل الـ **eval set** بتاعي على البديل الموصى بيه، (3) أظبط الـ prompts لو الأداء اختلف، وأتأكد من الـ breaking changes، (4) أغيّر الـ model ID (والأحسن يبقى في config/`.env` مش متوزّع في الكود)، و (5) أعمل ده **بدري**، مش في آخر أسبوع.
</details>

<details><summary>10. من جدول الـ deprecation history، الموديل بيعيش قد إيه تقريباً على الـ API؟ وإزاي ده يأثر على قرار build vs buy؟</summary>

حوالي **سنة لسنتين** (مثلاً `claude-3-5-sonnet-20240620`: يونيو 2024 لأكتوبر 2025، حوالي 16 شهر)، والإشعار قبلها بشهرين لـ 6 شهور.
التأثير: لو استخدمت API، لازم أخطط لـ **migration كل سنة تقريباً** (eval set، و prompts، و tests). ده **تكلفة engineering مستخبية** في الـ "buy". لو التطبيق في مجال regulated (لازم الموديل ميتغيّرش)، أو مفيش فريق يعمل migrations، ده سبب يخليني أفكر في **open weights** (الموديل ملف عندي، مش هيتشال). بس ساعتها أنا اللي بشغّل وبصون وبعمل security updates.
</details>

<details><summary>11. Anthropic شالت temperature و top_p و top_k من الـ API. إيه تأثير ده على client واحد بيدعم Ollama و Claude؟</summary>

الـ interface الموحّد (`chat(messages, temperature=..., top_k=...)`) مش هينفع يبعت نفس الـ parameters للاتنين: Ollama بيدعمهم، و Claude (الـ API version الجديد) هيرجّع **400**. لازم أقرر في التصميم: كل provider adapter **يشيل** الـ parameters اللي مش بيدعمها (مع warning أو log)، أو **يرمي error واضح** ("temperature not supported by this provider")، أو أخلّي الـ parameters دي **provider-specific options** مش جزء من الـ interface المشترك. الأوضح غالباً error أو warning صريح، عشان محدش يفتكر إن الـ temperature اتطبّقت وهي متطبقتش. وده بالظبط trade-off الكتاب: الـ standard API بيسهّل التبديل، بس بيخبي فروق الـ features.
</details>

<details><summary>12. "Combine models": اشرح فكرة executor/advisor بمثال من شغلك، وليه بتوفّر.</summary>

مثال: نظام بيرد على أسئلة الموظفين عن سياسات الشركة. الـ **executor** (موديل رخيص، Haiku أو موديل local) بيرد على 90% من الأسئلة السهلة. ولما يقابل سؤال صعب أو مش متأكد (مثلاً سؤال فيه استثناء قانوني)، يحوّله لـ **advisor** (Opus). بيوفّر لأن **أغلب الـ tokens** بتتحاسب بالسعر الرخيص، والموديل الغالي بيشتغل بس على القرارات اللي محتاجاه. وممكن كمان يخدم الـ privacy: الـ executor local للداتا الحساسة، والـ advisor cloud للأسئلة العامة بس.
</details>
