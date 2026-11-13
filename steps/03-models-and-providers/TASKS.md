# Step 03 — التاسكات

> **إنت اللي بتكتب الكود.** الملف ده فيه المطلوب بس، من غير حلول.
> لو وقفت: اطلب **تلميح** (مش حل)، وهتاخد تلميحات متدرّجة. ولو عايزني أكتب الكود وإنت تقراه وتشغّله (زي Step 02)، قولّي.
> التاسكات ماشية بنفس ترتيب **الـ model selection workflow** بتاع الكتاب: **hard attributes** (Task 1) ← **public info** (Task 2) ← **تفهم الـ self-hosting بالأرقام** (Tasks 3–4) ← **standard API** (Task 5) ← **eval بتاعك** (Task 6) ← **التكلفة والقرار** (Task 7).

| Task | الـ Concept | مهارة Python | يعتمد على شرح |
|---|---|---|:---:|
| 0 — تجهيز الخطوة | hardware بتاعك | venv، نسخ ملفات | Ollama (2، 6) |
| 1 — Model card من Ollama | hard attributes: license، و context، و quantization | `dataclass`، nested dicts، `str.endswith` | Ch.4 (5.1، 5.3.1)، Ollama (3، 7) |
| 2 — قارئ الـ leaderboard | public benchmarks، ونفس الموديل عند providers مختلفين | قراية ملف، parsing، `sorted(key=)`، `defaultdict` | Ch.4 (6)، AA (كله) |
| 3 — الوقت بيروح فين؟ | cold start، و keep_alive، و TTFT، و GPU/CPU | `@property`، `time.perf_counter`، JSON | Ollama (4.3، 4.11)، Ch.4 (3) |
| 4 — الـ context بياكل memory | `num_ctx`، والـ KV cache، و offloading | loops، تنسيق جدول | Ollama (4.2، 4.14، 5) |
| 5 — Providers زي drivers Laravel | standard API، و OpenAI compatibility، و Modelfile | `ABC`، factory، env vars، exceptions، tests | Ch.4 (5️⃣)، Ollama (7، 9) |
| 6 — Mini eval: الموديل كفاية؟ | الخطوة 3 في الـ workflow، و usefulness threshold | pydantic، تجميع نتايج، `statistics` | Ch.4 (5.2، 6.3)، Anthropic (2.4) |
| 7 — التكلفة والقرار | cost per task، و API مقابل self-host، و caching، و batch | دوال حسابية، tests بأرقام الـ docs | Ch.4 (3.3، 5️⃣)، Anthropic (3)، AA (1.3) |

> 📝 **الملفات اللي مش كود** (`hardware.md`، و `data/receipts.json`، و `data/prices.json`، و `observations.md`): **أنا اللي هكتبها.** لما توصل لتاسك محتاجة واحد منهم، قولّي. ولما تخلّص تجربة، ابعتلي ملف النتايج وأنا أكتب الـ observations. (استثناء: `model_decision.md` في Task 7 هو التمرين نفسه، بس لو عايزني أكتب مسودة منه من نتايجك، قولّي.)

> 📥 **الموديلات:** كل التاسكات الأساسية بـ `qwen2.5:3b` اللي عندك. Task 6 فيها موديلات **اختيارية** وحجمها مكتوب. **متنزّلش حاجة قبل ما تقولّي.**
> 🔑 **Claude API:** مفيش تاسك أساسية محتاجاه. فيه Bonus واحد (B2) لو عندك key، وقولّي الأول.

---

## 🌿 قبل ما تبدأ
بعد ما PR مواد الخطوة يتعمله merge:
```bash
git checkout main
git pull
git checkout -b work/03-models-and-providers
```
- `git checkout main`: روح على `main`.
- `git pull`: هات آخر نسخة (فيها مواد الخطوة بعد الـ merge).
- `git checkout -b work/03-models-and-providers`: branch جديد لشغلك.

كل الكود في `steps/03-models-and-providers/work/`.

---

## Task 0 — تجهيز الخطوة
**الهدف:** فولدر شغل جديد بالـ client بتاعك من Step 02، وتعرف **جهازك فيه إيه** (لأن ده hard attribute لأي موديل local).

