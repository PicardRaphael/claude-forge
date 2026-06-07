---
name: mcp-forge-brain-lifecycle-gotchas
description: 2 gotchas cycle de vie MCP forge-brain — restart = kill+NOUVELLE session (autostart au SessionStart only), et register_tools non testé si tests appellent BrainTools direct
metadata:
  type: reference
---

Deux gotchas empiriques du cycle de vie du serveur MCP forge-brain, découverts au Chantier 6-B (7 juin 2026, ajout des 4 outils `*_by_path`).

## 1. Recharger le code MCP = KILL + NOUVELLE session (jamais mid-session)

Après avoir modifié le code du serveur (`mcp-forge-brain/src/...`), les changements ne sont PAS visibles dans la session courante : le handshake MCP (liste des outils) est figé au SessionStart. Et `mcp-autostart.py` fait `if port_open(8091): exit(0)` — donc tant que l'ancien process tient le port 8091, **même une nouvelle session relance l'ANCIEN code**.

Séquence correcte : **`taskkill` le process Python qui tient le port 8091 → PUIS ouvrir une NOUVELLE session** (son SessionStart voit le port fermé → autostart lance le code à jour). Tuer mid-session ne relance rien (autostart ne tourne qu'au SessionStart). Oublier le kill = reconnexion silencieuse à l'ancien code → tout test "live" tourne contre des outils périmés = faux résultat déroutant.

**Conséquence pratique** : valider du nouveau code MCP via les outils live appartient à une session SUIVANTE, pas à celle qui code. C'est une frontière de session délibérée (Document & Clear).

## 2. La couche `register_tools` (wrappers `@_tool`) n'est PAS testée si les tests appellent `BrainTools` directement

Les tests forge appellent `tools.update_note(...)` sur l'instance `BrainTools` → les wrappers `@_tool` de `register_tools` (enregistrement FastMCP, validation/passage d'args, `log_call`) ne sont JAMAIS exécutés. Une faute dans un wrapper (ordre/nom d'args, oubli d'enregistrement) passe les tests verts et casse l'outil en prod.

**Fix, sans binder le port** (`register_tools(mcp, tools)` ne touche pas le port — seul `app.run()` dans `main()` le fait) :
- `asyncio.run(mcp._list_tools())` → liste d'objets `.name` : vérifier que les nouveaux outils sont enregistrés + les anciens préservés.
- `asyncio.run(mcp.call_tool("nom", {args}))` → `ToolResult`, lire `.structured_content["result"]` : exerce validation d'args + dispatch wrapper de bout en bout.

API FastMCP 2.x vérifiée empiriquement (Python 3.14, 7 juin) : `get_tools` n'existe pas ; `_list_tools`/`call_tool` sont des coroutines une fois le provider agrégé monté. Ne pas sonder `.fn`/`.func` (fragile, dérive entre versions) — passer par `call_tool` (API publique).

Foyer connexe vault : [[ajouter-source-donnees-mcp-forge-brain]] (section Tests — enrichie d'un renvoi à ce gotcha). Cf aussi [[gate-zero-diff-test-live-byte-exact]] (même esprit : tester la vraie couche d'exécution, pas une approximation).
