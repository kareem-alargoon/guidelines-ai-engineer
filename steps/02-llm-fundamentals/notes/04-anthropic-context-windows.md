# شرح: Anthropic docs — *Context windows*

> **المصدر:** صفحة في Claude Platform Docs — Anthropic — [الرابط](https://platform.claude.com/docs/en/build-with-claude/context-windows) (النسخة المحفوظة بتاريخ 17 أكتوبر 2026)
> **الملف:** `resources/articles/02-anthropic-context-windows.pdf` · **الجزء:** الصفحة كلها (PDF ص 1–8)
> **إزاي تقرا:** كل جزء هنا قبله `📍 PDF ص X`. اقرا الجزء في الـ PDF الأول (بالذات الـ diagrams)، وبعدين شرحه هنا.

## 🗺️ الصفحة دي بتتكلم عن إيه ومكانه فين في الـ roadmap

لحد دلوقتي الـ **context window** كان مفهوم نظري: في Step 01 (Karpathy: "الـ RAM بتاع الموديل")، وفي Ch.2 (الـ KV cache وليه الـ context الطويل غالي)، وفي فيديو Karpathy التاني (الـ context = **working memory** والـ parameters = تذكّر غامض). الصفحة دي بتنقلك من النظري لـ **API حقيقي**: إيه بالظبط اللي بيتحسب، وإزاي الـ thinking والـ tools بيستهلكوا المساحة، وبيحصل إيه لما المحادثة تطول أو تعدّي الحد.

**ليه مهمة ليك؟** لأن كل تطبيق هتبنيه (chat، و RAG، و agents) هيعيش جوّه الـ context window. ولو مافهمتهوش: هتدفع أكتر من اللازم، وهتلاقي requests بتفشل، أو الموديل بيبدأ "ينسى" أو يغلط في المحادثات الطويلة.

| # | الجزء | PDF ص | أهميته ليك |
|:---:|---|---|:---:|
| 1 | إزاي الـ context window بيشتغل | 1–2 | ⭐⭐⭐⭐ |
| 2 | أحجام الـ context window | 3 | ⭐⭐ |
| 3 | الـ context مع الـ thinking | 3–4 | ⭐⭐⭐ |
| 4 | الـ context مع الـ thinking والـ tools | 4–6 | ⭐⭐ (هيبقى ⭐⭐⭐⭐ في Step 10) |
| 5 | Context awareness | 6–7 | ⭐ |
| 6 | إدارة الـ context (compaction و context editing) | 7–8 | ⭐⭐⭐ |
| 7 | لما الـ context يتملي (overflow) | 8 | ⭐⭐⭐ |

> 💡 **عن الصفحة دي:** دي **docs رسمية** مش كتاب، يعني بتتحدّث باستمرار. النسخة اللي عندك محفوظة **النهارده**، فمفيش حاجة "قديمة" فيها، بس فيها **أسماء موديلات وأرقام هتتغيّر**. اللي تحفظه هو **المفاهيم**، والأرقام ارجع للصفحة الحية لما تحتاجها.

> ⚠️ **عن الـ thinking والـ tools:** أجزاء 3 و 4 فيها تفاصيل خاصة بـ API Claude (الـ thinking blocks والـ signatures). هنا هنفهم **الفكرة**، والتفاصيل العملية هتيجي لما نكتب كود في Step 04 و Step 10.

---

## 0. أول سطرين في الصفحة
> 📍 PDF ص 1

الصفحة بتبدأ بتنبيه: مع طول المحادثات هتقرب من حد الـ context window، وللمحادثات الطويلة والـ **agentic workflows**، الحل الأساسي اسمه **server-side compaction** (هنشرحه في جزء 6). يعني Anthropic بتقولك من أولها: **المشكلة دي هتقابلك أكيد**.

---

## 1. How the context window works
> 📍 PDF ص 1–2

**التعريف** (ص 1): الـ **context window** = **كل النص اللي الموديل يقدر "يشوفه" وهو بيولّد الرد، بما فيه الرد نفسه**.
- ده **غير** الداتا الضخمة اللي الموديل اتدرّب عليها.
- ده بيمثّل **"working memory"** للموديل. (⭐ نفس كلمة Karpathy بالظبط في جزء 13.4: الـ parameters = تذكّر غامض، والـ context = working memory.)

**⭐⭐ "More context isn't automatically better"** (ص 1): الـ context الأكبر بيخلّي الموديل يتعامل مع prompts أعقد وأطول، **بس**:
- كل ما عدد الـ tokens يزيد، **الدقة والقدرة على الاسترجاع (recall) بتقل**. الظاهرة دي اسمها **context rot** (الـ context "بيعفّن").
- فـ **اختيار اللي بتحطه في الـ context مهم قد مساحة الـ context نفسها**، أو أكتر.
- الصفحة بتحيلك لمقال *Effective context engineering* (موجود في ROADMAP Step 11).

**تشبيه من شغلك:** تخيّل إنك بتسلّم developer جديد **مستند 500 صفحة** فيه كل حاجة عن السيستم، وتطلب منه يصلّح bug. مقابل إنك تسلّمه **الـ 5 صفحات اللي ليها علاقة بالـ bug**. التاني هيشتغل أحسن وأسرع، مع إن الأول "فيه كل المعلومات". الموديل نفس الحكاية: **المعلومة الصح في context صغير أحسن من كل المعلومات في context ضخم.**

**ليه ده مهم جداً ليك؟** ده **الأساس النظري للـ RAG** (Step 09): بدل ما ترمي كل مستندات الشركة في الـ context (حتى لو بتساع في 1M token)، بتجيب **الأجزاء المناسبة بس**. أرخص، وأسرع، و**أدق**.

**الـ diagram الأولاني** (ص 2) ⭐ اتفرّج عليه كويس. بيوضّح 3 حاجات:
1. **التراكم (progressive accumulation):** مع كل turn، رسالة المستخدم ورد الموديل **بيتراكموا** في الـ context، والـ turns القديمة **بتفضل كاملة**.
2. **السعة:** الـ context window (لحد 1M token حسب الموديل) شايل **تاريخ المحادثة + الـ output الجديد**.
3. **كل turn فيه مرحلتين:**
   - **Input:** كل تاريخ المحادثة + الرسالة الجديدة.
   - **Output:** الرد، اللي **بيبقى جزء من الـ input في الـ turn الجاي**.

(footnote 1: الـ chat interfaces زي claude.ai ممكن تدير الـ context بطريقة "**first in, first out**": تشيل الأقدم لما يتملي. بس ده في الواجهة، **الـ API مش بيعمل كده لوحده**: إنت اللي بتقرر.)

**⭐ ربط بالـ Stateless LLM (Step 01):** ده بالظبط سبب إن **تكلفة المحادثة بتكبر مع طولها**: الموديل stateless، فإنت **بتبعت المحادثة كلها كل مرة**. turn رقم 20 بيبعت الـ 19 اللي قبله كمان. يعني لو كل turn حوالي 500 token، الـ turn العشرين input بتاعه حوالي 10 آلاف token.

**تشبيه من Laravel:** زي **session** بتكبر مع كل request، وكل request **بيبعت الـ session كلها للموديل** (مش بس بيقراها من الـ storage). وفي Laravel الـ session ليها حد (حجم الـ cookie أو الـ storage)، والـ context ليه حد.

**⭐⭐ إيه اللي بيتحسب في الـ context؟** (ص 2) **كل حاجة في الـ request**:
- الـ **system prompt**.
- **كل** رسالة في `messages`، بما فيها **نتايج الـ tools، والصور، والمستندات**.
- **تعريفات الـ tools** نفسها (الـ schemas بتاعتها).
- والـ **output** اللي الموديل بيولّده في الـ turn ده، **بما فيه الـ thinking**.

**إزاي تعرف استهلكت قد إيه؟** (ص 2)
- كل response فيه حقل **`usage`** بيقولك الـ request استهلك قد إيه.
- لو بتستخدم **prompt caching**، الـ input بيتقسم على 3 أرقام: `input_tokens` و `cache_read_input_tokens` و `cache_creation_input_tokens`، و**التلاتة بيتحسبوا في الـ context window**.
- ولو عايز **تقدّر قبل ما تبعت**، فيه **token counting API**.

**تشبيه من Laravel:** الـ `usage` زي الـ **query log** (`DB::getQueryLog()`) أو Laravel Debugbar: بيقولك بعد الـ request حصل إيه وكلّف قد إيه. والـ token counting API زي إنك تعمل **`EXPLAIN`** على query قبل ما تشغّلها: تعرف التكلفة من غير ما تنفّذ.

**💻 المقابل في Ollama (local):** رد Ollama فيه `prompt_eval_count` (عدد tokens الـ input) و `eval_count` (عدد tokens الـ output). ده الـ "usage" بتاعك وإنت شغّال local، وهنستخدمه في التاسكات.

---

## 2. Context window sizes by model
> 📍 PDF ص 3

- أغلب موديلات Claude الحالية (Claude Opus 5.5، و Sonnet 5.5، و Haiku 5.5، و Fable 5.1، وغيرهم) عندها context window **1M token** (مليون).
- الـ request الواحد يقدر يولّد لحد **128K output token** (ده حد الـ `max_tokens`).
- موديلات أقدم (زي Sonnet 4.5، deprecated) عندها **200K**.
- الـ 1M هو **الافتراضي** من غير أي إعداد إضافي، وبيتحاسب بالسعر العادي، **ما عدا** Claude Haiku 5.5: الـ prompts اللي فوق 100 ألف token **أغلى**.
- الـ request الواحد يقدر يشيل لحد **600 صورة أو صفحة PDF** (100 للموديلات اللي الـ context بتاعها 200K). ولو بتبعت صور أو مستندات كتير، **ممكن توصل لحد حجم الـ request قبل حد الـ tokens**.

**إزاي تقرا الأرقام دي؟**
- **1M token** تقريباً = 750 ألف كلمة إنجليزي (بقاعدة ¾ كلمة للـ token من Ch.1) = كذا كتاب كامل. وبالعربي أقل (العربي بياخد tokens أكتر).
- ⚠️ بس افتكر **context rot**: إنه **يساع** مش معناه إنه **هيشتغل كويس**. وكل token **بتدفع تمنه** (الـ input بتاع موديل زي Opus 5.5 مثلاً $4 لكل مليون token، يعني request واحد مليان 1M token ≈ $4، وكل turn في المحادثة هيبعته تاني!).

**💻 المقابل في Ollama:** الموديلات الـ local ليها **أقصى context** حسب الموديل نفسه (مثلاً موديلات Qwen2.5 بتدعم لحد 32K أو أكتر)، لكن **Ollama بيشغّلها بـ context أصغر بكتير افتراضياً** عشان الـ memory. بتغيّره بـ option اسمه **`num_ctx`**. ⚠️ وافتكر من Ch.2: كل ما تكبّر الـ context، **الـ RAM المستهلكة تزيد** (الـ KV cache). ⚠️ ونقطة مهمة: لو المحادثة عدّت الـ `num_ctx`، Ollama **بيشيل أقدم الرسايل من غير error واضح** (وغالباً بيحافظ على الـ system message وآخر رسالة)، فالموديل "ينسى" أول المحادثة وإنت مش واخد بالك. شيّك على `prompt_eval_count` دايماً. (هتجرّب ده بنفسك في Task 7.)

**تشبيه من Laravel:** الـ context window زي `post_max_size` و `memory_limit` في `php.ini`: حد أقصى للي ممكن يدخل في request واحد. والـ 600 صورة زي `max_file_uploads`: حد تاني ممكن تخبط فيه قبل الحد الأول.

---

## 3. The context window with thinking
> 📍 PDF ص 3–4

(الـ "thinking" هو الـ reasoning اللي شفناه في Karpathy جزء 21: الموديل بيولّد tokens تفكير قبل الرد.)

**الأساسيات** (ص 3):
- مع الـ thinking، **كل** الـ tokens (input و output، **ومنها tokens التفكير**) بتتحسب في حد الـ context window.
- **tokens التفكير جزء من الـ `max_tokens`** بتاعك، و**بتتحاسب كـ output tokens** (الأغلى!)، وبتتحسب في الـ rate limits.
- مع **adaptive thinking**، Claude بيقرر **قد إيه يفكر** لوحده، فاستهلاك tokens التفكير **بيختلف من request للتاني**.

**⚠️ ليه ده مهم عملياً؟**
- لو حطيت `max_tokens` صغير، ممكن الموديل **يخلّص الـ budget في التفكير** وماتلحقش تيجي الإجابة (أو تيجي ناقصة، `stop_reason: "max_tokens"`).
- التكلفة **مش ثابتة**: نفس نوع السؤال ممكن ياخد tokens تفكير مختلفة. فلما تحسب تكلفة تطبيقك، **قيس** على عينة حقيقية، متحسبش بالتخمين.

**الـ thinking blocks القديمة: بتفضل ولا بتتشال؟** (ص 3) ده بيختلف حسب الموديل:
- **الموديلات الأحدث** (Opus 4.5 وطالع، و Sonnet 4.6 وطالع، و Haiku 5.5، و Fable...): الـ API **بيحتفظ** بالـ thinking blocks من الـ turns اللي فاتت افتراضياً، و**بتتحسب في الـ context** زي أي input.
- **الموديلات الأقدم** (وكل Haiku لحد 4.5): الـ API **بيشيلها أوتوماتيك** لما تبعتها تاني، عشان يوفّر مساحة لكلام المحادثة.
- وتقدر تغيّر الافتراضي في الاتجاهين بحاجة اسمها **thinking block clearing**.

**الـ diagram التاني** (ص 4): بيوري موديل **بيشيل** الـ thinking القديم: في كل turn، الـ thinking (اللون الرمادي الغامق) بيتولّد في الـ output، **بس مش بيتنقل** كـ input للـ turn الجاي. ومش محتاج تشيله بنفسك: لو بعته، الـ API بيشيله.

**التكلفة** (ص 4): tokens التفكير بتتحاسب **كـ output مرة واحدة** وقت ما تتولّد. وفي الموديلات اللي **بتحتفظ** بيه، الـ blocks القديمة بتبقى جزء من الـ **input** في الـ requests الجاية، فبتتحاسب كـ input برضه (زي باقي تاريخ المحادثة).

**تشبيه من Laravel:** الـ thinking زي **مسودة** الموظف بيكتبها قبل ما يرد على الإيميل. في نظام (الموديلات القديمة)، المسودة بتترمي بعد ما الرد يتبعت. وفي نظام تاني (الموديلات الأحدث)، المسودة بتتحفظ في الملف مع الرد، فالملف بيتقل مع الوقت بس الموظف يقدر يرجع لتفكيره القديم.

---

## 4. The context window with thinking and tool use
> 📍 PDF ص 4–6

> 💡 الجزء ده هيبقى مهم جداً في **Step 10 (Tool Use)**. دلوقتي افهم الصورة العامة بس. (افتكر من Karpathy جزء 13.3: الموديل **بيطلب** tool، و**كودك** بينفّذ ويرجّع النتيجة.)

**الـ diagram التالت** (ص 5) بيوري 3 turns:

**Turn 1** (ص 5): الـ input = تعريفات الـ **tools** + رسالة المستخدم. والـ output = **thinking** + رد نصي + **طلب tool** (tool use). كله بيتحسب في الـ context، وكل الـ output بيتحاسب كـ output.

**Turn 2 (نتيجة الـ tool)** (ص 5):
- الـ input = **كل** حاجة من الـ turn الأول + **`tool_result`** (النتيجة اللي كودك جابها).
- ⚠️ **لازم ترجّع الـ thinking block** مع نتيجة الـ tool. وده **الحالة الوحيدة** اللي **لازم** ترجّع فيها thinking blocks.
- الـ output: Claude بيرد بنص بس (من غير thinking جديد لحد رسالة المستخدم الجاية، إلا لو **interleaved thinking** شغّال).

**Turn 3 (رسالة جديدة من المستخدم)** (ص 5–6):
- كل اللي فات بيتنقل. والـ thinking بتاع دورة الـ tool اللي خلصت **مبقاش لازم يفضل**: في الموديلات اللي بتشيل، الـ API بيشيله، وفي اللي بتحتفظ، بيفضل إلا لو مسحته.
- وفيه thinking block جديد لأن فيه رسالة جديدة من المستخدم.
- (في الـ diagram، Turn 3 مكتوب فيه "No text response due to truncation": يعني الـ context اتملي والرد **اتقطع**! ده تحذير بصري إن المحادثات الطويلة مع tools بتملا الـ context بسرعة.)

**اعتبارات مهمة** (ص 6):
- لما تبعت نتايج الـ tool، لازم تبعت الـ thinking block **كامل ومن غير أي تعديل**، بما فيه الـ **signature** بتاعه.
- الـ API بيستخدم **cryptographic signatures** عشان يتأكد إن الـ thinking block أصلي. **لو عدّلت فيه، الـ API بيرجّع error.**
- **Interleaved thinking:** أغلب موديلات Claude الحالية تقدر **تفكر بين الـ tool calls** (بعد ما تستلم نتيجة tool). ده **أوتوماتيك** في الموديلات اللي فيها adaptive thinking.
- **تعريفات الـ tools نفسها بتاكل context**: لو عندك tools كتير، فيه طرق تقلّل ده (زي **tool search tool**: الموديل يدوّر على الـ tool اللي محتاجها بدل ما كل التعريفات تبقى في الـ context).

**تشبيه من Laravel:** الـ signature زي **signed URLs** في Laravel (`URL::signedRoute()`) أو الـ **CSRF token**: الـ API بيتأكد إن اللي راجعله هو نفس اللي طلّعه بالظبط. لو غيّرت حرف، الـ signature مش هتطابق وهيرفض.

**⭐ الدرس العملي للـ agents:** كل tool call بيضيف للـ context: الطلب + **النتيجة** (ولو النتيجة صفحة ويب أو ملف كبير، ده آلاف الـ tokens) + الـ thinking. فالـ agent اللي بيعمل 20 tool call ممكن يملا الـ context بسرعة جداً. عشان كده إدارة الـ context (جزء 6) مهمة جداً للـ agents.

---

## 5. Context awareness
> 📍 PDF ص 6–7

**الفكرة** (ص 6): بعض موديلات Claude (Sonnet 5، و Sonnet 4.6، و Sonnet 4.5، و Haiku 4.5) عندها **context awareness**: بتعرف **قد إيه فاضل** من الـ context window ("token budget") طول المحادثة، فتقدر تدير المهام الطويلة على أساس المساحة الفاضلة بدل ما تخمّن. ده **أوتوماتيك**: الـ API بيعمله ليك.

**إزاي؟** (ص 7):
- في الـ system prompt، الـ API بيقول للموديل الحجم الكلي: `<budget:token_budget>200000</budget:token_budget>`.
- وبعد كل tool call، بيدّيه تحديث: `<system_warning>Token usage: 35000/200000; 165000 remaining</system_warning>`.
- (الـ tags دي الـ API بيحطها، **إنت مش بتبعتها**.)
- **الموديلات الأحدث** (Opus 4.7 وطالع، و Sonnet 5.5، و Haiku 5.5، و Fable) **مبتستقبلش** الـ tags دي. بدالها تقدر تدّي الموديل budget صريح بـ **task budgets** (beta).
- وللـ agents اللي بتشتغل على **كذا session**: صمم "state artifacts" (ملفات بتسجّل الحالة) بحيث الـ session الجديدة تقدر تكمّل بسرعة (فيه **memory tool** لده).

**تشبيه:** زي progress bar للـ upload، أو `memory_get_usage()` في PHP: الموديل بيشوف "استهلكت قد إيه وفاضل قد إيه" عشان يقرر يكمّل ولا يلم الدنيا.

**ليه يهمك؟** دلوقتي مش كتير. بس في الـ agents الطويلة (Step 11)، فكرة إن الموديل "عارف" المساحة الفاضلة بتأثر على إزاي بيخطط.

---

## 6. Manage context with compaction (وإدارة الـ context عموماً)
> 📍 PDF ص 7–8

**Compaction** (ص 7):
- لو محادثاتك بتقرب من الحد بانتظام، استخدم **server-side compaction**: بيلخّص **أوتوماتيك** الأجزاء القديمة من المحادثة على السيرفر، فالمحادثة تقدر **تكمّل بعد حد الـ context window**.
- متاح (beta) في موديلات Claude 4.6 وطالع.

**Context editing** (ص 7) لاحتياجات أدق:
- **Tool result clearing:** تمسح نتايج الـ tools القديمة في الـ agentic workflows (النتيجة دي خدمت غرضها، ليه تفضل تاخد مساحة؟).
- **Thinking block clearing:** تدير الـ thinking blocks من الـ turns القديمة.

**⭐ ملاحظة مهمة** (ص 8): **الـ cached prompt prefixes لسه بتاخد مساحة في الـ context**. الـ prompt caching بيغيّر **بتدفع قد إيه** على الـ tokens دي، **مش** إذا كانت بتتحسب ولا لأ. (فالـ caching بيوفّر فلوس ووقت، مش مساحة.)

**تشبيه من Laravel:**
- الـ **compaction** زي إنك **تأرشف** الـ logs القديمة: بدل ما تحتفظ بكل سطر، تحتفظ بـ **ملخص** ("الأسبوع اللي فات حصل كذا وكذا")، والتفاصيل تروح. ⚠️ والتلخيص **بيضيّع تفاصيل** (lossy)، فممكن معلومة مهمة من أول المحادثة تتنسي.
- الـ **tool result clearing** زي `Cache::forget()` لحاجة خلاص مش محتاجها.
- والـ caching مقابل المساحة: زي إن الـ **opcache** بيسرّع تشغيل الكود، بس مش بيقلّل حجم الكود.

**💡 الأفكار دي مش خاصة بـ Claude:** حتى لو بتستخدم Ollama local (مفيش compaction جاهز)، تقدر تعمل نفس الاستراتيجيات **بنفسك** في الكود:
1. **Sliding window:** تبعت آخر N رسالة بس.
2. **Summarization:** لما المحادثة تطول، تخلّي الموديل يلخّص القديم، وتبعت الملخص + الرسايل الأخيرة.
3. **تقصير نتايج الـ tools:** تبعت الجزء المهم بس من النتيجة، مش الصفحة كلها.
(وده هيبقى تاسك في الخطوة دي.)

---

## 7. Context window overflow behavior
> 📍 PDF ص 8

بيحصل إيه لما تعدّي الحد؟ حالتين:

| الحالة | بيحصل إيه |
|---|---|
| **الـ input لوحده أكبر من الـ context window** | الـ API بيرجّع **`400 invalid_request_error`** ("prompt is too long") في **كل** الموديلات. الـ request مبيتنفّذش أصلاً. |
| **الـ input + `max_tokens` أكبر من الـ context window** (بس الـ input لوحده بيساع) | في Claude 4.5 وطالع: الـ API **بيقبل** الـ request. ولو التوليد وصل لحد الـ context، **بيقف** بـ `stop_reason: "model_context_window_exceeded"`. (في الموديلات الأقدم كان بيرجّع validation error.) |

**الحل الوقائي:** استخدم **token counting API** عشان تقدّر الاستهلاك **قبل** ما تبعت.

**⭐ ربط بـ Ch.2 (Stopping condition):** دي **stop reason جديدة** تضيفها للستة اللي في شرح Ch.2 (`end_turn`، و `max_tokens`، و `stop_sequence`...). ونفس القاعدة: **دايماً شيّك على `stop_reason`** قبل ما تستخدم الرد. لو `model_context_window_exceeded` أو `max_tokens`، يبقى الرد **ناقص**.

**تشبيه من Laravel:** الحالة الأولى زي **`413 Payload Too Large`** أو `post_max_size` exceeded: الـ request بيترفض قبل ما يوصل للـ controller. والحالة التانية زي إن الـ response اتقطع لأن الـ script وصل لـ `max_execution_time`: بدأ يشتغل، بس مالحقش يخلّص.

**إزاي تتعامل معاها في تطبيقك؟**
1. **قبل ما تبعت:** احسب (أو قدّر) الـ tokens، ولو قربت من الحد، اعمل حاجة (لخّص، أو قص، أو شيل نتايج tools قديمة).
2. **بعد الرد:** شيّك على `stop_reason`، ولو الرد ناقص، اتعامل معاه (متعرضهوش كأنه كامل).
3. **في الـ chat apps:** متسيبش المحادثة تكبر للأبد؛ حط استراتيجية (جزء 6).

---

## 8. Next steps
> 📍 PDF ص 8

الصفحة بتحيلك لـ: **Compaction**، و **Model comparison table** (أحجام الـ context والأسعار)، و **Context editing**، و **Thinking**. هنقرا اللي محتاجينه منهم لما نوصل Step 04 (الـ API) و Step 11 (الـ agents).

---

## 🧭 الصورة الكاملة: الـ context window في كل اللي قريناه

| المصدر | قال إيه عن الـ context |
|---|---|
| Karpathy (Step 01) | "الـ RAM بتاع الموديل"، والموديل مايعرفش غير اللي فيه + الـ weights |
| Ch.2 | الـ KV cache بيكبر مع كل token، فالـ context الطويل **غالي ومحتاج memory**، وأقصى context مرتبط بالـ positions اللي الموديل اتدرّب عليها |
| Karpathy (Step 02) | الـ context = **working memory** (دقيق)، والـ parameters = **تذكّر غامض**. فحط المعلومة في الـ context |
| 3Blue1Brown | الـ attention بيخلّي الكلمات تفهم بعض حسب السياق |
| **Anthropic docs** | **كل حاجة** بتتحسب (system، و messages، و tools، و thinking، و output). الأكبر **مش دايماً أحسن** (context rot). بيحصل إيه لما يتملي، وإزاي تديره (compaction، و clearing) |

**الدرس الواحد اللي يجمعهم:** الـ context window **مورد محدود وغالي**: بتدفع على كل token، وكل token زيادة ممكن يقلّل الدقة. شغلك كـ AI Engineer إنك تحط فيه **المعلومة الصح بالحجم الصح**. وده اسمه **context engineering**.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md) تحت "Step 02 (المصدر 4)":
Context Rot · Token Usage و Token Counting · Thinking Tokens في الـ Context · Compaction و Context Editing · Context Window Overflow (`model_context_window_exceeded`).

