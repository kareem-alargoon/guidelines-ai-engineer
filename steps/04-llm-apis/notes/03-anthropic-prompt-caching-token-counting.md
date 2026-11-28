# شرح: Anthropic docs — Prompt caching، و Token counting

> **المصدر:** [Claude Platform Docs](https://platform.claude.com/docs/) — صفحتين، النسخة اللي اتحفظت يوم **2026-11-28**
> **الملفات:**
> - `resources/articles/04-anthropic-prompt-caching.pdf` ← *Prompt caching* (حوالي 40 صفحة)
> - `resources/articles/04-anthropic-token-counting.pdf` ← *Token counting* (185 صفحة، بس **الشرح الحقيقي في أول صفحة وفي آخر ~10 صفحات**. الباقي نسخة كاملة من الـ API reference للـ endpoint، **متقراهوش**)
>
> **إزاي تقرا:** صفحة الـ caching طويلة وكثيفة، اقراها على قعدتين (جزء 1–6 وبعدين 7–12). والـ 📍 فيه اسم الـ section بدل رقم الصفحة، لأن الـ PDF بيقسم الصفحات في أماكن غريبة.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

في Step 03 حسبت تكلفة الإيصالات في `cost.py` بعمود "cache" (`CACHED_RATIO = 0.5`)، وكان فيه سؤالين **اتأجلوا لـ Step 04**:
1. **إيه الحد الأدنى لطول الـ prompt عشان يتعمله cache في Claude؟** (لأن الـ system prompt بتاعك ~172 token بس.)
2. **الفرق الحقيقي في عدد الـ tokens بين tokenizer الـ Qwen و Claude** (لأن `cost.py` بيحسب بأرقام Qwen).

الصفحتين دول فيهم الإجابتين (جزء 7 وجزء 13 تحت). وكمان فيهم حاجة أهم: **الـ `usage` بتاع Anthropic بيتحسب بشكل مختلف** عن اللي `cost.py` مفترضه.

> ⏳ **عمر المصدر:** **الأسعار** في جدول الـ caching snapshot يوم 2026-11-28 (نفس أرقام `prices.json` من Step 03 لـ Haiku/Sonnet/Opus 5.5 و Fable 5.2). **الحدود الدنيا** و **الـ TTLs** بتتغيّر مع الموديلات الجديدة. اتعلّم **إزاي تتأكد** (حقول الـ `usage`)، مش الأرقام.

---

# الجزء الأول: Prompt caching

## 1. المقدمة: إيه هو الـ prompt caching؟
> 📍 أول صفحة (قبل *How prompt caching works*)

**الفكرة:** الـ API بيقدر **يكمّل من prefix محفوظ** من الـ prompt بتاعك بدل ما يقراه من الأول. ده بيقلل **الوقت والتكلفة** للمهام المتكررة.

**ليه ده ممكن أصلاً؟** افتكر من Step 02: الموديل وهو بيقرا الـ prompt (الـ **prefill**) بيبني **KV cache** لكل token. لو request جديد بيبدأ **بنفس الـ tokens بالظبط**، الـ KV cache بتاع الجزء ده ممكن يتعاد استخدامه، فالموديل يقرا الجزء الجديد بس. ده بالظبط اللي شفته في Step 03 Task 3 على Ollama: نفس الـ prompt المتكرر، الـ prompt eval نزل من 0.23 لـ 0.04 ث. Ollama بيعمله **لوحده**، و Anthropic بتخليك **تتحكم فيه وتتحاسب عليه** بشكل مختلف.

**فيه طريقتين:**
- **Automatic caching:** `cache_control` **واحد** في أعلى الـ request. الـ API بيحط الـ "breakpoint" على **آخر block** ممكن يتعمله cache، وبيحرّكه لقدام والمحادثة بتكبر. **أحسن حاجة للـ multi-turn.**
- **Explicit cache breakpoints:** `cache_control` على **blocks معيّنة** بإيدك، لتحكم دقيق.

وعلى **Managed Agents** الـ caching شغّال دايماً.

**المثال الأول:**
```python
client.messages.create(model=..., max_tokens=1024,
    cache_control={"type": "ephemeral"},     # ده كل اللي اتضاف
    system="You are an AI assistant tasked with analyzing literary works...",
    messages=[...])
```

**تشبيه من Laravel:** زي `Cache::remember()` بس على مستوى **الـ prefix**: المفتاح (الـ key) = **hash لكل الـ tokens لحد نقطة معيّنة**. أي تغيير ولو حرف واحد قبل النقطة دي = مفتاح مختلف = cache miss. ⚠️ والتشبيه مضلل في حاجة: في Laravel إنت بتحط **الناتج** في الـ cache، هنا الـ cache هو **حالة الموديل الداخلية** بعد ما قرا الـ prefix، و**الرد نفسه مش بيتعمله cache** (جزء 10).

## 2. How prompt caching works
> 📍 section *How prompt caching works*

**الفكرة:** لما تبعت request بالـ caching:
1. الـ API بيشوف: الـ prefix لحد الـ breakpoint **موجود في الـ cache** من request قريب؟
2. لو أيوه: بيستخدمه (أسرع وأرخص).
3. لو لأ: بيقرا الـ prompt كله، و**يكتب الـ prefix في الـ cache** أول ما الرد يبدأ.

**مفيد لـ:** prompts فيها أمثلة كتير، أو context كبير، أو مهام متكررة بنفس التعليمات، أو محادثات طويلة.

**الـ lifetime (TTL):**
- by default **5 دقايق**، و**بيتجدد ببلاش** كل مرة الـ cache يتستخدم.
- الـ 5 دقايق بتتحسب من **بداية** الـ request اللي كتب أو قرا، **مش من آخر الرد**. يعني لو الرد خد 4 دقايق streaming، فاضلك دقيقة واحدة بعده.
- لو 5 دقايق قليلة: فيه **ساعة** بسعر أعلى.

**الترتيب:** الـ cache بيغطي الـ prefix كله بالترتيب ده: **`tools` ← `system` ← `messages`**، لحد الـ block اللي عليه `cache_control`.

## 3. Pricing
> 📍 section *Pricing* (جدولين)

**الفكرة:** الـ caching ليه أسعار خاصة. الـ multipliers:

| النوع | السعر بالنسبة للـ base input |
|---|---|
| **Cache write (5 دقايق)** | **1.25x** (أغلى من الـ input العادي بـ 25%) |
| **Cache write (ساعة)** | **2x** |
| **Cache read (hit)** | **0.1x** (والاستثناءات تحت) |

**الاستثناءات (footnotes الجدول):** الـ cache hits على Fable 5.2 و Mythos 5.2 و Fable 5.1 و Mythos 5.1 = **0.025x**، وعلى **Opus 5.5 و Sonnet 5.5 = 0.05x**، والباقي (ومنهم **Haiku 5.5**) = 0.1x.

**أمثلة من الجدول (per MTok):**

| الموديل | Input | 5m write | 1h write | Hit |
|---|---|---|---|---|
| Haiku 5.5 (prompts ≤ 100K) | $0.10 | $0.125 | $0.20 | $0.01 |
| Sonnet 5.5 | $2 | $2.50 | $4 | $0.10 |
| Opus 5.5 | $4 | $5 | $8 | $0.20 |
| Fable 5.2 | $8 | $10 | $16 | $0.20 |

وده نفس اللي في `prices.json` بتاعك. والـ multipliers دي **بتتجمع** مع خصم الـ Batch وغيره.

**⚠️ النقطة اللي `cost.py` مش حاسبها:** أول مرة (الـ **write**) **أغلى** من request من غير caching (1.25x). يعني الـ caching **بيكسب بس لو الـ prefix اتقرا تاني** خلال الـ TTL. لو بتبعت request كل 10 دقايق بـ cache 5 دقايق، كل request = write، وإنت **بتدفع أكتر** من غير caching!

**حسبة سريعة (Haiku 5.5، prefix ألف token):**
- من غير caching: 1000 × $0.10/MTok = $0.0001 كل request.
- بالـ caching: أول request $0.000125 (write)، وكل request بعده خلال 5 دقايق $0.00001 (hit). يعني من تاني request إنت كسبان.

## 4. Supported models، و Automatic caching
> 📍 sections *Supported models* و *Automatic caching*

**الفكرة:** كل الموديلات الـ active بتدعم الاتنين.

**Automatic caching في محادثة:** الـ breakpoint بيتحرك لوحده لآخر block:

| Request | المحتوى | اللي بيحصل |
|---|---|---|
| 1 | System + User(1) + Asst(1) + User(2) ◀ | كله **write** |
| 2 | ... + Asst(2) + User(3) ◀ | لحد User(2) **read**، و Asst(2) + User(3) **write** |
| 3 | ... + Asst(3) + User(4) ◀ | لحد User(3) **read**، والجديد **write** |

يعني في كل turn بتدفع سعر الـ hit على التاريخ القديم كله، وسعر الـ write على الجديد بس. **ده مثالي للـ chat CLI.**

**TTL ساعة:** `{"cache_control": {"type": "ephemeral", "ttl": "1h"}}`.

**مع explicit breakpoints:** ينفعوا مع بعض، والـ automatic بياخد **واحد من الـ 4 breakpoints** المتاحين.

**Edge cases:** لو آخر block عليه `cache_control` بنفس الـ TTL ← مفيش حاجة بتحصل. بـ TTL مختلف ← 400. لو فيه 4 explicit ← 400 (مفيش مكان). لو آخر block مش ينفع ← بيرجع لورا لحد block ينفع. **ومش متاح على Bedrock (`bedrock-runtime`)**.

## 5. Explicit cache breakpoints — إزاي الـ lookup بيشتغل
> 📍 section *Explicit cache breakpoints*

**Structuring your prompt:** حط الحاجات **الثابتة** (tools، و system instructions، و context، و examples) **في الأول**، وحط `cache_control` في **آخر حاجة ثابتة**.

**3 مبادئ أساسية (اقراهم بتركيز):**
1. **الـ write بيحصل عند الـ breakpoint بس.** الـ `cache_control` بيكتب entry **واحدة**: hash للـ prefix لحد الـ block ده. ومفيش entries لأماكن قبله. والـ hash تراكمي، فأي تغيير في أي block **قبل أو عند** الـ breakpoint = hash مختلف.
2. **الـ read بيدوّر لورا على entries كتبتها requests قبل كده.** لو مفيش entry عند الـ breakpoint، بيرجع block block لورا. **بيدوّر على writes قديمة، مش على محتوى ثابت.**
3. **الـ lookback window = 20 block.** لو مالقاش في 20 مكان، بيقف.

**الغلطة الشائعة (مهمة جداً):** عندك system context ثابت كبير (blocks 1–5)، وبعده block 6 فيه **timestamp** ورسالة اليوزر، وحطيت `cache_control` على block 6:
- Request 1: write عند block 6 (والـ hash فيه الـ timestamp).
- Request 2: الـ timestamp اتغيّر ← hash مختلف ← بيدوّر لورا في 5، 4، 3... بس **محدش كتب entry هناك**. ← **مفيش hit أبداً**، وبتدفع write (1.25x) كل مرة!
- **الحل:** `cache_control` على **block 5** (آخر حاجة ثابتة).

**والـ automatic caching بيقع في نفس الغلطة** في الحالة دي، لأنه بيحط الـ breakpoint على آخر block (اللي بيتغيّر). فاستخدم explicit.

**💡 ربط مباشر بالإيصالات:** الـ request بتاعك = `system` (ثابت) + user message (نص الإيصال، **بيتغيّر كل مرة**). يعني الـ breakpoint لازم يبقى **على الـ system prompt**، مش automatic (اللي هيحطه على نص الإيصال).

**Multiple breakpoints (لحد 4):** لما يبقى عندك أجزاء بتتغيّر بسرعات مختلفة (tools نادراً، و context يومياً)، أو محادثة بتكبر أكتر من 20 block بين كل write والتاني.

**التكلفة:** الـ breakpoints نفسها **ببلاش**. بتدفع بس على اللي اتكتب واتقرا فعلاً.

## 6. What can and cannot be cached
> 📍 sections *What can be cached* و *What cannot be cached*

**ينفع:** tool definitions، و system blocks، و text messages (user و assistant)، و images و documents (في user turns)، و tool use و tool results.

**ماينفعش:** thinking blocks مباشرة بـ `cache_control` (بس بتتعمل cache مع المحتوى لو في turns قديمة، و**بتتحسب input tokens** لما تتقري)، و sub-blocks زي citations (اعمل cache للـ document الأصلي)، و **text blocks فاضية**.

## 7. ⭐ Cache limitations: الحد الأدنى (إجابة السؤال الأول اللي اتأجل)
> 📍 section *Caching strategies and considerations* ← *Cache limitations*

**الفكرة:** فيه **حد أدنى لطول الـ prompt** اللي يتعمله cache (على Claude API و AWS و Google managed و Foundry):

| الحد الأدنى | الموديلات |
|---|---|
| **512 token** | Fable 5.2، و Mythos 5.2، و Fable 5.1، و Mythos 5.1، و **Opus 5.5**، و Opus 5، و **Sonnet 5.5**، و Fable 5، و Mythos 5، و **Haiku 5.5** |
| **1,024 token** | Opus 4.8، و Sonnet 5، و Sonnet 4.6، و Sonnet 4.5، و Opus 4.1، و Opus 4، و Sonnet 4 |
| **2,048 token** | Mythos Preview، و Opus 4.7 |
| **4,096 token** | Opus 4.6، و Opus 4.5، و **Haiku 4.5** |

**والأخطر:** الـ prompts الأقصر **مش بتتعمل cache حتى لو عليها `cache_control`**، و**مفيش error**. بتتعالج عادي من غير caching. تعرف إزاي؟ من الـ `usage`: لو **`cache_creation_input_tokens` و `cache_read_input_tokens` الاتنين 0**، يبقى مفيش caching (غالباً عشان الحد الأدنى).

**النصيحة:** لو الـ prompt **قريب من الحد**، غالباً **يستاهل تطوّله** لحد ما يعدّيه، لأن الـ cache reads أرخص بكتير.

**وكمان:** في الـ requests المتوازية، الـ cache entry بتبقى متاحة **بعد ما أول رد يبدأ**. لو عايز hits لـ requests متوازية، **استنى أول رد** قبل ما تبعت الباقي. (ده هيفرق في Task 7: الـ async.)

**وفي الآخر:** `ephemeral` هو النوع الوحيد.

### 🎯 الإجابة لـ `cost.py` بتاعك
- الـ system prompt بتاع الإيصالات ≈ **172 token** بـ tokenizer الـ Qwen.
- الحد الأدنى لـ Haiku 5.5 (و Sonnet/Opus 5.5) = **512**.
- حتى لو Claude بيطلّع tokens أكتر من Qwen (جزء 13)، 172 بعيدة جداً عن 512.
- **يعني عمود الـ cache في `cost.py` (`CACHED_RATIO = 0.5`) مش هيحصل في الحقيقة** بالـ prompt الحالي. الـ request هيتحاسب كله input عادي، والـ `usage` هيقولك `cache_read_input_tokens: 0`.
- **عشان الـ caching يشتغل:** لازم الـ prefix الثابت يعدّي 512 token. والطريقة المنطقية: **few-shot examples** (إيصالين أو تلاتة بالـ JSON الصح) في الـ system prompt. ده **ممكن** كمان يحسّن الدقة (الغلطات في Step 03 كانت في الـ vendor). وده بالظبط اللي الـ docs بتقترحه في جزء 11 ("20+ diverse examples" مع الـ caching). هتحسب ده في Task 8.
- ⚠️ **وعلى الحجم بتاعك (1,760 إيصال/شهر):** التكلفة أصلاً سنتات، فالـ caching هنا **تمرين فهم**، مش توفير حقيقي. هيفرق في الـ chat (التاريخ بيكبر) وفي RAG (Step 09).

## 8. What invalidates the cache
> 📍 section *What invalidates the cache*

**الفكرة:** الـ hierarchy: **tools ← system ← messages**. تغيير في مستوى بيمسح المستوى ده **وكل اللي بعده**:

| التغيير | Tools cache | System cache | Messages cache |
|---|:---:|:---:|:---:|
| Tool definitions | ✘ | ✘ | ✘ |
| Web search / Citations toggle | ✓ | ✘ | ✘ |
| Speed setting (fast) | ✓ | ✘ | ✘ |
| `tool_choice` | ✓ | ✓ | ✘ |
| إضافة/شيل صور | ✓ | ✓ | ✘ |
| Thinking parameters / Effort | حسب الموديل | حسب الموديل | ✘ |

**و2 حاجات جديدة على الموديلات الحديثة:**
- **الـ thinking blocks بتتحفظ by default** على Opus 4.5+، و Sonnet 4.6+، و Haiku 5.5، و Fable، و Mythos، فالـ cache بيفضل valid. على الموديلات التانية بتتشال وبتبوظ الـ cache.
- **Mid-conversation system message** (الشرح 02، جزء 1.3): تقدر تضيف تعليمات في النص **من غير ما تمسح** الـ system cache. وكمان tool جديد في النص بـ beta header.

**وفي الشرح 02:** تغيير `output_config.format` (structured outputs) بيمسح الـ prompt cache.

## 9. Tracking cache performance — ⭐ الـ `usage` بيتحسب إزاي
> 📍 sections *Tracking cache performance* و *Understanding the token breakdown*

**الفكرة:** في `usage` (أو `message_start` في الـ streaming):
- **`cache_creation_input_tokens`**: tokens **اتكتبت** في الـ cache دلوقتي.
- **`cache_read_input_tokens`**: tokens **اتقرت** من الـ cache.
- **`input_tokens`**: الـ tokens **بعد آخر breakpoint** (اللي مش متعملها cache ولا اتكتبت).

**⚠️ أهم جملة لكودك:** `input_tokens` **مش** كل الـ input، ده الجزء **بعد آخر breakpoint** بس. والإجمالي:

```
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

**مثال الـ docs:** 100,000 token مقروين من الـ cache، و 0 اتكتبوا، و 50 في رسالة اليوزر ← `cache_read: 100000`، و `cache_creation: 0`، و `input_tokens: 50`. الإجمالي **100,050**.

### 🎯 ده بيتعارض مع `cost.py` إزاي؟
في `cost.py`، `request_cost()` بتفترض إن **`cached_tokens` جزء من `input_tokens`** (`uncached = input_tokens - cached_tokens`). ده صح لـ **OpenAI API** (Step 03 Task 5: `cached_tokens` في الـ OpenAI compatibility كان جزء من `prompt_tokens`). بس في **Anthropic** الـ 3 أرقام **منفصلين** ومابيتداخلوش. ولو دخّلت `usage` بتاع Anthropic في `request_cost()` زي ما هو، الحساب هيطلع **غلط** (ولو `cache_read > input_tokens`، الدالة هترمي `ValueError`!). وكمان `cost.py` **مابيحسبش الـ cache writes** (1.25x).

ده **نفس الكلمة "input tokens" بمعنيين مختلفين** حسب الـ provider، وده سبب إن الـ abstraction بتاعك (`ChatResult`) لازم يقرر معنى واحد. هتصلّحه في Task 8.

**تشبيه من Laravel:** زي API بيرجّع `total` في provider "شامل الضريبة" وفي provider تاني "من غير ضريبة". لو كتبت invoice service واحدة وماعملتش normalize، الأرقام هتطلع غلط من غير أي error.

## 10. Caching with thinking blocks، و Cache storage and sharing
> 📍 sections *Caching with thinking blocks* و *Cache storage and sharing*

**Thinking:** الـ thinking blocks بتتعمل cache كجزء من المحتوى لما ترجعها في tool use، و**بتتحسب input tokens** لما تتقري من الـ cache. (Step 10–11.)

**Storage and sharing (مهم للـ privacy):**
- **Organization isolation:** organizations مختلفة **عمرها ما بتشارك** cache، حتى لو الـ prompts متطابقة.
- **Workspace isolation:** على Claude API (وغيره)، كمان كل workspace ليه cache لوحده.
- **Exact matching:** الـ hit محتاج **تطابق 100%** لكل النص والصور لحد الـ breakpoint.
- **"Prompt caching has no effect on output token generation":** الرد **نفس الرد** اللي كان هيطلع من غير caching.

**⚠️ قارن بـ Ollama (Step 03):** في Ollama شفت إن الرد **اتغيّر** مع الـ prompt caching (70 ← 86 token مع `temperature=0`)، وفي Task 5 الـ prompt العربي اختلف بسبب الـ cache. Anthropic بتقول إن ده **مش بيحصل عندها**. الفرق ده نفسه درس: **"caching" مش حاجة واحدة**، كل provider بيعمله بطريقة، وبنتايج مختلفة.

## 11. Best practices، و use cases، و Troubleshooting
> 📍 sections *Best practices*، و *Optimizing for different use cases*، و *Troubleshooting*

**Best practices:** ابدأ بالـ automatic للمحادثات، واستخدم explicit لما الأجزاء بتتغيّر بسرعات مختلفة، واعمل cache للحاجات الثابتة، وحطها في الأول، و**حط الـ breakpoint على آخر block ثابت**، وراقب الـ hit rate.

**Use cases:** conversational agents، و coding assistants، و مستندات كبيرة، و **detailed instruction sets** ("20+ diverse examples" بدل مثال أو اتنين، لأن الـ caching بيخليهم رخاص)، و agentic tool use، و Q&A على كتب ومستندات.

**Troubleshooting (لو مفيش hits):** الأجزاء متطابقة؟ الـ markers في نفس المكان؟ جوه الـ TTL؟ `tool_choice` والصور والـ thinking والـ effort ثابتين؟ **عدّيت الحد الأدنى؟** الـ breakpoint على block ثابت؟ ترتيب الـ keys في JSON ثابت؟ (بعض اللغات زي Go بتلخبط ترتيب الـ keys، **Python dicts بتحافظ على الترتيب** فإنت آمن.) وفيه **cache diagnostics** (الـ API بيقارن requests متتالية ويقولك اختلفوا فين).

## 12. 1-hour cache، و Pre-warming، و Examples، و FAQ
> 📍 sections *1-hour cache duration* لآخر الصفحة

### 1-hour cache
**إمتى؟** لو الـ prompt بيتستخدم **أقل من كل 5 دقايق بس أكتر من كل ساعة** (agent جانبي بياخد أكتر من 5 دقايق، أو يوزر في chat ممكن يرد بعد 10 دقايق)، أو الـ latency مهمة، أو عايز تحسّن الـ rate limits (الـ cache reads **مش بتتحسب** في الـ ITPM، الشرح 04). ولو بتبعت أكتر من كل 5 دقايق: خليك على الـ 5 دقايق (بتتجدد ببلاش).

الرد بيقسم الـ writes: `"cache_creation": {"ephemeral_5m_input_tokens": 148, "ephemeral_1h_input_tokens": 100}`، و `cache_creation_input_tokens` = مجموعهم (248). **ده مثال حلو لـ test** في Task 8.

**Mixing TTLs:** الـ 1h لازم **قبل** الـ 5m. والفاتورة بتتقسم لـ 3 مواضع (A: آخر hit، و B: آخر 1h breakpoint بعد A، و C: آخر breakpoint): read لـ A، و 1h write لـ (B − A)، و 5m write لـ (C − B). (متقدم، اقراه للفهم بس.)

### Pre-warming the cache
**الفكرة:** تبعت request بـ **`max_tokens: 0`** قبل ما اليوزرز ييجوا: الـ API بيقرا الـ prompt ويكتب الـ cache ويرجع **فوراً** من غير توليد (`content: []`، و `stop_reason: "max_tokens"`، و **0 output tokens بتتحاسب**). فأول يوزر ياخد TTFT أحسن.
- الـ breakpoint لازم على الجزء **المشترك** (الـ system)، مش على رسالة الـ "warmup"، يعني **explicit** مش automatic.
- **مش مسموح** مع: `stream: true`، و extended thinking، و **structured outputs**، و `tool_choice` بـ `any`/`tool`، و جوه Batches.
- وخليك فاكر الـ TTL: pre-warm كل 5 دقايق، أو استخدم الساعة.
- وده أحسن من الـ workaround القديم `max_tokens: 1`.

**ربط بـ Step 03:** ده نفس فكرة **`load_model()`** اللي عملتها لـ Ollama (preload قبل أول request عشان الـ cold start)، بس على مستوى الـ prompt مش الموديل.

### Examples
**الفكرة:** أمثلة كود: **large context** (مستند 50 صفحة في الـ system عليه `cache_control`، وأول request الـ `cache_creation` = المستند، والباقي `cache_read`)، و **tool definitions** (`cache_control` على آخر tool)، و **multi-turn** (على آخر block في آخر رسالة كل turn)، و **4 breakpoints** (tools، و instructions، و RAG docs، و conversation). وفي كل مثال بيقولك الـ `usage` المتوقع في أول request والـ requests اللي بعده. **استخدم الأوصاف دي كـ expected values في تجاربك.**

### FAQ (أهم نقط)
- breakpoint واحد في آخر المحتوى الثابت **كفاية** في أغلب الحالات.
- **مفيش طريقة تمسح الـ cache بإيدك.** بيخلص لوحده.
- الـ cache keys = **cryptographic hash** للـ prompt، و**مش بتتشارك بين organizations**.
- مع **Batches**: الـ hits "best-effort" لأن الـ requests بتتعالج بأي ترتيب، والـ 1h cache بيساعد.
- ⏳ لو شفت `client.beta.prompt_caching...` في كود قديم: ده قديم، دلوقتي `client.messages.create(...)` عادي.

### Data retention
**ZDR eligible.** Anthropic مش بتخزّن نص الـ prompts. الـ KV cache والـ hashes **في الـ memory بس** طول الـ TTL، وبعدين بتتمسح.

---

# الجزء التاني: Token counting

## 13. ⭐ Token counting (إجابة السؤال التاني اللي اتأجل)
> 📍 `04-anthropic-token-counting.pdf` ص 1، وآخر ~10 صفحات (من *Supported models* لآخر الملف)

### الـ endpoint
**الفكرة:** `POST /v1/messages/count_tokens` بياخد **نفس شكل** request الـ messages (system، و tools، و صور، و PDFs)، ويرجّع `{"input_tokens": N}`. في Python:
```python
client.messages.count_tokens(model="...", system="...", messages=[...])
```
**ليه؟** تدير الـ rate limits والتكلفة **قبل** ما تبعت، وتختار موديل (routing)، وتظبط الـ prompt على طول معيّن.

**مثال من الـ docs:** system "You are a scientist" + "Hello, Claude" = **14 token**. وtool واحد بس + سؤال = **403 token** (تعريفات الـ tools بتاكل كتير، الـ "Hidden Token Overhead" من Step 03). وصورة + سؤال = **1,028**.

**حدود:** مش بيدعم server tools (web search وغيره)، ولا صور/PDFs بـ `url` أو `file` (ابعتهم base64).

**ملاحظات مهمة:**
- **الرقم تقدير.** ممكن يختلف شوية عن الـ request الحقيقي.
- ممكن يحتوي tokens Anthropic بتضيفها لتحسينات، و**مش بتتحاسب عليها**.
- **مش بيستخدم الـ caching** (حتى لو بعتّ `cache_control`).

### ⭐ الـ tokenizer الجديد
> 📍 sections *Supported models* و *Token counts on Claude Fable and Claude Mythos models*

**الفكرة:** **Claude Opus 4.7 والأحدث** (ومنهم Fable 5.x و Mythos 5.x) بيستخدموا **tokenizer أحدث**: نفس النص بيطلّع **حوالي 30% tokens أكتر** من الموديلات الأقدم (والنسبة بتختلف حسب المحتوى). والنصيحة: **اعد العدّ على الموديل اللي هتستخدمه**، ومتعيدش استخدام أرقام موديل قديم. **والفاتورة بتتحسب بأرقام الـ tokenizer ده.**

### 🎯 الإجابة الأمينة للسؤال التاني
السؤال كان: "الفرق الحقيقي بين tokenizer الـ Qwen و Claude".
- الـ docs بتدّيك مقارنة **بين tokenizers Claude نفسهم** (الجديد ≈ +30% عن القديم)، **مش** مقارنة مع Qwen. ولا مصدر من مصادرنا فيه رقم لـ Qwen مقابل Claude.
- يعني الجملة اللي في Step 03 ("Claude الجديد ~30% أكتر") كانت عن **Claude الجديد مقابل Claude القديم**، مش مقابل Qwen. **الفرق مع Qwen مجهول لحد ما تقيسه.**
- **إزاي تقيسه؟** الـ `count_tokens` endpoint **ببلاش** (بس عليه rate limit: 5,000 RPM في الـ Start tier)، وبيعدّ بـ **tokenizer الموديل اللي تبعته**. فتعدّ الـ 15 إيصال بـ Haiku 5.5 وبـ Opus 5.5، وتقارنهم بـ `prompt_eval_count` من Ollama. **بس محتاج API key** (ببلاش، بس لازم حساب).
- و **Ollama compatibility مش بيدعم `count_tokens`** (الشرح 05)، فمفيش طريقة local.
- ده **Bonus B1** في التاسكات (لما يبقى عندك key).

### Pricing and rate limits
**الفكرة:** الـ token counting **ببلاش**، بس ليه **rate limit منفصل** (requests per minute): 5,000 (Start)، و 10,000 (Build)، و 20,000 (Scale). ومنفصل تماماً عن limits الـ messages.

**FAQ:** "Does token counting use prompt caching?" لأ.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **Cache Breakpoint (`cache_control`)**، و **Automatic مقابل Explicit Caching**، و **Cache TTL (5m / 1h)**، و **Cache Write مقابل Cache Read**، و **Minimum Cacheable Length**، و **Lookback Window**، و **Cache Invalidation Hierarchy**، و **Usage Breakdown (input مقابل cache tokens)**، و **Cache Pre-warming**، و **Token Counting Endpoint**، و **Tokenizer Change (+30%)**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. حطيت cache_control على الـ system prompt بتاع الإيصالات (172 token) وبعتّ 100 request على Haiku 5.5. ليه الفاتورة ماقلّتش خالص؟</summary>

لأن الحد الأدنى للـ caching على Haiku 5.5 = 512 token، والـ prompt أقصر. الـ prompts الأقصر من الحد بتتعالج من غير caching **ومن غير error**. تعرف من الـ `usage`: `cache_creation_input_tokens = 0` و `cache_read_input_tokens = 0`. الحل لو عايز caching: تطوّل الجزء الثابت لأكتر من 512 (مثلاً few-shot examples)، وده كمان ممكن يحسّن الدقة.
</details>

<details><summary>2. الـ usage رجع input_tokens: 50، و cache_read_input_tokens: 100000. قد إيه الـ input الكلي؟ وليه ده مهم وإنت بتكتب cost.py؟</summary>

الإجمالي = 100,000 + 0 + 50 = **100,050**. في Anthropic الـ `input_tokens` هو الجزء بعد آخر breakpoint بس، والـ 3 أرقام منفصلين. ده مهم لأن `cost.py` الحالي بيفترض إن الـ cached جزء من الـ input (زي OpenAI)، فلو دخّلت الأرقام دي زي ما هي، هيرمي `ValueError` (cached > input) أو يحسب غلط. لازم الـ cost function تعرف شكل الـ usage بتاع كل provider، وتحسب الـ writes بـ 1.25x.
</details>

<details><summary>3. عندك system ثابت كبير، وبعده block فيه التاريخ والساعة، وبعده سؤال اليوزر. حطيت automatic caching. هيشتغل؟</summary>

لأ. الـ automatic بيحط الـ breakpoint على آخر block (السؤال)، والـ hash بتاعه بيتغيّر كل request (والـ timestamp كمان). والـ lookback بيدوّر على entries اتكتبت قبل كده، ومحدش كتب entry عند آخر الـ system. فكل request = write (1.25x) ومفيش read. الحل: explicit `cache_control` على آخر block في الـ system، وانقل الـ timestamp **بعد** الـ breakpoint (أو شيله لو مش محتاجه).
</details>

<details><summary>4. الـ caching ممكن يخليك تدفع أكتر من غيره؟</summary>

أيوه. الـ cache write (5 دقايق) = 1.25x سعر الـ input. لو الـ prefix مااتقراش تاني خلال الـ TTL (requests متباعدة أكتر من 5 دقايق، أو prompt بيتغيّر قبل الـ breakpoint)، كل request بيدفع write من غير ما يستفيد بـ read. الـ caching بيكسب بس لما نفس الـ prefix يتقرا كذا مرة خلال الـ TTL. ولو الـ requests كل 10–50 دقيقة، فكّر في الـ 1h TTL (2x write) أو مفيش caching خالص.
</details>

<details><summary>5. بعتّ 10 requests متوازية بنفس الـ system الطويل (فوق الحد) في نفس اللحظة. ليه الـ cache_read في كلهم صفر تقريباً؟</summary>

لأن الـ cache entry بتبقى متاحة بعد ما **أول رد يبدأ**. الـ 10 بدأوا مع بعض، فكلهم مالقوش entry، وكلهم عملوا write. الحل حسب الـ docs: ابعت request واحد الأول واستنى الرد يبدأ (أو pre-warm بـ `max_tokens: 0`)، وبعدين ابعت الباقي متوازي. ده هيفرق وإنت بتكتب الـ async في Task 7.
</details>

<details><summary>6. في Ollama الرد اتغيّر لما الـ prompt اتعمله cache. هل نفس الكلام ممكن يحصل في Claude؟</summary>

حسب الـ docs لأ: "Prompt caching has no effect on output token generation"، الرد هو نفس اللي كان هيطلع من غير caching. ده بيوضّح إن "prompt caching" اسم لحاجات مختلفة حسب الـ provider: Ollama (llama.cpp) بيعيد استخدام الـ KV cache بطريقة ممكن تأثر على الحسابات العددية، و Anthropic بتضمن نفس النتيجة. ومتعممش سلوك provider على التاني من غير ما تتأكد.
</details>

<details><summary>7. عايز تعرف الإيصال الواحد هياخد كام token على Claude قبل ما تدفع حاجة. تعمل إيه؟ وينفع على Ollama؟</summary>

`client.messages.count_tokens(model=..., system=..., messages=[...])`. ببلاش (بـ rate limit منفصل)، وبيعدّ بـ tokenizer الموديل اللي تبعته، فاعدّ على الموديل اللي هتستخدمه فعلاً (الجديد ≈ +30% عن القديم). بس محتاج API key. وعلى Ollama الـ endpoint ده مش مدعوم في الـ Anthropic compatibility، والبديل هناك `prompt_eval_count` من `/api/chat` (بعد ما تبعت فعلاً، وبـ tokenizer الموديل الـ local، مش بتاع Claude).
</details>

<details><summary>8. إمتى تستخدم الـ 1h cache بدل الـ 5m؟</summary>

لما نفس الـ prefix بيتستخدم كل أكتر من 5 دقايق بس أقل من ساعة (يوزر في chat بيرد ببطء، أو agent جانبي بياخد وقت طويل، أو batch بياخد بين 5 دقايق وساعة). لو بتستخدمه أكتر من كل 5 دقايق، الـ 5m كفاية لأنه بيتجدد ببلاش مع كل read. والـ 1h write = 2x الـ input، فلازم يتقرا كفاية عشان يستاهل. وكمان الـ cache reads مش بتتحسب في الـ ITPM rate limit، فالـ 1h بيساعد في الـ throughput.
</details>

<details><summary>9. Step 03 قال إن "Claude الجديد بيطلّع ~30% tokens أكتر". أكتر من مين؟</summary>

أكتر من **موديلات Claude الأقدم** (قبل Opus 4.7)، مش من Qwen. الـ docs بتقارن tokenizers Claude ببعض بس. الفرق بين Qwen و Claude مجهول، ولازم يتقاس بـ `count_tokens` على نفس النصوص. ولحد ما تقيس، أي تقدير لتكلفة Claude بأرقام Qwen فيه هامش خطأ مش معروف.
</details>
