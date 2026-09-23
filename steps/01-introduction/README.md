# Step 01 — مقدمة للـ AI Engineering

> **Branch:** `step/01-introduction` · **المدة المتوقعة:** 2–3 أيام · **المتطلبات:** أساسيات Python + OOP

## 🎯 الأهداف
بعد الخطوة دي هتقدر:
- تشرح مين هو الـ **AI Engineer** وبيعمل إيه في يومه فعلاً.
- تفرّق بوضوح بين **AI Engineer** و **ML Engineer** و **Data Scientist** و **Software Engineer**.
- ترسم شكل (architecture) أي **AI application** وتعرف كل جزء فيه دوره إيه.
- تفهم إمتى تستخدم AI في مشكلة وإمتى لأ.
- تجهّز بيئة شغل احترافية: `uv`، `.env`، و **API keys** بشكل آمن.
- تعمل أول **API call** لـ Claude وتفهم الـ response راجع شكله إيه.

## 🧭 الصورة الكبيرة
من كام سنة، لو عايز تعمل feature "ذكية" (تلخيص، تصنيف، chatbot) كان لازم فريق يجمع data ويدرّب موديل شهور. النهارده فيه **foundation models** جاهزة (زي Claude) بتعمل ده من غير تدريب — إنت بس بتكلّمها عن طريق **API**.

ده خلق دور جديد: الشخص اللي **بيبني منتجات حقيقية فوق الموديلات دي**. ده الـ AI Engineer، ودي الخطوة اللي بتحدد النطاق بتاع الـ roadmap كله. كل الخطوات الجاية (prompts، RAG، tools، agents، evals، deployment) هي أجزاء من الصورة اللي هنرسمها هنا.

---

## 1. مين هو الـ AI Engineer؟

### يعني إيه؟
الـ **AI Engineer** هو مهندس software بيبني **تطبيقات ومنتجات** بتستخدم **pre-trained models** (خصوصاً **LLMs**) كـ building block — زي ما الـ backend engineer بيستخدم database من غير ما يكتب database engine بنفسه.

> 🧱 **تشبيه:** الـ ML Engineer بيصنع **المحرّك**. الـ AI Engineer بياخد المحرّك الجاهز ويبني حواليه **عربية**: شاسيه، فرامل، عداد، أمان، وتجربة سواقة مريحة.

### إزاي بيشتغل؟ (يومه شكله إيه)
الشغل الفعلي بيدور حوالين الأسئلة دي:

| السؤال | الأداة/المهارة | الخطوة في الـ roadmap |
|---|---|---|
| أختار أنهي موديل؟ (quality vs cost vs latency) | Model selection | 03 |
| أكلّم الموديل إزاي من الكود؟ | LLM APIs، streaming، structured output | 04 |
| أكتب التعليمات إزاي عشان يدّي نتيجة ثابتة؟ | Prompt engineering | 05 |
| أحمي التطبيق من الاستخدام الغلط؟ | Guardrails، prompt injection | 06 |
| الموديل ميعرفش بيانات شركتي — أعمل إيه؟ | Embeddings، vector DBs، **RAG** | 07–09 |
| عايز الموديل ينفّذ actions (يبعت إيميل، يكلّم API)؟ | **Tool use**، **Agents**، **MCP** | 10–12 |
| صور وصوت وPDFs؟ | Multimodal | 13 |
| أعرف منين إن التعديل حسّن مش بوّظ؟ | **Evals** | 14 |
| أوصّله للـ users بشكل موثوق ورخيص؟ | Deployment، monitoring، caching | 15 |

لاحظ إن **ولا سؤال فيهم** "إزاي أدرّب neural network؟" — ده مش شغلنا.

### مثال عملي
نفس الطلب "عايزين نصنّف تذاكر الدعم الفني أوتوماتيك":

