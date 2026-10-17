# Step 02 — التاسكات

> **إنت اللي بتكتب الكود.** الملف ده فيه المطلوب بس، من غير حلول.
> لو وقفت: اطلب **تلميح** (مش حل)، وهتاخد تلميحات متدرّجة.
> التاسكات بتمرّنك على حاجتين في نفس الوقت: **concepts الخطوة** و **Python**.
> كل التاسكات على **Ollama local** (مجاني، والداتا مابتطلعش من جهازك)، لأن Ollama لسه بيدّيك تتحكم في الـ sampling بإيدك (أحدث موديلات Claude شالت الـ temperature، شوف شرح Ch.2 جزء 4.2.1).

| Task | الـ Concept | مهارة Python | يعتمد على شرح |
|---|---|---|:---:|
| 0 — تجهيز الخطوة | — | venv، نسخ ملفات | — |
| 1 — Token counter | tokenization + العربي أغلى | functions، `zip`، تنسيق جدول | Ch.2 (1.1)، Karpathy (3) |
| 2 — Sampling options في الـ client | sampling parameters + stop reason | optional parameters، بناء `dict` | Ch.2 (4.2) |
| 3 — تجربة الـ temperature والـ seed | probabilistic + inconsistency | loops، `set`، `json` | Ch.2 (4.2، 4.5)، 3Blue1Brown (2) |
| 4 — الـ stop reasons | stopping condition + output ناقص | exceptions، `json.JSONDecodeError` | Ch.2 (4.2.4)، Anthropic docs (7) |
| 5 — Structured outputs | prompting مقابل post-processing مقابل constrained sampling | `pydantic`، `re` | Ch.2 (4.4) |
| 6 — Self-consistency و "tokens to think" | test time compute + ترتيب الـ output | `collections.Counter` | Ch.2 (4.3)، Karpathy (15، 20) |
| 7 — Chat CLI بيدير الـ context | context window + truncation + sliding window | list slicing، تصميم function | Anthropic docs، Ch.2 (2.1.1) |

> 📝 **الملفات اللي مش كود** (ملفات الداتا اللي التاسكات محتاجاها، و `observations.md`): **أنا اللي هكتبها.** لما توصل لتاسك محتاجة داتا، قولّي وأنا أكتبهالك في `work/data/`. ولما تخلّص تجربة، ابعتلي ملف النتايج (JSON) وأنا أكتب `observations.md` منه، وإنت تراجعه وتعدّل فيه لو حابب.

---

## 🌿 قبل ما تبدأ
بعد ما PR مواد الخطوة يتعمله merge:
```bash
git checkout main
git pull
git checkout -b work/02-llm-fundamentals
```
- `git checkout main`: روح على `main`.
- `git pull`: هات آخر نسخة من GitHub (فيها مواد الخطوة بعد الـ merge).
- `git checkout -b work/02-llm-fundamentals`: اعمل branch جديد لشغلك.

كل الكود بتاعك في `steps/02-llm-fundamentals/work/`.

---

## Task 0 — تجهيز الخطوة
**الهدف:** تجهّز فولدر الشغل، وتبدأ من الـ client اللي كتبته في Step 01 بدل ما تبدأ من الصفر.

**المطلوب:**
1. اعمل الفولدر وانسخ الـ client (من PowerShell أو terminal بتاع PyCharm، وإنت في جذر الريبو):
   ```bash
   New-Item -ItemType Directory -Force steps\02-llm-fundamentals\work
   Copy-Item steps\01-introduction\work\llm_client.py steps\02-llm-fundamentals\work\
   cd steps\02-llm-fundamentals\work
   ```
   - السطر الأول بيعمل فولدر `work` (و `-Force` معناها "متشتكيش لو موجود").
   - السطر التاني بينسخ `llm_client.py` بتاعك من Step 01. (ليه نسخ مش import؟ عشان كل خطوة فولدرها مستقل، وهنعدّل الـ client في Task 2 من غير ما نلمس Step 01.)
   - السطر التالت بيدخلك الفولدر.
