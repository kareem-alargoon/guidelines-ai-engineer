# شرح: Anthropic Courses — *Anthropic API Fundamentals* (6 notebooks)

> **المصدر:** [anthropics/courses — anthropic_api_fundamentals](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) — Anthropic
> **الملفات:** `resources/articles/04-anthropic-course-0N-*.ipynb` (6 ملفات)
> **إزاي تقرا:** افتح الـ notebook في PyCharm (بيعرض الـ `.ipynb` بالخلايا) أو على GitHub، واقرا كل lesson وبعدين الشرح بتاعها هنا. الـ 📍 بيقولك اسم الـ notebook واسم الـ section جواه.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

لحد دلوقتي كلّمت الموديلات بطريقتين: `POST /api/chat` بتاع Ollama (Steps 01–03)، و OpenAI-compatible API (Step 03 Task 5). الكورس ده بيعلّمك الطريقة **التالتة والأهم في الشغل**: **الـ Messages API بتاع Anthropic عن طريق الـ SDK الرسمي بتاع Python** (`pip install anthropic`).

| # | الـ Lesson | الملف | أهميتها ليك |
|:---:|---|---|:---:|
| 1 | Getting started | `04-anthropic-course-01-getting-started.ipynb` | ⭐⭐ |
| 2 | Working with messages | `04-anthropic-course-02-messages-format.ipynb` | ⭐⭐⭐⭐ |
| 3 | Models | `04-anthropic-course-03-models.ipynb` | ⭐⭐ (قديم جداً) |
| 4 | Model parameters | `04-anthropic-course-04-parameters.ipynb` | ⭐⭐⭐⭐ |
| 5 | Streaming | `04-anthropic-course-05-streaming.ipynb` | ⭐⭐⭐⭐ |
| 6 | Prompting with images (Vision) | `04-anthropic-course-06-vision.ipynb` | ⭐⭐ (اختياري، Step 13) |

> ⏳ **عمر المصدر — مهم جداً:** الريبو ده **اتعمله archive يوم 2026-09-15** (بقى read-only). والأمثلة كلها مكتوبة على موديلات **Claude 3 و 3.5** (`claude-3-haiku-20240307` وأخواتها)، ودول **اتشالوا (retired)** من زمان (شوف شرح Model deprecations في Step 03). يعني **ولا سطر كود في الكورس هيشتغل زي ما هو** من غير ما تغيّر اسم الموديل.
> **طب ليه بنقراه؟** لأن **شكل الـ API نفسه** (messages، و content blocks، و stop_reason، و usage، و streaming events) لسه هو هو، والكورس بيشرحه ببطء وبأمثلة. بس فيه حاجات **اتغيّرت فعلاً** في الموديلات الجديدة، وهنبّه عليها في كل جزء بعلامة ⏳، والحقيقة الحالية من الـ docs اللي في الشرح [02](02-anthropic-messages-streaming-structured.md).

**الصورة الكبيرة قبل ما تبدأ:** الـ SDK ده **wrapper فوق HTTP**. كل `client.messages.create(...)` في الآخر هو `POST https://api.anthropic.com/v1/messages` بـ JSON body، زي اللي بتعمله بـ `httpx` في `llm_client.py` بالظبط. الـ SDK بيضيف: الـ headers (الـ key والـ version)، و **typed objects** بدل الـ dicts، و retries، و streaming helpers.

**تشبيه من Laravel:** الفرق بين `Http::post('https://api.stripe.com/...')` وبين `composer require stripe/stripe-php` وإنك تكتب `$stripe->charges->create([...])`. الاتنين نفس الـ HTTP request، بس الـ SDK الرسمي بيديك methods و objects ومعالجة errors جاهزة.

> 💡 **هتجرّب الكود ده إزاي من غير key؟** Ollama عنده endpoint **متوافق مع Anthropic** (`/v1/messages`)، يعني نفس الـ SDK يشتغل على `qwen2.5:3b` بتاعك بتغيير `base_url` بس. التفاصيل في الشرح [05](05-ollama-api-and-anthropic-compat.md)، وده اللي التاسكات مبنية عليه.

---

## 1. Getting started
> 📍 `04-anthropic-course-01-getting-started.ipynb` — كل الـ notebook

### 1.1 Installing the SDK
**الفكرة:** بتسطّب الـ package اسمها `anthropic` بـ `pip install anthropic`. الـ notebook بيفرّق بين `%pip install` (جوه notebook) و `pip install` (من الـ terminal). إنت هتشتغل من الـ terminal، فـ `pip` (أو `uv add`، شوف الشرح [06](06-httpx-pydantic-uv.md)).

> ⏳ الكورس بيقول الـ SDK محتاج **Python 3.7.1** أو أحدث. الـ README الحالي للـ SDK بيقول **Python 3.10+**. إنت على 3.13، فمفيش مشكلة.

