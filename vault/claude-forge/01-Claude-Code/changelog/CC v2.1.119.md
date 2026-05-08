---
titre: "Claude Code v2.1.119"
resume: "Auto Mode, hooks MCP direct, custom themes, /usage, fix Opus 4.7 context 1M"
aliases:
  - "CC 2.1.119"
  - "v2.1.119"
  - "auto mode release"
  - "hooks MCP"
  - "custom themes CC"
  - "claude code auto mode"
domaine: claude-code
type: changelog
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

## Date : 23 avril 2026

## Nouveautés majeures

### Auto Mode
- Shift+Tab cycle : Ask → Plan → Auto
- Auto-approve via classifier ML — plus besoin de babysitter
- Disponible Opus 4.7 pour Max, Teams, Enterprise
- Combiné avec worktrees = parallélisme massif sans friction

### Hooks MCP direct
- Nouveau type de handler : `type: "mcp_tool"`
- Permet aux hooks d'invoquer des outils MCP directement
- Format : `{"type": "mcp_tool", "server": "mon-server", "tool": "mon-outil", "input": {}}`

### Custom Themes
- Créer/switcher via `/theme`
- Fichiers JSON dans `~/.claude/themes/`
- Plugins peuvent shipper des thèmes via `themes/`

### /usage
- Fusionne `/cost` et `/stats` — les deux restent comme alias

## Améliorations

### Config
- `/config` persiste dans `~/.claude/settings.json` avec precedence projet/local/policy
- "Show turn duration" dans `/config`
- `--console` flag sur `claude auth login` pour Anthropic Console (API billing)

### Performance
- Fix Opus 4.7 context : calcul corrigé 200K → 1M natif (plus de faux auto-compact)
- `/fork` optimisé : pointeur au lieu de copie complète
- ~80MB RAM en moins au startup sur repos 250k+ fichiers
- `/resume` 67% plus rapide sur sessions 40MB+

### Plugins
- `install` sur plugin existant → installe dépendances manquantes
- `blockedMarketplaces` et `strictKnownMarketplaces` enforcées

### Sécurité / OS
- `DISABLE_UPDATES` env var — bloque tout update y compris manuel
- WSL hérite managed settings Windows via `wslInheritsWindowsSettings`
- Fix credential save crash Linux/Windows
- Fix PowerShell permission checks (trailing &, -ErrorAction Break, TOCTOU)

### Vim
- Visual mode (v) et visual-line mode (V) avec opérateurs

## Bug fixes notables
- Fix `/login` sans effet avec `CLAUDE_CODE_OAUTH_TOKEN`
- Fix Bedrock inference-profile 400 avec Opus 4.7 thinking disabled
- Fix nested CLAUDE.md re-injectés des dizaines de fois en longues sessions

## Liens

- Precedent : [[CC v2.1.116]]
- Suivant : [[CC v2.1.120]]
- [[Auto Mode]]
- [[Opus 4.7]]
- [[MOC-Claude-Code]]