2. اعمل venv جديد للخطوة:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install httpx pydantic
   pip freeze > requirements.txt
   ```
   - `python -m venv .venv`: environment معزول للخطوة دي.
   - `.venv\Scripts\activate`: فعّله (هتلاقي `(.venv)` في أول السطر).
   - `pip install httpx pydantic`: `httpx` للـ requests (زي Step 01)، و `pydantic` جديدة هتستخدمها في Task 5 (شبه FormRequest validation بس لـ Python objects).
   - `pip freeze > requirements.txt`: سجّل النسخ (زي `composer.lock`).
3. اتأكد إن الموديل موجود: `ollama list`. لو `qwen2.5:3b` مش موجود: `ollama pull qwen2.5:3b`. ولو جهازك 16GB RAM أو أكتر، نزّل كمان `qwen2.5:7b` (هتحتاجه للمقارنة في Task 6).

**✅ شروط القبول:**
- [ ] `python llm_client.py` جوه فولدر الخطوة الجديد شغّال ويرد.
- [ ] فيه `work/requirements.txt` فيه `httpx` و `pydantic`.

---

## Task 1 — Token counter: العربي بيكلّف قد إيه؟
> 📖 بعد شرح Ch.2 (جزء 1.1 Multilingual) و Karpathy (جزء 3 Tokenization).

**الهدف:** تقيس بنفسك اللي الكتاب قاله: نفس المعنى بالعربي بياخد tokens أكتر من الإنجليزي، يعني أغلى وأبطأ ومساحة أقل في الـ context.

**المطلوب:** `work/token_counter.py` فيه function بترجّع عدد الـ tokens لنص معيّن **حسب الـ tokenizer بتاع الموديل الـ local**، وبعدين تجربة بتقارن جمل بنفس المعنى بـ 3 صيغ.

**الـ Interface:**
```python
def count_tokens(text: str, model: str | None = None) -> int: ...
```

**مثال:**
```python
>>> count_tokens("Hello world")
2
```
(الرقم الحقيقي ممكن يختلف حسب الموديل، ده مثال للشكل بس.)

**✅ شروط القبول:**
- [ ] العدد جاي من **Ollama نفسه**، مش متقدّر بعدد الكلمات أو الحروف.
- [ ] العدد يبقى للنص **نفسه**، مش للنص + الـ chat template. (فكّر: `/api/chat` بيضيف special tokens للأدوار، فاكر Karpathy جزء 11؟ دوّر في docs الـ `/api/generate` على طريقة تبعت النص "خام" من غير template، وعلى option بيخلّي الموديل يولّد أقل حاجة ممكنة عشان متستناش.)
- [ ] قائمة فيها **6 جمل على الأقل**، كل واحدة بـ 3 صيغ: **إنجليزي**، و**فصحى**، و**عامية مصرية**، وبنفس المعنى. (جمل من شغل حقيقي: رسالة لعميل، أو سؤال عن طلب، أو بند في سياسة...)
- [ ] البرنامج بيطبع **جدول**: لكل جملة عدد tokens كل صيغة، ونسبة الفصحى للإنجليزي، والعامية للإنجليزي. وفي الآخر **متوسط النسبة**.
- [ ] الجدول متنسّق ومقروء في الـ terminal (الأعمدة متظبطة).
- [ ] **تجربة:** شغّل نفس الجمل على `qwen2.5:7b` (لو عندك). الأرقام اتغيّرت؟ (نفس العيلة غالباً نفس الـ tokenizer.) وجرّب كمان تحط الجمل في [tiktokenizer](https://tiktokenizer.vercel.app) بـ `o200k_base` وقارن. ابعتلي الأرقام وأنا أكتب الـ observations.

⚠️ **لو لقيت أرقام صغيرة بشكل غريب** لما تعيد نفس النص: ده مش bug في كودك. فكّر في الـ KV cache والـ prefill من شرح Ch.2 (جزء 2.1.1)، واسألني لو محتاج تلميح.

**📚 هيساعدك:**
- [Ollama API docs](https://docs.ollama.com/api): ابحث عن *Generate a completion* وحقوله.
- [Python — Format String Syntax](https://docs.python.org/3/library/string.html#format-specification-mini-language): عشان تظبط عرض الأعمدة (زي `str_pad` في PHP).
- [`zip`](https://docs.python.org/3/library/functions.html#zip)

---

## Task 2 — Sampling options و stop reason في الـ client
> 📖 بعد شرح Ch.2 (جزء 4.2 Sampling Strategies).

**الهدف:** تخلّي الـ client بتاعك يتحكم في الـ sampling (temperature، و top-k، و top-p، و seed، و max tokens، و stop)، ويرجّعلك **سبب وقوف** الرد.

**المطلوب:** عدّل `work/llm_client.py`:

**الـ Interface:**
```python
@dataclass
class ChatResult:
    text: str
    input_tokens: int
    output_tokens: int
    duration_seconds: float
    stop_reason: str            # جديد

