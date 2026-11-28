# شرح: Ollama API — Introduction، و Chat، و Streaming، و Structured outputs، و Anthropic compatibility

> **المصدر:** [Ollama docs](https://docs.ollama.com/) — 5 صفحات، النسخة اللي اتحفظت يوم **2026-11-28**
> **الملفات:**
> - `resources/articles/04-ollama-api-introduction.pdf` ← *API Reference: Introduction*
> - `resources/articles/04-ollama-api-chat.pdf` ← *Generate a chat message* (`POST /api/chat`)
> - `resources/articles/04-ollama-api-streaming.pdf` ← *API Reference: Streaming*
> - `resources/articles/04-ollama-structured-outputs.pdf` ← *Capabilities: Structured Outputs*
> - `resources/articles/04-ollama-anthropic-compatibility.pdf` ← *Anthropic compatibility* ⭐
>
> **إزاي تقرا:** بالترتيب ده. الصفحات قصيرة (2–9 صفحات)، وأهمها الأخيرة.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

الـ ROADMAP بيقول "Ollama API: نفس الأفكار على موديل local". يعني كل حاجة في الشروح 01–04 (messages، و streaming، و structured outputs، و usage) ليها **مقابل في Ollama**. والصفحات دي بتوريك المقابل، والفروق.

**والاكتشاف الأهم في الخطوة:** Ollama عنده endpoint **متوافق مع Anthropic Messages API** (`/v1/messages`). يعني **الـ SDK الرسمي بتاع `anthropic`** يشتغل على `qwen2.5:3b` بتاعك **من غير key ومن غير ما الداتا تخرج من جهازك**. وده اللي خلّى التاسكات الأساسية كلها تتعمل local. (واتأكدت إن الـ endpoint ده شغّال على **Ollama 0.34.4** اللي عندك، بـ request بسيط وبـ streaming.)

> ⏳ **عمر المصدر:** الأمثلة بتستخدم موديلات زي `gemma4` و `gpt-oss` و `qwen3-coder`. **متنزّلش حاجة منهم**، كل التاسكات على `qwen2.5:3b`. والـ docs بتوصف آخر نسخة من Ollama، وإنت على 0.34.4، فلو feature مش شغّالة، دي أول حاجة تشكّ فيها.

---

## 1. API Introduction
> 📍 `04-ollama-api-introduction.pdf` ص 1–3

**الفكرة:** تقدر تبني على Ollama بطريقتين:
- **Cloud:** API key، ومن غير ما تسطّب Ollama.
- **Local:** تسطّب Ollama وتشغّل موديل.

**الـ Base URLs (جدول ص 1):**

| الـ API | Cloud | Local |
|---|---|---|
| Ollama API (native) | `https://ollama.com/api` | `http://localhost:11434/api` |
| OpenAI compatibility | `https://ollama.com/v1` | `http://localhost:11434/v1` |
| **Anthropic client** | `https://ollama.com` | `http://localhost:11434` |

و"The Anthropic client appends `/v1/messages` to its base URL": يعني الـ SDK بتاع Anthropic بيزوّد `/v1/messages` لوحده، فالـ `base_url` يبقى **من غير** `/v1`.

> ⚠️ **افتكر من Step 03:** على Windows عندك، `localhost` كان بيضيّع ~2 ث في كل request (IPv6 الأول)، فالـ default في `llm_client.py` بقى `http://127.0.0.1:11434`. **نفس الكلام هنا**: في الـ SDK استخدم `base_url="http://127.0.0.1:11434"`، مش `localhost` اللي في الـ docs.

**قواعد:** الـ cloud محتاج key، والـ local لأ. ولو عايز cloud models من الـ local server، تعمل sign in (وده اللي حذّرناك منه في Step 03: الداتا بتخرج حتى لو الـ URL `localhost`). وإنشاء أو مسح موديلات محتاج local server.

**مثال الـ cloud (ص 2):** `curl https://ollama.com/api/chat -H "Authorization: Bearer $OLLAMA_API_KEY" ...` وبتقرا من `message.content`. وللـ local: نفس الـ request على `http://localhost:11434/api/chat` من غير الـ header.

**Libraries:** فيه libraries رسمية لـ Python و JavaScript. (إنت مش هتستخدمها، لأنك كاتب client بـ `httpx` من Step 01، وده بيعلّمك أكتر. والـ docs بتستخدمها في الأمثلة: `from ollama import chat`.)

**Versioning:** الـ API **مش متقسّم versions** بشكل صارم، بس "expected to be stable and backwards compatible"، والـ deprecations نادرة وبتتعلن في الـ release notes.

**قارن بـ Anthropic:** Anthropic عندها `anthropic-version` header و versions بتواريخ (`2026-10-21`)، يعني تقدر تختار السلوك. Ollama مفيهوش، فأي تحديث ممكن يغيّر السلوك (زي ما شفت في Step 03: الـ docs قالت default context 2048 والحقيقي 4096).

---

## 2. Generate a chat message (`POST /api/chat`)
> 📍 `04-ollama-api-chat.pdf` ص 1–5

**الفكرة:** ده الـ endpoint اللي `llm_client.py` بيستخدمه من Step 01. الصفحة دي هي الـ **reference الرسمي** ليه.

### Request body (ص 2–3)
| الحقل | معناه | في `llm_client.chat()` |
|---|---|---|
| `model` | **required** | ✅ |
| `messages` | **required**، كل رسالة فيها `role` و `content` | ✅ |
| `tools` | functions الموديل ممكن ينادي عليها (Step 10) | ❌ |
| `format` | `"json"` أو **JSON schema** | ✅ |
| `options` | runtime options (temperature، و num_ctx، و num_predict...) | ✅ |
| `stream` | **default: `true`** ⚠️ | بتبعت `False` |
| `think` | التحكم في الـ thinking output: `true`/`false`/`null` (default الموديل)، أو اسم مستوى بيحدده الموديل. **الأرقام مش مدعومة**. وتعرف القيم المدعومة من `/api/show` | ❌ |
| `keep_alive` | مدة بقاء الموديل في الـ memory (`"5m"`، أو `0` = unload فوراً) | ✅ (Step 03) |
| `logprobs` / `top_logprobs` | الـ log probabilities للـ tokens | ❌ (اتشرحت في Step 02) |

**⚠️ `stream` default `true`:** لو بعتّ request من غير `"stream": false`، Ollama **هيعمل stream**. ده سبب إن `llm_client.py` بيبعت `"stream": False` صريح. (قارن: في Anthropic الـ default non-streaming، ولازم تطلب `stream: true`.)

**`think`:** ده المقابل لـ `thinking` في Anthropic. `qwen2.5:3b` مش thinking model، فمش هيفرق معاك دلوقتي.

### Response (ص 1–2، و 3–5)
مثال الرد (ص 2):
```json
{"model": "gemma4", "created_at": "...",
 "message": {"role": "assistant", "content": "Hello! How can I help you today?"},
 "done": true, "done_reason": "stop",
 "total_duration": 174560334, "load_duration": 101397084,
 "prompt_eval_count": 11, "prompt_eval_duration": 13074791,
 "eval_count": 18, "eval_duration": 52479709}
```

| الحقل | معناه |
|---|---|
| `message` | الرد (role و content) |
| `done` / `done_reason` | خلص؟ وليه؟ (`stop`، و `length`...) |
| `total_duration` | الوقت الكلي **بالـ nanoseconds** |
| `load_duration` | وقت تحميل الموديل (ns) |
| `prompt_eval_count` | عدد tokens الـ prompt |
| **`prompt_eval_cached_count`** | **عدد tokens الـ prompt اللي اتقرت من الـ cache** ⭐ |
| `prompt_eval_duration` | وقت تقييم الـ prompt tokens **اللي مش متعملها cache** (ns) |
| `eval_count` / `eval_duration` | الـ tokens المتولّدة ووقتها (ns) |
| `logprobs` | لو طلبتها |

**⭐ `prompt_eval_cached_count` جديد عليك:** في Step 03 شفت الـ prompt caching في Ollama من **الوقت** بس (الـ prompt eval نزل). دلوقتي فيه **رقم صريح**. واتأكدت إن 0.34.4 بتاعك بيرجّعه في `/api/chat`. و `llm_client.py` **مش بيقراه** لحد دلوقتي (Task 8).

**⚠️ لاحظ الفرق في المعنى:** في Ollama الـ `prompt_eval_count` = **كل** الـ prompt tokens، والـ cached = **جزء منه**. ده **عكس** Anthropic اللي فيها `input_tokens` = الجزء **اللي مش متعمله cache** بس (الشرح 03، جزء 9). نفس الفكرة، **حسابات مختلفة**. وده اللي هتظبطه في `ChatResult` في Task 8.

**مقارنة كاملة بـ Anthropic:**

| | Ollama `/api/chat` | Anthropic `/v1/messages` |
|---|---|---|
| النص | `message.content` (string) | `content` (list of blocks) |
| السبب | `done_reason` (`stop`، `length`) | `stop_reason` (`end_turn`، `max_tokens`...) |
| الـ input | `prompt_eval_count` | `input_tokens` + cache fields |
| الـ output | `eval_count` | `output_tokens` |
| الـ cache | `prompt_eval_cached_count` (جزء من الـ input) | `cache_read_input_tokens` (منفصل) |
| التوقيت | 4 أوقات بالـ ns | مفيش |
| الـ system | `{"role": "system"}` في `messages` | parameter `system` |
| `max_tokens` | `options.num_predict` (اختياري) | `max_tokens` (إجباري) |
| الـ default | streaming | non-streaming |

---

## 3. Streaming
> 📍 `04-ollama-api-streaming.pdf` ص 1–2

**الفكرة:** بعض الـ endpoints بتعمل stream **by default** (زي `/api/generate` و `/api/chat`). والشكل: **newline-delimited JSON (NDJSON)**، content type `application/x-ndjson`. يعني **كل سطر = JSON object كامل**:
```
{"model":"gemma4","created_at":"...","response":"..."}
{"model":"gemma4","created_at":"...","response":"..."}
...
```
(المثال في الصفحة على `/api/generate` اللي بيرجّع `response`. في `/api/chat` كل سطر فيه `message.content` بحتة النص، وآخر سطر فيه `done: true` والأرقام: `eval_count` وغيرها.)

**تقفل الـ streaming:** `{"stream": false}` في الـ body، والرد يبقى JSON واحد (`application/json`).

**إمتى ده وإمتى ده (ص 1–2):**
- **Streaming:** real-time، و perceived latency أقل، و أحسن للردود الطويلة.
- **Non-streaming:** أسهل في المعالجة، و**أحسن للردود القصيرة أو الـ structured outputs**، وأسهل في بعض التطبيقات.

**💡 "Better for ... structured outputs":** منطقي: الـ JSON الناقص مالوش فايدة لحد ما يكمل. فاستخراج الإيصالات = non-streaming، و الـ chat = streaming.

### ⭐ NDJSON (Ollama) مقابل SSE (Anthropic)
ده فرق هتحسّه بإيدك في Task 3:

| | NDJSON (Ollama native) | SSE (Anthropic و Ollama `/v1/messages`) |
|---|---|---|
| الشكل | كل سطر JSON كامل | `event: <type>` + `data: <json>` + سطر فاضي |
| أنواع الـ chunks | نوع واحد (نفس الشكل كل سطر)، وآخر سطر `done: true` | events مختلفة (`message_start`، و `content_block_delta`...) |
| الـ parsing | `json.loads(line)` لكل سطر | تقرا سطر `data:` وتشيل البادئة وبعدين `json.loads`، وتتجاهل الـ events اللي مش محتاجها |
| الـ usage | في آخر سطر | `message_start` + `message_delta` |
| الـ errors في النص | — | event نوعه `error` (و Ollama compat مش بيبعته، جزء 5) |

**تشبيه من Laravel:** الـ NDJSON زي ملف log كل سطر فيه JSON (`Log::channel('json')`)، والـ SSE زي `response()->eventStream()` اللي بيبعت `event:` و `data:`.

---

## 4. Structured Outputs
> 📍 `04-ollama-structured-outputs.pdf` ص 1–5

**الفكرة:** تجبر رد الموديل على **JSON schema**. ده اللي استخدمته في Step 02 Task 5 و Step 03 Task 6.

**⚠️ أول سطر في الصفحة:** "Ollama's cloud currently does not support structured outputs". يعني الـ cloud models (`:cloud`) **مش بتدعمها** حالياً. (ده كان في Step 03 كمان.)

**طريقتين (ص 1–2):**
1. **`"format": "json"`**: أي JSON صحيح، من غير شكل محدد.
2. **`"format": {...schema...}`**: JSON بشكل الـ schema بالظبط.

**نصيحة مهمة (ص 2):** "It is ideal to also pass the JSON schema as a string in the prompt to ground the model's response". يعني **ابعت الـ schema في الـ prompt كمان** (مش في `format` بس)، عشان الموديل يفهم الشكل اللي مطلوب منه، والـ grammar يضمنه. (ده عكس Claude اللي بيضيف system prompt بالـ format لوحده، الشرح 02 جزء 3.7.)

**💡 ربط بكودك:** الـ `SYSTEM_PROMPT` بتاع الإيصالات بيوصف الـ fields بالكلام (vendor، و date بصيغة YYYY-MM-DD...). ده نوع من الـ grounding، بس مش الـ schema نفسه. ممكن تجرّب الفرق.

**Example: Extract structured data (ص 2–3):** بـ Pydantic: `Pet` (name، و animal، و age، و `color: str | None`، و `favorite_toy: str | None`)، و `PetList` فيه `pets: list[Pet]`. وبعدين:
```python
response = chat(model='gpt-oss', messages=[...], format=PetList.model_json_schema())
pets = PetList.model_validate_json(response.message.content)
```
**ده بالظبط** نفس الـ pattern اللي في `extract()` بتاعك (`model_json_schema()` ← `format` ← `model_validate_json`).

**Example: Vision with structured outputs (ص 3–4):** `ImageDescription` فيه `Literal['Morning', 'Afternoon', 'Evening', 'Night']`، و `Optional[str] = None`، والصورة بتتبعت في `images` جوه الرسالة، و `options={'temperature': 0}`. (فيه **`Literal`** هنا، وده هيفيدك لو عايز تقصر `currency` على قيم معيّنة. التفاصيل في الشرح 06.)

**Tips (ص 4–5):**
- عرّف الـ schemas بـ **Pydantic** (أو Zod في JS) عشان تستخدمها في الـ **validation** كمان.
- **قلل الـ temperature** (مثلاً `0`) لنتايج أكتر deterministic.
- structured outputs **بيشتغل من الـ OpenAI-compatible API** عن طريق `response_format`.

**قارن بـ Claude (الشرح 02):**

| | Ollama | Claude |
|---|---|---|
| الـ parameter | `format` | `output_config.format` (أو `messages.parse(output_format=...)`) |
| الـ validation | إنت بـ `model_validate_json` | `parse()` بيعملها |
| الـ schema في الـ prompt | **إنت** (نصيحة الـ docs) | Claude بيضيفه لوحده (وبتدفع tokens) |
| الـ constraints (`minimum`...) | مش مذكور في الصفحة، **اتأكد بنفسك** | مش مدعومة، والـ SDK بيحوّلها لـ description |
| `temperature` | مسموح | مش مسموح على الموديلات الجديدة |
| الـ cloud | ❌ مش مدعوم | ✅ |

---

## 5. ⭐ Anthropic compatibility
> 📍 `04-ollama-anthropic-compatibility.pdf` ص 1–9

**الفكرة:** "Connect Anthropic clients and tools such as Claude Code to Ollama. Ollama supports **a subset** of the Anthropic Messages API". يعني أدوات وكود مكتوبين لـ Anthropic يشتغلوا على Ollama، **بس مش كل الـ features**.

### Direct cloud access (ص 1–2)
`OLLAMA_API_KEY` و `curl https://ollama.com/v1/messages` بـ `Authorization: Bearer` (الـ cloud **مابيقبلش** `x-api-key` لوحده، عكس Anthropic) و `anthropic-version: 2023-06-01`. والموديلات المتوافقة بتدعم messages و streaming و function calling، والـ tool-choice والـ deferred tools والـ web search **مش مدعومين بالكامل**.

### Local server usage (ص 2–4) — ده اللي يهمك
- استخدم **`ollama`** كـ placeholder API key (الـ local server **مش بيتشيك على الـ key**، بس الـ SDK بيطلب key).
- **Environment variables** لأدوات زي Claude Code:
  - `ANTHROPIC_AUTH_TOKEN=ollama` (مطلوب بس متجاهَل)
  - `ANTHROPIC_BASE_URL=http://localhost:11434`

**مثال `basic.py` (ص 3):**
```python
client = anthropic.Anthropic(base_url='http://localhost:11434', api_key='ollama')
message = client.messages.create(model='qwen3-coder', max_tokens=1024,
                                 messages=[{'role': 'user', 'content': 'Hello, how are you?'}])
print(message.content[0].text)
```
**مثال `streaming.py`:** نفس `client.messages.stream(...)` و `stream.text_stream` بالظبط زي Claude.
**مثال `tools.py`:** tools بنفس شكل Anthropic، وبتلف على `message.content` وتشوف `block.type == 'tool_use'`. (Step 10.)

**تشبيه من Laravel:** ده زي إنك تغيّر `MAIL_HOST` لـ **Mailpit** local وإنت بتطوّر: نفس الكود ونفس الـ Mail facade، بس الإيميلات مش بتخرج من جهازك. ولما تنزل production تغيّر الـ host للـ SMTP الحقيقي. هنا: نفس كود الـ SDK، `base_url` = Ollama وإنت بتجرّب، و = Anthropic لما يبقى معاك key. ⚠️ والتشبيه مضلل في نقطة: Mailpit بيعمل **كل** حاجة الـ SMTP بيعملها تقريباً، لكن Ollama compatibility **subset**، والموديل نفسه مختلف تماماً (qwen 3B مش Claude)، فالجودة والسلوك مش هيبقوا زي بعض.

### Endpoints و Supported features (ص 5–7)
**Endpoint واحد:** `/v1/messages`.

**مدعوم:** Messages، و Streaming، و System prompts، و Multi-turn، و Vision (صور)، و Tools، و Tool results، و Thinking.

**Request fields المدعومة:** `model`، و `max_tokens`، و `messages` (نص، وصور base64، و arrays of blocks، و tool_use، و tool_result، و thinking)، و **`system`** (string أو array)، و `stream`، و **`temperature`**، و `top_p`، و `top_k`، و `stop_sequences`، و `tools`، و `thinking`، و **`output_config`** (مكتوب جنبه **`effort`** بس)، و `tool_choice`، و `metadata`.

**Response fields:** `id`، و `type`، و `role`، و `model`، و `content` (text، و tool_use، و thinking)، و `stop_reason` (**`end_turn`، و `max_tokens`، و `tool_use`** بس)، و `usage` (`input_tokens`، و `output_tokens`).

**Streaming events:** `message_start`، و `content_block_start`، و `content_block_delta` (text، و input_json، و thinking)، و `content_block_stop`، و `message_delta`، و `message_stop`، و `ping`، و `error`.

**Thinking:** `"enabled"` و `"disabled"` = on/off، والموديلات اللي ماتقدرش تقفل الـ thinking بتاخد أقل مستوى. والـ effort names بتتطبّق لو الموديل بيدعمها، وإلا بيرجع للـ default.

**🔍 حاجات لازم تتأكد منها بنفسك (Task 1 و 5):**
- **`output_config.format`** (structured outputs): الـ docs ذكرت `output_config` بـ `effort` **بس**، ومذكرتش `format`. يعني **مش مضمون** إن structured outputs شغّالة من الـ endpoint ده. **جرّب وشوف** هل الرد بيلتزم بالـ schema ولا لأ.
- **الـ `usage`:** الـ docs بتقول `input_tokens` و `output_tokens` بس. شوف الرد الحقيقي فيه إيه، وقارن `input_tokens` بـ `prompt_eval_count` من `/api/chat` لنفس الرسالة.
- **الـ `message_start` في الـ stream:** شوف الـ `usage` فيه أرقام حقيقية ولا لأ، وقارنها بالـ `message_delta`.

### Models (ص 7–8)
Local: `ollama pull <model>` الأول. Cloud: بأسماء زي `gemma4:cloud`. **وحيلة لطيفة:** لو أداة مصممة على اسم موديل Claude (`claude-3-5-sonnet`)، تعمل `ollama cp qwen3-coder claude-3-5-sonnet` (نسخة بالاسم ده)، والأداة تشتغل. (متعملهاش دلوقتي، بس افهم إن **اسم الموديل في Ollama مجرد label**.)

### ⭐ Differences from the Anthropic API (ص 8–9)
**سلوك مختلف:**
- الـ local server **مش بيتشيك على الـ API keys**.
- الـ cloud بيرفض `anthropic-version` أقدم من `2023-06-01`.
- **"Token counts are approximations based on the underlying model's tokenizer"**: الأرقام بـ tokenizer **الموديل الـ local** (Qwen)، **مش** Claude. يعني الـ `usage` من Ollama compatibility **مايتستخدمش** لتقدير تكلفة Claude.

**مش مدعوم:**

| الـ feature | يعني إيه ليك |
|---|---|
| `/v1/messages/count_tokens` | ماتقدرش تعدّ tokens Claude local (Bonus B1 محتاج key) |
| `tool_choice` | (Step 10) |
| `metadata` | (user_id) |
| **Prompt caching** (`cache_control`) | ماتقدرش تجرّب caching Claude local. (Ollama عنده caching **لوحده** بطريقته، بس مش بالـ `cache_control`) |
| Batches API | |
| Citations | |
| PDF support | |
| **Server-sent errors** | الـ errors بترجع **HTTP status**، مش error event في الـ stream |

**دعم جزئي:** الصور **base64 بس** (مش URL)، و extended thinking أساسي (`budget_tokens` بيتقبل بس مش بيتطبّق).

### 💡 الخلاصة: Ollama compatibility ينفع لإيه ومينفعش لإيه؟
- ✅ **ينفع:** تتعلم الـ SDK وشكل الـ API (messages، و content blocks، و streaming events، و errors) **ببلاش ومن غير ما الداتا تخرج**. وتكتب `AnthropicProvider` وتجرّبه وتعمل له tests. ولما يبقى معاك key، **نفس الكود** يشتغل على Claude بتغيير `base_url` و `api_key`.
- ❌ **مينفعش:** تقيس **جودة** Claude (الموديل qwen)، أو **tokens** Claude (tokenizer مختلف)، أو **caching** Claude، أو **structured outputs** Claude (مش مضمونة هنا)، أو **سلوك الـ parameters** (Claude الجديد بيرفض `temperature`، و Ollama بيقبله).
- يعني الكود اللي **عدّى على Ollama مش متأكد إنه هيعدّي على Claude**. وده سبب إن الـ `AnthropicProvider` لازم يتعامل مع فروق زي `temperature` بشكل صريح.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **NDJSON مقابل SSE**، و **Anthropic-compatible API (Ollama)**، و **API Compatibility Subset**، و **Base URL Swapping**، و **`prompt_eval_cached_count`**، و **Schema Grounding في الـ Prompt**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. بعتّ request لـ /api/chat في Ollama من غير "stream" في الـ body، والـ httpx.post(...).json() وقع. ليه؟</summary>

لأن الـ default في `/api/chat` هو `stream: true`، فالرد NDJSON: كذا سطر JSON ورا بعض، مش JSON واحد. `.json()` بيحاول يعمل parse للنص كله كـ JSON واحد ويقع. الحل: `"stream": false` صريح (زي `llm_client.py`)، أو تقرا الرد سطر سطر. وده عكس Anthropic اللي الـ default فيها non-streaming.
</details>

<details><summary>2. إيه الفرق بين NDJSON و SSE؟ وأنهي واحد أسهل في الـ parsing؟</summary>

NDJSON: كل سطر JSON كامل بنفس الشكل، وآخر سطر فيه `done: true` والأرقام. SSE: events بأنواع، كل event سطر `event:` وسطر `data:` وسطر فاضي، والنص في `content_block_delta` بس، والـ usage متقسّم بين `message_start` و `message_delta`. NDJSON أسهل (`json.loads` لكل سطر)، و SSE أغنى (أنواع blocks مختلفة زي thinking و tool_use في نفس الـ stream، و ping، و errors) بس محتاج تفلتر وتتجاهل الأنواع اللي مش محتاجها.
</details>

<details><summary>3. استخدمت الـ SDK بتاع anthropic على Ollama وكل حاجة اشتغلت. ده معناه إن الكود جاهز لـ Claude؟</summary>

مش بالضرورة. Ollama compatibility subset: بيقبل `temperature` (Claude الجديد بيرفضه بـ 400)، ومش بيدعم prompt caching ولا count_tokens، و structured outputs مش مذكورة كمدعومة، والـ errors بترجع HTTP status مش events، والصور base64 بس، والـ usage بـ tokenizer الـ Qwen. والموديل نفسه مختلف، فالـ prefill مثلاً ممكن يشتغل على qwen ويترفض على Claude. الكود "متوافق في الشكل"، لكن لازم تتعامل مع الفروق دي صراحةً وتجرّب على Claude لما يبقى معاك key.
</details>

<details><summary>4. prompt_eval_count = 330 و prompt_eval_cached_count = 172 في Ollama. ولو نفس الموقف في Anthropic، الـ usage هيبقى إزاي؟</summary>

في Ollama الـ cached **جزء** من الـ 330: يعني 158 اتقروا جديد و 172 من الـ cache. في Anthropic (لو الـ caching اشتغل)، الأرقام منفصلة: `cache_read_input_tokens: 172` و `input_tokens: 158` (اللي بعد الـ breakpoint)، والإجمالي = المجموع. نفس الفكرة بحسابات مختلفة، فلو الـ `ChatResult` بتاعك فيه `input_tokens` واحد، لازم تقرر هو "الكل" ولا "اللي مش متعمله cache"، وتحوّل كل provider للمعنى ده.
</details>

<details><summary>5. ليه الـ docs بتنصح تبعت الـ JSON schema في الـ prompt كمان، مع إن `format` بيجبر الشكل؟</summary>

لأن الـ `format` بيمنع الموديل يطلّع tokens تكسر الشكل (constrained decoding)، بس مش بيشرحله **معنى** كل field. لو الموديل مش فاهم المطلوب، هيطلّع JSON صحيح الشكل بقيم غلط أو فاضية، وهيحس إنه "محشور" في شكل مش متوقعه. الـ schema (أو وصف الـ fields) في الـ prompt بيعمل grounding: الموديل يخطط للرد صح، والـ grammar يضمن الشكل. Claude بيعمل ده لوحده (بيضيف system prompt بالـ format)، و Ollama بيسيبه عليك.
</details>

<details><summary>6. حاسب تكلفة Claude بالـ usage اللي راجع من Ollama /v1/messages. إيه الغلط؟</summary>

الـ docs بتقول إن الـ token counts في Ollama compatibility "approximations based on the underlying model's tokenizer"، يعني بـ tokenizer الـ Qwen، مش Claude. وClaude الجديد ليه tokenizer خاص بيطلّع tokens أكتر من القديم بـ ~30%، والفرق مع Qwen مجهول. فالتقدير ممكن يبعد بنسبة مش معروفة. الصح: `count_tokens` على Claude (ببلاش بس محتاج key)، أو `usage` من request حقيقي.
</details>

<details><summary>7. الـ docs بتستخدم http://localhost:11434 كـ base_url. ليه إنت هتستخدم 127.0.0.1؟</summary>

لأن في Step 03 Task 3 اكتشفنا إن `localhost` على Windows بيحاول IPv6 (`::1`) الأول، و Ollama بيسمع على IPv4، فكل request كان بيضيّع ~2 ثانية قبل ما يرجع لـ IPv4. `127.0.0.1` بيروح IPv4 على طول. وده بيفرق جداً في قياسات الـ TTFT في Task 3.
</details>
