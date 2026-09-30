---
name: preference-modele-opus
description: Ordre Opus (MAJ 25 sept. 2026) — défaut = alias opus → claude-opus-5-5 (effort API défaut medium ; forge pose medium exécution / high jugement, zéro sonnet depuis le 30 sept.) ; Fable 5.1 ne le remplace PAS (step-up mesuré) ; repli Opus 5 puis 4.8 ; jamais 4.7 (jugé moyen)
trigger: modele, opus, sonnet, haiku, fable, 4.8, 4.7, quel modele
metadata:
  type: feedback
---

Préférence modèle Opus de Raphael (29 mai 2026) : **4.8 en premier choix, 4.6 en repli, jamais 4.7** (« 4.7 j'ai jamais trop aimé », jugé moyen).

**Why:** Préférence qualitative vécue, pas juste « le plus récent ». 4.7 a été une release qu'il a trouvée décevante (cf aussi tokenizer 4.7 +35% tokens). 4.8 (sorti 28 mai 2026, `claude-opus-4-8`) corrige le tir.

**How to apply (mis à jour 25 sept. 2026)** : forge suit l'alias `opus` — c'est l'arbitrage Raphael du 27 juil. (« laisser tourner et surveiller » plutôt qu'épingler). Depuis CC v2.1.280 (22 sept. 2026), cet alias résout vers **`claude-opus-5-5`** ($4/$20, point de départ officiel Anthropic « for most workloads »). ⚠️ Son effort API par défaut est **`medium`** : un appel sans `effort:` tourne un cran plus bas qu'avant ; les frontmatters forge posent l'effort explicitement — `medium` pour l'exécution, `high` pour le jugement, et plus aucun `sonnet` depuis le 30 sept. 2026 (cf [[feedback_allocation_modele_effort]] + [[raisonnement-2026-09-30-zero-sonnet]]). Ordre de repli si problème/indisponibilité : `claude-opus-5` (legacy, toujours disponible) → `claude-opus-4-8` (préférence validée) → 4.6. **Jamais 4.7** (jugé moyen + exclu du fast mode depuis le 24 juil.). Cf [[Opus 5.5]] + [[Opus 5]] (vault).

**Fable 5.1 ne change PAS cette préférence (5 sept., reconfirmé 25 sept. 2026).** Fable 5.1 (classe Mythos, $10/$50) est au-dessus en capacité, mais Anthropic recommande l'inverse d'un passage par défaut, verbatim au 25 sept. : « start with Claude Opus 5.5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short. » Fable 5.1 reste un step-up **mesuré**, à 2,5× le prix d'Opus 5.5.
