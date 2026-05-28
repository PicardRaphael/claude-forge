# claude-forge 🔨

**Assistant personnel Claude Code — Conseiller, Créateur, Optimiseur**

Créé le : 31 mars 2026 · Dernière mise à jour : 2026-05-28

## Ce que c'est

Un studio méta-Claude Code : 10 agents, 48 skills, 12 hooks Python, 9 rules et un vault Obsidian de 438 notes interrogeable par MCP. Il conseille, fabrique de la config Claude Code conforme pour tous tes projets, et capitalise chaque leçon apprise.

Trois axes d'innovation revendiqués (canonique [[3-axes-strategiques-forge]]) : (1) diagnostic et workaround du **MCP décoratif sub-agent** — pattern brief-inline + hook `vault-cat-guard`, cause-racine plausible bug `anthropics/claude-code#60237` ; (2) critère architectural **Agent vs Skill basé densité d'écriture MCP vault** ; (3) **living doctrine** avec gate humain typé INFO/REINFORCE/PIVOT.

Pour la présentation externe (Anthropic, pairs CC, lecteurs sans contexte) → **`OVERVIEW.md`**.
Pour la cartographie technique interne (reprise de contexte rapide) → **`SELF_PORTRAIT.md`**.

## Structure

```
claude-forge/
├── CLAUDE.md                  Contrat Jarvis + doctrine (source d'autorité)
├── OVERVIEW.md                Présentation externe (Anthropic, audience large)
├── SELF_PORTRAIT.md           Photographie technique interne (reprise contexte)
├── .mcp.json                  Déclare le MCP forge-brain (HTTP :8091)
├── install.bat                Setup des prérequis CLI (Windows)
│
├── .claude/
│   ├── settings.json          Permissions + câblage des 12 hooks
│   ├── agents/                10 agents (créateurs, repo-inspector, devils-advocate…)
│   ├── skills/                48 skills (cc-advisor, cc-news, forge-brain, /recap, /done…)
│   ├── hooks/                 12 hooks Python (delegate-guard, security-guard, vault-cat-guard…)
│   ├── rules/                 9 rules de routing + doctrine
│   └── agent-memory/          mémoire par agent (project scope)
│
├── mcp-forge-brain/           Serveur MCP maison (FastMCP + SQLite FTS5, 22 outils)
├── vault/claude-forge/        Le "cerveau" — vault Obsidian (438 notes)
├── ia-lead-neoteem/           Plugin Cowork (7 skills Responsable IA)
└── scripts/                   .bat de tâches planifiées (cc-news, forge-review, vault-audit)
```

### Agents clés (10 forge + 3 user-scope)

- `repo-inspector` — analyse / audit / scan d'un repo (mode=analyze|audit|scan)
- `agent-creator` / `skill-creator` / `hook-creator` / `claudemd-optimizer` — créateurs spécialisés
- `devils-advocate` — critique adversariale avant ship d'un livrable majeur
- `outcomes-grader` — notation RUBRIC.md PASS/FAIL/PARTIAL
- `python-dev` — implémentation Python en TDD (hook inline `py_compile`)
- `self-updater` — détecte les nouveautés CC via `cc-news`, met à jour les skills `cc-*-ref`
- `responsable-ia` — casquette Lead IA Neoteem (CODIR, AI Act, roadmap, Loji)
- `boris-auditor` / `ecc-auditor` / `will-auditor` (user-scope) — audits lentilles externes

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