(والـ Context Window نفسه موجود من Step 01.)

---

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. إيه الفرق بين الـ context window وداتا التدريب؟ واربطه بكلام Karpathy.</summary>

داتا التدريب هي النص الضخم اللي الموديل اتعلم منه، ومعرفته منها متخزنة في الـ **parameters** (تذكّر غامض، بحسب Karpathy). الـ context window هو **كل النص اللي الموديل شايفه في الـ request ده** (بما فيه الرد نفسه)، وده الـ **working memory**: دقيق وموجود قدامه مباشرة، بس بيتمسح مع كل request جديد (إلا لو بعته تاني).
</details>

<details><summary>2. يعني إيه context rot؟ وإزاي بيبرر وجود RAG حتى مع موديلات الـ context بتاعها 1M token؟</summary>

كل ما عدد الـ tokens في الـ context يزيد، **الدقة والـ recall بيقلوا**. فإن الـ context **يساع** حاجة مش معناه إن الموديل **هيستخدمها كويس**. وده بيبرر الـ RAG: بدل ما ترمي كل المستندات في الـ context (حتى لو بتساع)، تجيب **الأجزاء المناسبة بس**: أدق، وأرخص (بتدفع على كل token)، وأسرع (prefill أقصر).
</details>

<details><summary>3. عندك chatbot، وكل turn حوالي 400 token (سؤال + رد). turn رقم 25 هيبعت حوالي كام token input؟ وليه؟ وإيه المشكلة؟</summary>

