---
titre: "Index Prompting — Quelle technique pour quel cas"
resume: "Guide de sélection : 12 techniques de prompting classées par objectif, complexité et modèle cible"
aliases:
  - "index prompting"
  - "quelle technique prompting"
  - "prompting decision tree"
  - "choisir technique prompt"
  - "prompting guide"
  - "prompt technique selector"
type: index
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/index"
  - "#domaine/prompt-engineering"
---

## Par objectif

| Je veux... | Technique | Note |
|------------|-----------|------|
| Structurer un system prompt | Amanda Askell Structure | [[amanda-askell-prompt-engineering]] |
| Obtenir un résultat précis sans micro-manager | Outcome-First Prompting | [[outcome-first-prompting]] |
| Éviter de sur-spécifier (modèles frontier) | Over-Specification Paradox | [[over-specification-paradox]] |
| Adapter le budget de réflexion | Adaptive Thinking | [[Adaptive Thinking]] |
| Prompter Chat vs Cowork vs Claude Code | Prompting par plateforme | [[prompting-chat-cowork-code]] |
| Forcer le raisonnement étape par étape | Chain of Thought | [[chain-of-thought]] |
| Donner des exemples au modèle | Few-Shot Prompting | [[few-shot-prompting]] |
| Construire un prompt robuste de A à Z | FORGE Machine | [[forge-prompt-machine]] |
| Savoir ce qui ne marche plus en 2026 | Techniques dépréciées | [[deprecated-techniques-2026]] |
| Optimiser le contexte (pas le prompt) | Context Engineering | [[Context Engineering]] |

## Par complexité

| Niveau | Techniques | Quand |
|--------|-----------|-------|
| Débutant | Few-Shot, Chain of Thought | Premiers prompts, tâches simples |
| Intermédiaire | Outcome-First, Amanda Askell Structure | System prompts, agents |
| Avancé | Over-Specification Paradox, Context Engineering | Optimisation frontier, pipelines agents |

## Par modèle cible

| Modèle | Conseils clés |
|--------|--------------|
| **Claude (Opus/Sonnet)** | Outcome-First, pas de few-shot inutile, Adaptive Thinking, `effort` levels |
| **GPT (5.x)** | Few-Shot efficace, function calling, structured output |
| **Gemini** | System instructions courtes, function declarations, ADK patterns |
| **Tout modèle frontier** | Over-Specification Paradox (seuil S*=0.509), Context Engineering > Prompt Engineering |

## Règles transversales

1. **Moins = mieux** sur modèles frontier (UCL 2601.00880)
2. **Outcome + critères de succès** > instructions procédurales (OpenAI GPT-5.5 guidelines)
3. **Context Engineering > Prompt Engineering** — ce que tu mets dans le contexte compte plus que comment tu le formules
4. **TDD prompts** (Askell) — tester le prompt comme du code, itérer sur les échecs

## Liens

- [[MOC-Prompts]]
- [[MOC-Techniques]]
- [[amanda-askell-prompt-engineering]]
- [[Context Engineering]]
