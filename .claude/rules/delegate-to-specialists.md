---
description: "Delegate agents to agent-creator, CLAUDE.md to claudemd-optimizer. Skills: invoke skill-creator skill directly — no hard block since 2026-06-06 pivot."
---

# Delegation aux specialistes — OBLIGATOIRE

Ne JAMAIS editer directement les fichiers que des specialistes savent creer.

| Action | Specialiste | BLOQUE PAR HOOK |
|--------|-------------|-----------------|
| Creer/modifier une skill (SKILL.md) | Skill `skill-creator` (Skill tool) | Non — advisory |
| Creer/modifier un agent (.md dans agents/) | Agent `agent-creator` | Oui — exit 2 |
| Creer/modifier un hook | `hook-creator` | Non — mais rule s'applique |
| Optimiser un CLAUDE.md | `claudemd-optimizer` | Oui — exit 2 |
| Critiquer un livrable majeur | `devils-advocate` | Non — mais rule s'applique |
| Evoluer/optimiser une skill | `skill-evolve` → skill `skill-creator` | Non — advisory |

## Pivot 6 juin 2026 — skill-creator devient une skill

`skill-creator` est maintenant une **skill** (`.claude/skills/skill-creator/`) invoquee par la session principale, non un agent. Le hard block delegate-guard sur `SKILL.md` a ete retire — enforcement advisory : la skill guide les best practices, rien ne bloque un edit direct.

## Exceptions hook agents (delegate-guard.py)

- Correction de typo < 20 caracteres = warning mais pas bloque
- `agent_type` ou `agent_id` = specialist → bypass automatique

## Pourquoi

Les specialistes appliquent les best practices automatiquement. L'edit direct a produit des composants non conformes a 3 reprises (2026-04-26). Documente dans le vault : `Knowledge/erreurs/erreur-edit-direct-skills.md`.
