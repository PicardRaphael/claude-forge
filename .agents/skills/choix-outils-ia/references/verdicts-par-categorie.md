# Verdicts build-vs-buy par catégorie — orientation rapide

Tables condensées pour orienter le dialogue. **Le pricing exact + les licences + les morts du marché vivent dans les notes vault** (lire via `mcp__forge-brain__read_note`, marqué vérifié-source vs rapporté). Les chiffres ci-dessous datent de juin 2026 — re-vérifier à la source avant d'engager un client (cf skill `veille-outils-ia`).

## 🎙️ Voix — tranché PAR brique (`outils-voix-ia-build-vs-buy`)

| Brique | Verdict | Reco principale | OSS souverain |
|---|---|---|---|
| **TTS** (synthèse) | ✅ BUY | ElevenLabs (FR premium, 99$/mo) · Google Cloud (moins cher) · Cartesia (temps réel) | Chatterbox (MIT, meilleur fit commercial) ⚠️ éviter XTTS/Coqui (CPML non-commercial) |
| **STT** (transcription) | ❌ BUILD viable | Gladia (#1 FR, RGPD, diarisation) · Deepgram (streaming) | Whisper/faster-whisper (Apache/MIT) au volume |
| **Agents vocaux** (robot tél.) | 🔶 BUY POC, BUILD échelle | Retell (transparent) · Vapi (orchestration) | LiveKit Agents (Apache-2.0) · Pipecat (BSD-2) |

Architecture : cascade STT→LLM→TTS (~1,4s, ~5× moins cher) vs speech-to-speech natif OpenAI Realtime (320-800ms). Morts : **PlayHT**. EU AI Act 2 août 2026 : disclosure IA en début d'appel.

## 🧩 Briques produit (`briques-produit-ia-build-vs-buy`)

| Brique | Verdict | Buy rapide | OSS souverain FR |
|---|---|---|---|
| **OCR / doc parsing** | BUY puis self-host | Mistral OCR 3 (2$/1000p, FR + self-hostable) | Docling (Apache, 61k★) · Marker/Surya |
| **Embeddings** | BUY (coût dérisoire) | Voyage-4 (0,06$/M) · Gemini · OpenAI 3-large | Qwen3-Embedding-8B (#1 MTEB, Apache) · BGE-M3 |
| **Reranking** | BUY (gain pertinence) | zerank-2 (0,025$/M) · Cohere · Voyage rerank-2.5 | BGE-reranker-v2 · FlashRank (CPU) |
| **Modération** | BUY gratuit | OpenAI Moderation (gratuit, contenu) **+** Llama Prompt Guard 2 (injection) | Llama Guard 4 · NeMo Guardrails |
| **RAG-as-a-Service** | BUY pour valider | Ragie (free→100$/mo, idéal PME) | (briques maison au scale) ⚠️ Vectara pas de free tier |
| **Extraction structurée** | adopter | Structured Outputs natifs (gratuit) puis Instructor (Python) | BAML (cross-langage TS+Python) · Outlines (local) |

Ne JAMAIS coder : classifieur de modération maison, parser JSON-repair maison.

## ⚙️ Infra / LLMOps (`MOC-paysage-outils-ia-marche-2026`)

| Couche | OSS gratuit | SaaS payant |
|---|---|---|
| Observabilité | **Langfuse** (MIT, leader) | LangSmith, Braintrust, Helicone |
| Gateway multi-LLM | **LiteLLM** (MIT) | OpenRouter, Portkey (→Palo Alto), Cloudflare AI Gateway |
| Éval | DeepEval, Ragas, Promptfoo (→OpenAI) | Braintrust, LangSmith |
| Serving | **vLLM**, SGLang, Ollama | Together, Fireworks, Groq, Baseten |
| Sécu/PII RGPD | **Presidio**, Llama Guard | Private AI, Lakera (→Cisco), Prisma AIRS |

Pile OSS souveraine gratuite : Langfuse + LiteLLM + DeepEval/Ragas + vLLM + Presidio. Morts : **Humanloop** (Anthropic, shutdown sept 2025), **Predibase** (→Rubrik). OpenAI fine-tuning par token en arrêt (seul o4-mini reste FT-able).

## 🧠 Intelligence de code (`intelligence-de-code-build-vs-buy`)

| Besoin | Reco |
|---|---|
| Context engine local gratuit souverain | **CodeGraph** (MIT, 50k★, MCP natif) · **Serena** (LSP, MIT) — zéro egress |
| + artefacts DB/API/infra + air-gap | SocratiCode (OSS) ⚠️ **AGPL-3.0** si distribué dans un produit |
| Context engine managé cross-repo | Augment (100$/mo, egress) · Tabnine ECE (air-gap) |
| Reviewer PR IA | BUY : Copilot review (si GitHub) ou CodeRabbit — ne pas builder |
| Gate déterministe qualité+sécu | OSS-first : SonarQube Community + Semgrep |
| Supply-chain / secrets | BUY (impossible maison) : Socket + GitGuardian |

Doctrine : règle prose = advisory ; CI gate déterministe = non négociable. Morts/pièges : Bloop (archivé), **GitNexus** (non-commercial), **SocratiCode** (AGPL-3.0). Builder l'indexation soi-même = non-sens (commodité).

## 🧠 Mémoire / vector DB / RAG entreprise (`outils-memoire-rag-gouvernance-juin-2026`)

| Catégorie | Outil | Choisir si… |
|---|---|---|
| Mémoire agent universelle | mem0 | stack agnostique, multi-tenant (⚠️ v3 OSS sans graphe) |
| Mémoire LangChain-native | LangMem | déjà LangGraph (lock-in fort, SDK figé) |
| Vector DB managée | Pinecone | prod scalable sans ops (pas si volume faible → pgvector/Qdrant) |
| RAG entreprise OSS | Onyx | recherche knowledge interne + souveraineté (stack lourde) |
| Gouvernance contexte agents code | Packmind | multi-équipes/repos ≥2 agents + audit |

## 🏢 Plateformes / pricing (`MOC-paysage` + `economie-agentique-pricing-2026`)

Build d'apps low-code : v0/Lovable/Bolt/Replit. Support client IA : Intercom Fin (0,99$/résolution). Avatars : HeyGen/Synthesia (buy). Analytics : Julius/ThoughtSpot (text-to-SQL plafonne ~50% → semantic layer). Gouvernance MAJ à l'échelle : PromptLayer + LaunchDarkly AI Configs (feature flags pour l'IA).

Pricing : siège mort, place à l'outcome (Fin 0,99$/résolution) / metering / model routing / inférence maison. Kill switches + spend ceilings obligatoires dès le départ.
