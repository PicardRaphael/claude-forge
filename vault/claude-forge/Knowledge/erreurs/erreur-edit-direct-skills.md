---
aliases:
- skill edition directe
- edit sans agent
- edit direct SKILL.md
- skill-creator non utilise
- composant non conforme edit manuel
auteur: claude
cree: 2026-04-26
derniere-maj: 2026-04-26
repo: neoteem-brain
resume: Editer les SKILL.md a la main produit des composants non-conformes — toujours
  deleguer a skill-creator
tags:
  - "#type/erreur"
  - "#erreur/comportement"
  - "#erreur/skill"
  - "#domaine/claude-code"
titre: Edit direct de skills au lieu d'utiliser skill-creator
type: erreur
---
# Edit direct de skills au lieu d'utiliser skill-creator

## Ce qui s'est passe

Le 2026-04-26, modification directe de 3 SKILL.md (neo-brain-dev, neo-brain-dev-ia, neo-brain-support) pour ajouter des fallback vault→code. Edits faits a la main au lieu d'utiliser l'agent skill-creator.

## Pourquoi c'est une erreur

- L'agent skill-creator applique automatiquement les best practices (taille < 500L, extraction references/, structure, frontmatter)
- L'edit direct a gonfle les fichiers sans extraire dans references/
- L'utilisateur a du rappeler la regle

## Recidive 2026-04-26 (ia_back)

Lors d'une analyse complete de ia_back, meme erreur a plus grande echelle :
- 6 skills modifiees + 1 creee sans skill-creator
- 14 agents modifies + 1 reecrit sans agent-creator
- Aucun check forge-brain, aucun check memoire, aucune skill de reference chargee
- Rules check-before-create, delegate-to-specialists, forge-brain-proactive, memory-discipline TOUTES ignorees

## Solution mise en place

1. **Hook deterministe** `delegate-guard.py` (PreToolUse sur Edit|Write) — bloque les edits sur SKILL.md, agents/*.md, CLAUDE.md
2. Rules renforcees avec reference au hook
3. Exceptions : typos < 20 chars, CLAUDE_AGENT = specialist

## Quoi faire a la place

1. Dispatcher skill-creator / agent-creator / claudemd-optimizer avec le contexte complet
2. Meme pour des petits changements — l'agent verifie les contraintes
3. Le hook bloquera de toute facon — autant deleguer d'entree

## Pattern general

Les rules advisory ne suffisent PAS. Chaque rule critique doit etre doublee d'un hook deterministe quand c'est techniquement possible.

## Liens

- [[e-descriptions-keyword-stuffing]] — autre erreur de non-respect des standards
