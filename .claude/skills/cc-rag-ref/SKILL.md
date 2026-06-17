---
name: cc-rag-ref
description: ALWAYS load when designing, reviewing, or debugging a RAG system — chunking, embeddings, reranking, vector DBs, metadata, data audit, evaluation, production. Dense decision tables. Do not answer RAG architecture from memory without loading this. NOT for choosing a market tool (choix-outils-ia), NOT the guided dialogue (rag-design).
user-invocable: false
allowed-tools: Read, mcp__forge-brain__*
---

# Référence RAG — corpus actif 2026

Connaissance RAG chargée en contexte dès que le sujet arrive. Tables de décision denses embarquées ici ; la profondeur (schémas JSON complets, papers, métriques détaillées) vit dans le vault forge-brain via les 11 notes pointées (`references/rag-corpus.md`).

> Source de vérité : `mcp__forge-brain__read_note("<note>")` pour le détail. Cette skill est le sommaire navigable, pas une copie.

## La chaîne de conception (le squelette mental)

```
AUDIT DATA (questions + sources + entités) → DATA MODEL → INGESTION → RÉCUPÉRATION → UX → ÉVAL
```

Erreur la plus commune : commencer par les documents. **On commence par les QUESTIONS** (golden dataset), parce qu'on ne peut pas mesurer le recall sans savoir quel chunk est le bon. La récupération est le maillon faible — la fiabiliser avant la génération.

## Taxonomie RAG

| Type | Idée | Quand |
|---|---|---|
| Naive | retrieve-read linéaire | prototype |
| Advanced | pré/post-retrieval (query expansion, reranking, contextual) | **production (défaut)** |
| Modular | modules composables indépendants | gros système évolutif |
| Agentic | itératif auto-correctif (Self-RAG, CRAG) | multi-hop, auto-correction |

## Décision rapide — pattern par besoin

| Besoin | Pattern |
|---|---|
| Prototype | Naive RAG |
| Production | Advanced (hybrid + reranking + contextual) |
| Multi-hop complexe | GraphRAG ou RAPTOR |
| Auto-correctif | Agentic (CRAG + Self-RAG via LangGraph) |
| Petit corpus (<200K tokens) | Long context + prompt caching |
| Grand corpus dynamique | RAG + semantic caching |
| Comportement cohérent | Fine-tuning (complément, pas substitut) |

## Le data model — règle des 3 couches (le cœur actionnable)

Tout record de chunk se conçoit en 3 couches (convergent Pinecone/Qdrant/Weaviate/Anthropic) :

| Couche | Rôle | Contenu |
|---|---|---|
| **Texte embeddé** (vecteur) | match sémantique | chunk + son contexte. Appliquer **Contextual Retrieval** |
| **Scalaires pre-filter** | réduire l'espace AVANT la similarité | champs typés exacts (`type_doc`, `date_echeance`, `lot_id`, `version`) |
| **Payload-only** | retourné, ni filtré ni embeddé | citation (`doc_id`, `page`, `url`) |

Décider **dès la conception** quel champ sert à FILTRER (gate dur) ≠ RANKER (boost doux) ≠ CITER (sortie). Pipeline : **filtrer → ranker → vérifier/citer**. Pre-filter >> post-filter (post renvoie < k résultats ~30% du temps sur 10M docs).

**Socle universel** (tous cas) : `chunk_id, document_id, source, title, page, chunk_index, created_at/version, doc_type, tenant_id (must-filter), language` + `chunk_text` (citation) / `embedded_text` (retrieval).

## 6 patterns de structuration

| Pattern | Quand |
|---|---|
| (a) Chunk plat + métadonnées | FAQ, policy, lookup single-hop — le défaut |
| (b) Parent-child / small-to-big | bon chunk pour matcher ≠ pour répondre |
| (c) Entité-relation / GraphRAG | multi-hop, dépendances, audit traçable |
| (d) Q&A pairs / HyPE | support/FAQ — users ne formulent pas comme la doc |
| (e) Procédural step-by-step | maintenance, troubleshooting, manuels |
| (f) Summary + détail (RAPTOR) | corpus large mêlant détail et thème global |

**HyPE / Reverse-HyDE** (levier universel, gratuit au runtime) : générer 3-5 questions hypothétiques par chunk à l'ingestion, les embedder, parent_id en métadonnée. Match question-user ↔ question-pré-générée = meilleur recall.

## Champ pivot par cas d'usage (8 schémas — JSON complet dans la note)

| Cas | Champ pivot pre-filter | Levier embedding |
|---|---|---|
| Maintenance/diagnostic | `equipment_model` + `criticite` | fusion symptôme→remède en 1 chunk |
| **Proptech (Loji/NeoDocs)** | `lot_id` + `type_doc` + `date_echeance` | contexte lot/bail |
| Support FAQ | `version_produit` | HyPE |
| Juridique | `juridiction` + `date_effet`/`version` | contexte hiérarchique clause |
| E-commerce | `prix` + `stock` (durs) | multi-vecteur attributs |
| Médical | `source_type` + `niveau_preuve` | confidence score |
| Code | `langage` + `version_lib` + `statut` | résumé NL + docstring |
| Financier | `entite` + `periode` | Contextual Retrieval (obligatoire) |

