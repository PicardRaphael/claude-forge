---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-05
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Système de conception de loops de travail livré : skill `/loop-forge` + doctrine vault + canoniques mises à jour. Commit `ca5ace7` poussé sur main.

## Dernière session (2026-06-05)
### Décisions prises
- `/loop-forge` = SKILL (pas agent) — sub-agent ne peut ni orchestrer ni appeler Agent. Session principale dispatche.
- 1 seule skill avec branche code/hors-code (pas 2 skills qui divergeraient).
- Sortie = SPEC `TODO/SPEC-loop-<nom>.md` puis dispatch séparé (pattern /spec, pre-compute).
- Checklist Tasks natif (`TaskCreate`/`TaskUpdate`) comme mécanisme anti-oubli sur skills-questionnaires + agents multi-phases.
- Réflexe "enrichir l'existant avant de créer" ancré 3 niveaux (CLAUDE.md + hook learning-reminder + memory-discipline).

### En cours
- Rien d'inachevé. Plan A+B+C entièrement exécuté, vérifié, commité, poussé.

### Prochaines étapes
- **Dogfooder `/loop-forge`** sur un premier vrai job : "détecter les écarts vault ↔ skills-ref" (le trou /goal+AgentView corrigé à la main cette session = candidat loop parfait). Produit une SPEC + teste la skill en réel.
- Tester `/loop-forge` en session fraîche (auto-trigger + déroulé 9 blocs + arrêt à la SPEC).

## Fils ouverts
- `cc-features-ref` était désynchro du vault (/goal, Agent View ajoutés) — pas de détection auto de ce type d'écart vault↔skill-ref. C'est le candidat loop n°1.
- Idée évoquée mais non traitée : automatiser l'alignement vault↔skills-ref via un loop conçu par `/loop-forge`.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[concevoir-loops-travail]]
[[pre-compute-vs-inference-loops-boris]]
