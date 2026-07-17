# Future backends

The application owns ports for canonical storage, lexical index, audit, outcomes and procedures. Semantic and temporal-graph ports define future boundaries but have no v1 implementation.

Before adding embeddings, benchmark FTS5 on a labeled retrieval set: recall@5/10, MRR/nDCG, private-document leakage (must remain zero), latency, index size, rebuild time and operator cost. Add semantic retrieval only if lexical recall misses outcome-relevant paraphrases by an agreed margin and reranking materially improves the held-out set.

A temporal graph such as Graphiti is justified only when multi-hop temporal questions, contradiction-over-time resolution or validity intervals cannot be answered reliably from canonical revisions plus lexical retrieval; the workload and accuracy gain must exceed operational/security cost. The graph remains a rebuildable projection, never canonical state.

Any external backend adapter must preserve fixed-principal filtering before retrieval, deterministic rebuild, non-revealing misses, idempotent mutations and domain independence from vendor types.
