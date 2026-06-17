---
titre: "Briques produit IA à intégrer (OCR, embeddings, reranking, modération, RAG-aaS) — build-vs-buy juin 2026"
resume: "Paysage des briques produit qu'une entreprise INTÈGRE plutôt que coder : OCR/doc-parsing, embeddings, reranking, modération/sécurité, RAG-as-a-service, extraction structurée. Verdict transversal : buy/intégrer gagne quasi partout (commodités), le moat reste data métier + evals."
aliases:
  - "briques produit IA"
  - "build vs buy briques IA"
  - "OCR doc parsing modération RAG-aaS"
  - "briques à intégrer Loji"
  - "Mistral OCR Ragie BAML"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://mistral.ai/news/mistral-ocr-3/"
  - "https://github.com/DS4SD/docling"
  - "https://docs.voyageai.com/docs/pricing"
  - "https://ragie.ai/pricing"
  - "https://github.com/567-labs/instructor"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

Briques produit IA qu'une entreprise (Neoteem/Loji) **intègre dans son produit SaaS** plutôt que de coder à la main. Légende : `[v]` = page officielle/GitHub vérifié juin 2026 · `[r]` = source secondaire ou page gated.

> [!tip] Verdict transversal : buy/intégrer gagne quasi partout
> Ces briques sont des **commodités à coût marginal faible, pas des différenciateurs** pour une proptech. Le moat Neoteem reste les **données métier** (baux, scoring, diagnostics) + les **evals propriétaires** (cohérent [[economie-agentique-pricing-2026]]), jamais le wrapper de modèle. Les deux seuls « build » légitimes : (1) **fine-tuning léger** d'un OSS sur le vocabulaire immobilier *après* mesure de sous-performance ; (2) **assemblage de briques RAG maison** quand le RAG-aaS devient plus cher que l'infra au scale.

## 1. OCR / Document parsing

Brique la plus critique pour NeoDocs (qualité tableaux + français). **BUY (API)** pour démarrer ; **SELF-HOST OSS** dès que souveraineté FR ou volume le justifient.

| Outil | Build-vs-buy | OSS ? | Pricing | Fiab. |
|---|---|---|---|---|
| **Mistral OCR 3** | **BUY** — meilleur prix/qualité, **provider FR + self-hostable** = idéal souveraineté | Non (self-host dispo) | **$2/1000 p**, batch $1 | `[v]` |
| **Docling** (IBM) | **SELF-HOST** — défaut OSS souveraineté FR | Oui (Apache 2.0, 61.7k★) | gratuit | `[v]` |
| **Marker** / **Surya** (Datalab) | SELF-HOST rapide / multilingue (90+ langues FR) | Oui | gratuit | `[v]` |
| **LlamaParse** | BUY si pipeline LlamaIndex (cher en mode agent) | Non | ~$1.25/1000 cr, free 10k cr/mois | `[v]` |
| **Unstructured.io** | BUY ingestion hétérogène ; OSS si MLOps | Oui (lib) | $0.03/page, 15k gratuites | `[v]` |
| **Reducto** | BUY si précision max + budget | Non | ~$1/1000 cr | `[v]` |
| **AWS Textract / Google Document AI / Azure DI** | BUY si déjà dans ce cloud | Non | OCR $1.50/1000p (+ tables/forms chers) | `[v]`/`[r]` |

**FR/souveraineté** : Mistral OCR self-hosted ou Docling.

## 2. Embeddings