- **الطريقة القديمة (ML):** نجمع 50 ألف تذكرة متصنّفة ← ننضّف الـ data ← ندرّب classifier ← نقيس الـ accuracy ← نعمل deploy. **أسابيع/شهور.**
- **طريقة الـ AI Engineer:** نكتب prompt فيه التصنيفات ← نكلّم LLM API ← نتحقق من الـ output ← نعمل eval على 100 تذكرة ← deploy. **أيام.**

الكود الكامل للطريقة التانية موجود في [`examples/ai_app_anatomy.py`](examples/ai_app_anatomy.py) وهنشرحه في الـ concept رقم 3.

### ⚠️ أخطاء شائعة
- **"AI Engineer = بيكتب prompts وخلاص".** لأ — الـ prompt جزء صغير. أغلب الشغل هندسة software عادية: APIs، error handling، data pipelines، testing، deployment، cost.
- **"لازم أذاكر رياضيات الـ ML الأول".** مش محتاجها عشان تبدأ. محتاج تفهم **سلوك** الموديل (tokens، context window، hallucination) — ودي Step 02.
- **"الموديل ذكي، هيتصرّف".** الموديل احتمالي (probabilistic) — ممكن يغلط أو يرجّع format غلط. شغلك إنك تبني نظام **يتحمّل** ده.

---

## 2. الفرق بين AI Engineer و ML Engineer و Data Scientist

### يعني إيه؟
الأدوار دي بتتداخل، بس كل واحد تركيزه مختلف:

| | **Data Scientist** | **ML Engineer** | **AI Engineer** | **Software Engineer** |
|---|---|---|---|---|
| **السؤال الأساسي** | إيه اللي الـ data بتقوله؟ | إزاي أدرّب وأشغّل موديل كويس؟ | إزاي أبني منتج مفيد فوق موديل جاهز؟ | إزاي أبني نظام شغّال وموثوق؟ |
| **الـ output** | Insights، تقارير، تجارب | Trained models، training pipelines | AI features وتطبيقات | Apps، APIs، systems |
| **بيبدأ من** | Data | Data + model architecture | **Pre-trained model + API** | Requirements |
| **أدوات نموذجية** | pandas، SQL، notebooks، statistics | PyTorch، GPUs، MLOps، feature stores | LLM APIs، prompts، vector DBs، agents، evals | Frameworks، databases، cloud |
| **الرياضيات** | Statistics كتير | Linear algebra، calculus، optimization | **شبه مفيش** — فهم سلوكي | مفيش غالباً |
| **دورة الشغل** | أسابيع (تحليل) | أسابيع–شهور (تدريب) | ساعات–أيام (prototype) | أيام–أسابيع |

### إزاي بيشتغل؟
الفرق الجوهري في **اتجاه الشغل**:

```
ML Engineer:   Data  ──►  Train  ──►  Model  ──►  (منتج)
AI Engineer:   Product idea  ──►  Model جاهز  ──►  Prompt/RAG/Tools  ──►  Evals  ──►  (منتج)
```

الـ ML Engineer بيبدأ بالـ data وينتهي بموديل. الـ AI Engineer بيبدأ بالموديل (جاهز) وينتهي بمنتج. عشان كده الـ AI Engineer أقرب لـ **Software Engineer + فهم عميق لسلوك الموديلات**.

### مثال عملي
شركة عايزة "chatbot بيجاوب على أسئلة العملاء من الـ documentation بتاعتها":

- **Data Scientist:** يحلل أكتر الأسئلة تكراراً ونسبة الأسئلة اللي بتتحل.
- **ML Engineer:** (لو احتاجوه) يعمل fine-tuning أو يستضيف open-source model على GPUs بتاعة الشركة.
- **AI Engineer:** يبني الـ chatbot نفسه: RAG على الـ docs، prompt، guardrails، evals، API، monitoring.
- **Software Engineer:** يبني الـ chat UI، الـ auth، ويربطه بباقي النظام.

