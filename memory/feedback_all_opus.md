---
name: model-allocation-strategy
description: "Politique Opus/Sonnet repos projet — Sonnet pour execution, Opus pour jugement. Validé CwC 2026 + Raphael 2026-05-21."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Agents d'EXÉCUTION (dev, schema-mapper) = Sonnet high. Agents de JUGEMENT (architect, reviewer, security, debug, analyse) = Opus xhigh.

**Why:** Anthropic Advisor Strategy (CwC 2026) — EVE Legal a obtenu "frontier quality at 5x lower cost" en séparant exécution et conseil. Les agents dev suivent un plan architect, pas du raisonnement ambigu. Le pipeline architect→dev→test→reviewer protège la qualité.

**How to apply:**
- Dev agents (implémentation post-architect) = `model: sonnet, effort: high`
- Exception : `dev-neochat` reste Opus — LangGraph multi-agent trop complexe pour Sonnet
- Jugement (architect, code-reviewer, security, debugger, analyst) = `model: opus, effort: xhigh`
- Gates critiques : `validator`, `refactor-pg-function` = `model: opus, effort: xhigh` (migrations architecturales). **`test-writer` = `opus, effort: high`** (PAS xhigh — révisé 22 mai, cf [[feedback_opus47_workflow]] qui fait foi : xhigh RÉSERVÉ architect/dev-lead/refactor-pg)
- Formatting/mapping (schema-mapper) = `model: sonnet, effort: high`
- SUPERSEDE la politique "zero sonnet" du 5 mai 2026 — invalidée par Anthropic CwC 2026
