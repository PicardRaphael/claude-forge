---
titre: "Stack Python IA — Reference complete"
resume: "Guide complet dev IA en Python 2026 : SDKs agents, RAG, ML/DL, fine-tuning, structured output, vector stores, deployment, architecture projet. Pour proposer, auditer et optimiser tout projet IA en Python"
aliases:
  - stack python ia
  - python ai stack
  - python ai development
  - python llm stack
  - python chatbot stack
  - python agent stack
  - fastapi llm
  - pydantic ai stack
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://github.com/langchain-ai/langgraph"
  - "https://github.com/pydantic/pydantic-ai"
  - "https://github.com/crewaiinc/crewai"
  - "https://python.useinstructor.com"
  - "https://dspy.ai"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/python"
  - "#domaine/stacks"
---

## Decision rapide

Pour choisir le framework agent → [[agents-frameworks]] | [[index-architectures]]

| Projet Python | SDK recommande | Pourquoi |
|---------------|---------------|---------|
| Agents complexes, workflows durables | **LangGraph** | Checkpointing, HITL, time-travel, enterprise |
| Prototype multi-agent rapide | **CrewAI** | 20 lignes, role-based |
| Type-safe, production-grade | **Pydantic AI** | Validation Pydantic partout, DI, model-agnostic |
| Structured output fiable | **Instructor** | Wrap n'importe quel client + retry auto |
| Prompt optimization | **DSPy** | Compile prompts, +10-40% qualite |
| Claude-only, max performance | **Anthropic Agent SDK** | Prompt caching natif, subagents |
| OpenAI-only, handoffs simples | **OpenAI Agents SDK** | Guardrails, tracing, MCP |
| Google Cloud / Vertex | **Google ADK** | A2A natif, multi-langage |
| RAG document-heavy | **LlamaIndex** | Index hierarchiques, chunkers, retrievers |
| API serving | **FastAPI** | SSE/WebSocket natif, Pydantic, async |

## SDKs agents — detail

### LangGraph

Orchestration par graphe dirige, etat type, checkpointing natif.

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import AsyncPostgresSaver

agent = create_react_agent(
    model=ChatAnthropic(model="claude-sonnet-4-6"),
    tools=[lookup_order, search_kb, create_ticket],
    prompt="Tu es un assistant support client.",
)

checkpointer = AsyncPostgresSaver(conn_string)
app = agent  # compile avec checkpointer pour persistence

config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = await app.ainvoke({"messages": [("user", query)]}, config)
```

Voir [[architecture-langgraph]] pour supervisor, swarm, HITL.

### Pydantic AI

Type-safe, validation everywhere, dependency injection.

```python
from pydantic_ai import Agent
from pydantic import BaseModel, Field

class SupportResponse(BaseModel):
    answer: str = Field(description="Reponse au client")
    confidence: float = Field(ge=0, le=1)
    needs_escalation: bool
    ticket_id: str | None = None

agent = Agent(
    'anthropic:claude-sonnet-4-6',
    output_type=SupportResponse,
    instructions='Tu es un agent support. Reponds factuellement.',
    deps_type=SupportDeps,  # injection dependances
)

# Outil avec DI
@agent.tool
async def lookup_order(ctx: RunContext[SupportDeps], order_id: str) -> str:
    """Cherche le statut d'une commande."""
    return await ctx.deps.db.get_order(order_id)

result = await agent.run('Ou est ma commande #12345 ?', deps=SupportDeps(db=db))
print(result.output)  # SupportResponse type-safe
```

**Forces** : validation automatique, retry sur erreur de schema, 20+ providers, DI propre.

### Instructor

Wrap n'importe quel SDK (Anthropic, OpenAI, Google, Mistral, Cohere, Ollama) avec validation Pydantic + retry automatique.

```python
import instructor
from anthropic import Anthropic
from pydantic import BaseModel

client = instructor.from_anthropic(Anthropic())

class Classification(BaseModel):
    intent: str
    confidence: float
    entities: list[str]

result = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": user_query}],
    response_model=Classification,
    max_retries=3,  # retry auto si validation echoue
)
# result est un Classification garanti valide
```

### DSPy

"Program, don't prompt" — compile les prompts automatiquement. +10-40% qualite vs prompting manuel.

```python
import dspy

lm = dspy.LM('anthropic/claude-sonnet-4-6')
dspy.configure(lm=lm)

class SupportQA(dspy.Signature):
    """Reponds aux questions support client."""
    question: str = dspy.InputField()
    context: str = dspy.InputField()
    answer: str = dspy.OutputField()

# Module avec chain-of-thought
qa = dspy.ChainOfThought(SupportQA)

# Optimisation automatique des prompts
optimizer = dspy.MIPROv2(metric=answer_quality_metric)
optimized_qa = optimizer.compile(qa, trainset=training_data)
```

**Forces** : optimisation automatique, reproductible, evaluation integree.
**Limites** : learning curve, besoin de donnees d'entrainement, overkill pour chatbot simple.

### CrewAI

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="Chercheur", goal="Trouver l'info", tools=[search_kb])
writer = Agent(role="Redacteur", goal="Repondre clairement")

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, response_task],
    memory=True,
)
result = crew.kickoff(inputs={"query": user_message})
```

Voir [[architecture-crewai]] pour Flows, delegation, limites.

## RAG stack Python

| Composant | Dev | Production | Budget |
|-----------|-----|-----------|--------|
| **Embeddings API** | OpenAI `text-embedding-3-small` | Voyage AI | Cohere |
| **Embeddings local rapide** | `fastembed` (ONNX, Rust, no GPU) | idem | idem |
| **Embeddings local qualite** | `sentence-transformers` | idem (GPU) | — |
| **Vector store dev** | `chromadb` (in-process) | — | — |
| **Vector store prod** | Qdrant / pgvector | Qdrant Cloud ($40-80/mo) | pgvector ($30/mo) |
| **Chunking** | LangChain `RecursiveCharacterTextSplitter` | LlamaIndex node parsers | — |
| **Reranking** | Cohere Rerank | Jina Reranker | `flashrank` (local) |
| **Evaluation** | `ragas` | idem | — |
| **Framework RAG** | LlamaIndex (retrieval-first) | LangChain (workflow-first) | — |

```python
# RAG rapide avec LlamaIndex
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Comment annuler une commande ?")

# RAG avec fastembed + Qdrant (production)
from qdrant_client import QdrantClient
from fastembed import TextEmbedding

embedder = TextEmbedding("BAAI/bge-small-en-v1.5")
client = QdrantClient(url="http://localhost:6333")
# ... index et search
```

Pour les concepts RAG → [[rag-chunking]], [[rag-embeddings]], [[rag-vector-databases]], [[rag-reranking]].

## ML/DL stack (au-dela des LLMs)

| Besoin | Librairie | Notes |
|--------|----------|-------|
| Deep learning | **PyTorch** | Standard industrie 2026 |
| Training distribue | **DeepSpeed**, **FSDP** (PyTorch natif) | Multi-GPU |
| Fine-tuning LLM | **Unsloth** (rapide), **Axolotl** (flexible) | Voir [[MOC-Fine-Tuning]] |
| Serving LLM local | **vLLM**, **SGLang** | Production inference |
| Serving LLM dev | **Ollama** | `ollama run llama3.2` |
| Computer vision | **ultralytics** (YOLO), **torchvision** | — |
| NLP classique | **spaCy**, **transformers** | — |
| Data processing | **polars** (rapide), **pandas** | — |
| Experiment tracking | **Weights & Biases**, **MLflow** | — |
| Evaluation LLM | **ragas** (RAG), **inspect-ai** (agents) | — |

## Structured output — Pydantic

