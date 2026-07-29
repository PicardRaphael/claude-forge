---
name: preference-modele-opus-4-8
description: Ordre Opus (MAJ 27 juil. 2026) — défaut claude-opus-5 (surveiller les agents jugement) ; repli 4.8 (préférence validée) puis 4.6 ; jamais 4.7 (jugé moyen)
trigger: modele, opus, sonnet, haiku, 4.8, 4.7, quel modele
metadata:
  type: feedback
---

Préférence modèle Opus de Raphael (29 mai 2026) : **4.8 en premier choix, 4.6 en repli, jamais 4.7** (« 4.7 j'ai jamais trop aimé », jugé moyen).

**Why:** Préférence qualitative vécue, pas juste « le plus récent ». 4.7 a été une release qu'il a trouvée décevante (cf aussi tokenizer 4.7 +35% tokens). 4.8 (sorti 28 mai 2026, `claude-opus-4-8`) corrige le tir.

**How to apply (mis à jour 27 juil. 2026, arbitrage Raphael)** : depuis le 24 juil., le défaut Opus est **`claude-opus-5`** (mapping forge `opus` = `claude-opus-5`, CLAUDE.md) — laisser tourner et surveiller les agents jugement sur Opus 5. Ordre de repli si problème/indisponibilité : `claude-opus-4-8` (préférence validée) → 4.6. **Jamais 4.7** (jugé moyen + exclu du fast mode depuis le 24 juil.). Cf [[Opus 5]] + [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] (vault).
