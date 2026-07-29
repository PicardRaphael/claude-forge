---
name: classification-type-ticket-jira
description: "Classer un ticket Jira par sa NATURE (FEATURE/BUG/OPTIMISATION), jamais par mimétisme avec un ticket voisin"
trigger: ticket, jira, feature, bug, optimisation, classer
metadata:
  type: feedback
---

Avant de créer un ticket Jira IA, classer par la nature réelle du travail, pas par imitation d'un ticket existant : FEATURE = capacité nouvelle ; BUG = écart cassé à corriger ; OPTIMISATION = amélioration à parité de comportement (perf, qualité, sécu/durcissement, dette, refacto). Durcissement/refacto à parité = OPTIMISATION, jamais FEATURE.

**Why:** 11 juin 2026 — j'ai créé N2-111316 (durcissement SQL, parité fonctionnelle) en `[IA] FEATURE` par mimétisme avec la story S1 (qui, elle, était une vraie feature). Raphael a corrigé : « c'est presque un bug/optimisation ». Mimétisme ≠ classification.
**How to apply:** /spec (neo_ia + back-ts + skill forge neoteem-back-ts) porte la grille dans references/epics-jira.md. Type non évident → AskUserQuestion. Le type Jira `[IA] Optimisation` est créé par le PO côté admin ; tant qu'il n'existe pas, OPTIMISATION retombe sur `[IA] BUG`.

## Lien

- [[feedback_spec_trous_structurels_a_checker]] — autres trous structurels à checker en audit spec
- [[pattern-spec-driven-development]] — workflow idée → forge → /spec → tickets Jira
