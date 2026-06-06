---
description: "Delegate agents to agent-creator, CLAUDE.md to claudemd-optimizer. Skills: invoke skill-creator skill directly — no hard block since 2026-06-06 pivot."
---

# Delegation aux specialistes — OBLIGATOIRE

Ne JAMAIS editer directement les fichiers que des specialistes savent creer.

| Action | Specialiste | BLOQUE PAR HOOK |
|--------|-------------|-----------------|
| Creer/modifier une skill (SKILL.md) | Skill `skill-creator` (Skill tool) | Non — advisory |
| Creer/modifier un agent (.md dans agents/) | Skill `subagent-creator` (Skill tool) | Non — advisory |
| Creer/modifier un hook | Skill `hook-creator` (Skill tool) | Non — advisory |
| Creer/optimiser un CLAUDE.md | Skill `claudemd-optimizer` (Skill tool) | Oui — exit 2 sur CLAUDE.md (protection conservée) |
| Critiquer un livrable majeur | `devils-advocate` | Non — mais rule s'applique |
| Evoluer/optimiser une skill | `skill-evolve` → skill `skill-creator` | Non — advisory |

## Pivot 6 juin 2026 — skill-creator + subagent-creator + hook-creator + claudemd-optimizer deviennent des skills

Les 4 créateurs sont maintenant des **skills** invoquées par la session principale.
- `SKILL.md` et `agents/*.md` : hard block retiré — advisory
- `CLAUDE.md` : hard block **conservé** (exit 2) — la skill `claudemd-optimizer` (thread principal) passe légitimement
- `hooks/` : pas de protection delegate-guard (hook-creator reste advisory)

## Exceptions hook agents (delegate-guard.py)

- Correction de typo < 20 caracteres = warning mais pas bloque
- `agent_type` ou `agent_id` = specialist → bypass automatique

## Pourquoi

Les specialistes appliquent les best practices automatiquement. L'edit direct a produit des composants non conformes a 3 reprises (2026-04-26). Documente dans le vault : `Knowledge/erreurs/erreur-edit-direct-skills.md`.
