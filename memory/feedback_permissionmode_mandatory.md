---
name: permissionmode-mandatory
description: "permissionMode obligatoire sur TOUS les agents — acceptEdits pour créateurs, plan pour read-only. Sans ça, auto mode classifier bloque."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Tous les agents qui écrivent dans .claude/ DOIVENT avoir `permissionMode: acceptEdits` dans leur frontmatter.

**Why:** Session 2026-05-21 — auto mode classifier bloque si permissionMode absent. Le `permissionMode` dans le frontmatter est ce qui détermine les permissions effectives, pas le mode passé à l'invocation.

**How to apply:**
- Agents qui écrivent : `permissionMode: acceptEdits`
- Agents read-only (auditors, graders) : `permissionMode: plan`
- Vérifier à chaque création d'agent (via skill `subagent-creator`) que permissionMode est défini
- Si un agent se fait bloquer → vérifier permissionMode en premier

> Note 6 juin 2026 : skill-creator et agent-creator sont devenus des skills (subagent-creator). La règle permissionMode s'applique toujours à TOUS les agents .md créés.
