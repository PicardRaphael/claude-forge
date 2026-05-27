---
name: analyse-first-not-questionnaire
description: "When setting up or auditing a repo, analyze codebase signals first, propose components, ask questions ONLY for what can't be deduced from code"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2c8f61e9-59a4-4658-863a-864e27242ec9
---

Quand Raphael dit "analyse ce repo" ou "setup Claude Code" : analyser le code d'abord, proposer les composants, poser des questions SEULEMENT pour ce qui ne se déduit pas (TDD strict ? commit direct ou PR ? solo ou multi-dev ?).

**Why:** Session 2026-05-21 — Raphael a explicitement dit "sors-toi de la tête les questions obligatoires, tu vas analyser le repo, tu vas me faire une proposition". Le plugin `claude-code-setup` d'Anthropic fait pareil : analyse automatique par signaux codebase, pas questionnaire.

**How to apply:** Suivre le workflow de `pattern-agentic-engineering` vault note : Étape 1 = analyse automatique, Étape 3 = questions seulement pour le non-déductible. Ne JAMAIS commencer par poser 8 questions avant d'avoir lu un seul fichier.

Lié à : [[vault-query-before-create]], [[present-before-build]]
