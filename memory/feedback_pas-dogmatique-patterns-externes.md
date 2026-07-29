---
name: pas-dogmatique-patterns-externes
description: "Adapter un pattern externe (Karpathy, etc.) à forge, jamais l'appliquer par mimétisme"
trigger: pattern, karpathy, externe, appliquer, mimetisme
metadata:
  type: feedback
---

Ne pas appliquer un pattern externe (Karpathy LLM Wiki, méthode d'un créateur, framework à la mode) par mimétisme. Garder ce qui sert la boucle agent forge, jeter le décoratif, proposer mieux si on voit mieux. Le vault est agent-first (cf [[decision-vault-agent-first]]).

**Why:** Raphael, 27 juin 2026 — « pattern Karpathy ok mais on peut mieux faire, fais quelque chose qui nous ressemble ». Karpathy a été l'échafaudage, pas la cible.
**How to apply:** Face à un pattern de référence externe, croiser avec l'usage réel forge (`usage_stats`, qui consomme quoi) avant d'adopter. Lié à [[jarvis-innovator]] et [[never-pure-executor]].
