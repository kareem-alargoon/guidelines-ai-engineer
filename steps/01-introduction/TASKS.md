# Step 01 — التاسكات

> **إنت اللي بتكتب الكود.** الملف ده فيه المطلوب بس، من غير حلول.
> لو وقفت: اطلب **تلميح** (مش حل)، وهتاخد تلميحات متدرّجة.
> التاسكات بتمرّنك على حاجتين في نفس الوقت: **concepts الخطوة** و **Python**.

| Task | الـ Concept | مهارة Python | يعتمد على الشرح؟ |
|---|---|---|:---:|
| 0 — تجهيز البيئة | local LLM | venv، pip | لأ |
| 1 — LLM client | الـ LLM = HTTP API | `httpx`، exceptions، env vars، type hints | لأ |
| 2 — نتيجة منظّمة | tokens و latency | `dataclass` | لأ |
| 3 — Chat CLI | **stateless** + الـ context بيكبر | loops، lists، `input()` | Karpathy |
| 4 — تجربة الـ hallucination | **hallucination** + probabilistic | `json`، `pathlib`، `datetime` | Karpathy |
| 5 — داتا الشركة | الموديل ميعرفش داتاك ← context | قراية ملفات، f-strings | Ch.1 |
| 6 — تقييم فكرة AI app | use case evaluation | — (كتابة) | Ch.1 |

---

## 🌿 قبل ما تبدأ
بعد ما PR مواد الخطوة يتعمله merge:
```bash
git checkout main          # روح على main
git pull                   # هات آخر نسخة من GitHub
git checkout -b work/01-introduction   # اعمل branch جديد لشغلك (زي feature branch)
```
كل الكود بتاعك في `steps/01-introduction/work/`.

---

## Task 0 — تجهيز البيئة
**الهدف:** تشغّل موديل على جهازك، وتجهّز Python environment معزول للخطوة.

