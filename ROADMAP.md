# 🗺️ AI Engineer Roadmap

كل خطوة = **branch لوحده** متفرّع من `main`، وجواه ملف الشرح `steps/<NN-name>/README.md`.

> **نطاق الـ roadmap:** ده AI Engineer مش ML Engineer. يعني بنبني تطبيقات ومنتجات فوق موديلات جاهزة (pre-trained / foundation models) عن طريق الـ APIs والـ prompts والـ RAG والـ agents. مش بندرّب موديلات، ومش بنذاكر رياضيات الـ ML أو الـ deep learning من الصفر.
>
> **المتطلبات اللي خلصت:** ✅ أساسيات Python + OOP. الأدوات العملية زي `async` و`httpx` و`pydantic` و`FastAPI` هنتعلمها جوه الخطوات اللي هنحتاجها فيها.

| الحالة | # | Branch | الموضوع | أهم النقاط |
|:---:|:---:|---|---|---|
| ⬜ | 01 | `step/01-introduction` | مقدمة للـ AI Engineering | مين هو الـ AI Engineer، الفرق بينه وبين ML Engineer و Data Scientist، شكل الـ AI app، تجهيز البيئة (uv, .env, API keys) |
| ⬜ | 02 | `step/02-llm-fundamentals` | أساسيات الـ LLMs (من منظور المستخدم) | Tokens، Context window، Temperature/Top-p، Hallucination، Knowledge cutoff، قيود الموديلات |
| ⬜ | 03 | `step/03-models-and-providers` | الموديلات والـ Providers | Closed vs Open models، Anthropic/OpenAI/Google، Hugging Face، Ollama (local)، اختيار الموديل (quality/cost/latency) |
| ⬜ | 04 | `step/04-llm-apis` | التعامل مع LLM APIs | Claude API، Messages & roles، System prompt، Streaming، Structured output (pydantic)، async، Rate limits، Prompt caching |
| ⬜ | 05 | `step/05-prompt-engineering` | Prompt Engineering | Zero/Few-shot، Chain-of-Thought، Role prompting، XML tags، Prompt chaining، Prompt templates |
| ⬜ | 06 | `step/06-ai-safety` | الأمان والـ Guardrails | Prompt injection، Jailbreaks، Input/Output validation، Content moderation، Privacy (PII)، Responsible AI |
| ⬜ | 07 | `step/07-embeddings` | Embeddings | يعني إيه embedding، Embedding APIs، Semantic search، Cosine similarity (عملياً)، Clustering |
| ⬜ | 08 | `step/08-vector-databases` | Vector Databases | Chroma، pgvector، Qdrant/Pinecone، Indexing، Metadata filtering |
| ⬜ | 09 | `step/09-rag` | RAG | Chunking، Retrieval، Re-ranking، Hybrid search، Advanced RAG، إمتى Prompting vs RAG vs Fine-tuning |
| ⬜ | 10 | `step/10-tool-use` | Tool Use / Function Calling | تعريف الـ tools، JSON schema، Tool loop، Error handling |
| ⬜ | 11 | `step/11-ai-agents` | AI Agents | Agent loop، ReAct، Planning، Memory، Multi-agent، Agent SDKs و Frameworks |
| ⬜ | 12 | `step/12-mcp` | Model Context Protocol | MCP architecture، Servers/Clients، Tools/Resources/Prompts، بناء MCP server |
| ⬜ | 13 | `step/13-multimodal` | Multimodal AI | Vision، Image generation، Speech-to-Text / TTS، التعامل مع PDFs و Documents |
| ⬜ | 14 | `step/14-evaluation` | Evaluation و Testing | Evals، LLM-as-a-judge، Golden datasets، Regression testing للـ prompts |
| ⬜ | 15 | `step/15-llmops-deployment` | LLMOps و Deployment | FastAPI، Docker، Observability/Tracing، Cost & Latency، Caching، Monitoring |
| ⬜ | 16 | `step/16-capstone` | Capstone Project | مشروع end-to-end: RAG + Agents + Tools + Evals + Deployment |

**الحالات:** ⬜ لسه، 🟡 شغّالين عليه، ✅ خلص واتعمله merge على `main`