**المطلوب:**
1. الفولدر والـ client (من PowerShell وإنت في جذر الريبو):
   ```bash
   New-Item -ItemType Directory -Force steps\03-models-and-providers\work\experiments\results
   Copy-Item steps\02-llm-fundamentals\work\llm_client.py steps\03-models-and-providers\work\
   cd steps\03-models-and-providers\work
   ```
   - السطر الأول بيعمل `work` و `experiments\results` جواه مرة واحدة (`-Force` = متشتكيش لو موجود).
   - السطر التاني بينسخ آخر `llm_client.py` (فيه `chat()` بكل الـ options و `ChatResult`).
   - السطر التالت بيدخلك الفولدر.
2. venv:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install httpx pydantic
   pip freeze > requirements.txt
   ```
   (نفس Step 02. ولو عايز تفتكر كل سطر، ارجع لـ Task 0 هناك.)
3. **نسخة Ollama:**
   ```bash
   ollama --version
   ```
   عندك حالياً **0.34.4** تقريباً، والـ docs اللي قريتها فيها features من versions أحدث (مكتوب جنبها "Added in v0.40.x"). **مش لازم تحدّث** للتاسكات الأساسية. بس لو حاجة من الـ docs مش شغالة، حدّث من أيقونة Ollama ← *Restart to update* (أو نزّل الأحدث من الموقع).
4. **جهازك فيه إيه؟** افتح **Task Manager** ← **Performance**، وابعتلي:
   - **CPU** (الاسم).
   - **Memory** (الـ RAM الكلية).
   - **GPU**: الاسم، و **Dedicated GPU memory** (ده الـ VRAM). لو مفيش GPU منفصل، قول كده.

   وأنا هكتب `work/hardware.md` منهم. (هنحتاجهم في Tasks 3 و 4 و 6.)

**✅ شروط القبول:**
- [ ] `python llm_client.py` شغّال من فولدر الخطوة الجديد ويرد.
- [ ] فيه `work/requirements.txt` و `work/experiments/results/`.
- [ ] `work/hardware.md` موجود (أنا هكتبه من اللي هتبعته).

---

## Task 1 — Model card: الـ hard attributes بتاعة موديلك
> 📖 بعد شرح Ch.4 (جزء 5.1 Hard/Soft attributes، و 5.3.1 Licenses) و Ollama (جزء 3 CLI، و 7.6 LICENSE).

**الهدف:** قبل ما تقارن أي موديل بأي حاجة، اعرف **الحاجات اللي مش هتقدر تغيّرها** فيه: الـ license، والحجم، والـ quantization، وأقصى context، والـ capabilities. ده **الخطوة 1** في الـ workflow (الفلتر).

**المطلوب:** `work/model_card.py` بيكلّم Ollama API **بـ httpx** (مش `subprocess` على الـ CLI) ويطبع "model card" لكل موديل عندك.

**الـ Interface:**
```python
@dataclass
class ModelCard:
    name: str
    family: str
    parameter_size: str          # زي "3.1B"
    quantization: str            # زي "Q4_K_M"
    context_length: int | None   # أقصى context الموديل نفسه يقدر عليه
    capabilities: list[str]
    license_name: str | None
    size_on_disk_gb: float

