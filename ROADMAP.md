# 🗺️ AI Engineer Roadmap

> **النطاق:** AI Engineer مش ML Engineer. بنبني تطبيقات ومنتجات فوق موديلات جاهزة (cloud أو local)، ومش بندرّب موديلات ولا بنذاكر رياضيات الـ ML.
>
> **الطريقة:** كل خطوة ليها **مصادر حقيقية** بتتقري بالترتيب ← شرح لكل مصدر في `notes/` ← تاسكات بتكتبها بإيدك في `work/` ← review على الـ PR. التفاصيل في [`CLAUDE.md`](CLAUDE.md)، وفهرس المصادر في [`resources/README.md`](resources/README.md).
>
> **الكتاب الأساسي (العمود الفقري):** 📘 *AI Engineering* — Chip Huyen (O'Reilly, 2025)
> **كتاب مساعد:** 📗 *Hands-On Large Language Models* — Jay Alammar & Maarten Grootendorst (O'Reilly, 2024)

## الملخص

| الحالة | # | Branch | الموضوع | المصدر الأساسي |
|:---:|:---:|---|---|---|
| 🟡 | 01 | `step/01-introduction` | مقدمة: يعني إيه AI Engineering | 📘 Ch.1 + Karpathy |
| ⬜ | 02 | `step/02-llm-fundamentals` | الـ LLMs من منظور المستخدم | 📘 Ch.2 + Karpathy Deep Dive |
| ⬜ | 03 | `step/03-models-and-providers` | الموديلات والـ Providers (Cloud vs Local) | 📘 Ch.4 (Model Selection) |
| ⬜ | 04 | `step/04-llm-apis` | التعامل مع LLM APIs من Python | Anthropic Course + docs |
| ⬜ | 05 | `step/05-prompt-engineering` | Prompt Engineering | 📘 Ch.5 + Anthropic Tutorial |
| ⬜ | 06 | `step/06-ai-safety` | الأمان والـ Guardrails | 📘 Ch.5 (Defensive) + OWASP |
| ⬜ | 07 | `step/07-embeddings` | Embeddings | 📗 Ch.2 + Simon Willison |
| ⬜ | 08 | `step/08-vector-databases` | Vector Databases | pgvector + Chroma docs |
| ⬜ | 09 | `step/09-rag` | RAG | 📘 Ch.6 + 📗 Ch.8 + Contextual Retrieval |
| ⬜ | 10 | `step/10-tool-use` | Tool Use / Function Calling | Anthropic Course + docs |
| ⬜ | 11 | `step/11-ai-agents` | AI Agents | 📘 Ch.6 + Building Effective Agents |
| ⬜ | 12 | `step/12-mcp` | Model Context Protocol | MCP docs + DeepLearning.AI course |
| ⬜ | 13 | `step/13-multimodal` | Multimodal AI | 📗 Ch.9 + Anthropic Vision/PDF docs |
| ⬜ | 14 | `step/14-evaluation` | Evaluation و Testing | 📘 Ch.3–4 + Hamel Husain |
| ⬜ | 15 | `step/15-llmops-deployment` | LLMOps و Deployment | 📘 Ch.9–10 + Applied LLMs |
| ⬜ | 16 | `step/16-capstone` | Capstone: tool كاملة تبنيها لوحدك | كل اللي فات |

**الحالات:** ⬜ لسه · 🟡 شغّالين عليه · ✅ خلص (المواد + PR الكود بتاعك اتعملهم merge)

**رموز المصادر:** 📘 الكتاب الأساسي · 📗 الكتاب المساعد · 📰 مقال · 🎥 فيديو · 📚 docs رسمية · 🎓 كورس مجاني

---

## تفاصيل كل خطوة ومصادرها
المصادر مترتبة **بترتيب القراية**. اللي عليه ⭐ أساسي، والباقي تعميق.

### 01 — مقدمة: يعني إيه AI Engineering
- ⭐ 📘 **Ch.1** — *Introduction to Building AI Applications with Foundation Models*
- ⭐ 🎥 **Andrej Karpathy — [Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g)** (ساعة)
- 📰 **swyx — [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer)**: المقال اللي سمّى الوظيفة

### 02 — الـ LLMs من منظور المستخدم
- ⭐ 📘 **Ch.2** — *Understanding Foundation Models* (training data، الـ sampling، الـ temperature، الـ hallucination). أجزاء الـ architecture والـ training هنعدّي عليها على مستوى الفكرة
- ⭐ 🎥 **Karpathy — [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)** (3.5 ساعة، على أجزاء)
- 🎥 **3Blue1Brown — [Large Language Models explained briefly](https://www.youtube.com/watch?v=LPZh9BOjkQs)**
- 📚 **Anthropic docs — [Context windows](https://docs.claude.com/en/docs/build-with-claude/context-windows)**

### 03 — الموديلات والـ Providers (Cloud vs Local)
- ⭐ 📘 **Ch.4** — section *Model Selection* (build vs buy، open vs closed، الـ benchmarks)
- ⭐ 📚 **[Ollama docs](https://docs.ollama.com/)**: تشغيل open-weight models local
- 📚 **[Anthropic — Models overview](https://docs.claude.com/en/docs/about-claude/models/overview)**
- 📰 **[Artificial Analysis](https://artificialanalysis.ai/)** و **[LMArena](https://lmarena.ai/)**: مقارنة الموديلات (quality / cost / speed)

### 04 — التعامل مع LLM APIs من Python
- ⭐ 🎓 **[Anthropic Courses](https://github.com/anthropics/courses)** — *Anthropic API Fundamentals*
- ⭐ 📚 **Anthropic docs**: Messages API، Streaming، Structured outputs، Prompt caching
- 📚 **Ollama API** (نفس الأفكار على موديل local)
- 📚 أدوات Python اللي هتظهر: **[httpx](https://www.python-httpx.org/)**، **[pydantic](https://docs.pydantic.dev/latest/)**، **[uv](https://docs.astral.sh/uv/)**، و 📰 **Real Python — [Async IO in Python](https://realpython.com/async-io-python/)**

### 05 — Prompt Engineering
- ⭐ 📘 **Ch.5** — *Prompt Engineering*
- ⭐ 🎓 **[Anthropic Courses](https://github.com/anthropics/courses)** — *Prompt Engineering Interactive Tutorial* ثم *Real World Prompting*
- 📚 **[Anthropic — Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)**
- 📰 **Lilian Weng — [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)**

### 06 — الأمان والـ Guardrails
- ⭐ 📘 **Ch.5** — section *Defensive Prompt Engineering*
- ⭐ 📰 **[OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)**
- 📰 **Simon Willison — [Prompt injection series](https://simonwillison.net/series/prompt-injection/)**
- 📚 **Anthropic — Mitigate jailbreaks & prompt injections** (docs)

### 07 — Embeddings
- ⭐ 📗 **Ch.2** — *Tokens and Embeddings*
- ⭐ 📰 **Simon Willison — [Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/)**
- 📰 **Jay Alammar — [The Illustrated Word2vec](https://jalammar.github.io/illustrated-word2vec/)** (الفكرة بالرسم، من غير رياضيات)
- 📚 **[Sentence Transformers](https://sbert.net/)**: embeddings local

### 08 — Vector Databases
- ⭐ 📚 **[pgvector](https://github.com/pgvector/pgvector)**: vectors جوه PostgreSQL اللي إنت عارفه
- ⭐ 📚 **[Chroma docs](https://docs.trychroma.com/)**
- 📰 **Pinecone — [What is a Vector Database?](https://www.pinecone.io/learn/vector-database/)**
- 📚 **[Qdrant — Concepts](https://qdrant.tech/documentation/concepts/)**

### 09 — RAG
- ⭐ 📘 **Ch.6** — الجزء الأول: *RAG*
- ⭐ 📗 **Ch.8** — *Semantic Search and Retrieval-Augmented Generation*
- ⭐ 📰 **Anthropic — [Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)**
- 📘 **Ch.7** — *Finetuning*: بس الجزء بتاع **إمتى** تعمل finetuning مقابل RAG (قرار، مش تنفيذ)
- 📰 **Eugene Yan — [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)**
- 📰 **Jason Liu — [Systematically Improving Your RAG](https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/)**

### 10 — Tool Use / Function Calling
- ⭐ 🎓 **[Anthropic Courses](https://github.com/anthropics/courses)** — *Tool Use*
- ⭐ 📚 **Anthropic docs — Tool use**
- 📰 **Anthropic — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)**
- 📚 **Ollama — Tool calling** (نفس الفكرة local)

### 11 — AI Agents
- ⭐ 📰 **Anthropic — [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)**
- ⭐ 📘 **Ch.6** — الجزء التاني: *Agents*
- 📰 **Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)**
- 📰 **Anthropic — [How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system)**
- 📰 **Lilian Weng — [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)**
- 📰 **Paper — [ReAct](https://arxiv.org/abs/2210.03629)** (Yao et al.): الفكرة اللي أغلب الـ agents مبنية عليها

### 12 — Model Context Protocol (MCP)
- ⭐ 📚 **[MCP docs](https://modelcontextprotocol.io/)**: Introduction ← Architecture ← Build a server ← Build a client
- ⭐ 🎓 **DeepLearning.AI — [MCP: Build Rich-Context AI Apps with Anthropic](https://www.deeplearning.ai/short-courses/mcp-build-rich-context-ai-apps-with-anthropic/)**
- 📚 **[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)**

### 13 — Multimodal AI
- ⭐ 📗 **Ch.9** — *Multimodal Large Language Models*
- ⭐ 📚 **Anthropic docs — Vision + PDF support**
- 📚 **[Whisper](https://github.com/openai/whisper)**: Speech-to-Text local

### 14 — Evaluation و Testing
- ⭐ 📘 **Ch.3** — *Evaluation Methodology*
- ⭐ 📘 **Ch.4** — *Evaluate AI Systems*
- ⭐ 📰 **Hamel Husain — [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)**
- 📰 **Hamel Husain & Shreya Shankar — [LLM Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)**
- 📰 **Eugene Yan — [Evaluating LLM-Evaluators (LLM-as-Judge)](https://eugeneyan.com/writing/llm-evaluators/)**
- 🎓 **[Anthropic Courses](https://github.com/anthropics/courses)** — *Prompt Evaluations*

### 15 — LLMOps و Deployment
- ⭐ 📘 **Ch.10** — *AI Engineering Architecture and User Feedback*
- ⭐ 📰 **[What We've Learned From A Year of Building with LLMs](https://applied-llms.org/)** (Applied LLMs)
- 📘 **Ch.9** — *Inference Optimization* (من منظور الـ AI Engineer: latency، cost، caching)
- 📚 **[FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)**، **Docker — Get started**، **[vLLM](https://docs.vllm.ai/)** (self-hosting في الـ production)

### 16 — Capstone
tool كاملة **تختارها وتبنيها لوحدك**: RAG + Tools/Agents + Evals + Deployment، على داتا حقيقية (مثلاً documents شغلك)، وتشتغل **local** أو **cloud** من الـ config. أنا بس بعمل review.

---

> **ليه مش بنقرا الكتاب كله؟** الفصل 8 (*Dataset Engineering*) وأجزاء من الفصل 7 (*Finetuning*) أقرب لشغل الـ ML Engineer، فبناخد منهم القرارات بس. لو حبيت تقراهم كاملين كتعميق، ممتاز.
