# شرح: Ollama docs (10 صفحات)

> **المصدر:** [Ollama documentation](https://docs.ollama.com/) — النسخة اللي اتحفظت يوم 2026-11-13
> **الملفات:** `resources/articles/03-ollama-*.pdf` (10 ملفات)
> **إزاي تقرا:** الصفحات هنا **بترتيب القراية**، مش بترتيب الموقع. افتح كل PDF جنب الجزء بتاعه. الـ 📍 بيقولك اسم الملف ورقم الصفحة جوه الـ PDF.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

إنت بتستخدم Ollama من Step 01، بس كـ "صندوق أسود": `ollama pull`، وبعدين `POST /api/chat`. في Step 03 السؤال بقى: **إزاي تشغّل موديلات open weight على جهازك صح؟** يعني:
- الموديل متخزّن فين، وبياخد RAM قد إيه، وشغّال على الـ GPU ولا الـ CPU؟
- ليه أول request دايماً بطيء؟
- إزاي تعمل "نسخة" من موديل بإعداداتك (system prompt، و `num_ctx`، و temperature)؟
- إزاي تكلّم Ollama بنفس الكود اللي بتكلّم بيه OpenAI؟ (ده "الـ standard API" اللي الكتاب نصح بيه.)
- وإيه حكاية **Ollama Cloud**؟ إزاي أداة "local" بقت بتقدّم موديلات cloud كمان؟

| # | الصفحة | الملف | أهميتها ليك |
|:---:|---|---|:---:|
| 1 | Quickstart | `03-ollama-quickstart.pdf` | ⭐⭐ |
| 2 | Windows | `03-ollama-windows.pdf` | ⭐⭐⭐ (جهازك Windows) |
| 3 | CLI Reference | `03-ollama-cli-reference.pdf` | ⭐⭐⭐ |
| 4 | Local FAQ | `03-ollama-faq.pdf` | ⭐⭐⭐⭐ **(أهم صفحة)** |
| 5 | Context length | `03-ollama-context-length.pdf` | ⭐⭐⭐ |
| 6 | Hardware support | `03-ollama-hardware-support.pdf` | ⭐⭐ |
| 7 | Modelfile Reference | `03-ollama-modelfile.pdf` | ⭐⭐⭐⭐ |
| 8 | Importing a Model | `03-ollama-importing-a-model.pdf` | ⭐⭐ |
| 9 | OpenAI compatibility | `03-ollama-openai-compatibility.pdf` | ⭐⭐⭐⭐ |
| 10 | Cloud | `03-ollama-cloud.pdf` | ⭐⭐⭐ |

> ⏳ **عمر المصدر:** الـ docs دي "حية" وبتتغيّر كل كام أسبوع (فيها features مكتوب جنبها "Added in v0.40.x"). اللي هنا صح يوم 2026-11-13. لو حاجة مش شغالة عندك، أول حاجة: `ollama --version`، وحدّث Ollama.

**الصورة الكبيرة قبل ما تبدأ:** Ollama فيه حاجتين:
1. **Server** (اسمه الـ daemon) شغّال في الخلفية على `http://localhost:11434`. ده الـ **inference service** اللي الكتاب اتكلم عنه: بيحمّل الموديل في الـ memory ويشغّله.
2. **CLI** (`ollama ...`) و **app**. دول مجرد **clients** بيكلّموا الـ server نفسه.

**تشبيه من Laravel:** زي **MySQL**: فيه `mysqld` (الـ server شغّال في الخلفية على port 3306)، وفيه `mysql` CLI و TablePlus و Laravel نفسه، وكلهم clients بيكلّموا نفس الـ server. Ollama نفس الشكل بالظبط، بس الـ port هو 11434، وبدل الجداول فيه موديلات.

---

## 1. Quickstart
> 📍 `03-ollama-quickstart.pdf` ص 1–4

**الفكرة:** الصفحة بتقسم استخدام Ollama لـ 3 طرق:

**1) Get started (ص 1):** نزّل Ollama، وافتح الـ app أو اكتب `ollama` في الـ terminal، واتبع الخطوات. وفيه حاجة جديدة: بيسألك **تعمل sign in عشان تستخدم cloud models، ولا تختار موديل local**. (هنرجع للـ cloud في جزء 10.)

**2) Connect a desktop app / Use a coding agent (ص 1–2):**
- على macOS تقدر توصّل Claude Desktop أو ChatGPT Desktop بموديلات Ollama.
- `ollama launch claude` بيشغّل **Claude Code** (أو Codex أو OpenCode) بس على **موديل من Ollama** بدل موديل الشركة. Ollama بيعرض يسطّبه لو مش موجود.

ده مثال عملي على كلام الكتاب: الأداة (Claude Code) والموديل (اللي بيفكّر) **حاجتين منفصلين**، وتقدر تبدّل الموديل. وده ممكن عشان Ollama بيقدّم API **شبه** API بتاع Anthropic (جزء 9).

**3) Build an application (ص 2–4):** ده اللي يهمنا:
- **Cloud:** تعمل **API key** من حسابك على ollama.com، وتحطه في environment variable اسمه `OLLAMA_API_KEY`، وتبعت للـ URL `https://ollama.com/api/chat` مع header `Authorization: Bearer ...`. **ومش محتاج تسطّب Ollama أصلاً.**
- **Local:** من غير key، على `http://localhost:11434`.
- والـ request نفسه **نفس الشكل** في الحالتين: `model` و `messages` و `stream`، وبتقرا الرد من `message.content`. (نفس اللي بتعمله في `llm_client.py` بالظبط.)
- وفيه tabs لنفس الـ request بأشكال تانية: **Ollama API**، و **OpenAI Chat Completions**، و **OpenAI Responses**، و **Anthropic Messages**. وبيقول إن الـ OpenAI والـ Anthropic compatibility كل واحد بيغطي **جزء** (subset) من الـ API الأصلي.

**النصيحة الأمنية (ص 3):** خلّي الـ key **على السيرفر بتاع التطبيق**، مش في كود الـ browser، ومش في الـ source control. (ده نفس كلام CLAUDE.md بتاعنا: `.env` و `.gitignore`.)

**ص 4:** `ollama run <model>` بينزّل الموديل لو مش موجود ويفتح chat. `/bye` عشان تخرج.

**تشبيه من Laravel:** Local مقابل Cloud هنا زي `DB_HOST=127.0.0.1` مقابل `DB_HOST=my-db.rds.amazonaws.com` مع `DB_PASSWORD`. نفس الـ driver، ونفس الـ queries، بس **مكان** مختلف و **credentials** مختلفة. الفرق المهم: في الحالة التانية **داتاك بتسافر** لسيرفر حد تاني (hard attribute من الكتاب!).

