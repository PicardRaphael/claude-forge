---
description: "Delegate SKILL.md to skill-creator, agents to agent-creator, CLAUDE.md to claudemd-optimizer. Hook delegate-guard enforces this."
---

# Delegation aux agents specialises — OBLIGATOIRE + HOOK

Ne JAMAIS editer directement les fichiers que des agents specialises savent creer.

**Un hook `delegate-guard.py` BLOQUE les edits directs.** Si tu te fais bloquer, c'est que tu n'as pas delegue.

| Action | Agent a utiliser | BLOQUE PAR HOOK |
|--------|-----------------|-----------------|
| Creer/modifier une skill (SKILL.md) | `skill-creator` | Oui — exit 2 |
| Creer/modifier un agent (.md dans agents/) | `agent-creator` | Oui — exit 2 |
| Creer/modifier un hook | `hook-creator` | Non — mais rule s'applique |
| Optimiser un CLAUDE.md | `claudemd-optimizer` | Oui — exit 2 |

## Exceptions (le hook les connait)

- Correction de typo < 20 caracteres = warning mais pas bloque
- Variable CLAUDE_AGENT = specialist → bypass automatique

## Pourquoi

Les agents specialises appliquent les best practices (taille, structure, references/, frontmatter) automatiquement. L'edit direct a produit des composants non conformes a 3 reprises (2026-04-26 neoteem-brain, 2026-04-26 ia_back analyse complete). Documente dans le vault : `Knowledge/erreurs/erreur-edit-direct-skills.md`.
