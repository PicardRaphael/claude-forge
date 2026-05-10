---
titre: "Few-Shot Prompting"
resume: "Fournir 2-5 exemples input/output pour calibrer le format et le style de réponse du modèle"
aliases:
  - "few-shot prompting"
  - "few-shot"
  - "exemples dans le prompt"
  - "in-context learning"
  - "few shot examples"
type: technique
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Principe

Inclure 2-5 paires input/output dans le prompt pour montrer le format attendu. Le modèle apprend le pattern et le reproduit.

## Quand utiliser

- Calibrer un format de sortie précis (JSON, tableau, style)
- Tâches de classification avec catégories custom
- Quand le modèle ne comprend pas la consigne verbale
- Modèles plus petits (Haiku, modèles open-source)

## Quand NE PAS utiliser

- Modèles frontier (Opus 4.7) sur tâches bien décrites — les exemples consomment du contexte sans gain
- Si le format peut être spécifié en JSON schema ou structured output
- Si les exemples sont ambigus ou contradictoires

## Bonnes pratiques

- **Diversité** : couvrir les cas edge dans les exemples
- **Ordre** : mettre les exemples les plus représentatifs en premier
- **Quantité** : 2-3 suffisent sur frontier, 5+ sur petits modèles
- **Format** : `Input: ... → Output: ...` clair et consistant

## Liens

- [[index-prompting]]
- [[outcome-first-prompting]]
- [[deprecated-techniques-2026]]