def list_local_models() -> list[str]: ...
def get_model_card(model: str) -> ModelCard: ...
```

**✅ شروط القبول:**
- [ ] `list_local_models` من الـ endpoint اللي بيعمل زي `ollama ls`، و `get_model_card` من الـ endpoint اللي بيعمل زي `ollama show`. دوّر عليهم في [Ollama API reference](https://docs.ollama.com/api/introduction) (في الـ sidebar: *List models* و *Show model details*).
- [ ] **ابدأ بإنك تطبع الـ JSON الخام** (`json.dumps(data, indent=2, ensure_ascii=False)`) وتقراه بعينك قبل ما تكتب الـ parsing. هتلاقي الحاجات اللي محتاجها متوزعة على أكتر من مكان في الرد.
- [ ] `context_length` بيتجاب **من غير ما تكتب اسم الـ architecture بإيدك** (يعني متكتبش `"qwen2.context_length"`). الـ key بيتغيّر من عيلة موديلات للتانية. (فكّر: إزاي تلاقي key **بينتهي** بكلمة معيّنة؟)
- [ ] `size_on_disk_gb` بالـ GB بخانتين عشريتين.
- [ ] موديل مش موجود يرمي `LLMError` برسالة فيها أمر الـ `ollama pull`.
- [ ] الـ `__main__` بيطبع جدول لكل الموديلات اللي عندك (الأعمدة متظبطة).
- [ ] **اقرا الـ license بعينك:** `ollama show qwen2.5:3b --license` (أول 30 سطر كفاية). **اكتب في الـ PR:** هل ينفع تستخدم `qwen2.5:3b` في **منتج تجاري** لشركتك؟ اقتبس الجملة (قصيرة) اللي بتحسم.
- [ ] **سؤال (في الـ PR):** الموديل نفسه بيقدر على `context_length` قد إيه؟ وإيه الـ default اللي Ollama بيدّيهولك فعلاً (جزء 4.2 و 5 في الشرح)؟ (هتتأكد من الرقم التاني بنفسك في Task 4.)

**📚 هيساعدك:** [Show model details](https://docs.ollama.com/api-reference/show-model-details)، و [List models](https://docs.ollama.com/api/tags)، و [`dataclasses`](https://docs.python.org/3/library/dataclasses.html).

---

## Task 2 — قارئ الـ leaderboard: نفس الموديل، providers مختلفين
> 📖 بعد شرح Ch.4 (جزء 6) و Artificial Analysis (كله) و LMArena (كله).

**الهدف:** تحوّل صفحة الـ providers اللي حفظتها (`resources/articles/03-artificial-analysis-providers.md`) لداتا تقدر تسألها أسئلة: مين أعلى موديل مفتوح؟ ونفس الموديل بيختلف قد إيه من provider للتاني؟ ده **الخطوة 2** في الـ workflow (التضييق بالمعلومات العامة).

**المطلوب:** `work/leaderboard.py`.

**الـ Interface:**
```python
@dataclass
class Endpoint:
    provider: str
    model: str
    intelligence: int | None
    cost_per_task: float | None       # "$1.27" -> 1.27 ، "--" -> None
    time_per_task_min: float | None
    first_answer_token_s: float | None
    error_rate: float | None          # "5.7%" -> 5.7
    context: str                      # سيبه نص زي "1M" أو "131k"
    license: str                      # "Open" أو "Proprietary"

def load_endpoints(path: Path) -> list[Endpoint]: ...
def top_models(endpoints: list[Endpoint], n: int = 10, license: str | None = None) -> list[Endpoint]: ...
def providers_for(endpoints: list[Endpoint], model: str) -> list[Endpoint]: ...
```

**✅ شروط القبول:**
- [ ] افتح الملف الأول وبص على الشكل: كل **صف** في الجدول متقسّم على **سطور كتير** (خلية في كل سطر)، وبيتكرر بنفس الترتيب. الجدول بيبدأ بعد سطر `Further Analysis`. لاحظ السطور اللي فيها كلمة `logo` والسطرين اللي في آخر كل صف.
- [ ] `load_endpoints` بترجّع **525** endpoint بالظبط (عدّيتهم من الـ snapshot بتاعك). لو طلعلك رقم تاني، فيه صف بيتقرا غلط.
- [ ] `"--"` بيتحوّل لـ `None` من غير ما البرنامج يقع، والأرقام بتتحوّل لـ `float`.
- [ ] `top_models` بترجّع **موديلات مختلفة** (نفس الموديل عند 10 providers يتحسب **مرة واحدة**)، مترتّبة بالـ intelligence، ومع فلتر اختياري بالـ license.
- [ ] الـ `__main__` بيطبع:
  1. عدد الـ endpoints **Open** وعدد **Proprietary**.
  2. أعلى **10** موديلات في الكل، وأعلى **10 Open**.
  3. لموديلين من اختيارك (واحد **proprietary** موجود على أكتر من cloud، وواحد **open** عند providers كتير): جدول بكل الـ providers مترتّب بالـ **cost per task**، وتحته: **الأرخص، والأسرع (time per task)، والأقل error rate**، و**نسبة** أغلى/أرخص.
- [ ] **سؤالين (في الـ PR):**
  1. أعلى موديل open في الـ snapshot بالـ index كام؟ وأعلى موديل في الكل؟ ده بيأكد توقّع الكاتبة ولا لأ؟
  2. لو هتختار provider للموديل الـ open اللي اخترته، هتختار مين؟ وليه مش الأرخص؟ (فكّر في الـ error rate والسرعة، والحاجات اللي **مش** في الجدول.)
- [ ] **جزء من غير كود (في الـ PR):** افتح [arena.ai/leaderboard/text](https://arena.ai/leaderboard/text) واختار category قريبة من شغلك (Coding، أو Instruction Following، أو Hard Prompts)، وفلتر **License Type = Open Source**. أول 3 موديلات مين؟ وهل فيه category للغة العربية؟ (اكتب تاريخ اليوم جنب إجاباتك.)

**📚 هيساعدك:** [`pathlib.Path.read_text`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text)، و [`sorted` بـ `key`](https://docs.python.org/3/howto/sorting.html)، و [`collections.defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict).

