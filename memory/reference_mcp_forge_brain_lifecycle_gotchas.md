---
name: mcp-forge-brain-lifecycle-gotchas
description: 3 gotchas cycle de vie MCP forge-brain — restart = kill+NOUVELLE session (élévation parfois requise), register_tools non testé en direct, et changement de PARSER exige delete DB (le watcher incrémental ne reparse pas l'existant)
metadata:
  type: reference
---

Deux gotchas empiriques du cycle de vie du serveur MCP forge-brain, découverts au Chantier 6-B (7 juin 2026, ajout des 4 outils `*_by_path`).

## 1. Recharger le code MCP = KILL + NOUVELLE session (jamais mid-session)

Après avoir modifié le code du serveur (`mcp-forge-brain/src/...`), les changements ne sont PAS visibles dans la session courante : le handshake MCP (liste des outils) est figé au SessionStart. Et `mcp-autostart.py` fait `if port_open(8091): exit(0)` — donc tant que l'ancien process tient le port 8091, **même une nouvelle session relance l'ANCIEN code**.

Séquence correcte : **`taskkill` le process Python qui tient le port 8091 → PUIS ouvrir une NOUVELLE session** (son SessionStart voit le port fermé → autostart lance le code à jour). Tuer mid-session ne relance rien (autostart ne tourne qu'au SessionStart). Oublier le kill = reconnexion silencieuse à l'ancien code → tout test "live" tourne contre des outils périmés = faux résultat déroutant.

**Conséquence pratique** : valider du nouveau code MCP via les outils live appartient à une session SUIVANTE, pas à celle qui code. C'est une frontière de session délibérée (Document & Clear).

**Wrinkle élévation (14 juin 2026)** : le `taskkill /PID <pid> /F` peut échouer « Accès refusé » si le process tenant le port a été lancé par une session à privilège différent (ex. session précédente élevée). L'agent non élevé ne peut alors PAS débloquer seul → le kill revient à l'utilisateur (PowerShell admin ou Gestionnaire des tâches). Symptôme combiné observé : outils `*_by_path` absents de la session **et** `taskkill` refusé = serveur périmé qui tient 8091 + non tuable sans élévation. Une fois tué par l'utilisateur + nouvelle session, l'autostart relance le code à jour (vérifié : les 4 `*_by_path` sont alors exposés).

## 2. La couche `register_tools` (wrappers `@_tool`) n'est PAS testée si les tests appellent `BrainTools` directement

Les tests forge appellent `tools.update_note(...)` sur l'instance `BrainTools` → les wrappers `@_tool` de `register_tools` (enregistrement FastMCP, validation/passage d'args, `log_call`) ne sont JAMAIS exécutés. Une faute dans un wrapper (ordre/nom d'args, oubli d'enregistrement) passe les tests verts et casse l'outil en prod.

**Fix, sans binder le port** (`register_tools(mcp, tools)` ne touche pas le port — seul `app.run()` dans `main()` le fait) :
- `asyncio.run(mcp._list_tools())` → liste d'objets `.name` : vérifier que les nouveaux outils sont enregistrés + les anciens préservés.
- `asyncio.run(mcp.call_tool("nom", {args}))` → `ToolResult`, lire `.structured_content["result"]` : exerce validation d'args + dispatch wrapper de bout en bout.

API FastMCP 2.x vérifiée empiriquement (Python 3.14, 7 juin) : `get_tools` n'existe pas ; `_list_tools`/`call_tool` sont des coroutines une fois le provider agrégé monté. Ne pas sonder `.fn`/`.func` (fragile, dérive entre versions) — passer par `call_tool` (API publique).

Foyer connexe vault : [[ajouter-source-donnees-mcp-forge-brain]] (section Tests — enrichie d'un renvoi à ce gotcha). Cf aussi [[gate-zero-diff-test-live-byte-exact]] (même esprit : tester la vraie couche d'exécution, pas une approximation).

## 3. Changement du PARSER (indexer) = supprimer la DB pour un reparse complet (le watcher incrémental ne suffit PAS)

`VaultWatcher.scan()` est incrémental : il ne reparse une note que si son `mtime`/hash a changé. Donc quand on modifie le CODE de parsing (`indexer.py` — ex. ajout de `_strip_code` pour ignorer les wikilinks dans les code spans, 14 juin 2026), les notes existantes inchangées **gardent leurs données parsées à l'ancienne façon**, même après kill + nouvelle session. Le nouveau parser ne s'applique qu'aux notes futures ou modifiées.

**Fix : supprimer la DB pour forcer un rebuild complet.** `forge-brain.db` est un index 100 % reconstructible depuis les `.md` (la vérité = les notes). Séquence : kill serveur (port 8091, élévation parfois requise — cf gotcha #1) → `Remove-Item mcp-forge-brain/forge-brain.db*` (le `.db` + `-wal` + `-shm`) → NOUVELLE session → `create_app` voit la DB vide → `watcher.scan()` reparse TOUT avec le nouveau code. Preuve 14 juin 2026 : après ce rebuild, `broken_wikilinks` est passé de 88 → 75 (les ~13 faux positifs `[[X]]`/`[[stem]]` en code spans ont disparu — sans rebuild, le compte n'aurait pas bougé).

Distinction nette : changement de NOTE → watcher suffit (≤ 30 s) ; changement de CODE serveur (nouveaux outils) → kill + nouvelle session (gotcha #1) ; changement de PARSER → **delete DB en plus** (ce gotcha #3, car les données déjà parsées ne se rafraîchissent pas seules).
