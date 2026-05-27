# claude-forge 🔨

**Assistant personnel Claude Code — Conseiller, Créateur, Optimiseur**

Créé le : 31 mars 2026

## Ce que c'est

Un studio méta-Claude Code : 11 agents, 47 skills, 9 hooks, 10 rules et un vault de connaissances (forge-brain) interrogeable par MCP. Il conseille, fabrique de la config Claude Code conforme pour tous tes projets, et capitalise chaque leçon apprise.

Pour une cartographie exhaustive (architecture, inventaire, sécurité, FAQ), voir **`CLAUDE_FORGE_SELF_PORTRAIT.md`**.

## Structure

```
claude-forge/
├── CLAUDE.md                  Contrat Jarvis + doctrine (source d'autorité)
├── .mcp.json                  Déclare le MCP forge-brain (HTTP :8091)
├── install.bat                Setup des prérequis CLI (Windows)
│
├── .claude/
│   ├── settings.json          Permissions + câblage des 9 hooks
│   ├── agents/                11 agents (créateurs, repo-inspector, devils-advocate…)
│   ├── skills/                47 skills (cc-advisor, cc-news, forge-brain, /recap, /done…)
│   ├── hooks/                 9 hooks Python (delegate-guard, security-guard, meta-commentary…)
│   ├── rules/                 10 rules de routing + doctrine
│   └── agent-memory/          mémoire par agent (project scope)
│
├── mcp-forge-brain/           Serveur MCP maison (FastMCP + SQLite FTS5, 21 outils)
├── vault/claude-forge/        Le "cerveau" — vault Obsidian (~412 notes)
├── ia-lead-neoteem/           Plugin Cowork (7 skills Responsable IA)
└── scripts/                   .bat de tâches planifiées (cc-news, forge-review, vault-audit)
```

### Agents clés

- `repo-inspector` — analyse / audit / scan d'un repo (mode=analyze|audit|scan)
- `agent-creator` / `skill-creator` / `hook-creator` / `claudemd-optimizer` — créateurs spécialisés
- `devils-advocate` — critique adversariale avant ship d'un livrable majeur
- `python-dev` — implémentation Python en TDD
- `responsable-ia` — casquette Lead IA Neoteem (CODIR, AI Act, roadmap, Loji)

## Installation

```bat
:: 1. Installer les prérequis CLI (Node, defuddle, yt-dlp, fastmcp…)
install.bat

:: 2. Dépendances du serveur MCP
cd mcp-forge-brain && pip install -e .

:: 3. Déployer globalement dans %USERPROFILE%\.claude\ (ou via la skill /install-forge)
xcopy /E /I .claude %USERPROFILE%\.claude
```

Vérifier : `/self-check` (cohérence interne), `/forge-status` (source vs installé). Le MCP forge-brain démarre seul au SessionStart (port 8091).

## Utilisation

```bash
# Reprise de contexte
/recap

# Analyser un projet et proposer une config CC
"Analyse mon repo /path/to/projet et propose la config Claude Code"

# Besoin flou → le conseiller décide
"J'ai besoin d'automatiser mes PRs"

# Créer un composant (délégué aux créateurs spécialisés)
"Crée un agent qui audite mon codebase"
"Je veux une skill /commit pour mon projet"
"J'ai besoin d'un hook de formatage Python"

# Optimiser
"Optimise mon CLAUDE.md"
"Améliore cette skill"

# Veille
"Quoi de neuf dans Claude Code ?"

# Capitalisation fin de session
/done
```

## Modèles utilisés

- `opus + effort:high` → jugement (devils-advocate, outcomes-grader, responsable-ia)
- `opus + effort:xhigh` → exploration agentique profonde (repo-inspector)
- `sonnet + effort:high` → exécution / création (creators, python-dev)
- `haiku` → tâches rapides

## Mise à jour

La skill `cc-news` vérifie les nouveautés Claude Code et capitalise dans le vault.
L'agent `self-updater` met à jour les skills de référence `cc-*-ref` quand une feature change.
