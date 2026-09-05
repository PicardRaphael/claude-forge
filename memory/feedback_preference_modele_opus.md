---
name: preference-modele-opus
description: Ordre Opus (MAJ 5 sept. 2026) — défaut claude-opus-5 ; Fable 5.1 ne le remplace PAS (step-up mesuré, double prix) ; repli 4.8 (préférence validée) puis 4.6 ; jamais 4.7 (jugé moyen)
trigger: modele, opus, sonnet, haiku, fable, 4.8, 4.7, quel modele
metadata:
  type: feedback
---

Préférence modèle Opus de Raphael (29 mai 2026) : **4.8 en premier choix, 4.6 en repli, jamais 4.7** (« 4.7 j'ai jamais trop aimé », jugé moyen).

**Why:** Préférence qualitative vécue, pas juste « le plus récent ». 4.7 a été une release qu'il a trouvée décevante (cf aussi tokenizer 4.7 +35% tokens). 4.8 (sorti 28 mai 2026, `claude-opus-4-8`) corrige le tir.

**How to apply (mis à jour 27 juil. 2026, arbitrage Raphael)** : depuis le 24 juil., le défaut Opus est **`claude-opus-5`** (mapping forge `opus` = `claude-opus-5`, CLAUDE.md) — laisser tourner et surveiller les agents jugement sur Opus 5. Ordre de repli si problème/indisponibilité : `claude-opus-4-8` (préférence validée) → 4.6. **Jamais 4.7** (jugé moyen + exclu du fast mode depuis le 24 juil.). Cf [[Opus 5]] + [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] (vault).

**MAJ 5 sept. 2026 — l'arrivée de [[Fable 5.1]] ne change PAS cette préférence.** Fable 5.1 (1er sept., classe Mythos, $10/$50) est au-dessus d'Opus 5 en capacité, mais Anthropic recommande explicitement l'inverse d'un passage par défaut : « For most workloads, start with Claude Opus 5… Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall short. » Opus 5 reste donc le défaut forge ; Fable 5.1 est un step-up **mesuré**, au double du prix. Ordre de repli inchangé.