### 1.2 Getting an API key
**الفكرة:** بتعمل حساب على الـ Console، وتروح لصفحة API Keys، وتعمل key باسم يوضّح هو لإيه. ملاحظتين مهمين:
- الـ key **بيظهر مرة واحدة بس**. لو قفلت الصفحة من غير ما تنسخه، اعمل واحد جديد.
- الـ **rate limits** بتتحسب على مستوى **الحساب (organization)**، مش على مستوى الـ key. يعني لو عملت 5 keys، مش هتاخد 5 أضعاف الـ limit. (هنشوف ده بالتفصيل في الشرح [04](04-anthropic-errors-rate-limits-sdk.md).)

> ⏳ الـ Console اسمه دلوقتي **Claude Console** وعنوانه `platform.claude.com` (الكورس بيقول `console.anthropic.com`).

### 1.3 Safely storing your API key
**الفكرة:** الـ key زي الـ password: **متحطوش في الكود، ومتعملوش commit**. الطريقة اللي الكورس بيقترحها: ملف `.env` فيه `ANTHROPIC_API_KEY=...`، وتقراه بـ `python-dotenv` (`load_dotenv()` وبعدين `os.getenv(...)`).

**تشبيه من Laravel:** ده **بالظبط** `.env` و `env('STRIPE_SECRET')` في Laravel، و `python-dotenv` بيعمل اللي Laravel بيعمله لوحده وهو بيقوم (بيقرا `.env` ويحطه في environment variables).

**عندنا في الريبو:** `.env` موجود في `.gitignore`. وفي Step 03 اتعودت على `$env:LLM_API_KEY = "..."` في PowerShell، ودي نفس الفكرة من غير ملف. الاتنين صح، المهم إن الـ key **مايدخلش الكود**.

### 1.4 Making basic requests with the client
**الفكرة:** خطوتين:
1. تعمل **client object**: `client = Anthropic()`. الـ SDK **بيدوّر لوحده** على environment variable اسمه `ANTHROPIC_API_KEY`، فمش لازم تبعته. (وتقدر تبعته صريح بـ `Anthropic(api_key=...)`.)
2. تبعت رسالة بـ `client.messages.create(model=..., max_tokens=..., messages=[...])`، وتقرا الرد من `response.content[0].text`.

**تشبيه من Laravel:** الـ client زي `Http::withToken($key)->baseUrl('https://api.anthropic.com')` متجهّز مرة واحدة، وبعدين كل request بيستخدمه. **اعمله مرة واحدة** وإعادة استخدامه، مش client جديد في كل request (ده هيظهر تاني في الـ httpx: connection pooling).

> ⏳ **`response.content[0].text` بقى خطر:** على الموديلات الجديدة اللي الـ **thinking** فيها شغّال by default (زي Opus 5.5)، أول block في `content` ممكن يبقى **thinking block** مش text، فـ `content[0].text` يقع. الـ docs الحالية بتاخد **أول block نوعه `text`**. (التفاصيل في الشرح 02، جزء 1.4.)

**التمرين:** script يحمّل الـ key ويطلب نكتة. (هتعمل نسخة منه على Ollama في Task 2.)

---

## 2. Working with messages
> 📍 `04-anthropic-course-02-messages-format.ipynb`

### 2.1 Messages format
> 📍 section *Messages format*

**الفكرة:** الـ parameter `messages` هو **list of dicts**، كل dict فيه key اتنين:
- `role`: يا `"user"` (إنت) يا `"assistant"` (Claude).
- `content`: يا **string**، يا **list of content blocks** (كل block فيه `type` زي `"text"` أو `"image"`). الـ string مجرد اختصار لـ block واحد نوعه text.

والـ messages **بتتبادل**: user ← assistant ← user ← ... والـ list دي هي **تاريخ المحادثة كله**، اللي بيدّي الموديل الـ context (الكورس بيسميها *context preservation*).

**اللي إنت عارفه من Step 01:** الـ LLM **stateless**. الـ API مش فاكر حاجة بين request والتاني، فإنت اللي بتبعت التاريخ كله كل مرة (زي ما عملت في `chat_cli.py` في Step 02). ونفس الكلام هنا.

**الفرق عن Ollama:** في `/api/chat` بتاع Ollama، الـ system prompt بيتبعت **جوه** `messages` كـ `{"role": "system", ...}`. في Anthropic، الـ `role` يا `user` يا `assistant` بس، والـ system prompt **parameter لوحده** اسمه `system` (جزء 4.5). ده أهم فرق هتقابله وإنت بتكتب `AnthropicProvider`.

> ⏳ فيه حاجة جديدة في الـ docs: تقدر تحط `{"role": "system"}` **في نص** المحادثة (مش أولها) على الموديلات الجديدة. ده موضوع متقدم، والشرح 02 بيوضّحه. للتاسكات: الـ system prompt في parameter `system`.

**الملحوظة المهمة:** مش كل استخدام محتاج تاريخ. list فيها رسالة واحدة بس **عادي جداً** (زي استخراج داتا من إيصال: كل إيصال request لوحده).

### 2.2 Inspecting the message response
> 📍 section *Inspecting the message response*

