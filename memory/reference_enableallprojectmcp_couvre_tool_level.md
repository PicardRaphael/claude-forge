---
name: enableallprojectmcp-couvre-tool-level
description: enableAllProjectMcpServers true + serveur dans .mcp.json auto-approuve les outils MCP au niveau TOOL sans prompt. Lister mcp__server__tool individuellement dans permissions.allow est redondant. Vérifié empiriquement 27 mai.
metadata:
  type: reference
---

`"enableAllProjectMcpServers": true` (dans settings.local.json ou settings.json) + le serveur déclaré dans `.mcp.json` + listé dans `enabledMcpjsonServers` = les outils du serveur sont auto-approuvés **au niveau tool, sans prompt de permission**. Lister chaque `mcp__forge-brain__read_note`, `mcp__forge-brain__list_notes`... dans `permissions.allow` est alors **redondant** — l'appel passe même si l'entrée est absente du allow.

**Vérifié empiriquement (27 mai 2026, nettoyage settings.local.json forge)** : retiré `mcp__forge-brain__list_notes` du allow → appel `list_notes` réussi **sans prompt**. Idem `vault_stats` (jamais dans le allow, appel OK sans prompt). Couverture sans-prompt confirmée.

**Nuance observée le même jour** : après un appel `search_brain`, le harness a **ré-ajouté** `mcp__forge-brain__search_brain` au allow automatiquement (le fichier est repassé de 11→12 entrées). Donc : l'appel ne prompte PAS (couverture OK), mais le harness peut re-persister l'entrée tool dans le allow lors d'un appel. Comportement non uniforme observé (list_notes/vault_stats non ré-ajoutés, search_brain ré-ajouté) — timing watcher probable. Conséquence pratique : supprimer les entrées MCP du allow réduit le bruit à l'instant T, mais certaines peuvent repousser au fil de l'usage. Ce n'est pas une régression (aucun prompt), juste une re-sédimentation cosmétique à re-nettoyer périodiquement.

**How to apply :**
- Si `enableAllProjectMcpServers: true` est présent → ne PAS lister les `mcp__server__tool` dans `permissions.allow` (redondant, bruit).
- Distinct de [[comment-creer-skill]] : celui-là porte sur `tools:`/`allowed-tools:` du FRONTMATTER agent/skill (donner accès à un sous-agent). Ici c'est `permissions.allow` des settings (éviter le prompt en session principale). Deux mécanismes, deux fichiers.
- Caveat : si `enableAllProjectMcpServers` est un jour retiré, le prompt par tool réapparaît. Le flag est le porteur de la couverture, pas le allow.

Lié à [[brief-premisse-fausse-verifier-avant-executer]] (le test empirique a tranché un ARBITRAGE plutôt qu'une affirmation de couverture non vérifiée).
