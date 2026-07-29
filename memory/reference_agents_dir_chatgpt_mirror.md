---
name: agents-dir-chatgpt-mirror
description: .agents/ et AGENTS.md (racine forge) = miroir pour ChatGPT/Codex géré par Raphael — ne jamais y écrire, ne jamais les flagger comme drift
trigger: AGENTS.md, .agents, chatgpt, codex, miroir, drift
metadata:
  type: reference
---

`.agents/skills/` et `AGENTS.md` à la racine de claude-forge sont des **copies destinées à ChatGPT/Codex**, gérées par Raphael (décision explicite du 27 juillet 2026, lors de l'audit de drift vault).

**Why :** ces fichiers ont l'air d'être des miroirs périmés de `.claude/skills/` et `CLAUDE.md` (contenu daté, encodage mojibake) — un audit naïf les flagge comme drift et propose de les supprimer/resynchroniser. Raphael a tranché : « fait rien sur tout ce qui est .agents, c'est chatgpt ».

**How to apply :** ne JAMAIS y écrire, les modifier, les supprimer ni les proposer en fix. Les exclure de tout audit de drift/pivot-check (exclusion codée dans `.claude/skills/pivot-check/SKILL.md` étape 3). Si une divergence avec `.claude/` semble poser un problème réel, la SIGNALER à Raphael sans agir. Cf [[feedback_ecart_consigne_chiffree_surfacer]].
