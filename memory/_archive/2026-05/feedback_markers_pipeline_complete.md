---
name: markers-pipeline-must-be-complete
description: "OBSOLÈTE depuis 22 mai 2026. Le pipeline markers est lui-même un anti-pattern (workflow enforcement). Conservé en archive."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e49ae7dd-c314-4666-aaa1-9c4885ca823f
  revised: 2026-05-22
  status: obsolete
---

## ARCHIVE — Pipeline markers complet

### Statut : OBSOLÈTE depuis 22 mai 2026

Ce feedback disait : "si guard hooks → il FAUT writer + reset, sinon blocage permanent". La règle technique reste correcte. **Mais le pipeline markers entier est un anti-pattern selon doctrine Anthropic 2026.**

Donc ce feedback n'a plus de cas d'application. Aucun pipeline markers ne doit être créé.

### Liens

- [[feedback_enforce_not_advise]] (révisé 22 mai 2026)
- [[feedback_hooks_enforcement_pattern]] (révisé 22 mai 2026)
- [[raisonnement-22mai-doctrine-vs-enforcement]] vault
- [[erreur-hooks-workflow-enforcement]] vault