**المطلوب:**
1. سطّب **Ollama** من [ollama.com/download](https://ollama.com/download). على Windows و macOS هو برنامج عادي بيفضل شغّال في الخلفية.
2. نزّل موديل وجرّبه:
   ```bash
   ollama pull qwen2.5:3b   # نزّل الموديل (~2GB). ده زي composer require بس لموديل
   ollama run qwen2.5:3b    # افتح chat معاه في الـ terminal. اكتب /bye للخروج
   ollama list              # اعرض الموديلات اللي عندك
   ```
   > لو جهازك 16GB RAM أو أكتر جرّب كمان `qwen2.5:7b`، هتلاحظ الفرق في الذكاء.
3. اعمل virtual environment جوه `work/`:
   ```bash
   cd steps/01-introduction/work
   python -m venv .venv                 # اعمل environment معزول (زي vendor/ بس للـ Python نفسه كمان)
   source .venv/bin/activate            # فعّله (Windows: .venv\Scripts\activate)
   pip install httpx                    # سطّب httpx جواه
   pip freeze > requirements.txt        # سجّل النسخ (زي composer.lock)
   ```

**✅ شروط القبول:**
- [ ] `ollama run qwen2.5:3b` بيرد عليك.
- [ ] فيه `work/requirements.txt`، و `.venv/` **مش** مرفوع على git (اتأكد إنه في `.gitignore` بتاع الريبو).

---

## Task 1 — LLM client
**الهدف:** تفهم إن الموديل الـ local مجرد **HTTP API** على `localhost:11434`، وتكتب client ليه بإيدك.

**المطلوب:** ملف `work/llm_client.py` فيه function بتبعت محادثة لـ Ollama (endpoint اسمه `/api/chat`) وترجّع رد الموديل كنص.

**الـ Interface:**
```python
class LLMError(Exception): ...

def chat(messages: list[dict[str, str]], model: str | None = None) -> str: ...
```
- `messages` شكلها: `[{"role": "user", "content": "..."}]`، والـ roles الممكنة: `system` و `user` و `assistant`.
- لو `model` مبعوتش، استخدم الموديل الافتراضي.

**مثال:**
```python
>>> chat([{"role": "user", "content": "قول أهلاً بس"}])
'أهلاً!'
```

**✅ شروط القبول:**
- [ ] الـ URL والموديل الافتراضي بيتقروا من **environment variables** (`OLLAMA_URL` و `OLLAMA_MODEL`) وليهم قيم default. **مفيش حاجة hardcoded جوه الـ function.**
- [ ] بتطلب الرد **مرة واحدة** مش stream (دوّر في docs الـ API على إزاي).
- [ ] فيه **timeout** معقول. أول request بيحمّل الموديل في الـ RAM فبياخد وقت.
- [ ] لو Ollama **مش شغّال**: ترمي `LLMError` برسالة واضحة بتقول تعمل إيه، مش traceback بتاع `httpx`.
- [ ] لو الموديل **مش متنزّل**: ترمي `LLMError` برسالة فيها الأمر اللي ينزّله. **جرّب بنفسك** تبعت اسم موديل غلط وشوف Ollama بيرجّع إيه (status code و body) قبل ما تكتب الـ handling.
- [ ] الـ function **مبتطبعش حاجة** (`print`)، بترجّع بس. الطباعة مسؤولية اللي بيناديها.
- [ ] Type hints على كل حاجة.
- [ ] في آخر الملف `if __name__ == "__main__":` بيجرّب الـ function بسؤال واحد.

**📚 هيساعدك:**
- [httpx — QuickStart](https://www.python-httpx.org/quickstart/): شبه `Http::post()` في Laravel
- [Ollama API docs](https://docs.ollama.com/api): ابحث عن *Generate a chat completion*
- [`os.environ.get`](https://docs.python.org/3/library/os.html#os.environ)
- [Python — User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions)

---

## Task 2 — نتيجة منظّمة بدل string
**الهدف:** تشوف إن كل request ليه **تكلفة**: عدد tokens داخلة وخارجة، ووقت.

**المطلوب:** عدّل `llm_client.py` بحيث `chat()` ترجّع object بدل string.

**الـ Interface:**
```python
@dataclass
class ChatResult:
    text: str
    input_tokens: int
    output_tokens: int
    duration_seconds: float
```

**✅ شروط القبول:**
- [ ] الأرقام جاية من **response بتاع Ollama نفسه**، مش محسوبة بإيدك. دوّر في الـ docs على الحقول اللي فيها عدد الـ tokens والوقت، وخد بالك من **وحدة** الوقت اللي Ollama بيرجّعها.
- [ ] الـ `__main__` بيطبع الرد + سطر زي: `in: 25 tokens | out: 48 tokens | 1.83s`
- [ ] جرّب سؤال قصير وسؤال بيطلب إجابة طويلة. الأرقام بتتغيّر إزاي؟ اكتب ملاحظتك كـ comment في الـ PR.

**📚 هيساعدك:** [dataclasses](https://docs.python.org/3/library/dataclasses.html): شبه DTO في Laravel/Java

---

## Task 3 — Chat CLI بذاكرة
> 📖 بعد ما تخلّص شرح فيديو Karpathy.

**الهدف:** تشوف بعينك إن الموديل **stateless**، وإن الـ "ذاكرة" هي إنك بتبعت المحادثة كلها كل مرة، فالـ tokens بتكبر مع كل رسالة.

**المطلوب:** `work/chat_cli.py`: برنامج chat في الـ terminal بيستخدم `llm_client.py`.

**✅ شروط القبول:**
- [ ] loop بيقرا رسالة من المستخدم، يبعتها، ويطبع الرد.
- [ ] بيحتفظ بالمحادثة (رسايلك **وردود الموديل**)، فالموديل "يفتكر" اللي اتقال.
- [ ] بعد كل رد بيطبع `input_tokens`. لازم تلاحظ إنها **بتزيد** مع كل رسالة.
- [ ] أوامر: `/reset` (يمسح الذاكرة)، `/history` (يعرض المحادثة)، `/exit` (يخرج).
- [ ] `Ctrl+C` يخرّج بشكل نضيف من غير traceback.
- [ ] **تجربة:** قوله "اسمي كريم" وبعدين "اسمي إيه؟". بعدها اعمل `/reset` واسأل تاني. اكتب اللي حصل وليه في الـ PR.

---

## Task 4 — تجربة الـ Hallucination
> 📖 بعد ما تخلّص شرح فيديو Karpathy.

**الهدف:** تقيس بنفسك إن الموديل **probabilistic** وإنه **بيألّف** لما ميعرفش.

**المطلوب:** `work/experiments/hallucination.py` بيسأل الموديل مجموعة أسئلة، كل سؤال كذا مرة، ويحفظ النتايج.

**✅ شروط القبول:**
- [ ] 6 أسئلة على الأقل في list: **3 عن حاجات حقيقية** (مثلاً "مين مؤلف رواية الحرافيش؟") و **3 عن حاجات وهمية مخترعة** (كتاب، أو شخص، أو شركة).
- [ ] كل سؤال بيتسأل **3 مرات**.
- [ ] النتايج بتتحفظ في `work/experiments/results/hallucination.json`، وفيها لكل إجابة: السؤال، ورقم المحاولة، والرد، والـ tokens، والوقت، وتاريخ التشغيل.
- [ ] الـ JSON بيتحفظ **بالعربي مقروء** (مش `ا...`).
- [ ] فولدر `results/` بيتعمل أوتوماتيك لو مش موجود.
- [ ] ملف `work/experiments/observations.md` تكتب فيه بإيدك: الإجابات على نفس السؤال اتغيّرت؟ الموديل ألّف في الأسئلة الوهمية؟ ولا قال "معرفش"؟ وليه ده بيحصل (اربطه بشرح Karpathy).

**📚 هيساعدك:** [`json.dump`](https://docs.python.org/3/library/json.html#json.dump) (دوّر على `ensure_ascii`)، [`pathlib`](https://docs.python.org/3/library/pathlib.html)، [`datetime`](https://docs.python.org/3/library/datetime.html)

---

## Task 5 — الموديل وداتا الشركة
> 📖 بعد ما تخلّص شرح الفصل الأول.

**الهدف:** تشوف إن الموديل **ميعرفش داتا شركتك**، وإنك لما تحطها في الـ context بيجاوب منها. دي أبسط صورة للفكرة اللي الـ RAG مبني عليها (Step 09).

**المطلوب:**
1. `work/data/company_policy.md`: اكتب بإيدك سياسة موظفين **لشركة وهمية** (8 بنود على الأقل: إجازات، شغل من البيت، مرتبات، ...).
2. `work/experiments/company_context.py`: يسأل نفس الأسئلة مرتين، مرة **من غير** المستند ومرة **مع** المستند في الـ `system` message.

**✅ شروط القبول:**
- [ ] 4 أسئلة على الأقل: 3 إجابتهم **في** المستند، و**واحد إجابته مش موجودة فيه**.
- [ ] المستند بيتقري من الملف، مش مكتوب جوه الكود.
- [ ] الـ system prompt بيطلب من الموديل يجاوب **من المستند بس**، ويقول إنه مش عارف لو الإجابة مش فيه.
- [ ] الـ output واضح: لكل سؤال، الرد من غير مستند جنب الرد مع المستند.
- [ ] كمّل `observations.md`: الموديل التزم بالمستند؟ في السؤال اللي مش في المستند ألّف ولا اعترف إنه مش عارف؟ جرّب موديل تاني (`qwen2.5:7b` مثلاً) لو تقدر وقارن.

---

## Task 6 — قيّم فكرة AI app من شغلك
> 📖 بعد ما تخلّص شرح الفصل الأول (الجزء بتاع *Planning AI Applications*).

**الهدف:** تطبّق طريقة تفكير الكتاب في تقييم الـ use case على حاجة حقيقية.

**المطلوب:** `work/use_case.md`: اختار فكرة واحدة لـ feature بـ AI في مشروع Laravel اشتغلت عليه أو تعرفه، وحلّلها **بالـ framework اللي في الفصل الأول**: ليه تعملها، ودور الـ AI فيها إيه، وإزاي تقيس نجاحها، والمخاطر، وتبدأ بإيه.

**✅ شروط القبول:**
- [ ] كل نقطة مربوطة بجزء من الفصل (اذكر الـ section).
- [ ] فيه قرار واضح: تنفع ولا لأ، وليه. ولو تنفع: cloud ولا local، وليه.

---

## 📤 التسليم
1. اعمل commit بعد كل task لوحده، بـ message واضحة (مثال: `work 01: task 1 llm client`).
2. `git push -u origin work/01-introduction`
3. افتح PR على `main`، واكتب فيه عملت إيه، واللي مش متأكد منه، وملاحظاتك من التجارب.
4. تقدر تفتح الـ PR بعد أول task وتكمّل عليه. هراجع كل push.
