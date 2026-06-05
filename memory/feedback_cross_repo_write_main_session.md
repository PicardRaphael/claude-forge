---
name: cross-repo-write-main-session-only
description: "Session principale forge a write sur autres repos (ia_back, neo_ia, lojii) via Bash/Edit direct. Sub-agents bloqués cross-repo — NE PAS déléguer fixes cross-repo"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Cf [[comment-creer-agent]] (doctrine : `permissions.allow` non hérité par les sub-agents — la frontière repo n'est pas traversée, même avec `CLAUDE_AGENT`). Voir aussi [[reference_subagent_permissions]].

**Règle empirique** : fix cross-repo (forge → ia_back/neo_ia/lojii/neoteem-brain) = Edit/Bash direct depuis la session principale, JAMAIS via sub-agent. Sub-agents OK pour tasks intra-forge et recherche read-only cross-repo (Read fonctionne en lecture). Lots > 5 fichiers cross-repo : séquentiel depuis session principale.

**Cas empirique(s) :**
- 2026-05-22, Vague 1 fixes ia_back depuis forge : 4 sub-agents lancés en parallèle (general-purpose, hook-creator, claudemd-optimizer), 3/4 ont échoué sur permission cross-repo (gain : ~0). Réexécution directe en session principale : 5 fixes en 2 minutes.
- Même avec `CLAUDE_AGENT=agent-creator`, le bypass ne traverse pas la frontière repo (vérifié 2026-05-22).
- Session principale forge → Edit/Bash sur `C:\Users\raphael.picard_neote\Documents\neot-v2\ia_back\` = OK (vérifié).

**Réconciliation 26 mai (révise cette règle pour UN cas)** : la délégation cross-repo via `agent-creator` avec **path absolu explicite dans le prompt** (`C:/Users/.../<repo>/.claude/agents/<nom>.md`) FONCTIONNE — 3/4 migrations Haiku + 2 fusions reviewer passées (ia_back, neo_ia). La règle « ne pas déléguer cross-repo » reste valable pour le **bypass `CLAUDE_AGENT` env-var** (qui ne traverse pas) et pour les **fix de fichiers projet** via sub-agent générique. Cf [[agent-creator-path-absolu-cross-repo]] (fait foi sur le cas agent-creator + path absolu).

Related : [[subagent-permissions-limitation]], [[feedback_audit_repo_method]], [[agent-creator-path-absolu-cross-repo]].