حوالي 24 × 400 = **9600 token** من تاريخ المحادثة + الرسالة الجديدة + الـ system prompt. السبب إن الموديل **stateless**، فلازم تبعت المحادثة كلها كل مرة (الـ diagram الأولاني: الـ turns بتتراكم وبتفضل كاملة). المشكلة: التكلفة والـ latency (الـ prefill) بيكبروا مع كل turn، ولو المحادثة طولت أوي هتوصل للحد أو للـ context rot. فمحتاج استراتيجية (sliding window، أو تلخيص، أو compaction).
</details>

<details><summary>4. عدّد كل الحاجات اللي بتتحسب في الـ context window في request لـ Claude.</summary>

الـ **system prompt**، و**كل** الرسايل في `messages` (بما فيها **نتايج الـ tools، والصور، والمستندات**)، و**تعريفات الـ tools**، والـ **output** اللي بيتولّد (بما فيه الـ **thinking**). ولو فيه prompt caching، الـ cached tokens **برضه بتتحسب** (الـ caching بيغيّر السعر مش المساحة).
</details>

<details><summary>5. إيه علاقة الـ thinking بالـ max_tokens والتكلفة؟ وإيه المشكلة لو حطيت max_tokens صغير مع موديل بيفكر؟</summary>

tokens التفكير **جزء من الـ `max_tokens`**، و**بتتحاسب كـ output** (الأغلى)، وبتتحسب في الـ context والـ rate limits. ومع adaptive thinking، كميتها بتختلف من request للتاني، فالتكلفة مش ثابتة. لو `max_tokens` صغير، الموديل ممكن **يصرف الـ budget كله في التفكير** والإجابة متيجيش أو تيجي ناقصة (`stop_reason: "max_tokens"`).
</details>

