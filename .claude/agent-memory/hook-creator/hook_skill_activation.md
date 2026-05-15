---
name: skill-activation-hook
description: UserPromptSubmit hook qui recommande les skills/commandes pertinentes via additionalContext quand le prompt contient des trigger keywords
metadata:
  type: project
---

Hook `skill-activation.py` — UserPromptSubmit, non-bloquant, timeout 3s.

**Fichiers :**
- `.claude/hooks/skill-activation.py` — le hook principal
- `.claude/.skill-triggers.json` — carte des triggers (étendue : `{"name": {"type", "triggers", "description"}}`)

**Design :**
- Word-boundary regex (`\b`) pour éviter faux positifs ("done" ne matche pas "abandoned")
- `type: "skill"` → `Skill(name)`, `type: "command"` → `/name`
- Multi-match : une seule additionalContext combinée
- Bypass si prompt commence par `*`, `/`, `#`, `!` (après lstrip)
- Session tracker `.skill-recommendations-session` — chaque skill recommandée une fois par session
- Reset du tracker dans `session-reminder.py` (SessionStart) — ajouté à la liste des markers

**Why:** 73% des skills avec descriptions passives n'activent jamais. Ce hook ferme ce gap.

**How to apply:** Ajouter de nouveaux triggers dans `.skill-triggers.json` uniquement — pas besoin de toucher le script. Utiliser word-boundary regex si des faux positifs émergent.

Liens : [[session-health-hook]] (même événement UserPromptSubmit, pattern additionalContext identique)
