# شرح: أدوات Python — HTTPX (Async)، و Pydantic (Models)، و uv (Projects)

> **المصدر:** 3 صفحات docs، النسخة اللي اتحفظت يوم **2026-11-28**
> **الملفات:**
> - `resources/articles/04-httpx-async.pdf` ← [HTTPX: Async Support](https://www.python-httpx.org/async/) (5 صفحات)
> - `resources/articles/04-pydantic-models.pdf` ← [Pydantic: Models](https://pydantic.dev/docs/validation/latest/concepts/models/) (43 صفحة)
> - `resources/articles/04-uv-projects.pdf` ← [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/) (7 صفحات)
>
> **إزاي تقرا:** مش لازم بالترتيب. **uv** قبل Task 0، و **Pydantic** قبل Task 5، و **HTTPX Async** مع الشرح [07](07-realpython-asyncio.md) قبل Task 7.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

دي مش مصادر AI، دي **الأدوات اللي كل كود AI Engineering في Python مبني عليها**:
- **httpx**: إنت بتستخدمه من Step 01 (sync). الجديد: الـ **async** عشان تبعت requests كتير في نفس الوقت، والـ **streaming** للردود.
- **Pydantic**: بتستخدمه من Step 02 للـ structured outputs. والـ SDK بتاع Anthropic نفسه مبني عليه (الـ `Message` object = Pydantic model) وبيستخدمه في `messages.parse()`.
- **uv**: بديل أسرع وأحدث لـ `pip` + `venv` + `requirements.txt`.

---

# الجزء الأول: uv — Working on projects

> 📌 **ابدأ بده** لأنه أول حاجة في Task 0.

**قبل الصفحة: إيه uv أصلاً؟** أداة بتدير **مشروع Python كامل**: نسخة Python، و الـ virtual environment، و الـ dependencies، و الـ lockfile. لحد دلوقتي كنت بتعمل كل ده بإيدك: `python -m venv .venv` ← `activate` ← `pip install` ← `pip freeze > requirements.txt` (واكتشفت في Step 03 إن PowerShell بيكتبه UTF-16!).

**تشبيه من Laravel (أهم تشبيه هنا):**

| uv | Composer |
|---|---|
| `pyproject.toml` | `composer.json` |
| `uv.lock` | `composer.lock` |
| `uv add httpx` | `composer require guzzlehttp/guzzle` |
| `uv remove httpx` | `composer remove ...` |
| `uv sync` | `composer install` |
| `uv lock --upgrade-package httpx` | `composer update guzzlehttp/guzzle` |
| `.venv/` | `vendor/` |
| `uv run script.py` | `php artisan ...` (بيشتغل بالـ dependencies الصح) |

⚠️ **التشبيه مضلل في نقطة:** في PHP الـ `vendor/` جنب الكود و PHP واحد على الجهاز. في Python الـ `.venv` فيه **نسخة Python كمان** (أو link ليها)، و uv ممكن ينزّل نسخة Python بنفسه حسب `.python-version`.

## 1. Creating a new project
> 📍 `04-uv-projects.pdf` ص 1

**الفكرة:** `uv init hello-world` بيعمل فولدر جديد، أو `uv init` جوه فولدر موجود. وبيعمل:
- `.git/` و `.gitignore`
- `.python-version`
- `pyproject.toml`
- `README.md`
- `src/hello_world/__init__.py`

وتشغّله بـ `uv run hello-world` ("Hello from hello-world!").

> 💡 **ليك:** فولدر `work/` جوه ريبو موجود، فـ `uv init` هيحاول يعمل `.git` جديد. في Task 0 هنستخدم options تمنع ده وتعمل مشروع بسيط من غير `src/`. (الـ options دي مش في الصفحة، فهشرحها في التاسك مع `uv init --help`.)

## 2. Project structure
> 📍 ص 1–3

**الفكرة:** أول مرة تشغّل **`uv run`** أو **`uv sync`** أو **`uv lock`**، uv بيعمل كمان:
- **`.venv/`**: الـ virtual environment (معزول عن باقي الجهاز، وفيه الـ dependencies).
- **`uv.lock`**: الـ lockfile.

### `pyproject.toml` (ص 2)
```toml
[project]
name = "hello-world"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = []

[project.scripts]
hello-world = "hello_world:main"
```
ده الـ metadata بتاع المشروع: الاسم، والنسخة، ونسخة Python المطلوبة، و**الـ dependencies**. تقدر تعدّله بإيدك أو بـ `uv add`/`uv remove`. وفيه `[tool.uv]` لإعدادات uv.

> ⚠️ **`requires-python = ">=3.14"` في المثال:** إنت على **3.13**. لو `uv init` كتب نسخة أعلى من اللي عندك، uv هيحاول ينزّل Python جديد. اتأكد إن الرقم مناسب (Task 0).

### `.python-version`
نسخة Python الـ default للمشروع. uv بيستخدمها وهو بيعمل الـ `.venv`.

### `.venv`
"isolated from the rest of your system". الـ dependencies بتتسطّب هنا. (زي ما كنت بتعمل، بس uv بيعمله لوحده.)

### `uv.lock` (ص 3)
**الفرق بينه وبين `pyproject.toml`:** الـ `pyproject.toml` فيه **المتطلبات العامة** (`httpx>=0.28`)، والـ **lockfile** فيه **النسخ بالظبط** اللي اتسطّبت (ومعاها dependencies الـ dependencies). و:
- **cross-platform** (نفس الملف لـ Windows و Linux و Mac، عكس `pip freeze`).
- **"should be checked into version control"**: يتعمله commit، عشان الجهازين بتوعك (الـ desktop ولاب الشغل) يبقى عليهم نفس النسخ بالظبط.
- **ماتعدّلهوش بإيدك**، uv بيديره.

**تشبيه من Laravel:** ده بالظبط سبب إنك بتعمل commit لـ `composer.lock`: `composer install` على أي جهاز يجيب نفس النسخ.

## 3. Managing dependencies
> 📍 ص 3–4

- **`uv add requests`**: بيضيفه لـ `pyproject.toml`، و**يحدّث الـ lockfile والـ `.venv`** في خطوة واحدة.
- **بنسخة معيّنة:** `uv add 'requests==2.31.0'`. **من git:** `uv add git+https://...`.
- **⭐ من `requirements.txt`:** `uv add -r requirements.txt`. ده اللي هيخليك تنقل dependencies Step 03 في سطر.
- **شيل:** `uv remove requests`.
- **حدّث package واحدة:** `uv lock --upgrade-package requests` (والباقي يفضل زي ما هو).

## 4. Viewing your version
> 📍 ص 4–5

`uv version` بيقرا نسخة **مشروعك** (من `pyproject.toml`)، و `--short` للرقم بس، و `--output-format json`. (مش مهم ليك دلوقتي.)

## 5. Running commands
> 📍 ص 5–6

**الفكرة:** **`uv run`** بيشغّل أي script أو command **جوه بيئة المشروع**. و**قبل كل `uv run`** بيتأكد إن الـ lockfile متطابق مع `pyproject.toml`، والـ `.venv` متطابق مع الـ lockfile. يعني **مش محتاج تعمل activate، ومش ممكن تنسى تسطّب حاجة**.

```
uv add flask
uv run -- flask run -p 3000
uv run example.py
```

**ملحوظة:** `uv run` **مش بيشيل** packages زيادة (مش في الـ lockfile) من الـ `.venv` by default.

**البديل (لو عايز الطريقة القديمة):** `uv sync` وبعدين activate:
```
PS> uv sync
PS> .venv\Scripts\activate
PS> python example.py
```
(والصفحة بتوري الشكل بتاع Windows PowerShell بالظبط.)

**💡 ليك:** في Step 03 كنت بتشغّل `python -m experiments.x` (عشان الـ imports). مع uv: **`uv run python -m experiments.x`**.

## 6. Building distributions
> 📍 ص 6

`uv build` بيعمل **wheel** و **source distribution** في `dist/` (لو هتنشر package). مش محتاجه دلوقتي.

---

# الجزء التاني: HTTPX — Async Support

> 📌 اقراه مع الشرح [07](07-realpython-asyncio.md) (asyncio)، لأن الصفحة بتفترض إنك عارف `async`/`await`.

## 7. المقدمة، و Making Async requests
> 📍 `04-httpx-async.pdf` ص 1

**الفكرة:** httpx فيه API **sync** (اللي بتستخدمه)، و API **async** اختياري. والـ async "far more efficient than multi-threading"، ومفيد لو بتشتغل في **async web framework** (زي FastAPI) أو connections طويلة.

```python
async with httpx.AsyncClient() as client:
    r = await client.get('https://www.example.com/')
```

**Tip:** تقدر تجرّب `await` على طول في **`python -m asyncio`** (الـ asyncio REPL، الشرح 07).

## 8. API Differences
> 📍 ص 1–3

**Making requests:** كل الـ methods بقت **async**، يعني `response = await client.get(...)`: `get`، و `post`، و `put`، و `patch`، و `delete`، و `request`، و `send`...

**Opening and closing clients:**
- `async with httpx.AsyncClient() as client:` (context manager)، **أو**
- `client = httpx.AsyncClient()` وبعدين `await client.aclose()`.

**⚠️ تحذير مهم (ص 2):** "make sure you're not instantiating multiple client instances - for example by using `async with` inside a 'hot loop'". يعني **ماتعملش client جديد لكل request**. اعمل **client واحد** وابعته لكل حتة محتاجاه (أو global). **ليه؟** الـ client عنده **connection pool**: بيفتح TCP connection (و TLS handshake مع HTTPS) ويعيد استخدامها. client جديد كل مرة = handshake كل مرة = بطء.

**💡 ربط بكودك:** `send_request()` في `llm_client.py` بيستخدم `httpx.post(...)` مباشرة، وده بيعمل client مؤقت **لكل request**. على Ollama local الفرق صغير (مفيش TLS والشبكة local)، بس على Anthropic (HTTPS عبر الإنترنت) الفرق يبان. والـ SDK بتاع Anthropic بيحل ده لوحده (الـ client بتاعه فيه pool، وعشان كده **اعمله مرة واحدة**).

**تشبيه من Laravel:** زي إنك تعمل `new \GuzzleHttp\Client()` جوه loop بدل ما تعمله مرة واحدة في الـ service container كـ singleton.

### Streaming responses (ص 2–3) ⭐
**الفكرة:** `AsyncClient.stream(method, url, ...)` = **async context block**:
```python
async with client.stream('GET', url) as response:
    async for chunk in response.aiter_bytes():
        ...
```
**الـ methods:**
- `aread()`: تقرا الـ body جوه الـ stream block (لو قررت تقراه كله).
- `aiter_bytes()`: bytes.
- `aiter_text()`: text.
- **`aiter_lines()`**: **سطر سطر** ⭐ (ده اللي محتاجه للـ NDJSON والـ SSE).
- `aiter_raw()`: bytes خام من غير decoding.
- `aclose()`: تقفل الـ response (والـ `with` بيعمله لوحده).

**والنسخة الـ sync** (اللي هتستخدمها في Task 3 الأول): نفس الفكرة من غير async: `with httpx.stream("POST", url, json=body) as response:` و `for line in response.iter_lines():`. (الأسماء من غير `a`: `iter_lines`، و `iter_text`، و `read`.)

**"Manual mode":** `client.send(request, stream=True)` لو الـ context block مش مناسب، و**إنت مسؤول** تعمل `aclose()`، وإلا "resource leaks" (connections مفتوحة). ومثال Starlette بيعمل forward لـ stream لـ endpoint تاني. (ده لو هتبني API بيعمل proxy للـ LLM stream، زي Step 15.)

**تشبيه من Laravel:** `Http::withOptions(['stream' => true])->get(...)` وبعدين `$response->toPsrResponse()->getBody()->read(1024)` في loop. وهنا أسهل بكتير.

**Streaming requests:** لو بتبعت body كبير بالتدريج، تستخدم async generator. (مش محتاجه.)

**Explicit transport instances:** `httpx.AsyncHTTPTransport(retries=1)`. ⚠️ الـ `retries` هنا للـ **connection failures بس** (مش لـ 429 أو 5xx)، فمش بديل لـ Task 6.

## 9. Supported async environments
> 📍 ص 4–5

**الفكرة:** httpx بيشتغل مع **asyncio** (المدمج في Python) أو **trio** (بديل)، وبيعرف لوحده. وفيه **AnyIO** فوق الاتنين. المثال الأساسي:
```python
async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(response)

asyncio.run(main())
```
**إنت هتستخدم asyncio** (المدمج، والـ SDK بتاع Anthropic بيستخدمه). و `anyio` موجود أصلاً في الـ venv بتاعك (dependency لـ httpx، بص على `requirements.txt` بتاع Step 03).

**Calling into Python Web Apps:** `ASGITransport` تكلّم app (FastAPI) من غير شبكة. (للـ tests، Step 15.)

---

# الجزء التالت: Pydantic — Models

> 📌 صفحة طويلة (43 صفحة). **اقرا الأجزاء 10–17 بتركيز**، و 18–19 بسرعة (للمعرفة).

## 10. المقدمة، و "Validation — a deliberate misnomer"
> 📍 `04-pydantic-models.pdf` ص 1–3

**الفكرة:** الـ model = class بيورث من **`BaseModel`** وفيه **fields** كـ type annotations. زي الـ **structs** أو "the requirements of a single endpoint in an API". وشبه الـ `dataclasses` (اللي استخدمتها في `ChatResult`)، بس مصمم للـ **validation** والـ **serialization** والـ **JSON schema**.

**الضمان الأساسي:** "Untrusted data can be passed to a model and, after parsing and validation, Pydantic guarantees that the fields of the resultant model instance will conform to the field types". يعني **داتا مش موثوقة تدخل، وداتا بالأنواع الصح تطلع، أو error**. وده بالظبط اللي محتاجه مع رد LLM.

**"Validation" اسم مش دقيق:** Pydantic بيضمن **شكل الـ output** مش الـ input. يعني ممكن **يحوّل** الداتا (`"123"` ← `123`)، مش بس يتشيك. والـ `ValidationError` معناه "مقدرتش أعمل instance صحيح من الداتا دي".

**تشبيه من Laravel:** **Form Request** (`rules()`) + **casts** في الـ Model + **API Resource** (للـ serialization) في حاجة واحدة. الفرق إن Pydantic بيعرف الـ rules **من الـ type hints** نفسها.

## 11. Basic model usage
> 📍 ص 3–4

```python
class User(BaseModel):
    id: int                 # required (مالوش default)
    name: str = 'Jane Doe'  # optional (ليه default)

user = User(id='123')       # '123' اتحول لـ 123
user.model_dump()           # {'id': 123, 'name': 'Jane Doe'}
```
- **Initialization = parsing + validation.** لو مفيش `ValidationError`، الـ instance صحيح.
- **`model_dump()`**: dict (والـ nested models بتتحول dicts كمان، عكس `dict(user)`).
- الـ models **mutable** by default (`user.id = 321` شغّال).
- وفيه `Field()` لتخصيص الـ fields (قيود، و description، و alias).

**⚠️ Caution:** ماتسميش field بنفس اسم type: `int: Optional[int] = None` هيبقى error غريب.

## 12. Model methods and properties
> 📍 ص 4–5

أهم الـ methods (هتستخدمها):

| Method | بيعمل إيه | استخدمته فين |
|---|---|---|
| `model_validate(obj)` | validate لـ **dict** | |
| **`model_validate_json(s)`** | validate لـ **JSON string** مباشرة | `extract()` في Step 03 |
| `model_construct()` | instance **من غير validation** (⚠️ لداتا موثوقة بس) | |
| `model_dump()` | dict | |
| `model_dump_json()` | JSON string | |
| `model_copy()` | نسخة (مع `update=`) | |
| **`model_json_schema()`** | **JSON Schema** للـ model | `format=Receipt.model_json_schema()` |
| `model_fields` | الـ fields وتعريفاتها | |

## 13. Data conversion، و Extra data
> 📍 ص 5–7

**Data conversion:** Pydantic **بيحوّل** الداتا للنوع المطلوب، وممكن **يضيّع معلومات**:
```python
Model(a=3.000, b='2.72', c=b'binary data').model_dump()
# {'a': 3, 'b': 2.72, 'c': 'binary data'}
```
ده مقصود، وفيه **strict mode** لو مش عايز تحويل.

**💡 ربط بالإيصالات:** في Step 03 لاحظت إن الـ total اتصلّح حتى من `"2l5.75"`. ده **مش** Pydantic (Pydantic كان هيرمي error لـ `"2l5.75"`)، ده الـ **schema في `format`** خلّى الموديل يطلّع رقم. بس لو الموديل طلّع `"215.75"` كـ string، Pydantic كان هيحوّله لـ float بهدوء. فيه **طبقتين**: الـ grammar (الموديل) والـ conversion (Pydantic).

**Extra data:** by default الـ keys الزيادة **بتتجاهل** (`Model(x=1, y='a')` ← `{'x': 1}`). وتقدر تغيّر بـ `model_config = ConfigDict(extra=...)`:
- `'ignore'` (الـ default)
- **`'forbid'`**: error لو فيه key زيادة.
- `'allow'`: بيتحفظ في `__pydantic_extra__`.

**💡 للـ LLM output:** `extra='forbid'` بيكشف لو الموديل زوّد fields من دماغه. بس خلي بالك: Claude structured outputs أصلاً بيضيف `additionalProperties: false`.

## 14. Nested models
> 📍 ص 7–8

```python
class Foo(BaseModel):
    count: int
    size: float | None = None

class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]

Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
```
الـ dicts جوه بتتحول models لوحدها. وده اللي محتاجه لو عايز إيصال فيه **line items** (`items: list[LineItem]`، زي مثال `Invoice` في الشرح 02).

**Cyclic references، و Rebuilding model schema (ص 8–10):** models بتشاور على بعض أو على نفسها، و `model_rebuild()` لو الـ type اتعرّف بعدين. (متقدم، ومش هتحتاجه، و Claude structured outputs **مش بيدعم recursive schemas** أصلاً.)

## 15. ⭐ Validating data
> 📍 ص 10–12

**3 modes:**
- **Python mode:** الـ constructor (`User(...)`، keyword args) و **`model_validate()`** (dict).
- **JSON mode:** **`model_validate_json()`**: JSON string أو bytes. "generally considered faster" من إنك تعمل `json.loads` الأول وبعدين `model_validate`.
- **Strings mode:** `model_validate_strings()`: dict فيه strings بس، ويتحوّل بقواعد JSON.

والـ `model_validate_*()` بتسمحلك تتحكم في الـ strictness والـ extra وغيره **في الـ call نفسه**.

**مثال (ص 11–12):**
```python
User.model_validate({'id': 123, 'name': 'James'})       # ✅
User.model_validate_json('{"id": 123, "name": 123}')   # ❌ name: Input should be a valid string
```
لاحظ: في **JSON mode** الرقم `123` **مش** بيتحوّل لـ string. ده مثال على إن الـ modes ليها سلوك مختلف.

**💡 ليه `model_validate_json` للـ LLM:** رد الموديل **نص**، فبتعمله validate مباشرة. ولو الـ JSON نفسه بايظ (ناقص `}` لأن `max_tokens` قطعه)، هتاخد `ValidationError` (مش `json.JSONDecodeError`)، وده بيبسّط الـ error handling.

**Creating models without validation (ص 12–13):** `model_construct()`، **من غير أي validation**، لداتا **اتعملها validate قبل كده** أو موثوقة. **ماتستخدمهوش مع رد LLM أبداً.**

**Defining a custom `__init__()` (ص 13):** "not recommended". لو عايز تعمل حاجة بعد الـ init، استخدم **validators** أو **`model_post_init()`**.

## 16. ⭐ Error handling
> 📍 ص 14

**الفكرة:** `ValidationError` **واحد** حتى لو فيه أخطاء كتير، وفيه **كل الأخطاء ومكانها**:
```python
data = {'list_of_ints': ['1', 2, 'bad'], 'a_float': 'not a float'}
# 2 validation errors for Model
# list_of_ints.2  Input should be a valid integer ...
# a_float         Input should be a valid number ...
```
لاحظ الـ **location**: `list_of_ints.2` = العنصر رقم 2 في الـ list. وتقدر تاخدهم كـ list بـ **`e.errors()`** (كل error فيه `loc` و `type` و `msg` و `input`). ده مفيد جداً لو عايز تسجّل **أنهي field بالظبط** الموديل غلط فيه (بدل "None" بس زي `extract()` الحالي).

**تشبيه من Laravel:** `$validator->errors()` فيها كل الأخطاء متقسّمة حسب الـ field (`items.2.price`)، مش أول خطأ بس.

## 17. Arbitrary class instances، و Model copy
> 📍 ص 14–17

**Arbitrary class instances (ORM mode):** `model_validate(obj, from_attributes=True)` بياخد attributes من object عادي (زي SQLAlchemy model). **تشبيه:** API Resource من Eloquent model. (مش محتاجه دلوقتي.)

**Model copy:** `m.model_copy(update={'banana': 0})` نسخة بتعديل (⚠️ الـ update **مش بيتعمله validate**). والـ copy العادي **shallow** (الـ nested objects نفس المرجع)، و `deep=True` نسخة كاملة.

## 18. Generic models، و Dynamic models، و RootModel
> 📍 ص 17–33 (للمعرفة)

- **Generic models:** `class Response(BaseModel, Generic[DataT]): data: DataT`، و `Response[int]`، و `Response[DataModel]`. wrapper واحد لأنواع مختلفة. (زي `ApiResponse<T>` في Java اللي إنت عارفها.)
- **`create_model()`:** model بيتعمل **runtime** من fields بتتحدد ديناميكياً. (⚠️ ممكن ينفّذ كود في الـ annotations لو strings.)
- **`RootModel[list[str]]`:** model **الـ root** بتاعه list أو dict مش object.

## 19. Immutability، و ABCs، و Field ordering، وغيره
> 📍 ص 33–43 (للمعرفة)

- **Frozen:** `ConfigDict(frozen=True)` بيمنع التعديل (بس الـ dict جوه لسه ممكن يتعدّل، "faux immutability").
- **ABCs:** ينفع `class X(BaseModel, abc.ABC)`. (زي `LLMProvider` بتاعك، بس Pydantic.)
- **Field ordering:** الترتيب **محفوظ** في الـ JSON Schema، والـ errors، والـ serialization، والـ validation. **ده مهم:** ترتيب الـ fields في `Receipt` = ترتيبهم في الـ schema اللي بتبعته للموديل = الترتيب اللي الموديل بيكتب بيه (الشرح 02 جزء 3.7: Property ordering).
- **`ClassVar`:** مش field. **Private attributes** (`_name`): مش fields ومش في الـ schema.
- **Structural pattern matching:** `match receipt: case Receipt(currency='EGP'): ...`.
- **Attribute copies:** Pydantic بينسخ الـ inputs وهو بيعمل validate (الـ list الأصلية مش هي نفس اللي جوه الـ model).

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **uv و pyproject.toml و Lockfile**، و **Connection Pooling (client واحد)**، و **Response Streaming (`iter_lines`)**، و **Pydantic Validation Modes**، و **ValidationError.errors()**، و **Extra Data Policy (`forbid`)**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. إيه الفرق بين pyproject.toml و uv.lock؟ وأنهي واحد تعمله commit؟</summary>

`pyproject.toml` فيه المتطلبات العامة (`httpx>=0.28`) والـ metadata، و `uv.lock` فيه النسخ **بالظبط** لكل package ولكل dependency تحتها، وهو cross-platform. **الاتنين** يتعملهم commit، زي `composer.json` و `composer.lock`، عشان أي جهاز يعمل `uv sync` ياخد نفس النسخ. والـ `.venv` **مايتعملهوش** commit (زي `vendor/`).
</details>

<details><summary>2. ليه uv run أحسن من إنك تعمل activate وتشغّل python؟</summary>

لأن `uv run` قبل ما يشغّل بيتأكد إن الـ lockfile متطابق مع `pyproject.toml` والـ `.venv` متطابق مع الـ lockfile، فمستحيل تشغّل بـ dependencies ناقصة أو قديمة، ومش محتاج تفتكر الـ activate (اللي بيختلف من shell لـ shell). الـ activate لسه شغّال لو عايزه (`uv sync` وبعدين `.venv\Scripts\activate`).
</details>

<details><summary>3. ليه ماتعملش httpx.AsyncClient() جديد جوه loop بيبعت 100 request؟</summary>

لأن كل client بيفتح connections جديدة (TCP handshake، و TLS handshake مع HTTPS)، ومش بيستفيد من الـ **connection pool**. client واحد بيعيد استخدام الـ connections، فالـ requests أسرع وأخف على السيرفر. الـ docs بتحذّر صراحةً من `async with` جوه "hot loop". الصح: client واحد تبعته للـ functions أو global. ونفس الكلام للـ SDK بتاع Anthropic: `Anthropic()` مرة واحدة.
</details>

<details><summary>4. إزاي تقرا رد streaming سطر سطر بـ httpx (sync)؟ وليه مش response.json()؟</summary>

`with httpx.stream("POST", url, json=body) as response:` وبعدين `for line in response.iter_lines():`. الـ `.json()` بيستنى الـ body **كله** ويعمله parse كـ JSON واحد، وده عكس فكرة الـ streaming (ومع NDJSON أو SSE أصلاً مش JSON واحد). والـ `with` مهم عشان يقفل الـ connection حتى لو حصل error.
</details>

<details><summary>5. الموديل رجّع '{"vendor": "X", "date": "2026-01-05", "total": "215.75", "currency": "EGP"}'. Receipt.model_validate_json هيقبل الـ total كـ string؟</summary>

في الـ JSON mode، Pydantic (في lax mode العادي) بيقبل string فيها رقم لـ field نوعه `float` ويحوّلها (`"215.75"` ← `215.75`). مش هيقبل `"2l5.75"` (مش رقم). ولو عايز تمنع أي تحويل: strict mode. (والأمثلة في الصفحة بتوضّح إن العكس، رقم لـ field نوعه `str`، **مش** بيتقبل في الـ JSON mode.) والدرس: فيه طبقتين، الـ grammar في الموديل والـ conversion في Pydantic، ولازم تعرف كل واحدة بتعمل إيه.
</details>

<details><summary>6. extract() في Step 03 بترجع None لو الـ validation فشل. إيه اللي بتخسره؟ وتعمل إيه أحسن؟</summary>

بتخسر **ليه** فشل: أنهي field، وإيه القيمة اللي الموديل طلّعها، وهل الـ JSON نفسه اتقطع (max_tokens) ولا نوع غلط. `ValidationError` فيه `e.errors()` (list فيها `loc` و `msg` و `input` لكل غلطة). الأحسن: تحفظ الـ errors في النتايج (أو log)، وتشيك `stop_reason` الأول عشان تفرّق بين "اتقطع" و "شكل غلط". ده بيفيد في الـ error analysis (اللي عملته يدوي في Step 03).
</details>

<details><summary>7. ترتيب الـ fields في Pydantic model ممكن يأثر على جودة رد الموديل؟</summary>

ممكن. Pydantic بيحافظ على الترتيب في الـ JSON Schema، والـ structured outputs بيطلّع الـ properties بترتيب الـ schema (الـ required الأول في Claude). والموديل بيولّد token ورا token، فاللي بيتكتب الأول بيأثر على اللي بعده. مثلاً لو عايز الموديل "يفكّر" في نوع الإيصال قبل ما يستخرج الـ total، الترتيب يفرق. (ده موضوع prompt engineering هنرجعله في Step 05.)
</details>