### ⚠️ أخطاء شائعة
- الخلط في الـ job descriptions حقيقي — شركات كتير بتكتب "AI Engineer" وهي عايزة ML Engineer. **اقرا المتطلبات** مش العنوان: لو فيها PyTorch training و GPUs و model architectures يبقى ML.
- **Fine-tuning** مش ممنوع على الـ AI Engineer، بس هو **آخر حل** مش أوله. الترتيب: prompting ← RAG ← fine-tuning (هنشوف ده في Step 09).

---

## 3. شكل الـ AI Application (Anatomy)

### يعني إيه؟
أي AI app — من أبسط chatbot لأعقد agent — مبني من نفس الطبقات. الـ LLM call نفسه **سطر واحد**؛ الباقي هو اللي بيفرّق بين demo ومنتج.

### إزاي بيشتغل؟

```
┌──────────┐   ┌───────────────┐   ┌───────────────────┐   ┌───────────┐   ┌──────────────────┐   ┌──────────┐
│  User    │──►│ 1. Input      │──►│ 2. Prompt building│──►│ 3. LLM    │──►│ 4. Output parsing│──►│ Response │
│  input   │   │   validation  │   │  + context (RAG)  │   │   API     │   │   & validation   │   │ to user  │
└──────────┘   └───────────────┘   └───────────────────┘   └─────┬─────┘   └──────────────────┘   └──────────┘
                                                                 │ ▲
                                                           ┌─────▼─┴─────┐
                                                           │ 5. Tools    │  (APIs، DB، search...)
                                                           └─────────────┘
               ─────────────── 6. Logging / Monitoring / Evals / Cost tracking (حوالين كل ده) ───────────────
```

| الطبقة | بتعمل إيه | هنتعلمها فين |
|---|---|---|
| **1. Input validation** | ترفض الفاضي/الطويل جداً/الخطير (prompt injection) | 06 |
| **2. Prompt building** | تجمع التعليمات + input المستخدم + context (من RAG أو memory) | 05، 09 |
| **3. LLM call** | تبعت للـ API، تتعامل مع errors و rate limits و streaming | 04 |
| **4. Output parsing** | تحوّل النص لـ data (JSON)، وتتحقق إنه صح — **عمرك ما تثق فيه على طول** | 04، 06 |
| **5. Tools** | الموديل يطلب ينفّذ action، الكود بتاعك ينفّذ ويرجّعله النتيجة | 10–12 |
| **6. Observability** | logs، traces، تكلفة كل request، evals مستمرة | 14، 15 |

### مثال عملي
[`examples/ai_app_anatomy.py`](examples/ai_app_anatomy.py) بيطبّق الطبقات 1–4 على "مصنِّف تذاكر دعم فني". القلب بتاعه:

```python
def classify(ticket: str, llm=call_llm_mock) -> TicketResult:
    ticket = validate_input(ticket)        # 1) Input validation
    messages = build_messages(ticket)      # 2) Prompt building
    raw = llm(SYSTEM_PROMPT, messages)     # 3) LLM call
    return parse_output(raw)               # 4) Output parsing & validation
```

لاحظ إن الـ `llm` **parameter** — فتقدر تبدّل الموديل الحقيقي بـ **mock** للتجربة والـ testing من غير API key ومن غير فلوس:

```bash
uv run ai_app_anatomy.py --mock   # بيشتغل من غير API key
uv run ai_app_anatomy.py          # بيكلّم Claude فعلاً
```

الـ output في الـ mock mode:
```
[billing  ] 'اتخصم مني فلوس مرتين على نفس الفاتورة الشهر د'
            ↳ (mock) ملخص التذكرة
[technical] 'التطبيق بيقفل لوحده أول ما أفتح صفحة الإعدادا'
            ↳ (mock) ملخص التذكرة
[account  ] 'نسيت الباسورد ومش عارف أعمل login'
            ↳ (mock) ملخص التذكرة
[rejected ] '' ← التذكرة فاضية
```

