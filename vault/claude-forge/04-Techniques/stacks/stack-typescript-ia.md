---
titre: "Stack TypeScript IA — Reference complete"
resume: "Guide complet dev IA en TypeScript 2026 : SDKs agents, RAG, streaming, structured output, vector stores, deployment edge, architecture projet. Pour proposer, auditer et optimiser tout projet IA en TS"
aliases:
  - stack typescript ia
  - typescript ai stack
  - ts ai development
  - vercel ai sdk
  - mastra framework
  - typescript llm
  - typescript chatbot stack
  - typescript agent stack
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://github.com/vercel/ai"
  - "https://github.com/mastra-ai/mastra"
  - "https://sdk.vercel.ai/docs"
  - "https://mastra.dev"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/typescript"
  - "#domaine/stacks"
---

## Decision rapide

Pour choisir le framework agent → [[agents-frameworks]] | [[index-architectures]]

| Projet TS | SDK recommande | Pourquoi |
|-----------|---------------|---------|
| Chat UI streaming (React/Next) | **Vercel AI SDK** | `useChat()`, SSE natif, Zod structured output |
| Multi-agent / workflows durables | **Mastra** | LangGraph-level en TS, RAG built-in, MCP |
| RAG document-heavy | **LlamaIndex.TS** | Index hierarchiques, node parsers, retrievers |
| Single-provider, controle max | **SDK provider** (Anthropic/OpenAI/Google) | Zero abstraction, zero overhead |
| Integrations massives | **LangChain.js** | 500+ integrations, port Python |

## SDKs agents — detail

### Vercel AI SDK (`ai`)

Provider-agnostic, streaming-first, React hooks natifs.

```typescript
import { streamText, generateObject, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// Streaming chatbot avec tools
const result = streamText({
  model: anthropic('claude-sonnet-4-6'),
  system: 'Tu es un assistant support client.',
  messages,
  tools: {
    lookupOrder: tool({
      description: 'Cherche le statut de commande',
      parameters: z.object({ orderId: z.string() }),
      execute: async ({ orderId }) => db.getOrder(orderId),
    }),
  },
});
return result.toDataStreamResponse();

// Structured output (type-safe)
const { object } = await generateObject({
  model: anthropic('claude-sonnet-4-6'),
  schema: z.object({
    intent: z.enum(['billing', 'tech', 'faq']),
    confidence: z.number(),
    summary: z.string(),
  }),
  prompt: `Classifie: ${userMessage}`,
});
// object.intent est type-safe (autocomplete)

// React client
const { messages, input, handleSubmit, isLoading } = useChat({
  api: '/api/chat',
});
```

**Forces** : streaming UI imbattable, Zod-native, provider-agnostic (Anthropic, OpenAI, Google, Mistral, Groq...).
**Limites** : pas de multi-agent, pas de workflows durables, pas de memoire cross-session.

### Mastra

Full-stack TS : agents, workflows durables, RAG, memory, evals, MCP. Du team Gatsby.

```typescript
import { Agent, createTool } from '@mastra/core';
import { z } from 'zod';

const searchTool = createTool({
  id: 'search',
  description: 'Recherche dans la KB',
  inputSchema: z.object({ query: z.string() }),
  execute: async ({ context }) => vectorSearch(context.query),
});

const agent = new Agent({
  name: 'support',
  model: anthropic('claude-sonnet-4-6'),
  instructions: 'Tu es un agent support.',
  tools: { search: searchTool },
  memory: true, // memoire cross-session
});

// Workflow durable (equivalent LangGraph)
const workflow = new Workflow({ name: 'support-pipeline' })
  .step('classify', classifyStep)
  .step('enrich', enrichStep, { after: 'classify' })
  .step('respond', respondStep, { after: 'enrich' })
  .commit();
```

**Forces** : LangGraph-level en TS pur, RAG built-in, serverless (Vercel/Cloudflare).
**Limites** : ecosysteme plus jeune que LangChain, moins d'integrations.

### Provider SDKs directs

```typescript
// Anthropic
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
const msg = await client.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 1024,
  system: 'Support client ACME.',
  messages: [{ role: 'user', content: query }],
  tools: toolDefs,
});

// OpenAI
import OpenAI from 'openai';
const client = new OpenAI();
const response = await client.responses.create({
  model: 'gpt-4.1',
  instructions: 'Support client.',
  input: query,
  tools: toolDefs,
});

// Google GenAI
import { GoogleGenAI } from '@google/genai';
const ai = new GoogleGenAI({ apiKey: '...' });
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: query,
  config: { tools: [{ functionDeclarations: toolDefs }] },
});
```

## RAG stack TypeScript

| Composant | Dev | Production | Budget |
|-----------|-----|-----------|--------|
| **Embeddings API** | OpenAI `text-embedding-3-small` | Voyage AI (meilleure qualite) | Cohere |
| **Embeddings local** | `@huggingface/transformers` | idem (ONNX, browser+Node) | idem |
| **Vector store** | ChromaDB (REST) | Qdrant Cloud ($40-80/mo) | pgvector (si deja Postgres) |
| **Chunking** | Mastra built-in | LlamaIndex.TS node parsers | LangChain.js splitters |
| **Reranking** | Cohere Rerank | Jina Reranker | — |
| **Framework RAG** | Mastra (built-in) | LlamaIndex.TS | — |

