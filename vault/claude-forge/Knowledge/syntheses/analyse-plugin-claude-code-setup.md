---
titre: "Analyse du plugin claude-code-setup (Anthropic)"
resume: "Analyse comparative du plugin officiel vs forge — gaps identifiés et intégrés"
aliases:
  - "claude-code-setup"
  - "automation recommender"
  - "plugin setup anthropic"
  - "isabella he plugin"
  - "analyse plugin officiel"
type: knowledge
derniere-maj: 2026-05-26
auteur: claude
sources:
  - "~/.claude/plugins/cache/claude-plugins-official/claude-code-setup/1.0.0/"
  - "Isabella He (isabella@anthropic.com)"
tags:
  - "#type/knowledge"
  - "#domaine/claude-code"
---
## Contexte

Plugin officiel Anthropic `claude-code-setup` v1.0.0, auteur Isabella He. Contient une seule skill `claude-automation-recommender` (read-only) avec 5 fichiers references/.

## Découvertes

### Structure
- `SKILL.md` — workflow en 3 phases (analyse → recommandations → rapport)
- `references/hooks-patterns.md` — hooks par framework (Prettier, ESLint, Ruff, Black, gofmt, rustfmt, mypy, pyright)
- `references/mcp-servers.md` — 15+ MCP servers mappés par signal codebase
- `references/skills-reference.md` — 8 templates skills custom + plugins officiels
- `references/subagent-templates.md` — 8 templates agents (code-reviewer, security-reviewer, test-writer, api-documenter, performance-analyzer, ui-reviewer, dependency-updater, migration-helper)
- `references/plugins-reference.md` — 11 plugins LSP + plugins workflow

### Forces du plugin
- Tables de détection systématiques signal → recommandation (exhaustives)
- Catalogue MCP structuré et à jour
- Decision Framework clair "quand recommander quoi"
- Recommandation de plugins LSP par langage

### Faiblesses vs forge
- Zéro contexte métier — générique pur
- Pas de mode optimisation (ne gère pas l'existant)
- Pas de priorisation (🔴🟡🟢)
- Pas de mémoire — chaque analyse part de zéro
- Pas d'anti-patterns (pas d'orchestrateur, pas de doc agent)
- Pas de pipeline qualité, pas de gates

## Implications

### Intégré dans forge (2026-04-26)
1. **`cc-advisor/references/mcp-catalog.md`** — nouveau fichier, catalogue MCP structuré adapté + contexte Neoteem
2. **`project-analyzer.md`** — Phase 0 détection mécanique + Phase 0.5 audit config CC existante + sections rapport (Config, Commandes CLI, Plugins)
3. **`cc-advisor/SKILL.md`** — table LSP plugins + plugins workflow + commandes CLI + config settings + lien MCP catalog + 12 nouvelles lignes grille décision
4. **`cc-news/SKILL.md`** — veille sur version plugin Anthropic ajoutée aux sources

### Non intégré (par choix)
- Templates subagents `api-documenter` et `migration-helper` → contradisent nos règles (no-doc-agent, pas d'orchestrateur)
- Hooks patterns détaillés par framework → déjà implicite dans `cc-hooks-ref`, Anthropic en cache local si besoin

## Liens

- [[cowork-architecture|Plugin Marketplace]]
- [[workflow-claude-code-optimal|Best practices Boris Thariq]]


## Veille 26 mai 2026 — 11 plugins additionnels analysés

Analyse étendue à 11 plugins officiels (hookify, skill-creator, agent-sdk-dev, code-review, mcp-server-dev, remember, atomic-agents, pydantic-ai, sourcegraph, data-engineering, forge-skills). Marketplace claude-plugins-official compte désormais **203 plugins**.

**Verdict consolidé** : 2 ADAPT (skill-creator eval pattern, code-review confidence scoring), 3 REFERENCE (agent-sdk-dev, mcp-server-dev, pydantic-ai watch-list), 6 SKIP.

Synthèse complète : [[plugins-officiels-veille-2026-05-26]].

**Découvertes ajoutées au forge** :
- Pattern eval A/B Anthropic ([[eval-pattern-anthropic-skill-creator]]) — gap mesurable vs outcomes-grader
- Confidence scoring 0-100 (code-review Boris Cherny) — enrichissement [[da-blocking-arbitrage]]
- Anti-pattern hookify workflow hooks ([[anti-pattern-hookify-workflow-hooks]]) — confirme doctrine 22 mai