> ⚠️ **أسماء الموديلات في الـ docs:** الأمثلة فيها `gemma4:31b` و `gemma4:e2b` و `qwen3.5` وغيرهم. **متنزّلش حاجة لمجرد إنها في المثال**: كل موديل بأحجام مختلفة، وفيه اللي محتاج RAM كتير. قبل أي `pull` بص على حجمه في [ollama.com/library](https://ollama.com/library).

---

## 2. Windows
> 📍 `03-ollama-windows.pdf` ص 1–4

**الفكرة (ص 1):** Ollama على Windows **app عادي** (native) بيدعم كروت NVIDIA و AMD Radeon. بعد التسطيب، **بيشتغل في الخلفية** لوحده (الأيقونة في الـ tray جنب الساعة)، والـ `ollama` command شغّال من cmd أو PowerShell أو أي terminal، والـ API على `http://localhost:11434` كالعادة.

**System requirements:** Windows 10 22H2 أو أحدث، و driver NVIDIA 551.61+ لو عندك NVIDIA، و AMD ROCm v7 أو Vulkan لو AMD.

**ملحوظة صغيرة:** Ollama بيستخدم رموز unicode في الـ progress bar، فممكن تظهر مربعات في fonts قديمة على Windows 10.

**Filesystem (ص 2) ⭐ مهم ليك:**
- التسطيب **مش محتاج Administrator**، وبيتسطّب في الـ home directory.
- محتاج **4GB على الأقل** للبرنامج نفسه، **وكمان** مساحة للموديلات، وده ممكن يبقى **عشرات أو مئات الجيجات**.
- **تغيير مكان التسطيب:** `OllamaSetup.exe /DIR="d:\some\location"`.
- **تغيير مكان الموديلات:** environment variable اسمه **`OLLAMA_MODELS`** في حساب المستخدم:
  1. افتح Settings وابحث عن *environment variables*.
  2. *Edit environment variables for your account*.
  3. اعمل variable جديد `OLLAMA_MODELS` بالمسار اللي عايزه.
  4. OK/Apply.
  5. **مهم:** اقفل Ollama من الـ tray وافتحه تاني من الـ Start menu (أو terminal جديد)، لأن البرامج بتقرا الـ environment variables وقت ما بتفتح بس.

**ليك:** الريبو بتاعك على `D:`، فلو `C:` ضيق والموديلات كبرت، `OLLAMA_MODELS=D:\ollama-models` بيحل المشكلة.

**تشبيه:** ده بالظبط زي `.env` في Laravel: لو غيّرت `.env` والـ server شغّال، لازم تعمل restart أو `php artisan config:clear`، عشان القيم بتتقري مرة واحدة في الأول.

**Troubleshooting (ص 3) ⭐ احفظ الأماكن دي:** (اكتبها في `Win+R`)

| المسار | فيه إيه |
|---|---|
| `%LOCALAPPDATA%\Ollama` | اللوجات: **`server.log`** (لوجات الـ server، أهم ملف)، و `app.log`، و `upgrade.log` |
| `%LOCALAPPDATA%\Programs\Ollama` | البرنامج نفسه (والـ installer بيضيفه للـ PATH) |
| `%HOMEPATH%\.ollama` | **الموديلات** والإعدادات |
| `%TEMP%` | ملفات مؤقتة في فولدرات `ollama*` |

**تشبيه:** `server.log` هو `storage/logs/laravel.log` بتاع Ollama. لو حاجة غريبة حصلت (الموديل مش بيحمّل، أو الرد بطيء جداً)، أول مكان تبص فيه.

**Uninstall:** من *Add or remove programs*. ولو غيّرت `OLLAMA_MODELS`، الموديلات **مش هتتمسح**، لازم تمسحها بإيدك.

**Standalone CLI (ص 3–4):** فيه zip فيه الـ CLI بس (`ollama-windows-amd64.zip`)، لو عايز تشغّل Ollama **كـ service** (مثلاً بـ NSSM) أو تحطه جوه تطبيق. ده للـ servers، مش لجهازك.

---

## 3. CLI Reference
> 📍 `03-ollama-cli-reference.pdf` ص 1–5

**الأوامر الأساسية** (اللي هتستخدمها كل يوم):

| الأمر | بيعمل إيه | المقابل اللي تعرفه |
|---|---|---|
| `ollama run gemma4` | يشغّل chat (وينزّل الموديل لو مش موجود) | `php artisan tinker` |
| `ollama pull gemma4` | ينزّل موديل | `composer require` |
| `ollama rm gemma4` | يمسح موديل | `composer remove` |
| `ollama ls` | يعرض الموديلات اللي عندك وأحجامها | `composer show` |
| `ollama ps` | يعرض الموديلات **المحمّلة في الـ memory دلوقتي** | `ps` / Task Manager |
| `ollama stop gemma4` | يشيل موديل من الـ memory (مش بيمسحه) | — |
| `ollama serve` | يشغّل الـ server بنفسك (على Windows الـ app بيعمله لوحده) | `php artisan serve` |
| `ollama create -f Modelfile` | يعمل موديل مخصص من Modelfile (جزء 7) | `docker build` |
| `ollama signin` / `signout` | دخول/خروج من حسابك على ollama.com (للـ cloud) | — |
| `ollama launch` | يجهّز ويشغّل integrations (Claude Code، Codex، VS Code...) | — |

**الفرق المهم بين `ls` و `ps`:** `ls` = الموديلات **على الـ disk**. `ps` = الموديلات **في الـ RAM/VRAM دلوقتي**. الموديل ممكن يبقى منزّل بس مش محمّل (أول request هيستنى التحميل).

**حاجات تانية في الصفحة:**
- **Multiline input** (ص 2): في `ollama run` تقدر تكتب أكتر من سطر بإنك تحطهم بين `"""`.
- **Multimodal** (ص 2): تحط مسار صورة جوه الـ prompt لموديل بيدعم الصور (Step 13).
- **Embeddings** (ص 2–3): `ollama run embeddinggemma "Hello world"` بيطلّع **array أرقام** بدل نص. ده الـ embedding اللي هنشرحه في Step 07.
- **Decision models** (ص 3): ⏳ حاجة جديدة: موديلات صغيرة مخصوص لأسئلة "آه/لأ" أو "اختار من دول" (`--ask` و `--choice` و `--level`). مثال: "العميل ده عايز refund؟"، "التذكرة دي تروح لأنهي team؟". ده **classification** متغلّف في أمر جاهز.
- **Speech** (ص 3): موديلات بتحوّل نص لصوت.
- **`ollama serve --help`** (ص 5): بيعرض **كل الـ environment variables** اللي ينفع تظبط بيها الـ server. مفيد جداً.

> 💡 **أمر مش في الصفحة دي بس هتحتاجه:** `ollama show <model>` بيعرض معلومات الموديل (الـ architecture، وعدد الـ parameters، والـ context length، والـ quantization، والـ capabilities، والـ license). وفيه flags زي `--modelfile` (هيتذكر في جزء 7) و `--license`. شوف كل الـ flags بـ `ollama show --help`. هتستخدمه كتير في التاسكات.

---

## 4. Local FAQ
> 📍 `03-ollama-faq.pdf` ص 1–15
> دي أطول وأهم صفحة. هنمشي على الأسئلة بالترتيب، ونطوّل في اللي يهمك.

### 4.1 Upgrade و logs و GPU (ص 1)
- على Windows و macOS، Ollama **بينزّل التحديثات لوحده**. تدوس على الأيقونة وتختار *Restart to update*.
- اللوجات: صفحة Troubleshooting (والأماكن في جزء 2).
- الـ GPU متوافق ولا لأ: صفحة Hardware (جزء 6).

### 4.2 حجم الـ context window (ص 2) ⭐
- **الـ default 4096 token** (على الأجهزة اللي VRAM بتاعها أقل من 24GB، شوف جزء 5).
- تغيّره **لكل الموديلات** وقت تشغيل الـ server: `OLLAMA_CONTEXT_LENGTH=8192`.
- جوه `ollama run`: `/set parameter num_ctx 4096`.
- من الـ API: `"options": {"num_ctx": 4096}`. **وده اللي عملته بالظبط** في Step 02 Task 7 (`context_size` في `llm_client.py`).

**ربط بـ Step 02:** فاكر لما Ollama **شال رسالة الاسم بصمت** في Task 7؟ ده كان بسبب الـ `num_ctx` الصغير. هنا بقيت عارف إن الـ default نفسه صغير (4K)، وإن موديل `qwen2.5:3b` نفسه **يقدر** على context أكبر بكتير (هتشوف الرقم في `ollama show`)، بس Ollama **مش بيدّيه ده تلقائي** عشان يوفّر memory.

### 4.3 الموديل على الـ GPU ولا الـ CPU؟ (ص 2–3) ⭐⭐
`ollama ps` بيطلّع عمود اسمه **PROCESSOR**:
- `100% GPU` = الموديل كله في الـ VRAM (**أسرع حاجة**).
- `100% CPU` = الموديل كله في الـ RAM العادية (أبطأ بكتير).
- `48%/52% CPU/GPU` = **جزء هنا وجزء هنا** (اسمها **offloading**)، لأن الـ VRAM مكفّتش. وده غالباً **أبطأ بكتير** من الـ GPU لوحده.

**ليه ده مهم؟** ده بيفسّر ليه موديل **أكبر شوية** ممكن يبقى **أبطأ بشكل كبير** مش "شوية": أول ما يعدّي الـ VRAM ويتقسم، السرعة بتقع. فقبل ما تنزّل موديل أكبر، اسأل: **هيدخل كله في الـ VRAM؟** (ولو جهازك مفيهوش GPU مناسب، كل حاجة بتتحسب على الـ CPU والـ RAM.)

### 4.4 إعداد الـ server بالـ environment variables (ص 3–4)
Ollama بيتظبط كله بـ **environment variables**. على Windows:
1. اقفل Ollama من الـ taskbar.
2. Settings ← ابحث عن *environment variables* ← *Edit environment variables for your account*.
3. ضيف/عدّل (`OLLAMA_HOST`، `OLLAMA_MODELS`...).
4. OK/Apply.
5. افتح Ollama من الـ Start menu.

(وعلى Mac بـ `launchctl setenv`، وعلى Linux بـ `systemctl edit ollama.service`.)

**تشبيه:** Ollama ملوش `config/*.php`، كل الـ config **في الـ environment** (فلسفة الـ [Twelve-Factor App](https://12factor.net/config)، نفس فكرة `.env` في Laravel).

### 4.5 Proxy (ص 4–5)
لو شغّال ورا proxy (شائع في الشركات): استخدم **`HTTPS_PROXY`** بس، و**متستخدمش `HTTP_PROXY`** لأنه ممكن يبوّظ اتصال الـ clients بالـ server. ولازم شهادة الـ proxy تبقى متسطّبة في الـ system. **ليك:** لو Ollama على لاب الشركة مبيعرفش ينزّل موديلات، غالباً ده السبب.

### 4.6 هل Ollama بيبعت الـ prompts لـ ollama.com؟ (ص 5–6) ⭐⭐⭐
ده أهم سؤال **ليك** (الداتا الحساسة):
- **Local:** بيقولوا إنهم **مش بيشوفوا** الـ prompts ولا الداتا لما بتشغّل local.
- **Cloud models:** بيعالجوا الـ prompts والردود عشان يقدّموا الخدمة، بس بيقولوا إنهم **مش بيخزّنوها ولا بيعملوا لها log، ومش بيدرّبوا عليها**. وبيجمعوا معلومات الحساب و metadata استخدام محدودة (من غير محتوى).

**إزاي تقرا الكلام ده كـ AI Engineer؟** (من الكتاب، محور الـ privacy): ده **وعد في سياسة**، والسياسات **بتتغيّر** (مثال Zoom). الفرق الحقيقي: في الـ local، الداتا **فيزيائياً** مش بتخرج من جهازك، فمش محتاج تثق في وعد حد. في الـ cloud، إنت **بتثق** في الوعد.

### 4.7 تقفل الـ cloud خالص (ص 6) ⭐⭐
لو عايز Ollama **local بس** (مثلاً على جهاز عليه داتا حساسة، ومحدش يستخدم cloud model بالغلط):
- في `~/.ollama/server.json`: `{"disable_ollama_cloud": true}`
- أو environment variable: **`OLLAMA_NO_CLOUD=1`**

وبعدين restart. واللوج هيقول `Ollama cloud disabled: true`. هتخسر الـ cloud models والـ web search.

**تشبيه:** زي إنك تقفل الـ outbound network على سيرفر الداتابيز: حتى لو حد غلط، مفيش طريق للداتا تخرج.

### 4.8 تفتح Ollama على الشبكة (ص 6–7)
- الـ default: Ollama بيسمع على **`127.0.0.1:11434`**، يعني **جهازك بس**.
- تغيّره بـ `OLLAMA_HOST` (مثلاً `0.0.0.0:11434` عشان أي جهاز على الشبكة).
- وفيه أمثلة: تحطه ورا **Nginx** كـ reverse proxy، أو تفتحه للإنترنت بـ **ngrok** أو **Cloudflare Tunnel**.

> ⚠️ **تحذير مني (مش من الصفحة):** الـ local API بتاع Ollama **مفيهوش authentication**. أي حد يوصل للـ port يقدر يشغّل موديلاتك (ويستهلك جهازك)، ويـ pull ويمسح موديلات. فلو فتحته على `0.0.0.0` أو ngrok، إنت فتحت endpoint من غير password. لو محتاج كده، حطه ورا Nginx فيه auth. (زي إنك متفتحش port 3306 بتاع MySQL على الإنترنت.)

### 4.9 CORS و browser extensions (ص 7–8)
Ollama بيسمح بـ cross-origin requests من `127.0.0.1` و `0.0.0.0` بس. لو عايز صفحة ويب أو browser extension تكلّمه، ضيف الـ origin في **`OLLAMA_ORIGINS`**. (نفس فكرة `config/cors.php` في Laravel.)

### 4.10 الموديلات متخزّنة فين؟ (ص 8)
- Windows: **`C:\Users\%username%\.ollama\models`**
- تغيّره بـ `OLLAMA_MODELS` (جزء 2).

### 4.11 Preload و keep_alive (ص 9–11) ⭐⭐⭐
**ده بيفسّر حاجة شفتها كتير:** ليه أول request **بطيء جداً**، والتاني سريع؟
- عشان الموديل لازم **يتحمّل من الـ disk للـ memory** الأول (ملف بالجيجات).
- **الـ default:** الموديل بيفضل في الـ memory **5 دقايق** بعد آخر استخدام، وبعدين بيتشال.

**تتحكم فيه إزاي؟**
- **Preload:** ابعت request فاضي (من غير messages) لـ `/api/chat` أو `/api/generate`، أو `ollama run llama3.2 ""`. الموديل يتحمّل ويستنى.
- **`keep_alive`** في الـ API request:
  - مدة: `"10m"` أو `"24h"`
  - ثواني: `3600`
  - **رقم سالب** (`-1`): يفضل محمّل **على طول**
  - **`0`**: اشيله **فوراً** بعد الرد
- أو لكل الموديلات: **`OLLAMA_KEEP_ALIVE`** (والـ `keep_alive` في الـ request بيكسب عليه).
- أو `ollama stop <model>` عشان تشيله دلوقتي.

**ربط بالكتاب (Cost and Latency):** ده مثال حقيقي على **trade-off بين الـ latency والـ memory**: لو الموديل محمّل على طول، الـ TTFT واطي، بس الـ RAM محجوزة طول الوقت. ولو بتشيله، بتوفّر RAM بس أول request بيستنى. ودي **الـ cold start** نفسها اللي في الـ serverless (Lambda).

**ربط بكودك:** الـ error message اللي في `llm_client.py` بتاعك ("The model may still be loading") كانت صح بالظبط: الـ timeout في أول request غالباً كان التحميل ده.

### 4.12 الـ queue والـ concurrency (ص 11–12) ⭐⭐
**الـ queue:** لو بعت requests أكتر من اللي Ollama يقدر عليه، بيرد بـ **`503` overloaded**. تكبّر الـ queue بـ `OLLAMA_MAX_QUEUE` (الـ default **512**).

**الـ concurrency على مستويين:**
1. **أكتر من موديل محمّل في نفس الوقت** (لو فيه memory). الـ default: **3 موديلات** (أو 3 × عدد الـ GPUs). لو مفيش memory لموديل جديد، الـ requests بتستنى، وموديل قديم مش مستخدم بيتشال يفضّي مكان.
2. **أكتر من request لنفس الموديل في نفس الوقت**: **`OLLAMA_NUM_PARALLEL`**، والـ **default = 1**.

**النقطة المهمة جداً (ص 12):** الـ parallel requests **بتضرب الـ context في عددها**: لو `num_ctx` = 2K و 4 parallel requests، يبقى فعلياً **8K context** و memory أكتر. يعني الـ RAM المطلوبة بتزيد بـ `OLLAMA_NUM_PARALLEL × OLLAMA_CONTEXT_LENGTH`.

**ليه ده مهم للتطبيقات؟** الـ default إن Ollama بيخدم **request واحد في المرة** للموديل الواحد، والباقي في طابور. فلو عملت تطبيق ويب عليه 10 مستخدمين في نفس الوقت على Ollama عادي، كل واحد هيستنى اللي قبله. ده الفرق بين Ollama (ممتاز للتطوير والاستخدام الشخصي) وأدوات زي **vLLM** للـ production (Step 15). وده بالظبط **محور الـ scalability** في الكتاب.

**تشبيه:** `OLLAMA_NUM_PARALLEL` زي عدد الـ **PHP-FPM workers** (`pm.max_children`)، و `OLLAMA_MAX_QUEUE` زي الـ backlog. worker واحد = request واحد في المرة. وكل worker زيادة بياكل memory.

### 4.13 أكتر من GPU (ص 12)
لو الموديل يدخل في GPU واحد، Ollama بيحطه على واحد (أسرع، عشان الداتا متتنقلش بين الكروت). لو مش داخل، بيوزّعه على الكل.

### 4.14 Flash Attention و KV cache quantization (ص 12–14)
> 🚫 التنفيذ الداخلي برّه النطاق (inference optimization، Ch.9). محتاج تعرف بس إن **فيه زراير** للـ memory.
- **Flash Attention:** طريقة أكفأ لحساب الـ attention بتقلل الـ memory لما الـ context يكبر. Ollama بيشغّلها لوحده لو الـ hardware بيدعم (`OLLAMA_FLASH_ATTENTION=1` تجبره، و `0` تقفله).
- **KV cache quantization:** فاكر الـ **KV cache** من Step 02 (الموديل بيحتفظ بحسابات الـ tokens اللي فاتت عشان ميعيدهاش)؟ ده بياكل memory كتير مع الـ context الطويل. **`OLLAMA_KV_CACHE_TYPE`**:
  - `f16` (الـ default): دقة عالية، memory كتير.
  - `q8_0`: **نص الـ memory** تقريباً، وفقد دقة صغير جداً غالباً مش ملحوظ (**الموصى بيه** لو مش هتستخدم f16).
  - `q4_0`: **ربع الـ memory**، وفقد دقة أوضح خصوصاً مع context طويل.
- وبيقولوا إن موديلات زي **Qwen2** (يعني عيلة موديلك) ممكن تتأثر بالـ quantization ده **أكتر** من غيرها. فلو جربته، اختبر الجودة.

**الدرس:** context أطول = memory أكتر، وفيه طرق تقللها **على حساب الدقة**. نفس فكرة الـ quantization بتاعة الـ weights (Step 01 و 02)، بس على الـ cache.

### 4.15 Public key و startup (ص 14–15)
- **Ollama Public Key** (`C:\Users\<username>\.ollama\id_ed25519.pub`): بيربط جهازك بحسابك على ollama.com، عشان تـ push موديلات، أو تـ pull موديلات private، أو تشغّل cloud models. `ollama signin` بيعملها لوحده.
- لو مش عايز Ollama يفتح مع الـ Windows: Task Manager ← Startup apps ← Disable. (**ليك:** فاكر إن Ollama كتير بيبقى مقفول عندك؟ ده العكس: لو عايزه يفتح دايماً، اتأكد إنه **Enabled** هنا.)

---

## 5. Context length
> 📍 `03-ollama-context-length.pdf` ص 1–3

**التعريف (ص 1):** الـ context length هو **أقصى عدد tokens** الموديل يقدر "يشوفه" في الـ memory.

**الـ default بيعتمد على الـ VRAM:**

| الـ VRAM | الـ default context |
|---|---|
| أقل من 24 GiB | **4K** |
| 24–48 GiB | 32K |
| 48 GiB أو أكتر | 256K |

**النصيحة:** المهام اللي محتاجة context كبير (web search، و **agents**، و coding tools) لازم تبقى **64,000 token على الأقل**. (افتكر ده في Step 10 و 11.)

**التمن:** context أكبر = **memory أكتر**. اتأكد إن عندك VRAM كفاية قبل ما تكبّره. والـ **cloud models** بتشتغل على أقصى context ليها تلقائي.

**إزاي تغيّره (ص 1–2):** من الـ app (slider في الـ settings)، أو `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`، أو `num_ctx` في الـ request (جزء 4.2).

**إزاي تتأكد (ص 2–3):** `ollama ps` فيه عمود **CONTEXT** بيقولك الـ context المحجوز فعلاً، وعمود **PROCESSOR** (جزء 4.3). ونصيحتهم: للأداء الأحسن، استخدم أقصى context للموديل **ومن غير ما يتقسم على الـ CPU**. يعني لو الـ context الكبير خلّى الموديل يعمل offload، إنت خسرت سرعة.

> ⚠️ **تعارض في الـ docs:** صفحة الـ Modelfile (جزء 7) مكتوب فيها إن الـ default بتاع `num_ctx` هو **2048**، والـ FAQ والصفحة دي بيقولوا **4096**. الـ docs نفسها مش متسقة (ده بيحصل في أدوات بتتغيّر بسرعة). **متصدّقش الـ docs، اتأكد**: شغّل موديل وبص على عمود CONTEXT في `ollama ps`. (هتعملها في التاسكات.)

**تشبيه:** الـ context length زي `memory_limit` في `php.ini`: كل ما تكبّره، الـ process تقدر تشيل داتا أكتر، بس بتاخد RAM أكتر. ولو كبّرته أكتر من الـ RAM الفعلية، الجهاز يبدأ يستخدم swap ويبقى بطيء جداً (ده الـ CPU offloading هنا).

---

## 6. Hardware support
> 📍 `03-ollama-hardware-support.pdf` ص 1–7

**الفكرة:** Ollama بيشتغل على الـ CPU دايماً، بس **أسرع بكتير** على GPU متوافق. الصفحة بتقولك أنهي GPUs متوافقة:

- **NVIDIA (ص 1–2):** محتاج **compute capability 5.0+** و driver **550+** (والكروت من 5.0 لـ 6.2 محتاجة driver 570+). الجدول فيه من RTX 50xx لحد GTX 750. اعرف الـ compute capability بتاعة كارتك من موقع NVIDIA.
- **AMD Radeon (ص 3–5):** عن طريق **ROCm v7** (على Windows قايمة كروت أقصر من Linux)، وفيه طرق "تخدع" بيها ROCm لكروت مش مدعومة على Linux (`HSA_OVERRIDE_GFX_VERSION`).
- **Apple (ص 6):** عن طريق **Metal**.
- **Vulkan (ص 6–7):** دعم إضافي لكروت كتير على Windows و Linux، وشغّال by default. وعلى Windows أغلب الـ drivers فيها Vulkan جاهز.

**GPU selection (ص 3، 5، 6–7):** لو عندك أكتر من GPU، تختار بـ `CUDA_VISIBLE_DEVICES` (NVIDIA) أو `ROCR_VISIBLE_DEVICES` (AMD) أو `GGML_VK_VISIBLE_DEVICES` (Vulkan). و**لو عايز تجبر Ollama يستخدم الـ CPU بس**، ادّيله ID غلط زي **`-1`**. (ده مفيد للتجربة: تقيس الفرق بين GPU و CPU على نفس الموديل.) وعلى الأجهزة اللي فيها GPU مدمج (iGPU) و GPU منفصل (dGPU)، ممكن تحتاج تحدد المنفصل.

**ليك عملياً:** اعرف جهازك فيه إيه:
- Task Manager ← Performance ← GPU: هتشوف اسم الكارت و **Dedicated GPU memory** (ده الـ VRAM).
- لو مفيش GPU منفصل (لاب عادي بـ Intel/AMD مدمج)، الموديل غالباً هيشتغل على الـ CPU أو Vulkan، والـ RAM العادية هي اللي هتحدد أكبر موديل.
- وبعد ما تشغّل موديل: `ollama ps` ← عمود PROCESSOR هيقولك الحقيقة.

> 🚫 الـ drivers والـ ROCm overrides والـ SELinux: شغل DevOps، مش محتاجه دلوقتي. المهم تعرف **تسأل**: الموديل شغّال على إيه؟

---

## 7. Modelfile Reference
> 📍 `03-ollama-modelfile.pdf` ص 1–10

**الفكرة (ص 1):** الـ **Modelfile** هو **الـ blueprint** اللي بتعمل بيه موديل "مخصص" وتشاركه.

**تشبيه من Laravel/Docker (أدق تشبيه):** الـ Modelfile هو **`Dockerfile`** بتاع الموديلات:
```
# Dockerfile                    # Modelfile
FROM php:8.3-fpm                FROM qwen2.5:3b
ENV APP_ENV=production          PARAMETER temperature 0.2
COPY . /var/www                 SYSTEM """You are a support agent..."""
docker build -t myapp .         ollama create support-bot -f Modelfile
docker run myapp                ollama run support-bot
```
ومهم: `ollama create` **مش بينسخ الـ weights** ولا بيدرّب حاجة. بيعمل "طبقة" فوق الموديل الأصلي فيها إعداداتك. 🚫 **ده مش finetuning**: الموديل نفسه هو هو، إنت بس ثبّت الـ system prompt والـ parameters.

### 7.1 الـ Format والـ instructions (ص 2)
كل سطر `INSTRUCTION arguments`، والـ `#` comment:

| Instruction | بيعمل إيه |
|---|---|
| **`FROM`** (إجباري) | الموديل الأساسي |
| **`PARAMETER`** | إعدادات التشغيل (temperature، num_ctx...) |
| **`TEMPLATE`** | الـ prompt template الكامل اللي بيتبعت للموديل |
| **`SYSTEM`** | الـ system message |
| **`LICENSE`** | الـ license |
| **`MESSAGE`** | تاريخ محادثة جاهز |
| **`REQUIRES`** | أقل version من Ollama |
| **`CAPABILITY`** | قدرة إضافية للموديل |

### 7.2 المثال: Mario (ص 2–3)
موديل `llama3.2` بـ temperature 1، و `num_ctx` 4096، و system message "إنت Mario". تحفظه كـ `Modelfile`، و `ollama create <name> -f ./Modelfile`، و `ollama run <name>`.

**`ollama show --modelfile llama3.2` (ص 3):** بيوريك الـ Modelfile بتاع أي موديل موجود. وهتلاقي فيه حاجة مهمة:
- `FROM` بيشاور على **blob** (ملف الـ weights بالـ hash بتاعه في `.ollama/models/blobs`).
- **`TEMPLATE`** فيه **special tokens** زي `<|start_header_id|>` و `<|eot_id|>`.
- **`PARAMETER stop`** على الـ special tokens دي.

**ربط بـ Step 02 (Karpathy):** ده بالظبط **الـ conversation protocol** اللي Karpathy شرحه: الـ chat مش "رسايل" جوه الموديل، ده **نص واحد طويل** فيه tokens خاصة بتفصل الـ system عن الـ user عن الـ assistant. والـ TEMPLATE هو اللي بيحوّل الـ `messages` بتاعتك للنص ده. وكل عيلة موديلات ليها format مختلف (Llama بـ `<|start_header_id|>`، و Qwen بـ `<|im_start|>`). وده اللي بيخلّي الـ stop reason `stop` لما الموديل يطلّع `<|eot_id|>`.

### 7.3 FROM (ص 3–4)
3 أشكال: من موديل موجود (`FROM llama3.2`)، أو من فولدر **Safetensors**، أو من ملف **GGUF** (جزء 8).

### 7.4 PARAMETER والـ defaults (ص 4–7) ⭐⭐
ده الجدول اللي يهمك، لأنه فيه **الـ defaults** اللي Ollama بيستخدمها لو مبعتش حاجة:

| Parameter | بيعمل إيه | الـ Default في الجدول | تعرفه من |
|---|---|---|---|
| `num_ctx` | حجم الـ context | 2048 ⚠️ (شوف التعارض في جزء 5) | Step 02 Task 7 |
| `repeat_last_n` | يبص ورا قد إيه عشان يمنع التكرار | 64 (`0` = مقفول، `-1` = `num_ctx`) | جديد |
| `repeat_penalty` | قد إيه يعاقب التكرار (1.5 قوي، 0.9 متساهل) | 1.0 (مقفول) | جديد |
| `temperature` | العشوائية | **0.8** | Step 02 Task 3 |
| `seed` | تثبيت العشوائية | 0 | Step 02 Task 3 |
| `stop` | stop sequences (تقدر تحط أكتر من واحد) | — | Step 02 Task 4 |
| `num_predict` | أقصى tokens يطلّعها | **-1 (لانهائي)** | Step 02 (`max_tokens`) |
| `draft_num_predict` | للـ speculative decoding | 4 | 🚫 Ch.9 |
| `top_k` | | **40** | Step 02 |
| `top_p` | | **0.9** | Step 02 |
| `min_p` | | 0.0 | Step 02 |

**ملاحظات:**
- **`temperature` الـ default 0.8** مش 0! يعني لو مبعتش temperature، الموديل **عشوائي** by default. (ده اللي خلّى ردودك تختلف في Step 02.)
- **`num_predict` = -1** يعني مفيش حد. لو الموديل "دخل في loop" ممكن يفضل يكتب لحد ما الـ context يخلص. عشان كده `max_tokens` في الـ client بتاعك مهم.
- **`repeat_penalty`** جديد عليك: بيقلل احتمال الـ tokens اللي اتكررت قريب. مفيد مع الموديلات الصغيرة اللي بتعيد نفسها.
- 🚫 **`draft_num_predict`** خاص بالـ **speculative decoding**: موديل صغير "بيخمّن" كام token وموديل كبير بيراجعهم، عشان السرعة. ده inference optimization (Ch.9)، عدّيه.

### 7.5 TEMPLATE (ص 7–8)
الـ template بلغة **Go templates** (شبه Blade بالظبط: `{{ if .System }}...{{ end }}` زي `@if($system)...@endif`). والمتغيرات: `{{ .System }}` و `{{ .Prompt }}` و `{{ .Response }}`. ومثال الصفحة بـ `<|im_start|>`، وده format عيلة Qwen.

**هتعدّل الـ TEMPLATE؟** غالباً **لأ**. الموديلات اللي من الـ library جاية بالـ template الصح. بتحتاجه بس لو عملت import لموديل من برّه (جزء 8). لو بوّظته، الموديل هيرد ردود غريبة لأنه مش شايف الـ format اللي اتدرّب عليه.

### 7.6 SYSTEM و LICENSE (ص 8–9)
- **`SYSTEM """..."""`**: بتثبّت system message جوه الموديل. أي حد يعمل `ollama run` عليه هيلاقيه.
- **`LICENSE """..."""`**: الـ license اللي الموديل متوزّع بيه. وده اللي `ollama show --license` بيطبعه. **ربط بالكتاب:** ده مكان تقرا فيه شروط الاستخدام (تجاري ولا لأ؟).

### 7.7 MESSAGE (ص 9)
بتحط **محادثة جاهزة** (أمثلة) جوه الموديل، بـ roles: `system` و `user` و `assistant`. مثال الصفحة: أسئلة "المدينة دي في كندا؟" والإجابة `yes`/`no`. ده **few-shot prompting** (فاكره من Step 01؟) **متخزّن جوه الموديل**، عشان الموديل يرد بنفس الأسلوب.

### 7.8 CAPABILITY و REQUIRES (ص 9–10)
- `CAPABILITY`: تضيف قدرة للموديل (مثلاً `decision` للموديلات المدرّبة على أسئلة System One). نادر.
- `REQUIRES 0.14.0`: أقل version من Ollama الموديل محتاجه (زي `"php": "^8.2"` في `composer.json`).

### 7.9 Notes (ص 10)
الـ Modelfile **مش case sensitive**، والـ instructions بأي ترتيب (بس `FROM` في الأول أوضح).

**إمتى تستخدم Modelfile عملياً؟**
- ✅ عايز `num_ctx` أكبر **ومش عارف تبعته** (زي مع الـ OpenAI-compatible API، جزء 9).
- ✅ عايز "bot" جاهز بـ system prompt ثابت لناس مش مبرمجين يستخدموه من `ollama run` أو app.
- ❌ في كود تطبيقك، **الأوضح غالباً تبعت الـ system والـ options في الـ request**: الإعدادات تبقى في الكود (و git) مش مستخبية في موديل على جهاز واحد. (زي ما بتفضّل config في الكود عن إعداد يدوي على السيرفر.)

---

## 8. Importing a Model
> 📍 `03-ollama-importing-a-model.pdf` ص 1–4

**الفكرة:** مش كل الموديلات في الـ Ollama library. ممكن تلاقي موديل على **Hugging Face** (أكبر مكان بيتنشر فيه الموديلات المفتوحة، زي "Packagist بتاع الموديلات") وعايز تشغّله. فيه 2 format:

| Format | يعني إيه | إمتى |
|---|---|---|
| **Safetensors** | الـ format الأصلي اللي الموديلات بتتنشر بيه (غالباً بدقة كاملة 16-bit، يعني كبير) | الموديل لسه "خام" |
| **GGUF** | format بتاع **llama.cpp** (المحرك اللي Ollama مبني عليه أصلاً)، ملف واحد، وغالباً **quantized** (مضغوط) | جاهز للتشغيل local |

**من Safetensors (ص 1–2):** Modelfile فيه `FROM /path/to/safetensors/directory`، وبعدين `ollama create my-model`، و `ollama run my-model`.

**من GGUF (ص 2):**
- `FROM /path/to/file.gguf`، ولو الموديل متقسّم لأكتر من ملف (shards): `FROM /path/to/model-*.gguf`.
- ⚠️ **Ollama مش بيعمل quantization للـ GGUF وقت الـ import**. لو عايز نسخة مضغوطة، لازم تعملها **قبل كده** بأداة زي `llama-quantize` من llama.cpp.

> 🚫 **الـ quantization بنفسك برّه النطاق.** اللي محتاج تعرفه **كقرار**: نفس الموديل بيتنشر بأكتر من quantization (هتشوف أسماء زي `Q4_K_M` و `Q8_0` و `F16`). **رقم أصغر = ملف أصغر وأسرع، وجودة أقل شوية**. والـ default في Ollama library غالباً 4-bit. يعني لما تختار موديل local، إنت بتختار **حجم** (3B، 7B) **و** **quantization**. (ارجع لـ "Memory و Model Size" في Step 02.)

**Sharing على ollama.com (ص 2–4):** تعمل account، وتضيف الـ public key (جزء 4.15)، وتسمّي الموديل باسمك (`ollama cp mymodel myuser/mymodel`)، وتعمل `ollama push`. والناس تعمل `ollama run myuser/mymodel`. (زي `docker push` لـ Docker Hub.)

**إمتى هتحتاج ده؟** نادراً في التعلم. غالباً لما تلاقي موديل **متخصص** (مثلاً موديل اتعمله finetune على العربي) مش موجود في الـ library.

---

## 9. OpenAI compatibility
> 📍 `03-ollama-openai-compatibility.pdf` ص 1–13

**الفكرة (ص 1):** Ollama بيدعم **جزء من OpenAI API**. يعني أي كود أو أداة مكتوبة لـ OpenAI تقدر تشغّلها على Ollama **بتغيير الـ URL بس**.

**ده تطبيق مباشر لنصيحة الكتاب** (محور الـ cost، ص 188): "اختار موديل بيتبع API standard عشان تبدّل بسهولة"، و "providers كتير بيقلّدوا OpenAI API". Ollama واحد منهم.

### 9.1 Cloud مباشرة (ص 1–2)
بـ library بتاعة OpenAI الرسمية (`pip install openai`):
- `base_url="https://ollama.com/v1"`
- `api_key` من `OLLAMA_API_KEY`
- وبعدين `client.chat.completions.create(model=..., messages=[...])` والرد في `response.choices[0].message.content`.

وكمان الـ **Responses API** (الـ API الأحدث بتاع OpenAI) بشكل **stateless** بس. (يعني مفيش "المحادثة متخزنة عند السيرفر"، إنت اللي بتبعت الـ history، زي ما اتعلمت في Step 01: الـ LLM stateless.)

### 9.2 Local (ص 2–4) ⭐
نفس الكود بالظبط، بس:
- `base_url='http://localhost:11434/v1/'`
- `api_key='ollama'` ← **مطلوب في الـ library بس Ollama بيتجاهله** (الـ library بتاعة OpenAI بترفض تشتغل من غير key، فبتحط أي حاجة).

وأمثلة لـ `/v1/chat/completions`، و `/v1/responses`، و vision (صورة بـ base64).

**قارن ده بالـ client بتاعك:**

| | `llm_client.py` بتاعك | OpenAI-compatible |
|---|---|---|
| URL | `http://localhost:11434/api/chat` | `http://localhost:11434/v1/chat/completions` |
| الرد | `data["message"]["content"]` | `choices[0].message.content` |
| الـ tokens | `prompt_eval_count` و `eval_count` | `usage.prompt_tokens` و `usage.completion_tokens` |
| الـ stop reason | `done_reason` | `finish_reason` |
| الـ options | `options: {num_ctx, top_k, ...}` | top-level: `temperature`، `top_p`، `max_tokens`، `seed`... |

نفس الموديل، ونفس الـ server، بس **"لغتين"** مختلفين. الـ native API (`/api/chat`) فيه **كل** features بتاعة Ollama. والـ OpenAI-compatible فيه **الجزء المشترك** اللي يخليك تبدّل.

### 9.3 الـ endpoints والـ features (ص 4–11)
- **`/v1/chat/completions`** بيدعم: chat، و streaming، و **JSON mode**، و **reproducible outputs** (`seed`)، و vision، و **tools**، و التحكم في الـ thinking (`reasoning_effort`)، و **logprobs**. والـ fields: `temperature`، و `top_p`، و `max_tokens`، و `stop`، و `seed`، و `response_format`، و `tools`، و `tool_choice`، و `logit_bias`، و `n`...
  - **ربط بالكتاب:** الكتاب قال إن الـ APIs التجارية **مش بتدّي logprobs غالباً**، وإن الـ self-hosting **بيدّيها**. أهو: Ollama بيدّيها.
  - **`reasoning_effort` (ص 6):** للموديلات اللي بتفكّر (thinking models). كل موديل ليه مستويات مختلفة، وتعرفها من `/api/show`. وفيه تحويلات (مثلاً `minimal` بتبقى `low`). **يعني نفس الـ parameter ممكن يتفسّر بشكل مختلف من موديل لموديل**، ودي حاجة تاخد بالك منها لما تبدّل.
- **`/v1/completions`** (ص 6–7): الـ API القديم (نص يتكمّل، من غير roles).
- **`/v1/models`** (ص 7–8): لستة الموديلات.
- **`/v1/embeddings`** (ص 8): للـ embeddings (Step 07).
- **`/v1/audio/speech` و `/transcriptions` و `/translations`** (ص 8–10): صوت (⏳ جديد، Step 13).
- **`/v1/responses`** (ص 10–11): الـ Responses API **من غير state** (مفيش `previous_response_id` ولا `conversation`).

### 9.4 أسماء الموديلات الافتراضية (ص 12)
فيه أدوات مكتوبة بأسماء موديلات OpenAI ثابتة (زي `gpt-3.5-turbo`). الحل: `ollama cp llama3.2 gpt-3.5-turbo`، يعني تعمل **نسخة باسم تاني** (alias)، والأداة تفتكر إنها بتكلّم OpenAI. 😄

### 9.5 الـ context size (ص 12–13) ⭐
**OpenAI API مفيهوش طريقة تحدد بيها `num_ctx`** (لأن الموديلات عند OpenAI ليها context ثابت). فلو بتستخدم الـ OpenAI-compatible API ومحتاج context أكبر: اعمل **Modelfile** فيه `FROM <model>` و `PARAMETER num_ctx <size>`، وبعدين `ollama create mymodel`، واستخدم `mymodel` في الـ request.

**الدرس العام (مهم للتاسكات):** الـ "standard API" بيدّيك **سهولة التبديل**، بس بتخسر **الـ features الخاصة** بكل provider. ده trade-off حقيقي:
- **native API لكل provider** + abstraction بتاعتك (زي drivers Laravel) = كل الـ features، وكود أكتر.
- **API واحد compatible** = كود أقل، و features أقل.

**تشبيه من Laravel:** زي Eloquent/Query Builder مقابل raw SQL. الـ Query Builder بيشتغل على MySQL و PostgreSQL و SQLite بنفس الكود، بس لو محتاج feature خاصة بـ PostgreSQL (زي `JSONB` operators المتقدمة) هتنزل لـ `DB::raw()`. نفس الحكاية: الـ OpenAI-compatible API هو الـ Query Builder، و `/api/chat` بـ `options.num_ctx` هو الـ raw SQL.

> 💡 **في الـ docs كمان صفحة *Anthropic compatibility*** (مكتوب في آخر الصفحة "Previous: Anthropic compatibility")، يعني Ollama بيقلّد API بتاع Anthropic كمان. وده اللي بيخلّي `ollama launch claude` يشتغل. مش محتاجينها دلوقتي.

---

## 10. Cloud
> 📍 `03-ollama-cloud.pdf` ص 1–2

**الفكرة (ص 1):** Ollama بقى عنده **cloud**: تشغّل **موديلات أكبر** من غير ما يكون عندك GPU قوي، والـ inference بيحصل **على سيرفرات Ollama**.

**تفاصيل مهمة:**
- ⚠️ **Cloud models حالياً مبتدعمش structured outputs.** (إنت في Step 02 Task 5 وصلت لـ 100% format صح بالـ schema على **local**. على الـ cloud models دي مش هتنفع!) ده مثال حي على كلام الكتاب: **نفس الأداة، features مختلفة حسب مكان التشغيل**. لازم تتأكد من الـ features قبل ما تبدّل.
- القدرات بتختلف من موديل للتاني.
- **طريقتين توصل بيهم (ص 1–2):** (1) تكلّم `https://ollama.com/api` مباشرة بـ API key، من غير تسطيب. (2) من الـ app أو الـ CLI أو الـ local API بتاعك بعد `ollama signin` (يعني `localhost:11434` نفسه بيعمل forward للـ cloud لما تختار cloud model، والأسماء شكلها زي `gemma4:cloud`). الاتنين محتاجين حساب.
- **Use only local models:** لو عايز الـ inference يفضل على جهازك، استخدم local وبس، أو **اقفل الـ cloud** (جزء 4.7).
- **Retirements (ص 2):** الـ cloud models **ممكن تتشال** لما موديلات أحدث تنزل، وفيه صفحة *Cloud model lifecycle*. **ده بالظبط** محور الـ control في الكتاب: "خطر إنك تفقد الموديل". والموديل الـ local؟ ملف عندك، محدش هيشيله.
- **Data handling (ص 2):** بيقولوا إنهم بيعالجوا الـ prompts عشان يردوا، ومبيدرّبوش عليها (وشوف جزء 4.6).

**الدرس الكبير من الصفحة دي:** "Cloud vs Local" مبقاش "شركة مقابل أداة". **نفس الأداة (Ollama) بقت الاتنين.** فالسؤال الصح مش "بستخدم Ollama ولا Claude؟"، السؤال: **"الـ inference بيحصل فين؟ وداتايا بتروح فين؟"**. موديل اسمه `:cloud` على `localhost` **داتاك بتخرج** رغم إن الـ URL بتاعك `localhost`!

> ⚠️ **ليك:** لو بتشتغل على داتا حساسة بـ Ollama، اتأكد إن الموديل اللي بتستخدمه **local فعلاً** (مش cloud)، أو اقفل الـ cloud بـ `OLLAMA_NO_CLOUD=1`. **الـ `localhost` في الـ URL مش ضمان.**

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md) تحت "Step 03 (المصدر 2)":
**Ollama Server (Daemon) و Client** · **Model Loading و keep_alive (Cold Start)** · **GPU / CPU Offloading** · **Default Context (num_ctx) في Ollama** · **Concurrency: NUM_PARALLEL و Queue** · **Modelfile** · **Chat Template** · **GGUF و Safetensors** · **OpenAI-compatible API** · **Local-only Mode (OLLAMA_NO_CLOUD)** · **Cloud Models في Ollama**

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. أول request لـ Ollama خد 25 ثانية، والتاني ثانيتين. ليه؟ وإزاي تحل ده في تطبيق؟</summary>

أول request كان لازم **يحمّل الموديل** من الـ disk للـ memory (cold start). بعد كده الموديل بيفضل محمّل **5 دقايق** (الـ default) فالـ requests بعدها سريعة. الحل: **preload** (request فاضي وقت ما التطبيق يبدأ)، و `keep_alive` أطول (أو `-1` يفضل على طول) لو الـ RAM تسمح. التمن: الـ memory محجوزة طول الوقت. ولو الجهاز عليه حاجات تانية محتاجة RAM، ممكن تحتاج `keep_alive: 0` بعد كل استخدام. ده trade-off بين الـ latency والـ memory.
</details>

<details><summary>2. موديل 7B شغّال عندك بطيء جداً مقارنة بالـ 3B (مش ضعف الوقت، أكتر بكتير). إيه أول حاجة تعملها؟</summary>

`ollama ps` وأبص على عمود **PROCESSOR**. غالباً الـ 3B كان داخل كله في الـ VRAM (`100% GPU`)، والـ 7B مدخلش فاتقسم (`40%/60% CPU/GPU`) أو اشتغل كله على الـ CPU. الـ offloading بيوقّع السرعة بشكل كبير مش خطي. وكمان أبص على عمود **CONTEXT**، لأن context كبير بياكل memory وممكن هو اللي يزق الموديل برّه الـ VRAM. الحلول: موديل أصغر، أو quantization أصغر، أو context أصغر.
</details>

<details><summary>3. عملت تطبيق ويب فوق Ollama، و 5 مستخدمين بيستخدموه في نفس الوقت، والكل بيشتكي من البطء. ليه؟ وإيه اللي ممكن يحصل لو 1000 request جم مرة واحدة؟</summary>

الـ default بتاع `OLLAMA_NUM_PARALLEL` = **1**، يعني الموديل بيخدم request واحد في المرة والباقي في **queue**، فكل مستخدم بيستنى اللي قبله. ولو 1000 request جم، الـ queue الـ default **512**، فاللي زيادة هياخدوا **503 overloaded**. تقدر تزوّد `NUM_PARALLEL`، بس **الـ memory بتزيد** (`NUM_PARALLEL × context`). وفي الآخر Ollama معمول للتطوير والاستخدام الشخصي، وللـ production على scale فيه أدوات زي vLLM (Step 15) أو API provider. ده محور الـ **scalability** في الكتاب.
</details>

<details><summary>4. إيه الفرق بين ollama ls و ollama ps و ollama stop و ollama rm؟</summary>

`ls`: الموديلات **المنزّلة على الـ disk**. `ps`: الموديلات **المحمّلة في الـ memory دلوقتي** (ومعاها الحجم، و GPU/CPU، والـ context، وهتتشال إمتى). `stop`: يشيل الموديل **من الـ memory** بس (لسه على الـ disk). `rm`: يمسحه **من الـ disk**.
</details>

<details><summary>5. الـ local API بتاع Ollama على 127.0.0.1. زميلك عايز يستخدم الموديل من جهازه، فغيّرت OLLAMA_HOST لـ 0.0.0.0. إيه الخطر؟</summary>

الـ API بتاع Ollama **مفيهوش authentication**. دلوقتي أي جهاز على الشبكة (ولو فتحته بـ ngrok، أي حد على الإنترنت) يقدر يبعت requests: يشغّل موديلاتك ويستهلك جهازك، ويـ pull موديلات ضخمة تملى الـ disk، ويمسح موديلات. الأحسن: حطه ورا reverse proxy (Nginx) فيه auth و HTTPS، أو VPN، أو على الأقل firewall يسمح لـ IP زميلك بس. زي إنك متفتحش MySQL على `0.0.0.0` من غير password.
</details>

<details><summary>6. إيه الـ Modelfile؟ وهل `ollama create` بيعمل finetuning؟</summary>

الـ Modelfile زي **Dockerfile** للموديلات: `FROM` موديل أساسي، وفوقه `PARAMETER` (temperature، num_ctx...) و `SYSTEM` و `MESSAGE` (أمثلة few-shot) و `TEMPLATE` و `LICENSE`. و `ollama create` بيعمل موديل جديد **بالإعدادات دي فوق نفس الـ weights**. **مش finetuning**: الـ weights متغيّرتش، والموديل مااتعلمش حاجة جديدة. ده بيثبّت الـ prompt والإعدادات بس.
</details>

<details><summary>7. لو مبعتش temperature في الـ request لـ Ollama، الموديل هيبقى deterministic؟</summary>

لأ. الـ default في Ollama **temperature 0.8** (و top_k 40، و top_p 0.9)، يعني فيه عشوائية. عشان تقرّب من الـ deterministic لازم تبعت `temperature: 0` (وممكن `seed` ثابت). ولو الموديل جاي بـ Modelfile فيه `PARAMETER temperature`، ده هو الـ default بتاعه. اتأكد بـ `ollama show <model> --parameters` أو `--modelfile`.
</details>

<details><summary>8. الـ docs بتقول مرة إن default الـ num_ctx هو 4096 ومرة 2048. تعمل إيه؟</summary>

متعتمدش على الـ docs، **اتأكد بنفسك**: شغّل الموديل (request عادي من غير `num_ctx`) وبص على عمود **CONTEXT** في `ollama ps`. ده الرقم الحقيقي على جهازي وبالـ version بتاعي. والأحسن في الكود: **متعتمدش على الـ default خالص**، ابعت `num_ctx` صريح، عشان الـ default ممكن يتغيّر مع أي تحديث لـ Ollama أو يختلف حسب الـ VRAM.
</details>

<details><summary>9. إيه فايدة الـ OpenAI compatibility؟ وإيه اللي بتخسره لما تستخدمها بدل الـ native API؟</summary>

الفايدة: أي كود أو أداة مكتوبة لـ OpenAI (library `openai`، أو أدوات جاهزة) تشتغل على Ollama بتغيير `base_url` بس. ده "الـ standard API" اللي الكتاب نصح بيه، بيسهّل التبديل بين providers.
اللي بتخسره: الـ features الخاصة بـ Ollama. أوضح مثال: **مفيش طريقة تحدد `num_ctx`** من الـ OpenAI API (لازم Modelfile)، و options زي `top_k` و `min_p` و `keep_alive` مش موجودة في القايمة. وكمان بعض الـ parameters (زي `reasoning_effort`) بتتفسّر بشكل مختلف من موديل لموديل.
</details>

<details><summary>10. ليه في مثال الـ local بنحط api_key='ollama' مع إن Ollama مش محتاج key؟</summary>

لأن الـ library بتاعة OpenAI نفسها **بترفض تشتغل من غير `api_key`** (معمولة لـ OpenAI اللي لازم key). فبنحط أي قيمة عشان نعدّي الـ validation بتاع الـ library، و Ollama local **بيتجاهلها**. ولو نفس الكود كلّم `https://ollama.com/v1` (الـ cloud)، ساعتها لازم key حقيقي من الـ environment.
</details>

<details><summary>11. شغّال على داتا حساسة، والكود بيكلّم http://localhost:11434. ده معناه إن الداتا مش بتخرج من جهازك؟</summary>

**مش بالضرورة.** لو عامل `ollama signin` والموديل اللي بتستخدمه **cloud model** (زي `gemma4:cloud`)، الـ local server بيعمل forward للـ request لسيرفرات Ollama، فالداتا **بتخرج** رغم إن الـ URL `localhost`. عشان تضمن: استخدم موديلات local بس (اتأكد بـ `ollama ls` و `ollama show`)، والأحسن **اقفل الـ cloud** بـ `OLLAMA_NO_CLOUD=1` أو `disable_ollama_cloud` في `server.json`. السؤال الصح دايماً: **الـ inference بيحصل فين؟** مش "الـ URL إيه؟".
</details>

<details><summary>12. قارن بين Ollama local و Ollama Cloud بمحاور الكتاب (privacy، functionality، control).</summary>

**Privacy:** local الداتا فيزيائياً مش بتخرج. cloud بتخرج، وبتعتمد على **وعد** إنهم مش بيخزّنوا ولا بيدرّبوا.
**Functionality/Performance:** cloud بيشغّل موديلات **أكبر** من غير GPU عندك، و context أقصى تلقائي. بس **مفيش structured outputs** في الـ cloud models حالياً، و local فيه.
**Control:** local الموديل ملف عندك، تقدر "تجمّده". cloud الموديلات **ممكن تتشال** (cloud model lifecycle / retirements).
**Cost:** local تكلفته جهازك والكهربا. cloud بالاستخدام وحساب.
يعني نفس الـ 7 محاور بتوع الكتاب، جوه **نفس الأداة**.
</details>

<details><summary>13. الـ default context في Ollama 4K على جهازك، والـ docs بتقول الـ agents محتاجة 64K على الأقل. إيه تأثير ده لما تبني agent على Ollama local؟</summary>

الـ agent بيجمّع في الـ context: system prompt طويل، وتعريفات الـ tools، ونتايج كل tool call، والمحادثة. ده بيعدّي الـ 4K بسرعة، و Ollama **هيقص الرسايل القديمة بصمت** (زي ما شفت في Step 02 Task 7)، فالـ agent هينسى نتايج أو تعليمات. لازم أكبّر `num_ctx`، وده **بياكل memory** (والـ KV cache بيكبر)، فممكن الموديل يعمل offload على الـ CPU ويبطأ جداً. فلازم أوازن: موديل أصغر بـ context أكبر، أو KV cache quantization (`q8_0`)، أو cloud، أو أقلل اللي بيدخل في الـ context (Step 11).
</details>
