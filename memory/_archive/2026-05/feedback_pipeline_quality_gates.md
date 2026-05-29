---
name: pipeline-quality-gates
description: "Pipeline qualité = gates CONDITIONNELLES (pas systématiques). architect+test-writer+dev+code-reviewer toujours, le reste selon critères. Revu 22 mai 2026"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2e41f528-a0ac-468c-a271-ba63d887cbd2
---

**Mise à jour 22 mai 2026** — révision majeure après session frustration 4h/feature.

## Règle révisée

Pipeline qualité = gates CONDITIONNELLES selon scope, PAS systématiques. Voir [[pipeline-boris-adapte-neoteem]].

**Why:** Avant le 22 mai, la rule disait "TOUJOURS tous les gates" → ia_back enchaînait api-designer → architect → test-writer red → dev → test-writer refactor → code-reviewer → validator → perf-engineer → security-auditor = 8 agents systématiques sur CRUD simple = 4h pour une feature. Raphael Lead IA disait perdre le plaisir de développer. C'était un signal technique légitime.

**How to apply:**

Gates TOUJOURS : `architect → test-writer red → dev → code-reviewer → commit` (5 étapes).

Gates CONDITIONNELLES (déclencher SEULEMENT si critère rempli) :
- `security-auditor` : SI auth/PII/secrets/file upload touchés
- `performance-engineer` : SI SQL 3+ joins OR endpoint sur table > 100k rows
- `validator` : UNIQUEMENT migrations critiques (PG→TS, refacto critique)
- `outcomes-grader` : SI rubric.md présent dans le dossier feature

Phase REFACTOR test-writer SUPPRIMÉE (fusionnée dans code-reviewer en LIGHT). Voir [[feedback_test_writer_systematic]].

Pour TOUT nouveau repo : démarrer avec le pattern [[pipeline-boris-adapte-neoteem]] et la checklist incluse. Sinon recréation de l'erreur du 21 mai.

## Anti-pattern à NE PLUS faire

- ❌ Rule qui dit "TOUJOURS tous les gates"
- ❌ Pipeline 8 agents sur CRUD simple sans auth/PII/SQL complexe
- ❌ test-writer 2 passes (RED + REFACTOR) systématique
