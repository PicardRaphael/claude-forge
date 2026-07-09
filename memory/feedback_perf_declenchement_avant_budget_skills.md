---
name: perf-declenchement-avant-budget-skills
description: "Arbitrage corpus skills : performance de déclenchement > budget tokens"
metadata:
  type: feedback
---

Pour tout arbitrage sur le corpus skills forge (fusion, kill, raccourcissement, ajout), la performance de déclenchement prime sur le budget tokens : une optimisation budget n'est acceptable que si le routing s'améliore ou reste intact. Les collisions de descriptions sont un signal PRO-fusion (perf-positive) ; une fusion budget-only est refusée.

**Why:** Consigne explicite Raphael (9 juil. 2026, chantier forge-review fusions) : « oui budget mais pas au détriment des performances, je veux surtout que les skills soient parfaitement call ». A requalifié 2 fusions du plan (F4 python-script-refactor-masse, F5 cc-prompt-ref) en KEEP.

**How to apply:** Avant de proposer fusion/kill/trim de skills (forge-review, skill-evolve, doctor) : classer chaque item perf-positive / perf-neutre / perf-négative sur le déclenchement. Les perf-négatives ne passent que sur décision explicite de Raphael. Cf [[critique-2026-07-09-fusions-skills-forge]].
