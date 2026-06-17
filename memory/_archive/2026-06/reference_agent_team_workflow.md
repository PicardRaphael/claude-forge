---
name: agent-team-workflow-reference
description: Workflow d'equipe d'agents valide pour projets complets. Pattern rules CTO + agents specialises + gates. Reusable pour tout projet.
type: reference
---

## Workflow d'equipe d'agents — Pattern valide

### Orchestration = Rules, PAS un agent CTO

Depuis 2026-04-08, l'orchestration se fait via **rules** (.claude/rules/) pas un agent CTO :
- `cto-mindset.md` — vision produit, esprit critique, knowledge first
- `agent-delegation.md` — triage, workflows, gates, comment deleguer
- `skill-navigator.md` — quel skill pour quel besoin

La session principale orchestre directement. Pas d'agent intermediaire (#19077).

### Agents specialises (ia_back = 11 agents)

| Agent | Model | Role |
|-------|-------|------|
| architect | opus/high | Design + Review code (TOUJOURS apres dev) |
| dev | sonnet/medium | Implemente le plan de l'architecte |
| debugger | opus/high | Diagnostic root-cause + fix minimal |
| api-designer | sonnet/high | Design endpoints REST |
| refactor-pg-function | opus/high | Migration fonction PG → TS hexagonal |
| validator | sonnet/medium | Hard gate equivalence comportementale (migrations) |
| performance-engineer | sonnet/medium | Profiling, indexes, N+1 |
| security-auditor | sonnet/medium | OWASP, injection SQL |
| test-writer | sonnet/medium | Tests unitaires systematiques |
| code-reviewer | sonnet/medium | Review post-dev |
| db-inspector | sonnet/medium | Exploration ad-hoc BDD |

### Triage (via rules)

| Demande | Flow |
|---------|------|
| Feature/Migration | Architect → User valide → Dev → Architect Review → Validator → Performance → Security |
| Bug | Debugger → Test non-regression → Code-reviewer |
| Performance | Performance Engineer → Dev si fix → Architect Review |
| Securite | Security Auditor → Dev si fix → Security re-audit |

### Gates apres dev

| Gate | Systematique | Conditionnel |
|------|-------------|-------------|
| test-writer | TOUJOURS | — |
| code-reviewer | TOUJOURS | — |
| validator | Migrations PG | — |
| performance-engineer | Features + Migrations | "C'est lent" |
| security-auditor | Nouveaux endpoints | Avant release |

### Principes cles
- CLAUDE.md = constitution projet. Roles = agents separes.
- Descriptions YAML en anglais avec "Use when" trigger
- Opus pour architecture/debugging. Sonnet pour execution.
- `memory: project` sur tous les agents
- Skills metier avec section "Apprentissage"
- Knowledge First : neo-brain AVANT MCP PostgreSQL
