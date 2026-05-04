---
titre: "Computer Use dans Claude Code"
resume: "Research preview macOS+Windows, controle souris/clavier, Dispatch integration, Pro/Max only"
type: feature
date: 2026-03-24
derniere-maj: 2026-05-04
auteur: claude
tags:
  - "#type/feature"
  - "#domaine/claude-code"
---

# Computer Use dans Claude Code

## Statut

- **Research preview** — macOS (24 mars) + Windows (3 avril)
- **Pro et Max** uniquement (pas Team/Enterprise)
- CC v2.1.85+ requis, session interactive uniquement (pas `-p`)
- Pas dispo via Bedrock/Vertex/Foundry

## Activation

1. `/mcp` → selectionner `computer-use` → Enable
2. Premiere utilisation : permissions macOS Accessibility + Screen Recording
3. Persiste par projet

## Fonctionnement

- Priorite : connectors existants → browser control → desktop control
- Demande permission avant chaque nouvelle app
- Screenshots pour comprendre l'ecran
- Peut compiler, lancer, cliquer, screenshoter dans la meme conversation

## Integration Dispatch

- Assigner des taches depuis le telephone
- Claude les execute sur le Mac/PC au bureau
- Supporte taches recurrentes (emails, metriques, PRs)

## Limitations

- Taches complexes parfois besoin d'un 2eme essai
- Plus lent que les integrations directes
- Voit tout ce qui est visible a l'ecran (attention donnees sensibles)

## Liens

- [[Dispatch]]
- [[Cowork GA]]
