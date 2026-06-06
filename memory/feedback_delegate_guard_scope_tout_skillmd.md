---
name: delegate-guard-scope-tout-skillmd
description: "OBSOLÈTE — delegate-guard ne bloque plus SKILL.md (pivot 6 juin 2026 : skill-creator est devenu une skill, hard block retiré). Seuls agents/*.md et CLAUDE.md restent protégés."
metadata:
  type: feedback
  statut: obsolete
---

> ⚠️ **OBSOLÈTE depuis 6 juin 2026** — `SKILL.md` a été retiré de `PROTECTED` dans `delegate-guard.py`. La skill `skill-creator` remplace l'agent. Écriture directe de SKILL.md : permise, mais passer par `Skill(skill-creator)` reste la bonne pratique (checklist 6 dimensions, workflow Anthropic complet).

~~`delegate-guard.py` bloquait l'écriture de TOUT fichier nommé `SKILL.md` peu importe son emplacement.~~

**How to apply (mis à jour) :** Pour créer/modifier un `SKILL.md`, invoquer la skill `skill-creator` depuis la session principale. Advisory, pas hard-bloqué. Les agents `*.md` et `CLAUDE.md` restent hard-bloqués par delegate-guard.