**BUY (API)** par défaut — coût dérisoire (≤ $0.18/M, souvent < $20/mois à l'échelle PME). **SELF-HOST OSS** si > ~10M embeddings/mois, souveraineté, ou expertise GPU. Détail technique + comparatif → [[rag-embeddings]].

- API : **Voyage-4** ($0.06/M), Voyage-4-large ($0.12), OpenAI text-embedding-3-large ($0.13), Cohere Embed v4 ($0.12 multimodal), Gemini embedding-001 ($0.15).
- OSS souverain : **Qwen3-Embedding-8B** (#1 MTEB multilingue ~70.58, self-host, Apache 2.0) = le plus défendable techniquement ; BGE-M3 (hybride dense/sparse/multi-vector).

## 3. Reranking

**BUY (API)** — gros gain de pertinence pour quelques $/M et < 100ms. **Vaut le coût** quand le 1er étage ramène trop de candidats bruités (top-50/100 → top-5/10) = quasi tout RAG sérieux sur corpus hétérogène (baux/diagnostics). Détail → [[rag-reranking]].

- **zerank-2** (ZeroEntropy, 100+ langues, le moins cher $0.025/M), Cohere Rerank ($2/1000 searches), Voyage rerank-2.5 ($0.05/M), Jina reranker v3.
- OSS souverain : **BGE-reranker-v2** ou zerank-1-small (Apache 2.0) ; **FlashRank** (ultra-léger CPU, sans GPU).

## 4. Modération / sécurité contenu

Deux problèmes DISTINCTS : (a) modération contenu (toxique/haine/violence) et (b) détection d'attaques (prompt injection/jailbreak). Il en faut souvent **deux**.

| Outil | Rôle | Build-vs-buy | OSS ? | Pricing | Fiab. |
|---|---|---|---|---|---|
| **OpenAI Moderation** (`omni-moderation-latest`) | Modération contenu texte+image (13 catégories). PAS d'injection | **BUY systématique — gratuit** | Non | **Gratuit** | `[v]` |
| **Llama Prompt Guard 2** (86M/22M) | **Détecte prompt injection + jailbreak**, 8 langues dont FR | **BUY self-host** — meilleur gratuit/perf | Oui (DeBERTa MIT) | gratuit · latence 19-92ms | `[v]` |
| **Llama Guard 4** (12B) | Modération contenu texte+image multilingue | BUY self-host si souveraineté FR | Oui (Llama 4 License) | gratuit en poids | `[r]` |
| **Lakera Guard** | Injection directe ET indirecte (PDF/HTML/tool), PII, managé | BUY si clé-en-main | Non | non public (racheté **Cisco** 2025) | `[r]` |
| **NeMo Guardrails** (NVIDIA) | Rails programmables (input/dialog/retrieval/output) | BUILD-assist si rails métier complexes | Oui (Apache 2.0) | gratuit | `[v]` |

**Ne JAMAIS coder un classifieur de modération maison** : sujet résolu, OpenAI Moderation est gratuit. Reco Neoteem : **OpenAI Moderation (contenu) + Llama Prompt Guard 2 (injection)** en pipeline.

## 5. RAG-as-a-Service

Pipeline RAG clé-en-main (ingestion + chunking + embed + retrieval + rerank + génération managés). Le « buy » du RAG : tu uploades les docs, le service gère les 6 étapes. (Concept détaillé : le RAG fait main = 6 briques à coder/maintenir vs RAG-aaS = juste uploader + interroger.)

| Outil | Build-vs-buy | OSS ? | Pricing | Fiab. |
|---|---|---|---|---|
| **Ragie** | **BUY pour démarrer vite** — pricing lisible, idéal PME/proptech | Non | Free (1k pages) · Starter **$100/mo** · Pro $500/mo | `[v]` |
| **Vectara** | BUY si **anti-hallucination certifiée** = argument contractuel | Non (HHEM OSS séparé) | **PAS de free tier : dès ~100k$/an** | `[v]` |
| **Pinecone Assistant** | BUY si déjà Pinecone | Non | Starter gratuit · Enterprise min $500/mo | `[r]` |
| **Azure AI Search** | BUY si Azure (retriever, génération à assembler) | Non | Basic $75/mo · S1 $250/mo | `[r]` |

**Reco Loji** : **Ragie** (free → $100/mo) pour **valider NeoDocs** vite, ré-internaliser (briques maison) au scale ou pour la souveraineté. Détail Pinecone → [[pinecone-vector-database]] ; Onyx (RAG entreprise OSS) → [[onyx-enterprise-search]].

## 6. Extraction structurée / function calling fiable

**Point clé 2026** : les Structured Outputs natifs (OpenAI `strict:true`, Anthropic tool use) couvrent le cas simple. Ces libs valent pour le multi-provider, la validation+retry, ou le constrained decoding local.

| Outil | Build-vs-buy | OSS ? | Adoption | Fiab. |
|---|---|---|---|---|
| **Structured Outputs natifs** (OpenAI/Anthropic) | **Défaut — commencer ici, gratuit** | n/a | inclus | `[v]` |
| **Instructor** (Python) | **BUY (adopter)** — standard de fait Python, multi-provider + retry + Pydantic | Oui (MIT, 13.2k★) | — | `[v]` |
| **Outlines** (dottxt) | adopter si modèles locaux, sortie invalide impossible (constrained decoding) | Oui (14k★) | — | `[v]` |
| **BAML** (BoundaryML) | **adopter** pour équipe cross-langage : un schéma `.baml` → clients Python/TS/Ruby/Go | Oui (8.4k★) | — | `[v]` |

**Ne jamais coder un parser JSON-repair maison.** Pour Loji : **BAML** = le levier réel (un schéma `.baml` → clients NeoChat TS *et* back Python).

## Deux piles recommandées Neoteem/Loji

- **⚡ Buy rapide (time-to-market)** : Mistral OCR 3 → Voyage-4/Gemini → Voyage rerank-2.5/zerank-2 → Ragie → OpenAI Moderation + Prompt Guard 2 → BAML.
- **🇫🇷 Souveraineté FR self-host** : Docling/Mistral OCR self-hosted → Qwen3-Embedding-8B → BGE-reranker-v2 → briques RAG maison → Llama Guard 4 + Prompt Guard 2 → BAML. Tout OSS, hébergeable en France.

## Liens

- [[rag-embeddings]] · [[rag-reranking]] · [[rag-vector-databases]] — profondeur technique des briques
- [[pinecone-vector-database]] · [[onyx-enterprise-search]] — vector DB / RAG entreprise
- [[outils-voix-ia-build-vs-buy]] — briques voix (TTS/STT/agents)
- [[outils-memoire-rag-gouvernance-juin-2026]] — hub mémoire/RAG/gouvernance
- [[economie-agentique-pricing-2026]] — économie build-vs-buy, moat data métier
- [[MOC-Techniques]]
