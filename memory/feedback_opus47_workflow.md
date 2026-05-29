---
name: opus47-workflow-decisions
description: "Decisions validées Opus 4.7 — architect-first obligatoire, code-reviewer séparé, neo-brain-dev-ia injection. Session 17 avril 2026, révisé 21 mai 2026."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Cf [[raisonnement-revirement-pipeline-mai-2026]] (doctrine : chemin de raisonnement du pivot pipeline mai 2026 — retire architect → architect rapide → pipeline conditionnel, advisor+DA obligatoires, mesurer avant optimiser).

**Cas empirique(s) :**

- **Architect-First obligatoire (ia_back + neo_ia)** : l'architect Opus DOIT toujours passer avant tout agent dev, même pour les tâches S (fast pass 1 tour). Vérification : aucun dev appelé sans architect en amont dans `agent-delegation.md`.

- **Allocation effort par agent (RÉVISÉ 22 mai après frustration 4h/feature)** — `xhigh` RÉSERVÉ : `architect` + `dev-lead` (cross-app jugement) + `refactor-pg-function` (raisonnement lourd PG→TS). `high` par défaut PARTOUT ailleurs :
  - Dev execution = `sonnet, high` (y compris dev-neochat — corrigé 22 mai)
  - Test-writer = `opus, high` (PAS xhigh)
  - Code-reviewer / security-reviewer = `opus, high`
  - Analystes read-only (sql-optimizer, db-inspector, validator, performance-engineer, etc.) = `opus, high`

- **test-writer dépréciations** : Phase REFACTOR SUPPRIMÉE (fusionnée code-reviewer light). MAX 3 tests par comportement (pattern Willison "red-green TDD"). Voir aussi [[pipeline-boris-adapte-neoteem]] (recette complète) et [[model-allocation-strategy]] (politique sonnet vs opus détaillée).

- **neo-brain-dev-ia sur dev-neochat et dev-lead uniquement** : NeoChat et dev-lead appellent l'API ia_back. Les autres n'en ont pas besoin.

- **Code-reviewer dédié** : séparer design (architect) et review (code-reviewer). Gate obligatoire : dev → test-writer → code-reviewer → commit.