**الفكرة:** الرد مش string، ده **`Message` object** فيه:

| الـ field | معناه | المقابل في Ollama `/api/chat` |
|---|---|---|
| `id` | رقم فريد للرسالة (`msg_...`) | مفيش |
| `type` | دايماً `"message"` | مفيش |
| `role` | دايماً `"assistant"` | `message.role` |
| `content` | **list of blocks**، والنص في `content[i].text` | `message.content` (string) |
| `model` | الموديل اللي رد | `model` |
| `stop_reason` | ليه وقف (جزء 4) | `done_reason` |
| `stop_sequence` | أنهي stop sequence وقّفته (لو فيه) | مفيش |
| `usage` | `input_tokens` و `output_tokens` | `prompt_eval_count` و `eval_count` |

ورسالة الكورس الأساسية: **لو هتفتكر حاجة واحدة، افتكر إن `content` فيه اللي الموديل كتبه**، وإنه **list** مش string.

**ليه list؟** لأن الرد ممكن يبقى فيه أكتر من نوع: نص، وبعده **طلب استخدام tool** (Step 10)، أو **thinking** قبل النص. كل نوع block لوحده.

**تشبيه من Laravel:** زي `$response->json()` من API بيرجّع `data` كـ array of items، كل item ليه `type`. مش بتعمل `$response['data'][0]` وخلاص، لأن الترتيب مش مضمون.

**التمرين:** function اسمها `translate(word, language)`، والـ bonus إنها ترجع الكلمة بس من غير مقدمة. (الحل في الكورس بيستخدم `claude-3-opus` اللي اتشال.)

### 2.3 Message list mistakes
> 📍 section *Message list mistakes*

**الفكرة:** الكورس بيقول فيه غلطتين بيرجعوا error:
1. **الـ list تبدأ بـ assistant message.** لازم تبدأ بـ user.
2. **رسالتين ورا بعض بنفس الـ role** (assistant ← assistant).

> ⏳ **الغلطة التانية اتغيّرت:** الـ API reference الحالي (جوه صفحة Token counting اللي عندك، تحت `messages`) بيقول إن الـ **turns المتتالية بنفس الـ role بتتدمج في turn واحد**، يعني مبقتش error. متعتمدش على ده في الكود: خلّي الـ list بتتبادل، لأن ده أوضح ولأن providers تانية (و Ollama compatibility) ممكن تتصرف بشكل مختلف.

### 2.4 Messages list use cases
> 📍 section *Messages list use cases*

**1) Putting words in Claude's mouth (الـ prefill):** تحط **assistant message في الآخر** فيها بداية الرد، والموديل **يكمّل** منها. مثال الكورس: تحط أول سطر من الـ haiku، والرد يبقى باقي الـ haiku بس (من غير السطر اللي إنت كتبته). وبتجمعهم بنفسك.

> ⏳ **الـ prefill مبقاش شغّال على الموديلات الجديدة:** حسب الـ docs الحالية، الموديلات بعد Claude 4.5 (يعني 4.6 وما بعدها، وده فيه كل الموديلات اللي هتستخدمها) **بترجع 400 error** لو آخر رسالة assistant. البدائل: **structured outputs** لو عايز JSON، أو **تعليمات في الـ system prompt** للشكل ("رد بالحرف بس"). التفاصيل في الشرح 02، جزء 1.3.
> **على Ollama** الـ prefill لسه بيشتغل مع موديلات كتير، فمتتلخبطش لو جرّبته local واشتغل.

**2) Few-shot prompting:** تستخدم تاريخ المحادثة كـ **أمثلة**. مثال الكورس: عايز تصنّف tweets لـ `POSITIVE` أو `NEGATIVE` بكلمة واحدة بدل فقرة تحليل طويلة. فبتبعت 3 أزواج (user: tweet، assistant: التصنيف) وبعدين الـ tweet الجديد، والموديل بيقلّد الشكل.

ده **in-context learning** اللي اتشرح في Step 01 (concept موجود في `docs/concepts.md`)، والكورس بيوريك إن الـ messages format نفسه طريقة سهلة تبعت بيها الأمثلة (ومش لازم كلها في نص واحد). وده لسه شغّال على كل الموديلات.

**💡 ربط بشغلك:** في Step 03 Task 6 كان الـ prompt بتاع الإيصالات zero-shot (تعليمات بس). Few-shot بإيصال أو اتنين **ممكن** يحسّن الـ vendor (الغلطات كانت نسخ OCR noise). ده هيرجع في Task 8 كطريقة "تطوّل" الـ prompt عشان يعدّي الحد الأدنى للـ caching.

### 2.5 Exercise: build a chatbot
**الفكرة:** chatbot في الـ terminal: list للتاريخ، و `input()`، وتضيف رسالة اليوزر، وتبعت، وتطبع، وتضيف رد الموديل، وتلف. وطريقة تخرج (`quit`).

ده **نفس** `chat_cli.py` اللي عملته في Step 02 Task 7 (وكان فيه كمان context size و sliding window و summary). في Task 4 هتطوّره عشان يعمل **streaming** ويشتغل على أي provider.

