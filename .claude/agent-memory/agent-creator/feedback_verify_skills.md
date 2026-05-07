---
name: verify-skills-before-listing
description: Toujours vérifier l'existence des skills dans le projet cible avant de les lister dans skills: du frontmatter agent
type: feedback
---

Avant de générer un agent pour un projet X, Glob `<projet>/.claude/skills/<nom>/SKILL.md` pour CHAQUE entry dans `skills:`.

**Why:** La spec de codebase-analyst référençait `audit-health` — mais cette skill n'existe que dans `neo_ia/.claude/skills/` (Python/uv/FastAPI), pas dans `ia_back`. Lister une skill inexistante dans le projet cible charge rien silencieusement. L'agent tourne mais le workflow manque.

**How to apply:** Si la skill existe en user-level (`~/.claude/skills/`) ou en plugin, confirmer qu'elle est accessible depuis le projet cible (voir les agents existants du projet comme référence). Si absente, implémenter le workflow inline dans l'agent et le signaler à Raphael.
