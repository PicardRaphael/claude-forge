---
titre: "CLAUDE_AGENT env var = dead code dans les hooks"
resume: "Les hooks tdd-guard de neo_ia et ia_back utilisaient os.environ.get('CLAUDE_AGENT') pour détecter le test-writer — variable jamais settée par le runtime CC. Dead code masqué car le bypass fonctionnait via une autre exemption (fichiers tests/)."
aliases:
  - "CLAUDE_AGENT dead code"
  - "env var agent detection hook"
  - "erreur agent_type vs CLAUDE_AGENT"
  - "hook subagent detection"
  - "dead code env var hook"
type: erreur
domaine: claude-code
derniere-maj: 2026-05-21
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#domaine/hooks"
sources:
  - "Session 2026-05-21 — dispatch-guard + fix tdd-guard"
---
## Ce qui s'est passé

Les hooks `tdd-guard.py` (neo_ia) et `tdd-guard.ts` (ia_back) contenaient :
```python
if os.environ.get("CLAUDE_AGENT") == "test-writer":
    sys.exit(0)
```

Cette condition ne se déclenchait JAMAIS car `CLAUDE_AGENT` n'est pas une variable d'environnement automatique du runtime Claude Code.

## Pourquoi c'était masqué

Le bypass test-writer fonctionnait quand même car le test-writer écrit dans `tests/` qui est exempté par une autre règle (`TEST_INDICATORS`). Le dead code n'a jamais causé de blocage visible.

## Le vrai problème aurait émergé avec dispatch-guard

Si dispatch-guard avait utilisé le même pattern (`CLAUDE_AGENT` env var), il aurait bloqué TOUS les subagents (dev-neochat, dev-neodoc, etc.) car la variable est toujours vide.

## Quoi faire à la place

Lire `agent_type` ou `subagent_type` dans le JSON stdin du hook (multi-field fallback) :
```python
agent_type = data.get("agent_type", "") or data.get("subagent_type", "")
```

Le runtime CC injecte ces champs quand le hook s'exécute dans un subagent nommé. Le nom du champ varie selon les versions CC → toujours vérifier les deux.

## Comment l'éviter

- Jamais utiliser d'env var pour détecter le contexte d'exécution d'un hook — le runtime passe tout dans le JSON stdin
- Quand un hook utilise un champ du runtime, le tester empiriquement (pas juste en pipant du JSON pré-formé)
- Auditer les hooks existants pour d'autres patterns env var potentiellement dead code

## Liens

- [[critique-2026-05-21-dispatch-guard-livraison]] — critique DA qui a identifié le risque multi-field
- [[erreur-advisory-rules-insuffisantes]] — même pattern : code qui semble fonctionner mais ne fait rien
- [[architecture-decision-hook-maison-vs-plugin-tiers]] — contexte du tdd-guard maison


## Confirmation empirique — 2026-05-21

Tests end-to-end exécutés sur neo_ia ET ia_back. Payloads runtime capturés via `.claude/dispatch-debug.json`.

**Champ confirmé : `agent_type`** (top-level dans le JSON stdin).

| Contexte | `agent_type` | `subagent_type` |
|----------|-------------|-----------------|
| Main session | ABSENT | ABSENT |
| Subagent test-writer | `"test-writer"` | non testé |
| Subagent dev-neochat | `"dev-neochat"` | non testé |
| Subagent dev (ia_back) | `"dev"` | non testé |

Le fallback `data.get("agent_type", "") or data.get("subagent_type", "")` est correct et robuste.

### Bug connexe corrigé

`has_failing_test()` dans `tdd-guard.py` (neo_ia) ne lisait que `data.get("failed", 0)`. En phase RED avec ImportError, pytest reporte `errors: 1, failed: 0` → le guard bloquait le dev à tort. Fix : `return bool(failed or errors)`.

### Recommandation mise à jour

Le champ runtime est **`agent_type`** (pas `subagent_type`). Le multi-field fallback reste la bonne pratique pour robustesse cross-version.