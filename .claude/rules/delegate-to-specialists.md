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
| Optimiser un CLAUDE.md | `claudemd-optimizer` | Oui — exit 2 |
| Critiquer un livrable majeur | `devils-advocate` | Non — mais rule s'applique |
| Evoluer/optimiser une skill | `skill-evolve` → skill `skill-creator` | Non — advisory |

## Pivot 6 juin 2026 — skill-creator + subagent-creator deviennent des skills

`skill-creator` et `subagent-creator` sont maintenant des **skills** invoquées par la session principale. Les hard blocks delegate-guard sur `SKILL.md` et `agents/*.md` ont été retirés — enforcement advisory : les skills guident les best practices, rien ne bloque un edit direct.

## Exceptions hook agents (delegate-guard.py)

- Correction de typo < 20 caracteres = warning mais pas bloque
- `agent_type` ou `agent_id` = specialist → bypass automatique

## Pourquoi

Les specialistes appliquent les best practices automatiquement. L'edit direct a produit des composants non conformes a 3 reprises (2026-04-26). Documente dans le vault : `Knowledge/erreurs/erreur-edit-direct-skills.md`.
