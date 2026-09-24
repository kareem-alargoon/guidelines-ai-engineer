# Project Memory — AI Engineer Study Repo

## الهدف
الريبو ده لمذاكرة تخصص **AI Engineer** بالكامل، خطوة بخطوة حسب `ROADMAP.md`.

## ⚠️ النطاق: AI Engineer مش ML Engineer
- **AI Engineer** بيبني تطبيقات فوق موديلات جاهزة: LLM APIs، prompts، RAG، embeddings، vector DBs، tool use، agents، MCP، evals، deployment.
- **ممنوع نخلط بـ ML Engineer**: مفيش تدريب موديلات من الصفر، ولا رياضيات الـ ML (linear algebra، gradients، backprop)، ولا scikit-learn/PyTorch training، ولا بناء neural networks.
- لو محتاجين نلمس حاجة من دول (زي cosine similarity أو fine-tuning) بنشرحها **على مستوى الاستخدام والقرار** بس، مش النظرية الرياضية ولا تفاصيل التدريب.

## خلفية المتعلّم
- جاي من **backend development**: خبرة في **Laravel (PHP)** و Java، وفاهم APIs و HTTP requests و integrations كويس — متشرحهمش من الأول.
- خلّص كورس Python وعارف أساسياته و OOP.
- **جديد على مجال الـ AI**: لازم المفاهيم تتشرح الأول (الموديل بيعمل إيه وليه) قبل الأدوات والـ setup والكود.
- استخدم **تشبيهات من Laravel** لما تفيد (مثلاً: `.env` / `DB_CONNECTION` ↔ اختيار الـ LLM provider، `composer` ↔ `uv`، Http facade ↔ `httpx`، session ↔ chat history).
- مهتم بموضوع **الداتا الحساسة و local LLMs** — اعرض دايماً البديل الـ local (Ollama) جنب الـ cloud APIs.
- أدوات Python الأكثر تقدماً (`async`، `httpx`، `pydantic`، `FastAPI`، `uv`) بنشرحها جوه الخطوة اللي بتحتاجها لما تظهر لأول مرة.
- متحطش أوامر terminal معقدة من غير ما تشرحها سطر بسطر.

## القواعد الأساسية (لازم تتبع دايماً)

1. **كل خطوة في الـ roadmap = branch لوحده** باسم `step/NN-short-name` (الأسماء الرسمية في `ROADMAP.md`).
   - الـ branch بيتفرّع من `main` دايماً.
   - لو الـ session اتحدد لها branch تاني (زي `claude/...`) استخدمه، بس الشغل يبقى لخطوة واحدة بس.
2. **كل branch جواه فولدر واحد**: `steps/NN-short-name/` — ممنوع تعديل فولدرات خطوات تانية (عشان الـ merge يبقى نضيف).
3. **الملف الأهم في كل branch**: `steps/NN-short-name/README.md` — شرح كامل لكل نقطة/concept مع مثال أو تطبيق عملي، ماشي على `templates/LESSON_TEMPLATE.md`.
4. الأمثلة القابلة للتشغيل في `steps/NN-short-name/examples/` (Python افتراضياً)، ولو فيه dependencies يتعمل `requirements.txt` جوه الفولدر.
5. `main` = الفهرس + القوالب + القواعد + الخطوات اللي خلصت واتعملها merge.
6. بعد ما خطوة تخلص: نحدّث حالتها في `ROADMAP.md` (⬜ → 🟡 → ✅).

## أسلوب الشرح
- **اللغة:** عربي (عامية مصرية بسيطة وواضحة)، والمصطلحات التقنية تفضل **بالإنجليزي** (مثلاً: embeddings, context window, fine-tuning).
- الترتيب لكل concept: يعني إيه ← إزاي بيشتغل ← مثال عملي بالكود ← أخطاء شائعة.
- الشرح يبدأ من البساطة ويعمّق تدريجياً، مع تشبيهات من الواقع لما تفيد.
- كل ملف لازم يحتوي: أهداف، شرح الـ concepts، تطبيق عملي (hands-on)، تمارين، أسئلة مراجعة بأسلوب الانترفيوهات، cheat sheet، مصادر.
- الأمثلة لازم تكون صحيحة وتشتغل فعلاً؛ اختبر الكود قبل الـ commit لما يكون ممكن.
- عند استخدام LLM APIs: الافتراضي Anthropic Claude API بأحدث الموديلات، مع ذكر البدائل.
- مفيش API keys في الكود أبداً — استخدم environment variables و `.env` (موجود في `.gitignore`).

## Workflow كل Session جديدة
1. اقرأ `ROADMAP.md` واعرف الخطوة المطلوبة.
2. اعمل/انتقل للـ branch الخاص بيها من `main`.
3. اكتب `steps/NN-name/README.md` + `examples/`.
4. حدّث حالة الخطوة في `ROADMAP.md` لـ 🟡.
5. Commit بـ message واضحة (مثال: `step 01: add introduction lesson`) و push على نفس الـ branch.
