---
name: multiedit-matcher-blind-spot-hooks
description: "Les hooks PreToolUse Write|Edit sans MultiEdit créent un trou architectural. MultiEdit échappe à tous les guards. TOUJOURS matcher `Write|Edit|MultiEdit` partout, sinon bypass facile."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

Découvert sur neo_ia + ia_back audit 22 mai 2026.

**Règle :** Tous les hooks PreToolUse qui matchent `Write|Edit` DOIVENT aussi matcher `MultiEdit`.

**Why:** MultiEdit est un outil séparé du point de vue matcher CC. Un hook architect-guard / dispatch-guard / repo-scope-guard / core-imports-guard qui matche seulement Write|Edit laisse passer toute modification faite via MultiEdit. Trou silencieux exploitable par accident (Claude utilise MultiEdit naturellement sur batch d'edits).

**How to apply:**
- Auditer settings.json : grep `"Write|Edit"` doit être ZÉRO occurrence (toujours `Write|Edit|MultiEdit`)
- Vérifier que le code .py/.ts du hook traite déjà MultiEdit (`tool_input.get("file_path")` ou `tool_input.get("edits")[*].file_path`)
- ia_back avait 4 guards critiques touchés, neo_ia 1 (architect-guard)
- Quand on crée un nouveau hook → matcher full triplet par défaut, jamais juste Write|Edit
