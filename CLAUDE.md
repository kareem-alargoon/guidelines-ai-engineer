# Project Memory — AI Engineer Study Repo

## الهدف
الريبو ده لمذاكرة تخصص **AI Engineer** بالكامل، خطوة بخطوة حسب `ROADMAP.md`.

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