```typescript
// RAG avec Mastra
import { RAG } from '@mastra/rag';

const rag = new RAG({
  embedder: openaiEmbedder,
  vectorStore: qdrantStore,
  chunker: { strategy: 'recursive', chunkSize: 512, overlap: 50 },
});

await rag.ingest(documents);
const results = await rag.retrieve(query, { topK: 5 });
```

Pour les concepts RAG (strategies chunking, types embeddings, evaluation) → [[rag-chunking]], [[rag-embeddings]], [[rag-vector-databases]].

## Streaming patterns

### SSE (defaut 2026)

```typescript
// Next.js App Router
export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: anthropic('claude-sonnet-4-6'),
    messages,
  });
  return result.toDataStreamResponse();
}

// Client React
const { messages, input, handleSubmit } = useChat({ api: '/api/chat' });
```

### WebSocket (bidirectionnel)

Quand le client doit envoyer pendant le stream (cancel mid-stream, collaborative editing). Economise des tokens a scale (cancel frame vs attendre la fin).

### RSC (pause)

Vercel AI SDK RSC est **en pause**. Utiliser `useChat()` + SSE a la place.

## Type safety — Zod

```typescript
import { z } from 'zod';

// Schema outil (description = ce que le LLM voit)
const orderSchema = z.object({
  orderId: z.string().describe('ID de commande format #XXXXX'),
  includeHistory: z.boolean().optional().describe('Inclure historique de suivi'),
});

// Schema structured output
const classificationSchema = z.object({
  intent: z.enum(['billing', 'tech', 'faq', 'escalation']),
  confidence: z.number().min(0).max(1),
  entities: z.array(z.object({
    type: z.string(),
    value: z.string(),
  })),
});

// Principe : TOUJOURS valider avec Zod, meme si le provider garantit le schema.
// Le provider garantit le format, pas la correction semantique.
```

## Deployment

| Plateforme | Cold start | Cout | Ideal pour |
|-----------|-----------|------|-----------|
| **Vercel** | ~0ms (Edge) | Per-invocation | Next.js + AI SDK, chat apps |
| **Cloudflare Workers** | <10ms | CPU time | Agents stateful (Durable Objects), 330+ villes |
| **Bun** (self-hosted) | N/A | Fixe | Performance max, self-hosted |
| **AWS Lambda** | ~500ms | Per-invocation | Enterprise AWS |

**Cloudflare Durable Objects** = unique pour agents stateful edge (state persiste entre requetes sans DB externe).

## Architecture projet type

```
src/
  agents/          # Definitions agents (model, tools, instructions)
  tools/           # Implementations outils (Zod schema + execute)
  workflows/       # Orchestration multi-step (Mastra/LangGraph)
  prompts/         # System prompts (fichiers texte, iterables sans code)
  memory/          # Gestion contexte (messages, vector search)
  rag/             # Embedding, chunking, retrieval
  types/           # Interfaces TypeScript centralisees
  middleware/      # Auth, rate limiting, logging
  api/             # Route handlers
  index.ts
config/
tests/
  agents/          # Tests agents (mocked LLM)
  tools/           # Tests outils (unit)
  e2e/             # Tests end-to-end
```

### Principes architecture 2026
1. **Prompts = config, pas code** — fichiers texte dans `/prompts`, iterables sans deployer
2. **Tools = frontiere** — chaque outil a un schema Zod + validation explicite
3. **Memory en couches** — message array → vector search quand le contexte grandit
4. **Types centralises** — quand un schema change, l'impact est visible partout
5. **Provider-agnostic** — abstraire le provider derriere Vercel AI SDK ou Mastra

## Optimisations performance

### Tokens
- **Prompt caching** : system prompt statique → cache hit (Claude -90%, OpenAI -50-90%)
- **Streaming** : latence percue /3 a /5
- **Structured output** : Zod `generateObject()` force une reponse compacte
- **Deferred tools** : charger les definitions d'outils a la demande (> 10 outils)

### Latence
- **Edge deployment** : Cloudflare Workers <10ms cold start
- **Parallel tool calls** : outils independants en parallele
- **Model routing** : Haiku/Nano pour classify, Sonnet/4.1 pour generate
- **Connection pooling** : reutiliser les connexions HTTP/2 vers les providers

### Cout
- **Batch API** : -50% si latence 24h acceptable
- **Model tiering** : Gemini Flash-Lite ($0.10/MTok) pour volume eleve
- **Cache KV** : Cloudflare KV ou Vercel KV pour reponses frequentes

## Observability, Memory, Guardrails, MCP

### Observability / Tracing
| Outil | Usage |
|-------|-------|
| **Langfuse** (open-source) | Tracing LLM, cout par requete, latence, evals |
| **LangSmith** | Natif LangChain/LangGraph, tracing + debugging |
| **Helicone** | Proxy HTTP, zero-code, logs + analytics |
| **Braintrust** | Evals + tracing, dataset management |
| **Arize Phoenix** | Open-source, traces + embeddings viz |

