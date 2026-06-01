---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-01
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle
Chantier complet d'optimisation + audit du setup **neoteem-brain** (repo `neot-v2/neoteem-brain`) : 5 plugins distribués neo-brain + tout le `.claude/` interne. 7 commits poussés sur `master`.

## Derniere session (2026-06-01)
### Decisions prises (toutes dans le repo neoteem-brain, pas forge)
- **5 skills neo-brain : 0 fusion / 0 division.** Axe de découpage = domaine (généraliste vs stack IA) + permission (RO vs RO+write). Le plugin installé EST le gate RBAC (write sans authz serveur, vérifié dans `brain.py` : `username` = nom de branche git seulement).
- **Seuils pipeline gravés** (`pipeline.md` source unique, `quality-gates.md` fusionné dedans) : vault-linker ≥1 note, sync-checker >3, vault-validator >5. Le "≥1 vs >3" n'était pas une contradiction (>3 = pipeline complet, pas vault-linker seul).
- **Lint references-* = outil mainteneur**, pas dans les skills. Backfill au merge via `scripts/enrich-references.py` (existait déjà). 101 notes enrichies appliquées.
- **Réindexation symbols = automatique** : le watcher MCP (`parse_note`→`index_note`) peuple FTS5 ET la table symbols en une passe, sur la boucle `_git_pull`. Reindex manuel superflu (prouvé par le log watcher).
- **Sécurité honnête** : CLAUDE.md neoteem-brain disait à tort "le hook bloque les écritures hors vault" → corrigé (Bash non intercepté + SoT par convention). Bug prefix-match du hook corrigé (sibling `-backup` passait).

### En cours
- Rien d'ouvert. 7 commits sur `origin/master` neoteem-brain (de `bdad3a8` à `fdae8d4`). Working tree propre.
- ⚠️ Raphael doit **redémarrer sa session** pour que le nouveau `settings.json` neoteem-brain (permissions MCP + hooks) soit pris en compte, + `/reload-plugins` pour propager versions plugins (3.0.3/2.0.3) au cache.

### Prochaines etapes
- (Optionnel) 160 notes residuelles ont des references-* non auto-déductibles du corps → décision humaine si on veut pousser la complétude graph plus loin.
- (Optionnel) Câbler le Lint au merge (hook post-merge OU CI Bitbucket) quand le flux PR/VM neoteem-brain sera stabilisé — la logique (`validate-v2.py` + `enrich-references.py`) est prête, seul le déclencheur manque.

## Fils ouverts
- ⚠️ Hygiène mémoire forge : ~233 fichiers memory/ (cible <100) → `/clean-memory` en session dédiée.
- Trilogie docs stratégiques IA Neoteem : présentation Jérôme puis CODIR (commit `3a0f373`).
- Cadrage NeoMail = décision client, trame d'interview à préparer.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
