---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-07
auteur: claude
tags: ["#type/context", "#meta"]
---
## Phase actuelle
Capitalisation de connaissances dans le vault terminée — dossier `Important/` entièrement réconcilié et vidé, doctrine single-source rétablie.

## Dernière session (2026-06-07)
### Décisions prises
- Sous-dossier `04-Techniques/serving/` créé (granularité validée vs stacks/) : serving-inference-optimisation + prompt-caching-kv-cache + reference-technique-stack-ia (déplacée d'Important/).
- Doctrine reference-grade : doc source = référence exhaustive cherchable MCP, notes atomiques = deltas décisionnels seulement.
- Réconciliation `Important/` menée 1 doc à la fois, 1 commit par doc, validation utilisateur par doc.
- Stack IA.md supprimé + 4 sources mortes nettoyées (pas gardé comme archive).

### En cours
- Rien de bloqué. 7 commits poussés sur main (c3a29b7 → 78f21ef). Working tree clean, branche synchro origin.

### Prochaines étapes
- **Chantier 3/5 wikilinks : CLÔTURÉ 7 juin** (133 → 96 liens brisés, −37). 0 lien cassé par ERREUR ; le résidu 96 est sain et expliqué : ~70 roadmap G1 (contenu à écrire), 8 narration CHANGELOG (→ exclusion Ch.5), ~15 placeholders syntaxiques (F). Voir CHANGELOG entrées 2026-06-07.
- Chantier CONTENU futur (roadmap G1 responsable-ia, ~52 cibles distinctes) — les liens s'auto-réparent à mesure que les notes sont écrites.
- **Chantier 4/5 outils MCP dormants : CLÔTURÉ 7 juin — « rien à réveiller » (résultat prouvé).** Diagnostic `usage_stats(365j)` : 20/22 outils appelés, 2 zéro-appel. `move_note` → LAISSÉ dormant (rare par design, capacité de sûreté réécriture wikilinks ; 0 rename en Ch.2+3 donc aucun bypass). `read_note_resolved` → CANDIDAT SUPPRESSION Ch.5 (cf Fils ouverts). Hypothèse « sur-usage `search_brain` » (1192 appels) testée et INVALIDÉE : échantillon 20 requêtes réelles = 80% vraie exploration / 20% ciblage déguisé (les 4 = 2 notes re-cherchées 2× intra-session, pas un défaut de ciblage). Sur-usage structurel non prouvé → AUCUNE rule de ciblage créée (nuirait à 80% de cas légitimes). `search_brain` à 1192 = sain pour un vault de concepts.

## Fils ouverts
- Le garde-fou lecture-entière (feedback + rule sequence-canonique renforcée) vient d'être posé — surveiller qu'il tient sur les prochains audits/comparaisons (ne plus juger « doublon/subsumé » sur 30 lignes).
- Les canoniques `comment-creer-hook`/`-agent`/`-skill` ont reçu des sections « AJOUT 7 juin » (deltas vérifiés source primaire) — si elles approchent une taille lourde, envisager déport en references/ à terme.
- **Bug frontmatter — `comment-creer-agent`/`-skill`/`-hook`** : double bloc YAML + BOM en tête (`derniere-maj:` seul, puis `﻿---`) → 0 alias / 0 tag au lint. 3 canoniques majeures. Réparation dédiée (retrait BOM + fusion des 2 blocs). Rejoint la tâche hygiène frontmatter du plan. Manip YAML délicate (le BOM casse le parsing) → session attentive, Obsidian fermé, séparée de toute autre écriture — PAS un coup de fin de journée. **+ pendant cette même session dédiée** : dans `comment-creer-agent` (~L762), la liste-exemple d'outils MCP « 21 outils en mai 2026 » cite encore `read_note_resolved` (retiré au Ch.5) — exemple daté, à rafraîchir avec les 3 canoniques ensemble (pas urgent, traces historiques laissées intactes ailleurs).
- ✅ **Chantier 5/5 items à besoin prouvé — EXÉCUTÉS 7 juin** (commit code `0b369b9`) :
  - **`read_note_resolved` SUPPRIMÉ** (arbitrage tranché : pas de consommateur, dormant faute de matériau). Retiré du serveur (`tools/brain.py` méthode + `_resolve_embeds` + wrapper MCP), 6 tests embed, doc vivante (`SKILL.md` 3 lignes via skill-creator + `mcp-vault-llm-design` matrice courante + STATUT v1.4 daté). Historique daté laissé intact (comparaison-28mai, CHANGELOG, exemple comment-creer-agent). 138 tests passent, 0 réf résiduelle dans `.claude/`.
  - **`CHANGELOG.md` exclu du scan source `lint_vault`** (`tools/brain.py:755`, précédent `log.md`). Les 8 liens « cassés » du CHANGELOG = 100% noms morts narratifs entre backticks (vérifiés 1 par 1 : 0 vrai lien réparable). Effet mesuré : **98 → 90 liens cassés** (résidu 90 = roadmap G1 + placeholders, sain).
  - **`traverse_graph` / multi-hop : NON porté** (décision Raphael : pas de consommateur, get_backlinks 1-hop déjà à 8 appels/90j). Laissé prêt-à-porter — faisabilité acquise (table `links` présente), effort faible-moyen, à réveiller si un besoin émerge.
- **Pistes externes à confronter à l'usage RÉEL au Chantier 5** (apportées par Raphael 7 juin — consigne : ne PAS copier, vérifier le besoin per-outil avant tout port). NE PAS migrer vers framework tiers (Cognee/Graphiti/Mem0) : l'espace se consolide H2 2026, le SQLite/FTS5 maison est plus durable.
  - **#1 Multi-hop / graphe (port depuis obsidian-brain)** — **FAISABILITÉ TRANCHÉE par lecture du code (7 juin, `mcp-obsidian-brain/src/database.py`), verdict PER-OUTIL** :
    - **`traverse_graph` → PORTABLE.** `_neighbors` (database.py:466-513) construit les arêtes depuis DEUX sources : (a) **wikilinks** `SELECT target FROM links WHERE source_id = ?` + backlinks — forge A ça, riche ; (b) co-références **symboles** `FROM symbols` — bonus optionnel, ajouté seulement s'il existe. Table symbols vide ⇒ rend le sous-graphe de wikilinks seul (dégradation gracieuse, pas d'échec). Sur forge il marcherait sur le graphe wikilinks (objet du Ch.3). **C'est le vrai candidat.**
    - **`find_concept_chain` → BLOQUÉ** (comme `find_by_symbol`). Structure de couches EN DUR Neoteem `app → app-routes → pg-function → table` (database.py:777-819) ; transitions reposent sur `_frontmatter_refs(note_id,"pg_function"/"table")` + table `symbols WHERE kind=...` + `layer` dérivé du `type` frontmatter. Seule la 1re couche (`app`) utilise les wikilinks ; tout le reste exige le typage `references-*` que forge n'a pas → `_empty_chain (start_layer_unknown)` sur quasi toute note forge. Non portable sans pivot frontmatter structurel.
    - **Table `links` : OUI, persistée + indexée (vérifié 7 juin, forge `database.py:52-57`)** — `CREATE TABLE links (source_id INTEGER REFERENCES notes, target TEXT)` + `idx_links_target` + `idx_links_source`. Peuplée à l'indexation (database.py:110-111, `INSERT INTO links` par wikilink). Schéma **identique** à obsidian-brain. Déjà requêtée en prod par `get_backlinks` (L265-281) et `vault_stats` (`SELECT COUNT(*) FROM links`). Résolution de cible (`exact stem → alias → substring %-stem%`) déjà inline dans `get_backlinks` forge = équivalent de `_resolve_target_to_id` obsidian (L436-463).
    - **Effort port `traverse_graph` seul = FAIBLE-MOYEN** (chirurgie ciblée, pas copier-coller). Forker `traverse()` (BFS) + `_neighbors` + `_resolve_start_ids` depuis obsidian-brain, et **RETIRER les volets symbole** : (a) `_neighbors` L500-512 (co-références `FROM symbols`) ; (b) `_resolve_start_ids` L207-221 (branche `start_kind=='symbol'` → `find_by_symbol`). ⚠️ **forge n'a AUCUNE table `symbols` (absente, pas vide** — grep CREATE TABLE = notes/aliases/links/tags/fts uniquement) : porter `_neighbors` verbatim throw `no such table: symbols`. Le retrait du volet symbole est donc OBLIGATOIRE, pas optionnel. Garder le volet wikilink (L476-498, tables identiques) + le volet note de `_resolve_start_ids` (`resolve_note`, forge a). + enregistrer l'outil dans `server.py` + 1 test (convention forge). **NE PAS porter `find_concept_chain` ni `find_by_symbol`.** Gain 6,8-49× toujours NON vérifié.
    - **⚠️ SHOULD-port (le besoin tranche, pas l'effort) — principe du chantier : réveiller ≠ forcer.** `traverse_graph` à depth=1 EST la généralisation multi-hop de `get_backlinks` — or `get_backlinks` n'a logué que **8 appels / 90j** (bande basse Ch.4). Si le 1-hop est à peine consommé, quel consommateur concret pour le multi-hop que `search_brain` + `get_backlinks` ne couvrent pas déjà ? Trancher AVANT de porter : sans consommateur identifié, ajouter `traverse_graph` = créer un nouvel outil dormant (exactement le set que le Ch.4 vient d'auditer). À arbitrer par Raphael sur le besoin, pas sur la faisabilité (qui, elle, est acquise).
  - **#2 Temporal (Zep/Graphiti)** — raisonner sur « vrai à quelle date » (périmé, contradiction). **Question ouverte, NE PAS résoudre maintenant** : Jarvis en a-t-il besoin vu [[doctrine-vivante]] (verdicts INFO / PIVOT_CANDIDATE / REINFORCE + gate humaine) qui couvre déjà l'évolution doctrinale ? À confronter, pas à porter.
  - **#3 Grille d'éval 5 dimensions (mem0)** — contradiction / temporal / abstention / mise à jour. **Ce n'est PAS un outil mais une grille de MESURE** de la qualité du MCP. Candidate critère d'éval, hors scope « réveiller un outil ».
- **Lecture / positionnement Anthropic (PAS une piste outil)** : arxiv **2601.20404** « On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents » — fichier d'instructions structuré → −28,6 % runtime, −16,6 % tokens, complétion comparable. Conforte la discipline tokens. ⚠️ **Métadonnées du brief corrigées sur source primaire** : auteurs = Lulla/Mohsenimofidi/Galster/Zhang/Baltes/Treude (Canterbury NZ / Singapour / Adelaide), **PAS ETH Zurich** ; **1 papier, pas 2** ; sujet = `AGENTS.md`, pas « fichiers contexte » générique. Fait qualitatif vrai, attribution hallucinée (pattern [[feedback_llm_deep_research_version_numbers]]).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
