---
name: audit-repo-method-4-parallel-auditors
description: "Pour auditer un repo `.claude/`, lancer 4 project-auditor en parallèle (agents/skills/hooks/rules+CLAUDE.md). Pas 1 seul, pas Explore. Volumétrie 60-80 composants nécessite ce découpage."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

Méthode d'audit `.claude/` validée sur neo_ia (22 mai) + ia_back (22 mai).

**Why:** Un seul auditeur sur 60+ composants tronque, perd des détails. Explore ne convient pas (read-only mais pas conçu pour audit conformité). general-purpose dilue.

**How to apply:**
- 4 `project-auditor` en parallèle, un par catégorie : agents · skills · hooks+settings · rules+CLAUDE.md
- Chaque auditeur reçoit checklist explicite (frontmatter, body, cross-check code, cross-check vault)
- Mentionner stack du repo (TS vs Python) pour éviter faux positifs cross-stack
- Lancer en `run_in_background: true` pour parallélisme réel
- Spécifier scope élargi : audit `.claude/` ET racine repo (`.mcp.json`, `conftest.py`, etc.) sinon angles morts (cf audit neo_ia raté `.mcp.json.postgres-optional`)

Réf : [[audit-claude-folder-pattern]] dans vault.
