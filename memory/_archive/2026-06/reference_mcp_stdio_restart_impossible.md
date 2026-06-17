---
name: mcp-stdio-restart-in-session-impossible
description: MCP stdio servers ne peuvent PAS être redémarrés en cours de session pour exposer de nouveaux tools — le client Claude Code spawn le serveur au démarrage via stdin/stdout JSON-RPC
metadata: 
  node_type: memory
  type: reference
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Découvert 2026-05-22 en tentant de redémarrer le MCP forge-brain après ajout de `update_note` + `insert_section` :

**Comportement vérifié** :
- MCP stdio servers (vs MCP HTTP) = process child du client Claude Code
- Communication via stdin/stdout JSON-RPC, parent = Claude Code
- Lancer le serveur via Bash externe ne marche PAS : pas de client connecté → exit 1 / process zombie
- Tuer le process ne suffit pas : Claude Code ne re-spawn pas automatiquement
- `/mcp` rechargerait peut-être (non testé empiriquement)

**Conséquence** : si je modifie le code d'un MCP stdio (Python, TypeScript, etc.), les nouveaux tools NE seront disponibles QU'À la prochaine session Claude Code (après restart complet du client).

**Workaround pour CETTE session** :
- Continuer avec les outils existants (Edit direct sur fichiers vault, Bash, etc.)
- Commit le code du MCP — il sera utilisable session suivante

**Pour MCP HTTP/SSE** : redémarrage possible côté serveur sans toucher au client. Pas applicable au MCP forge-brain (stdio).

**How to apply** :
- Avant de promettre "je vais ajouter un outil au MCP et continuer" → vérifier si le MCP est stdio. Si oui = nouveaux outils dispo PROCHAINE session, pas celle-ci
- Commit le code MCP de toute façon (utilisable session suivante)
- Pour la session courante, basculer sur Edit/Bash direct
- Documenter dans le commit message "nouveaux outils dispo prochaine session"

Related : [[reference_neo_brain_pattern]], [[feedback_use_brain_skills]], [[feedback_delegate_guard_env_var_blocked]] (autre cas de limitation harness en cours de session).
