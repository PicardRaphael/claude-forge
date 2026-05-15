---
titre: "Pattern Prompt Rewriter — réécriture automatique des prompts utilisateur"
resume: "Hook UserPromptSubmit qui intercepte les prompts vagues et les enrichit avant que Claude les traite — analyse coût/bénéfice et alternatives"
aliases:
  - "prompt rewriter"
  - "prompt improver hook"
  - "UserPromptSubmit rewriter"
  - "input rewriter agent"
  - "prompt pre-processor"
  - "réécriture de prompt"
domaine: technique
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://github.com/severity1/claude-code-prompt-improver"
  - "https://mcpmarket.com/tools/skills/prompt-rewrite-scoping"
  - "https://egghead.io/lessons/rewrite-prompts-on-the-fly-with-user-prompt-submit-hooks~76rrt"
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#domaine/prompt-engineering"
---

## Description

Pattern qui intercepte les prompts utilisateur via un hook `UserPromptSubmit` et les enrichit (ajout de contexte, clarification, scoping) avant que Claude ne les traite.

## Implémentations existantes

### claude-code-prompt-improver (severity1)

- Hook `UserPromptSubmit` Python (~70 lignes)
- Évalue la clarté du prompt (~189 tokens, 2.8% d'un contexte 200K)
- Si vague → lance une skill qui pose 1-6 questions ciblées + fait de la recherche via Explore (Haiku)
- Si clair → passe directement (zéro overhead)
- Bypass avec préfixes : `*` (skip), `/` (slash), `#` (memorize)

### Prompt Rewrite & Scoping (mcpmarket)

- Skill qui transforme un input vague en spécification technique précise
- Identifie les livrables concrets, la définition de "terminé", les unknowns critiques
- Borne le scope et nomme explicitement le hors-scope

## Analyse coût/bénéfice

| Pour | Contre |
|------|--------|
| Réduit les allers-retours | +189 tokens par prompt = coût récurrent |
| Standardise la qualité | Risque de misinterpretation |
| Aide sur les tâches vagues | Sur tâches précises (majorité), c'est du gaspillage |
| Un hook suffit, pas d'agent | Latence ajoutée sur chaque prompt |

## Recommandation forge

**Pas en hook systématique** pour un utilisateur avancé. Préférer :
1. **Skill Activation Hook** — injecte des recommandations de skills, pas de réécriture
2. **Skill `/expand` manuelle** — invocable quand l'utilisateur décide qu'un prompt mérite d'être enrichi
3. **Hook léger** — si adopté, uniquement sur prompts < 20 mots, avec bypass sur préfixes

## Alternative retenue : Skill Activation Hook

Au lieu de réécrire le prompt, injecter des recommandations de skills pertinentes via `additionalContext`. Claude ne peut pas oublier car il n'a jamais eu à se souvenir. Voir [[skills-guide]] et [[cowork-skills-reliability]].

## Liens

- [[MOC-Techniques]]
- [[skills-guide]] — Activation des skills et budget
- [[hooks-guide]] — UserPromptSubmit et additionalContext
- [[harness-engineering]] — Feedforward controls (guides avant action)
- [[context-management]] — Token economy
