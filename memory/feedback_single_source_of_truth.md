---
name: single-source-of-truth
description: Chaque concept a UN fichier canonique. Les skills/agents pointent vers doc/ au lieu de dupliquer.
type: feedback
---

Chaque concept doit avoir UN fichier source de vérité. Les skills et agents y réfèrent au lieu de dupliquer.

**Why:** L'architecture hexagonale était expliquée dans CLAUDE.md, doc/architecture.md ET la skill architecture-rules. Quand le dev agent avait un pattern "route → service" qui contredisait l'archi hexa, c'est justement parce que la duplication crée du drift.

**How to apply:**
- `doc/architecture.md` = source pour l'archi hexagonale
- `doc/testing.md` = source pour la stratégie de test
- Skills = rappel des règles essentielles + "lire doc/X.md pour le détail"
- Agents = pointent vers skills, jamais de templates ou patterns inline longs
- Si un template est dans un agent, l'extraire dans une skill