### ⚠️ أخطاء شائعة
- **تثق في الـ output على طول:** الموديل ممكن يرجّع category مش موجودة، أو JSON ملفوف في ` ```json `. شوف `parse_output()` — بتنضّف وبتتحقق وبترجع لـ `"other"` لو القيمة غريبة. (في Step 04 هنتعلم **structured outputs** اللي بتضمن الـ format من الـ API نفسه.)
- **تخلط تعليماتك بكلام المستخدم:** لاحظ إننا حاطين التذكرة جوه `<ticket>...</ticket>` عشان الموديل يعرف ده **data** مش أوامر. ده أول خط دفاع ضد prompt injection (Step 06).
- **تربط الكود بموديل واحد:** خلّي الـ LLM call في function لوحدها — عشان تبدّل الموديل/الـ provider أو تعمل mock بسهولة.

---

## 4. إمتى تستخدم AI (وإمتى لأ)

### يعني إيه؟
أهم مهارة للـ AI Engineer مش إنه يعرف يستخدم LLM — إنه يعرف **إمتى ميستخدموش**.

### إزاي بيشتغل؟
اسأل نفسك الأسئلة دي:

| السؤال | لو الإجابة "آه" |
|---|---|
| فيه قاعدة واضحة (if/else، regex، SQL) بتحل المشكلة؟ | **استخدم الكود العادي** — أرخص وأسرع و100% ثابت |
| المدخلات لغة طبيعية مش منظّمة (إيميلات، شكاوى، مستندات)؟ | LLM مناسب |
| الغلطة الواحدة كارثية ومفيش مراجعة بشرية (حسابات مالية، قرارات طبية)؟ | LLM لوحده **لأ** — لازم human-in-the-loop أو validation صارم |
| محتاج نفس الإجابة بالظبط كل مرة؟ | فكّر مرتين — الـ LLMs مش deterministic |
| الـ latency لازم تبقى أقل من كام millisecond؟ | LLM غالباً بطيء ليك |

### مثال عملي
- ❌ "احسب إجمالي الفاتورة" ← `sum(items)`. متبعتهاش لـ LLM.
- ❌ "اتأكد إن الإيميل format صح" ← regex.
- ✅ "استخرج اسم العميل ورقم الطلب من الإيميل ده المكتوب بأي شكل" ← LLM ممتاز.
- ✅ "لخّص الـ 40 صفحة دول في نقاط" ← LLM ممتاز.
- ⚠️ "وافق أو ارفض طلب القرض" ← LLM ممكن **يساعد** (يلخّص، يرتّب)، بس القرار يفضل بقواعد واضحة + إنسان.

### ⚠️ أخطاء شائعة
- **"AI for everything":** كل LLM call ليه تكلفة (فلوس + وقت + احتمال غلط). لو الكود العادي بيحلها، هو الأحسن.
- **تقيس بالإحساس:** "جرّبته 3 مرات واشتغل" مش قياس. من أول يوم فكّر: هقيس الجودة إزاي؟ (Step 14).

---

## 5. تجهيز البيئة: `uv` و `.env` و API keys

### يعني إيه؟
- **`uv`**: أداة حديثة (مكتوبة بـ Rust) بتدير نسخ Python والـ virtual environments والـ packages — بديل سريع جداً لـ `pip` + `venv` + `pyenv` في أداة واحدة.
- **API key**: "باسورد" بيثبت هويتك للـ provider وبيتحسب عليه الاستهلاك (الفلوس). **أي حد معاه الـ key بتاعك بيصرف من حسابك.**
- **`.env`**: ملف محلي فيه الـ secrets كـ `KEY=value`، والكود بيقراه كـ **environment variables**. الملف ده **مبيترفعش على git أبداً**.

### إزاي بيشتغل؟

**أ) تسطيب `uv`:**
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv --version
```

**ب) مشروع جديد بـ `uv`** (ده الـ workflow اللي هنستخدمه في المشاريع بتاعتنا):
```bash
uv init my-ai-app          # بيعمل pyproject.toml + main.py + .python-version
cd my-ai-app
uv add anthropic python-dotenv   # بيضيفهم لـ pyproject.toml ويعمل .venv و uv.lock
uv run main.py             # بيشغّل جوه الـ venv من غير activate
```

