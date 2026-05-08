---
titre: "System Prompt — Amanda Askell"
resume: "Structure optimale system prompt Claude par Amanda Askell : role, constraints, output format, examples"
aliases:
  - "amanda askell system prompt"
  - "system prompt structure"
domaine: technique
type: prompt
cible: claude
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts"
tags:
  - "#type/prompt"
  - "#domaine/claude"
---

## Objectif

Structurer un system prompt Claude efficace selon les recommandations d'Amanda Askell (Anthropic).

## Structure recommandée

1. **Rôle** — Qui est Claude dans ce contexte
2. **Contraintes** — Ce qu'il ne doit PAS faire
3. **Format de sortie** — Structure attendue
4. **Exemples** — Few-shot si nécessaire
5. **Tone** — Style de communication

## Principes

- Mi-avril 2026 : Amanda a mis à jour le system prompt claude.ai "en collaboration avec Claude"
- Le prompt est co-écrit avec le modèle pour optimiser la compliance
- Priorité : contraintes > exemples > instructions positives

## Quand utiliser

Chaque fois qu'on crée un system prompt pour l'API Claude ou un agent.

## Liens

- [[Amanda Askell]]
- [[Context Engineering]]
- [[MOC-Prompts]]
