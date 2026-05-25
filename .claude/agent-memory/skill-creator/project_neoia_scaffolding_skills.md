---
name: neoia-scaffolding-skills-created
description: 4 skills de scaffolding NeoIA créées 2026-05-25 — patterns FastAPI endpoint, SQLAlchemy repo, LangGraph agent, Langfuse debugging
metadata:
  type: project
---

4 skills créées dans `neo_ia/.claude/skills/` basées sur scan code réel (étape 5 méthode-analyser-repo).

**Why:** Patterns récurrents observés (20+ endpoints, 15+ repos, 8 agents, wrapper Langfuse centralisé) sans skills de scaffolding dédiées. Développeurs copient à la main sans patron de référence.

**How to apply:** Charger ces skills quand on scaffolde de nouveaux composants dans neo_ia.

## Skills créées

| Skill | Path | LOC | Catégorie |
|-------|------|-----|-----------|
| `create-fastapi-endpoint` | `.claude/skills/create-fastapi-endpoint/SKILL.md` | 155 | code-scaffolding |
| `create-sqlalchemy-repo` | `.claude/skills/create-sqlalchemy-repo/SKILL.md` | 276 | code-scaffolding |
| `create-langgraph-agent` | `.claude/skills/create-langgraph-agent/SKILL.md` | 281 | code-scaffolding |
| `langfuse-trace-debugging` | `.claude/skills/langfuse-trace-debugging/SKILL.md` | 195 | debugging |

## Pattern NeoIA extrait empiriquement

- **FastAPI** : APIRouter prefix/tags, constantes rate limit en haut, `Annotated[UserContext, Depends(get_current_user)]`, guard `if not user.acteur_id:`, Google docstrings
- **SQLAlchemy** : `AsyncSession`, window function `func.count().over()` pour pagination, JSONB preview via `type_coerce(literal("..."), Text)`, acteur_id guard systématique, JAMAIS `session.commit()` dans repo
- **LangGraph agent** : 4 fichiers (state.py TypedDict, nodes.py async, graph.py builder, prompts.py), `total=False` sur TypedDict, retour dict partiel, JAMAIS `saver.setup()`
- **Langfuse** : `get_langfuse_handler()` retourne None si non configuré (graceful degradation), `finalize_trace()` en 1 appel (pas update_trace_attributes + update_trace_input_output séparés)

## Discrimination avec skills existantes

- `langfuse` (existante) = CLI + API Langfuse générique. `langfuse-trace-debugging` = wrapper NeoIA spécifique.
- `langgraph` (existante) = StateGraph patterns génériques. `create-langgraph-agent` = scaffolding 4 fichiers custom pipeline NeoIA.
