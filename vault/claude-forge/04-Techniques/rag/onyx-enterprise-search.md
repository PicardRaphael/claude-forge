---
titre: "Onyx (ex-Danswer) — Plateforme RAG/recherche entreprise open-source"
resume: "Onyx (onyx-dot-app/onyx, MIT) = assistant IA + enterprise search connecté à 50-60+ sources avec sync ACL ; v4.0 (mai 2026) a remplacé le moteur Vespa par OpenSearch. Self-host lourd (Postgres+OpenSearch+Redis+MinIO+Celery+model server)."
aliases:
  - "Onyx"
  - "Danswer"
  - "onyx.app"
  - "onyx-dot-app"
  - "enterprise search open-source"
  - "assistant IA entreprise Onyx"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://github.com/onyx-dot-app/onyx"
  - "https://docs.onyx.app/changelog"
  - "https://onyx.app/"
  - "https://onyx.app/pricing"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

**Onyx** (ex-**Danswer**, repo `onyx-dot-app/onyx`) = plateforme open-source de **« AI chat / enterprise search »** : un assistant IA connecté aux docs, apps et personnes de l'entreprise, interface chat unifiée par-dessus n'importe quel LLM. Slogan : *« the open-source AI chat connected to your docs, apps, and people »*.

- Fondée 2023 (Yuhong Sun, Chris Weaver), San Francisco, ~20 employés (rapporté).
- **Double modèle** : Community Edition **MIT** auto-hébergeable (couvre tout le cœur : Chat, RAG, Agents, Actions) + Cloud + Enterprise Edition (SSO OIDC/SAML, SCIM, RBAC, audit, **permission-sync**).

## Comment ça marche (technique)

**Stack** : backend **Python/FastAPI** (67 %), frontend **Next.js/TS** (27 %), workers **Celery**, **PostgreSQL** (comptes, ACL, métadonnées), **Redis** (cache + queues), **MinIO** (blob S3-compatible), **Model Server** dédié (embeddings, GPU recommandé en self-host).

> [!warning] Changement majeur — moteur d'index (vérifié changelog primaire)
> **v4.0.0 (26 mai 2026) : « Vespa is gone, OpenSearch is now the only document index. »** Toute doc/blog antérieure citant Vespa comme cœur est **périmée** (la quasi-totalité du contenu secondaire). **Migration d'index requise avant upgrade** (sinon perte des docs indexés).

**RAG** : Agentic RAG = hybrid index (vector + keyword BM25) + reranking optionnel + knowledge graph. Pipeline : connectors → fetch/parse/chunk → embeddings → index OpenSearch → query hybride → rerank → LLM.

**Embeddings** : défaut self-host historique `nomic-embed-text-v1` (MRL 64–768). Providers cloud : Cohere (embed-v4.0), OpenAI, Voyage, Gemini. Changer de modèle = **réindexation complète**.

**Connectors** : **50-60+** (Slack, Google Drive, Confluence, Jira, Notion, GitHub, SharePoint, Salesforce…) + connecteurs **MCP** et **federated** (recherche externe). Permissions : 3 modes par connecteur — Private / Public / **Auto Sync Permissions** (reconstruit l'ACL depuis la source ; **EE + Cloud uniquement**).

**LLM** : self-host (Ollama, vLLM, LiteLLM) ou propriétaires (Anthropic, OpenAI, Gemini).

## Déploiement

- **Docker Compose, Kubernetes, Helm/Terraform**. One-liner : `curl -fsSL https://onyx.app/install_onyx.sh | bash`.
- **Onyx Lite** (< 1 Go RAM, Chat + Agents) vs **Standard** (full stack).
- **API publique** `POST /api/search` (v4.0), **Scoped PAT** + OAuth MCP (v4.1.0, 11 juin 2026), Slack bot natif + Enterprise Grid, Coding Agent sandboxé (opt-in).

## Quand utiliser

| Idéal | Plutôt éviter |
|---|---|
| Recherche unifiée du knowledge interne, assistant connecté multi-sources avec **respect des ACL natives** | RAG mono-source sur-mesure (un simple vector store + pipeline maison suffit) |
| Besoin **self-host / data residency / souveraineté** (secteur sensible) | Équipe sans capacité à opérer la stack (lourde : Postgres + OpenSearch + Redis + MinIO + Celery + model server) |
| Éviter le cycle de vente enterprise long (alternative open à **Glean**) | Besoin d'un SaaS clé-en-main sans ops → Cloud Onyx ou Glean |

## Optimisation

- Embeddings : GPU sur le model server en self-host, sinon provider cloud (qualité+latence). Reranking = +pertinence vs léger surcoût latence.
- Connectors : régler la fréquence de sync selon volatilité ; **activer Auto Sync Permissions dès qu'une source a des ACL** (sinon fuite de données entre users) — mais EE/Cloud.
- Index gourmand : dimensionner mémoire/disque. Re-embedding = réindexation totale → choisir le modèle dès le départ.
- **Pièges** : ne pas upgrader vers v4.0 sans migration d'index (perte de données).

## Maturité (source primaire GitHub, juin 2026)

- **⭐ 30.4k**, 4.2k forks, 214 releases, dernière **v4.1.1 (12 juin 2026)**. Releases ~hebdo.
- **Financement** (rapporté) : YC 2024 puis **seed 10 M$ (mars 2025)**, Khosla Ventures + First Round.
- **Adoption** (marketing, non indépendant) : Netflix, Ramp, Thales ; benchmarks maison win-rate 64–76 % vs ChatGPT/Claude/Notion AI — auto-déclarés, prudence.
- **Pricing Cloud** : Business 20 $/user/mois, Enterprise sur devis.

## Liens

- [[rag-vector-databases]] — Onyx utilise désormais OpenSearch comme index hybride
- [[rag-production]] — patterns RAG en production
- [[rag-reranking]] — reranking post-retrieval (Cohere)
- [[RAG]] — index principal
- [[MOC-Techniques]]
