# 🤖 AI Engineer — Study Guide

ريبو لمذاكرة تخصص **AI Engineer** خطوة بخطوة، شرح بالعربي مع أمثلة وتطبيقات عملية.

## 🌳 طريقة تنظيم الريبو

- **`main`**: الفهرس — فيه الـ roadmap والقوالب والقواعد، ومع الوقت بيتجمّع فيه كل الخطوات اللي خلصت.
- **كل خطوة في الـ roadmap = branch لوحده** باسم `step/NN-name` (مثال: `step/01-introduction`).
- جوه كل branch فولدر `steps/NN-name/` فيه:
  - `README.md` ← **ملف الشرح الأساسي**: كل concept بالتفصيل + أمثلة + تطبيق + تمارين + أسئلة مراجعة.
  - `examples/` ← الكود اللي بيشتغل للأمثلة.

```
guidelines-ai-engineer/
├── README.md                 ← انت هنا
├── ROADMAP.md                ← خريطة الخطوات وحالة كل واحدة
├── CLAUDE.md                 ← ذاكرة المشروع وقواعد الشغل
├── templates/
│   └── LESSON_TEMPLATE.md    ← القالب اللي كل ملف شرح ماشي عليه
└── steps/                    ← بتتملي من الـ branches بعد الـ merge
    └── 01-introduction/
        ├── README.md
        └── examples/
```

## 🔁 الـ Workflow لكل خطوة

1. نفتح branch جديد من `main`: `git checkout main && git pull && git checkout -b step/NN-name`
2. نكتب `steps/NN-name/README.md` على القالب + الأمثلة في `examples/`.
3. نذاكر ونحل التمارين.
4. نعمل merge على `main` (PR) ونعلّم الخطوة ✅ في `ROADMAP.md`.

## 🗺️ الـ Roadmap
شوف [ROADMAP.md](./ROADMAP.md).
