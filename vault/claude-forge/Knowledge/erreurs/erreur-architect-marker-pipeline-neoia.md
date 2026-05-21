---
aliases:
  - "architect marker pipeline neo_ia"
  - "session reset markers resume bug"
  - "architect-guard tests blocage"
  - "marker perdu test-writer dev"
  - "pipeline architect test dev casse"
tags:
  - "#type/erreur"
  - "#projet/neo_ia"
  - "#technique/hooks"
resume: "Pipeline architect→test-writer→dev casse sur neo_ia : SessionStart:resume wipe le marker + apps/*/tests/ matche le guard architect"
derniere-maj: 2026-05-21
projet: neo_ia
type: erreur
---

# Erreur — Pipeline architect-marker neo_ia casse entre turns

## Symptôme observé (2026-05-21)

Raphael lance architect → test-writer (RED) → dev-shared-tools (GREEN). À chaque turn, dev se fait bloquer par `architect-guard.py` : "marker manquant, relancer architect en fast-pass". Le marker est re-posé 3 fois dans le même run, gaspillant ~80k tokens par architect fast-pass redondant.

## Root causes (2 bugs distincts)

### Bug 1 — `session-reset-markers.py` wipe sur `SessionStart:resume`

Le hook est branché sur `SessionStart` sans filtrer le sous-type. SessionStart a 3 sous-types : `startup`, `resume`, `clear`. Sur `resume` (reprise de session après pause/refresh), le hook wipe alors que c'est la MEME session continue côté utilisateur.

Résultat : entre 2 turns de la même session perçue, le marker disparaît.

### Bug 2 — `architect-guard.py` n'exempte pas les tests

```python
GUARDED_PREFIXES = ("apps/", "packages/", ".github/")
EXEMPT_PREFIXES = (".claude/", "docs/")
```

Or `apps/neochat/tests/unit/test_x.py` matche `apps/` → test-writer se fait bloquer sur l'écriture des tests rouges. Le user voit "test-writer a perdu le marker" mais le marker est là, c'est le scope du guard qui est trop large.

## Fix

### Fix 1 — `session-reset-markers.py`

```python
import json, sys
try:
    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
except (json.JSONDecodeError, ValueError):
    data = {}
if data.get("source") == "resume":
    sys.exit(0)
# ... reset existant ...
```

### Fix 2 — `architect-guard.py`

Ajouter dans `is_guarded()` avant le check GUARDED_PREFIXES :

```python
if "/tests/" in p or p.startswith("tests/"):
    return False
```

## Leçon générale

Un pipeline marker (writer + guard + reset) doit définir explicitement la frontière "session" ET la frontière "scope". Les 2 bugs ici viennent d'avoir pris des défauts implicites :
- "SessionStart = nouvelle session" — FAUX, inclut `resume` qui est continuité
- "apps/ = code source" — FAUX, inclut `apps/*/tests/`

À auditer sur ia_back qui a le même pattern marker (architect-guard + agent-marker-writer + session-reset-markers).

## Anti-pattern observé

User accepte le surcoût ("je relance l'architect en fast-pass pour poser le marker") au lieu de diagnostiquer le hook. 3 fast-pass × 80k tokens = 240k tokens gaspillés sur un run, et l'erreur se reproduira à chaque session future tant que les hooks ne sont pas patchés.

**Règle Jarvis** : quand un workaround revient ≥ 2 fois dans la même session, c'est un bug à diagnostiquer, pas un workflow à mémoriser.

## Liens

- [[erreur-marker-ttl-blocage-agents]] — précédent bug marker sur les mêmes hooks
- [[markers-pipeline-must-be-complete]]
- [[hooks-enforcement-pattern]]
- [[neo-ia-tests-lenteur-diagnostic]] — autre sédiment hook/conftest sur neo_ia
