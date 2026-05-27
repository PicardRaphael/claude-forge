---
name: permissionmode-mandatory
description: "permissionMode obligatoire sur TOUS les agents — acceptEdits pour créateurs, plan pour read-only. Sans ça, auto mode classifier bloque."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 87f41a8b-2683-4db0-ad9a-28804d7ea186
---

Tous les agents qui écrivent dans .claude/ (skill-creator, agent-creator, hook-creator, claudemd-optimizer, self-updater) DOIVENT avoir `permissionMode: acceptEdits` dans leur frontmatter.

**Why:** Session 2026-05-21 — le skill-creator s'est fait bloquer par l'auto mode classifier en essayant de créer outcomes-test. Le mode: "auto" passé à l'invocation Agent n'a pas suffi. Le `permissionMode` dans le frontmatter de l'agent est ce qui détermine les permissions effectives.

**How to apply:**
- Agents qui écrivent : `permissionMode: acceptEdits`
- Agents read-only (auditors, graders) : `permissionMode: plan`
- Vérifier à chaque création d'agent que permissionMode est défini
- Si un agent se fait bloquer → vérifier permissionMode en premier
