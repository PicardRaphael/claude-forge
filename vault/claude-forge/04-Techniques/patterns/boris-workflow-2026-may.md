---
titre: "Boris Cherny Workflow Mai 2026 — AI Ascent Sequoia"
resume: "Setup actuel Boris : 5-10 sessions web + centaines d'agents + /loop partout. 150 PRs/jour record. Coding is solved depuis oct 2025. /loop = feature killer. Routines = loops serveur. Modèle décide de tout à terme"
aliases:
  - "boris workflow 2026"
  - "boris ascent sequoia"
  - "boris 150 PRs"
  - "boris loop workflow"
  - "how boris uses claude code 2026"
  - "boris setup may 2026"
type: technique
derniere-maj: 2026-05-11
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=SlGRN8jh2RI"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Contexte

AI Ascent 2026, Sequoia Capital. Boris Cherny (créateur Claude Code) interviewé par Lauren Reeder. Mai 2026.

## Setup personnel Boris (mai 2026)

| Aspect | Détail |
|--------|--------|
| **Interface** | Principalement **téléphone** (Claude app iOS → code tab) |
| **Sessions** | 5-10 sessions web en parallèle |
| **Agents** | "Probably a few hundred agents going" par session |
| **Nuit** | "A few thousand agents doing deeper work" chaque nuit |
| **PRs** | "Usually a few dozen PRs every day", record = **150 PRs en 1 jour** |
| **Code écrit à la main** | 0% depuis octobre-novembre 2025 |

### Évolution vs janvier 2026
En janvier 2026 (thread Twitter) : 5 instances terminal + 5-10 claude.ai/code. Maintenant : principalement mobile, moins de terminal.

## /loop = feature killer

> "I sort of feel like loops are the future at this point."

Boris a **des dizaines de loops** en permanence :
- Babysit PRs (fix CI, auto-rebase)
- Keep CI healthy (fix flaky tests)
- Cluster Twitter feedback toutes les 30 minutes → envoi Slack via MCP
- Opus 4.7 propose spontanément des loops ("I noticed the data is changing, I'll start a loop and give you a report every 30 minutes")

### Routines = loops côté serveur
Même concept mais persistent même si laptop fermé. Lancé au Code with Claude.

## Insights clés

### "Coding is solved"
- Pour Boris : 100% du code écrit par le modèle depuis oct 2025
- Claude Code codebase = TypeScript + React ("nothing complicated")
- Choisi car "on distribution" pour le modèle en 2024 (modèle moins intelligent, langage/framework comptait plus)
- Pas encore solved partout : gros codebases complexes, langages exotiques → "wait for the next model"

### Product overhang
Claude Code construit 6 mois avant PMF, en anticipant le prochain modèle. PMF arrivé avec Opus 4 (mai 2025), inflecté à chaque release (4.5, 4.6, 4.7).

### Parallélisme = product design problem
> "It's not on users to figure out how to hold the tools better. If that's the case, it's actually a product design problem."

Le modèle devrait naturellement paralléliser. Si l'utilisateur doit forcer → c'est un bug de prompting/harness.

### Org structure > technologie
> "The place that we're ahead is not the technology — it's the organizational structure and process."

La même techno est disponible pour tous (Anthropic = platform). L'avantage = comment l'organisation s'adapte.

### Vision long terme
> "By a couple years from now, the model is going to be doing all the code. It's going to be starting the agents. It's going to be building the environments."

L'agent décide de tout : quel modèle utiliser, local ou cloud, quelle architecture.

### MCP = réponse universelle
Pour l'accès aux tools (Salesforce, Docs, Calendar) : MCP. Pour le reste : Computer Use (lent mais efficace avec 4.7).

### Claude Design = prochain product overhang
Boris nomme Claude Design comme le prochain produit qui sera "pretty good today, a lot better soon".

## Pertinence pour forge

| Insight | Action forge |
|---------|-------------|
| /loop = killer feature | Utiliser plus de /loop (monitoring, vault check, PR babysit) |
| Routines = loops serveur | Adopter /schedule pour les tâches récurrentes |
| Opus 4.7 fait /loop spontanément | Ne pas forcer — laisser le modèle proposer |
| Org structure > tech | Le workflow forge (rules, pipeline, vault) EST notre avantage |
| Parallélisme = prompting | Si un agent ne parallélise pas → améliorer le prompt, pas blâmer le modèle |

## Liens

- [[Boris Cherny]] — Fiche leader
- [[best-practices-claude-code-leaders]] — Synthèse leaders CC
- [[MOC-Techniques]]