def chat(
    messages: list[dict[str, str]],
    model: str | None = None,
    *,
    temperature: float | None = None,
    top_k: int | None = None,
    top_p: float | None = None,
    seed: int | None = None,
    max_tokens: int | None = None,
    stop: list[str] | None = None,
) -> ChatResult: ...
```
(الـ `*` معناها إن كل اللي بعدها لازم يتبعت بالاسم: `chat(msgs, temperature=0)` مش `chat(msgs, None, 0)`. ده بيخلّي النداء أوضح، زي named arguments في PHP 8.)

**✅ شروط القبول:**
- [ ] الـ parameters اللي قيمتها `None` **ماتتبعتش خالص** لـ Ollama (سيب Ollama يستخدم الافتراضي بتاعه). يعني لو ناديت `chat(msgs)` من غير options، الـ request يبقى زي Step 01 بالظبط.
- [ ] الأسماء عندك (`max_tokens`، و `stop`...) بتتحوّل لأسماء Ollama الصح. دوّر في docs على الـ options المتاحة (فيه واحد منهم اسمه مختلف عن `max_tokens`).
- [ ] `stop_reason` جاي من رد Ollama (دوّر على الحقل اللي بيقول الرد خلص ليه).
- [ ] **Validation بسيط قبل الـ request:** temperature سالبة أو top_p برّه 0–1 ترمي `LLMError` برسالة واضحة، مش تستنى Ollama يرفض.
- [ ] الكود القديم (Step 01 style) لسه شغّال من غير تعديل.
- [ ] الـ `__main__` بيجرّب request بـ `temperature=0` و `max_tokens=20`، ويطبع الرد و الـ `stop_reason`. (المفروض تلاقي الرد مقطوع وسبب الوقوف مش "stop". ليه؟)

**📚 هيساعدك:**
- [Ollama — Modelfile parameters](https://docs.ollama.com/modelfile): جدول الـ parameters وقيمها الافتراضية (نفس الأسماء بتتبعت في `options`).
- [Ollama API docs](https://docs.ollama.com/api): حقل `options` في الـ chat request.
- [Python — Keyword-only arguments](https://docs.python.org/3/tutorial/controlflow.html#special-parameters)

---

## Task 3 — تجربة الـ temperature والـ seed
> 📖 بعد شرح Ch.2 (جزء 4.2.1 Temperature، و 4.5.1 Inconsistency) و 3Blue1Brown (جزء 2).

**الهدف:** تشوف بعينك إن الـ temperature بتتحكم في التنوّع، وإن الـ seed بيخلّي الـ "عشوائية" تتكرر، وإن "الموديل deterministic والـ sampling لأ".

**المطلوب:** `work/experiments/temperature.py`.

**✅ شروط القبول:**
- [ ] **3 prompts** من أنواع مختلفة: واحد **ليه إجابة واحدة** (مثلاً "عاصمة اليابان إيه؟ جاوب بكلمة")، وواحد **إبداعي قصير** (مثلاً "اقترح اسم واحد لمحل قهوة في المعادي")، وواحد **تصنيف** (مثلاً تصنّف رسالة عميل: شكوى / استفسار / شكر، والرد كلمة واحدة).
- [ ] كل prompt بيتسأل **5 مرات** على كل temperature من دول: `0`، و `0.7`، و `1.5`.
- [ ] لكل (prompt، temperature): البرنامج بيحسب **عدد الردود المختلفة** من الـ 5 (ركّز: "مختلفة" بعد ما تشيل المسافات الزيادة في الأول والآخر).
- [ ] **جزء الـ seed:** نفس الـ prompt الإبداعي، temperature `1.0`، و `seed=42`، **مرتين**. وبعدين `seed=7` مرتين. الردود بتتطابق؟
- [ ] النتايج بتتحفظ في `work/experiments/results/temperature.json` (كل رد، والـ prompt، والـ temperature، والـ seed لو فيه، والـ tokens)، **بالعربي مقروء** (زي Task 4 في Step 01).
- [ ] البرنامج بيطبع ملخص: جدول (prompt × temperature) فيه عدد الردود المختلفة.
- [ ] ابعتلي الـ JSON، وأنا أكتب `observations.md`: إيه اللي حصل مع كل temperature، وأنهي نوع prompt اتأثر أكتر، والـ seed عمل إيه، وربط كل ده بالشرح.

**📚 هيساعدك:** [`set`](https://docs.python.org/3/tutorial/datastructures.html#sets) (لعدّ المختلف، زي `array_unique` + `count`)، و [`str.strip`](https://docs.python.org/3/library/stdtypes.html#str.strip).

---

## Task 4 — الـ stop reasons: لما الرد يتقطع
> 📖 بعد شرح Ch.2 (جزء 4.2.4 Stopping condition) و Anthropic docs (جزء 7 Overflow).

**الهدف:** تتعوّد على قاعدة "**شيّك على سبب الوقوف قبل ما تستخدم الرد**"، وتشوف إزاي الـ JSON بيبوظ لما الرد يتقطع.

**المطلوب:** `work/experiments/stop_reasons.py`، وفيه function بتعمل parse لـ JSON من رد الموديل بأمان.

**الـ Interface:**
```python
class TruncatedResponseError(LLMError): ...
class InvalidJSONError(LLMError): ...

