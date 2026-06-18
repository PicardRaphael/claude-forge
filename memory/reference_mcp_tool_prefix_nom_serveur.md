---
name: mcp-tool-prefix-nom-serveur
description: Le préfixe d'un tool MCP dans allowed-tools = le NOM du serveur dans .mcp.json (ou le connector), pas le nom d'affichage. Doublon d'URL = un serveur masqué.
metadata:
  type: reference
---

Quand on câble un outil MCP dans `allowed-tools` (skill) ou `tools:` (agent), le préfixe est `mcp__<nom-serveur>__*` où `<nom-serveur>` = la **clé exacte du serveur dans `.mcp.json`** (ou le nom interne du connector claude.ai), JAMAIS le nom d'affichage humain.

**Cas vécu 18 juin 2026 (ia-workbench)** : `.mcp.json` déclarait `"neobrain": {url: ...}` → le tool est `mcp__neobrain__*`. J'avais écrit `mcp__claude_ai_MCP_NeoBrain_-_NEOTEEM__*` (le nom d'AFFICHAGE du connector claude.ai) → tools jamais résolus. Le connector claude.ai a son propre préfixe `mcp__claude_ai_MCP_NeoBrain_-_NEOTEEM__*` ; le serveur `.mcp.json` a `mcp__neobrain__*`. **Deux serveurs distincts, deux préfixes, MÊME URL.**

**Corollaire — doublon d'URL = masquage** : deux serveurs MCP sur la même URL (`https://mcp-brain.neoteem.fr/mcp`) → Claude Code en masque un (« hidden — same URL as ... »). C'est la « MCP deduplication claude.ai connectors » (changelog CC avril 2026). Symptôme : un serveur configuré mais ses tools absents. Fix : retirer le doublon (garder soit le `.mcp.json` local, soit le connector claude.ai), aligner le préfixe sur celui qui reste.

**Réflexe avant de câbler un MCP dans une skill/agent** : vérifier le NOM réel du serveur (`claude mcp list` ou la clé du `.mcp.json`), pas supposer depuis le nom d'affichage. Vérification empirique seulement en session fraîche (les MCP ne se rechargent pas en cours de session).

Lié : [[mcp-wildcard-syntax-officielle]] (wildcard `mcp__server__*` suffit, jamais lister les tools) · [[enableallprojectmcp-couvre-tool-level]].
