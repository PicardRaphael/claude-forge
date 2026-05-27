---
name: cross-repo-write-main-session-only
description: "Session principale forge a write sur autres repos (ia_back, neo_ia, lojii) via Bash/Edit direct. Sub-agents bloqués cross-repo — NE PAS déléguer fixes cross-repo"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Découvert 2026-05-22 lors de la Vague 1 fixes ia_back depuis forge :

**Comportement vérifié** :
- ✅ Session principale forge → Edit/Bash sur `C:\Users\raphael.picard_neote\Documents\neot-v2\ia_back\` = OK
- ❌ Sub-agents lancés depuis forge (general-purpose, hook-creator, claudemd-optimizer) → permissions cross-repo bloquées
- ❌ Même avec `CLAUDE_AGENT=agent-creator`, le bypass ne traverse pas la frontière repo

**Règle Jarvis** :
- Pour fix cross-repo (forge → ia_back/neo_ia/lojii/neoteem-brain), Edit/Bash **direct depuis session principale**, JAMAIS via sub-agent
- Sub-agents OK pour : tasks intra-forge, recherche read-only cross-repo (Read fonctionne en lecture)
- Pour lots > 5 fichiers cross-repo, exécuter séquentiellement depuis session principale plutôt que paralléliser via sub-agents bloqués

**Why** : J'ai lancé 4 sub-agents en parallèle pour Vague 1 ia_back, 3/4 ont échoué sur permission cross-repo (gain : ~0). Réexécution directe en session principale : 5 fixes en 2 minutes.

**How to apply** : Quand l'utilisateur dit "fix ce repo X depuis forge", check immédiatement si fix = intra-forge ou cross-repo. Si cross-repo → édits directs, pas sub-agents (sauf read pure).

Related : [[subagent-permissions-limitation]], [[feedback_audit_repo_method]].