def parse_json_result(result: ChatResult) -> dict | list: ...
```

**✅ شروط القبول:**
- [ ] `parse_json_result` بترمي `TruncatedResponseError` لو الرد اتقطع (من `stop_reason`)، **قبل** ما تحاول تعمل parse.
- [ ] وبترمي `InvalidJSONError` لو الرد خلص طبيعي بس مش JSON صحيح، ورسالة الـ error فيها **أول 200 حرف** من الرد عشان تقدر تعمل debug.
- [ ] **تجربة 1:** اطلب من الموديل لستة JSON فيها 10 أسماء مدن مصرية، مرة بـ `max_tokens=15` ومرة من غير. اطبع اللي حصل في كل مرة (من غير ما البرنامج يقع: اعمل catch للـ errors بتوعك واطبع رسالتها).
- [ ] **تجربة 2:** اطلب "عدّ من 1 لـ 20، كل رقم في سطر" مع `stop=["7"]`. الموديل وقف فين؟ وإيه الـ `stop_reason`؟ (قارنها بالـ stop reason بتاع تجربة 1.)
- [ ] الـ exceptions الجديدة **بتورث** من `LLMError` (عشان اللي بينادي يقدر يعمل catch لـ `LLMError` بس لو عايز).

**📚 هيساعدك:** [`json.loads` و `JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError)، و [Exception hierarchies](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions).

---

## Task 5 — Structured outputs: 3 طرق ومقارنة
> 📖 بعد شرح Ch.2 (جزء 4.4 Structured Outputs).

**الهدف:** تطبّق 3 من طبقات الـ structured outputs اللي في الكتاب (prompting، و post-processing، و constrained sampling)، وتقيس كل واحدة **بالأرقام**. وتتعلم إن الـ schema بيضمن **الشكل** مش **الصح**.

**الفكرة:** عندك رسايل طلبات من عملاء متجر (بالعامية، ومكتوبة بشكل عشوائي)، وعايز تطلّع منها داتا منظمة. **قولّي لما توصل هنا وأنا أكتبلك `work/data/orders.json`**: حوالي 10 رسايل، ومع كل رسالة الإجابة الصح (عشان تقيس الدقة).

**الـ Interface:**
```python
class OrderItem(BaseModel):
    product: str
    quantity: int

class Order(BaseModel):
    customer_name: str | None
    items: list[OrderItem]
    city: str | None
    is_urgent: bool

def extract_prompt_only(message: str) -> str: ...          # بترجّع النص الخام من الموديل
def extract_with_cleanup(message: str) -> str: ...         # prompt + post-processing
def extract_with_schema(message: str) -> str: ...          # Ollama format + JSON schema
```

