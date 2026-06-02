---
name: workflow-ultracode-keyword
description: Le mot-déclencheur des Dynamic Workflows passe de `workflow` à `ultracode` en CC v2.1.160 (2 juin 2026)
metadata:
  type: reference
---

Depuis **CC v2.1.160** (2 juin 2026), le mot-déclencheur des Dynamic Workflows n'est plus `workflow` mais **`ultracode`**. Dire « workflow » dans un prompt ne déclenche plus l'orchestration multi-agents en arrière-plan.

Vérifié source primaire : raw GitHub CHANGELOG (`"renamed the dynamic-workflow trigger keyword from workflow to ultracode"`).

**Impact forge :** tout setup (rule, doc, skill, automatisation) qui mentionne « workflow » comme déclencheur attendu doit être mis à jour. À grep si un comportement de déclenchement automatique est attendu.

Détail complet du drop 2.1.155→2.1.160 : note vault [[CC juin 2026 - v2.1.160 ultracode]]. Cf [[reference_workflow_args_array_gotcha]] pour les autres gotchas Dynamic Workflows.
