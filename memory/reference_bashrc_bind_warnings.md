---
name: bashrc-bind-warnings-non-interactive
description: "Warnings \"bind: line editing not enabled\" dans sorties Bash Claude Code = bind readline dans .bashrc sans garde interactive"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Quand toutes les commandes Bash exécutées par Claude Code (Git Bash sous Windows) commencent par 3+ warnings du type :

```
/c/Users/<user>/.bashrc: line N: bind: warning: line editing not enabled
```

Cause : `~/.bashrc` contient des commandes `bind '...'` (raccourcis readline) hors garde interactive. Bash one-shot non-interactif → readline désactivé → warnings sur chaque appel `bind`.

**Fix canonique** : wrapper avec `$-` qui contient les flags du shell (`i` = interactif) :

```bash
if [[ $- == *i* ]]; then
    bind '"\e[A": history-search-backward'
    bind '"\e[B": history-search-forward'
fi
```

Ou inline : `[[ $- == *i* ]] && bind '...'`

**Pourquoi c'est important** : ces warnings polluent stdout/stderr de chaque Bash tool call, gaspillent du contexte, et peuvent masquer des erreurs réelles. Vu chez Raphael 2026-05-22 (lignes 20-22 du `.bashrc`).

Related : [[python-path-windows-hooks]], [[python-windows-cross-machine]] — autres gotchas environnement Windows.