---

## 3. Models
> 📍 `04-anthropic-course-03-models.ipynb`

> ⏳ **الـ lesson دي أقدم حاجة في الكورس.** بتتكلم عن Claude 3 Haiku/Sonnet/Opus و 3.5 Sonnet، وكلهم اتشالوا. الموديلات الحالية (Haiku 5.5، و Sonnet 5.5، و Opus 5.5، و Fable 5.2) والأسعار اتشرحوا بالتفصيل في Step 03 (`steps/03-models-and-providers/notes/03-anthropic-models-and-pricing.md`). خد من الـ lesson دي **طريقة التفكير** بس.

### 3.1 Claude models
**الفكرة:** 3 محاور لاختيار الموديل: **latency** (سريع قد إيه)، و **capabilities** (ذكي قد إيه)، و **cost** (غالي قد إيه). ده نفس الـ Pareto اللي في Ch.4 من الكتاب (Step 03).

### 3.2 Comparing model speeds
**الفكرة:** function بتبعت نفس الـ prompt لكل موديل وتقيس الوقت، و `time_per_token = execution_time / output_tokens`. والنتيجة إن Haiku الأسرع.

**⚠️ نقدها بعين Step 03:** القسمة على **الوقت الكلي** فيها الـ TTFT (الشبكة والـ prefill)، فدي مش سرعة التوليد الحقيقية. في Step 03 Task 3 عملت ده صح: `output_tokens / eval_seconds`. وعلى الـ API مفيش `eval_seconds` (الـ API مش بيرجّع الوقت متقسّم)، فالقياس الأدق بيبقى بالـ **streaming**: من أول token لآخر token (Task 3).

والكورس نفسه بيعترف إن المقارنة دي "مش rigorous"، وإنهم عملوا رسمة تانية بـ 50 تكرار و `max_tokens` ثابت عشان المقارنة تبقى عادلة. وده **evaluation hygiene** اللي الكتاب اتكلم عنه: كرّر، وثبّت الطول.

### 3.3 Comparing model capabilities
**الفكرة:** مسألة حسابية (geometric mean) بتتسأل 7 مرات لكل موديل. الموديلات الأقوى جابت 7/7، والأضعف 2/7 و 3/7. والكورس بينبّه إن ده **demo تعليمي** مش benchmark.

**الدرس الحقيقي:** **تكرار نفس السؤال** بيكشف الـ **inconsistency** (concept من Step 02). موديل بيجيب الصح "أحياناً" مش موديل ينفع لمهمة محتاجة دقة. ونفس الفكرة في Step 03 Task 6: لازم eval set بتاعك.

### 3.4 Picking a model
**الفكرة:** الكورس بيقترح: **ابدأ بأرخص وأسرع موديل** (كان Haiku)، وجرّب، ولو مش كفاية **اعمل upgrade**، وده لازم يبقى قرار مبني على **evals بتاعتك**.

ده نفس اقتراح الكتاب ونفس صفحة Choosing a model في Step 03 (الـ "efficiency-first approach"). يعني الفكرة **لسه صح**، والأسماء بس اللي اتغيّرت.

---

## 4. Model parameters
> 📍 `04-anthropic-course-04-parameters.ipynb`

### 4.1 Max tokens
> 📍 section *Max tokens*

**الفكرة:** فيه **3 parameters إجباريين** في كل request: `model`، و `max_tokens`، و `messages`.

> 💡 **فرق عن Ollama والـ OpenAI:** في Ollama الـ `num_predict` (اللي `llm_client` بيسميه `max_tokens`) **اختياري**. في Anthropic `max_tokens` **إجباري**، ولو مبعتهوش الـ request يترفض. افتكر ده وإنت بتكتب `AnthropicProvider`: لازم default.

**Tokens:** الموديل مش بيشتغل بالكلمات، بيشتغل بـ **tokens** (أجزاء كلمات)، وبيولّد **token واحد في المرة**. والكورس بيقول إن الـ token ≈ **3.5 حرف إنجليزي** لـ Claude.

> ⏳ **الرقم ده قديم:** الموديلات من Claude Opus 4.7 وأحدث (ومنهم Fable و Opus 5.5) بتستخدم **tokenizer أحدث** بيطلّع **~30% tokens أكتر** لنفس النص (صفحة Token counting، الشرح 03). يعني الـ 3.5 حرف بقت أقل. والعربي أصلاً بياخد tokens أكتر من الإنجليزي (Step 02).

**`max_tokens` بيعمل إيه بالظبط؟** **سقف** لعدد الـ tokens اللي الموديل يولّدها. لو وصل له، بيقف **في نص الكلام** (مثال الكورس: `max_tokens=10` ← "Here is a poem for you: The"). وتعرف ده من `stop_reason == "max_tokens"`. ولو خلّص طبيعي: `stop_reason == "end_turn"`.

