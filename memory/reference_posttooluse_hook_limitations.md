---
name: posttooluse-hook-pas-tokens-api
description: Hook PostToolUse voit I/O outils, PAS tokens API Claude ni attribution skill/agent
metadata:
  type: reference
---

Un hook PostToolUse reçoit via stdin JSON : `session_id`, `tool_name`, `tool_input`, `tool_response`, `transcript_path`, `cwd`. Il NE VOIT PAS le contexte cumulé Claude ni la skill/agent invoquant l'outil. Conséquence : `(input_chars + output_chars) / 3.3` est un proxy I/O outils, jamais les tokens API Claude réels. Pour tokens API réels : Anthropic Console (clé API) ou `/context` (abonnement Claude Code).

**Why:** Phase 1 forge 28 mai — advisor a détecté ce blocker conceptuel avant que je code un "metrics-tracker" qui prétendrait mesurer les tokens. Raphaël a corrigé : abonnement Claude Code, donc Console pas pertinente, garder hook I/O seul comme MVP.
**How to apply:** Avant de proposer un hook qui "mesure tokens", clarifier : I/O outils OU tokens API ? Les deux sources sont disjointes. Pour attribution skill/agent depuis un hook : nécessite parser transcript via session_id (non trivial, souvent à drop).
