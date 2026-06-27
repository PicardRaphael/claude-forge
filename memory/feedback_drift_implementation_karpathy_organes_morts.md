---
name: drift-implementation-karpathy-organes-morts
description: forge-brain a dérivé du pattern Karpathy — raw/ abandonné, index.md stale +51%, Query keyword-only. Un système qui marche malgré un organe mort cache son drift.
metadata:
  type: feedback
---

Constat empirique 8 juin 2026 (comparaison forge-brain vs pattern Karpathy LLM Wiki) : forge-brain a un **meilleur moteur** que le Gist Karpathy (read_section, pagination, lint, observabilité, lifecycle) mais **n'alimente plus 2 des 3 organes obligatoires** et a **sauté la moitié vectorielle** du retrieval :

- **`raw/` abandonné** : 8 notes, toutes du 22 mai. cc-news/x-read/defuddle/watch transforment la source en note wiki sans archiver le brut → perte de la « source of truth » Karpathy (anti-hallucination).
- **`index.md` stale +51%** : annonce 318 notes, le vault en a 480. L'organe « lu en premier au Query » est périmé.
- **Query keyword-only** : search_brain = FTS5 BM25 pur (0 vectoriel, 0 rerank), et c'est l'outil n°1 (1237 appels/30j). Karpathy recommande nommément qmd = BM25+vector+rerank. Le savoir RAG existe déjà au vault ([[rag-reranking]]) — le manque est l'application au MCP, pas le savoir.

**MISE À JOUR 27 juin 2026 — raw/ n'est plus une « dérive » mais une DÉCISION DÉLIBÉRÉE :** pivot agent-first acté ([[decision-vault-agent-first]]) — forge-brain s'émancipe de Karpathy, `raw/` **supprimé** (bruts = variables jetables), index/log/MOC = couche humaine optionnelle. Le trigger de réouverture devient une **condition de falsification** : re-créer raw/ uniquement au 1er incident d'hallucination remontant à une source non archivée. La méta-leçon ci-dessous (« un système qui marche cache son drift » + « valoriser ≠ consommer ») reste valide. Instruction du pivot : [[raisonnement-2026-06-27-vault-agent-first]].

**MISE À JOUR 8 juin (mesure usage.jsonl) — le constat tient, l'implication « défaut à réparer » est FAUSSE pour 2 des 3 :** mesuré sur 1239 search_brain/30j → **vrai ratage BM25 = 0,89%** (et non-sémantique : recherches par nom de fichier qui auraient dû être des read_note). Bilan tokens d'un vectoriel = NÉGATIF (embedding 1239 req/mois + re-embed 680k tokens vault vs ~20k chars économisés). **Accès à raw/ = 0 sur 30j** (besoin fiabilité non matérialisé). → **② vectoriel et ① raw/ = écarts ASSUMÉS, pas chantiers** (avec triggers de réouverture). Seul #3 index.md (non mesuré) reste un geste mécanique possible. Détail chiffré + triggers : section « REQUALIFICATION POST-MESURE » de [[pattern-vault-llm-karpathy]].

**Why:** Le drift est SILENCIEUX car le système marche quand même (on tape search_brain direct, donc index stale + raw mort ne bloquent rien). Le pattern canonique est contourné dans la pratique sans décision explicite. **Un système qui fonctionne malgré un organe mort cache son propre drift** — d'où la nécessité de vérifier empiriquement l'état réel (vault_stats, usage_stats, list_notes) et pas seulement lire la doctrine.

**How to apply:** Quand on compare l'implémentation à une doctrine canonique, NE PAS se fier aux notes qui décrivent l'état passé — vérifier le réel (`vault_stats`, `usage_stats`, `list_notes("raw")`, lecture des fichiers obligatoires). Détail complet + réparations par ROI dans la section « DRIFT D'IMPLÉMENTATION » de [[pattern-vault-llm-karpathy]]. Cas frère du drift doctrine↔réel : [[doctrine-drift-silent-regression]].

**Garde-fou anti sur-diagnostic (objection Raphael 8 juin, dans le même échange) :** un manque vs la doctrine n'est un DÉFAUT que s'il a un CONSOMMATEUR prouvé. **Valoriser ≠ consommer** : Karpathy peut valoriser une feature (ex. graph view / traverse_graph) sans qu'on en ait l'usage. Avant de qualifier un manque d'« angle mort à combler », vérifier `usage_stats` du consommateur le plus proche (ex. `get_backlinks` à 10 appels/30j → un traverse_graph N-sauts n'a aucune demande). Sinon on confond la **discipline anti-gonflage** (manque théorique sciemment écarté faute de besoin = sain, cf limites #3/#4 Chantier 5, `read_note_resolved` retiré pour 0 appel) avec une **lacune**. J'ai fait cette erreur en présentant la traversée graphe comme un défaut — corrigé après objection. Distinction codifiée dans la section « manque à combler vs écarté faute de consommateur » de [[pattern-vault-llm-karpathy]].