**نقطتين مهمين جداً:**
1. **الموديل مش "عارف" الـ `max_tokens`.** مش بيقصّر رده عشان السقف قريب، هو بيكتب عادي والـ API بيقطعه. يعني لو عايز رد قصير، **اطلبه في الـ prompt**، و `max_tokens` حماية بس.
2. **السقف مش هدف.** `max_tokens=1000` لنكتة طلّع 55 token بس.

ده نفس اللي شفته في Step 02 Task 4 (stop reasons) على Ollama (`done_reason: "length"`).

**ليه تغيّر `max_tokens`؟** الكورس بيقول 3 أسباب: الـ **API limits**، و الـ **performance** (توليد أكتر = وقت أكتر)، و **جودة الرد** (لو صغير قوي الرد يتقطع). والتجربة بتاعته: 100 token في 1.5 ث، و 1000 في 8.3 ث، و 3433 في 28.8 ث. يعني **الوقت تقريباً خطي مع الـ output tokens** (ده الـ decode اللي في Step 02 و 03).

> ⏳ **تحديثين من الـ docs الحالية:**
> - الـ **thinking tokens بتتحسب جوه `max_tokens`** على الموديلات اللي فيها thinking شغّال by default. يعني `max_tokens` صغير ممكن يخلّص في الـ thinking قبل ما الموديل يكتب الرد.
> - الـ OTPM rate limit بيتحسب على الـ tokens **اللي اتولّدت فعلاً**، مش على `max_tokens`. يعني مفيش عقوبة في الـ rate limit لو حطيت `max_tokens` كبير (صفحة Rate limits، الشرح 04). بس الـ SDK بيرفض request **non-streaming** متوقع ياخد أكتر من 10 دقايق، فلـ `max_tokens` الكبير جداً استخدم streaming.

### 4.2 Stop sequences
> 📍 section *Stop sequences*

**الفكرة:** `stop_sequences=["}"]` = list of strings، أول ما الموديل يولّد واحدة منهم **يقف**. وبتعرف من `stop_reason == "stop_sequence"`، و `stop_sequence` بيقولك **أنهي واحدة**.

**مثال الكورس:** طلب JSON، والموديل كتب الـ JSON وبعده شرح طويل. بـ `stop_sequences=["}"]` وقف بعد الـ JSON. **بس** الـ `}` نفسه **مش موجود** في الرد، فلازم تضيفه بنفسك قبل الـ parsing.

**⚠️ ليه ده حل ضعيف للـ JSON؟** لو الـ JSON فيه object جوه object، أول `}` هيقفل الداخلي ويقطع الباقي. والحل الصح للـ JSON هو **structured outputs** (الشرح 02، جزء 3)، اللي إنت استخدمته على Ollama بـ `format`.

**الاستخدام المعقول:** تقفل list بعدد معيّن (التمرين: لو عايز 3 أسئلة، وقّف عند `"4."`)، أو تقفل عند علامة إنت محددها في الـ prompt.

### 4.3 Temperature
> 📍 section *Temperature*

**الفكرة:** من 0 لـ 1، والـ default **1**. القيمة القليلة = الموديل يختار الأكثر احتمالاً (ردود متشابهة)، والعالية = اختيارات أكتر تنوع. والنصيحة: **قريب من 0 للمهام التحليلية، وقريب من 1 للإبداع**. وتجربة الكورس: `temperature=0` ← "Xendor" 3 مرات، و `1` ← 3 أسماء مختلفة. وبينبّه إن **0 مش deterministic 100%**.

ده كله اتشرح بالتفصيل في Step 02 (concept: Temperature، و Probabilistic مقابل Deterministic)، وشفته بنفسك في Step 02 Task 3 وفي Step 03 (الرد اتغيّر مع `temperature=0` بسبب الـ caching).

> ⏳ **أهم تغيير في الكورس كله:** حسب صفحة *Using the Messages API* الحالية (الشرح 02، جزء 1.1)، الـ `temperature` و `top_p` و `top_k` **مبقوش مدعومين على Claude 4.7 والأحدث**، وعلى **أي موديل** بـ API version `2026-10-21`. لو بعتّ قيمة غير الـ default ← **400 error**، ومن `2026-10-21` أي قيمة خالص ← 400. والبديل: **توجّه الموديل بالـ prompt**.
> **يعني إيه ليك؟** الـ `temperature=0` اللي بتستخدمه في الـ eval بتاع الإيصالات (Step 03 Task 6) **مش هينفع يتبعت لـ Claude الجديد**. وده بالظبط نوع الـ "parameter deprecation" اللي اتشرح في Step 03. وعلى **Ollama** (حتى من الـ Anthropic-compatible endpoint) لسه شغّال عادي. فالـ `AnthropicProvider` بتاعك لازم يقرر يعمل إيه لو حد بعت `temperature` (Task 2).

### 4.4 System prompt
> 📍 section *System prompt*

**الفكرة:** `system="..."` parameter **اختياري** بيدّي الموديل تعليمات عامة: دوره، والنبرة، والـ context. وبيأثر على **المحادثة كلها**.

