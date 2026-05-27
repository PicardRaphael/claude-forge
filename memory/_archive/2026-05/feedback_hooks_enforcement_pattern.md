---
name: hooks-enforcement-pattern
description: "OBSOLÈTE depuis 22 mai 2026. Le pattern marker+guard pour forcer un workflow agentique (architect → dev → reviewer) est un anti-pattern selon doctrine Anthropic. Conservé en archive — voir feedback_enforce_not_advise pour la doctrine révisée."
type: feedback
originSessionId: a0a0f09b-5e48-4a59-b83d-c29d9a0d60ff
revised: 2026-05-22
status: obsolete
---

## ARCHIVE — Pattern marker+guard pour workflow agentique

### Statut : OBSOLÈTE depuis 22 mai 2026

Ce pattern (PostToolUse Agent → marker, PreToolUse Write/Edit → guard exit 2) a été appliqué sur neo_ia (7 mai) puis ia_back. Friction 6× mesurée le 22 mai. Tous les hooks workflow ont été supprimés :

- `architect-guard.{ts,py}` ❌
- `commit-guard.{ts,py}` ❌
- `dispatch-guard.{ts,py}` ❌
- `marker-protect.{ts,py}` ❌
- `agent-marker-writer.{ts,py}` ❌
- `pipeline-reset.{ts,py}` ❌
- `session-reset-markers.{ts,py}` ❌

### Pourquoi obsolète

Doctrine Anthropic 2026 :
- Agent SDK : "Claude decides when to invoke subagents"
- Boris Cherny : "thinnest wrapper", "complex scaffolding rendered obsolete by next model"
- Hooks reference : exemples = lint/security/scope, JAMAIS workflow

Le pattern marker+guard force la séquence agentique, ce qui contredit ces 3 doctrines.

### Pattern actuel (à utiliser)

- **Doctrine workflow** : `rules/when-to-architect.md` + `rules/quality-gates.md` + descriptions d'agents
- **Hooks légitimes** : `repo-scope-guard`, `guard-pytest-scope`, `guard-test-scope`, `guard-core-imports`, `guard-pg-repo-readonly`, lint/format/typecheck

### Pattern technique conservé pour hooks LÉGITIMES

Si tu crées un hook légitime (security, scope, lint), les détails techniques restent valides :
- Chemins absolus via `Path(__file__)` / `import.meta.dir`
- `_make_relative()` pour normaliser chemins absolus des subagents
- Champ "if" settings.json NE FONCTIONNE PAS → filtrer dans le script
- Détecter agent via stdin JSON `agent_type`/`subagent_type`, PAS via env var `CLAUDE_AGENT`

### Liens

- [[feedback_enforce_not_advise]] (révisé 22 mai avec scope)
- [[raisonnement-22mai-doctrine-vs-enforcement]] vault
- [[erreur-hooks-workflow-enforcement]] vault