---

## Task 3 — الوقت بيروح فين؟ Cold start و keep_alive
> 📖 بعد شرح Ollama (جزء 4.3 GPU/CPU، و 4.11 keep_alive) و Ch.4 (جزء 3.2 مقاييس الـ latency).

**الهدف:** تشوف بالأرقام **ليه أول request بطيء**، والوقت بيتقسم إزاي بين **تحميل الموديل** و **قراية الـ prompt** (prefill) و **توليد الرد** (decode).

**المطلوب:**
1. **وسّع `ChatResult`** في `llm_client.py` بـ 3 حقول جديدة جاية من رد Ollama: وقت التحميل، ووقت قراية الـ prompt، ووقت التوليد (بالثواني). (الحقول دي موجودة في الرد بتاع `/api/chat`، دوّر عليها، وهي بالـ nanoseconds زي `total_duration`.)
2. ضيف **`@property`** اسمها `output_tokens_per_second`.
3. ضيف parameter **`keep_alive`** لـ `chat()`. ⚠️ ده **مش** جوه `options` زي `num_ctx`، ده في **body الـ request نفسه**. (ارجع لجزء 4.11.)
4. في `model_card.py`: ضيف `get_running_models()` من الـ endpoint اللي بيعمل زي `ollama ps`.
5. `work/experiments/latency.py`: التجربة.

**الـ Interface:**
```python
@dataclass
class RunningModel:
    name: str
    size_gb: float
    vram_gb: float
    gpu_percent: float          # قد إيه من الموديل على الـ GPU
    context_length: int | None
    expires_at: str

def get_running_models() -> list[RunningModel]: ...
```

**التجربة:** نفس prompt قصير، `temperature=0`، `max_tokens=100`:
- **Cold:** 3 requests، كل واحد بـ `keep_alive=0` (الموديل يتشال بعد كل رد، فاللي بعده لازم يحمّله تاني).
- **Warm:** request واحد فاضي للـ preload (جزء 4.11)، وبعده 5 requests عادي.

**✅ شروط القبول:**
- [ ] الكود القديم (من Step 02) لسه شغّال: الحقول الجديدة ليها default، و `keep_alive` اختياري.
- [ ] جدول لكل request: النوع (cold/warm)، و load، و prompt eval، و eval، و total، و tokens/s، و **TTFT تقريبي** (فكّر: TTFT = إيه + إيه؟).
- [ ] بعد الـ warm requests: اطبع `get_running_models()` (الحجم، والـ VRAM، ونسبة الـ GPU، والـ context، وهيتشال إمتى).
- [ ] النتايج في `work/experiments/results/latency.json`. ابعتهالي وأنا أكتب الـ observations.
- [ ] **أسئلة (في الـ PR):** (1) في الـ cold، أنهي جزء واخد أغلب الوقت؟ (2) الموديل على جهازك **كام % GPU**؟ وده بيفسّر سرعتك في Step 02 (5–8 ثواني لـ 150 token)؟ (3) لو عملت chatbot على Ollama، هتظبط `keep_alive` على إيه؟ وليه؟