ونصيحة الكورس: الـ system prompt للـ **tone والـ context والـ role** بس، والتعليمات التفصيلية والمستندات والأمثلة **في أول user message**. (دي نصيحة prompt engineering، هنرجعلها في Step 05.)

**تشبيه من Laravel:** الـ system prompt زي **config** أو middleware بيتطبّق على كل request في المحادثة، والـ user messages زي الـ request body.

**التمرين:** `generate_questions(topic, num_questions)` بـ `system` و `max_tokens` و `stop_sequences=[f"{num_questions+1}."]`. فكرة لطيفة، بس ⚠️ لو الموديل ماكتبش "4." بالظبط (مثلاً "4)")، مش هيقف.

---

## 5. Streaming
> 📍 `04-anthropic-course-05-streaming.ipynb`

### 5.1 ليه streaming؟
**الفكرة:** من غير streaming، **مش بتاخد ولا حرف** لحد ما الرد كله يخلص. ده كويس لـ background jobs (زي الإيصالات)، بس **وحش للـ UX** لو يوزر مستني قدام الشاشة. الـ streaming = تاخد الرد **حتة حتة وهو بيتكتب** (زي claude.ai).

### 5.2 Working with streams
> 📍 section *Working with streams*

**الفكرة:** `stream=True` في `messages.create(...)`، والنتيجة مش `Message`، دي **`Stream` object** (generator) بيطلّع **server-sent events (SSE)** واحد واحد، وإنت بتلف عليه بـ `for event in stream`.

**ترتيب الـ events:**
1. **`message_start`**: `Message` بـ `content` فاضي (وفيه `usage.input_tokens`).
2. لكل content block:
   - **`content_block_start`**
   - **`content_block_delta`** (واحد أو أكتر): ده اللي فيه النص في `event.delta.text`.
   - **`content_block_stop`**
3. **`message_delta`** (واحد أو أكتر): تغييرات على الرسالة كلها، زي `stop_reason`، و `usage.output_tokens`.
4. **`message_stop`**: خلاص.

**طباعة النص:** بتفلتر على `event.type == "content_block_delta"` وتطبع `event.delta.text`. وعشان النص يطلع على نفس السطر وفوراً: `print(text, end="", flush=True)`.
- `end=""` = متنزّلش سطر جديد بعد كل حتة.
- `flush=True` = اطبع دلوقتي، متستناش الـ buffer يتملي.

**الـ tokens في الـ streaming:** الـ input tokens في `message_start`، والـ output tokens في `message_delta`. يعني لازم تمسك الاتنين لو عايز تحسب التكلفة.

> ⏳ **تحديث من الـ docs:** الـ usage في `message_delta` **تراكمي (cumulative)**، يعني آخر قيمة هي الإجمالي (متجمعهمش). (الشرح 02، جزء 2.2.)

**تشبيه من Laravel:** زي **Server-Sent Events** في Laravel (`response()->stream(...)` أو `->eventStream()`)، بس إنت هنا **الـ client** اللي بيستقبل. أو زي إنك بتقرا ملف كبير بـ `fgets()` سطر سطر بدل `file_get_contents()`.

### 5.3 Other streaming event types
**الفكرة:** فيه كمان:
- **`ping`**: ملهوش محتوى، بس بيحافظ على الـ connection. تجاهله.
- **`error`**: ممكن يجي error **في نص الـ stream** (مثلاً `overloaded_error`، اللي بيقابل HTTP 529 من غير streaming). يعني الـ request بدأ بـ 200 OK، وبعدين حصلت مشكلة.

> ⏳ **تحديث:** لو بتستخدم الـ SDK، الـ docs الحالية بتقول إن كودك **مش هيشوف** event الـ error. الـ SDK بيقفل الـ stream ويرمي **exception**. ولو بتقرا الـ HTTP بنفسك (Task 3)، لازم تتعامل معاه. وكمان: **أنواع events جديدة ممكن تتضاف**، فكودك لازم **يتجاهل الأنواع اللي مايعرفهاش** بدل ما يقع.

### 5.4 Time to first token (TTFT)
> 📍 section *Time to first token (TTFT)*

**الفكرة:** أهم سبب للـ streaming هو الـ **TTFT**. أرقام الكورس (Haiku، 500 token): من غير streaming أول حرف بعد **4.19 ث** (= الرد كله)، وبـ streaming بعد **0.49 ث**، والإجمالي تقريباً هو هو (4.27 ث). ومع Opus و 1000 token: **47 ث** مقابل **1.9 ث**.

**الجملة الأهم في الـ lesson:** الـ streaming **مش بيسرّع** الرد كله. الوقت الكلي هو هو، بس اليوزر بيشوف حاجة **بدري**.

**ربط بـ Step 03:** الـ TTFT = load + prompt eval (لو local). على Ollama الـ cold start كان 1.81 ث TTFT و 0.08 warm. في Task 3 هتقيس TTFT بـ streaming على Ollama وتقارنه بالأرقام دي.

### 5.5 Streaming helpers
> 📍 section *Streaming helpers*