### Memory frameworks
| Outil | Usage |
|-------|-------|
| **Mem0** | Memory-as-a-service, multi-user, cross-session |
| **Zep** | Long-term memory, fact extraction, temporal |
| **Letta/MemGPT** | Self-editing memory, agent autonome |
| **Mastra Memory** | Built-in si Mastra utilise |

### Guardrails / Safety
| Outil | Usage |
|-------|-------|
| **NeMo Guardrails** (NVIDIA) | Rails YAML, topical/safety/jailbreak |
| **Llama Guard** | Classification safety open-source |
| **Lakera Guard** | API, prompt injection detection |
| **Zod validation** | Schema validation sur outputs (natif TS) |

### MCP (Model Context Protocol)
97M downloads SDK/mois. Standard pour la decouverte et l'utilisation d'outils.
```typescript
// Mastra supporte MCP nativement
const agent = new Agent({
  tools: { ...mcpTools },  // outils MCP auto-decouverts
});

// Vercel AI SDK supporte aussi MCP via plugins
```

### Provider routing / Fallback
| Outil | Usage |
|-------|-------|
| **LiteLLM** | Proxy unifie 100+ providers, load balancing |
| **Portkey** | Gateway AI, fallback, caching, analytics |
| **OpenRouter** | API unifiee multi-provider |

### Agent sandboxing
| Outil | Usage |
|-------|-------|
| **E2B** | Sandboxes cloud pour execution code agent |
| **Cloudflare Durable Objects** | State + isolation edge |

## Audit Checklist — Anti-patterns a detecter

| Symptome dans le repo | Diagnostic | Correction |
|---|---|---|
| Pas de streaming (response complete puis affichage) | Latence percue x3-5 | `streamText()` + SSE |
| System prompt inline dans le code TS | Non-iterable sans deploy | Externaliser dans `/prompts/` |
| `any` sur les reponses LLM | Pas de validation, hallucinations silencieuses | Zod schema + `generateObject()` |
| > 20 outils dans un seul agent | Precision selection chute | Deferred tools ou split agents |
| Pas de tracing/observability | Impossible de diagnostiquer en prod | Langfuse ou Helicone |
| `fetch()` direct vers LLM provider | Pas de retry, pas de fallback | Vercel AI SDK ou LiteLLM |
| Vector store sans reranking | Recall faible sur queries ambigues | Ajouter Cohere/Jina reranker |
| Pas de rate limiting sur API chat | DDoS et cout explosif | Middleware rate limiter |
| Imports `langchain` monolithiques | Bundles 10x trop gros | Imports specifiques ou Mastra |
| Pas de tests sur les outils | Tool bugs = agent broken | Tests unitaires sur chaque tool |
| ChromaDB en prod multi-user | Write-lock contention | Migrer vers Qdrant/pgvector |
| Pas de prompt caching | Cout x10 sur system prompts | Activer cache provider |

## Diagnostic optimisation (flux)

### Si latence p95 > 3s
1. Streaming actif ? → sinon, `streamText()` + SSE
2. Model routing en place ? → Haiku/Nano pour classify, Sonnet/4.1 pour generate
3. Edge deploy ? → Cloudflare Workers <10ms cold start
4. Outils paralleles ? → `parallel_tool_calls` actif
5. Framework overhead ? → raw SDK si LangChain.js ajoute > 50ms

### Si cout/conversation > $0.02
1. Prompt caching actif ? → system prompt + tools statiques → cache hit
2. Batch API applicable ? → traitement asynchrone = -50%
3. Model tiering ? → Flash-Lite $0.10/MTok pour volume
4. Historique tronque ? → summarize les vieux messages, garder les N derniers
5. Outils deferred ? → `defer_loading` si > 10 outils

### Si qualite reponse < 80% satisfaction
1. System prompt specifique ? → role/regles/exemples/escalade
2. RAG en place ? → retrieval avant generation
3. Reranking ? → +15-25% precision post-retrieval
4. Structured output ? → Zod force des reponses coherentes
5. Evaluation metriques ? → RAGAS faithfulness >= 0.9

## Gotchas TypeScript IA

- `@xenova/transformers` renomme en `@huggingface/transformers` — les deux existent sur NPM
- Vercel AI SDK RSC en pause — utiliser `useChat()` SSE
- LangChain.js verbose et "Python-ported" — preferer Vercel AI SDK ou Mastra pour du TS idiomatique
- `strict: true` (OpenAI) incompatible avec parallel tool calls
- Node.js natif n'a pas de `fetch` sur anciennes versions — utiliser Node 18+ ou Bun

## Liens

- [[stack-python-ia]] — Equivalent Python
- [[index-architectures]] — Decision pattern + framework chatbot
- [[rag-embeddings]] — Concepts embeddings (language-agnostic)
- [[rag-chunking]] — Strategies chunking
- [[rag-vector-databases]] — Comparatif vector stores
- [[agents-frameworks]] — Comparatif frameworks agents
