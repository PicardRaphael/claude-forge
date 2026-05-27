---
name: plugin-cache-refresh-bug
description: Bug connu — le cache plugin Claude Code ne se rafraichit pas automatiquement. Workaround = bumper version dans plugin.json a chaque mise a jour.
type: reference
originSessionId: a0d051cb-3e6f-429d-9908-b2cfe3295ea9
---
## Bug cache plugin Claude Code

Le cache local (`~/.claude/plugins/cache/`) n'est PAS invalide quand le plugin source est mis a jour (GitHub #17361, #14061, #38271). Le `autoUpdate` du marketplace fait un `git pull` mais le cache n'est pas rafraichi.

**Workaround fiable** : bumper la `version` dans `plugin.json` a chaque mise a jour. Le cache est indexe par version — nouvelle version = nouveau dossier = pas de stale cache.

**Commande de secours** : `/reload-plugins` ou `rm -rf ~/.claude/plugins/cache/neoteem-brain/`

**Pas de difference** entre source `github` et source `git-url` (Bitbucket) — meme comportement de cache.

**Cowork Desktop** (marketplace GitHub) : resync auto 30 min apres merge. Systeme different du CLI.

**Cleanup auto** : anciens dossiers de version marques "orphaned" et supprimes apres 7 jours.

**How to apply** : Quand on met a jour le plugin neoteem-brain, TOUJOURS bumper la version dans `plugin/.claude-plugin/plugin.json` avant de push. Informer l'equipe si maj importante.
