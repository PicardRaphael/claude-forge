---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-07
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle
**Tâche RULES finale CLOSE** (la dernière du plan post-6-B). Doctrine d'écriture vault périmée purgée des skills + CLAUDE.md. Plus rien à reprendre à froid sur le chantier doctrine. Restent les fils ouverts indépendants (Chantier 5 limites MCP #1/#3/#4, bug frontmatter 3 canoniques).

## Dernière session (2026-06-07)
### Décisions prises
- **Tâche rules — diagnostic puis 5 édits ciblés** (commit `327fc3e`), tous validés ligne par ligne par Raphael avant écriture :
  - `done/SKILL.md` L222+L301 : « `Write` la note vault » → MCP-only. C'était **cassé au runtime** (`vault-write-guard` matche `Write|Edit|MultiEdit`, pas que Edit), pas juste obsolète. Distinction note NEUVE (`create_note`, porte garde BOM) vs note EXISTANTE (`append_note`/`update_property`/`update_note` ou `*_by_path` si stem ambigu) — correction Raphael : `create_note` seul aurait échoué sur une note déjà créée.
  - `forge-brain/SKILL.md` : ajout des 4 outils `*_by_path` (table écriture + matrice décision) pour stems ambigus log/index/CHANGELOG. Non redondant avec le hook : le hook bloque l'Edit direct mais ne dit pas QUEL outil utiliser à la place (capacité).
  - `CLAUDE.md` L20 : « l'enrichir (`insert_section`/Edit) » → distingue vault (`insert_section`/MCP) vs hors-vault rules/CLAUDE.md/memory (`Edit`). L'ancien `/Edit` seul envoyait vers un Edit bloqué = message-piège. Bloc Critiques reste sous 25 lignes (fin L23).
  - **L218 `done` (`Write` dans `memory/`, hors vault) NON touché** — `memory/` hors `vault/claude-forge/`, le hook ne le matche pas, `Write` y reste valide. Pas de zèle.
- **#9 SKIP confirmé** : aucune rule « vault via MCP » créée — redondante avec le hook + CLAUDE.md L18/L20.
- **Item PRIORITÉ du brief tranché** : l'interdiction « jamais `update_property` sur array YAML » est **absente** de la couche comportement permanent (rules/CLAUDE.md/skills). Elle ne vivait qu'en vault (`erreur-mcp-yaml-dump-corruption`, **déjà corrigé** 2 encadrés RÉSOLU `2ff0538`+`63a8f66`) + CHANGELOG (historique, hors-scope). Fix array-safe EN PROD (`brain.py:1150,1364`, 17 tests). → aucune action rule/skill. Anti-gonflage respecté.
- **Capitalisation** : feedback tier-2 `feedback_hook_arme_perime_instructions_skills.md` — armer un hook PreToolUse périme SILENCIEUSEMENT au runtime les instructions de skills écrites avant ; réflexe = grep le verbe bloqué dans le périmètre gardé après avoir armé un hook. Réutilisable à chaque futur hook bloquant.

### En cours
- Rien de bloqué. Commit `327fc3e` poussé sur main, working tree clean, branche synchro origin.

### Prochaines étapes
- Reprendre le **Chantier 5/5 (DEV MCP)** : 3 limites MCP restantes (#1 `lint_vault` non paginé · #3 lock inter-écritures · #4 lag réindexation agrégats). #2 array-safe = FAIT (`2ff0538`). Détails dans Fils ouverts.
- Réparer le **bug frontmatter** des 3 canoniques `comment-creer-agent`/`-skill`/`-hook` (double bloc YAML + BOM en milieu → 0 alias/0 tag au lint). Session attentive dédiée, Obsidian fermé.

## Fils ouverts

- 🟡 **Chantier 5/5 (DEV MCP) — 3 limites restantes** (faites : #2 array-safe `2ff0538` ; #5 CHANGELOG exclu scan source `lint_vault` `0b369b9` ; #6 `read_note_resolved` supprimé `0b369b9`) :
  - ⬜ **#1 — `lint_vault` non paginé** : plafond `limit=50` par catégorie (`tools/brain.py:715`). Fix = pagination autoguidée (porter le mécanisme `read_note` offset/header).
  - ⬜ **#3 — lock inter-écritures MCP** : race-condition si 2 écritures MCP concurrentes (sub-agents //). Fix = lock fichier/DB sur les ops d'écriture. Cf [[limite-mcp-lock-inter-ecritures]].
  - ⬜ **#4 — lag réindexation agrégats** : `get_tags`/`lint_vault` accusent un délai après écriture HORS MCP. Vérité prise sur `find_by_property` en attendant. Fix = invalidation/refresh agrégats post-write. Cf [[limite-mcp-lag-reindexation-agregats]].
  - ❌ Piste multi-hop `traverse_graph` : NON portée (décision Raphael — pas de consommateur, `get_backlinks` 1-hop à 8 appels/90j). Faisabilité acquise (table `links` présente), prêt-à-porter si un besoin émerge.

- **Bug frontmatter — `comment-creer-agent`/`-skill`/`-hook`** : double bloc YAML + BOM en milieu de fichier (`derniere-maj:` seul, puis `﻿---`) → 0 alias / 0 tag au lint. 3 canoniques majeures. Réparation dédiée (retrait BOM + fusion des 2 blocs). Manip YAML délicate → session attentive, Obsidian fermé, séparée. + dans `comment-creer-agent` (~L762) : exemple « 21 outils en mai 2026 » cite encore `read_note_resolved` (retiré Ch.5) — à rafraîchir avec les 3 canoniques ensemble.

- 🟡 **Hors-scope tracés par la tâche rules (à corriger plus tard, NE PAS confondre avec un blocage)** :
  - ⬜ **`context-actuel.md` (cette note) — array-safe #2** : était marqué ⬜ non-fait alors qu'en prod (`2ff0538`). **CORRIGÉ dans cette mise à jour** (passé en « faite »).
  - ⬜ **`mcp-vault-llm-design` (vault)** : métrique « 15→19 tools » + exemple citant `read_note_resolved` dans le corps, alors que le STATUT v1.4 documente bien son retrait (Ch.5). Incohérence interne mineure — correction via MCP (`update_note`/`insert_section`) plus tard, pas urgent.

- Les canoniques `comment-creer-hook`/`-agent`/`-skill` ont des sections « AJOUT 7 juin » (deltas source primaire) — si elles deviennent lourdes, envisager déport en `references/`.
- Le garde-fou lecture-entière (feedback + rule sequence-canonique) reste à surveiller sur les prochains audits.
- **Pistes externes à confronter à l'usage RÉEL** (apportées par Raphael 7 juin, NE PAS migrer vers framework tiers Cognee/Graphiti/Mem0) : #1 multi-hop `traverse_graph` (faisabilité tranchée, port faible-moyen, manque consommateur) · #2 temporal Zep/Graphiti (question ouverte vs [[doctrine-vivante]]) · #3 grille d'éval 5 dimensions mem0 (grille de mesure, pas un outil).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
