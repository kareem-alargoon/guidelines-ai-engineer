# Step 03 — Observations

## Task 2 — قارئ الـ leaderboard (2026-11-27)

> **المصدر:** `resources/articles/03-artificial-analysis-providers.md`، وده **snapshot يوم 2026-11-13**. الأرقام دي (أسعار، وسرعة، و error rate) بتتغيّر كل أسبوع، فهي **صورة من يوم واحد**، مش حقيقة ثابتة.
> **الكود:** `work/leaderboard.py` (شغّله من `work/`: `python leaderboard.py`).

### 1. الأرقام العامة
| | العدد |
|---|---:|
| Endpoints | **525** |
| أسماء موديلات زي ما هي مكتوبة | 253 |
| موديلات بعد شيل tags الـ provider | 176 |
| **Open** | **408** |
| **Proprietary** | **117** |
| Endpoints الـ intelligence بتاعها `--` | 179 |

- الـ open أكتر بـ **3.5 مرة** تقريباً، لأن أي provider يقدر يشغّل موديل مفتوح، أما المقفول فبس صاحبه والـ clouds اللي متفقة معاه.
- **253 اسم مقابل 176 موديل:** الـ providers بيضيفوا على اسم الموديل tags خاصة بيهم: سرعة (`FAST` و `ULTRA` و `Turbo` و `High Speed`)، و quantization (`FP8` و `FP4` و `NVFP4` و `BF16`)، و platform (`Vertex` و `AI Studio` و `Base`). من غير ما نشيلهم، الـ top 10 open كانت فيها **Kimi K3.1 Pro 4 مرات** بأسماء مختلفة.
- **الـ reasoning effort** (`max` و `high` و `non-reasoning`) **فضل موديل لوحده** عن قصد، لأن الـ index بيتغيّر معاه (Claude Fable 5.2: max = 65، و xhigh = 62).
- **اتأكدنا إن الدمج صح:** كل مجموعة اتدمجت ليها **نفس الـ intelligence ونفس الـ license** في كل الـ endpoints بتاعتها. ودي برضه بتأكد اللي في الشرح (AA 3.4): الـ index **رقم الموديل** مش رقم كل endpoint، فالجدول **مش هيوريك** إن نسخة FP4 ممكن تبقى أضعف شوية.
- **غلطة اتصلحت:** في الأول `Nemotron 3 Ultra` بقى `Nemotron 3`، لأن `Ultra` هنا **جزء من اسم الموديل** مش tag. عشان كده الـ tags اللي من غير أقواس لستة أصغر.

### 2. أعلى الموديلات (سؤال 1 في الـ PR)
- **أعلى موديل في الكل:** Claude Fable 5.2 (max)، index **65** (Proprietary). أول 10 كلهم proprietary (Anthropic و Google و OpenAI).
- **أعلى موديل open:** Kimi K3.1 Pro، index **46**، وترتيبه **الـ 26** بين الموديلات المختلفة في صفحة الـ providers.
- **توقّع الكاتبة** ("أقوى موديل مفتوح هيفضل ورا أقوى مقفول") **لسه ماشي** في الـ snapshot ده: الفرق **19 نقطة** (46 مقابل 65).
- بعده في الـ open: DeepSeek V4.1 Flash 1017 (max) = 33، و GLM-5.3 (max) = 32. يعني فيه **قفزة كبيرة** بين أول موديل open والتاني (46 ← 33).

### 3. نفس الموديل، providers مختلفين

#### Claude Opus 5.5 (max): proprietary على 4 platforms
| Provider | Cost/Task | Time (min) | Errors |
|---|---:|---:|---:|
| Anthropic | $10.04 | 25.2 | 3.2% |
| Amazon Bedrock | $10.04 | 25.9 | 6.3% |
| Microsoft Azure | $11.43 | 30.8 | **9.8%** |
| Google | **$21.07** | **24.7** | 3.2% |