**الفكرة:** بدل `create(..., stream=True)` والفلترة بإيدك، فيه `client.messages.stream(...)`:
- بيتستخدم كـ **context manager** (`with ... as stream:`)، فبيقفل الـ connection لوحده.
- **`stream.text_stream`**: iterator على **النص بس** (من غير ما تفلتر الـ events).
- **`stream.get_final_message()`**: بعد ما الـ stream يخلص، بيرجّعلك **`Message` كامل متجمّع** (النص كله و usage و stop_reason)، زي اللي `create()` بيرجّعه.

والكورس بيوريك ده بـ **`AsyncAnthropic`** و `async with` و `async for` و `await` (الـ async في الشرح [07](07-realpython-asyncio.md)). وفيه كمان **event handlers** (class بتورث `AsyncMessageStream` وتعمل override لـ `on_text` و `on_stream_event`)، وفيه `on_message`، و `on_content_block`، و `on_exception`، و `on_timeout`، و `on_end`.

> ⏳ **الـ event handlers دي (subclass بـ `event_handler=`) مش موجودة في الـ docs الحالية** اللي عندك (صفحة Streaming بتوري `text_stream` و `get_final_message()` و loop على الـ events بس). متعتمدش عليها من غير ما تتأكد من نسخة الـ SDK. استخدم الـ loop على الـ events أو `text_stream`.

**تشبيه من Laravel:** `get_final_message()` زي `LazyCollection` بتلف عليها حتة حتة، وفي الآخر تعمل `->all()` وتاخد الكل.

### 5.6 Exercise: streaming chatbot
**الفكرة:** نفس الـ chatbot بتاع lesson 2، بس الرد بيتطبع وهو بيتكتب، وفي الآخر بتجمع النص (`assistant_response += content`) وتضيفه للتاريخ.

⚠️ **حاجة الحل مش بيعملها:** لو الـ stream وقع في النص (error أو Ctrl+C)، إيه اللي يتحفظ في التاريخ؟ ده جزء من Task 4.

---

## 6. Prompting with images (Vision) — اختياري
> 📍 `04-anthropic-course-06-vision.ipynb`

> 📌 **ليه اختياري؟** الـ multimodal ليه خطوة لوحده (Step 13). بس الـ lesson دي بتوضّح فكرة مهمة لـ Step 04: **`content` = list of blocks بأنواع مختلفة**. وكمان الإيصالات في الحقيقة **صور**، فده هيرجع لما نوصل هناك.

**الفكرة:**
- عشان تبعت صورة، لازم `content` يبقى **list**، فيها **image block**: `{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": "..."}}`، وجنبه text block فيه السؤال.
- الـ media types المدعومة: `image/jpeg`، و `image/png`، و `image/gif`، و `image/webp`.
- الصورة بتتحول لـ **base64**: تقرا الملف bytes (`open(path, "rb")`) ← `base64.b64encode(...)` ← `.decode("utf-8")` عشان تبقى string.
- ممكن تبعت **أكتر من صورة** في نفس الرسالة.
- **helper function** بتعمل الـ image block من path، وبتستخدم `mimetypes.guess_type()` عشان الـ media type.
- صور من URL: بـ `httpx.get(url).content` وبعدين base64. (والكورس بيستخدم `httpx` هنا، نفس اللي إنت بتستخدمه.)
- **Vision prompting tips:** كن محدد (عدّ الناس بـ "خطوة خطوة" وانتبه للمقطوعين في الصورة)، واستخدم **أمثلة** (few-shot بصورة + الـ JSON المطلوب).

> ⏳ **الـ docs الحالية بتضيف:** نوع source اسمه **`url`** (تبعت لينك الصورة على طول من غير base64)، ونوع **`file`** (صورة اترفعت بالـ Files API). والصورة بتاكل tokens كتير (في مثال الـ docs صورة واحدة ≈ 1,000 input token).
> **و Ollama compatibility** بيدعم base64 بس، **مش URL** (الشرح 05).

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **Official SDK (مقابل raw HTTP)**، و **Messages API**، و **Content Blocks**، و **Prefill**، و **Server-Sent Events (SSE)**، و **Stream Events**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. إيه الفرق بين إنك تكلّم Claude بـ httpx مباشرة وإنك تستخدم الـ SDK الرسمي؟ وإمتى تختار كل واحد؟</summary>

الاتنين في الآخر نفس الـ `POST /v1/messages`. الـ SDK بيضيف: headers جاهزة (الـ key من `ANTHROPIC_API_KEY`، و `anthropic-version`)، و typed objects بدل dicts، و **retries** تلقائي، و streaming helpers (`text_stream` و `get_final_message`)، و exceptions مقسّمة حسب نوع الـ error. اختار الـ SDK في أي تطبيق حقيقي على Claude. والـ raw HTTP مفيد عشان **تفهم** إيه اللي بيحصل، أو في لغة/بيئة مفيهاش SDK، أو لما تحتاج تحكم كامل في الـ requests.
</details>

