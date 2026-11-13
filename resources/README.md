# 📚 المصادر (Resources)

هنا بنحط **المصادر نفسها** اللي الـ roadmap مبني عليها، عشان الشرح اللي في `steps/NN/notes/` يبقى ماشي مع الأصل بالظبط.
الخريطة الكاملة (كل مصدر لأنهي خطوة وبأنهي ترتيب) في [`ROADMAP.md`](../ROADMAP.md).

```
resources/
├── books/      ← PDFs الكتب
├── articles/   ← المقالات محفوظة (PDF أو Markdown)
└── videos/     ← transcripts الفيديوهات (Markdown)
```

> ⚠️ **خلّي الريبو ده private.** الكتب بفلوس وعليها حقوق، ونسختك لاستخدامك الشخصي بس.
> ⚠️ GitHub مبيقبلش ملف أكبر من **100MB**. لو الـ PDF أكبر، قولّي ونستخدم Git LFS.

## 📂 الملفات الموجودة (لكل خطوة)

| الخطوة | الملفات |
|---|---|
| 01 | `books/ai-engineering-chip-huyen.pdf` (Ch.1)، و `videos/01-karpathy-intro-to-llms.md`، و `articles/01-swyx-rise-of-the-ai-engineer.pdf` |
| 02 | الكتاب (Ch.2)، و `videos/02-karpathy-deep-dive-into-llms.md`، و `videos/02-3blue1brown-llms-explained-briefly.md`، و `articles/02-anthropic-context-windows.pdf` |
| 03 | الكتاب (Ch.4 + ملحق Ch.3)، و `articles/03-ollama-*.pdf` (10 صفحات)، و `articles/03-anthropic-*.pdf` (4 صفحات)، و `articles/03-artificial-analysis-*` (3 صفحات، `.md` و `.pdf`)، و `articles/03-lmarena-*` (صفحتين) — كلهم snapshot يوم 2026-11-13 |

باقي المصادر بنرفعها **خطوة بخطوة** قبل ما نبدأ كل خطوة، مش مرة واحدة.

> 💡 **صفحات الـ leaderboards:** الـ PDF بيطلع ناقص (أول كام صف بس) لأن الجداول بتتحمّل بالـ JavaScript. عشان كده بنحفظها كمان `.md` (`Ctrl+A` ← `Ctrl+C` ← paste)، والـ `.md` هو اللي بنشرح منه.

## 🏷️ تسمية الملفات
- **كتب:** `books/<title>-<author>.pdf` (مثال: `hands-on-llms-alammar.pdf`)
- **مقالات:** `articles/<step>-<author>-<short-title>.pdf` أو `.md` (مثال: `09-anthropic-contextual-retrieval.pdf`)
- **فيديوهات:** `videos/<step>-<author>-<short-title>.md`، وأول سطر فيه لينك الفيديو

## 📖 الكتب

| الكتاب | الدور | الحالة |
|---|---|:---:|
| 📘 **AI Engineering** — Chip Huyen (O'Reilly, 2025) | **الأساسي**: أغلب الخطوات مبنية عليه | ✅ موجود |
| 📗 **Hands-On Large Language Models** — Jay Alammar & Maarten Grootendorst (O'Reilly, 2024) | **مساعد**: Embeddings و RAG و Multimodal بالرسومات (Ch.2, 8, 9) | ⬜ مش محتاجينه قبل Step 07 |

### ليه الكتاب ده بالذات؟
*AI Engineering* هو المرجع الأشهر المكتوب **مخصوص للـ AI Engineer** مش للـ ML Engineer. بيتكلم عن بناء تطبيقات فوق foundation models: الـ evaluation، والـ prompting، والـ RAG، والـ agents، والـ architecture. وكاتبته Chip Huyen من أشهر الناس في المجال (كتبت قبله *Designing Machine Learning Systems*، وبتدرّس في Stanford).
وعندها ريبو مجاني فيه مصادر إضافية للكتاب: [chiphuyen/aie-book](https://github.com/chiphuyen/aie-book).

## 🎓 كورسات ومصادر مجانية بنرجعلها كتير
- **[Anthropic Courses](https://github.com/anthropics/courses)**: API Fundamentals، Prompt Engineering Tutorial، Real World Prompting، Prompt Evaluations، Tool Use
- **[Anthropic Engineering blog](https://www.anthropic.com/engineering)**: مقالات عملية عن الـ agents والـ tools والـ context
- **[Anthropic docs](https://docs.claude.com/)** و **[Ollama docs](https://docs.ollama.com/)**
- **[DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/)**: كورسات قصيرة (ساعة أو ساعتين) لكل موضوع
- **Blogs** بنرجعلها: [Simon Willison](https://simonwillison.net/)، [Eugene Yan](https://eugeneyan.com/)، [Hamel Husain](https://hamel.dev/)، [Lilian Weng](https://lilianweng.github.io/)

> **ملحوظة:** اللينكات دي مجمّعة من مصادر معروفة، بس البيئة اللي بشتغل منها مبتفتحش أغلب المواقع، فمقدرتش أتأكد من كل لينك واحد واحد. لو لقيت لينك بايظ قولّي وأصلّحه.
