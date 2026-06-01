---
name: skill-activation-hook
description: UserPromptSubmit hook qui recommande les skills/commandes pertinentes via additionalContext quand le prompt contient des trigger keywords
metadata:
  type: project
---

Hook `skill-activation.py` — UserPromptSubmit, non-bloquant.

**Fichiers :**
- `.claude/hooks/skill-activation.py` — le hook principal
- `.claude/.skill-triggers.json` — carte des triggers, 2 formats supportés
- `.claude/hooks/test_skill_activation.py` — tests 8/8 PASS

**Design — 2 formats de triggers (rétro-compatible) :**
- **Legacy** : `{"name": {"type", "triggers": [...], "description"}}` — once-per-session par nom de skill
- **By_subject** : `{"name": {"type", "triggers_by_subject": {"sujet": [...]}, "description"}}` — re-fire si SUJET change. Tracker key = `skill_name::sujet`.

Seul `forge-brain` utilise `triggers_by_subject`. Les 30 autres entrées restent en format legacy, inchangées.

**Sujets `forge-brain`** (ordre priorité, specific avant general) :
`skill`, `agent`, `hook`, `claudemd`, `general`

**Design critique (advisor 2026-06-01) :**
- Subject déterminé par PRIORITÉ d'abord (premier subject qui matche en ordre dict), PUIS check tracker. Ne pas interleaver. Sinon `"propose une skill"` matcherait `skill` ET `general` lors d'un 2e appel (faux positif).
- `_tracker_key` attaché à chaque match (pas le nom brut). `main()` sauvegarde `m["_tracker_key"]`, pas `m["name"]`. Sinon les clés composites `forge-brain::skill` ne sont jamais markées, re-fire infini.

**Autres invariants :**
- Word-boundary regex (`\b`) sur tous les triggers
- Multi-match : une seule additionalContext combinée
- Bypass si prompt commence par `*`, `/`, `#`, `!` (après lstrip)
- Session tracker reset par suppression fichier dans `session-reminder.py` (SessionStart)
- Fail-open partout, exit 0 toujours

**Why:** `forge-brain` doit re-fire quand le sujet change (skill → agent dans une même session), mais ne pas spammer si le sujet est le même.

**How to apply:** Ajouter nouveaux triggers dans `.skill-triggers.json`. Pour skill non-forge-brain : format legacy. Pour forge-brain : ajouter triggers dans `triggers_by_subject[sujet]`.

Liens : [[session-health-hook]] (même événement UserPromptSubmit, pattern additionalContext identique)
