# شرح: Anthropic docs — Messages API، و Streaming، و Structured outputs

> **المصدر:** [Claude Platform Docs](https://platform.claude.com/docs/) — 3 صفحات، النسخة اللي اتحفظت يوم **2026-11-28**
> **الملفات:**
> - `resources/articles/04-anthropic-messages-api.pdf` ← *Using the Messages API* (10 صفحات)
> - `resources/articles/04-anthropic-streaming.pdf` ← *Streaming messages* (17 صفحة)
> - `resources/articles/04-anthropic-structured-outputs.pdf` ← *Structured outputs* (19 صفحة)
>
> **إزاي تقرا:** افتح كل PDF جنب الجزء بتاعه. الـ 📍 بيقولك اسم الملف ورقم الصفحة.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

الكورس (الشرح [01](01-anthropic-course-api-fundamentals.md)) علّمك **شكل** الـ API بأمثلة قديمة. الـ docs دي هي **الحقيقة الحالية** لنفس المواضيع: إزاي تبعت request، وإزاي تعمل stream، وإزاي تاخد **JSON مضمون الشكل**. وهي اللي هترجعلها وإنت بتكتب `AnthropicProvider` (Task 2) والـ streaming (Task 3) واستخراج الإيصالات (Task 5).

| # | الصفحة | أهميتها ليك |
|:---:|---|:---:|
| 1 | Using the Messages API | ⭐⭐⭐⭐ (فيها أهم تغييرين عن الكورس) |
| 2 | Streaming messages | ⭐⭐⭐⭐ |
| 3 | Structured outputs | ⭐⭐⭐⭐⭐ (ده اللي بيعمله `format` في Ollama، بس في Claude) |

> ⏳ **عمر المصدر:** الصفحات دي بتتغيّر كتير (فيها features بـ "beta header" بتواريخ 2026). اللي هنا صح يوم 2026-11-28. **أسماء الموديلات** في الأمثلة (`claude-opus-5-5`، و `claude-sonnet-5`) أمثلة، والاختيار الحقيقي اتشرح في Step 03.

**ملحوظة على الأمثلة:** الـ PDFs محفوظة على tab **Python**، فكل الأمثلة بالـ SDK (`anthropic.Anthropic()`). وفي أمثلة الصور هتلاقي `import httpx2`، ودي اسم الـ HTTP library اللي الـ SDK الحالي بيستخدمها جواه (صفحة Errors بتقول كده). إنت هتفضل على `httpx` في كودك، والفرق مش هيأثر عليك.

---

# الجزء الأول: Using the Messages API

## 1.0 المقدمة: طريقتين تبني بيهم على Claude
> 📍 `04-anthropic-messages-api.pdf` ص 1

**الفكرة:** Anthropic بتقدّم طريقتين:
- **Messages API:** إنت بتكلّم الموديل مباشرة. مناسب لـ **agent loop بتاعك** وتحكم كامل. ده موضوع الخطوة دي.
- **Claude Managed Agents:** "harness" جاهز للـ agents بيشتغل على سيرفرات Anthropic، للمهام الطويلة والـ async. (هنرجعله في Step 11.)

**تشبيه من Laravel:** الأولى زي إنك تكتب الـ queue worker بتاعك بنفسك فوق Redis، والتانية زي **Laravel Vapor/Forge**: حد تاني مدير البنية وإنت بتديله الشغل.

## 1.1 Basic request and response
> 📍 ص 2

**الفكرة:** نفس اللي في الكورس: `messages.create(model=..., max_tokens=1024, messages=[...])`، والرد JSON فيه `id`، و `type: "message"`، و `role: "assistant"`، و `content` (list فيها `{"type": "text", "text": "Hello!"}`)، و `model`، و `stop_reason: "end_turn"`، و `stop_sequence: null`، و `usage` (`input_tokens: 12`، و `output_tokens: 6`).

**⚠️ أهم تنبيه في الصفحة (ص 2):** الـ **`temperature` و `top_p` و `top_k` مش مدعومين**:
- على **Claude 4.7 وأحدث** (و Claude Mythos Preview): أي قيمة **غير الـ default** ← **400 error**.
- على **أي موديل** لو بتستخدم **API version `2026-10-21`**: **أي قيمة** خالص ← 400.
- المطلوب: **شيلهم من الـ request**، ووجّه الموديل بالـ **prompt**.

**يعني إيه "API version"؟** كل request لـ Anthropic فيه header اسمه `anthropic-version` (الـ SDK بيبعته لوحده). ده زي **API versioning** في أي API محترم (`/v1/` أو header): Anthropic بتغيّر سلوك الـ API في version جديد، والكود القديم بيفضل شغّال على الـ version القديم. والـ docs بتقول إن من الـ version `2026-10-21` الـ sampling parameters اتشالوا خالص.

**ليه ده مهم لك تحديداً؟**
- في Step 02 و 03 كنت بتعتمد على `temperature=0` عشان التجارب تبقى قابلة للتكرار. على Claude الجديد **مفيش الخيار ده**. فالـ consistency هتيجي من: **prompt واضح**، و **structured outputs**، و **eval بتكرار** (زي ما عملت).
- الـ `LLMProvider.chat()` بتاعك فيه `temperature` و `seed`. الـ `AnthropicProvider` لازم يقرر يعمل إيه فيهم (Task 2). و `seed` أصلاً **مش موجود** في Anthropic API.

**Refusals (ص 2):** لو الموديل رفض الطلب، `stop_reason` بيبقى **`"refusal"`**، والرد فيه `stop_details` بيحدد نوع الـ policy. يعني `stop_reason` بقى فيه قيم أكتر من اللي في الكورس: `end_turn`، و `max_tokens`، و `stop_sequence`، و `tool_use` (Step 10)، و `refusal`. كودك لازم **مايفترضش** إن الرد نص كامل لمجرد إنه 200 OK.

## 1.2 Multiple conversational turns
> 📍 ص 3

**الفكرة:** الـ Messages API **stateless**: بتبعت **التاريخ كله** كل مرة. وحاجة مهمة: الـ turns القديمة **مش لازم تكون جاية من Claude فعلاً**. تقدر تكتب assistant messages بنفسك (**synthetic**)، وده اللي بيخلّي few-shot شغّال (الشرح 01، جزء 2.4).

**جديد (beta):** **message threads**، الـ API يقدر **يحفظ المحادثة** عنده، وكل request بعد كده تبعت فيه الرسايل الجديدة بس. الـ thread بيخلص بعد **5 دقايق** من آخر request، وبيتمسح خلال ساعة على الأكتر.

**تشبيه من Laravel:** الطريقة العادية زي API stateless بـ JWT: كل request فيه كل حاجة. والـ threads زي **session** على السيرفر بـ expiry قصير. ⚠️ والتشبيه مضلل في نقطة: الـ session في Laravel بتعيش ساعات، هنا 5 دقايق.

**للتاسكات:** هنفضل على الطريقة العادية (إنت شايل التاريخ)، لأنها شغّالة مع كل الـ providers (و Ollama compatibility مش بيدعم الـ threads).

## 1.3 System role in messages، و Prefilling
> 📍 ص 4–6

### System message في نص المحادثة
**الفكرة:** على الموديلات الجديدة (Fable، و Mythos، و Opus 5.5 و 5 و 4.8، و Sonnet 5.5، و Haiku 5.5)، تقدر تحط رسالة `{"role": "system", ...}` **بعد user turn** (مش أول رسالة). ليها نفس سلطة الـ `system` field، والميزة إنها **في آخر التاريخ**، فـ **مابتبوظش الـ cache** للي قبلها (الشرح 03).

**النصيحة:** الـ `system` field للتعليمات اللي من أول المحادثة، والـ system message في النص للتعليمات اللي بتظهر بعدين.

⚠️ **ده عكس الكورس** اللي قال إن الـ role يا user يا assistant بس. وده **مش** نفس `{"role": "system"}` بتاع Ollama/OpenAI اللي بيبقى **أول** رسالة. في Anthropic أول رسالة system ← مرفوضة.

### Prefilling Claude's response
**الفكرة:** الـ prefill = assistant message **في آخر** الـ `messages`، وClaude بيكمّل منها، والرد فيه **التكملة بس**.

**هل الـ API بيقبله؟** ده بيعتمد على **الموديل** مش على الـ API version:
- **Claude 4.5 وأقدم:** مقبول (طالما الموديل مش retired).
- **كل الموديلات التانية:** **400 error**.

ومثال الـ docs (على Opus 4.5): سؤال اختيار من متعدد، والـ prefill `"The answer is ("`، و `max_tokens=1`، فالرد `"C"` بس و `stop_reason: "max_tokens"`. وحتى على 4.5 فيه قيود: الـ prefill **مايخلصش بمسافة**، و**مش مع structured outputs**.

**البدائل (ص 6):** خلّي آخر رسالة **user**، وبعدين:
- **JSON بـ schema** ← structured outputs (الجزء التالت هنا).
- **شكل تاني** ← اوصفه في الـ **system prompt**.
- **من غير مقدمة** ← اطلب في الـ system prompt رد مباشر.

وتنبيه مهم: تعليمات الـ system prompt **مش بتضمن** بداية الرد زي الـ prefill، فـ **اتأكد من النص في الكود**.

**خطوات نقل مثال الاختيار من متعدد لموديل جديد:**
1. غيّر الموديل وشيل الـ assistant message.
2. اطلب في الـ system prompt الحرف بس.
3. كبّر `max_tokens` كفاية للرد كله. **وعلى الموديلات اللي الـ thinking فيها شغّال by default، الـ thinking tokens بتتحسب من `max_tokens` كمان.**
4. اقرا الحرف من الـ **text block**، و**الـ block ده ممكن ييجي بعد thinking block**.

ودي الجملة اللي بتقول ليه `content[0].text` مبقاش آمن.

## 1.4 Vision
> 📍 ص 7–8

**الفكرة:** 3 أنواع `source` للصورة: **`base64`** (زي الكورس)، و **`url`** (لينك مباشر)، و **`file`** (صورة اترفعت بالـ Files API). والأنواع: jpeg و png و gif و webp. ومثال الـ docs: صورة واحدة = **1,030 input token**.

(التفاصيل في Step 13. و Ollama compatibility بيدعم base64 بس.)

## 1.5 Next steps و Availability
> 📍 ص 9–10

**الفكرة:** لينكات لمواضيع جاية (stop reasons، و tool use، و structured outputs، و computer use)، وجدول بيوضّح إن الـ Messages API متاح على Claude API، و Amazon Bedrock، و Google Cloud، و Microsoft Foundry، و Claude Platform on AWS.

**وبعدين "Data handling":** الـ `/v1/messages` **eligible لـ Zero Data Retention (ZDR)** و **HIPAA**. ده مهم لموضوع الداتا الحساسة اللي بيهمك: فيه اتفاقيات تخلّي Anthropic ماتخزّنش الـ prompts. بس **ZDR اتفاق** مش حاجة بتتفعّل لوحدها، والداتا لسه **بتخرج** من جهازك (نفس نقاش Step 03 عن قانون 151).

---

# الجزء التاني: Streaming messages

## 2.1 Streaming with SDKs
> 📍 `04-anthropic-streaming.pdf` ص 1–2

**الفكرة:** `"stream": true` ← الرد بيجي **server-sent events (SSE)**. والـ Python SDK فيه sync و async streams. المثال الأساسي:

```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

**Get the final message without handling events (ص 2):** لو مش محتاج تعرض النص وهو بيتكتب، تقدر تستخدم streaming **جوه** وتاخد `Message` كامل في الآخر بـ `stream.get_final_message()`. **ليه تعمل كده؟** عشان الـ requests اللي `max_tokens` بتاعها كبير (المثال `max_tokens=128000`): الـ **SDK بيطلب streaming** عشان مايحصلش **HTTP timeout** (الـ connection تفضل ساكتة دقايق وحد في النص يقفلها). الـ SSE بيخلّي الـ connection "عايشة".

**تشبيه من Laravel:** زي job طويل بيبعت **heartbeat** كل شوية عشان الـ supervisor مايقتلوش.

## 2.2 Event types
> 📍 ص 2–3

**الفكرة:** كل event ليه **اسم** (`event: message_stop`) و JSON `data` فيه نفس النوع. والترتيب:
1. `message_start`: `Message` بـ `content` فاضي.
2. لكل content block: `content_block_start` ← `content_block_delta` (أي عدد) ← `content_block_stop`. وكل block ليه **`index`** هو مكانه في الـ `content` النهائي. **وفيه blocks بتيجي كاملة من غير deltas** (زي نتايج server tools).
3. `message_delta` (واحد أو أكتر): تغييرات على الرسالة كلها.
4. `message_stop`.

**⚠️ "The token counts shown in the usage field of the `message_delta` event are cumulative":** الأرقام في `message_delta` **تراكمية**. آخر واحد = الإجمالي.

**Ping events:** ممكن ييجي أي عدد منهم. **Error events:** زي `overloaded_error` (المقابل لـ HTTP 529). **ولو بتستخدم الـ SDK، الـ event ده مش بيوصلك**: الـ SDK بيقفل الـ stream ويرمي error.

**Other events:** حسب الـ versioning policy، **ممكن تتضاف أنواع events جديدة**، و "your code should handle unknown event types gracefully". يعني الـ parser بتاعك (Task 3) لازم **يتجاهل** أي نوع مايعرفهوش، **مايقعش**.

**تشبيه من Laravel:** زي webhook handler من Stripe: بتعمل `match ($event->type)` على الأنواع اللي تهمك، و `default => null`، عشان لما Stripe تضيف نوع جديد ماتطلعش 500.

## 2.3 Content block delta types
> 📍 ص 3–5

**الفكرة:** كل `content_block_delta` فيه `delta` ليه `type`:
- **`text_delta`**: حتة نص: `{"type": "text_delta", "text": "ello frien"}`.
- **`input_json_delta`**: لـ **tool_use** blocks (Step 10). الـ input بيجي **JSON ناقص** (`partial_json`)، بتجمعه كـ string وتعمله parse لما ييجي `content_block_stop`. والـ API by default بيستنى كل key و value يكملوا قبل ما يبعتهم.
- **`thinking_delta`**: حتة من الـ thinking. وقبل `content_block_stop` بتاع الـ thinking بيجي **`signature_delta`** (توقيع بيتأكد إن الـ thinking ماتلعبش فيه). ولو `display: "omitted"` مفيش نص thinking بيتبعت.

**للتاسكات:** هتتعامل مع `text_delta` بس، وتتجاهل الباقي (بأمان).

## 2.4 Full HTTP stream response
> 📍 ص 5–14

**الفكرة:** "Use the client SDKs when using streaming mode" (استخدم الـ SDK). بس لو بتبني **direct API integration**، لازم تتعامل مع الـ events بنفسك. والصفحة بتوري 4 أمثلة لـ HTTP stream حقيقي:

**1) Basic streaming request (ص 6–7):** شكل الـ SSE الخام:
```
event: message_start
data: {"type": "message_start", "message": {..., "usage": {"input_tokens": 25, "output_tokens": 1}}}

event: content_block_start
data: {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}

event: ping
data: {"type": "ping"}

event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Hello"}}
...
event: message_delta
data: {"type": "message_delta", "delta": {"stop_reason": "end_turn", ...}, "usage": {"output_tokens": 15}}

event: message_stop
data: {"type": "message_stop"}
```

**شكل الـ SSE:** نص عادي، كل event عبارة عن سطر `event: <النوع>` وسطر `data: <JSON>`، وبين كل event والتاني **سطر فاضي**. ده اللي هتعمله parse بإيدك في Task 3 بـ `httpx` (`iter_lines()`).

**2) Streaming with tool use (ص 7–10):** text block الأول ("Okay, let's check the weather...")، وبعده `tool_use` block في `index: 1` والـ input بيجي `input_json_delta`، و `stop_reason: "tool_use"`. (Step 10.)

**3) Streaming with thinking (ص 10–12):** `thinking: {"type": "adaptive", "display": "summarized"}`، و thinking block في `index: 0` (بـ `thinking_delta` و `signature_delta`)، وبعده text block في `index: 1`. **شوف بعينك:** النص الحقيقي في `index: 1` مش 0.

**4) Web search tool (ص 12–14):** `server_tool_use` و `web_search_tool_result` (block بييجي كامل)، وفي الآخر `usage` فيه `cache_creation_input_tokens` و `cache_read_input_tokens` و `server_tool_use`. (Step 10.)

## 2.5 Error recovery
> 📍 ص 15–16

**الفكرة:** لو الـ stream وقع في النص (شبكة، timeout)، **متبدأش من الأول**. الطريقة:
1. **احفظ** الجزء اللي وصلك.
2. اعمل **request جديد يكمّل**:
   - **Claude 4.5 وأقدم:** تحط الجزء ده كـ **assistant message** (prefill) وهو يكمّل.
   - **Claude 4.6 وأحدث:** (عشان الـ prefill مبقاش مسموح) تحط **user message** فيها الجزء اللي وصلك وتعليمات زي: "ردك اتقطع وخلص بـ [...]. كمّل من مكان ما وقفت".
3. **كمّل الـ streaming.**

**Best practices:** اعتمد على الـ SDK في الـ accumulation والـ errors. والـ tool_use والـ thinking blocks **مايتكمّلوش جزئياً**، تقدر تكمّل من آخر **text** block بس.

**ربط بـ Task 4:** الـ streaming chat CLI لما الـ stream يقع (أو تدوس Ctrl+C)، لازم تقرر: تحفظ الجزء في التاريخ؟ تعيد؟ تكمّل؟

## 2.6 Next steps و Availability
> 📍 ص 16–17

متاح على كل الـ platforms. وملحوظة: **Amazon Bedrock (`bedrock-runtime`) مش بيبعت SSE عادي**. يعني الـ parser اليدوي بتاعك **مش portable** لكل مكان، وده سبب كمان تفضّل الـ SDK.

---

# الجزء التالت: Structured outputs

## 3.0 المقدمة: ليه structured outputs؟
> 📍 `04-anthropic-structured-outputs.pdf` ص 1–2

**الفكرة:** structured outputs بيجبر رد Claude **يمشي على schema**. وفيه feature اتنين:
- **JSON outputs (`output_config.format`):** **الرد نفسه** JSON بشكل معيّن. ده موضوع الصفحة.
- **Strict tool use (`strict: true`):** ضمان إن **أسماء الـ tools وقيم الـ inputs** صح (Step 10).

**من غيره** ممكن يحصل: JSON بايظ (parsing errors)، أو field ناقص، أو نوع غلط (`"total": "215"` بدل `215`)، فتحتاج retries.
**بيه** (عن طريق **constrained decoding**): **Always valid**، و **Type safe**، و **Reliable** (مفيش retries عشان الـ schema).

**ده نفس اللي إنت عملته:** في Step 02 Task 5 قارنت 3 طرق للـ JSON، والطريقة التالتة (`format` بـ JSON schema في Ollama) هي **constrained sampling** (concept موجود). وفي Step 03 Task 6 استخدمتها على 15 إيصال. structured outputs في Claude **نفس الفكرة بالظبط**، بس على الـ API.

## 3.1 How it works
> 📍 ص 2

**3 خطوات:**
1. **عرّف الـ schema:** JSON Schema، أو **type في لغتك** (Pydantic في Python).
2. **ابعته في `output_config.format`** بـ `type: "json_schema"`. (الـ SDK helpers بيعملوا ده لوحدهم.)
3. **اقرا الرد:** JSON صحيح في **text block**. والـ SDK helpers بيعملوله parse لـ type بتاعك.

## 3.2 Usage: `client.messages.parse()` (الطريقة الموصى بيها)
> 📍 ص 2–3

**الفكرة:**
```python
class ContactInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool

response = client.messages.parse(model=..., max_tokens=1024, messages=[...], output_format=ContactInfo)
print(response.parsed_output)   # ContactInfo(name='John Smith', ...)
```
بتدّي **Pydantic model** لـ `messages.parse()` كـ `output_format`. والـ SDK: بيحوّل الـ schema، ويبعته كـ `output_config.format`، و**يعمل validate** للرد، ويرجّعلك الـ model في **`parsed_output`**.

**المقارنة بكودك في Step 03:** إنت عملت كل ده بإيدك: `Receipt.model_json_schema()` ← `format` في Ollama ← `Receipt.model_validate_json(result.text)` ← `except ValidationError`. الـ SDK بيعمل الـ 3 خطوات دول في سطر.

**⚠️ تحذير مهم (ص 3):** لو عندك field نوعه **`dict`** (من غير keys معروفة)، الـ SDK بيبعته object من غير properties، فـ **Claude يقدر يرجّع `{}` بس**. لو الـ keys معروفة، اعمل **nested Pydantic model**.

## 3.3 How SDK transformation works
> 📍 ص 3–4

**الفكرة:** الـ API **مش بيدعم** كل حاجات الـ JSON Schema (جزء 3.7). فالـ SDK بيعمل **transformation**:
1. **يشيل الـ constraints اللي مش مدعومة** (`minimum`، و `maximum`، و `minLength`، و `maxLength`).
2. **يكتبها في الـ description** بتاع الـ field (مثلاً `{minimum: 100}`)، فالموديل "يقراها" كتعليمات.
3. **يضيف `additionalProperties: false`** لكل object.
4. **يفلتر الـ string formats** للي مدعوم بس.
5. **يعمل validate للرد** على الـ schema **الأصلي** بكل الـ constraints.

**يعني:** Claude بياخد schema مبسّط، بس الـ SDK لسه بيتأكد من كل حاجة **في كودك**. مثال: field بـ `minimum: 100` بيتبعت integer عادي + `{minimum: 100}` في الـ description، والـ SDK بيرفض الرد لو الرقم أقل من 100.

**💡 ليه ده مهم لك:** لو ضفت لـ `Receipt` حاجة زي `total: float = Field(ge=0)`، الـ **grammar** مش هيمنع رقم سالب، بس الـ **validation** في Python هيمسكه. ده نفس الفرق اللي اتعلمته في Step 03: الـ schema بيضمن **الشكل**، مش إن القيم **صح**.

## 3.4 Using a raw JSON schema
> 📍 ص 4–5

**الفكرة:** لو الـ schema جاي من ملف أو OpenAPI spec أو بيتبني runtime، ابعته بنفسك في `output_config` بـ `messages.create()`:
```python
output_config={"format": {"type": "json_schema", "schema": {..., "additionalProperties": False}}}
```
وتقرا: `text = next(block.text for block in response.content if block.type == "text")` وبعدين `json.loads(text)`.

**شوف السطر ده كويس:** `next(... if block.type == "text")` = "أول block نوعه text". **ده الـ pattern الصح** بدل `content[0].text` (الشرح 01).

وفيه `transform_schema()` من الـ package: بتعمل نفس الـ transformation وترجّعلك الـ schema من غير ما تبعته، عشان تشوفه أو تعدّله.

## 3.5 Common use cases
> 📍 ص 5–8

**الفكرة:** 3 أمثلة:
- **Data extraction:** `Invoice` فيه `invoice_number`، و `date`، و `total_amount`، و `line_items: list[LineItem]`، و `customer_name`. **ده أقرب مثال لمشروعك** (الإيصالات)، وفيه **nested model** في list (لو حبيت تستخرج البنود).
- **Classification:** `category`، و `confidence`، و `tags`، و `sentiment`.
- **API response formatting:** model فيه nested models و `list[APIError] | None = None`.

## 3.6 Strict tool use، و Using both together
> 📍 ص 8–9

**الفكرة:** الـ JSON outputs بيتحكم في **اللي Claude بيقوله**، والـ strict tool use بيتحكم في **إزاي بينادي الـ functions**. والاتنين ينفعوا مع بعض (agent بيستخدم tools بـ inputs مضمونة وبيرجّع رد نهائي JSON). (Step 10.)

## 3.7 Important considerations
> 📍 ص 9–15

### Grammar compilation and caching (ص 9–10)
**الفكرة:** الـ schema بيتحول لـ **grammar** (قواعد بتمنع الموديل يطلّع token يكسر الـ schema).
- **أول request بـ schema جديد أبطأ** (الـ grammar بيتعمله compile).
- الـ grammar بيتعمله **cache لمدة 24 ساعة** من آخر استخدام.
- الـ cache بيتمسح لو **شكل الـ schema** اتغيّر (تغيير `name` أو `description` بس مش بيمسحه).

**ربط بقياساتك:** لو عملت eval على 15 إيصال بـ Claude، أول إيصال هيبقى أبطأ. متحسبوش في المتوسط من غير ما تفهم ده (زي الـ cold start في Ollama).

### Prompt modification and token costs (ص 10)
**الفكرة:** لما تستخدم structured outputs، Claude بياخد **system prompt إضافي** بيشرح الـ format. يعني:
- **input tokens أكتر شوية** (بتدفعهم).
- **تغيير `output_config.format` بيمسح الـ prompt cache** للمحادثة دي (الشرح 03).

### JSON Schema limitations (ص 10–11)
**مدعوم:** كل الأنواع الأساسية، و `enum` و `const`، و `anyOf` و `allOf` (بقيود)، و `$ref` و `$defs`، و `default`، و `required`، و `additionalProperties` (**لازم `false`**)، و string formats (`date-time`، و `date`، و `email`، و `uuid`...)، و `minItems` (0 أو 1 بس).

**مش مدعوم:** recursive schemas، و `oneOf` (استخدم `anyOf`)، و `not`، و **numerical constraints** (`minimum`، و `maximum`، و `multipleOf`)، و **string constraints** (`minLength`، و `maxLength`)، و `additionalProperties` بأي قيمة غير `false`. ولو استخدمت حاجة مش مدعومة ← **400** (لو بتبعت raw schema؛ الـ SDK بيحوّلها زي جزء 3.3).

**Regex (`pattern`):** البسيط شغّال (`^...$`، و `\d`، و `[]`، و `{n,m}` البسيط). مش مدعوم: backreferences، و lookahead/lookbehind، و `\b`.

### Objects with arbitrary keys (ص 11–12)
**الفكرة:** عشان `additionalProperties` لازم `false`، Claude يقدر يرجّع **الـ keys اللي إنت كاتبها بس**. فـ `dict[str, str]` ← `{}`. والحل لو الـ keys مش معروفة: **array** من `{"key": ..., "value": ...}`.

**تشبيه من Laravel:** زي `$fillable` الصارم: أي key مش في القايمة مش هيدخل.

### Property ordering (ص 12–13)
**الفكرة:** الـ properties بتطلع **بترتيب الـ schema**، بس **الـ required الأول وبعدين الـ optional**. لو الترتيب مهم، خلّي كل حاجة required.

**💡 ليه الترتيب ممكن يفرق؟** الموديل بيولّد token ورا token، فاللي بيتكتب الأول بيأثر على اللي بعده. (ده هيرجع في prompt engineering في Step 05.)

### Invalid outputs (ص 13–14)
**الفكرة:** الضمان "في أغلب الحالات"، مش دايماً:
- **Refusal (`stop_reason: "refusal"`):** Claude رفض لأسباب أمان. **الـ status 200**، و**بتدفع الـ tokens**، و**الرد ممكن مايمشيش على الـ schema**. وكمان: لو عملت property بتطلب "التفكير خطوة بخطوة"، ممكن يرفض (`reasoning_extraction`)، اطلب شرح قصير بدل كده.
- **Max tokens (`stop_reason: "max_tokens"`):** الرد اتقطع، فالـ JSON **ناقص**. أعد بـ `max_tokens` أكبر.

**ربط بكودك:** في Step 03 الـ review ضاف `max_tokens=256` لـ `model_eval.py` عشان موديل يعلّق مايفضلش شغّال. ودلوقتي إنت عارف إن لازم **تشيك `stop_reason`** قبل ما تعمل parse، مش تعتمد على الـ `ValidationError` بس.

### Enum value casing (ص 14)
**الفكرة:** structured outputs **مش بيضمن الـ capitalization** بتاع قيم الـ `enum` و `const`. ممكن ترجع `"Conversation Topic 3"` والـ enum فيه `"Conversation topic 3"`، **من غير error**. الحل: **قارن case-insensitive**، ومتعملش enum values بتفرق في الـ case بس.

**💡 ربط مباشر:** لو عملت `currency: Literal["EGP", "USD", "SAR", "AED"]`، Claude ممكن يرجّع `"Egp"`؟ القيم دي كلها capital فالخطر قليل، بس القاعدة: **normalize قبل ما تقارن** (زي `normalize_name()` في `model_eval.py`).

### Schema complexity limits (ص 14–15)
**الفكرة:** حدود صريحة على **كل الـ schemas في الـ request مع بعض**: **20** strict tool، و **24** optional parameter، و **16** parameter بـ union types (`anyOf` أو `["string", "null"]`)، لأنها بتعمل compilation cost أُسّي. ولو عدّيت الحدود الداخلية: 400 "Schema is too complex for compilation"، وفيه timeout للـ compile **180 ثانية**.

**نصايح التبسيط:** خلّي الـ strict للـ tools المهمة بس، و**قلّل الـ optional** (كل optional بيضاعف جزء من الـ grammar)، وفلطّح الـ nested، وقسّم على requests.

**💡 ليه يهمك:** `str | None = None` في Pydantic = optional **و** union في نفس الوقت. `Receipt` بتاعك فيه 4 fields required، فبعيد جداً عن الحدود. بس لو عملت schema لإيصال بـ line items وكل حاجة optional، افتكر الحدود دي.

## 3.8 Migrating from the beta، و Feature compatibility
> 📍 ص 15–16

**الفكرة:** الـ `output_format` (parameter الـ beta القديم) اتنقل لـ **`output_config.format`**. لو بعتّ `output_format={...}` dict في Python SDK v1 ← `TypeError`. بس **Pydantic model** كـ `output_format=Model` في `parse()` لسه شغّال (الـ SDK بيحوّله).

> ⏳ يعني لو لقيت مثال قديم على الإنترنت بـ `output_format` و beta header، ده قديم.

**بيشتغل مع:** **Batch** (خصم 50%)، و **Token counting**، و **Streaming**، و strict tools مع بعض.
**مش بيشتغل مع:** **Citations** (400)، و **Prefill**.
**نطاق الـ grammar:** على **رد Claude المباشر** بس، مش على الـ thinking ولا الـ tool calls. يعني Claude يقدر "يفكّر بحرية" والرد النهائي JSON.

## 3.9 Availability و Data handling
> 📍 ص 16–19

**الفكرة:** متاح على كل الـ platforms، و **ZDR eligible (qualified)**: الـ prompts والردود مش بتتخزن، **بس الـ JSON schema نفسه بيتعمله cache لحد 24 ساعة**. ولـ **HIPAA**: **ماتحطش داتا حساسة (PHI) في الـ schema** (أسماء properties، أو قيم enum، أو patterns)، لأن الـ schemas بتتخزن منفصلة ومن غير نفس الحماية.

**💡 ربط بموضوع الداتا الحساسة:** لو عملت `enum` بأسماء موظفين أو عملاء حقيقيين في الـ schema، دي داتا **بتتخزن** حتى مع ZDR. الـ schema لازم يبقى **شكل** بس، والداتا في الـ messages.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **API Versioning (`anthropic-version`)**، و **Sampling Parameters Removal**، و **Stop Reason: refusal**، و **Synthetic Assistant Messages**، و **Mid-conversation System Message**، و **Unknown Event Types (forward compatibility)**، و **Stream Error Recovery**، و **SDK Schema Transformation**، و **Grammar Compilation Cache**، و **Zero Data Retention (ZDR)**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. ليه `temperature=0` مش هيشتغل على Claude الجديد؟ وإزاي تحافظ على consistency في الـ extraction من غيره؟</summary>

الـ docs بتقول إن الـ sampling parameters (`temperature` و `top_p` و `top_k`) مش مدعومين على Claude 4.7+، وأي قيمة غير الـ default بترجع 400، ومن API version `2026-10-21` أي قيمة خالص. الـ consistency بتيجي من: structured outputs (الشكل مضمون)، و prompt واضح بقواعد محددة (زي الـ SYSTEM_PROMPT بتاع الإيصالات)، و few-shot examples، و eval بتكرار يقيس الـ consistency بدل ما تفترضها. وفي الكود: normalize وvalidate للقيم.
</details>

<details><summary>2. الرد رجع 200 OK. ده معناه إن عندك نص كامل تقدر تستخدمه؟</summary>

لأ. لازم تشيك `stop_reason`: `max_tokens` = الرد اتقطع (والـ JSON ناقص)، و `refusal` = Claude رفض (والرد ممكن مايمشيش على الـ schema رغم إنك دفعت الـ tokens)، و `tool_use` = Claude عايز ينادي tool مش بيرد. وكمان في الـ streaming ممكن error ييجي بعد الـ 200. الـ 200 بيقول إن الـ request اتقبل، مش إن الرد صالح لاستخدامك.
</details>

<details><summary>3. في الـ SSE stream، إزاي تفرّق بين event والتاني؟ وتعمل إيه لو جالك نوع event مش عارفه؟</summary>

كل event = سطر `event: <type>` وسطر `data: <json>`، وبين الـ events سطر فاضي. والـ `data` فيه `type` كمان. لو النوع مش معروف: **تجاهله**. الـ docs بتقول صراحة إن أنواع جديدة ممكن تتضاف، والكود لازم يتعامل معاها "gracefully". لو عملت `raise` على أي نوع مش معروف، كودك هيقع أول ما Anthropic تضيف event جديد.
</details>

<details><summary>4. الـ stream وقع بعد 300 token من رد على Opus 5.5. تعمل إيه عشان ماتدفعش الـ 300 تاني؟</summary>

تحفظ النص اللي وصل، وتعمل request جديد بنفس التاريخ + **user message** فيها النص الناقص وتعليمات "ردك اتقطع وخلص بـ [...]، كمّل من مكان ما وقفت". (على Claude 4.5 وأقدم كان ينفع تحطه كـ assistant prefill، بس الموديلات الجديدة بترفض الـ prefill.) وتكمّل من آخر text block بس، لأن الـ thinking والـ tool_use مايتكمّلوش جزئياً. ⚠️ وانتبه: الـ input بتاع الـ request التاني فيه النص القديم، فبتدفعه **input** (أرخص من output بكتير).
</details>

<details><summary>5. إيه الفرق بين `messages.parse(output_format=Receipt)` وإنك تبعت `output_config.format` بنفسك؟</summary>

`parse()` بياخد Pydantic model، ويعمل transformation للـ schema (يشيل الـ constraints اللي مش مدعومة ويكتبها في الـ description، ويضيف `additionalProperties: false`)، ويبعته، ويعمل validate للرد على الـ schema الأصلي بكل الـ constraints، ويرجّع `parsed_output` جاهز. الـ raw `output_config.format` إنت اللي بتكتب الـ schema (لازم يكون مدعوم بالكامل وإلا 400)، وبتقرا الـ text block وتعمل `json.loads` بنفسك، ومفيش validation للـ constraints. الـ raw مناسب لما الـ schema جاي من ملف أو OpenAPI.
</details>

<details><summary>6. ضفت `total: float = Field(ge=0)` لـ Receipt. Claude ممكن يرجّع total سالب؟</summary>

ممكن **يولّده**، لأن `minimum` مش مدعوم في الـ grammar، والـ SDK بيشيله ويكتبه في الـ description (تعليمات، مش قيد). بس `messages.parse()` بيعمل validate على الـ schema الأصلي، فالرد السالب هيترفض في Python (validation error). يعني الـ constraint اتنقل من "مستحيل يحصل" لـ "هيتمسك لو حصل". ده نفس مبدأ Step 03: الـ schema يضمن الشكل، والـ validation في كودك تضمن القواعد.
</details>

<details><summary>7. ليه field نوعه `dict[str, float]` في Pydantic ممكن يرجع دايماً `{}` من Claude؟</summary>

عشان structured outputs بيطلب `additionalProperties: false`، فـ Claude يقدر يرجّع الـ keys المكتوبة في الـ schema بس. والـ `dict` مفيهوش keys، فالـ SDK بيبعته object بـ properties فاضية، فمفيش key مسموح. الحل: nested model لو الـ keys معروفة، أو list من `{key, value}` لو مش معروفة.
</details>

<details><summary>8. شغّال على بيانات طبية بـ HIPAA، وعملت enum في الـ schema بأسماء المرضى عشان الـ extraction يبقى أدق. إيه المشكلة؟</summary>

الـ JSON schemas بتتعملها cache لحد 24 ساعة **منفصلة** عن محتوى الرسايل، ومن غير نفس حماية الـ PHI. الـ docs بتقول صراحة: ماتحطش PHI في أسماء الـ properties أو قيم الـ enum أو الـ const أو الـ patterns. الداتا الحساسة مكانها الـ messages بس. والحل: enum بأكواد أو IDs مش أسماء، أو field string عادي.
</details>

<details><summary>9. أول request بـ structured outputs خد وقت أطول بكتير من الباقي. ده bug؟</summary>

لأ. أول مرة بتستخدم schema معيّن، الـ API بيعمل compile للـ grammar، وده بيزود الـ latency. بعدها الـ grammar بيتعمله cache 24 ساعة من آخر استخدام، والـ requests بتبقى أسرع. ولو غيّرت شكل الـ schema (مش الأسماء والـ descriptions بس)، الـ compile هيحصل تاني. فلو بتقيس latency في eval، افصل أول request أو استبعده (زي الـ cold start في Ollama).
</details>
