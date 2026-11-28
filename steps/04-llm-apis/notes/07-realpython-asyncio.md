# شرح: Real Python — *Python's asyncio: A Hands-On Walkthrough*

> **المصدر:** [Real Python — Async IO in Python](https://realpython.com/async-io-python/) — Leodanis Pozo Ramos — آخر تحديث Oct 24, 2026
> **الملف:** `resources/articles/04-realpython-async-io.pdf`
> **إزاي تقرا:** المقال ماشي بالترتيب ده بالظبط. جرّب كل مثال بنفسك (انسخه في ملف وشغّله)، لأن الـ async بيتفهم **بالتجربة** أكتر من القراية. والـ 📍 فيه اسم الـ section.

## 🗺️ المصدر ده بيتكلم عن إيه ومكانه فين في الـ roadmap

في Step 03 Task 6 الـ eval على 15 إيصال خد ~43 ثانية (2.85 ث للإيصال، **واحد ورا التاني**). لو بتكلّم API على الإنترنت، أغلب الوقت ده **انتظار** (الشبكة والسيرفر). الـ **async** بيخليك تبعت requests كتير **وتستنى ردودهم في نفس الوقت**. وده أساس:
- Task 7 (معالجة الإيصالات بالتوازي).
- `AsyncAnthropic` و `httpx.AsyncClient` (الشرح 01 و 06).
- أي API هتبنيه بـ **FastAPI** بعدين (Step 15)، لأنه async من الأساس.

**تشبيه من Laravel (للصورة الكبيرة):** PHP في Laravel **sync**: كل request ليه process (أو worker في PHP-FPM)، ولو عايز تبعت 10 HTTP calls بالتوازي بتستخدم **`Http::pool()`** (اللي جواه Guzzle promises). الـ asyncio هو الطريقة "الطبيعية" في Python لده، بس **في process واحد و thread واحد**.

> ⏳ المقال حديث (أكتوبر 2026) وبيستخدم Python 3.13. مفيش حاجة قديمة فيه.

---

## 1. A First Look at Async I/O
> 📍 section *A First Look at Async I/O*

**الفكرة:** المقال بيبدأ بالمصطلحات:
- **Parallelism:** عمليات كتير **في نفس اللحظة بالظبط**.
- **Multiprocessing:** parallelism عن طريق توزيع الشغل على **CPU cores** مختلفة. مناسب للـ **CPU-bound** (حسابات تقيلة).
- **Concurrency:** أعم: مهام كتير **بتتداخل** في التنفيذ. **مش لازم** تبقى في نفس اللحظة.
- **Threading:** threads بتتبادل التنفيذ في process واحد. مناسب للـ **I/O-bound**. (وفيه GIL، خارج نطاق المقال.)
- **I/O-bound** = أغلب الوقت **انتظار** (شبكة، ملفات). **CPU-bound** = الـ CPU شغّال طول الوقت.

**وبعدين async I/O:** موديل تالت، "**single-threaded, single-process**" بيستخدم **cooperative multitasking**. يعني **مش** threading ومش multiprocessing. **Concurrency مش parallelism.** والـ coroutines بتتعمل schedule بالتداخل، بس هي نفسها مش "parallel".

**تعريف "asynchronous" هنا:** (1) الـ routine تقدر **توقف نفسها** وهي مستنية نتيجة وتسيب غيرها يشتغل، و (2) الكود بينسّق تنفيذ مهام كتير بالتداخل.

**💡 ليه ده يهمك؟** استدعاء LLM API = **I/O-bound** بامتياز: إنت بتبعت request وتستنى ثواني من غير ما الـ CPU بتاعك يعمل حاجة. فالـ async مثالي. **بس** Ollama local ده **مختلف**: الـ "انتظار" هو الـ CPU بتاعك (اللي شغّال الموديل) مشغول بالحساب. هنرجع لده في جزء 10.

## 2. Async I/O Explained (مثال الشطرنج)
> 📍 section *Async I/O Explained*

**الفكرة:** بطلة شطرنج بتلعب ضد **24 واحد**. هي بتلعب النقلة في **5 ث**، وكل منافس في **55 ث**، والدور 30 نقلة لكل واحد.
- **Sync:** دور دور: كل دور (55 + 5) × 30 = 30 دقيقة، والـ 24 دور = **12 ساعة**.
- **Async:** بتلف على الترابيزات، تلعب نقلة وتمشي (والمنافس بيفكّر). لفة كاملة = 24 × 5 = دقيقتين، و 30 لفة = **ساعة واحدة**.

**الدرس:** **فيه بطلة واحدة بس** (thread واحد)، بتعمل نقلة واحدة في المرة. بس بدل ما **تستنى** المنافس، بتستغل وقت الانتظار في ترابيزة تانية. ده بالظبط الـ **event loop**.

**💡 ترجمها لمشروعك:** البطلة = كودك، والمنافسين = requests للـ API. كودك بيبعت request (5 ث مثلاً "شغل")، وبدل ما يستنى رد الـ API (الـ 55 ث)، يبعت request تاني. **بشرط** إن الـ "منافس" بيفكّر **لوحده** (سيرفر Anthropic). لو المنافس بيستخدم **نفس دماغ** البطلة (Ollama على نفس الـ CPU)، الحكاية بتختلف.

## 3. Async I/O Isn't Simple
> 📍 section *Async I/O Isn't Simple*

**الفكرة:** الـ async أسهل من الـ threading في حاجات (مفيش race conditions بنفس الشكل)، بس **مش سهل**: فيه مصطلحات كتير (callbacks، و coroutines، و events، و transports، و futures). والخبر الحلو إن الـ `asyncio` بقى stable والـ docs اتحسّنت.

## 4. Coroutines and Coroutine Functions
> 📍 section *Coroutines and Coroutine Functions*

**الفكرة:** الـ **coroutine** = object يقدر **يوقف تنفيذه ويكمّل بعدين**، وفي الوقت ده يسلّم التحكم للـ **event loop**. والـ coroutine بيتعمل لما تنادي **coroutine function** (`async def`).

**المثال (`countsync.py` مقابل `countasync.py`):**
- **Sync:** `count()` بتطبع "One"، و `time.sleep(1)`، و "Two"، و `time.sleep(1)`. ولو اتنادت 3 مرات = **6.03 ث**.
- **Async:**
  ```python
  async def count():
      print("One")
      await asyncio.sleep(1)
      print("Two")
      await asyncio.sleep(1)

  async def main():
      await asyncio.gather(count(), count(), count())

  asyncio.run(main())
  ```
  = "One One One Two Two Two" في **2.00 ث**.

**إيه اللي حصل؟**
- `async def` بيخلّي `count()` **coroutine function**.
- `await asyncio.sleep(1)` = "هنام ثانية، **روح شغّل حاجة تانية**". التحكم بيرجع للـ event loop.
- `asyncio.gather(...)` بيشغّل الـ 3 **بالتداخل**.
- `asyncio.run(main())` بيشغّل الـ event loop.

**⚠️ أهم فرق:** `time.sleep()` = **blocking**: بيوقف **كل حاجة** (البطلة واقفة قدام ترابيزة واحدة). `asyncio.sleep()` = **non-blocking**: بيسيب غيره يشتغل. و"any other blocking call is incompatible with asynchronous Python code".

**💡 ده بيترجم لإيه في كودك؟** `httpx.post(...)` (sync) = blocking زي `time.sleep`. لو حطيته جوه `async def`، **مش هيبقى async**. لازم `await client.post(...)` من **`httpx.AsyncClient`**. ونفس الكلام: `Anthropic()` (sync) مقابل `AsyncAnthropic()`.

## 5. The async and await Keywords
> 📍 section *The async and await Keywords*

**القواعد:**
- `async def` = coroutine function (أو **async generator** لو فيها `yield`). و `async with` و `async for` = نسخ async من `with` و `for`.
- **`await`** = "وقّف الـ coroutine دي لحد ما النتيجة تيجي، وفي الوقت ده سيب غيرها يشتغل".
- عشان تنادي coroutine function: يا **`await`** عليها، يا تشغّلها في event loop (`asyncio.run`).
- `yield` جوه `async def` = async generator (تلف عليه بـ `async for`). و `yield from` جوه `async def` ← SyntaxError.
- **`await` برا `async def` ← SyntaxError.**
- اللي بتعمله `await` لازم يبقى **awaitable** (coroutine غالباً).

**مثال `rand.py`:** `makerandom(delay, threshold)` بتولّد أرقام عشوائية لحد ما رقم يعدّي الـ threshold، و `await asyncio.sleep(delay)` بين كل محاولة. و 3 نسخ بـ `gather` بيشتغلوا بالتداخل (بألوان مختلفة في الـ terminal). والنتيجة من `gather` = **list بنفس ترتيب الـ inputs** (`r1, r2, r3 = asyncio.run(main())`).

**والملاحظة المهمة:** توليد الأرقام **CPU-bound** بس صغير جداً. الـ `asyncio.sleep` بيمثّل I/O. و"**only I/O-bound or non-blocking tasks benefit from the async I/O model**".

**تشبيه من Laravel:** `await` قريب من `$promise->wait()` في Guzzle، بس الفرق إن `wait()` بيوقف كل حاجة، و `await` بيوقف الـ coroutine دي بس.

## 6. The Async I/O Event Loop
> 📍 section *The Async I/O Event Loop*

**الفكرة:** الـ event loop = loop لا نهائية بتراقب الـ coroutines، وتشوف مين مستني ومين جاهز، وتصحّي اللي جاهز.
- **`asyncio.run()`** هي الطريقة الموصى بيها: بتعمل الـ loop، وتشغّل لحد ما الشغل يخلص، وتقفله. **ومينفعش تناديها لو فيه loop شغّال أصلاً.**
- `asyncio.get_running_loop()` بيجيب الـ loop الحالي (لو مفيش ← `RuntimeError`).

**3 نقط مهمة:**
1. **"Coroutines don't do much on their own until they're tied to the event loop."** لو ناديت `main()` من غير `await` أو `asyncio.run`، بترجعلك **coroutine object** (`<coroutine object main at 0x...>`) **ومفيش حاجة بتتنفذ**.
2. الـ loop بيشتغل في **thread واحد على core واحد**، وغالباً فيه loop واحد في البرنامج.
3. الـ loops **pluggable**: على **Windows الـ default `ProactorEventLoop`**، وعلى Unix `SelectorEventLoop`، وفيه `uvloop` أسرع.

**⚠️ غلطة شائعة جداً:** تنسى `await` قبل coroutine. الكود مش هيقع، بس **مش هيعمل حاجة** (وغالباً Python هيطلّع warning "coroutine was never awaited"). لو حاجة "مش بتحصل" في كود async، أول حاجة تدوّر عليها: `await` ناقص.

## 7. The asyncio REPL
> 📍 section *The asyncio REPL*

**الفكرة:** `python -m asyncio` بيفتح REPL تقدر تكتب فيه **`await`** على طول (من غير `asyncio.run`). مفيد للتجريب:
```
>>> await main()
Hello...
World!
```
**💡 جرّبه مع الـ SDK:** في الـ REPL ده تقدر تعمل `client = AsyncAnthropic(base_url=..., api_key="ollama")` و `await client.messages.create(...)` وتشوف النتيجة على طول.

## 8. Common Async I/O Programming Patterns
> 📍 section *Common Async I/O Programming Patterns*

### 8.1 Coroutine Chaining
**الفكرة:** coroutine بيعمل `await` على coroutine تاني وياخد نتيجته ويديها للتالت. مثال `chained.py`:
- `fetch_user(user_id)` (انتظار عشوائي 0.5–2 ث) ← بيرجّع user.
- `fetch_posts(user)` (انتظار عشوائي) ← بيطبع الـ posts.
- `get_user_with_posts(user_id)` = `user = await fetch_user(...)` وبعدين `await fetch_posts(user)` (**chain**: الخطوة التانية محتاجة نتيجة الأولى).
- `main()` = `await asyncio.gather(*(get_user_with_posts(uid) for uid in user_ids))`.

النتيجة: **2.68 ث** بدل ~7.6 ث sync. و**الـ `*`** قبل الـ generator expression بيفكّه عشان `gather` ياخد كل coroutine كـ argument منفصل.

**💡 ترجمة لمشروعك:** `process_receipt(receipt)` = `result = await extract(text)` وبعدين `score(result, expected)`. والـ chain ده لكل إيصال، و `gather` على الـ 15.

### 8.2 Coroutine and Queue Integration ⭐
**الفكرة:** بديل للـ chaining: **producers** بيحطوا حاجات في **`asyncio.Queue`**، و **consumers** بيسحبوا منها. ومفيش ربط مباشر بينهم: الـ producer مايعرفش عدد الـ consumers، والعكس.

مثال `queued.py`:
- `producer(queue, user_ids)`: بيجيب الـ users (بالتوازي) ويعمل `await queue.put(user)` لكل واحد. وفي الآخر بيحط **`None` لكل consumer** (اسمها **sentinel** أو **poison pill**) عشان يقولهم "خلاص".
- `consumer(queue)`: `while True: user = await queue.get()`، ولو `None` ← `break`، وإلا بيعالج.
- `main()`: `gather(producer(...), *(consumer(queue) for _ in user_ids))`.

ونفس الوقت (2.68 ث).

**💡 ليه ده أهم pattern لـ Task 7؟** عشان **عدد الـ consumers = حد الـ concurrency**. لو عندك 1,000 إيصال وعملت `gather` على الـ 1,000، هتبعت 1,000 request في نفس اللحظة: rate limits و ramp limits (الشرح 04)، أو Ollama يتخنق. بالـ queue: producer يحط الـ 1,000 إيصال، و **N consumers بس** (مثلاً 4) بيسحبوا منها. يعني **4 requests في نفس الوقت بالظبط**، مهما كان عدد الإيصالات.

**تشبيه من Laravel:** ده **Queue + Workers** بالظبط: `dispatch(new ProcessReceipt($r))` = `queue.put()`، و `php artisan queue:work` × 4 = 4 consumers. والـ sentinel زي إنك تبعت signal للـ workers يقفلوا (`queue:restart`). ⚠️ الفرق: Laravel queue **بتعيش برا** الـ process (Redis/DB) وبتستحمل إن البرنامج يقع، و `asyncio.Queue` **في الـ memory** وبتروح لو البرنامج وقع.

## 9. Other Async I/O Features in Python
> 📍 section *Other Async I/O Features in Python*

### 9.1 Async Iterators, Loops, and Comprehensions
**الفكرة:** `async for` بيلف على **async iterator**، ومع كل لفة بيسلّم التحكم للـ loop. و **async generator** = `async def` فيها `yield`:
```python
async def powers_of_two(stop=10):
    exponent = 0
    while exponent < stop:
        yield 2**exponent
        exponent += 1
        await asyncio.sleep(0.2)
```
وتستخدمه: `async for i in powers_of_two(5)`، أو comprehension: `[j async for j in powers_of_two(5) if ...]`.

**⚠️ فرق مهم:** الـ `async for` **مش بيخلّي اللفات parallel**. اللفات لسه **بالترتيب**، بس بين كل لفة والتانية الـ loop يقدر يشغّل حاجات تانية. لو عايز تداخل حقيقي: `gather`.

**💡 ده بالظبط الـ streaming في الـ SDK:** `async for text in stream.text_stream:` (الشرح 01، جزء 5.5). كل حتة نص بتيجي من الشبكة، وفي الوقت ده الـ loop حر.

### 9.2 Async with Statements
**الفكرة:** `async with` = `with` بس الـ setup والـ teardown نفسهم async (فتح وقفل connection). مثال بـ **aiohttp**: `async with aiohttp.ClientSession() as session:` و `async with session.get(url) as response:`، و `gather` على 3 مواقع.

**ليك:** إنت هتستخدم **httpx** مش aiohttp (الاتنين في قايمة libraries آخر المقال). المقابل: `async with httpx.AsyncClient() as client:`. و`async with` بيضمن إن الـ connections تتقفل حتى لو حصل error.

⚠️ **لاحظ في مثال المقال:** بيعمل `ClientSession` جديد **جوه** `check(url)`، يعني session لكل URL. ده **عكس** نصيحة httpx (الشرح 06، جزء 8): client واحد للكل. للـ 3 مواقع مش مشكلة، بس لـ 1,000 request هتفرق.

### 9.3 Other asyncio Tools
**`asyncio.create_task(coro)`:** بيحوّل الـ coroutine لـ **Task** ويعمله schedule **في الخلفية فوراً**. والفرق عن `await coro`: الـ `await` بيشغّله **دلوقتي ويستناه**، و `create_task` بيبدأه ويكمّل.

**⚠️ "if you create tasks with `create_task()` but don't await them or wrap them in `gather()`, and your `main()` coroutine finishes, then those manually created tasks will be canceled".** يعني لازم تعمل `await` على كل task عايزه يخلص.

**`asyncio.gather()`:** بيستنى **الكل**، والنتيجة **list بنفس ترتيب الـ inputs** (deterministic)، مش بترتيب الخلصان.

**`asyncio.as_completed()`:** iterator بيدّيك الـ tasks **بترتيب ما بتخلص**. مثال: task فيها `sleep(1)` بتطلع قبل task فيها `sleep(2)` حتى لو اتبدأت بعدها. **مفيد لو عايز تطبع/تحفظ كل نتيجة أول ما تيجي** (progress bar مثلاً).

**💡 لـ Task 7:** `gather` لو محتاج النتايج بالترتيب (عشان تقارنها بالـ expected بالـ index)، و `as_completed` لو عايز تعرض التقدم. والـ queue لو عايز تحدد الـ concurrency.

### 9.4 Async Exception Handling
**الفكرة (Python 3.11+):** لو كذا coroutine وقعت بـ errors مختلفة:
- `gather(..., return_exceptions=True)`: بدل ما أول error يوقع الكل، الـ exceptions بترجع **في list النتايج** جنب النتايج الناجحة.
- وتقدر تجمعهم في **`ExceptionGroup`** وتمسكهم بـ **`except*`** (كل نوع لوحده).

**⚠️ الـ default مهم:** من غير `return_exceptions=True`، **أول exception** بيطلع من `gather`. فلو إيصال واحد من 15 فشل (timeout مثلاً)، هتخسر نتايج الـ 14 التانيين. **للـ eval: استخدم `return_exceptions=True`** وسجّل الفشل كنتيجة.

**تشبيه من Laravel:** `Http::pool()` بيرجّعلك كل الـ responses حتى لو بعضها فشل، وإنت بتشيك كل واحد (`$responses[0]->ok()`). ده زي `return_exceptions=True`.

## 10. Async I/O in Context
> 📍 section *Async I/O in Context*

### When to Use Async I/O
**الفكرة:**
- **"Using `async def` for functions that perform blocking operations ... will block the entire event loop".** استخدم `async def` للعمليات **non-blocking** بس.
- **Multiprocessing** للـ CPU-bound (ومش "منافس" للـ async، ينفعوا مع بعض).
- **Threading** أصعب (race conditions) وبيتوسّع أقل (الـ threads محدودة). **آلاف الـ async tasks عادي جداً.**
- الـ async بيلمع في: **network I/O** (client أو server)، و serverless designs، و read/write fire-and-forget.
- **أكبر عيب:** لازم الـ library تدعم async. مثلاً DB driver لازم يبقى عنده نسخة async.

### 💡 السؤال المهم: الـ async هيسرّع Ollama local؟
المقال بيقول الـ async بيفيد في الـ **I/O-bound**. مع **Claude API** الـ request = انتظار سيرفر بعيد، فـ 4 requests مع بعض ≈ وقت request واحد (لحد الـ rate limits). **مع Ollama على الـ CPU بتاعك** (`size_vram = 0` من Step 03)، الـ "سيرفر" هو **نفس الجهاز**، والموديل شغّال على نفس الـ cores. فالـ requests المتوازية:
- يا Ollama **بيحطها في queue** ويعالجها واحدة واحدة (concept "Concurrency: NUM_PARALLEL و Queue" من Step 03).
- يا بيعالجها مع بعض بس **كل واحدة أبطأ** (نفس الـ CPU متقسّم).

**مش هقولك النتيجة.** ده بالظبط اللي هتقيسه في Task 7، وهتقارن الوقت الكلي والـ tok/s.

### Libraries Supporting Async I/O
قايمة: **FastAPI** و Starlette و Sanic و Quart و Tornado (web)، و **uvicorn** و Hypercorn (ASGI servers)، و aiohttp و **HTTPX** و websockets و aiosmtplib (networking)، و **SQLAlchemy** (async) و Tortoise و Gino و PyMongo (databases)، و aiofiles و aiocache و APScheduler و **pytest-asyncio** (utilities).

**ليك:** FastAPI و uvicorn (Step 15)، و httpx (دلوقتي)، و pytest-asyncio (لو عايز تعمل tests لـ async functions بـ pytest).

## 11. Conclusion و FAQ
> 📍 sections *Conclusion* و *Frequently Asked Questions*

**الخلاصة:** اتعلمت الفرق بين نماذج الـ concurrency، و `async def`/`await`، و الـ event loop، و `asyncio.run` و `gather` و `create_task`، والـ chaining والـ queues، و `async for`/`async with`.

**الـ FAQ:** asyncio = concurrent code بـ async/await لـ I/O-bound في thread واحد، وغالباً أحسن من الـ threading في الـ I/O-bound (آلاف المهام من غير overhead)، وبتشغّل coroutine بـ `asyncio.run()` أو `create_task()`، والـ event loop بيدّي كل coroutine فرصة لما بيعمل `await`.

---

## 🧩 Concepts جديدة
اتضافت لـ [`docs/concepts.md`](../../../docs/concepts.md): **Concurrency مقابل Parallelism**، و **I/O-bound مقابل CPU-bound**، و **Coroutine و Event Loop**، و **Blocking Call في كود async**، و **`asyncio.gather` مقابل `as_completed`**، و **Producer/Consumer Queue (bounded concurrency)**، و **`return_exceptions=True`**.

## ❓ أسئلة فهم (Interview-style)

<details><summary>1. الـ asyncio بيشغّل الكود على كذا CPU core؟</summary>

لأ. asyncio = thread واحد في process واحد، بـ cooperative multitasking. ده concurrency مش parallelism: مهمة واحدة بس بتتنفذ في أي لحظة، بس لما مهمة بتستنى I/O (بـ `await`)، الـ event loop بيشغّل غيرها. للـ CPU-bound محتاج multiprocessing.
</details>

<details><summary>2. حطيت httpx.post(...) جوه async def وعملت gather على 10 منهم. ليه الوقت زي الـ sync بالظبط؟</summary>

لأن `httpx.post` (الـ sync API) **blocking**: بيوقف الـ event loop كله لحد ما الرد ييجي، فالـ coroutines بتتنفذ واحدة ورا التانية. `async def` لوحده مش بيخلّي الكود async. لازم `await client.post(...)` من `httpx.AsyncClient`، عشان الـ `await` هو اللي بيسلّم التحكم للـ loop وقت الانتظار. ونفس الكلام في الـ SDK: `AsyncAnthropic` مش `Anthropic`.
</details>

<details><summary>3. ناديت process_receipt(r) (async def) من غير await، والبرنامج خلص من غير error ومن غير نتيجة. ليه؟</summary>

لأن نداء coroutine function بيرجّع coroutine object بس، ومش بينفّذ حاجة لحد ما تعمل عليه `await` أو تشغّله في event loop (`asyncio.run`، أو `create_task` + await، أو `gather`). Python غالباً بيطلّع warning "coroutine ... was never awaited". دايماً دوّر على `await` ناقص لو حاجة async "مش بتحصل".
</details>

<details><summary>4. عندك 1,000 إيصال. ليه asyncio.gather(*[extract(r) for r in receipts]) فكرة وحشة؟ وتعمل إيه بدلها؟</summary>

لأنها بتبعت الـ 1,000 request في نفس اللحظة: على Claude هتضرب الـ rate limits والـ ramp limits (429 كتير)، وعلى Ollama local هتخنق الـ server (والـ queue الداخلي بتاعه). الحل: **bounded concurrency**، عن طريق `asyncio.Queue` بـ N consumers (pattern الـ producer/consumer في المقال)، فبيبقى فيه N requests بس في أي لحظة. وتختار N حسب الـ rate limits أو حسب `OLLAMA_NUM_PARALLEL`.
</details>

<details><summary>5. إمتى تستخدم gather وإمتى as_completed؟</summary>

`gather` لو محتاج **كل** النتايج **بنفس ترتيب** الـ inputs (مثلاً تقارن نتيجة كل إيصال بالـ expected بتاعه بالـ index). `as_completed` لو عايز تتعامل مع كل نتيجة **أول ما تخلص** (تطبع progress، أو تحفظ على طول، أو تبدأ خطوة تانية)، والترتيب بيبقى ترتيب الخلصان. وفي `as_completed` لازم تعرف كل نتيجة تخص أنهي input (ترجّعها مع الـ ID).
</details>

<details><summary>6. إيصال واحد من 15 عمل timeout جوه gather. إيه اللي بيحصل للـ 14 التانيين؟</summary>

by default، أول exception بيطلع من `gather` وإنت مش هتاخد النتايج (رغم إن باقي الـ coroutines ممكن تكون كملت). بـ `gather(..., return_exceptions=True)`، الـ exception بيرجع **كقيمة** في list النتايج مكان الإيصال ده، والـ 14 نتيجة التانيين موجودين، وإنت بتشيك `isinstance(r, Exception)`. وده المناسب للـ eval: الفشل نتيجة بتتسجل، مش سبب يوقف كل حاجة.
</details>

<details><summary>7. ليه الـ async ممكن مايسرّعش Ollama على جهازك بنفس قدر Claude API؟</summary>

لأن مع Claude الـ request I/O-bound من ناحيتك: الحساب بيحصل على سيرفرات Anthropic، فإنت بتستنى بس، والـ async بيخليك تستنى كذا request في نفس الوقت. مع Ollama على الـ CPU بتاعك، الحساب بيحصل على **نفس الجهاز**: الـ requests المتوازية بتتنافس على نفس الـ cores (أو Ollama بيحطها في queue حسب `OLLAMA_NUM_PARALLEL`)، فالوقت الكلي ممكن مايقلش كتير، والـ tok/s لكل request ممكن يقل. الـ async بيشيل انتظار الشبكة، مش حدود الـ hardware.
</details>
