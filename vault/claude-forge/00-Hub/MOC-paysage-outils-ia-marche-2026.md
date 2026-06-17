---
titre: "MOC — Paysage des outils IA du marché (entreprise) 2026"
resume: "Cartographie navigable des outils IA réellement utilisés en entreprise (juin 2026), en 5 catégories : voix, briques produit, productivité interne, infra/LLMOps, plateformes générales. Angle build-vs-buy + adoption. Pour équiper l'équipe OU proposer l'IA aux clients (Loji)."
aliases:
  - "paysage outils IA 2026"
  - "cartographie outils IA marché"
  - "outils IA entreprise"
  - "build vs buy IA"
  - "outils IA utilisés marché"
  - "MOC outils IA"
domaine: ia
type: index
derniere-maj: 2026-06-17
auteur: claude
tags:
  - "#type/index"
  - "#domaine/ia"
---

# Paysage des outils IA du marché — 5 catégories

> [!info] Cadrage
> Outils IA réellement adoptés en entreprise (juin 2026), pour deux finalités : **équiper ses équipes** (usage interne) OU **proposer l'IA à ses clients** (produit SaaS, ex. Loji). Angle de décision = **build-vs-buy** (acheter vs coder) + **adoption marché**. Pricing/valorisations volatils → marqués vérifié-source-primaire vs rapporté dans les notes détaillées. Recherche : fan-out de 5 agents (site officiel + GitHub + adoption).

## Principe transversal (consensus marché 2026)

**Buy/intégrer gagne quasi partout** : ces outils sont des commodités, pas le différenciateur. Le **moat reste les données métier + les evals propriétaires** (cf [[economie-agentique-pricing-2026]] : 76% des solutions IA entreprise achetées en 2025, Menlo). Le « build » n'est justifié que sur : briques où le self-host bat l'API au volume/souveraineté (STT, embeddings, RAG), apps spécifiques, et orgs à forte compétence infra.

---

## 🎙️ 1. Voix — TTS / STT / agents vocaux
→ **Note dédiée : [[outils-voix-ia-build-vs-buy]]**

