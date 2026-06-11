---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-11
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Migration ia_back → neoteem-back-ts en cours (story S1, N2-111278) — sessions parallèles par worktree opérationnelles sur les deux repos actifs.

## Derniere session (2026-06-11)
### Decisions prises
- Sessions parallèles par US = `claude -w` natif + `/feature <ticket>` (PAS de script worktree manuel — `/feature` gère la branche depuis origin/develop). Déployé neoteem-back-ts (a415bfe) + neo_ia (0e0a696), directement sur develop.
- Fix config-guard validé par Raphael (classifier avait bloqué) : chemin relatif à la racine du worktree, testé 5 chemins — sans lui, sous-agents bloqués en écriture dans tout worktree.
- Sources : doc officielle Anthropic uniquement (howborisusesclaudecode.com = compilation tweets non officielle, rappel Raphael).

### En cours
- neoteem-back-ts : US3 (N2-111281, requalifiée outillage Zod) et US4 (N2-111282, harnais parité — livré d'après CHANGELOG) ; US2 socle neoia-api mergée. Jérôme actif sur le repo.
- neo_ia : us/N2-111316 (durcissement SQL) mergée pendant la session, checkout principal revenu sur develop.

### Prochaines etapes
- Lancer la prochaine vague parallélisable (US5-US8 domaines, après US4) — 4 worktrees possibles, vigilance BDD partagée.
- Vérifier au premier usage réel `claude -w` par Jérôme que `.worktreeinclude` copie bien tout (1er test humain du flow).

## Fils ouverts
- ia_back : système worktrees NON porté (repo en migration vers neoteem-back-ts) — porter seulement si besoin réel.
- Hooks path-based `.claude/` = 5e brique à vérifier dans tout futur repo recevant le système (cf memory reference_worktree_natif_vs_convention_develop).
- Actions humaines back-ts restantes : SEMGREP_APP_TOKEN, branch restrictions, Aikido (devops).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
