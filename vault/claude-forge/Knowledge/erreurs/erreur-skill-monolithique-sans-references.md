---
aliases:
- skill monolithique
- erreur skill longue
- references skill
- skill trop longue
- refactor skill references
auteur: claude
derniere-maj: 2026-05-10
domaine: claude-code
resume: 'Une skill qui grossit au-delà de ~200 lignes DOIT être refactorisée en orchestrateur
  + references/. Le cas cc-news : 459 lignes, 96 queries, agent tronqué, info ratée.'
sources: []
tags:
  - "#type/erreur"
  - "#erreur/skill"
  - "#domaine/claude-code"
titre: Erreur — Skill monolithique sans references/
type: knowledge
---
## Ce qui s'est passé

La skill `cc-news` a grandi progressivement de ~150 lignes à 459 lignes (limite 500) en ajoutant des leaders et des queries par domaine. Résultat :

1. **96 queries dans un seul fichier** — la gotcha dit "max 6-8 par agent" mais rien ne l'enforce
2. **GPT-5.5 raté** — le vault affichait encore GPT-5.3 parce que le scan ne couvrait pas bien les concurrents
3. **Triple répétition** — chaque leader apparaît 3x (roster, queries, format template)
4. **L'agent devil's advocate tronqué** — le fichier était trop long pour être analysé en 8 tours
5. **Pas de routing $ARGUMENTS** — `/cc-news RAG` et `/cc-news` exécutaient le même scan complet

## Pourquoi c'était une erreur

On ajoutait du contenu à un fichier monolithique au lieu de refactoriser. La règle `SKILL.md < 500 lignes` dans CLAUDE.md dit aussi `déporter le détail dans references/` — on l'a ignorée jusqu'au mur.

**Signal d'alarme manqué :** dès qu'une skill dépasse ~200 lignes, elle devrait être évaluée pour un split en references/.

## Ce qu'on aurait dû faire

Dès le premier ajout de 16 leaders + 20 queries (fine-tuning), se poser la question : "est-ce que ce contenu est de l'orchestration ou de la référence ?" Réponse : référence → `references/domain-finetuning.md`.

## Pattern correct

```
SKILL.md (~100-150 lignes)
├── Orchestrateur léger
├── Tier 0 queries (toujours exécutées)
├── Routing $ARGUMENTS → domaine
├── Spawn agents parallèles, chacun lit UN fichier reference
├── Capitalisation rules
└── Gotchas

references/
├── domain-X.md (leaders + sources + queries, auto-suffisant)
├── domain-Y.md
└── format-reponse.md
```

## Règle à appliquer

> **Seuil de refactor : 200 lignes.** Au-delà, évaluer si le contenu est de l'orchestration (reste dans SKILL.md) ou de la référence (part dans references/). Si >50% est de la référence → refactoriser.

> **Quand on ajoute un nouveau domaine à une skill existante**, toujours créer un fichier `references/domain-X.md` plutôt que d'ajouter au SKILL.md.

## Liens

- [[workflow-claude-code-optimal]] — Boris/Thariq best practices
- cc-news (skill forge) — la skill refactorisée
- [[erreur-edit-direct-skills]] — erreur liée (éditer sans spécialiste)