| الأمر | المقابل القديم |
|---|---|
| `uv init` | عمل الفولدر و `requirements.txt` بإيدك |
| `uv add pkg` | `pip install pkg` + تعديل requirements بإيدك |
| `uv run file.py` | `source .venv/bin/activate && python file.py` |
| `uv python install 3.12` | `pyenv install 3.12` |
| `uv.lock` | نسخ دقيقة لكل dependency ← نفس البيئة عند أي حد |

**ج) تشغيل أمثلة الخطوة دي** (فيها `requirements.txt` بدل `pyproject.toml`):
```bash
cd steps/01-introduction/examples
uv venv                               # يعمل .venv
uv pip install -r requirements.txt    # يسطّب الـ dependencies
uv run check_env.py
```

**د) الحصول على API key:**
1. ادخل على [Claude Console](https://console.anthropic.com/) واعمل account.
2. من **Settings → API Keys** اعمل key جديد (بيبدأ بـ `sk-ant-...`). **هيظهر مرة واحدة بس** — انسخه.
3. ضيف رصيد (credits) أو استخدم الـ free credits لو متاحة، وحط **spending limit** عشان متتفاجئش.

**هـ) تخزين الـ key في `.env`:**
```bash
cp .env.example .env
# افتح .env وحط الـ key:
# ANTHROPIC_API_KEY=sk-ant-...
```

الـ `.gitignore` في الريبو فيه `.env` أصلاً، فمش هيترفع. اتأكد بنفسك:
```bash
git check-ignore -v .env    # لازم يطبع السطر اللي في .gitignore
```

**و) الكود بيقرا الـ key إزاي:**
```python
from dotenv import load_dotenv
import anthropic

load_dotenv()                  # يقرا .env ويحط القيم في os.environ
client = anthropic.Anthropic() # يدوّر على ANTHROPIC_API_KEY لوحده
```
مفيش ولا مكان في الكود فيه الـ key نفسه. ده **القاعدة** مش اختيار.

### مثال عملي
[`examples/check_env.py`](examples/check_env.py) بيفحص كل ده ويقولك إيه ناقص — **من غير ما يطبع الـ key** (بيعمله mask):
```
— فحص البيئة —
✅ Python 3.12.4
✅ package: anthropic
✅ package: python-dotenv
✅ لقيت ملف .env
✅ ANTHROPIC_API_KEY موجود (sk-ant-...x9Qa)

🎉 البيئة جاهزة. جرّب: uv run hello_claude.py
```

### ⚠️ أخطاء شائعة
- **`api_key="sk-ant-..."` في الكود:** أشهر غلطة. bots بتمسح GitHub كل دقيقة بتدوّر على keys. لو حصل: **اعمل revoke للـ key فوراً من الـ Console** — مسح الـ commit مش كفاية لأنه موجود في الـ history.
- **تطبع الـ key في logs أو error messages:** استخدم mask زي `check_env.py`.
- **`.env` اتعمله commit قبل ما تضيفه لـ `.gitignore`:** الـ `.gitignore` مبيأثرش على ملفات متتبّعة أصلاً. لازم `git rm --cached .env` + revoke للـ key.
- **تسطّب packages في الـ Python بتاع النظام:** دايماً virtual environment (و `uv` بيعمل ده لوحده).
- **تنسى إن فيه تكلفة:** كل call بيتحسب بالـ tokens. حط spending limit من أول يوم.

---

## 6. أول API call لـ Claude

### يعني إيه؟
الـ **LLM API** عبارة عن HTTP endpoint: بتبعتله request فيه (الموديل + الرسايل)، بيرجّعلك response فيه (رد الموديل + معلومات الاستهلاك). الـ **SDK** (`anthropic`) بيغلّف ده في Python functions سهلة.

### إزاي بيشتغل؟
```
Your code ──► POST https://api.anthropic.com/v1/messages
              { model, max_tokens, messages: [{role: "user", content: "..."}] }
          ◄── { content: [{type: "text", text: "..."}], stop_reason, usage: {input_tokens, output_tokens} }
```

