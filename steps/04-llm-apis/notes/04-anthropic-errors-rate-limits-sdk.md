# شرح: Anthropic docs — Errors، و Rate limits، و الـ Python SDK README

> **المصدر:** [Claude Platform Docs](https://platform.claude.com/docs/) + [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python) — النسخة اللي اتحفظت يوم **2026-11-28**
> **الملفات:**
> - `resources/articles/04-anthropic-errors.pdf` ← *Claude API errors*
> - `resources/articles/04-anthropic-rate-limits.pdf` ← *Rate limits*
> - `resources/articles/04-anthropic-sdk-python-readme.md` ← README الـ SDK
>
> **إزاي تقرا:** ابدأ بالـ README (دقيقتين)، وبعدين Errors كلها، وبعدين Rate limits (الجداول اقراها بسرعة، الكلام اللي حواليها هو المهم).

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

لحد دلوقتي كل الـ errors في كودك كانت "Ollama مش شغّال" أو "الموديل مش موجود" (`LLMError` في `llm_client.py`). لما تكلّم **API حقيقي على الإنترنت**، فيه عالم تاني من المشاكل: الـ key غلط، و rate limit، و السيرفر overloaded، و الفلوس خلصت، و الـ connection وقعت في النص. الـ 3 مصادر دول بيقولولك **إيه اللي ممكن يحصل وإزاي تتعامل معاه**، وده أساس Task 6 (الـ retries) وجزء من `AnthropicProvider` (Task 2).

> ⏳ **عمر المصدر:** أرقام الـ rate limits والـ tiers والـ spend caps بتتغيّر. وأسماء الموديلات في الجداول snapshot. **أنواع الـ errors والـ headers** هي اللي بتعيش.

---

# الجزء الأول: README الـ SDK
> 📍 `04-anthropic-sdk-python-readme.md` (ملف قصير)

**الفكرة:** الـ README بقى قصير جداً، وبيحوّلك على الـ docs الكاملة (`platform.claude.com/docs/en/api/sdks/python`). اللي فيه:
- **التسطيب:** `pip install anthropic`.
- لو جاي من نسخة **`0.x`** في **migration guide لـ v1**. يعني الـ SDK الحالي **v1**، وأي مثال قديم على الإنترنت ممكن يكون على 0.x (زي `client.beta.prompt_caching` في الشرح 03).
- **Getting started:** `Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))` (والـ comment بيقول إن ده الـ default وتقدر تشيله)، وبعدين `client.messages.create(max_tokens=1024, messages=[...], model="claude-opus-5-5")`.
- **Python 3.10+**.
- **License: Apache 2.0** (والنسخ القديمة MIT). يعني تقدر تستخدمه تجارياً من غير مشاكل (فاكر موضوع الـ licenses من Step 03؟ ده بيسري على الـ libraries كمان مش الموديلات بس).

**💡 حاجة مهمة الـ README مش بيقولها بس الـ docs التانية بتقولها:** الـ SDK **بيقبل `base_url`** (صفحة Ollama Anthropic compatibility بتستخدم `anthropic.Anthropic(base_url='http://localhost:11434', api_key='ollama')`). ده اللي هيخليك تجرّب كل حاجة على Ollama.

---

# الجزء التاني: Claude API errors

## 1. HTTP errors
> 📍 `04-anthropic-errors.pdf` ص 1–2

**الفكرة:** كل error ليه **HTTP status** و **`type`**:

| Status | `type` | معناه | تعيد المحاولة؟ |
|:---:|---|---|:---:|
| 400 | `invalid_request_error` | مشكلة في شكل أو محتوى الـ request. **وكمان** لما توصل لـ spend limit **إنت** حاطه | ❌ صلّح الـ request |
| 401 | `authentication_error` | مشكلة في الـ API key (غلط، اتلغى، انتهى) | ❌ |
| 402 | `billing_error` | مشكلة في الدفع | ❌ |
| 403 | `permission_error` | الـ key مالوش صلاحية على الـ resource ده | ❌ |
| 404 | `not_found_error` | الـ resource مش موجود (endpoint أو ID غلط) | ❌ |
| 409 | `conflict_error` | تعارض مع حالة الـ resource | ✅ بعد ما تحل التعارض |
| 413 | `request_too_large` | الـ request أكبر من الحد (جزء 3) | ❌ صغّره |
| 429 | `rate_limit_error` | rate limit، **أو** وصلت لـ spend cap بتاع الـ tier | ✅/❌ (جزء 5) |
| 500 | `api_error` | مشكلة داخلية عند Anthropic | ✅ لو `x-should-retry` مش `false` |
| 504 | `timeout_error` | الـ request خد وقت كتير | ✅ (واستخدم streaming للطويل) |
| 529 | `overloaded_error` | الـ API مضغوط من كل اليوزرز | ✅ |

**حالات خاصة تستاهل تفتكرها:**
- **401 برسالة "CORS requests are not allowed..."**: مش مشكلة key. ده لأنك بتكلّم الـ API **من browser** مباشرة، والحل إنك تكلّمه من **الـ backend بتاعك**. (منطقي: الـ key مايتحطش في كود الـ frontend، نفس كلام Step 03 عن Ollama Cloud.)
- **400 بسبب spend limit إنت حاطه** مقابل **429 بسبب spend cap بتاع الـ tier**: نفس الموقف (الفلوس خلصت)، بـ status مختلف حسب مين اللي حاطط الحد.

**⚠️ Errors في الـ streaming (ص 2):** لو الـ stream بدأ بـ **200**، والـ error حصل بعد كده، **مش هيمشي** على النظام ده (الشرح 02، جزء 2.2). و**الـ SDK مش بيعمل retry لـ error في stream.**

**تشبيه من Laravel:** زي ما بتعمل في `Http::...->throw()` وبعدين `catch (RequestException $e)` وتشوف `$e->response->status()`. الفرق إن هنا لازم تفكّر في كل status: **أعيد ولا لأ؟** (في Laravel ده `->retry(3, 100, fn ($e) => ...)`، والـ closure بتقرر).

## 2. Retries
> 📍 ص 3

**الفكرة:** الـ SDK **by default بيعيد المحاولة مرتين** (يعني 3 محاولات). تغيّرها بـ `max_retries` على الـ client، و`0` = مفيش retries.

**الـ SDK بيقرر إزاي؟**
- **يعيد ولا لأ:** لو الرد فيه header **`x-should-retry`** (`true` أو `false`)، بيمشي عليه. لو مفيش، بيعيد في: **connection errors**، و **timeouts**، و الـ statuses **408، و 409، و 429، و 500 وأكبر**.
- **يستنى قد إيه:** لو فيه header **`retry-after`**، بيستنى المدة دي. لو مفيش: **exponential backoff من 0.5 لـ 8 ثواني**.

**ومن غير الـ SDK** (زي `llm_client.py` أو الـ raw httpx في Task 1): "follow `x-should-retry` and `retry-after` in your own code and use backoff and a retry limit". **ده بالظبط Task 6.**

**يعني إيه exponential backoff؟** كل محاولة فاشلة تستنى **ضعف** اللي قبلها: 0.5 ← 1 ← 2 ← 4 ← 8 (وتقف عند حد أقصى). **ليه؟** لو السيرفر مضغوط وكل الـ clients بتعيد فوراً، الضغط بيزيد. الانتظار المتزايد بيدّي السيرفر فرصة يتنفس. (وغالباً بيتضاف **jitter**، عشوائية صغيرة، عشان الـ clients ماتعيدش كلها في نفس اللحظة. ده مش في الصفحة بس معروف.)

**تشبيه من Laravel:** `public $backoff = [1, 5, 10];` في الـ Job، أو `Http::retry(3, fn ($attempt) => $attempt * 100)`.

## 3. Request size limits
> 📍 ص 3

| Endpoint | الحد الأقصى |
|---|---|
| Messages API | 128 MB |
| Token Counting | 128 MB |
| Batch | 256 MB |
| Files | 500 MB |

ولو عدّيته ← **413**، و Cloudflare بيرجّعه **قبل** ما الـ request يوصل لـ Anthropic.

## 4. Error shapes، و Error codes
> 📍 ص 4–5

**الفكرة:** الـ error دايماً JSON بالشكل ده:
```json
{"type": "error",
 "error": {"type": "not_found_error", "message": "..."},
 "request_id": "req_011CSHoEeqs5C35K2UUqR7Fy"}
```
و**أنواع جديدة ممكن تتضاف** (نفس مبدأ الـ stream events).

**Error codes:** بعض الـ errors فيها **`error.details.error_code`** بيحدد **السبب بالظبط**، لأن الـ `type` الواحد ممكن يغطي أسباب كتير. أهم مثال:
- `429 rate_limit_error` عادي ← استنى وأعد.
- `429 rate_limit_error` بـ **`"error_code": "enforced_spend_limit_reached"`** ← **الفلوس بتاعة الشهر خلصت**، و**مش هيرجع لحد أول الشهر**. الإعادة **مالهاش لازمة**.

والنصيحة: لو مفيش code أو code مش معروف، اتعامل بالـ `type` أو الـ status. و**متعملش match على نص الـ `message`** (ممكن يتغيّر).

## 5. SDK error types
> 📍 ص 5–6

**الفكرة:** الـ SDK بيحوّل كل status لـ **exception class**:

| Status | الـ class |
|---|---|
| 400 | `BadRequestError` |
| 401 | `AuthenticationError` |
| 403 | `PermissionDeniedError` |
| 404 | `NotFoundError` |
| 409 | `ConflictError` |
| 413 | `ContentTooLargeError` |
| 422 | `UnprocessableEntityError` |
| 429 | `RateLimitError` (ومنها `EnforcedSpendLimitReachedError`) |
| 504 | `GatewayTimeoutError` |
| 529 | `OverloadedError` |
| أي 5xx | `InternalServerError` |

**والـ classes الأعم:**
- **`APIStatusError`**: أي رد فيه error status (ولـ status مالوش class زي 402، استخدمها وشيك `status_code`). **وكمان error event في stream.**
- **`APITimeoutError`**: الـ SDK زهق من الاستنى (client timeout).
- **`APIConnectionError`**: الـ connection فشل قبل ما ييجي رد (ومنها الـ timeout).
- **`httpx2.TransportError`**: connection وقعت **في نص stream**.
- **`APIError`**: كل اللي فوق، **ما عدا** الـ stream اللي وقع.

**قاعدة Python المهمة:** "A class also catches its subclasses, so put the narrower class first". يعني `RateLimitError` بتمسك `EnforcedSpendLimitReachedError` كمان، فلو عايز تتعامل مع الـ spend cap لوحده، اكتب `except EnforcedSpendLimitReachedError` **قبل** `except RateLimitError`.

**تشبيه من Laravel:** نفس الـ exception hierarchy في PHP: `catch (ModelNotFoundException $e)` قبل `catch (Exception $e)`، وإلا الـ generic هيمسك كل حاجة.

**💡 ربط بكودك:** في Step 03، `LLMError` كان الـ base لكل حاجة، و `UnsupportedParameterError(LLMError)`. الـ `AnthropicProvider` (Task 2) لازم **يترجم** exceptions الـ SDK لـ `LLMError` (أو subclasses منه)، عشان الكود اللي فوق مايعرفش إن فيه SDK أصلاً. ده نفس مبدأ الـ drivers: الـ app بيمسك `LLMError` بس، زي ما Laravel بيرمي `QueryException` سواء MySQL أو PostgreSQL.

## 6. Request ID
> 📍 ص 6–7

**الفكرة:** كل رد فيه header **`request-id`** (`req_...`)، ونفس القيمة في `request_id` في الـ error body. لو هتكلّم الـ support، ابعت الـ ID ده. وفي Python: `message._request_id` على الرد الناجح، و `request_id` على الـ error.

**💡 ممارسة كويسة:** اعمل **log للـ request_id** مع كل error (وحتى مع كل request في production). ده زي الـ **correlation ID** في الـ logs بتاعة Laravel: لما حاجة تبوظ، تقدر تتتبعها.

## 7. Long requests
> 📍 ص 7–8

**الفكرة:** للـ requests الطويلة (خصوصاً **أكتر من 10 دقايق**): استخدم **streaming** أو **Batches**. وماتحطش `max_tokens` كبير من غير streaming، لأن **بعض الشبكات بتقفل الـ connections الساكتة** بعد فترة. والـ SDK:
- **بيرفض** request non-streaming متوقع ياخد أكتر من **10 دقايق**.
- بيظبط **TCP keep-alive**.
- ولو مش محتاج تعرض النص وهو بيتكتب: `with client.messages.stream(...) as stream: message = stream.get_final_message()`.

## 8. Common validation errors
> 📍 ص 8–12

**الفكرة:** الـ 400 errors الشائعة ورسايلها. اللي يهمك دلوقتي:

- **Prefill not supported:** Claude 4.6+ بيرجّع: "This model does not support assistant message prefill. The conversation must end with a user message." (الشرح 01 و 02.)
- **Extended thinking not supported:** Claude 4.7+ بيرفض `thinking: {"type": "enabled"}`، واستخدم `"adaptive"` و `output_config.effort`. والعكس: الموديلات القديمة (4.5 وأقدم) بترفض `adaptive`.
- **Thinking cannot be disabled:** على Fable 5.x و Mythos 5.x و **Opus 5.5**، الـ thinking **دايماً شغّال** و `"disabled"` ← 400. على **Sonnet 5.5** استخدم `{"type": "between_tools"}` كأقل مستوى. و **Haiku 5.5 بيقبل `{"type": "disabled"}`** (بقيود على الـ effort). ولو ما بعتّش `thinking` خالص ← adaptive.
- **Forced tool use not supported:** Fable 5.2، و Opus 5.5، و Sonnet 5.5 وغيرهم بيرفضوا `tool_choice` بـ `any` أو `tool`. (Step 10.)
- وفيه errors تانية متقدمة (thinking block signatures، و computer use versions) هنرجعلها بعدين.

**💡 ليه ده مهم للإيصالات؟** مهمة extraction بسيطة **مش محتاجة thinking**، والـ thinking بياكل tokens (بتدفعها output) ووقت. حسب الصفحة دي: **Haiku 5.5** يقدر يقفل الـ thinking، و **Opus 5.5 لأ**. ده عامل جديد في اختيار الموديل والتكلفة مكانش في Step 03. (ولو استخدمت Opus 5.5 للإيصالات، الـ output tokens الحقيقية هتبقى أكتر من الـ 49.8 بتاعة Qwen بكتير.)

**وكل رسالة 400 "says what caused it"**: اقرا الرسالة قبل ما تدوّر.

---

# الجزء التالت: Rate limits

## 9. نوعين limits
> 📍 `04-anthropic-rate-limits.pdf` ص 1–2

**الفكرة:**
1. **Spend limits:** أقصى **فلوس في الشهر**.
2. **Rate limits:** أقصى **عدد requests/tokens في فترة**.

والاتنين على مستوى **الـ organization** (وتقدر تحط limits أقل لكل workspace).

**About rate limits:**
- الـ limits حسب **usage tier**، وبتطلع tier تلقائي مع الاستخدام. والحسابات الجديدة ممكن تبدأ في **Evaluation tier** (أقل من الأرقام المكتوبة).
- **ممكن يتطبّق على فترات أقصر:** 60 RPM ممكن يبقى **1 request في الثانية**. يعني **burst** من 10 requests في ثانية ممكن ياخد 429 حتى لو إنت تحت الـ 60 في الدقيقة.
- الخوارزمية: **token bucket**. الـ capacity **بتتملي باستمرار** لحد الحد الأقصى، مش بتتصفّر كل دقيقة.

**يعني إيه token bucket؟** تخيّل جردل فيه 60 token، وكل request بياخد واحد، والجردل بيتملي بمعدل token كل ثانية. لو الجردل فاضي ← 429. فتقدر تعمل burst صغير (لو الجردل مليان)، بس مش تعدّي المعدل على المدى الطويل.

**تشبيه من Laravel:** `RateLimiter::for('api', fn () => Limit::perMinute(60))` و `ThrottleRequests` middleware. بس هنا إنت **الـ client** اللي بيتعمله throttle، مش السيرفر.

## 10. Spend limits
> 📍 ص 2–4

| Tier | Monthly spend cap |
|---|---|
| Start | $500 |
| Build | $1,000 |
| Scale | $200,000 |

**لما توصل للـ cap:** الـ API **يقف لحد 00:00 UTC أول الشهر الجاي**، وكل request ← **429** بـ `error_code: "enforced_spend_limit_reached"`، و**من غير `retry-after`**. و**الـ retries (حتى بتاعة الـ SDK) هتفشل**. والحل: tier أعلى.

**Spend limit بتاعك (أقل من الـ cap):** من الـ Console، ولما توصل ← **400** (مش 429) برسالة "You have reached your specified API usage limits".

**💡 نصيحة عملية:** أول ما تعمل key للتجارب، **حط spend limit صغير** (مثلاً $5). لو كودك فيه loop غلط بيبعت requests من غير توقف، الخسارة محدودة. (ده زي `max_execution_time` بس للفلوس.)

## 11. Rate limits: RPM و ITPM و OTPM
> 📍 ص 4–5

**الفكرة:** 3 مقاييس **لكل model class**:
- **RPM:** requests per minute.
- **ITPM:** input tokens per minute.
- **OTPM:** output tokens per minute.

لو عدّيت أي واحد ← 429 بيقولك أنهي واحد، وغالباً فيه `retry-after`.

**Ramp limits:** زيادة **مفاجئة** في الاستخدام ممكن تدّيك 429 **حتى وإنت تحت الـ limits** (جزء 13).

## 12. ⭐ Cache-aware ITPM
> 📍 ص 5–6

**الفكرة:** الـ ITPM بيعدّ **الـ input اللي مش متعمله cache بس**:

| الحقل | بيتحسب في الـ ITPM؟ |
|---|:---:|
| `input_tokens` (بعد آخر breakpoint) | ✓ |
| `cache_creation_input_tokens` | ✓ |
| `cache_read_input_tokens` | **✗** |

**مثال الـ docs:** ITPM = 2,000,000 و cache hit rate 80% ← تقدر تعالج **10,000,000** input token في الدقيقة (2M مش متعملهم cache + 8M من الـ cache). يعني **الـ caching بيزوّد الـ throughput**، مش بيوفّر فلوس بس.

**والـ OTPM:** بيتحسب على الـ tokens **اللي اتولّدت فعلاً**، و**`max_tokens` مالوش دعوة**. "there is no rate limit downside to setting a higher `max_tokens` value".

**ونفس معادلة الشرح 03:** `total_input_tokens = cache_read + cache_creation + input_tokens`.

## 13. جداول الـ tiers، و Ramp limits، و Batches
> 📍 ص 6–10

**الجداول:** كل موديل ليه RPM و ITPM و OTPM. مثال **Start tier**: Haiku 5.5 = **4,000 RPM**، و **2,000,000 ITPM**، و **400,000 OTPM**. وبعض الموديلات بتشارك bucket واحد (Opus 4.x كلها مع بعض مثلاً، والـ footnotes بتوضّح).

**على الحجم بتاعك:** 80 إيصال في اليوم ≈ **request كل 6 دقايق** في المتوسط. يعني إنت **بعيد جداً** عن أي limit. الـ rate limits هتهمك لو عملت batch لكل الإيصالات القديمة مرة واحدة، أو async بـ concurrency عالي (Task 7).

**Ramp limits (ص 8–9):** حد على **سرعة زيادة** استخدامك. حدك = أعلى استخدام ليك في الدقيقة مؤخراً + "step". وبيعلى مع الاستخدام الناجح لحد الـ rate limit، وبينزل لو استخدامك قل. والـ cache reads مش بتتحسب فيه. والـ error: `error_code: "ramp_limit_exceeded"`. **والنصيحة:** استنى `retry-after`، وزوّد ترافيكك **step واحد في الدقيقة**، و**ابدأ الـ bulk jobs بمعدل قليل** ووزّعها، **ماتبعتش كله مرة واحدة**. والـ Batches API **مش عليه** ramp limits.

**💡 ربط بـ Task 7:** لو عملت `asyncio.gather()` على 1,000 إيصال مرة واحدة على حساب جديد، ده بالظبط الـ "sharp increase" اللي بيجيب ramp limit. عشان كده الـ async محتاج **حد للـ concurrency** (workers أو queue).

**Message Batches API:** ليه limits منفصلة: RPM (1,000 في Start)، و **عدد الـ batch requests في الـ queue** (200,000 في Start)، و **100,000 request في الـ batch الواحد**.

**وفيه:** limits لـ Managed Agents، و Files API، و **fast mode** (limits منفصلة).

## 14. Monitoring، و Requesting higher limits، و Workspaces
> 📍 ص 10–12

- **الـ Console** فيه charts للاستخدام والـ rate limits والـ **cache rate**.
- **Request tier increase** من صفحة Rate limits.
- **Workspace limits:** تقدر تحط limit أقل لـ workspace (مثلاً workspace التجارب)، عشان مايستهلكش limit الـ production. وحدود الـ organization دايماً بتتطبّق.

**تشبيه من Laravel:** زي إنك تعمل **queue منفصلة** للـ jobs التقيلة عشان ماتعطّلش الـ emails المهمة.

## 15. Response headers
> 📍 ص 12–13

**الفكرة:** كل رد فيه headers بتقولك وضعك:

| Header | معناه |
|---|---|
| `retry-after` | استنى كام ثانية قبل ما تعيد. **مش كل 429 فيه** (الـ spend cap مفيهوش أبداً) |
| `anthropic-ratelimit-requests-limit` / `-remaining` / `-reset` | الـ requests |
| `anthropic-ratelimit-tokens-limit` / `-remaining` / `-reset` | الـ tokens (الأكثر تقييداً حالياً) |
| `anthropic-ratelimit-input-tokens-*` | الـ input tokens |
| `anthropic-ratelimit-output-tokens-*` | الـ output tokens |

- الـ `remaining` للـ tokens **متقرّب لأقرب ألف**.
- الـ `reset` بصيغة **RFC 3339** (تاريخ ووقت).
- وفيه `anthropic-workspace-id` بيقولك الـ request اتحسب على أنهي workspace.

**💡 استخدام عملي:** تقدر تقرا `remaining` بعد كل request وتبطّأ **قبل** ما تاخد 429 (proactive throttling)، بدل ما تستنى الـ error. وفي الـ SDK الـ headers دي بتتقري بـ `with_raw_response`.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **Retryable مقابل Non-retryable Errors**، و **Exponential Backoff**، و **`retry-after` و `x-should-retry`**، و **Error Code (مقابل Error Type)**، و **Exception Hierarchy (catch narrow first)**، و **Request ID**، و **Spend Limit مقابل Spend Cap**، و **Token Bucket**، و **RPM / ITPM / OTPM**، و **Cache-aware ITPM**، و **Ramp Limits**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. كودك أخد 429. تعيد المحاولة على طول؟</summary>

مش على طول ومش دايماً. أولاً: شيك `error.details.error_code`. لو `enforced_spend_limit_reached`، الفلوس خلصت ومش هترجع لحد أول الشهر، فالإعادة مالهاش لازمة (وده مافيهوش `retry-after`). لو rate limit أو ramp limit عادي: استنى المدة اللي في `retry-after` لو موجود، أو exponential backoff، وأعد عدد محدود من المرات. والـ SDK بيعمل ده لوحده (مرتين by default)، بس مش بيفرّق في الحالة دي، فاعمل except للـ `EnforcedSpendLimitReachedError` قبل `RateLimitError`.
</details>

<details><summary>2. إيه الـ errors اللي ماينفعش تعيد المحاولة فيها أبداً؟ وليه؟</summary>

400 (الـ request نفسه غلط، هيفشل كل مرة)، و 401 (الـ key غلط)، و 402 (الدفع)، و 403 (صلاحيات)، و 404 (مش موجود)، و 413 (كبير). كلها مشاكل في **الـ request أو الحساب**، مش مشاكل مؤقتة. الإعادة بتضيّع وقت (وأحياناً بتعمل ضغط). اللي بيتعاد: connection errors، و timeouts، و 408، و 409، و 429 (غير الـ spend cap)، و 5xx، و 529. والأهم إنك تحترم `x-should-retry` لو موجود.
</details>

<details><summary>3. ليه exponential backoff وليه مش تعيد كل ثانية؟</summary>

لأن الـ 429 والـ 529 معناهم إن السيرفر (أو حسابك) مضغوط. لو كل الـ clients بتعيد كل ثانية، الضغط بيفضل زي ما هو أو بيزيد، ومحدش بيعدّي. الـ exponential (0.5، 1، 2، 4، 8) بيقلل الضغط بسرعة ويدّي فرصة للتعافي. ومع jitter (عشوائية صغيرة) الـ clients ماتعيدش كلها في نفس اللحظة. والـ SDK بيعمل 0.5 لـ 8 ثواني، و `retry-after` لو موجود له الأولوية.
</details>

<details><summary>4. عملت except RateLimitError وتحته except EnforcedSpendLimitReachedError. إيه المشكلة؟</summary>

`EnforcedSpendLimitReachedError` subclass من `RateLimitError`، فأول except هيمسكها، والتاني عمره ما هيتنفّذ. في Python (زي PHP) الـ except بيتشيك بالترتيب، و class بتمسك الـ subclasses بتاعتها. لازم الأضيق الأول.
</details>

<details><summary>5. ليه الـ AnthropicProvider بتاعك المفروض يترجم exceptions الـ SDK لـ LLMError بدل ما يسيبها تطلع؟</summary>

عشان الكود اللي بيستخدم `LLMProvider` (زي `model_eval.py` أو الـ chat CLI) مايعرفش إن فيه SDK أو provider معيّن. لو `OllamaProvider` بيرمي `LLMError` و `AnthropicProvider` بيرمي `anthropic.APIStatusError`، كل caller لازم يمسك الاتنين، والـ abstraction يقع. ده نفس فكرة Laravel: `QueryException` واحد لكل الـ databases. وتقدر تحفظ الـ exception الأصلي (`raise LLMError(...) from e`) والـ request_id عشان الـ debugging.
</details>

<details><summary>6. عندك ITPM limit = 2M، و system prompt طويل متعمله cache. ليه تقدر تعالج أكتر من 2M input token في الدقيقة؟</summary>

لأن الـ ITPM بيعدّ `input_tokens` و `cache_creation_input_tokens` بس، والـ `cache_read_input_tokens` مش بيتحسب. فلو 80% من الـ input جاي من الـ cache، تقدر توصل لـ 10M في الدقيقة. يعني الـ caching مش بس بيوفّر فلوس (0.1x)، كمان بيزوّد الـ throughput من غير ما تطلب limit أعلى.
</details>

<details><summary>7. حساب جديد، و عايز تعالج 5,000 إيصال قديم دلوقتي بـ asyncio.gather. إيه اللي ممكن يحصل؟ وتعمل إيه؟</summary>

الـ burst ده ممكن يجيب 429 من الـ RPM (لأنه ممكن يتطبّق على الثانية)، أو من الـ **ramp limit** (زيادة مفاجئة من صفر)، حتى لو إنت تحت الـ limit الدقيقي. والحساب الجديد ممكن يكون في Evaluation tier بـ limits أقل. الحل: حد للـ concurrency (عدد workers ثابت أو queue)، وتبدأ بمعدل قليل وتزوّد تدريجي، وتحترم `retry-after`. أو أحسن: **Batches API** (خصم 50%، ومفيش ramp limits، والإيصالات القديمة مش مستعجلة).
</details>

<details><summary>8. وصلت لـ spend limit إنت حاطه على الـ workspace. هتاخد 429 زي الـ rate limit؟</summary>

لأ، هتاخد **400** `invalid_request_error` برسالة "You have reached your specified API usage limits". الـ 429 للـ spend cap بتاع الـ tier (حد Anthropic). ده مهم لو كودك بيعمل retry على 429 بس: الـ 400 مش هيتعاد (وده صح)، بس لازم تعرض للمستخدم رسالة مفهومة بدل "bad request".
</details>
