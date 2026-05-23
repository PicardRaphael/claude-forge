---
titre: "GSD Framework — Get Shit Done, ~59K stars (mai 2026)"
resume: "Framework SDD ~59K stars créé par Lex Christopherson (TACHES org). Chaque subagent reçoit contexte frais 200K tokens. Plans = prompts exécutables. Résout le context rot"
aliases:
  - GSD
  - get shit done
  - gsd framework
  - gsd-build
  - context rot solution
  - Lex Christopherson
domaine: development
type: technique
derniere-maj: 2026-05-23
sources:
  - "https://github.com/gsd-build/get-shit-done"
  - "https://gsd.build/"
  - "https://www.augmentcode.com/learn/gsd-58k-stars-claude-code"
tags:
  - "#type/technique"
  - "#domaine/workflow"
  - "#domaine/framework"
auteur: claude
---

## Problème résolu

**Context rot** — la qualité se dégrade à mesure que la fenêtre de contexte se remplit. La tâche 50 est moins bien faite que la tâche 1.

## Auteur et stats

- Créé par **Lex Christopherson** (GitHub : glittercowboy), house music producer à Costa Rica, sous l'org TACHES
- Repo : `gsd-build/get-shit-done`
- Crossé **59K+ stars** en mai 2026 (~58.9K confirmé par Augment Code mi-mai)
- Adopté en production par engineers chez Amazon, Google, Shopify, Webflow

## Pipeline (6 étapes)

Le workflow suit une séquence : **define → discuss → plan → execute → verify → ship**. GSD expose 29 Skills + 12 Custom Agents + 2 Hooks. Les noms exacts de slash commands varient par release (consulter le README repo pour la liste actuelle).

## Artefacts persistants

```
PROJECT.md       ← vision et scope
REQUIREMENTS.md  ← requirements dérivés
ROADMAP.md       ← phases et dépendances
STATE.md         ← état courant
CONTEXT.md       ← contexte technique consolidé
```

## Innovation clé : contexte frais par agent

> ✅ Verbatim Augment Code (review GSD) : *"up to 200K tokens dedicated to implementation"* + *"Each plan is 2–3 tasks, designed to fit in ~50% of a fresh context window"*

- Chaque subagent reçoit une **fenêtre de contexte fraîche de 200K tokens**
- Session principale reste à 30-40% de contexte
- Plans scopés à **~50% d'un contexte frais**
- Résultat : Task 50 a la même qualité que Task 1

## Insight fondamental

> ✅ Verbatim GSD docs (via Augment Code) : *"Plans are prompts: The PLAN.md file isn't a document that becomes a prompt — it IS the executable instruction. Subagents read it directly."*

## Ce qu'on a pris pour /spec Neoteem

- Concept de discussion AVANT planning (notre phase 1 interview)
- Artefacts persistants entre sessions
- Vagues parallèles (intégré dans decompose-ticket)

## Liens

- [[MOC-Techniques]]
- [[pattern-spec-driven-development]]
- [[pattern-github-spec-kit]]
- [[Context Engineering]]
- [[Lex Christopherson]]
