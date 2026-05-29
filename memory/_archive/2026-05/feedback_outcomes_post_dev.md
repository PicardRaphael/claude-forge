---
name: outcomes-post-dev-not-architect
description: "Outcomes-test évalue du CODE (post-dev), pas des PLANS (post-architect). Pattern Anthropic CwC 2026 conçu pour artefacts concrets."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Le pattern Outcomes (grader séparé + rubric) évalue du CODE concret, pas des plans textuels.

**Why:** Session 2026-05-21 — DA a identifié comme bloquant : les Outcomes Anthropic évaluent des outputs concrets (code, fichiers) contre des critères vérifiables (tests passent, types corrects). Appliquer ça à des plans textuels produit des jugements d'opinion déguisés en tableaux factuels.

**How to apply:**
- Pipeline : architect → dev → test-writer → `/outcomes-test` → code-reviewer → commit
- Outcomes = post-dev (évalue le code produit)
- Pour évaluer un plan architect → DA (critique créative), pas Outcomes (vérification mécanique)
- Rubric templates adaptés par stack (TypeScript hexagonal, Python LangGraph, générique)