Le build-vs-buy se tranche **par brique** : TTS = **buy** (ElevenLabs/Cartesia/Google ; OSS Chatterbox MIT) · STT = **build viable** (Whisper OSS = même modèle que l'API ; sinon Gladia FR) · agents vocaux = **buy pour POC** (Retell/Vapi), **build à l'échelle** (LiveKit/Pipecat OSS). ⚠️ PlayHT mort, XTTS/Coqui piège de licence, EU AI Act 2 août 2026.

## 🧩 2. Briques produit à intégrer
→ **Note dédiée : [[briques-produit-ia-build-vs-buy]]**

OCR (**Mistral OCR 3** FR / Docling OSS) · embeddings (**Voyage-4** / Qwen3 OSS, cf [[rag-embeddings]]) · reranking (**zerank-2** / BGE, cf [[rag-reranking]]) · modération (**OpenAI Moderation gratuit** + **Llama Prompt Guard 2**) · RAG-aaS (**Ragie** free→$100/mo) · extraction structurée (**BAML**). Buy quasi partout ; self-host FR possible sur toute la pile.

## 🔧 3. Productivité interne / agents

| Sous-catégorie | Leaders & verdict |
|---|---|
| **Automatisation no-code** | **n8n** (OSS self-host, *le* candidat BUILD pour process internes + agents) · Zapier/Make (buy, par tâche) · Gumloop (AI-native) |
| **Réunions / notes** | **Granola** (momentum 2026, bot-free, Mac only) · Fathom (meilleur gratuit) · Fireflies (sales/CRM) |
| **Knowledge interne** | **Glean** (leader premium sales-led ~$50+/user) · **Dust** (29€, transparent) · Onyx (OSS self-host, cf [[onyx-enterprise-search]]) |
| **Agents métier no-code** | Lindy/Relay (back-office) · **Sierra** (agents client, valo $15,8 Md) · Decagon |
| **Assistants généraux** | M365 Copilot ($18/u) · Gemini Workspace · **Claude Team** ($20/seat) · ChatGPT Enterprise (sur devis) — suivre l'écosystème en place |

Détail automatisation/workflows → [[agents-automation]]. Build réel = **n8n** (OSS) ; le reste = buy selon écosystème.

## ⚙️ 4. Infra / LLMOps (faire tourner l'IA en prod)

| Couche | OSS gratuit | SaaS payant |
|---|---|---|
| **Observabilité** | **Langfuse** (MIT, leader self-host) | LangSmith, Braintrust, Helicone |
| **Gateway multi-LLM** | **LiteLLM** (MIT) | OpenRouter, Portkey, Cloudflare AI Gateway |
| **Éval** | DeepEval, Ragas, Promptfoo | Braintrust, LangSmith |
| **Serving** | **vLLM**, SGLang, Ollama | Together, Fireworks, Groq, Baseten |
| **Sécu/PII (RGPD)** | **Presidio**, Llama Guard | Private AI, Lakera, Prisma AIRS |

**Pile OSS souveraine gratuite** : Langfuse + LiteLLM + DeepEval/Ragas + vLLM + Presidio. Détail implémentation → [[reference-technique-stack-ia]], [[agents-evaluation]], [[stack-python-ia]].

> [!warning] Consolidation M&A 2026 (vérifié source primaire) — le gateway devient le « control plane » sécu
> **Humanloop MORT** (racheté Anthropic, shutdown 8 sept. 2025 — ne plus recommander) · **Langfuse → ClickHouse** (16 janv. 2026, reste MIT/self-host) · **Promptfoo → OpenAI** (9 mars 2026, reste OSS) · **Portkey → Palo Alto** (clos 29 mai 2026, dans Prisma AIRS) · **Predibase → Rubrik** (rapporté). ⚠️ OpenAI : plateforme fine-tuning par token en cours d'arrêt (seul `o4-mini` reste FT-able).

## 🧠 6. Intelligence de code (faire coder MIEUX les agents)
→ **Note dédiée : [[intelligence-de-code-build-vs-buy]]**

Deux familles : (A) **context engines** qui indexent le repo pour l'agent — **CodeGraph** (50k★ MIT) et **Serena** (25k★ LSP) sont les leaders OSS locaux, **SocratiCode** (MCP, AGPL-3.0) et Augment (managé 100$/mo) suivent. Builder l'indexation soi-même = non-sens. (B) **revue de code IA + gates** : CodeRabbit/Copilot review (buy) + SonarQube/Semgrep (gate déterministe OSS). Doctrine : règle prose = advisory, CI gate = non négociable.

## 🏢 5. Plateformes générales / gros sujets entreprise

| Sous-catégorie | Leaders & verdict |
|---|---|
| **Build d'apps IA (low-code)** | v0, Lovable, Bolt, Replit (vibe-coding) · Copilot Studio / Vertex Agent Builder / Bedrock (agents hyperscaler gouvernés, suivre où vivent les données) |
| **Support client IA** | **Intercom Fin** (0,99$/résolution, vérifié) · Sierra · Decagon · Ada — pricing à l'outcome (cf [[economie-agentique-pricing-2026]]) |
| **Créatif (marketing)** | Midjourney/Ideogram (image) · Runway/Pika (vidéo) · **HeyGen/Synthesia** (avatars/formation) — buy systématique |
| **Analytics IA** | Julius, ThoughtSpot (text-to-SQL plafonne ~50% → le vrai travail = semantic layer) |
| **Gouvernance à l'échelle** (sujet « éviter le chaos des MAJ ») | **PromptLayer** + **LaunchDarkly AI Configs** (= feature flags pour l'IA : changer prompt/modèle en prod sans redéployer, audit, par-équipe) · Langfuse prompt mgmt · Packmind (standards de code, cf [[packmind-context-governance]]) |

---

## Notes détaillées reliées

- [[outils-voix-ia-build-vs-buy]] — TTS / STT / agents vocaux
- [[briques-produit-ia-build-vs-buy]] — OCR, embeddings, reranking, modération, RAG-aaS, extraction
- [[outils-memoire-rag-gouvernance-juin-2026]] — mem0, LangMem, Pinecone, Onyx, Packmind (batch précédent)
- [[economie-agentique-pricing-2026]] — économie build-vs-buy, pricing à l'outcome, moat data
- [[reference-technique-stack-ia]] · [[stack-python-ia]] · [[stack-typescript-ia]] — implémentation
- [[agents-automation]] · [[agents-evaluation]] · [[agents-frameworks]] — agents & LLMOps
- [[MOC-Techniques]]
