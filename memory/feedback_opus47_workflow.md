---
name: opus47-workflow-decisions
description: "Decisions validées Opus 4.7 — architect-first obligatoire, code-reviewer séparé, neo-brain-dev-ia injection. Session 17 avril 2026, révisé 21 mai 2026."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

## Architect-First obligatoire (ia_back + neo_ia)

L'architect Opus DOIT toujours passer avant tout agent dev, même pour les tâches S (fast pass 1 tour).

**Why:** Les dev agents sont Sonnet — ils exécutent un plan, pas du raisonnement ambigu. Sans architect, un "bug S" peut se révéler un "problème M" que le dev Sonnet ne détectera pas.

**How to apply:** Vérifier chaque workflow dans agent-delegation.md : aucun dev ne doit être appelé sans architect en amont.

## Effort levels — Politique CwC 2026 (RÉVISÉ 22 mai après frustration 4h/feature)

**Révision** : xhigh est diminishing returns au-delà du raisonnement profond (Anthropic mai 2026). Précédente politique mettait xhigh partout = 20-40% tokens et latence supplémentaires sans gain qualité.

### Politique révisée

- **xhigh RÉSERVÉ** : `architect` + `dev-lead` (cross-app jugement) + `refactor-pg-function` (raisonnement lourd PG→TS)
- **high par défaut PARTOUT ailleurs** :
  - Dev execution = `sonnet, high` (y compris dev-neochat — corrigé 22 mai)
  - Test-writer = `opus, high` (PAS xhigh — écrire un test n'a pas besoin du même budget que l'architecture)
  - Code-reviewer / security-reviewer = `opus, high`
  - Analystes read-only (sql-optimizer, db-inspector, validator, performance-engineer, etc.) = `opus, high`

### test-writer DÉPRÉCATIONS

- Phase REFACTOR SUPPRIMÉE (fusionnée code-reviewer light)
- MAX 3 tests par comportement (pattern Willison "red-green TDD")

Voir [[pipeline-boris-adapte-neoteem]] pour la recette complète.
Voir [[model-allocation-strategy]] pour la politique sonnet vs opus détaillée.

## neo-brain-dev-ia sur dev-neochat et dev-lead uniquement

NeoChat et dev-lead appellent l'API ia_back. Les autres n'en ont pas besoin.

## Code-reviewer dédié

Séparer design (architect) et review (code-reviewer). Gate obligatoire : dev → test-writer → code-reviewer → commit.