```python
from pydantic import BaseModel, Field
from enum import Enum

class Intent(str, Enum):
    billing = "billing"
    tech = "tech"
    faq = "faq"
    escalation = "escalation"

class ToolCall(BaseModel):
    tool_name: str
    arguments: dict
    reasoning: str = Field(description="Pourquoi cet outil")

class AgentResponse(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0, le=1)
    tool_calls: list[ToolCall] = []
    response: str
    needs_human: bool = False

# Principe : TOUJOURS valider avec Pydantic.
# Le provider garantit le format, pas la correction semantique.
# Instructor ou Pydantic AI ajoutent le retry automatique.
```

## Streaming — FastAPI

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import anthropic

app = FastAPI()

@app.post("/chat")
async def chat(request: ChatRequest):
    client = anthropic.AsyncAnthropic()

    async def generate():
        async with client.messages.stream(
            model="claude-sonnet-4-6",
            system=SYSTEM_PROMPT,
            messages=request.messages,
            max_tokens=1024,
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

# WebSocket (bidirectionnel)
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        async for chunk in stream_response(data["message"]):
            await websocket.send_json({"text": chunk})
```

## Deployment

| Plateforme | Cold start | GPU | Ideal pour |
|-----------|-----------|-----|-----------|
| **FastAPI + Docker** (Railway/Fly) | ~2s | Non | Chatbots, APIs LLM, majorite des cas |
| **Modal** | <1s GPU | **Oui** (A100/H100) | Embeddings local, fine-tuning, inference lourde |
| **AWS Lambda** (Mangum) | ~1-3s | Non | Event-driven, AWS ecosystem |
| **Replicate** | Variable | Oui | Serving modeles custom |
| **BentoML** | Variable | Oui | Packaging modeles ML |

```python
# Modal — GPU on demand
import modal

app = modal.App("embeddings")

@app.function(gpu="A100", image=modal.Image.debian_slim().pip_install("sentence-transformers"))
def embed(texts: list[str]) -> list[list[float]]:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-large-en-v1.5")
    return model.encode(texts).tolist()
```

## Architecture projet type

```
app/
  agents/          # Definitions agents (LangGraph graphs, CrewAI crews, Pydantic AI)
  tools/           # Fonctions outils + schemas Pydantic
  chains/          # Pipelines LLM (prompt chaining, evaluator-optimizer)
  prompts/         # Templates prompts (fichiers texte, Jinja2)
  memory/          # Conversation history, vector memory
  rag/             # Embedding, chunking, retrieval, reranking
  models/          # Pydantic data models (input/output)
  services/        # Logique metier (DB, APIs externes)
  api/             # FastAPI routers
  deps.py          # Dependency injection (FastAPI Depends)
  config.py        # Settings (pydantic-settings)
  main.py
scripts/
  eval/            # Evaluation scripts (ragas, custom metrics)
  ingest/          # Data ingestion pipelines
  fine_tune/       # Fine-tuning scripts
tests/
  agents/          # Tests agents (mocked LLM via instructor)
  tools/           # Tests outils (unit)
  rag/             # Tests retrieval (precision, recall)
  e2e/             # Tests end-to-end API
pyproject.toml     # uv/poetry, ruff config
Dockerfile
```

### Principes architecture 2026
1. **Prompts = config** — fichiers texte dans `/prompts`, pas dans le code Python
2. **Tools = frontiere** — chaque outil a un schema Pydantic, validation stricte
3. **DI partout** — FastAPI `Depends` + Pydantic AI `deps_type` pour testabilite
4. **Type annotations** — `ruff` + `mypy`/`pyright` sur tout le codebase
5. **Eval-driven** — metriques RAGAS + custom avant chaque deploy
6. **uv** pour package management (10-100x plus rapide que pip)

## Optimisations performance

### Tokens
- **Prompt caching** : system prompt statique → -90% (Claude), -50-90% (OpenAI)
- **Structured output** : Pydantic force reponses compactes
- **DSPy** : optimisation automatique des prompts (+10-40% qualite)
- **Deferred tools** : `defer_loading: true` (Claude) pour > 10 outils

### Latence
- **Async everywhere** : `AsyncAnthropic`, `ainvoke`, FastAPI async handlers
- **Parallel tool calls** : outils independants en parallele
- **fastembed** : embeddings ONNX sans GPU, ~5x plus rapide que sentence-transformers CPU
- **Connection pooling** : `httpx.AsyncClient` reutilise les connexions

### Cout
- **Model tiering** : Haiku/Flash-Lite pour classify, Sonnet pour generate
- **Batch API** : -50% sur tous les providers
- **Embeddings local** : fastembed elimine les couts API embeddings
- **vLLM** : serving local pour modeles open-source (eliminate le cout API)

### Qualite
- **Instructor retry** : re-genere si validation Pydantic echoue (max_retries=3)
- **Evaluator-optimizer** : boucle generate-evaluate (RAGAS faithfulness >= 0.9)
- **Reranking** : Cohere/Jina apres retrieval (+15-25% precision)
- **Hybrid search** : vector + keyword (BM25) pour meilleur recall

## Observability, Memory, Guardrails, MCP

### Observability / Tracing
| Outil | Usage |
|-------|-------|
| **Langfuse** (open-source) | Tracing LLM complet, cout, latence, evals, self-hosted possible |
| **LangSmith** | Natif LangChain/LangGraph, debugging time-travel |
| **Arize Phoenix** (open-source) | Traces + embeddings visualization |
| **Helicone** | Proxy HTTP zero-code, analytics |
| **Braintrust** | Evals + tracing + datasets |
| **OpenTelemetry** | Standard ouvert, Pydantic AI l'utilise nativement |

### Memory frameworks
| Outil | Usage |
|-------|-------|
| **Mem0** | Memory-as-a-service, multi-user, SDK Python natif |
| **Zep** | Long-term memory, fact extraction, temporal knowledge |
| **Letta/MemGPT** | Self-editing memory, agent autonome |
| **LangGraph Store** | Cross-thread persistence (MongoDB, InMemory) |
| **CrewAI Memory** | Unified Memory class (LanceDB) |

### Guardrails / Safety
| Outil | Usage |
|-------|-------|
| **NeMo Guardrails** (NVIDIA) | Rails YAML, topical/safety/jailbreak |
| **Llama Guard** | Classification safety open-source (local) |
| **Lakera Guard** | API cloud, prompt injection detection |
| **Pydantic validation** | Schema validation + retry (via Instructor) |
| **OpenAI Agents SDK Guardrails** | Input/output tripwire + tool validation |

### MCP (Model Context Protocol)
97M downloads SDK/mois. Standard pour outils agent.
```python
# LangGraph + MCP
from langchain_mcp import MCPToolkit
toolkit = MCPToolkit(server_url="http://localhost:8091")
tools = toolkit.get_tools()

# Anthropic SDK natif
tools = [{"type": "mcp", "server": {"url": "..."}}]
```

### Provider routing / Fallback
| Outil | Usage |
|-------|-------|
| **LiteLLM** | Proxy unifie 100+ providers, fallback, load balance |
| **Portkey** | AI Gateway, cache, analytics, budget limits |
| **OpenRouter** | API unifiee multi-provider, pricing optimise |

### Agent sandboxing
| Outil | Usage |
|-------|-------|
| **E2B** | Sandboxes cloud pour code execution agent |
| **Modal** | GPU sandboxes on-demand |
| **Daytona** | Dev environments isoles |

## Audit Checklist — Anti-patterns a detecter

| Symptome dans le repo | Diagnostic | Correction |
|---|---|---|
| `invoke()` dans handler FastAPI async | Blocking event loop | `ainvoke()` partout |
| Pas de retry sur structured output | Hallucinations silencieuses | `Instructor(max_retries=3)` |
| ChromaDB en prod > 5 users | Write-lock contention | Migrer Qdrant/pgvector |
| System prompt dans le code Python | Non-iterable sans deploy | Externaliser `/prompts/` (Jinja2) |
| `from langchain import ...` (monolithique) | Import lent, deps inutiles | `from langchain_anthropic import ...` |
| Pas de tracing/observability | Impossible diagnostiquer prod | Langfuse ou OpenTelemetry |
| `pip install` sans lock | Deps non reproductibles | `uv` + `uv.lock` |
| Embeddings API sans cache | Cout proportionnel au volume | `fastembed` local ou cache Redis |
| Vector store sans reranking | Recall faible queries ambigues | Cohere/Jina reranker |
| Pas de rate limiting | DDoS, cout explosif | FastAPI middleware + Redis |
| `sentence-transformers` en prod sans GPU | Latence embeddings > 1s | `fastembed` (ONNX, 5x plus rapide CPU) |
| Historique messages illimite | Context window overflow | Truncate + summarize vieux messages |
| Pas de tests sur tools/agents | Regression silencieuse | Mocked LLM via Instructor |
| `black`+`isort`+`flake8` separes | 3 configs, lent | `ruff` unique (100x plus rapide) |
| Pas de prompt caching provider | Cout x10 sur system prompts | Activer cache Anthropic/OpenAI |

## Diagnostic optimisation (flux)

### Si latence p95 > 3s
1. Streaming actif ? → `client.messages.stream()` + FastAPI `StreamingResponse`
2. `invoke()` vs `ainvoke()` ? → async obligatoire sous FastAPI
3. Model routing ? → Haiku pour classify, Sonnet pour generate
4. Outils paralleles ? → parallel tool calls actifs
5. Embeddings lents ? → `fastembed` (ONNX) vs `sentence-transformers`
6. Connection pooling ? → `httpx.AsyncClient` reutilise connexions

### Si cout/conversation > $0.02
1. Prompt caching actif ? → system prompt statique → cache hit (-90%)
2. Batch API applicable ? → traitement asynchrone = -50%
3. Model tiering ? → Flash-Lite $0.10/MTok pour volume
4. Embeddings local ? → `fastembed` elimine couts API embeddings
5. Historique tronque ? → summarize, garder N derniers messages
6. vLLM/Ollama ? → serving local pour open-source (elimine cout API)

### Si qualite reponse < 80% satisfaction
1. System prompt specifique ? → role/regles/exemples/escalade
2. RAG en place ? → retrieval avant generation
3. Reranking ? → +15-25% precision post-retrieval
4. Structured output ? → Pydantic/Instructor force reponses coherentes
5. DSPy ? → optimisation automatique prompts (+10-40%)
6. Evaluation metriques ? → RAGAS faithfulness >= 0.9, inspect-ai pour agents

### Si scaling > 1000 req/min
1. Connection pooling ? → `httpx.AsyncClient` persistent
2. Provider routing ? → LiteLLM load balance multi-providers
3. Cache reponses ? → Redis pour questions frequentes
4. Batch processing ? → Batch API pour non-temps-reel
5. Auto-scaling ? → Modal/Lambda pour burst, FastAPI pour steady

## Gotchas Python IA

- `asyncio` + FastAPI : utiliser `ainvoke()` pas `invoke()` — sinon blocking
- `sentence-transformers` telecharge des Go de modeles au premier import — `fastembed` = alternative legere
- ChromaDB in-process = write-lock sous concurrence — Qdrant en prod
- LangChain imports lents : `from langchain_anthropic import ChatAnthropic` pas `from langchain import ...`
- `uv` remplace pip/poetry — 10-100x plus rapide, resolver fiable
- `ruff` remplace black+isort+flake8 — un seul outil, plus rapide

## Liens

- [[MOC-Techniques]]
- [[stack-typescript-ia]] — Equivalent TypeScript
- [[index-architectures]] — Decision pattern + framework chatbot
- [[MOC-Fine-Tuning]] — Guide complet fine-tuning
- [[rag-chunking]], [[rag-embeddings]], [[rag-vector-databases]] — Concepts RAG
- [[agents-frameworks]] — Comparatif frameworks agents
- [[python-ref]] — Skill Python best practices