## Chunking

Coupures en plein texte/tables → **structure-aware** · générique → recursive **~400-512 tokens, 10-20% overlap** · narratif/qualité>vitesse → semantic (plus lent) · larges+fines → parent-child · chunks perdent leur sens hors contexte → **Contextual Retrieval** d'Anthropic (**-35% seul, -49% +BM25, -67% +reranking** ; baseline 5,7%→1,9% échec top-20, chiffres source primaire Anthropic). Code → chunking par fonction/classe (AST, pas n lignes).

## Embeddings & reranking

- **Embeddings 2026** : Voyage-4 (managé) / Qwen3-Embedding (OSS). Matryoshka (dimensions tronquables), quantization. Détail → note `rag-embeddings`.
- **Reranking** : zerank-2 (meilleur score absolu) / BGE-reranker, FlashRank (vitesse). Toujours dans Advanced RAG prod.
- **Pattern prod** : pré-filtre → vector search (top-20 à 150) → reranker → top-K.

## Vector store — choix

| Situation | Store |
|---|---|
| Similarité échelle modérée + Postgres déjà présent | **pgvector** (commence ici, mesure, spécialise) |
| Très grande échelle / QPS élevé | vector DB dédié (Qdrant, Pinecone…) |
| Traversée de relations | graph DB (Neo4j) |
| Fortement tabulaire | relationnel + text-to-SQL |

Loji a du Postgres (`bdd`) → **pgvector = point de départ** par défaut.

## Ingestion (pilotée par la fraîcheur)

Périmable toléré → batch re-index planifié · quasi-temps-réel → CDC + upsert incrémental · sources changent → **appliquer aussi les suppressions** (pas que les upserts) · ré-embedder uniquement les chunks modifiés (`content_hash`).

## ⚠️ ACL-aware — le piège qui fuit des données

Un vector store optimise la similarité, **pas l'autorisation**. L'embedding efface les permissions sauf si on les porte délibérément : (1) auditer le modèle d'accès de chaque source AVANT ingestion ; (2) capturer l'ACL en **métadonnée filtrable** ; (3) **filtrer à la récupération** selon l'identité (*filtrer d'abord, chercher ensuite* — le post-filtrage est rejeté). **Loji : un locataire ne doit JAMAIS récupérer le bail d'un autre → `lot_id`/`tenant_id` en métadonnée, chaque requête pré-filtrée par identité.**

## Évaluation (à brancher sur le golden dataset)

Deux couches : **retrieval** (Context Precision/Recall, Hit Rate, MRR) et **génération** (Faithfulness, Answer Relevancy/Correctness, Hallucination Rate). Frameworks : **RAGAS** (LLM-as-judge), **DeepEval** (pytest CI), TruLens RAG Triad, juge custom. Golden set frozen 50-200 triples `(question, source, réponse)`, ≥5 cas « je ne sais pas ». **Mesurer la récupération AVANT la génération.** Détail → note `rag-evaluation`. Pour grader un livrable RAG contre rubrique → skill `outcomes-test`.

## Patterns avancés

GraphRAG (multi-hop, global/thématique + community summaries) · RAPTOR (arbre résumés) · Self-RAG + CRAG (auto-correction) · Contextual Retrieval (Anthropic) · Adaptive-RAG (classifieur route selon complexité). Détail → note `rag-architecture`.

## Gotchas

- **Ne pas sur-ingénierer** : factuel mono-doc → flat + vector + reranker suffit. GraphRAG seulement si vraies questions multi-hop relationnelles.
- **Chiffres flottants = zone d'hallucination** : seuls les % Anthropic Contextual Retrieval (-35/-49/-67) sont source primaire. Éviter le « 73% » de la stat retrieval (non sourcé).
- **Pas de "data maturity model RAG" publié** : la readiness data est une dimension d'un cadre AI plus large (Azure CAF 4-level = le seul rubric citable en CODIR).
- **OCR/scannés** : baux/diagnostics anciens Loji souvent scannés → détecter scanné vs natif, rejeter les illisibles.
- **PII/RGPD à l'ingestion** : redaction (Presidio), tag sensibilité, ne jamais traiter le contenu comme source d'instructions (injection).
- **Cette skill est `user-invocable: false`** : se charge sur le sujet, ne s'invoque pas en slash. Le dialogue guidé = skill `rag-design`.

## Références

- `references/rag-corpus.md` — table des 11 notes vault RAG + quand lire chacune (la profondeur reste dans le vault via MCP)