- الأغلى/الأرخص = **2.1x** (Google ضعف Anthropic).
- **نفس السعر مش معناه نفس الجودة:** Bedrock بنفس سعر Anthropic بالظبط، بس الـ error rate **الضعف**.
- Azure أغلى شوية **و** أبطأ **و** error rate تلات أضعاف. يعني مفيش سبب تقني تختاره، إلا لو شركتك متعاقدة مع Microsoft.
- الفرق في السرعة صغير (24.7 ← 30.8 دقيقة)، لأن الموديل نفسه هو اللي بياخد الوقت (reasoning `max`).

#### gpt-oss-120b (high): open عند 16 endpoint (13 بالاسم ده بالظبط + 3 بـ tags)
- **التكلفة:** من **$0.07** (CoreWeave) لـ **$0.76** (Cerebras)، يعني **10.5x**.
- **السرعة:** من **0.9 دقيقة** (Cerebras) لـ **40.7 دقيقة** (DeepInfra)، يعني **45x**.
- **الـ errors:** من **0%** (SambaNova و Cerebras) لـ **17.4%** (Google Vertex).
- **الأرخص هو تقريباً الأسوأ:** CoreWeave الأرخص، بس error rate **13.1%**. و DeepInfra التاني في الرخص، بس الأبطأ في الجدول و error rate **10.6%**.
- **الـ context مش واحد:** Baseten و Nebius و Scaleway **128k**، والباقي **131k**.
- **الـ tag بيغيّر كل حاجة:** `DeepInfra [Turbo]` بـ **$0.35** و `DeepInfra` العادي بـ **$0.09**، ونفس الموديل.

### 4. لو هختار provider لـ gpt-oss-120b (سؤال 2 في الـ PR)
**مش الأرخص (CoreWeave):** request من كل 8 تقريباً بيفشل، يعني retries، والـ retry بيتحسب عليك tokens ووقت. فالـ $0.07 الحقيقية أغلى من كده.

**الاختيارات المعقولة (من الجدول):**
- **Crusoe أو Novita** ($0.12، و 1% errors، و 5.6–8 دقايق): أحسن **سعر مقابل reliability**. اختيار كويس لشغل batch مش مستعجل.
- **Groq** ($0.32، و 3.3 دقيقة، و first token في **4.9 ثانية**): لو فيه user مستني الرد (chat).
- **SambaNova** ($0.49، و **0%** errors، و 3.1 دقيقة): لو الـ reliability أهم حاجة.
- **Cerebras** ($0.76، و 0.9 دقيقة): لو السرعة هي المنتج نفسه.

**الحاجات اللي مش في الجدول وبتأثر على القرار:**
- **الـ privacy وشروط الداتا:** بيحتفظ بالـ prompts؟ بيدرّب عليها؟ الـ servers في أنهي دولة؟
- **الـ rate limits** والـ SLA والـ support.
- **الـ quantization** اللي الـ provider شغّال بيها (ممكن تقلل الجودة، والـ index **مش** بيقيسها لكل endpoint).
- **OpenAI-compatible؟** وفيه tool calling و structured output؟
- **عقود شركتك:** لو عندكم AWS، Bedrock ($0.35، و 2.8%) أسهل في الفواتير والـ compliance.
- **الـ snapshot يوم واحد:** قبل ما تقرر، شوف الأرقام النهارده واعمل eval صغير على الـ provider نفسه (Task 6).

### 5. ⚠️ حدود الأرقام دي
- **صورة من يوم 2026-11-13:** الأسعار والسرعة والـ error rate بيتغيّروا كل أسبوع.
- **"Cost per Task" و "Time per Task"** دول على **الـ benchmark بتاع AA** (المهام بتاعتهم وطول الـ output بتاعهم)، مش على شغلك. استخدمهم **للمقارنة بين الـ providers**، مش عشان تحسب فاتورتك.
- **179 endpoint قدامها `--` في الـ intelligence:** مش معناه إنها وحشة، معناه إنها **مااتقيّمتش** على الـ index الحالي، و `top_models` بتستبعدها.
- **لستة الـ provider tags** متجمّعة من الـ snapshot ده. لو حفظت صفحة جديدة وطلع tag جديد، هتلاقي الموديل متكرر في الـ top 10، فضيفه لـ `PROVIDER_TAGS`.
