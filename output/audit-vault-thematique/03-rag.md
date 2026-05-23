# Audit Vault — Thème : RAG

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md`
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème large, PAS bloqué sur Anthropic) :
>    - **Sources primaires** (les meilleurs du domaine RAG, single source acceptable) : **Douwe Kiela (RAG paper co-auteur, Contextual AI)**, **Patrick Lewis (RAG paper co-auteur)**, **Omar Khattab (ColBERT, DSPy)**, **Nils Reimers (Sentence-BERT, BEIR, Cohere)**, **Han Xiao (Jina AI, late chunking)**, **Greg Kamradt (ChunkViz, semantic chunking)**, **Harrison Chase (LangChain)**, **Jerry Liu (LlamaIndex)**
>    - **Papers académiques arXiv** = single source acceptable (RAG paper original, ColBERT, BGE, etc.)
>    - **Docs officielles** providers RAG (LangChain, LlamaIndex, Cohere, Jina, Voyage AI) sur LEUR produit = single source
>    - **Anthropic** = single source uniquement sur ses features Claude liées RAG (citations, document tokens), pas sur RAG en général
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Scope

**Dossier** : `04-Techniques/rag/`

**Notes à auditer (~10)** :
1. `RAG` (note principale)
2. `rag-architecture`
3. `rag-chunking`
4. `rag-embeddings`
5. `rag-evaluation`
6. `rag-metadata`
7. `rag-production`
8. `rag-reranking`
9. `rag-vector-databases`
10. `tool-retrieval-query-expansion`
11. `ColPali`
12. `jina-embeddings-v4`
13. `sqlite-fts5-vault`

**Note transverse** : `04-Techniques/fine-tuning/rag-vs-fine-tuning`

## Hiérarchie experts (priorité ce thème)

### Liste actuelle forge

**Experts RAG reconnus** (P1) :
- Douwe Kiela (Contextual AI, créateur RAG paper 2020)
- Patrick Lewis (Meta, RAG paper co-auteur)
- Omar Khattab (ColBERT, DSPy)
- Nils Reimers (Sentence-Transformers, Cohere)
- Han Xiao (Jina AI)
- Jerry Liu (LlamaIndex)
- Harrison Chase (LangChain)
- James Briggs (RAG content creator)
- Greg Kamradt (Needle in haystack, RAG)
- Jonas Roman

**Académique** (P2) :
- Auteurs papers RAG, ColBERT, DPR, ANCE

**Vendor** (P3) :
- Pinecone, Weaviate, Qdrant, Chroma, LanceDB (docs)

### Étape 0 — Valider/étendre

WebSearch : "RAG expert 2026", "best RAG researchers", "vector database leader", "embeddings expert reconnu", "reranking expert", "ColBERT Omar Khattab", "DSPy author".

## Sources spécifiques

### Papers (arXiv) — TOUS à fouiller
- "Retrieval-Augmented Generation" (Lewis et al, 2020) — paper RAG original
- "ColBERT" (Khattab Zaharia 2020)
- "ColPali" (Faysse et al, 2024)
- "DPR Dense Passage Retrieval" (Karpukhin 2020)
- "REPLUG" (Shi 2023)
- "Self-RAG" (Asai 2024)
- "Corrective RAG" (Yan 2024)
- "GraphRAG" (Microsoft 2024)
- "Late Chunking" (Jina, 2024)

### Officiel vendors
- python.langchain.com/docs/use_cases/question_answering
- docs.llamaindex.ai
- docs.pinecone.io / weaviate.io / qdrant.io / cohere.com
- platform.openai.com/docs (embeddings)
- jina.ai/news (papers et benchmarks)

### Blogs reconnus
- jamesbriggs.com / pinecone.io/blog
- gkamradt content (LangChain integration RAG)
- huggingface.co/blog (Sentence-Transformers, RAG)
- vespa.ai/blog (production RAG)
- contextual.ai/blog (Kiela)

### Vidéos YouTube à transcripter
- James Briggs RAG videos
- LangChain YouTube channel (Harrison Chase)
- LlamaIndex YouTube
- Jerry Liu RAG talks
- Greg Kamradt "Needle in Haystack" benchmarks
- Anthropic RAG cookbook walkthroughs

## Claims à vérifier (priorité)

### Stats benchmark
- Chunking strategies comparison (fixed vs semantic vs late chunking)
- Embeddings benchmark MTEB
- Vector DB latency comparisons
- Reranker improvements (Cohere reranker, BGE reranker)

### Verbatim
- Toutes les citations attribuées dans rag-architecture
- Stats production (Pinecone, Weaviate users)
- Chiffres ColPali, jina-embeddings-v4

### Choix techno
- Vector DB recommandé : convergence experts ?
- Embeddings 2026 recommandés
- Reranking nécessaire vs optionnel
- Chunking strategy par défaut

### Spécifique forge
- `sqlite-fts5-vault` — décision techno forge, valider performance vs vector DB
- `tool-retrieval-query-expansion` — Anthropic ou pattern général ?

## Étape F — Propagation RAG

Si modifications notes vault :

**Forge** :
- MCP forge-brain (utilise SQLite FTS5 — note rag-architecture impacte)
- Skill `forge-brain` (instructions navigation vault)
- Skills `neo-brain*` qui consomment RAG patterns

**Autres repos** :
- ia_back : aucune RAG appli (à vérifier)
- neo_ia : neodoc utilise RAG potentiellement
- neoteem-brain : vault Obsidian + MCP RAG

**Backlinks** :
- `get_backlinks` pour chaque note rag-*

## Output

`output/audit-vault-thematique/03-rag/` (A à F + rapport)

---

**Commence par étape 0 puis A. advisor() avant transitions.**
