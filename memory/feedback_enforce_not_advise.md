---
name: enforce-not-advise
description: "Quand l'advisory est SKIPPÉ (compliance miss), corriger via hook. PAS quand la sur-conformité existe déjà — la sur-enforcement est son propre mode de défaillance. Hooks = lint/security/scope, JAMAIS workflow agentique."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42f0ff3e-7431-4682-bf0b-f2823840a715
  revised: 2026-05-22
---

## Règle (révisée 22 mai 2026)

### Scope d'application

Si un comportement est identifié comme "advisory mais pas enforced" ET que la session ignore systématiquement l'advisory → créer un hook bloquant exit 2.

### Anti-scope (NOUVEAU 22 mai 2026)

Si la session respecte déjà l'advisory (compliance > 80%) ET que le hook proposé forcerait un **workflow agentique** (architect-first, code-reviewer-before-commit, delegation forcée à un dev agent) → **NE PAS créer le hook**. C'est l'inverse du problème : sur-enforcement génère sa propre friction (mesurée 6× sur ia_back + neo_ia le 21-22 mai).

**Why scope révisé :** Session 22 mai 2026 — refonte ia_back + neo_ia. Suppression de 7 hooks workflow (architect-guard, commit-guard, dispatch-guard, marker-protect, agent-marker-writer, pipeline-reset, session-reset-markers) car friction 6×. Doctrine Anthropic 2026 (Agent SDK "Claude decides when to invoke", Boris Cherny "thinnest wrapper") : hooks = lint/security/observabilité, workflow = doctrine dans rules + session juge.

### How to apply

**Hook légitime** (toujours créer si advisory skippé) :
- Sécurité : empêcher `rm -rf`, force-push main, commit de secrets
- Scope : `repo-scope-guard` (pas de lecture repos voisins)
- Architecture immutable : `guard-pg-repo-readonly`, `guard-core-imports`
- Convention de test : pas de `pytest`/`bun test` global
- Lint/format/typecheck

**Hook illégitime** (NE PAS créer même si l'advisory peut être skippé) :
- Forcer une séquence d'agents (architect → dev → reviewer)
- Bloquer la session principale d'écrire du code
- Liste de paths/fichiers critiques dans le code du hook (devient obsolète au prochain refacto)
- Markers `.foo-marker` pour orchestrer un pipeline

**Si l'advisory workflow est skippé** : améliorer la description de l'agent + la rule + CLAUDE.md gotcha. Le skip indique souvent que la doctrine est mal calibrée, pas qu'il manque d'enforcement.

### Source

- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[erreur-hooks-workflow-enforcement]]
- Anthropic Agent SDK overview, Boris Cherny (Pragmatic Engineer)