<details><summary>6. في دورة tool use مع thinking، إيه اللي لازم ترجّعه للـ API؟ وليه مينفعش تعدّل في الـ thinking block؟</summary>

لما تبعت `tool_result`، **لازم** ترجّع الـ thinking block اللي جه مع طلب الـ tool **كامل ومن غير تعديل** بالـ signature بتاعه (ودي الحالة الوحيدة اللي لازم فيها). الـ API بيستخدم **cryptographic signature** يتأكد إن الـ block أصلي، فلو عدّلته هيرجّع error (زي signed URLs في Laravel).
</details>

<details><summary>7. ليه الـ agents بالذات بتملا الـ context بسرعة؟ وإيه الطرق اللي الصفحة بتقترحها؟</summary>

لأن كل tool call بيضيف: الطلب + **النتيجة** (ممكن تبقى صفحة ويب أو ملف = آلاف الـ tokens) + الـ thinking، وكمان تعريفات الـ tools نفسها بتاخد مساحة. فـ 20 tool call ممكن يملوا الـ context. الطرق: **server-side compaction** (تلخيص أوتوماتيك للقديم)، و**tool result clearing** (مسح نتايج الـ tools القديمة)، و**thinking block clearing**، و**tool search** (بدل كل تعريفات الـ tools في الـ context). وللـ agents اللي على كذا session: memory و state artifacts.
</details>