**✅ شروط القبول:**
- [ ] **الطريقة 1 (prompting):** الـ prompt بيطلب JSON بالشكل المطلوب، ومن غير أي تنضيف.
- [ ] **الطريقة 2 (post-processing):** نفس الـ prompt، بس بتنضّف الرد قبل ما ترجّعه (مثلاً: تشيل الـ markdown code fence، أو تاخد من أول `{` لآخر `}`). اكتشف الغلطات الشائعة من نتايج الطريقة 1 الأول، وصلّحها.
- [ ] **الطريقة 3 (constrained sampling):** بتبعت لـ Ollama الـ JSON schema في الـ parameter بتاع الـ structured outputs. والـ schema **متولّد من الـ pydantic model** (`Order`)، مش مكتوب بإيدك.
- [ ] لكل رد من كل طريقة، بتعمل **validation بـ pydantic** وبتسجّل: (أ) JSON صحيح؟ (ب) مطابق للـ schema؟ (ج) **الداتا صح** مقارنة بالإجابة اللي في `orders.json`؟
- [ ] كل رسالة × كل طريقة × **3 مرات**، و `temperature` ثابتة (اختار قيمة وقول ليه).
- [ ] البرنامج بيطبع جدول: لكل طريقة نسبة (أ) و (ب) و (ج).
- [ ] النتايج في `work/experiments/results/structured.json`. ابعتهالي وأنا أكتب الـ observations.
- [ ] **سؤال تفكير (اكتب إجابتك في الـ PR):** الطريقة 3 ممكن تطلع 100% في (ب) وأقل في (ج). إزاي؟ وده معناه إيه لتطبيق حقيقي؟

