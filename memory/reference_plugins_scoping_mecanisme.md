---
name: plugins-scoping-mecanisme
description: Plugins Claude Code se scopent via "scope" dans installed_plugins.json (user/project/local) + activation via enabledPlugins dans settings.json correspondant. Marketplace declaration + Plugin:* permissions auto-charge sans enabledPlugins.
metadata:
  type: reference
---

**Mecanisme empirique 28 mai 2026** — audit context tokens Step 6.

## 3 lieux de configuration plugins

1. **`~/.claude/plugins/installed_plugins.json`** : registry des plugins installes.
   - Chaque plugin a `"scope": "user" | "project" | "local"`
   - Si `scope=project|local`, `"projectPath"` est specifie (ex: `C:\...\neot-v2\neo_ia`)
   - `scope=user` → potentiellement disponible partout selon enabledPlugins
   - `scope=project` → disponible UNIQUEMENT dans le repo `projectPath`

2. **`~/.claude/settings.json` `enabledPlugins`** : whitelist user-scope (charge dans toutes sessions sauf override repo).

3. **`<repo>/.claude/settings.json` `enabledPlugins`** : whitelist project-scope (charge dans ce repo specifiquement).

## Marketplace auto-discovery (gotcha)

Un plugin **declared dans `extraKnownMarketplaces`** (settings.json L75-94 forge) **+** permission `Plugin:*` (allow L27) **peut etre auto-charge SANS etre dans enabledPlugins**. Verifie empiriquement sur `obsidian@obsidian-skills` : pas dans enabledPlugins user-scope, pas dans aucun repo, et pourtant ses 5 skills (obsidian-markdown, defuddle, etc.) apparaissent dans le system-reminder de chaque session forge.

Pour desactiver completement un plugin auto-charge via marketplace : retirer la declaration du marketplace OU retirer `Plugin:*` des permissions.

## Tokens cost

Chaque plugin enabled charge les `name:` + `description:` de TOUTES ses skills au demarrage de session du repo concerne. Mesure 28 mai : 8 plugins enabled user-scope = ~1 690 tokens / session forge.

Reduction empirique Step 7 : passe de 10 plugins → 4 plugins enabled user-scope = -1 098 tokens / session.

## Methode audit usage reel

Pour chaque plugin, grep des skills exposees dans `.claude/` de chaque repo :
```powershell
Get-ChildItem <repo>\.claude -Recurse -File -Include '*.md','*.json' |
  Select-String -Pattern '<skill-name>' -SimpleMatch
```

Decision matrix :
- 0 ref dans tous repos → DESINSTALLER global
- N refs dans 1-2 repos → SCOPE project sur ces repos
- N refs dans 3-4 repos → GARDER GLOBAL

Lien : [[skills-metadata-tokens-load]] (cas general skills frontmatter charges au demarrage).
