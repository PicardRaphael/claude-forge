---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-10
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Migration ia_back → neoia-api lancée pour de vrai : S1 (N2-111278) + 12 sous-tâches dans Jira, US1 en correction par Jérôme (refacto schéma), harness des 3 repos durci et optimisé suite aux premiers incidents de production.

## Dernière session (2026-06-10)
### Décisions prises
- Hiérarchie Jira réelle : 5 epics permanents FIGÉS, story S1 = N2-111278 ([IA] FEATURE), 12 sous-tâches N2-111279→91. Assigné demandé via AskUserQuestion avant toute création (×3 skills).
- Fin convention E0 : neoteem-back-ts travaille sur develop (PR `us/{N°}` → develop), 6 branches alignées à la demande.
- neo_ia aligné modèle back-ts : /feature, Default-FAIL, memory/ compounding, workflow PR, CI Bitbucket créée (l'ancienne GitHub Actions ne tournait PAS).
- Relance sub-agent après escalade = resume `agent_id` ou re-brief riche, jamais un prompt nu (rule ×3 repos + vault).
- Optimisation 3 repos : checks lourds → hook Stop (typecheck), hooks python direct neo_ia (-50 % latence), dispatchers forge, security-guard durci fail-closed, agents dev en vérifs par LOTS.
- Incident US1 : schéma généré monolithique → organisation à DEUX AXES (logique par domaine MÉTIER commun/syndic/gerance/comptabilite/reporting ; schéma généré par groupes d'ARTICULATION BDD), limite stricte 1000 lignes (hook + CI + rule), assertion structurelle = critère de done des artefacts générés.
- Méthode : taxonomie d'archi = croiser PLUSIEURS sources NeoBrain (Damier × 01-Domaines × MOC-BDD × schema-public) — jamais une seule.

### En cours
- Jérôme refactore le schéma sur `us/N2-111279` (prompt fourni : mapping schema-domains.json → assertion structurelle TDD → postprocess éclaté → vert). develop mergé dans sa branche (dee288f).
- CI back-ts à surveiller sur a43e32a.

### Prochaines étapes
- US2+ du pipeline /feature (canari validé, discipline anti-relances active).
- Session dédiée : fin fusion rules (forge 16→13 fait partiellement, neo_ia 18→12 pas commencé), /clean-memory forge (261 fichiers), descriptions skills forge > 250c.
- Actions humaines : activer Bitbucket Pipelines neo_ia, webhooks GChat+Discord à régénérer (laissés tels quels sur décision Raphael), PGSSLROOTCERT back-ts différé.

## Fils ouverts
- Faux positif security-guard forge : `push .*-f` traverse les segments d'une commande composée (raffiner regex `[^|;&]*`).
- `_a-classer`/mapping schema-domains.json : à valider sur la PR de Jérôme.
- Analyse mémoire/architecture neo_ia approfondie (reportée après les stories).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[workflow-claude-code-optimal]] · [[anti-reentrance-sub-agents-pattern-escalade]] · [[comment-creer-hook]] · [[conventions-naming-typescript]]