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
**Chantier 6-B ENTIÈREMENT CLOS** (les 3 pièces prouvées en prod + poussées). Plus rien à reprendre à froid sur 6-B. Restent des fils ouverts indépendants (chantier 5 limites MCP, hygiène frontmatter canoniques).

## Dernière session (2026-06-07)
### Décisions prises
- **Pièce 2 (hook `vault-write-guard.py`) PROUVÉE EN PROD** — 5 cas testés en session fraîche (hook armé `e566e76`), **zéro faux positif** :
  - CAS 1 (Edit direct note `.md` vault → bloqué exit 2) : **vrai Edit LIVE** refusé par le harness, debug log confirme `vault-write-guard`, fichier intact.
  - CAS 2 (`append_note_by_path` sur note vault → marche) : **vrai MCP LIVE**, hook aveugle au MCP.
  - CAS 3 (Edit hors-vault → marche) : **vrai Edit LIVE** sur `memory/MEMORY.md` + isolation `.claude/` racine et code `.py`.
  - CAS 4 (`MEMORY.md` sous `vault/claude-forge/.claude/` → exemption) : exit 0.
  - CAS 5 (plan file `~/.claude/plans/` → PAS de faux positif) : isolation sur le **vrai** plan file, exit 0. Le faux positif historique [[erreur-hook-garde-hors-vault-bloque-plan-file]] est **ABSENT** (chemin sans marqueur `vault/claude-forge` → exclu par construction).
  - +2 bonus robustesse : note vault forward-slash → bloque ; `.claude`-dans-le-nom hors sous-arbre → bloque (détection par **SEGMENT** prouvée, pas substring).
- **fix(tests) `bf6cf00`** : `test_delegate_guard.py` resynchronisé au refactor du modèle de bypass (`required_agent`→`required_specialist`, `is_typo_edit`→`is_typo_change` nouvelle signature, `agent_bypass_active` supprimé → 9 tests de bypass réécrits end-to-end via subprocess + transcript `attributionSkill`, dont le joyau « vrai spécialiste mais MAUVAIS pour ce type de fichier → bloqué »). +8 tests (28→36). Zone d'ombre (collection plantait) FERMÉE.
- **docs(hooks) `0ae5a0d`** : pièce 3 messages-pièges corrigés (`mcp-alias-guard.py` docstring+message stderr, `vault-cat-guard.py` 2 docstrings, `vault-write-guard.py` parenthétique + 2 commentaires de test) → pointent les 4 outils `*_by_path` au lieu du fallback « Read+Edit direct » devenu interdit. Texte pur, zéro logique.
- **Racine du drift corrigée** : `memory/feedback_mcp_alias_ambigu_chemin_exact.md` prêchait massivement « Edit/Python-FS direct » → encadré RÉSOLU 6-B en tête + prescriptions périmées neutralisées (historique 7 violations préservé).
- **Capitalisation** : enrichi `reference_auto_mode_classifier.md` (classifier bloque aussi les hooks sécu `.py` voisins, juge l'intention par-dessus le brief) + nouveau feedback tier-2 `feedback_test_hook_json_dumps.md`.

### En cours
- Rien de bloqué. 3 commits poussés sur main (`bf6cf00` → `0ae5a0d`), working tree clean, branche synchro origin. 273 tests verts toute la suite hooks.

### Prochaines étapes
- Reprendre le **Chantier 5/5 (DEV MCP)** : 4 limites MCP restantes (#1 `lint_vault` non paginé · #2 `rename_tag`/écriture array-safe · #3 lock inter-écritures · #4 lag réindexation agrégats). Détails dans Fils ouverts.
- Réparer le **bug frontmatter** des 3 canoniques `comment-creer-agent`/`-skill`/`-hook` (double bloc YAML + BOM → 0 alias/0 tag au lint). Session attentive dédiée, Obsidian fermé.

## Fils ouverts

- 🟡 **Chantier 5/5 (DEV MCP) — 4 limites restantes** (2 faites le 7 juin : #5 CHANGELOG exclu du scan source `lint_vault` `0b369b9` ; #6 `read_note_resolved` supprimé `0b369b9`) :
  - ⬜ **#1 — `lint_vault` non paginé** : plafond `limit=50` par catégorie (`tools/brain.py:715`). Fix = pagination autoguidée (porter le mécanisme `read_note` offset/header).
  - ⬜ **#2 — outil `rename_tag` / écriture array-safe** : `update_property` corrompt les arrays YAML (tags/aliases/sources) — 3 incidents (cf [[erreur-mcp-yaml-dump-corruption]]). Contournement actuel = jamais `update_property` sur array → `update_note`/Edit+reindex. Fix = `rename_tag` dédié + sérialisation array-safe.
  - ⬜ **#3 — lock inter-écritures MCP** : race-condition si 2 écritures MCP concurrentes (sub-agents //). Fix = lock fichier/DB sur les ops d'écriture. Cf [[limite-mcp-lock-inter-ecritures]].
  - ⬜ **#4 — lag réindexation agrégats** : `get_tags`/`lint_vault` accusent un délai après écriture HORS MCP. Vérité prise sur `find_by_property` en attendant. Fix = invalidation/refresh agrégats post-write. Cf [[limite-mcp-lag-reindexation-agregats]].
  - ❌ Piste multi-hop `traverse_graph` : NON portée (décision Raphael — pas de consommateur, `get_backlinks` 1-hop à 8 appels/90j). Faisabilité acquise (table `links` présente), prêt-à-porter si un besoin émerge.

- **Bug frontmatter — `comment-creer-agent`/`-skill`/`-hook`** : double bloc YAML + BOM en tête (`derniere-maj:` seul, puis `﻿---`) → 0 alias / 0 tag au lint. 3 canoniques majeures. Réparation dédiée (retrait BOM + fusion des 2 blocs). Manip YAML délicate → session attentive, Obsidian fermé, séparée. + dans `comment-creer-agent` (~L762) : exemple « 21 outils en mai 2026 » cite encore `read_note_resolved` (retiré Ch.5) — à rafraîchir avec les 3 canoniques ensemble.
- Les canoniques `comment-creer-hook`/`-agent`/`-skill` ont des sections « AJOUT 7 juin » (deltas source primaire) — si elles deviennent lourdes, envisager déport en `references/`.
- Le garde-fou lecture-entière (feedback + rule sequence-canonique) reste à surveiller sur les prochains audits.
- **Pistes externes à confronter à l'usage RÉEL** (apportées par Raphael 7 juin, NE PAS migrer vers framework tiers Cognee/Graphiti/Mem0) : #1 multi-hop `traverse_graph` (faisabilité tranchée, port faible-moyen, manque consommateur) · #2 temporal Zep/Graphiti (question ouverte vs [[doctrine-vivante]]) · #3 grille d'éval 5 dimensions mem0 (grille de mesure, pas un outil).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
