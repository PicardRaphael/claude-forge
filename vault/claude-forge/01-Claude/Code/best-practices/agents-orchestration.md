---
titre: "Agents et orchestration Claude Code"
resume: "Guide des subagents et orchestration Claude Code — format YAML complet, pattern Generator/Evaluator, Dreaming, Outcomes, Agent Teams experimental"
aliases: ["agents orchestration", "orchestration agents CC", "subagents YAML", "agent frontmatter", "agent permissionMode", "agent memory project", "generator evaluator pattern", "agent delegation", "agent pipeline", "agent isolation worktree", "agent effort levels", "agent maxTurns"]
  - "agents orchestration CC"
  - "subagents guide"
  - "orchestration agents"
  - "Agent Teams guide"
  - "Dreaming Outcomes"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://www.anthropic.com/engineering/harness-design-long-running-apps"
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
---
## Philosophie

Boris Cherny :
> "Feature-specific subagents beat general 'qa' or 'backend engineer' agents. Specificity buys you better tool selection and tighter context."

Utiliser les subagents pour "throw more compute at a problem and offload tasks to keep your main context clean."

## Frontmatter YAML complet

| Champ | Description |
|-------|-------------|
| `name` | Identifiant unique, lowercase + tirets. Recu par les hooks comme `agent_type` |
| `description` | QUAND Claude doit deleguer a cet agent |
| `tools` | Allowlist d'outils. Herite tout si omis. `Agent(worker, researcher)` restreint les subagents |
| `disallowedTools` | Denylist. Appliquee avant `tools` |
| `model` | `sonnet`, `opus`, `haiku`, model ID complet, ou `inherit` (defaut) |
| `effort` | Override effort |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Max tours agentic avant arret |
| `skills` | Skills pre-chargees au demarrage (contenu complet injecte) |
| `mcpServers` | Serveurs MCP disponibles |
| `hooks` | Hooks scopes a cet agent |
| `memory` | Scope memoire persistante : `user`, `project`, `local` |
| `background` | `true` = toujours en tache de fond |
| `isolation` | `worktree` = git worktree isole, auto-nettoye si pas de changements |
| `color` | Couleur d'affichage : `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | Auto-soumis comme premier tour quand lance via `--agent` |

### Built-in subagents

- **Explore** — Haiku, read-only, recherche rapide
- **Plan** — Modele herite, read-only, architecture
- **general-purpose** — Modele herite, tous les outils

**Contrainte** : les subagents ne peuvent PAS spawner d'autres subagents.

## Pattern Generator/Evaluator (Anthropic)

> "Separating the agent doing the work from the agent judging it proves to be a strong lever."

Les agents "reliably skew positive when grading their own work." La separation est obligatoire pour la fiabilite.

### Architecture 3 agents (long-running)

1. **Planner** — 1-4 phrases → spec produit complete (~$0.46)
2. **Generator** — Sprints iteratifs, git, auto-evaluation avant handoff (~$113.85)
3. **Evaluator** — Playwright MCP pour tester comme un user, grade contre rubric (~$10.39)

Performance : Solo agent = 20 min / $9 vs Full harness = 3h50 / $124.70. Qualite incomparable.

### Sprint Contracts

Avant chaque sprint, generator et evaluator negocient :
- Ce qui constitue "termine"
- Criteres de succes testables
- Limites d'implementation

## Dreaming (research preview)

Process background planifie qui analyse les sessions passees :
- Detecte les erreurs recurrentes et workflows convergents
- Identifie les preferences d'equipe
- Restructure la memoire pour garder le high-signal

Harvey : **~6x increase** en taux de completion de taches.

Deux modes : mise a jour automatique ou review manuelle avant application.

## Outcomes (public beta)

Rubrics de succes en langage naturel. Un evaluateur separe (son propre context window, pas de biais) grade l'output. Si en dessous du seuil → feedback detaille → iteration.

Performance : +10 points sur taches complexes, +8.4% sur .docx, +10.1% sur .pptx.

## Multi-agent orchestration (public beta)

Lead agent decompose le travail, delegue a des subagents specialises avec modeles/prompts/outils custom. Subagents en parallele sur filesystem partage. Le lead peut check-in mid-workflow.

## Agent Teams (experimental)

Feature distincte des subagents. Instances CC independantes qui se parlent directement.

```
Team Lead
  ├── Teammate A (instance CC independante)
  ├── Teammate B
  └── Teammate C
      ↕ Task list partagee + Mailbox
```

Hooks specifiques : `TeammateIdle`, `TaskCreated`, `TaskCompleted`.

### Quand utiliser Agent Teams vs subagents

- **Subagents** : taches sequentielles, pipeline (architect → dev → reviewer)
- **Agent Teams** : taches paralleles independantes avec coordination

## Orchestration a l'echelle (Boris, Sequoia mai 2026)

- 5-10 root sessions, chacune spawning "probablement quelques centaines d'agents"
- Overnight : "quelques milliers d'agents doing deeper work"
- Record : 150 PRs en un seul jour, entierement depuis son telephone
- "Loops are the future" — dizaines de loops persistants : babysit PRs, fix CI flaky, cluster feedback Twitter

## Pattern claude-progress.txt (Anthropic)

Chaque session coding suit cette sequence :
1. `pwd` pour confirmer le working directory
2. Lire git logs et fichiers de progres
3. Lire la features list, selectionner la plus haute priorite incomplete
4. Lancer `init.sh` pour demarrer le dev server
5. Test E2E basique AVANT d'implementer
6. Fixer les bugs existants AVANT d'ajouter des features

Feature list en **JSON** (pas Markdown — "le modele est less likely to inappropriately change JSON files").

## Liens

- [[skills-guide]] — Skills pre-chargees dans les agents
- [[hooks-guide]] — Hooks scopes aux agents
- [[context-management]] — Subagents pour isolation de contexte
- [[harness-engineering]] — Agents dans le paradigme harness
- [[Boris Cherny]] — Fleet Commander workflow
- [[Cowork GA]] — Agent Teams et Dispatch
