# Step 04 — التاسكات

> **إنت اللي بتكتب الكود.** الملف ده فيه المطلوب بس، من غير حلول.
> لو وقفت: اطلب **تلميح** (مش حل)، وهتاخد تلميحات متدرّجة. ولو عايزني أكتب الكود وإنت تقراه وتشغّله (زي Step 03)، قولّي.
> التاسكات **مبنية على كود Step 03** (`llm_client.py`، و `providers.py`، و `cost.py`، و `model_eval.py`)، مش بتعيده من الأول. والترتيب: **الـ API بإيدك** (Task 1) ← **الـ SDK الرسمي** (Task 2) ← **streaming** (Tasks 3–4) ← **structured outputs** (Task 5) ← **errors** (Task 6) ← **async** (Task 7) ← **الـ usage والتكلفة الحقيقية** (Task 8).

| Task | الـ Concept | مهارة Python | يعتمد على شرح |
|---|---|---|:---:|
| 0 — تجهيز الخطوة بـ uv | uv، و pyproject، و lockfile | `uv init`، و `uv add`، و `uv run` | 06 (1–6) |
| 1 — Messages API بإيدك | شكل الـ request والـ response، و content blocks، و stop_reason | `httpx`، dict building، `next()` على generator | 01 (2، 4)، 02 (1)، 05 (2، 5) |
| 2 — `AnthropicProvider` بالـ SDK | الـ SDK الرسمي، و base_url swapping، و الفروق بين الـ providers | class، mapping، exceptions، tests من غير network | 01 (1، 4)، 02 (1)، 04 (5)، 05 (5) |
| 3 — Streaming بـ 3 طرق، و TTFT | SSE، و NDJSON، و stream events، و TTFT | generators (`yield`)، `iter_lines()`، `time.perf_counter` | 01 (5)، 02 (2)، 05 (3)، 06 (8) |
| 4 — Streaming chat CLI | streaming UX، وتاريخ المحادثة، و stream error recovery | `try/except KeyboardInterrupt`، refactor | 01 (2.5، 5.6)، 02 (2.5) |
| 5 — Structured outputs: 3 طرق | `format` مقابل `output_config.format`، و schema grounding | Pydantic (`Field`، `Literal`، `ValidationError.errors()`) | 02 (3)، 05 (4، 5)، 06 (10–16) |
| 6 — Errors و retries | retryable مقابل لأ، و backoff، و `retry-after` | decorator أو wrapper، injection للـ sleep، tests | 04 (1–5، 15) |
| 7 — Async: الإيصالات بالتوازي | I/O-bound، و bounded concurrency، و Ollama queue | `async`/`await`، `asyncio.Queue`، `gather(return_exceptions=True)` | 07 (كله)، 06 (7–9)، 04 (13) |
| 8 — الـ usage والتكلفة الحقيقية | usage breakdown، و cache writes، و الحد الأدنى للـ caching | refactor لـ `cost.py`، tests بأرقام الـ docs | 03 (3، 7، 9، 12)، 05 (2) |

> 📝 **الملفات اللي مش كود** (`observations.md`، وأي data جديدة): **أنا اللي هكتبها.** ولما تخلّص تجربة، ابعتلي ملف النتايج وأنا أكتب الـ observations.

> 🔑 **Claude API key:** **مفيش تاسك أساسية محتاجاه.** كل حاجة بتشتغل على `qwen2.5:3b` عن طريق **الـ Anthropic-compatible endpoint بتاع Ollama** (`http://127.0.0.1:11434`، و `api_key="ollama"`). وفيه **Bonus B1 و B2** لما يبقى معاك key (قولّي الأول). **نفس الكود** هيشتغل على Claude بتغيير `base_url` و `api_key` بس.
> 📥 **الموديلات:** كل التاسكات بـ `qwen2.5:3b` اللي عندك. **متنزّلش حاجة.**

---

## 🌿 قبل ما تبدأ
بعد ما PR مواد الخطوة يتعمله merge:
```bash
git checkout main
git pull
git checkout -b work/04-llm-apis
```
- `git checkout main`: روح على `main`.
- `git pull`: هات آخر نسخة (فيها مواد الخطوة بعد الـ merge).
- `git checkout -b work/04-llm-apis`: branch جديد لشغلك.

كل الكود في `steps/04-llm-apis/work/`.

---

## Task 0 — تجهيز الخطوة بـ uv
> 📖 بعد شرح 06 (الجزء الأول: uv).

**الهدف:** فولدر شغل جديد **بـ uv** بدل `venv` + `pip freeze`، وتنقل فيه كود Step 03 اللي هتبني عليه.

