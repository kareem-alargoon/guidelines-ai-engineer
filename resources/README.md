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

## 📥 المطلوب ترفعه دلوقتي (عشان نبدأ Step 01)

| الملف | المكان | إزاي تجيبه |
|---|---|---|
| 📘 *AI Engineering* — Chip Huyen | `books/ai-engineering-chip-huyen.pdf` | نسختك من الكتاب |
| 🎥 Karpathy — *Intro to Large Language Models* | `videos/01-karpathy-intro-to-llms.md` | من YouTube: تحت الفيديو **…more ← Show transcript**، انسخ الـ transcript كله **بالـ timestamps** والزقه في الملف |
| 📰 swyx — *The Rise of the AI Engineer* | `articles/01-swyx-rise-of-the-ai-engineer.pdf` | افتح المقال ← **Print ← Save as PDF** |

باقي المصادر بنرفعها **خطوة بخطوة** قبل ما نبدأ كل خطوة، مش مرة واحدة.

## 🏷️ تسمية الملفات
- **كتب:** `books/<title>-<author>.pdf` (مثال: `hands-on-llms-alammar.pdf`)
- **مقالات:** `articles/<step>-<author>-<short-title>.pdf` أو `.md` (مثال: `09-anthropic-contextual-retrieval.pdf`)
- **فيديوهات:** `videos/<step>-<author>-<short-title>.md`، وأول سطر فيه لينك الفيديو

## 📖 الكتب

| الكتاب | الدور | الحالة |
|---|---|:---:|
| 📘 **AI Engineering** — Chip Huyen (O'Reilly, 2025) | **الأساسي**: أغلب الخطوات مبنية عليه | ⬜ مستني الرفع |
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
