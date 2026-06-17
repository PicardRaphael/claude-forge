---
name: posttooluse-hook-pas-tokens-api
description: Hook PostToolUse voit I/O outils, PAS tokens API Claude ni attribution skill/agent
metadata:
  type: reference
---

Un hook PostToolUse reçoit via stdin JSON : `session_id`, `tool_name`, `tool_input`, `tool_response`, `transcript_path`, `cwd`. Il NE VOIT PAS le contexte cumulé Claude ni la skill/agent invoquant l'outil. Conséquence : `(input_chars + output_chars) / 3.3` est un proxy I/O outils, jamais les tokens API Claude réels. Pour tokens API réels : Anthropic Console (clé API) ou `/context` (abonnement Claude Code).

**Why:** un hook I/O présenté comme « mesure de tokens » ment sur son mécanisme. Un tel hook (proxy I/O sur tous les outils) a été retiré de forge : overhead ~450 ms/outil pour une donnée jamais agrégée ni consommée. La limite technique reste vraie indépendamment de ce composant.
**How to apply:** Avant de proposer un hook qui "mesure tokens", clarifier : I/O outils OU tokens API ? Les deux sources sont disjointes. Pour attribution skill/agent depuis un hook : nécessite parser transcript via session_id (non trivial, souvent à drop).