**المطلوب:**
1. **سطّب uv** لو مش عندك. اتأكد الأول:
   ```bash
   uv --version
   ```
   لو قال "not recognized": سطّبه من [صفحة التسطيب الرسمية](https://docs.astral.sh/uv/getting-started/installation/) (فيها طريقة لـ Windows، أو `pip install uv`). وبعدين افتح terminal جديد وأعد `uv --version`. **لو وقفت هنا قولّي.**
2. **الفولدر والكود** (من PowerShell وإنت في جذر الريبو):
   ```bash
   New-Item -ItemType Directory -Force steps\04-llm-apis\work\experiments\results, steps\04-llm-apis\work\data
   Copy-Item steps\03-models-and-providers\work\llm_client.py, steps\03-models-and-providers\work\model_card.py, steps\03-models-and-providers\work\providers.py, steps\03-models-and-providers\work\test_providers.py, steps\03-models-and-providers\work\cost.py, steps\03-models-and-providers\work\test_cost.py, steps\03-models-and-providers\work\test_model_eval.py steps\04-llm-apis\work\
   Copy-Item steps\03-models-and-providers\work\data\receipts.json, steps\03-models-and-providers\work\data\prices.json steps\04-llm-apis\work\data\
   Copy-Item steps\03-models-and-providers\work\experiments\model_eval.py steps\04-llm-apis\work\experiments\
   cd steps\04-llm-apis\work
   ```
   - السطر الأول بيعمل `work\experiments\results` و `work\data` مرة واحدة (الفاصلة = أكتر من path، و `-Force` = متشتكيش لو موجود).
   - التاني والتالت والرابع بينسخوا الكود والداتا اللي هتبني عليهم (نفس الأماكن النسبية، عشان الـ paths اللي جوه الكود تفضل صح).
   - الأخير بيدخلك الفولدر.
3. **المشروع بـ uv:**
   ```bash
   uv init --bare
   uv add httpx pydantic anthropic
   ```
   - `uv init --bare`: بيعمل `pyproject.toml` **بس** (من غير `src/` ولا `.git` جديد، لأنك جوه ريبو أصلاً). لو الـ option دي مش موجودة في نسختك، شوف `uv init --help` وقولّي.
   - `uv add ...`: بيضيف الـ 3 لـ `pyproject.toml`، ويعمل `uv.lock`، ويعمل `.venv` ويسطّب فيه.
   - **افتح `pyproject.toml`** وبص على `requires-python`: لازم يناسب Python 3.13 اللي عندك.
4. **اتأكد إن كله شغّال:**
   ```bash
   uv run python llm_client.py
   uv run python test_providers.py
   uv run python test_cost.py
   uv run python test_model_eval.py
   ```
   (نفس طريقة Step 03 بالظبط، بس قدامها `uv run` بدل الـ activate.)
5. **PyCharm:** خلّيه يستخدم `work\.venv` كـ interpreter للمشروع ده (Settings ← Python Interpreter ← Add ← Existing).

**✅ شروط القبول:**
- [ ] فيه `work/pyproject.toml` و `work/uv.lock`، و **مفيش** `requirements.txt` جديد.
- [ ] `uv run python llm_client.py` بيرد من `qwen2.5:3b`، والـ tests القديمة passed.
- [ ] `git status` **مش** بيوري `.venv` (موجود في `.gitignore`)، و**بيوري** `pyproject.toml` و `uv.lock`.
- [ ] **سؤال (في الـ PR):** ليه بنعمل commit لـ `uv.lock`؟ وإيه المقابل في Laravel؟

**📚 هيساعدك:** [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/) (الملف اللي رفعته).

---

## Task 1 — Messages API بإيدك (من غير SDK)
> 📖 بعد شرح 01 (جزء 2 و 4)، و 02 (الجزء الأول)، و 05 (جزء 2 و 5).

**الهدف:** قبل ما تستخدم الـ SDK، **تشوف بعينك** الـ HTTP request والـ response بتوع Messages API. نفس اللي عملته مع Ollama في Step 01، ومع OpenAI-compatible في Step 03.

**المطلوب:** `work/messages_raw.py` بيبعت **بـ httpx** لـ **`http://127.0.0.1:11434/v1/messages`** (الـ Anthropic-compatible endpoint بتاع Ollama).

**الـ Interface:**
```python
def build_messages_body(messages: list[dict[str, str]], model: str, max_tokens: int,
                        system: str | None = None,
                        stop_sequences: list[str] | None = None) -> dict: ...

def first_text(content: list[dict]) -> str: ...     # أول block نوعه "text"

def parse_messages_response(data: dict, duration_seconds: float) -> ChatResult: ...

def messages_create_raw(messages: list[dict[str, str]], model: str = "qwen2.5:3b",
                        max_tokens: int = 512, system: str | None = None,
                        base_url: str = "http://127.0.0.1:11434",
                        api_key: str = "ollama") -> ChatResult: ...
```

**✅ شروط القبول:**
- [ ] **ابدأ بإنك تطبع الرد الخام** (`json.dumps(data, indent=2, ensure_ascii=False)`) وتقارنه بمثال الـ docs (شرح 02، جزء 1.1). اكتب في الـ PR: إيه الـ fields اللي موجودة؟ وإيه اللي في الـ docs ومش موجود في رد Ollama (أو العكس)؟
- [ ] الـ headers زي Anthropic: `x-api-key` و `anthropic-version: 2023-06-01` و `content-type`. (Ollama local بيتجاهل الـ key، بس **الكود يبقى صح لـ Claude**.)
- [ ] `max_tokens` **إجباري** في الـ body (مش اختياري زي Ollama native).
- [ ] الـ system prompt في **parameter `system`**، مش رسالة في `messages`. ولو حد بعت `{"role": "system"}` في `messages`، `build_messages_body` ترمي `LLMError` واضح.
- [ ] `first_text` بتدوّر على **أول block نوعه `text`** (مش `content[0]`)، وترمي `LLMError` لو مفيش. (افتكر ليه، شرح 02 جزء 1.3.)
- [ ] `parse_messages_response` **pure** (من غير network)، و `ChatResult` بنفس الشكل بتاع Step 03. الـ `stop_reason` يتنقل زي ما هو (`end_turn`، و `max_tokens`...).
- [ ] `work/test_messages_raw.py` (بنفس شكل `test_providers.py`: functions اسمها `test_...` وتتشغّل بـ `uv run python test_messages_raw.py`): tests على dicts شكلها زي أمثلة الـ docs، ومنهم: رد فيه **thinking block قبل الـ text** (اعمله بإيدك من مثال شرح 02 جزء 2.4)، ورد `stop_reason: "max_tokens"`، و `content` من غير text block.
- [ ] **التجربة:** نفس الرسالة (system + user) مرة لـ `/api/chat` (بـ `llm_client.chat`) ومرة لـ `/v1/messages` (بـ `messages_create_raw`). **سؤال (في الـ PR):** الـ input tokens متطابقة؟ لو لأ، ليه ممكن تختلف رغم إنه نفس الموديل ونفس النص؟
- [ ] **جرّب الـ prefill** (آخر رسالة assistant فيها بداية الرد) على Ollama. اشتغل؟ **سؤال (في الـ PR):** نفس الـ request هيحصل له إيه على Claude Opus 5.5؟ (من غير ما تجرّب، من الـ docs.)

**📚 هيساعدك:** شرح 02 جزء 1، وشرح 05 جزء 2 (جدول المقارنة) وجزء 5، و [`next()` built-in](https://docs.python.org/3/library/functions.html#next).

---

## Task 2 — `AnthropicProvider` بالـ SDK الرسمي (Bonus B2 من Step 03)
> 📖 بعد شرح 01 (جزء 1 و 4)، و 02 (جزء 1.1)، و 04 (جزء 5)، و 05 (جزء 5).

**الهدف:** provider تالت في `providers.py`، **بالـ SDK الرسمي** (`anthropic`)، يشتغل على **Ollama دلوقتي** وعلى **Claude** لما يبقى معاك key، بتغيير الـ environment variables بس. زي ما Laravel بيبدّل `MAIL_MAILER` من `log` لـ `smtp`.

**المطلوب:** في `work/providers.py`:
- **`AnthropicProvider(LLMProvider)`** بيستخدم `anthropic.Anthropic(base_url=..., api_key=...)`.
- **`get_provider()`** بيدعم `LLM_PROVIDER=anthropic`.

**الـ Interface:**
```python
class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, model: str, api_key: str, base_url: str | None = None,
                 default_max_tokens: int = 1024, allow_sampling_params: bool = False): ...

    def chat(self, messages, *, temperature=None, max_tokens=None, seed=None, stop=None) -> ChatResult: ...

def split_system(messages: list[dict[str, str]]) -> tuple[str | None, list[dict[str, str]]]: ...
def parse_anthropic_message(message, duration_seconds: float) -> ChatResult: ...
```

**✅ شروط القبول:**
- [ ] **client واحد** بيتعمل في الـ constructor، مش في كل `chat()`. (شرح 06 جزء 8: ليه؟)
- [ ] `split_system` بتطلّع رسالة الـ `system` (لو موجودة) من الـ list وترجّعها لوحدها، عشان الـ caller يفضل يبعت `messages` بنفس شكل Step 03 (`{"role": "system"}` أول رسالة) لأي provider. **pure** وليها tests.
- [ ] `max_tokens=None` ← يستخدم `default_max_tokens` (لأنه إجباري في Anthropic).
- [ ] `stop` ← `stop_sequences`.
- [ ] **`seed`:** مش موجود في Anthropic API. لو اتبعت ← `UnsupportedParameterError` برسالة واضحة.
- [ ] **`temperature`:** Claude الجديد بيرجّع 400 (شرح 02 جزء 1.1)، و Ollama بيقبله. القرار: لو `allow_sampling_params=False` (الـ default) وحد بعت `temperature` ← `UnsupportedParameterError` **قبل** ما الـ request يتبعت. ولو `True` (للـ Ollama) ← يتبعت. **اكتب في الـ PR ليه اخترنا الـ default ده** (فكّر: أنهي غلطة أسوأ؟ request يترفض من Claude في production، ولا parameter مايتبعتش على Ollama؟).
- [ ] `parse_anthropic_message` بتاخد الـ text من **text blocks بس**، وبتنقل `usage` و `stop_reason`. وتقدر تعمل لها test **من غير network** بـ object شكله زي `Message` (فكّر: `types.SimpleNamespace` أو dataclass صغير).
- [ ] **الـ errors:** exceptions الـ SDK (`anthropic.APIConnectionError`، و `AuthenticationError`، و `NotFoundError`، و `APIStatusError`...) بتتحول لـ `LLMError` برسالة مفهومة (و `raise ... from e`). جرّب: Ollama مقفول، وموديل مش موجود. والرسالة فيها الـ `request_id` لو موجود.
- [ ] **`get_provider()`:** `LLM_PROVIDER=anthropic` بيقرا `LLM_MODEL` و `LLM_API_KEY` و `LLM_BASE_URL` (اختياري: لو مش موجود، الـ SDK بيروح لـ Anthropic الحقيقي). ومن غير key ← error واضح. **مفيش key في الكود.**
- [ ] **الإثبات:** نفس سطر الكود بيرد من الـ 3 providers على `qwen2.5:3b`، بتغيير الـ env بس:
  ```bash
  $env:LLM_PROVIDER="anthropic"; $env:LLM_BASE_URL="http://127.0.0.1:11434"; $env:LLM_API_KEY="ollama"
  ```
  (الأوامر دي بتحط 3 environment variables للـ terminal ده بس، و `;` بتفصل بينهم.)
- [ ] `test_providers.py` فيه tests جديدة للـ `AnthropicProvider` (من غير network): `split_system`، و الـ seed/temperature errors، و `parse_anthropic_message`.
- [ ] **سؤال (في الـ PR):** إيه اللي ماتقدرش تتأكد منه على Ollama وهتحتاج Claude عشان تتأكد منه؟ (لستة.)

**📚 هيساعدك:** README الـ SDK (الملف اللي رفعته)، وشرح 05 جزء 5 (`base_url` و `api_key='ollama'`)، وشرح 04 جزء 5 (exception classes)، و [`types.SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace).

---

## Task 3 — Streaming بـ 3 طرق، وقياس الـ TTFT
> 📖 بعد شرح 01 (جزء 5)، و 02 (الجزء التاني)، و 05 (جزء 3)، و 06 (جزء 8: Streaming responses).

**الهدف:** تشوف الـ streaming **من تحت لفوق**: الـ bytes اللي جاية على الـ connection (NDJSON و SSE)، وبعدين الـ SDK اللي بيخبّي ده. وتقيس الـ **TTFT** اللي الكورس اتكلم عنه، بأرقامك.

**المطلوب:** `work/streaming.py` فيه 3 **generators** (كل واحد بيعمل `yield` لحتت النص وهي جاية):

**الـ Interface:**
```python
@dataclass
class StreamStats:
    ttft_seconds: float          # من قبل الـ request لحد أول حتة نص
    total_seconds: float
    input_tokens: int
    output_tokens: int
    stop_reason: str

def parse_sse_lines(lines: Iterable[str]) -> Iterator[dict]: ...      # pure: سطور SSE -> events (dicts)
def parse_ndjson_lines(lines: Iterable[str]) -> Iterator[dict]: ...   # pure: سطور NDJSON -> chunks

def stream_ollama_native(messages, model="qwen2.5:3b", stats: StreamStats | None = None) -> Iterator[str]: ...
def stream_messages_sse(messages, model="qwen2.5:3b", max_tokens=512, system=None,
                        stats: StreamStats | None = None) -> Iterator[str]: ...
def stream_with_sdk(client, messages, model="qwen2.5:3b", max_tokens=512, system=None,
                    stats: StreamStats | None = None) -> Iterator[str]: ...
```

**✅ شروط القبول:**
- [ ] `stream_ollama_native`: `httpx.stream("POST", ...)` على `/api/chat` بـ `"stream": true`، و `iter_lines()`، والنص من كل chunk، والأرقام من آخر chunk (`done: true`).
- [ ] `stream_messages_sse`: `httpx.stream` على `/v1/messages` بـ `"stream": true`، وبتعمل parse للـ SSE **بإيدك** (`parse_sse_lines`): سطر `data:` ← JSON، وتطلّع النص من `content_block_delta` اللي `delta.type == "text_delta"`. والـ tokens من `message_start` و `message_delta`.
- [ ] **أي event type مش معروف بيتجاهل** (مايوقعش الكود). و event نوعه `error` ← `LLMError`.
- [ ] `stream_with_sdk`: `client.messages.stream(...)` و `text_stream`، والأرقام من `get_final_message()`.
- [ ] الـ `stats` (لو اتبعت) بيتملي بعد ما الـ generator يخلص.
- [ ] `parse_sse_lines` و `parse_ndjson_lines` **pure** وليهم tests في `work/test_streaming.py` على سطور شكلها زي أمثلة الـ docs (شرح 02 جزء 2.4، وشرح 05 جزء 3)، **ومنهم** event نوعه مش معروف، و `ping`، وسطور فاضية.
- [ ] **سؤال (في الـ PR):** في الـ SSE من Ollama، الـ `usage` في `message_start` فيه أرقام حقيقية؟ قارنه بـ `message_delta`. ده بيقولك إيه عن **إنك تعتمد على مكان واحد** للـ tokens؟
- [ ] `work/experiments/ttft.py`: نفس الـ prompt (رد طويل، مثلاً "اكتب 300 كلمة عن...")، و `keep_alive` ثابت والموديل **warm** (اعمل `load_model()` الأول). لكل طريقة من: **non-streaming** (`llm_client.chat`)، والـ 3 streaming، **5 مرات**: الـ TTFT، والوقت الكلي، والـ output tokens. جدول بالمتوسطات، والنتايج في `results/ttft.json`.
- [ ] **سؤال (في الـ PR):** الـ streaming قلّل الـ TTFT قد إيه؟ والوقت الكلي اتغيّر؟ قارن بأرقام الكورس (4.19 ث مقابل 0.49 ث)، وبالـ TTFT من Step 03 Task 3 (0.08 ث warm). ولو فيه فرق بين الـ 3 طرق streaming، ليه ممكن يحصل؟

**📚 هيساعدك:** [HTTPX: Streaming Responses](https://www.python-httpx.org/quickstart/#streaming-responses) (والـ async في الملف اللي رفعته)، و [generators (`yield`)](https://docs.python.org/3/howto/functional.html#generators)، وشرح 02 جزء 2.2 (ترتيب الـ events).

---

## Task 4 — Streaming chat CLI على أي provider
> 📖 بعد شرح 01 (جزء 2.5 و 5.6)، و 02 (جزء 2.5: Error recovery).

**الهدف:** الـ `chat_cli.py` بتاع Step 02 (context size، و sliding window، و summary) يبقى **streaming** ويشتغل على **أي provider** من `get_provider()`. ده تمرين الكورس، بس على الكود بتاعك.

**المطلوب:**
1. انسخ `steps/02-llm-fundamentals/work/chat_cli.py` (واللي محتاجه معاه) لـ `work/`.
2. ضيف لـ `LLMProvider` method جديدة:
   ```python
   def stream(self, messages, *, max_tokens: int | None = None,
              stats: StreamStats | None = None) -> Iterator[str]: ...
   ```
   ونفّذها في `OllamaProvider` و `AnthropicProvider` (استخدم اللي كتبته في Task 3). و `OpenAICompatibleProvider` يرمي `UnsupportedParameterError` (أو نفّذها لو عايز تحدي زيادة).
3. الـ CLI يستخدم `get_provider()` و `provider.stream(...)`.

**✅ شروط القبول:**
- [ ] الرد بيتطبع **وهو بيتكتب** (`end=""` و `flush=True`)، وبعد ما يخلص بيتضاف للتاريخ.
- [ ] نفس الـ CLI شغّال بـ `LLM_PROVIDER=ollama` وبـ `LLM_PROVIDER=anthropic` (على Ollama)، من غير تغيير في كود الـ CLI.
- [ ] الـ system prompt بيتبعت صح للاتنين (افتكر `split_system`).
- [ ] **Ctrl+C في نص الرد** مايقفلش البرنامج: بيوقف الرد ده بس، ويرجع للـ prompt. **قرار تصميم (اكتبه في الـ PR):** الجزء اللي اتكتب يتحفظ في التاريخ ولا لأ؟ وليه؟ (فكّر في اللي الموديل هيشوفه في الـ turn الجاي.)
- [ ] لو الـ provider وقع في النص (اقفل Ollama وإنت بتستنى رد): رسالة واضحة، والـ CLI يفضل شغّال.
- [ ] بعد كل رد: سطر صغير فيه الـ TTFT و الـ tokens (من `stats`).
- [ ] الـ features القديمة (context size، و sliding window، و `/summarize`) لسه شغّالة.

**📚 هيساعدك:** [`KeyboardInterrupt`](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt)، وشرح 02 جزء 2.5 (Error recovery).

---

## Task 5 — Structured outputs: نفس الإيصالات بـ 3 طرق
> 📖 بعد شرح 02 (الجزء التالت)، و 05 (جزء 4 و 5)، و 06 (الجزء التالت: Pydantic).

**الهدف:** الـ extraction اللي عملته في Step 03 Task 6 (`format` في Ollama native) **بطريقتين تانيين**، وتقارن. وتطوّر الـ `Receipt` model وطريقة التعامل مع الأخطاء.

**المطلوب:** `work/experiments/structured_three_ways.py` بيشغّل الـ 15 إيصال (`data/receipts.json`) بـ:
- **A — Ollama native `format`** (اللي عندك في `model_eval.extract`).
- **B — `/v1/messages` بـ `output_config.format`** عن طريق الـ SDK (`client.messages.create(..., output_config={"format": {"type": "json_schema", "schema": ...}})`) على Ollama.
- **C — نفس B بس الـ schema كمان في الـ system prompt** (نصيحة Ollama docs: "ground the model's response").

**الـ Interface:**
```python
class Receipt(BaseModel):         # نسخة مطوّرة من بتاعة Step 03
    model_config = ConfigDict(extra="forbid")
    vendor: str
    date: str = Field(description="...")
    total: float = Field(ge=0, description="...")
    currency: Literal[...]          # الأكواد اللي في الـ eval data

@dataclass
class ExtractionOutcome:
    receipt: Receipt | None
    errors: list[dict] | None       # من ValidationError.errors()
    stop_reason: str
    result: ChatResult

def extract_native(text: str, model: str) -> ExtractionOutcome: ...
def extract_messages(client, text: str, model: str, ground_schema: bool) -> ExtractionOutcome: ...
```

**✅ شروط القبول:**
- [ ] `Receipt` فيه `Field(description=...)` لكل field (الوصف اللي كان في الـ SYSTEM_PROMPT)، و `currency` بـ `Literal`، و `total` بـ `ge=0`. **اطبع `Receipt.model_json_schema()`** وشوف الـ descriptions والـ `enum` والـ `minimum` اتكتبوا فين.
- [ ] **قبل الـ parsing:** شيك `stop_reason`. لو `max_tokens` ← outcome فيه السبب ده (مش validation error عادي).
- [ ] لو الـ validation فشل: `errors` = `e.errors()` (مش `None` وخلاص زي Step 03). واطبع في الآخر **أنهي fields** فشلت وكام مرة.
- [ ] نفس `score()` بتاع `model_eval.py` على الـ 3 طرق (import، مش copy).
- [ ] جدول: لكل طريقة: % JSON صحيح (الـ validation عدّى)، ودقة كل field، والوقت المتوسط، والـ input tokens المتوسطة. والنتايج في `results/structured_three_ways.json`.
- [ ] **سؤال (في الـ PR):** في طريقة B، الـ schema **اتطبّق فعلاً** على Ollama؟ (إزاي تعرف؟ بص على الردود الخام اللي فشلت.) قارن بشرح 05 جزء 5 (الـ docs ذكرت `output_config` بـ `effort` بس).
- [ ] **سؤال (في الـ PR):** طريقة C زوّدت الـ input tokens قد إيه؟ وحسّنت إيه؟ وفي Claude الحقيقي، مين بيضيف الـ schema للـ prompt (شرح 02 جزء 3.7)؟
- [ ] **سؤال (في الـ PR):** الـ `ge=0` بيتطبّق فين: في الـ grammar ولا في Pydantic؟ في Ollama native (A)، وفي Claude بـ `messages.parse()` (شرح 02 جزء 3.3)؟

**📚 هيساعدك:** [Pydantic Fields](https://docs.pydantic.dev/latest/concepts/fields/)، و [`typing.Literal`](https://docs.python.org/3/library/typing.html#typing.Literal)، وشرح 06 جزء 16 (`e.errors()`).

---

## Task 6 — Errors و retries
> 📖 بعد شرح 04 (الجزء التاني: Errors، وجزء 15: headers).

**الهدف:** الـ SDK بيعمل retries لوحده (مرتين، و backoff من 0.5 لـ 8 ث). الـ httpx بتاعك (`llm_client.py` و `messages_raw.py`) **لأ**. هتكتب الـ retry logic بنفسك، بنفس قواعد الـ docs، وبـ tests من غير network ومن غير ما تستنى بجد.

**المطلوب:** `work/retry.py`.

**الـ Interface:**
```python
RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}

class RetryableError(LLMError):
    def __init__(self, message: str, retry_after: float | None = None): ...

def classify_response(status: int, headers: dict[str, str], body: dict | None) -> str: ...
    # "ok" | "retry" | "fail"

def backoff_delay(attempt: int, base: float = 0.5, cap: float = 8.0) -> float: ...

def with_retries(fn: Callable[[], T], max_attempts: int = 3,
                 sleep: Callable[[float], None] = time.sleep) -> T: ...
```

**✅ شروط القبول:**
- [ ] `classify_response` بتمشي على قواعد الـ docs: `x-should-retry` (لو موجود) **ليه الأولوية**، وبعده الـ status (الـ set اللي فوق = retry، و 400/401/403/404/413 = fail).
- [ ] **الـ spend cap:** 429 فيه `error.details.error_code == "enforced_spend_limit_reached"` ← **fail** (مش retry). (شرح 04 جزء 4 و 10.)
- [ ] `backoff_delay` exponential: 0.5، و 1، و 2، و 4، و 8، و 8... (ممكن تضيف jitter، بس الـ tests لازم تفضل deterministic: فكّر إزاي).
- [ ] `with_retries`: لو الـ `RetryableError` فيه `retry_after` ← يستنى المدة دي، وإلا `backoff_delay`. وبعد `max_attempts` ← يرمي آخر error. والـ errors التانية (مش `RetryableError`) ← تطلع على طول.
- [ ] **الـ `sleep` بيتبعت كـ parameter** عشان الـ tests تبعت function وهمية بتسجّل المدد بدل ما تستنى بجد. (ده اسمه **dependency injection**، زي ما بتعمل bind لـ fake في الـ service container في Laravel tests.)
- [ ] `work/test_retry.py`: tests لكل الحالات: نجح من أول مرة، ونجح بعد 2 فشل، وفشل 3 مرات، و `retry_after` اتحترم، و 401 مااتعادش، و spend cap مااتعادش، و `x-should-retry: false` على 500 مااتعادش.
- [ ] `llm_client.chat` و `messages_create_raw` بيستخدموا `with_retries` (الـ connection errors والـ timeouts = retry).
- [ ] **الـ SDK:** في `AnthropicProvider`، `max_retries` بيتظبط من الـ constructor. **سؤال (في الـ PR):** لو عملت retries بتاعتك **فوق** retries الـ SDK (3 × 3)، إيه اللي هيحصل وقت ما Anthropic عندها مشكلة؟
- [ ] **سؤال (في الـ PR):** ليه `with_retries` ماينفعش يتحط حوالين **stream** بالكامل زي ما هو؟ (افتكر: الـ SDK مش بيعمل retry لـ error في stream. ليه؟)

**📚 هيساعدك:** شرح 04 جزء 2 (Retries) و 4 (Error codes)، و [`typing.Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)، و [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar).

---

## Task 7 — Async: الإيصالات بالتوازي
> 📖 بعد شرح 07 (كله)، و 06 (الجزء التاني: HTTPX Async)، و 04 (جزء 13: Ramp limits).

**الهدف:** الـ eval بتاع Step 03 خد ~43 ث للـ 15 إيصال (واحد ورا التاني). هتعمله **async** بـ **concurrency محدود**، وتقيس: الـ async بيسرّع Ollama على جهازك فعلاً؟

**المطلوب:** `work/experiments/async_eval.py`.

**الـ Interface:**
```python
async def extract_async(client, text: str, model: str) -> ExtractionOutcome: ...

async def run_with_queue(receipts: list[dict], workers: int, client, model: str) -> list[dict]: ...
    # producer/consumer بـ asyncio.Queue و N workers، والنتايج بنفس ترتيب الإيصالات

async def main() -> None: ...
```

**✅ شروط القبول:**
- [ ] `AsyncAnthropic(base_url="http://127.0.0.1:11434", api_key="ollama")`، **client واحد** للكل. (أو `httpx.AsyncClient` على `/api/chat` لو عايز الـ native، بس واحد بس.)
- [ ] `run_with_queue` بالـ pattern بتاع شرح 07 جزء 8.2: **producer** بيحط الإيصالات، و **N consumers**، و sentinel (`None`) لكل consumer. **مفيش** `gather` على الـ 15 مرة واحدة.
- [ ] النتايج **بنفس ترتيب** الإيصالات (فكّر: الـ consumer بيعرف رقم الإيصال إزاي؟).
- [ ] إيصال فشل (exception) **مايوقفش** الباقي: بيتسجّل كنتيجة فاشلة. (شرح 07 جزء 9.4.)
- [ ] **التجربة:** `workers` = 1، و 2، و 4، و 8، والموديل warm. لكل واحد: الوقت الكلي، والوقت المتوسط للإيصال، والـ tok/s المتوسط (لو بتستخدم `/api/chat` عندك `eval_duration`، ولو `/v1/messages` احسبه من الوقت). جدول، والنتايج في `results/async_eval.json`.
- [ ] **وإنت بتشغّل `workers=4`:** افتح terminal تاني و `ollama ps`. وشيك الدقة: لازم تفضل زي Step 03 (الإيصالات نفسها والموديل نفسه).
- [ ] **سؤال (في الـ PR):** الوقت الكلي قلّ مع زيادة الـ workers؟ وقد إيه؟ والـ tok/s لكل request حصله إيه؟ **فسّر** بـ: CPU-bound مقابل I/O-bound (شرح 07 جزء 10)، و `OLLAMA_NUM_PARALLEL` (Step 03).
- [ ] **سؤال (في الـ PR):** لو نفس الكود ده بيكلّم Claude Haiku 5.5 بـ 1,000 إيصال، تختار كام worker؟ وإيه اللي هيحددلك الرقم (شرح 04 جزء 11–13)؟ وإمتى الـ Batches API أحسن من الـ async خالص؟

**📚 هيساعدك:** [`asyncio.Queue`](https://docs.python.org/3/library/asyncio-queue.html)، وشرح 07 جزء 8.2 (`queued.py`)، و [AsyncAnthropic في README الـ SDK](https://github.com/anthropics/anthropic-sdk-python).

---

## Task 8 — الـ usage والتكلفة الحقيقية
> 📖 بعد شرح 03 (جزء 3، و 7، و 9، و 12)، و 05 (جزء 2: `prompt_eval_cached_count`).

**الهدف:** `cost.py` من Step 03 بيفترض شكل **OpenAI** للـ usage (الـ cached جزء من الـ input) ومابيحسبش الـ cache writes. هتصلّحه لشكل **Anthropic**، بـ tests من أرقام الـ docs نفسها، وتحسب (من غير key) **هل الإيصالات هيتعملها caching أصلاً**.

**المطلوب:**
1. في `work/cost.py`:
   ```python
   @dataclass
   class Usage:                                  # شكل Anthropic: الـ 3 منفصلين
       input_tokens: int                         # بعد آخر breakpoint
       output_tokens: int
       cache_creation_input_tokens: int = 0
       cache_read_input_tokens: int = 0
       cache_creation_1h_input_tokens: int = 0   # جزء من cache_creation لو فيه 1h

       @property
       def total_input_tokens(self) -> int: ...

   def usage_cost(price: Price, usage: Usage, batch: bool = False) -> float: ...
   def from_ollama(prompt_eval_count: int, prompt_eval_cached_count: int, eval_count: int) -> Usage: ...
   ```
2. `ChatResult` (في `llm_client.py`) يبقى فيه `cached_input_tokens` (بـ default `0` عشان الكود القديم)، و `llm_client.chat` و `AnthropicProvider` يملوه.

**✅ شروط القبول:**
- [ ] `usage_cost`: الـ `input_tokens` بسعر الـ input، والـ `cache_read` بسعر الـ hit، والـ cache creation: الـ 5m بـ `cache_write_5m_per_mtok` والـ 1h بسعر الـ 1h (ضيفه لـ `prices.json` من جدول شرح 03 جزء 3). والـ batch خصم 50% على الكل.
- [ ] `work/test_cost.py` فيه tests بأرقام الـ docs **بالظبط**:
  - مثال شرح 03 جزء 9: `cache_read=100000`، و `creation=0`، و `input=50` ← `total_input_tokens == 100050`.
  - مثال شرح 03 جزء 12 (1h cache): `input=2048`، و `cache_read=1800`، و `creation=248` منهم `1h=100` (والـ 5m = 148). احسب التكلفة المتوقعة بإيدك على Haiku 5.5 واكتبها في الـ test.
  - الـ tests القديمة (مثال الـ $0.50 و $0.348) لسه passed (لو `request_cost` القديمة لسه موجودة، أو اعمل لها بديل واضح).
- [ ] `from_ollama` بيحوّل أرقام Ollama (الـ cached **جزء** من الـ prompt_eval) لشكل Anthropic (المنفصل). وليه test.
- [ ] **التجربة الـ local (`experiments/ollama_cache.py`):** نفس الـ system prompt بتاع الإيصالات + 15 إيصال مختلف، **بالترتيب**، على `/api/chat`. اطبع `prompt_eval_count` و `prompt_eval_cached_count` لكل واحد. **سؤال (في الـ PR):** أول إيصال كام cached؟ والباقي؟ الرقم قريب من طول الـ system prompt؟ وده بيقولك إيه عن الـ caching في Ollama (من غير `cache_control` خالص)؟
- [ ] **الحساب (`experiments/cache_threshold.py`، من غير key):**
  - طول الـ system prompt بـ tokenizer الـ Qwen (من التجربة اللي فوق).
  - هل يعدّي الحد الأدنى لـ Haiku 5.5 (شرح 03 جزء 7)؟ حتى لو Claude بيطلّع tokens **ضعف** Qwen؟
  - **كام few-shot example** (إيصال + الـ JSON بتاعه، خد طولهم من الـ eval) لازم تضيفهم عشان الـ prefix يعدّي الحد بأمان؟
  - التكلفة الشهرية (1,760 إيصال) لـ Haiku 5.5 في 3 حالات: الـ prompt الحالي من غير caching، والـ prompt بالأمثلة من غير caching، والـ prompt بالأمثلة **بالـ caching** (افترض إن الإيصالات بتيجي متفرقة طول اليوم: كل كام دقيقة في المتوسط؟ والـ TTL 5 دقايق: كام request هيبقى write وكام read؟).
- [ ] **سؤال (في الـ PR):** الـ caching يستاهل للإيصالات على الحجم ده؟ وإمتى يبدأ يستاهل؟ (مش الإجابة "أيوه/لأ" بس: بالأرقام.)

**📚 هيساعدك:** شرح 03 جزء 3 (الجدول) و 7 (الحد الأدنى) و 9 (الـ usage) و 12 (مثال الـ 1h)، و `prices.json`.

---

## 🎁 Bonus (اختياري)
> 🔑 **B1 و B2 محتاجين Claude API key. قولّي الأول قبل ما تبدأ**، وحط **spend limit صغير** على الـ workspace (شرح 04 جزء 10). والإيصالات وهمية، فمفيش مشكلة privacy.

- **B1 — الـ tokenizer والـ caching على Claude بجد:**
  - `client.messages.count_tokens(...)` (ببلاش) للـ 15 إيصال + الـ system prompt على **Haiku 5.5** وعلى **Opus 5.5**، وقارن بـ `prompt_eval_count` من Ollama. **ده الرد الحقيقي على السؤال اللي اتأجل من Step 03** (الفرق بين tokenizer الـ Qwen و Claude). جدول بالنسب.
  - الإيصالات على Haiku 5.5 بالـ `AnthropicProvider` و `cache_control` على الـ system: مرة بالـ prompt الحالي (المتوقع: `cache_creation` و `cache_read` = 0)، ومرة بالـ few-shot (فوق الحد). وقارن الـ `usage` الحقيقي بتوقعات Task 8.
- **B2 — Claude structured outputs على الإيصالات:** `client.messages.parse(output_format=Receipt)` على Haiku 5.5 (وجرّب `thinking: {"type": "disabled"}`، شرح 04 جزء 8)، وشغّل `score()` على الـ 15. قارن بـ `qwen2.5:3b`: الدقة، والوقت (مع ملاحظة الـ grammar compilation في أول request)، والتكلفة الحقيقية بـ `usage_cost`. ⚠️ **افتكر:** `temperature` مش هيتبعت (Task 2).
- **B3 — Pre-warming (من غير key، تمرين فهم):** في `cache_threshold.py`، احسب: لو عملت pre-warm بـ `max_tokens: 0` كل 5 دقايق طول ساعات الشغل (8 ساعات)، ده هيكلّف كام في الشهر على Haiku 5.5؟ ويستاهل مقابل الـ TTFT اللي هيوفّره؟ (الإيصالات background job: الـ TTFT مهم أصلاً؟)

---

## 📤 التسليم
1. `git add` و `git commit` بعد كل تاسك (مثال: `work 04: task 1 messages api with httpx`).
2. `git push -u origin work/04-llm-apis`
3. افتح PR على `main`، واكتب فيه إجابات الأسئلة اللي مكتوب جنبها "(في الـ PR)"، واللي مش متأكد منه.
4. هراجع شغلك في الشات، ملف ملف، وإنت تصلّح وتعمل push لحد ما يبقى جاهز.
