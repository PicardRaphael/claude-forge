---
titre: "Setup vibe coding complet — pattern neo_ia/ia_back"
resume: "Architecture complete pour vibe coding avec Claude Code : agents, skills, pipeline, journalier, RECAP, /go, /recap, shared-learnings"
aliases:
  - "vibe coding pattern"
  - "setup projet claude code"
  - "journalier pattern"
domaine: claude-code
type: technique
derniere-maj: 2026-05-04
auteur: claude
sources:
  - "Session claude-forge 2026-05-04"
  - "[[Boris Cherny]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

# Setup Vibe Coding Complet

Pattern teste et deploye sur neo_ia (Python/FastAPI) et ia_back (Bun/Hono/TypeScript). Applicable a tout projet.

## Architecture agents — 100% opus

| Role | Modele | Effort | Pourquoi |
|------|--------|--------|----------|
| **Analystes** (architect, debugger, codebase-analyst) | opus | high | Raisonnement profond |
| **Devs** (tous les dev-*) | opus | medium | Opus medium > sonnet high en qualite pour cout comparable |
| **Gates** (test-writer, code-reviewer, perf, validator) | opus | medium | Meme logique |
| **Securite** (security-auditor/reviewer) | opus | high | Critique, pas de compromis |
| Session principale | opus | xhigh | Defaut 4.7 |

**Zero sonnet.** Boris : "opus medium fait du meilleur code que sonnet high pour le meme prix".

## Pipeline obligatoire

```
architect → dev-* → test-writer → code-reviewer
```

Enforce par 3 rules : `cto-mindset`, `agent-delegation`, `quality-gates`.

## Skills essentielles (a creer sur tout nouveau projet)

### Slash commands utilisateur

| Skill | Quand | Ce qu'elle fait |
|-------|-------|-----------------|
| `/recap` | Debut de session | Git status + log + tests + lint en 30s |
| `/go` | Implem terminee | Test → review → changelog → commit+push |
| `/evolve` | Planification | Propositions produit/archi priorisees |
| `/audit-health` | Health check | Deps, coverage, patterns perf |
| `/refactor-scan` | Code quality | Duplication, dead code, god files |

### Trio d'analyse (pour codebase-analyst)

1. `/evolve` — gaps produit/architecture
2. `/audit-health` — sante technique
3. `/refactor-scan` — code quality

L'agent `codebase-analyst` (opus high) orchestre les trois et produit un top 10 unifie.

## Documents a creer dans .claude/

| Fichier | Contenu |
|---------|---------|
| `RECAP.md` | Bilan complet : commandes, agents, skills, rules, effort levels |
| `journalier.md` | Guide journee type avec exemples concrets, quand ouvrir nouvelle fenetre |

### journalier.md — Structure

1. **Regle d'or** : quand nouvelle fenetre vs meme session (70-80% contexte = reset)
2. **Journee heure par heure** : feature, bug, refacto, pause, planification
3. **Chaque section** precise "(meme session)" ou "(nouvelle fenetre)"
4. **Scenarios speciaux** : reset, collegue, hotfix, saturation
5. **Tableau questions naturel** : "implemente X" → ce qui se passe
6. **Resume** : tableau commandes tapees vs automatique

## Rule shared-learnings (CRITIQUE)

Auto Memory = locale a chaque dev. Les apprentissages importants DOIVENT aller dans les sections Apprentissage des skills (commitees) pour que tous les devs en beneficient.

## Repos autonomes

Chaque repo doit etre self-contained. Pas de dependance vers claude-forge ou un repo externe pour les skills/agents. Si un dev quitte, les autres continuent.

## Pattern Boris au quotidien

```
/recap                    <- debut de session
  "implemente X"          <- pipeline auto
/go                       <- finalise
  ... pause ...
/recap                    <- reprise
  "fixe ce bug"           <- pipeline auto
/go                       <- finalise
```

90% du temps : `/recap` + `/go`. Le reste c'est situationnel.

## Prochaine etape : automatisation Jira

Le setup est pret pour brancher sur des tickets Jira :
- Option 1 : `/schedule` — routine planifiee qui check les tickets
- Option 2 : Manuel leger — "fais le ticket N2-12345" (MCP Atlassian)
- Option 3 : Hook sur branche — `feature/N2-12345` declenche la lecture du ticket

## Voir aussi

- [[Opus 4.7]] — effort levels, adaptive thinking
- [[Boris Cherny]] — workflow 5 terminaux, /go, /recap
- [[kit-rules-standard]] — rules de base pour tout projet
- [[pattern-agentic-engineering]] — checklist agentic engineering (evolution de ce pattern)
- [[neoteem-agentic-engineering-mapping]] — validation externe Karpathy
