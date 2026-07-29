---
name: present-before-build
description: "TOUJOURS présenter le plan complet à Raphael AVANT de construire quoi que ce soit. Ne pas commencer à créer des notes, skills, ou agents sans validation."
trigger: cree, construis, ecris, genere, fais moi, plan
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42f0ff3e-7431-4682-bf0b-f2823840a715
---

## Règle

Présenter le plan complet AVANT de construire. Ne JAMAIS commencer à créer (notes vault, skills, agents) sans que Raphael ait validé la direction.

**Why:** Session 2026-05-12 — j'ai commencé à créer une note vault `pattern-spec-driven-development` avant que Raphael valide le design de /spec. Il a dit "tu as commencé sans moi". Le plan doit être présenté et validé AVANT toute action de construction.

**How to apply:**
- Recherche/exploration = OK sans validation (orientation, pas substantif)
- Construction (Write, skills, agents, notes vault) = TOUJOURS après validation Raphael
- Advisor/DA = OK sans validation (c'est du counsel, pas de la construction)
- Si Raphael dit "go" → construire. Sinon → présenter et attendre.