أهم الحاجات في الـ request:
| الـ parameter | يعني إيه |
|---|---|
| `model` | أنهي موديل. هنا `claude-opus-5` (الأقوى في الاستخدام العام). بدائل: `claude-sonnet-5` (توازن سعر/جودة)، `claude-haiku-4-5` (الأرخص والأسرع) |
| `max_tokens` | أقصى طول للرد (بالـ tokens). لو الرد وصله بيتقطع |
| `messages` | المحادثة: list من `{"role": "user" \| "assistant", "content": "..."}` |
| `system` | (اختياري) تعليمات عامة للموديل — شفناه في `ai_app_anatomy.py` |

وأهم الحاجات في الـ response:
| الحقل | يعني إيه |
|---|---|
| `content` | **list** من blocks (مش string!) — كل block ليه `type`؛ النص في الـ blocks اللي `type == "text"` |
| `stop_reason` | الموديل وقف ليه: `end_turn` (خلّص طبيعي)، `max_tokens` (اتقطع)، `refusal` (رفض)، `tool_use` (عايز يستخدم tool — Step 10) |
| `usage` | عدد الـ `input_tokens` و `output_tokens` — **دي اللي بتتحاسب عليها** |

### مثال عملي
[`examples/hello_claude.py`](examples/hello_claude.py) — الجزء الأساسي:
```python
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "عرّفني بنفسك في جملتين."}],
)

if response.stop_reason == "refusal":
    raise SystemExit("الموديل رفض الطلب")

answer = "".join(block.text for block in response.content if block.type == "text")
print(answer)
print(response.usage.input_tokens, response.usage.output_tokens)
```

التشغيل:
```bash
uv run hello_claude.py
uv run hello_claude.py "اشرحلي يعني إيه AI Engineer في جملتين"
```

الملف الكامل كمان بيتعامل مع الـ errors الأساسية (`AuthenticationError`، `RateLimitError`، `APIConnectionError`) وبيطبع الـ usage.

> 🔁 **البدائل:** نفس الفكرة بالظبط مع OpenAI (`openai` SDK) أو Google Gemini (`google-genai`) أو موديلات local عن طريق Ollama — الشكل: client ← create(model, messages) ← response. هنقارن بينهم في Step 03.