**📚 هيساعدك:** [Generate a chat message](https://docs.ollama.com/api/chat) (حقول الرد)، و [List running models](https://docs.ollama.com/api/ps)، و [`@property`](https://docs.python.org/3/library/functions.html#property).

---

## Task 4 — الـ context بياكل memory
> 📖 بعد شرح Ollama (جزء 4.2، و 4.12، و 4.14 KV cache، و 5 Context length).

**الهدف:** تقيس بنفسك **تمن** الـ context الكبير: memory أكتر، وممكن الموديل يتنقل للـ CPU ويبطأ. وتحسم **التعارض في الـ docs** (الـ default 2048 ولا 4096؟).

**المطلوب:** `work/experiments/context_memory.py`. لكل `context_size` في `[None, 2048, 4096, 8192, 16384, 32768]`:
- ابعت request قصير بالـ `context_size` ده.
- اقرا `get_running_models()` (من Task 3) وسجّل: الحجم في الـ memory، والـ VRAM، ونسبة الـ GPU، والـ `context_length` اللي Ollama حجزه.
- سجّل الـ load time والـ tokens/s (من Task 3).

**✅ شروط القبول:**
- [ ] `None` معناه "مبعتش `context_size` خالص". ده اللي هيحسم الـ default الحقيقي على جهازك.
- [ ] جدول: context، والحجم (GB)، والـ VRAM، ونسبة الـ GPU، و load time، و tokens/s.
- [ ] ⚠️ **لو الـ RAM عندك 8GB**: وقّف عند 16384، وبص على Task Manager وإنت شغّال. لو الجهاز بدأ يهنّج، اقفل التجربة.
- [ ] النتايج في `work/experiments/results/context_memory.json`. ابعتهالي.
- [ ] **أسئلة (في الـ PR):** (1) الـ default الحقيقي كام؟ مين في الـ docs كان صح؟ (2) الـ memory زادت قد إيه من 2K لـ 32K؟ وليه (الـ KV cache)؟ (3) لاحظت إيه في الـ load time لما غيّرت الـ context؟ (يعني تغيير الـ `num_ctx` بيعمل إيه للموديل المحمّل؟) (4) بناءً على الأرقام: agent محتاج 64K context (جزء 5 في الشرح) ينفع على جهازك بالموديل ده؟

---

## Task 5 — Providers زي drivers Laravel
> 📖 بعد شرح Ch.4 (جزء 5️⃣ API cost vs engineering cost: "standard API") و Ollama (جزء 7 Modelfile، و 9 OpenAI compatibility).

**الهدف:** تبني الـ abstraction اللي الكتاب نصح بيه: كود التطبيق بيقول `provider.chat(...)` ومش فارق معاه مين تحت، والاختيار من environment variable. بالظبط زي:
```php
// Laravel
MAIL_MAILER=smtp      // Mail::to(...)->send(...) مش فارق معاها
DB_CONNECTION=mysql   // Query Builder مش فارق معاه
```

**المطلوب:** `work/providers.py`:
- **`LLMProvider`** (abstract base class) فيها `chat()` بالـ parameters **المشتركة** بس.
- **`OllamaProvider`**: بيستخدم `llm_client.chat` (الـ native API). وبياخد `context_size` في الـ constructor (إعداد للـ provider، مش لكل request).
- **`OpenAICompatibleProvider`**: بيبعت **بـ httpx** لـ `{base_url}/chat/completions` (مش بالـ library بتاعة `openai`، عشان تشوف الـ mapping بعينك). جرّبه على **Ollama نفسه**: `base_url="http://localhost:11434/v1"` و `api_key="ollama"`.
- **`get_provider()`**: factory بيقرا `LLM_PROVIDER` و `LLM_MODEL` و `LLM_BASE_URL` و `LLM_API_KEY` من الـ environment.
- **`UnsupportedParameterError(LLMError)`**: لو حد طلب حاجة الـ provider مبيدعمهاش.

**الـ Interface:**
```python
class LLMProvider(ABC):
    name: str

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        seed: int | None = None,
        stop: list[str] | None = None,
    ) -> ChatResult: ...

class OllamaProvider(LLMProvider):
    def __init__(self, model: str, context_size: int | None = None): ...

class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, base_url: str, api_key: str, model: str, context_size: int | None = None): ...

def parse_openai_response(data: dict, duration_seconds: float) -> ChatResult: ...
def get_provider() -> LLMProvider: ...
```

**✅ شروط القبول:**
- [ ] `ChatResult` **نفس الشكل** من الاتنين. الـ mapping في الـ OpenAI-compatible: النص، و tokens الـ input والـ output، والـ stop reason (اتشرحوا في جدول جزء 9.2). ومفيش `total_duration` في الرد، فاحسب المدة بنفسك.
- [ ] `parse_openai_response` **pure function** (من غير network)، وليها tests في `work/test_providers.py` (زي `test_trim.py`) على dict شكله زي الأمثلة في الـ docs. ومنهم test لحالة الرد اللي اتقطع بسبب الطول.
- [ ] `OpenAICompatibleProvider` بـ `context_size` يرمي `UnsupportedParameterError` **في الـ constructor**، والرسالة بتقول الحل (Modelfile). (الـ OpenAI API مفيهوش `num_ctx`، جزء 9.5.)
- [ ] **مفيش API key في الكود.** `LLM_API_KEY` من الـ environment، ولو `LLM_PROVIDER=openai_compat` و مفيش key، يرمي error واضح. (لـ Ollama local حط أي قيمة.) في PowerShell: `$env:LLM_PROVIDER="openai_compat"`.
- [ ] `LLM_PROVIDER` بقيمة مش معروفة يرمي error فيه القيم المسموحة.
- [ ] **Modelfile:** اعمل `work/Modelfile` فيه `FROM qwen2.5:3b` و context 8192، و `ollama create qwen2.5-3b-8k -f Modelfile`. استخدمه من `OpenAICompatibleProvider`، واتأكد بـ `get_running_models()` إن الـ context بقى 8192.
- [ ] `work/experiments/same_model_two_apis.py`: نفس **5 prompts**، `temperature=0`، `seed=42`، من الـ providers الاتنين على **نفس الموديل**. جدول: الـ prompt، والنص متطابق ولا لأ، و tokens كل واحد، والوقت. النتايج في `results/same_model_two_apis.json`.
- [ ] **سؤال (في الـ PR):** الردود اتطابقت؟ الـ input tokens اتطابقت؟ لو فيه فرق، إيه السبب المحتمل؟ وده بيقولك إيه عن نصيحة الكتاب "اعمل tests لما تبدّل الـ API"؟
- [ ] **سؤال تصميم (في الـ PR):** ليه `top_k` و `context_size` **مش** في `LLMProvider.chat()`؟ وإيه البديل لو تطبيق معيّن محتاجهم؟

**📚 هيساعدك:** [`abc` — Abstract Base Classes](https://docs.python.org/3/library/abc.html)، و Ollama [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility) (الملف اللي رفعته)، و [OpenAI Chat Completions response](https://platform.openai.com/docs/api-reference/chat/object) (شكل الرد)، و [`os.environ`](https://docs.python.org/3/library/os.html#os.environ).

---

## Task 6 — Mini eval: الموديل الـ local كفاية لفكرتك؟
> 📖 بعد شرح Ch.4 (جزء 5.2 الـ workflow، و 6.3 custom leaderboards) و Anthropic (جزء 2.4 "evaluation set هو أهم خطوة").

**الهدف:** **الخطوة 3** في الـ workflow: تقيس على **داتا شبه داتاك**. هنرجع لفكرة Step 01 (`use_case.md`: استخراج داتا الإيصالات)، بس على **نص الإيصال** (كأنه طالع من OCR)، مش الصورة. والسؤال: الموديل ده بيوصل للـ **usefulness threshold** اللي حددته هناك (≥ 95% للإجمالي والتاريخ)؟

**المطلوب:**
- **الداتا:** قولّي وأنا أكتب `work/data/receipts.json`: حوالي 15 إيصال (عربي وإنجليزي ومخلوط، ونصوص "وسخة" زي OCR حقيقي)، ولكل واحد الإجابة الصح: `vendor`، و `date` (YYYY-MM-DD)، و `total`، و `currency`.
- `work/experiments/model_eval.py`: لكل **موديل** في لستة candidates، ولكل إيصال: structured output (طريقة 3 من Step 02 Task 5، بـ pydantic schema)، و `temperature=0`.

**الـ Interface:**
```python
class Receipt(BaseModel):
    vendor: str
    date: str
    total: float
    currency: str

def extract(text: str, model: str) -> tuple[Receipt | None, ChatResult]: ...
def score(predicted: Receipt | None, expected: dict) -> dict[str, bool]: ...   # لكل حقل: صح ولا لأ
```

**✅ شروط القبول:**
- [ ] `score` بيقارن بعقل: `total` بفرق صغير مسموح (فكّر في 120 و 120.0)، و `vendor` من غير فرق الـ case والمسافات الزيادة. اكتب القواعد في docstring.
- [ ] لكل موديل: **الدقة لكل حقل** (%)، و**الإيصالات اللي كل حقولها صح** (%)، و**متوسط الـ latency**، و**متوسط الـ input/output tokens**، و**tokens/s**، و**الحجم في الـ memory** (من `get_running_models()`)، و**الـ license** (من Task 1).
- [ ] جدول مقارنة، وتحته: أنهي موديل **عدّى الـ threshold** بتاع `use_case.md`؟
- [ ] لكل إيصال غلط: اطبعه مع الإجابة المتوقعة والمتولّدة (هنحتاجهم في الـ error analysis).
- [ ] النتايج في `work/experiments/results/model_eval.json`. ابعتهالي وأنا أكتب الـ observations.
- [ ] **الـ candidates:**
  - **أساسي:** `qwen2.5:3b` (عندك).
  - **اختياري، قولّي الأول قبل ما تنزّل:**

    | الموديل | الحجم (من ollama.com) | ليه |
    |---|---|---|
    | `qwen2.5:1.5b` | **986MB** | efficiency-first: الأصغر من نفس العيلة كفاية؟ |
    | `llama3.2:3b` | **2.0GB** | نفس الحجم، **عيلة تانية** (tokenizer وتدريب و license مختلفين) |
    | `qwen2.5:7b` | **4.7GB** | الأكبر من نفس العيلة (لو الـ RAM عندك 16GB أو أكتر) |
- [ ] **أسئلة (في الـ PR):** (1) الموديل اللي عدّى (لو فيه) ينفع **قانونياً** في منتج تجاري (Task 1)؟ (2) لو مفيش موديل local عدّى، إيه الخطوة الجاية حسب الـ workflow؟ (ارجع لجزء 5.2 في شرح الكتاب: "الخطوات iterative".) (3) 15 إيصال عدد كفاية تاخد بيه قرار؟ ليه؟

---

## Task 7 — التكلفة والقرار
> 📖 بعد شرح Anthropic (جزء 3 Pricing)، و Ch.4 (جزء 3.3 والمحور 5️⃣)، و AA (جزء 1.3 Cost per Task).

**الهدف:** تحسب **التكلفة الحقيقية** لفكرة الإيصالات لو استخدمت Claude API بدل الـ local، بالـ tokens اللي **قستها فعلاً** في Task 6، وتكتب **قرار** مبني على كل اللي عملته.

**المطلوب:**
- **الداتا:** قولّي وأنا أكتب `work/data/prices.json` من صفحة Pricing اللي رفعتها (Haiku 5.5، و Sonnet 5.5، و Opus 5.5، و Fable 5.2: input، و output، و cache hit، وتاريخ الـ snapshot).
- `work/cost.py`.

**الـ Interface:**
```python
@dataclass
class Price:
    name: str
    input_per_mtok: float
    output_per_mtok: float
    cache_hit_per_mtok: float

def load_prices(path: Path) -> list[Price]: ...
def request_cost(price: Price, input_tokens: int, output_tokens: int,
                 cached_tokens: int = 0, batch: bool = False) -> float: ...
def monthly_cost(price: Price, avg_input: float, avg_output: float, requests_per_day: int,
                 days: int = 30, cached_ratio: float = 0.0, batch: bool = False) -> float: ...
```

**✅ شروط القبول:**
- [ ] `cached_tokens` **جزء من** `input_tokens` (مش زيادة عليه): الجزء ده بيتحسب بسعر الـ cache hit، والباقي بسعر الـ input العادي.
- [ ] `batch=True` = خصم 50% (جزء 3.6).
- [ ] `work/test_cost.py` فيه test **بالمثال المحسوب في صفحة Anthropic** (جزء 3.9 في الشرح): Opus 5.5، و 50,000 input، و 15,000 output = **$0.50** (من غير الـ runtime)، و مع 40,000 cached = **$0.348**. لو الـ test عدّى، الـ function بتاعتك بتحسب زي Anthropic بالظبط.
- [ ] الـ `__main__`: بالـ **متوسط الحقيقي** للـ tokens من `results/model_eval.json`، ولعدد إيصالات في اليوم **تختاره إنت** (من `use_case.md`: شركة 200 موظف)، اطبع جدول: كل موديل Claude × (عادي، و batch، و caching للـ system prompt). وجنبهم سطر للـ local: **$0 لكل request** (بس اكتب جنبه إيه التكاليف اللي **مش** في الرقم ده).
- [ ] ⚠️ **ملاحظة تكتبها في الـ output أو في الـ PR:** الـ tokens اللي قستها جاية من **tokenizer الـ Qwen**. على Claude العدد هيختلف (جزء 3.2 في الشرح). يعني الأرقام **تقدير** مش فاتورة.
- [ ] **`work/model_decision.md`** (ده التمرين نفسه، بس لو عايز مسودة مني من نتايجك قولّي): **Decision record** لفكرة الإيصالات:
  1. **Hard attributes** (الـ privacy، والـ license، والـ hardware، واللغة).
  2. **Shortlist** من الـ leaderboards (بتاريخ الـ snapshot).
  3. **نتايج الـ eval** بتاعك (Task 6).
  4. **التكلفة** (الجدول اللي فوق).
  5. **القرار**: local ولا API ولا هجين (مثلاً executor/advisor، جزء 2.5 في شرح Anthropic)؟ وليه.
  6. **إيه اللي يخليك تغيّر القرار** (حجم أكبر؟ موديل جديد؟ تغيير في السياسة؟ deprecation؟).

---

## 🎁 Bonus (اختياري)
- **B1 — Local-only mode:** فعّل `OLLAMA_NO_CLOUD=1` (جزء 4.7، و environment variables على Windows في جزء 4.4)، واعمل restart لـ Ollama، واتأكد من السطر اللي في `server.log` (جزء 2: مكانه). ده أول حاجة تعملها على جهاز عليه داتا حساسة.
- **B2 — `AnthropicProvider`** (⚠️ **محتاج Claude API key، قولّي الأول**): provider تالت بـ httpx على Messages API. ⚠️ أحدث الموديلات **شالت `temperature`** (جزء 4.6 في شرح Anthropic)، فقرر هيعمل إيه لو حد بعتها (`UnsupportedParameterError`؟). وشغّل Task 6 على Haiku 5.5 **بإيصالات وهمية بس** (الـ eval set بتاعنا وهمي أصلاً)، وقارن الدقة والتكلفة الحقيقية من الـ `usage`. (Step 04 هيعمل ده بالـ SDK الرسمي بالتفصيل.)
- **B3 — KV cache quantization:** `OLLAMA_KV_CACHE_TYPE=q8_0` (جزء 4.14)، وأعد Task 4. الـ memory قلّت قد إيه؟ وأعد Task 6 بسرعة: الدقة اتأثرت؟

---

## 📤 التسليم
1. `git add` و `git commit` بعد كل تاسك (مثال: `work 03: task 1 model card from ollama api`).
2. `git push -u origin work/03-models-and-providers`
3. افتح PR على `main`، واكتب فيه إجابات الأسئلة اللي مكتوب جنبها "(في الـ PR)"، واللي مش متأكد منه.
4. هراجع شغلك في الشات، ملف ملف، وإنت تصلّح وتعمل push لحد ما يبقى جاهز.