**📚 هيساعدك:**
- [Ollama — Structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [Pydantic — Models](https://docs.pydantic.dev/latest/concepts/models/) (`model_validate_json` و `ValidationError`) و [JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)
- [`re`](https://docs.python.org/3/library/re.html) (لو هتستخدم regex في التنضيف، شبه `preg_match`)

---

## Task 6 — Self-consistency و "Models need tokens to think"
> 📖 بعد شرح Ch.2 (جزء 4.3 Test Time Compute) و Karpathy (جزء 15 و 20).

**الهدف:** تجرّب تكنيكين بيحسّنوا الدقة من غير موديل أكبر: (1) إن الموديل يفكر **قبل** ما يجاوب، و(2) **self-consistency** (تسأل كذا مرة وتاخد الإجابة الأكتر تكراراً). وتقيس **التكلفة** بالـ tokens.

**الفكرة:** مسائل حساب كلامية بالعربي (زي مسألة Emily عند Karpathy) ليها إجابة رقمية واحدة. **قولّي وأنا أكتبلك `work/data/math_problems.json`**: حوالي 10 مسائل متدرّجة الصعوبة مع إجاباتها.

**الـ Interface:**
```python
def solve_direct(problem: str) -> tuple[int | None, ChatResult]: ...          # الإجابة على طول
def solve_with_reasoning(problem: str) -> tuple[int | None, ChatResult]: ...  # يفكر الأول وبعدين الإجابة
def majority_vote(answers: list[int | None]) -> int | None: ...
```

**✅ شروط القبول:**
- [ ] `solve_direct`: structured output (من Task 5) فيه حقل `answer` بس.
- [ ] `solve_with_reasoning`: structured output فيه حقل `reasoning` **قبل** حقل `answer` في الـ schema. (ليه الترتيب مهم؟ ارجع لـ Karpathy جزء 15.)
- [ ] `majority_vote` بترجّع الإجابة الأكتر تكراراً، وبتتجاهل الـ `None` (الردود اللي فشلت). حالة التعادل: قرّر تعمل إيه واكتبه في docstring.
- [ ] التجربة بتقارن **4 إعدادات** على كل المسائل:
  1. direct، مرة واحدة، temperature 0.
  2. with reasoning، مرة واحدة، temperature 0.
  3. direct، 5 مرات، temperature 0.8، و majority vote.
  4. with reasoning، 5 مرات، temperature 0.8، و majority vote.
- [ ] لكل إعداد: **الدقة** (كام مسألة صح من الكل)، و**متوسط الـ output tokens لكل مسألة** (التكلفة).
- [ ] البرنامج بيطبع جدول بالأربع إعدادات.
- [ ] لو عندك `qwen2.5:7b`: شغّل الإعداد 2 عليه كمان وقارن. موديل أكبر بمحاولة واحدة، ولا موديل أصغر بـ 5 محاولات؟
- [ ] النتايج في `work/experiments/results/self_consistency.json`. ابعتهالي وأنا أكتب الـ observations.

**📚 هيساعدك:** [`collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) (بالذات `most_common`).

---

## Task 7 — Chat CLI بيدير الـ context window
> 📖 بعد شرح Anthropic docs (كله) و Ch.2 (جزء 2.1.1، الـ KV cache).

**الهدف:** تشوف بعينك إن الـ context window **محدود**، وإن Ollama بيشيل **أقدم الرسايل بصمت** لما المحادثة تعدّيه، وتكتب استراتيجية إنت اللي بتتحكم فيها بدل ما تسيبها للصدفة.

**المطلوب:** انسخ `chat_cli.py` بتاعك من Step 01 لـ `work/chat_cli.py`، وطوّره.

**الـ Interface (الـ function الأساسية الجديدة):**
```python
def trim_history(
    messages: list[dict[str, str]],
    max_messages: int,
) -> list[dict[str, str]]: ...
```

**✅ شروط القبول:**
- [ ] الـ client بيقبل `context_size: int | None` (أضفه لـ `chat()` في `llm_client.py`) وبيبعته لـ Ollama في الـ option الصح.
- [ ] الـ CLI فيه **system message** ثابت في أول المحادثة (مثلاً: "إنت assistant اسمك نور، وبترد بالعامية المصرية دايماً").
- [ ] بعد كل رد بيطبع `input_tokens` و `context_size` الحالي، وبينبّهك لو `input_tokens` قرّبت من `context_size` (مثلاً عدّت 80%).
- [ ] **تجربة الـ truncation:** شغّل بـ `context_size` صغير (مثلاً 512)، وقول في أول رسالة "اسمي كريم، وبشتغل Laravel developer". كمّل كلام في مواضيع تانية لحد ما `input_tokens` تعدّي الـ context. وبعدين اسأله "اسمي إيه وبشتغل إيه؟"، و"إنت اسمك إيه؟". سجّل اللي حصل. (لاحظ: مفيش error!)
- [ ] `trim_history` بتطبّق **sliding window**: بتحتفظ **دايماً** بالـ system message، وبآخر `max_messages` رسالة بس. ومتقطعش في نص turn (يعني متسيبش رد assistant من غير السؤال بتاعه).
- [ ] أمر `/trim N` في الـ CLI بيشغّل الـ sliding window بحد N.
- [ ] أعد التجربة مع الـ sliding window. الـ system message اتحفظ؟ الاسم اتنسى؟ (أيوه هيتنسي، وده متوقع: الـ sliding window بيضحّي بالقديم عن قصد.)
- [ ] `trim_history` **مبتعدّلش** الـ list الأصلية، بترجّع list جديدة. اختبرها بـ `assert` بسيط في آخر الملف أو في ملف `test_trim.py`.
- [ ] ابعتلي اللي حصل في التجربتين وأنا أكتب الـ observations.

**🌟 Bonus (اختياري):** أمر `/summarize`: بيخلّي الموديل يلخّص الرسايل القديمة في رسالة واحدة، ويحطها بعد الـ system message، ويشيل الرسايل اللي اتلخّصت (دي فكرة الـ **compaction** في Anthropic docs جزء 6، بس بإيدك). جرّب: الاسم اتحفظ المرة دي؟

**📚 هيساعدك:**
- [Ollama — Modelfile parameters](https://docs.ollama.com/modelfile) (دوّر على الـ parameter بتاع حجم الـ context).
- [Python — List slicing](https://docs.python.org/3/tutorial/introduction.html#lists) (زي `array_slice`)، و [`copy`](https://docs.python.org/3/library/copy.html) لو احتجت.

---

## 📤 التسليم
1. اعمل commit بعد كل task لوحده، بـ message واضحة (مثال: `work 02: task 1 token counter`).
2. `git push -u origin work/02-llm-fundamentals`
3. افتح PR على `main`، واكتب فيه عملت إيه، واللي مش متأكد منه، وإجابات أسئلة التفكير.
4. تقدر تفتح الـ PR بعد أول task وتكمّل عليه. هراجع كل push.
