---
titre: "GSD Framework — Get Shit Done, 59K stars"
resume: "6 commandes (new-project → discuss → plan → execute → verify → ship). Chaque subagent reçoit un contexte frais 200K tokens. Plans = prompts exécutables. Résout le context rot"
aliases:
  - GSD
  - get shit done
  - gsd framework
  - gsd-build
  - context rot solution
domaine: development
type: technique
derniere-maj: 2026-05-12
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/framework"
---

## Problème résolu

**Context rot** — la qualité se dégrade à mesure que la fenêtre de contexte se remplit. La tâche 50 est moins bien faite que la tâche 1.

## Pipeline

1. `/gsd-new-project` — questions → recherche → requirements → roadmap
2. `/gsd-discuss-phase [N]` — capture les décisions AVANT le planning (layouts, API shapes, error handling)
3. `/gsd-plan-phase [N]` — boucle recherche → plan → vérification jusqu'à validation
4. `/gsd-execute-phase <N>` — plans exécutés en vagues parallèles, chaque exécuteur reçoit un contexte frais
5. `/gsd-verify-work [N]` — parcourt ce qui a été construit, crée des fix plans pour les problèmes
6. `/gsd-ship [N]` — crée une PR depuis le travail vérifié

## Artefacts persistants

```
PROJECT.md       ← vision et scope
REQUIREMENTS.md  ← requirements dérivés
ROADMAP.md       ← phases et dépendances
STATE.md         ← état courant
CONTEXT.md       ← contexte technique consolidé
```

## Innovation clé : contexte frais par agent

- Chaque subagent reçoit une **fenêtre de contexte fraîche de 200K tokens**
- La session principale reste à 30-40% de contexte
- Les plans sont scopés à **~50% d'un contexte frais** (atomicité agressive)
- Résultat : Task 50 a la même qualité que Task 1

## Insight fondamental

> "Plans are prompts — the PLAN.md file isn't a document that becomes a prompt, it IS the executable instruction."

## Ce qu'on a pris pour /spec Neoteem

- Concept de discussion AVANT planning (notre phase 1 interview)
- Artefacts persistants entre sessions
- Vagues parallèles (intégré dans decompose-ticket)

## Liens

- [[pattern-spec-driven-development]] — Pattern SDD complet
- [[pattern-github-spec-kit]] — Framework concurrent (Spec Kit)
- [[Context Engineering]] — Le contexte frais est du context engineering