---
name: cross-repo-naming-decision-propagation
description: Décisions de naming/structure faites sur un repo (neo_ia 22 mai) doivent être propagées explicitement aux autres repos (ia_back). Pas de propagation automatique. Auditer cross-repo après chaque décision majeure.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

Pattern observé audit neo_ia → ia_back 22 mai 2026.

**Règle :** Après chaque renaming/restructuring d'un composant `.claude/` partagé conceptuellement, vérifier les autres repos.

**Why:** Les décisions vault sont vraies par défaut sur le repo où elles ont été prises. Les autres repos gardent l'ancien nom/structure → drift cross-repo. Exemples 22 mai :
- `cto-mindset` → `orchestrator-mindset` (renommé neo_ia, encore ancien nom ia_back jusqu'à audit)
- `outcomes-after-architect` → `outcomes-after-dev` (idem)
- Dédup `shared-learnings` ↔ `learn-from-mistakes` (fait neo_ia, à refaire ia_back)
- Kill TDD strict + suppression tdd-guard.py (fait neo_ia 21 mai, fait ia_back 21 mai, mais test-writer.md description pas alignée jusqu'au 22 mai)

**How to apply:**
- Après décision majeure : checklist cross-repo (`ia_back`, `neo_ia`, `lojii`, `neoteem-brain`)
- Si décision faite via skill-creator/agent-creator/claudemd-optimizer sur un repo → relancer sur les autres en mode "propagation"
- Garder une note vault `Knowledge/decisions/cross-repo-propagation.md` qui liste les décisions à propager (pas encore créée)