<details><summary>8. "استخدمت prompt caching، يبقى وفّرت مساحة في الـ context". صح ولا غلط؟</summary>

غلط. الـ cached prefixes **لسه بتاخد مساحة** في الـ context window. الـ caching بيغيّر **التمن** (أرخص) والسرعة (حسابات الـ prefill محفوظة، زي ما شرحنا في Ch.2 عن الـ KV cache)، مش المساحة. زي الـ opcache: بيسرّع الكود مش بيصغّره.
</details>

<details><summary>9. إيه الفرق بين حالتين الـ overflow؟ وإزاي تتعامل مع كل واحدة في تطبيقك؟</summary>

(1) **الـ input لوحده أكبر من الـ context** ← `400 invalid_request_error` ("prompt is too long")، والـ request مبيتنفّذش (زي 413 Payload Too Large). التعامل: احسب الـ tokens قبل ما تبعت (token counting API)، وقلّل الـ input (لخّص، أو قص، أو امسح نتايج قديمة). (2) **الـ input بيساع بس الـ input + max_tokens أكبر** ← في الموديلات الحديثة الـ request بيتقبل، ولو التوليد وصل للحد بيقف بـ `stop_reason: "model_context_window_exceeded"` (زي script وصل max_execution_time). التعامل: **شيّك على `stop_reason`** ومتعرضش الرد كأنه كامل.
</details>

<details><summary>10. عايز تبني chat app على Ollama local ومحادثاته طويلة. إيه اللي لازم تاخد بالك منه بناءً على الصفحة دي وعلى Ch.2؟</summary>

(1) Ollama بيشغّل الموديل بـ **context افتراضي صغير** (`num_ctx`)، ولو المحادثة عدّته بيشيل **أقدم الرسايل** من غير error واضح، فالموديل "ينسى" أول المحادثة. (2) تكبير `num_ctx` بيزوّد **الـ RAM** (الـ KV cache من Ch.2). (3) شيّك على `prompt_eval_count` و `eval_count` عشان تعرف الاستهلاك الحقيقي (المقابل لـ `usage`). (4) مفيش compaction جاهز، فاعمل استراتيجية بنفسك: **sliding window** أو **تلخيص** القديم. (5) وافتكر **context rot**: الموديلات الصغيرة بتتأثر أكتر بالـ context الطويل.
</details>