### ⚠️ أخطاء شائعة
- **`response.content[0].text` على طول:** الـ `content` list وممكن يبقى فيها blocks مش text (زي thinking أو tool_use)، أو يبقى الرد refusal. فلتر بالـ `type` واتأكد من `stop_reason` الأول.
- **`max_tokens` صغير أوي:** الرد يتقطع في النص. لو `stop_reason == "max_tokens"` زوّده.
- **تتجاهل الـ `usage`:** من أول call اتعوّد تبص على عدد الـ tokens — ده اللي هيحدد تكلفة منتجك.
- **تكتب اسم الموديل غلط أو بتاريخ قديم من الإنترنت:** استخدم الأسماء من [صفحة الموديلات الرسمية](https://docs.anthropic.com/en/docs/about-claude/models).

---

## 🛠️ تطبيق عملي (Hands-on)
المطلوب تمشي على الخطوات دي بالترتيب:

1. **سطّب `uv`** وتأكد بـ `uv --version`.
2. **جهّز الأمثلة:**
   ```bash
   cd steps/01-introduction/examples
   uv venv && uv pip install -r requirements.txt
   ```
3. **شغّل الـ pipeline من غير API key:** `uv run ai_app_anatomy.py --mock` واقرا الكود وحدد كل طبقة من الـ 4.
4. **اعمل API key** وحطه في `.env`، وشغّل `uv run check_env.py` لحد ما كله يبقى ✅.
5. **أول call:** `uv run hello_claude.py` وبص على الـ tokens.
6. **الـ pipeline الحقيقي:** `uv run ai_app_anatomy.py` (من غير `--mock`) وقارن الـ summaries بتاعة Claude بالـ mock.

| الملف | بيعمل إيه | محتاج API key؟ |
|---|---|:---:|
| [`check_env.py`](examples/check_env.py) | يفحص Python والـ packages والـ `.env` والـ key | لأ |
| [`hello_claude.py`](examples/hello_claude.py) | أول API call + error handling + usage | آه |
| [`ai_app_anatomy.py`](examples/ai_app_anatomy.py) | AI app كامل بسيط (4 طبقات) مع mock mode | لأ مع `--mock` |

## 🧪 تمارين
1. **جدول أدوار:** اختار 3 job postings حقيقية عنوانها "AI Engineer" وصنّف كل واحدة: هي فعلاً AI Engineer ولا ML Engineer متنكّر؟ على أساس إيه؟
2. **AI ولا لأ؟** لكل مشكلة قول هتحلها بـ LLM ولا بكود عادي وليه: (أ) التحقق من رقم قومي، (ب) الرد على review سلبي بنبرة مهذبة، (ج) ترجمة واجهة التطبيق، (د) حساب الضريبة، (هـ) استخراج مهارات من CV.
3. **Anatomy:** ضيف لـ `ai_app_anatomy.py` category جديدة `"shipping"` (للشحن والتوصيل) — عدّل `CATEGORIES` والـ mock، وجرّب بتذكرة "الأوردر بتاعي متأخر أسبوع". لاحظ إن الـ `SYSTEM_PROMPT` اتحدّث لوحده.
4. **Observability بسيطة:** عدّل `hello_claude.py` يحسب **التكلفة التقريبية** للـ call بالدولار (اضرب الـ tokens في أسعار الموديل من [صفحة الأسعار](https://www.anthropic.com/pricing)).
5. **جرّب موديلات:** شغّل نفس السؤال على `claude-opus-5` و `claude-haiku-4-5` وقارن: الجودة، السرعة (استخدم `time.perf_counter()`)، وعدد الـ tokens.
6. **Secret hygiene:** اعمل ملف `test.env` فيه key وهمي، واعمل `git status` — بيظهر؟ ليه؟ إزاي تصلّحها؟ (تلميح: بص على `.gitignore`).

## ❓ أسئلة مراجعة (Interview-style)

<details><summary>1. إيه الفرق بين AI Engineer و ML Engineer؟</summary>

الـ ML Engineer بيدرّب ويحسّن ويستضيف الموديلات نفسها (data، training، model architecture، GPUs). الـ AI Engineer بيبني منتجات فوق موديلات جاهزة: بيختار الموديل، يكتب الـ prompts، يبني RAG و tools و agents، يعمل evals، ويعمل deploy. الـ ML Engineer بيبدأ من الـ data وينتهي بموديل؛ الـ AI Engineer بيبدأ من الموديل وينتهي بمنتج.
</details>

<details><summary>2. ارسم الـ architecture بتاعة AI app بسيط واشرح كل جزء.</summary>

Input validation ← Prompt building (+ context من RAG/memory) ← LLM call (مع retries/errors) ← Output parsing & validation ← response. وممكن loop مع Tools لو الموديل محتاج ينفّذ actions. وحوالين كله: logging، monitoring، cost tracking، evals. النقطة المهمة: الـ LLM call جزء صغير؛ الـ reliability بتيجي من باقي الطبقات.
</details>

<details><summary>3. ليه متثقش في output الـ LLM على طول؟ وإزاي تحمي نفسك؟</summary>

لأن الموديل probabilistic: ممكن يرجّع format غلط، قيمة مش في القائمة المسموحة، أو معلومة غلط (hallucination). الحماية: structured outputs، validation للـ output (schema + قيم مسموحة)، fallback values، retries، وevals بتقيس معدّل الغلط.
</details>

<details><summary>4. هتخزّن API keys إزاي في مشروع؟ ولو key اترفع على GitHub بالغلط تعمل إيه؟</summary>

في environment variables (محلياً عن طريق `.env` متجاهَل في git، وفي الـ production عن طريق secrets manager). ولا key في الكود أبداً. لو اترفع: **revoke فوراً** من الـ Console واعمل key جديد — مسح الـ commit مش كفاية لأنه موجود في الـ history وممكن يكون اتسحب خلاص.
</details>

<details><summary>5. إمتى تقول "لأ، مش هنستخدم LLM هنا"؟</summary>

لما فيه حل deterministic واضح (قواعد، regex، SQL، حسابات)، لما محتاج نفس النتيجة بالظبط كل مرة، لما الـ latency أو التكلفة مش مقبولين، أو لما الغلطة كارثية ومفيش human review. الـ LLM مناسب للغة الطبيعية غير المنظّمة والمهام اللي فيها "فهم".
</details>

<details><summary>6. إيه أهم الحقول في response الـ Messages API؟</summary>

`content` (list من blocks — النص في الـ `type == "text"`)، `stop_reason` (`end_turn` / `max_tokens` / `refusal` / `tool_use`)، و `usage` (`input_tokens` و `output_tokens` اللي بتتحاسب عليهم).
</details>

<details><summary>7. ليه `uv` بدل `pip` + `venv`؟</summary>

أداة واحدة بتدير نسخة Python والـ venv والـ packages، أسرع بمراحل، وبتعمل `uv.lock` بيضمن إن كل الناس (والـ server) عندهم نفس النسخ بالظبط، و `uv run` بيشغّل جوه الـ venv من غير activate.
</details>

## 📌 الملخص (Cheat Sheet)
| المفهوم | في جملة واحدة |
|---|---|
| AI Engineer | بيبني منتجات فوق موديلات جاهزة عن طريق APIs — مش بيدرّب موديلات |
| ML Engineer | بيدرّب ويحسّن ويستضيف الموديلات نفسها |
| Foundation model | موديل كبير متدرّب مسبقاً ينفع لمهام كتير من غير تدريب إضافي |
| AI app anatomy | Input validation ← Prompt ← LLM ← Output validation (+ Tools + Observability) |
| متى AI | لغة طبيعية/مهام "فهم"؛ مش للحسابات والقواعد الواضحة |
| `uv` | أداة واحدة للـ Python versions + venvs + packages، سريعة وبـ lockfile |
| `.env` | ملف secrets محلي، متجاهَل في git، بيتقري بـ `python-dotenv` |
| API key | باسورد بيتحسب عليه الاستهلاك — عمره ما يدخل الكود أو الـ git |
| `messages.create` | `model` + `max_tokens` + `messages` ← `content` + `stop_reason` + `usage` |
| `stop_reason` | اتأكد منه قبل ما تقرا الـ `content` |

**أوامر مهمة:**
```bash
uv init app && cd app && uv add anthropic python-dotenv && uv run main.py
cp .env.example .env
git check-ignore -v .env
```

## 📚 مصادر إضافية
- [Anthropic — Get started with Claude](https://docs.anthropic.com/en/docs/get-started)
- [Anthropic — Models overview](https://docs.anthropic.com/en/docs/about-claude/models)
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (مقدمة ممتازة لطريقة تفكير الـ AI Engineer)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [uv documentation](https://docs.astral.sh/uv/)
- [Chip Huyen — *AI Engineering* (O'Reilly, 2025)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) — Chapter 1 بالذات
- [Latent Space — The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer)

## ✅ Checklist
- [ ] أقدر أشرح الفرق بين AI Engineer و ML Engineer و Data Scientist في دقيقة
- [ ] أقدر أرسم الـ anatomy بتاعة AI app من الذاكرة
- [ ] سطّبت `uv` وعملت مشروع بـ `uv init` / `uv add`
- [ ] عندي API key في `.env` و `check_env.py` كله ✅
- [ ] شغّلت `hello_claude.py` وفهمت `content` و `stop_reason` و `usage`
- [ ] شغّلت `ai_app_anatomy.py` بالـ mock وبالـ API الحقيقي
- [ ] حليت التمارين
