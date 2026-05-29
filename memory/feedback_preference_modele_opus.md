---
name: preference-modele-opus-4-8
description: Raphael préfère Opus 4.8 ; à défaut 4.6 ; jamais 4.7 (jugé moyen)
metadata:
  type: feedback
---

Préférence modèle Opus de Raphael (29 mai 2026) : **4.8 en premier choix, 4.6 en repli, jamais 4.7** (« 4.7 j'ai jamais trop aimé », jugé moyen).

**Why:** Préférence qualitative vécue, pas juste « le plus récent ». 4.7 a été une release qu'il a trouvée décevante (cf aussi tokenizer 4.7 +35% tokens). 4.8 (sorti 28 mai 2026, `claude-opus-4-8`) corrige le tir.

**How to apply:** Quand on choisit/recommande un modèle Opus (frontmatter agent, `/model`, fast mode, conseil) → défaut `claude-opus-4-8`. Si 4.8 indisponible (rate limit, env) → basculer sur 4.6, pas 4.7. Le mapping doctrine forge `opus` = `claude-opus-4-8` (CLAUDE.md L73) est cohérent avec cette préférence. Cf [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] (vault).
