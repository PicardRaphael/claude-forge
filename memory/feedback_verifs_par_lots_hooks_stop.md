---
name: verifs-par-lots-hooks-stop
description: Agents dev = vérifs par LOTS (jamais après chaque fichier, jamais de lint manuel si hook PostToolUse formate) ; checks lourds (tsc, tests) = hook Stop, JAMAIS PostToolUse ; spawn interpréteur additif sur matchers larges
metadata:
  type: feedback
---

US1 neoteem-back-ts (10 juin 2026) : ~1h30 au lieu de ~30 min — le dev relançait lint+typecheck+tests après CHAQUE fichier, lançait biome à la main (le hook PostToolUse formatait déjà), et tsc tournait en PostToolUse à chaque Write.

**Why:** chaque vérif redondante = wall-clock + tokens ; « 50 edits × 10-30s de tsc = 25 min perdues » (état de l'art hooks 2026, convergent avec Boris : PostToolUse = format rapide only, vérification lourde en fin de tour).

**How to apply:** à toute création d'agent dev / audit de repo : (1) graver « vérifs par LOTS, tests ciblés package, jamais relancer sans nouveau changement, pas de lint manuel si hook » dans l'agent ; (2) checks lourds → hook **Stop** (`stop_hook_active` guard, `decision:block` si erreurs, inclure les fichiers untracked via `git ls-files --others`) ; (3) hooks Python : interpréteur direct ~250 ms vs `uv run`/`py` ~450-640 ms, coûts ADDITIFS sur matchers larges, `timeout` partout. Canoniques : [[comment-creer-hook]] + [[comment-creer-agent]] AJOUTs 10 juin.