<details><summary>2. ليه `content` في الرد list مش string؟ وإيه المشكلة في `response.content[0].text`؟</summary>

لأن الرد ممكن يبقى فيه أكتر من نوع block: text، و tool_use، و thinking. `content[0].text` بيفترض إن أول block نص، وده مش مضمون: على الموديلات اللي الـ thinking فيها شغّال by default، أول block ممكن يبقى thinking (ملوش `.text`)، فالكود يقع. الصح إنك تدوّر على أول block نوعه `"text"` (أو تجمع كل الـ text blocks).
</details>

<details><summary>3. الكورس بيعلّمك تحط بداية رد Claude في آخر assistant message (prefill). ينفع على الموديلات اللي هتستخدمها؟ وإيه البديل؟</summary>

لأ. حسب الـ docs الحالية، الموديلات من بعد Claude 4.5 بترجع 400 لو الـ request بيخلص بـ assistant message. البديل: لو عايز JSON بشكل معيّن ← structured outputs. ولو عايز شكل تاني أو من غير مقدمة ← تعليمات في الـ system prompt، وتتأكد من الرد في الكود (لأن التعليمات مش بتضمن البداية زي الـ prefill). على Ollama الـ prefill لسه شغّال مع موديلات كتير.
</details>

<details><summary>4. حطيت max_tokens=50 والرد اتقطع. الموديل "كان عارف" إن السقف 50؟ وتعرف من الكود إن الرد اتقطع إزاي؟</summary>

لأ، الموديل مش عارف `max_tokens`. هو بيكتب عادي، والـ API بيوقّفه لما يوصل للسقف. تعرف من `stop_reason == "max_tokens"` (مقابل `"end_turn"` لو خلّص طبيعي). ولو عايز رد قصير، اطلبه في الـ prompt، و `max_tokens` حماية مش طريقة تحكم في الطول. وعلى الموديلات اللي فيها thinking، الـ thinking نفسه بياكل من `max_tokens`.
</details>

<details><summary>5. ليه stop_sequences=["}"] طريقة ضعيفة إنك تاخد JSON؟</summary>

1) الـ `}` نفسه مش بيرجع في الرد، فلازم تضيفه. 2) لو الـ JSON فيه nested object، أول `}` هيقفل الداخلي ويقطع الباقي. 3) مفيش ضمان إن اللي قبل الـ `}` JSON صحيح أو بالـ schema بتاعك (ممكن يبدأ بـ "Here's the JSON:"). الحل الصح: structured outputs (`output_config.format` أو `messages.parse` في Claude، أو `format` في Ollama).
</details>

<details><summary>6. الكود بتاعك بيبعت temperature=0 لـ Claude Opus 5.5. هيحصل إيه؟ وليه الكورس مابيقولش كده؟</summary>

حسب الـ docs الحالية، `temperature` و `top_p` و `top_k` مش مدعومين على Claude 4.7 والأحدث، وأي قيمة غير الـ default بترجع 400 (ومن API version `2026-10-21` أي قيمة خالص). الكورس اتكتب على Claude 3، قبل التغيير ده، والريبو اتعمله archive. الدرس: الـ parameters بتتشال زي الموديلات، فلازم تراجع الـ docs الحالية وتخلّي الـ provider بتاعك يتعامل مع ده (يرمي error واضح أو مايبعتهوش).
</details>

<details><summary>7. الـ streaming بيخلّي الرد يخلص أسرع؟</summary>

لأ. الوقت الكلي تقريباً هو هو (في الكورس 4.19 ث مقابل 4.27 ث). اللي بيتحسّن هو الـ **TTFT**: اليوزر بيشوف أول كلمة بعد نص ثانية بدل ما يستنى الرد كله. يعني الـ streaming تحسين في **الـ UX والـ perceived latency**، مش في الـ throughput. ولـ background job (زي الإيصالات) مالوش لازمة غالباً، إلا لو `max_tokens` كبير جداً (الـ SDK بيطلب streaming عشان الـ timeout).
</details>

<details><summary>8. في الـ streaming، تجيب عدد الـ input والـ output tokens منين؟</summary>

الـ input tokens من `message_start` (`event.message.usage.input_tokens`)، والـ output tokens من `message_delta` (`event.usage.output_tokens`)، وده رقم تراكمي فآخر قيمة هي الإجمالي. أو بالـ helper: `stream.get_final_message().usage` بعد ما الـ stream يخلص.
</details>

<details><summary>9. الكورس بيقول ابدأ بأرخص موديل. ده بيتعارض مع إن "الأذكى أحسن"؟</summary>

لأ. الفكرة إن الموديل الأرخص والأسرع غالباً **كفاية** لمهام كتير، وبيخليك تجرّب بسرعة وبتكلفة قليلة. وتعمل upgrade لما **الـ evals بتاعتك** تقول إنه مش كفاية، مش لأن leaderboard قال إن فيه أذكى. ده نفس الـ efficiency-first في صفحة Choosing a model ونفس الـ workflow بتاع الكتاب في Step 03.
</details>
