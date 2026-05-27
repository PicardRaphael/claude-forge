# Domaine — RAG & Embeddings

Couvre : Retrieval-Augmented Generation, embeddings, rerankers, vector databases, techniques retrieval.
Nombre de queries : 11 (acceptable pour 1 agent, splitter si perte de focus)

## Sources directes

- `llamaindex.ai/blog`
- `pinecone.io/learn`
- `weaviate.io/blog`
- `jina.ai/news`
- `contextual.ai/blog`
- `sbert.net`

<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->

## Leaders canonisés (10) — vault 05-Leaders/rag/

| Personne | Rôle | Sources |
|----------|------|---------|
| **Douwe Kiela** | CEO & co-fondateur Contextual AI | contextual.ai, en.wikipedia.org |
| **Greg Kamradt** | Créateur indépendant | gregkamradt.com, github.com |
| **Han Xiao** | VP of AI, Elastic (fondateur Jina AI) | jina.ai, hanxiao.io |
| **Harrison Chase** (@hwchase17) | Co-fondateur & CEO LangChain | www.langchain.com, twitter.com |
| **James Briggs** | Fondateur Aurelio AI | www.youtube.com, www.pinecone.io |
| **Jerry Liu** (@jerryjliu0) | Co-fondateur & CEO LlamaIndex | www.llamaindex.ai, twitter.com |
| **Jonas Roman** | Fondateur Lagentia.fr, AI Engineer | www.youtube.com, lagentia.fr |
| **Nils Reimers** | VP of AI Search | www.nils-reimers.de, sbert.net |
| **Omar Khattab** (@lateinteraction) | Assistant Professor MIT EECS & CSAIL | omarkhattab.com, x.com |
| **Patrick Lewis** | Research Scientist | arxiv.org, cohere.com |

> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer la fiche dans `05-Leaders/rag/` puis relancer `py scripts/sync-leaders.py`.
> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.

<!-- SYNC:leaders:end -->

## Watchlist signaux non canonisés

> Cibles suivies par cc-news mais sans fiche vault dédiée. Section éditable à la main, **jamais touchée par le sync**. Promouvoir un signal en fiche `05-Leaders/rag/` quand il le mérite.

| Personne | Rôle | Sources |
|----------|------|---------|
| **Chip Huyen** (@chiphuyen) | AI Engineering author (fiche vault en `industrie/`) | x.com/chiphuyen, huyenchip.com |

## Queries à exécuter

```
Jonas Roman RAG production
@lateinteraction ColBERT DSPy new features
LlamaIndex new features agentic RAG
Jina AI embeddings reranker new model
Cohere embed rerank new features
@chiphuyen AI engineering RAG
Contextual AI RAG 2.0
MTEB v2 embedding benchmark new leader
@jamescalam RAG tutorial
pgvector OR Qdrant OR Pinecone OR Weaviate new features
new RAG technique pattern (GraphRAG, RAPTOR, CRAG, corrective)
```

## Capitalisation vault

Nouvelles techniques RAG → `04-Techniques/rag/`
Nouveaux modèles d'embeddings → `03-Modeles/<provider>/`
