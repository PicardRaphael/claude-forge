---
name: devil-advocate-pair-hooks
description: Paire tracker+guard PostToolUse Agent rappelant devils-advocate avant livraison skill/agent, plus reasoning-cache-reminder
type: project
---

Trois hooks déployés le 2026-05-08 sur PostToolUse Agent :

- `devil-advocate-tracker.py` — quand `subagent_type == "devils-advocate"`, crée `.claude/.devil-advocate-done` (existence seule, pas de TTL)
- `devil-advocate-guard.py` — quand `subagent_type in (skill-creator, agent-creator)`, check marker : si présent → consume (delete one-shot) silencieusement ; si absent → print WARNING sur stdout
- `reasoning-cache-reminder.py` — si agent description contient debug/investigate/fix/resolve/architecture (word-boundary regex), print reminder `/reasoning-cache`, once-per-session via marker `.claude/.reasoning-reminder-shown`

**Why:** La rule `devils-advocate-pipeline.md` était advisory et ignorée systématiquement. Pattern marker+guard force la conscience du pipeline sans bloquer (exit 0).

**How to apply:**
- Tous les 3 hooks dans le même bloc matcher `Agent` dans settings.json PostToolUse
- Marker paths absolus hardcodés — jamais de chemins relatifs
- `subagent_type` est le champ canonique, mais fallback JSON scan complet car field name varie selon les CC versions
- Pas de TTL — existence seule (`os.path.exists(marker)`)
- One-shot pour devil-advocate : si skill-creator tourne 2x de suite, seule la 1ère passe silencieusement (intentionnel : chaque livrable = sa propre validation)
- `.claude/.devil-advocate-done` et `.claude/.reasoning-reminder-shown` ajoutés au .gitignore racine
- WARNING affiché via `print()` sur stdout — PostToolUse non-bloquant, Claude lit le stdout dans son contexte
- Reasoning-cache pattern regex : `r"\b(debug|investigate|fix|resolve|architecture|diagnose|troubleshoot|analyse|analyze)\b"` (re.IGNORECASE)
