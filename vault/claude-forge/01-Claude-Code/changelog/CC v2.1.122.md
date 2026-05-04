---
titre: "Claude Code v2.1.122"
resume: "Bedrock service tier, /resume PR URL, MCP dedup, OTEL numerique, bug fixes"
aliases:
  - "CC 2.1.122"
  - "v2.1.122"
domaine: claude-code
type: changelog
derniere-maj: 2026-04-29
auteur: claude
sources:
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Date : 28 avril 2026

## Nouveautes

### Bedrock Service Tier
- `ANTHROPIC_BEDROCK_SERVICE_TIER` env var
- Valeurs : `default`, `flex`, `priority`
- Envoye comme header `X-Amzn-Bedrock-Service-Tier`

### /resume trouve les sessions par PR URL
- Coller une URL de PR dans la recherche `/resume`
- Trouve la session qui a cree ce PR
- Supporte GitHub, GitHub Enterprise, GitLab, Bitbucket

### MCP deduplication
- `/mcp` montre les claude.ai connectors caches par un serveur manuellement ajoute avec la meme URL
- Hint pour supprimer le doublon

## Ameliorations

- Message clarifie dans `/mcp` quand serveur reste non autorise apres sign-in browser
- OpenTelemetry : attributs numeriques sur `api_request`/`api_error` en nombres (plus strings)
- OpenTelemetry : event `claude_code.at_mention` pour resolution `@`-mention
- Voice mode : keybindings lies a Caps Lock montrent erreur (terminals ne delivrent pas Caps Lock)

## Bug fixes

- Fix `/branch` produisant forks qui echouent avec "tool_use ids without tool_result blocks" quand source contient timelines rewound
- Fix `/model` ne montrant pas l'option Effort pour Bedrock inference profile ARNs
- Fix Vertex AI / Bedrock erreur "output_config: Extra inputs are not permitted" sur queries structured-output
- Fix Vertex AI `count_tokens` 400 errors derriere proxy gateways
- Fix `spinnerTipsOverride.excludeDefault` ne supprimant pas tips time-based
- Fix ToolSearch ratant outils MCP connectes apres session start en mode nonblocking
- Fix `!exit` / `!quit` en bash mode terminant le CLI au lieu d'executer comme commande shell
- Fix images redimensionnees a 2576px au lieu du max correct 2000px pour nouveaux modeles
- Fix remote control session idle status redraw 2x/sec (flood tmux -CC)
- Fix messages assistant blank dans certaines sessions (stale view preference)
- Fix entree hooks malformee dans settings.json n'invalidant plus tout le fichier

## Liens

- [[CC v2.1.121]]
- [[CC v2.1.123]]
