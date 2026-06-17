---
titre: "Pinecone — Vector database managée serverless"
resume: "Pinecone (SaaS propriétaire, pas de self-host) = vector DB zero-ops leader historique. Archi serverless (storage/compute découplés), pricing RU/WU qui scale avec la taille du namespace, Inference (embeddings+rerank hébergés) et Assistant (RAG clé en main) intégrés."
aliases:
  - "Pinecone"
  - "pinecone.io"
  - "Pinecone serverless"
  - "vector database managée"
  - "Pinecone Inference"
  - "Pinecone Assistant"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://www.pinecone.io/pricing/"
  - "https://docs.pinecone.io/guides/index-data/indexing-overview"
  - "https://docs.pinecone.io/guides/manage-cost/understanding-cost"
  - "https://www.pinecone.io/blog/integrated-inference/"
  - "https://techcrunch.com/2023/04/27/pinecone-drops-100m-investment-on-750m-valuation-as-vector-database-demand-grows/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Description

**Pinecone** (pinecone.io) = **vector database managée, SaaS, propriétaire** (pas de self-host, pas open-source — c'est le différenciateur structurant vs toute la concurrence open-source). Pionnier de la catégorie (fondée 2019, Edo Liberty, ex-Amazon AI). Proposition de valeur centrale : **zéro-ops** — on crée un index, on choisit cloud + région, Pinecone provisionne / shard / réplique / scale sans changement de code ; on paie l'usage, jamais la gestion d'infra.

> Pour le **comparatif inter-vector-DB** (Pinecone vs Qdrant/Weaviate/Milvus/pgvector, tiers d'échelle), voir [[rag-vector-databases]]. Cette note = Pinecone **en profondeur**.

## Comment ça marche (technique)

**Architecture serverless** (défaut ; pods = legacy en 2026) : storage sur object storage, compute élastique, pas de provisioning de nodes/replicas, sharding et parallélisation automatiques, de milliers à milliards de vecteurs.

**Index & namespaces** : un index serverless peut **mixer `dense_vector` + `sparse_vector` + champs `string`** dans le même document. **Namespaces** = partition au sein d'un index ; toute opération cible **exactement un** namespace, créés auto à l'upsert. Usage canonique : **isolation multi-tenant** (1 namespace/client) + perf (la query ne scanne que le namespace ciblé).

**Métriques** : dense = `cosine` / `dotproduct` / `euclidean` ; sparse = `dotproduct` uniquement.

**Métadonnées** : paires clé-valeur **plates** (pas d'objets imbriqués), **limite 40 KB/record**. Opérateurs `$eq $ne $gt $gte $lt $lte $in $nin $exists $and $or`. (Le « metadata filtering limitée » des vieux comparatifs est largement périmé.)

**Recherche hybride sparse-dense** : combine dense + lexical (BM25/sparse) à la query, optionnellement avec reranking (`score_by` par query).

**Pinecone Inference** (GA) : embeddings + reranking **hébergés**, embed/rerank/query via une seule API (workload et facture restent dans Pinecone). Embeddings `llama-text-embed-v2` (1024 par défaut), `multilingual-e5-large`, `pinecone-sparse-english-v0`. Reranking `pinecone-rerank-v0`, `bge-reranker-v2-m3`, `cohere-rerank-v3.5`.

**Pinecone Assistant** (RAG managé clé en main) : upload de docs, Assistant gère chunking + embedding + indexing + retrieval + query planning + reranking + génération LLM. Une seule API key. Node n8n officiel.

**API** : SDK Python & TS, `upsert` / `query` (par namespace), `fetch`, `list`. Intégrations LangChain (`PineconeVectorStore`) et LlamaIndex (namespaces natifs).

## Pricing (vérifié pinecone.io/pricing, juin 2026)

| Plan | Minimum mensuel |
|---|---|
| Starter | Gratuit |
| Builder | 20 $/mois flat (au-delà des quotas : usage **bloqué**, pas facturé) |
| Standard | 50 $/mois min |
| Enterprise | 500 $/mois min |

- **Pricing = 3 axes** : Read Units (RU), Write Units (WU), Storage. Pas de charge compute idle.
- Storage 0,33 $/GB/mois · WU 4–4,50 $/M (Standard) · RU 16–18 $/M (Standard).
- **Modèle RU clé** : une query consomme **1 RU par GB de namespace ciblé**, min **0,25 RU/query**. Le coût scale **linéairement avec la taille du namespace** → d'où l'importance du design des namespaces.
- Inference : embeddings 0,08–0,16 $/M tokens, reranking 2 $/1000 requêtes.
- ⚠️ **Piège récurrent** (rapporté) : factures 2,5–4× au-dessus du budget estimé quand le workload réel (agents, queries fréquentes sur gros namespaces) diverge du calculateur.

## Quand utiliser

| Idéal | Éviter / overkill |
|---|---|
| Production scalable sans gérer d'infra, time-to-market rapide | Volume faible (pgvector/Qdrant free suffit) |
| Équipe prête à payer le zéro-ops | Besoin de contrôle total / éviter le lock-in propriétaire |
| Pack intégré (DB + Inference + Assistant en une API) | Budget serré à grande échelle (factures imprévisibles) |
| | Vecteurs = 1 feature d'un stack Postgres existant → pgvector ([[rag-vector-databases]]) |

**Pinecone gagne sur la simplicité opérationnelle, PAS sur le benchmark brut** (Qdrant plus rapide/moins cher self-host).

## Optimisation

- **Design des namespaces = levier de coût n°1** : RU scale avec la taille du namespace ciblé → segmenter (tenant, catégorie) garde les queries petites et bon marché. Namespaces > index séparés pour le multi-tenant.
- **Batching upserts** : batches 64–100, parallèle. Le goulot est souvent l'embedding (modèle externe), pas Pinecone.
- **Filtrage métadonnées** : plat, types simples, < 40 KB/record.
- **Reranking two-stage** : récupérer large (dense) puis reranker → précision + réduction du contexte/coût LLM.
- **Dimension embeddings** : 1024 souvent ; 384/512 réduisent storage et RU au prix d'un peu de rappel.

## Maturité

- **Financement** (vérifié TechCrunch/Menlo) : Série B **100 M$ à 750 M$ de valo (avril 2023)**, a16z. Total ~138 M$. ⚠️ **Aucun tour public postérieur trouvé — la valo 750 M$ date de 2023, potentiellement obsolète.**
- Adoption : Shopify, Gong, Zapier (rapporté).

## Liens

- [[rag-vector-databases]] — comparatif inter-vector-DB (Pinecone vs Qdrant/Weaviate/Milvus/pgvector)
- [[memoire-agent-mem0]] — mem0 supporte Pinecone comme backend vector
- [[rag-reranking]] — Pinecone Inference héberge le reranking
- [[rag-embeddings]] — dense vs sparse
- [[RAG]] · [[MOC-Techniques]]
