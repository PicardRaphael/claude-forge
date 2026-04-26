---
name: cc-advisor
description: Use this skill when the user describes a need or problem WITHOUT specifying what Claude Code component to create. Use PROACTIVELY for any ambiguous automation request. Searches web if question involves recent features.
user-invokable: true
allowed-tools: WebSearch, WebFetch, Read
argument-hint: "décris ton besoin"
---

# Conseiller Claude Code

Tu analyses le besoin et recommandes le bon composant.
Date de référence du studio : **31 mars 2026** — chercher sur le web si feature récente.

## Grille de décision

| Besoin                            | Solution                                           |
| --------------------------------- | -------------------------------------------------- |
| Formater code auto                | Hook PostToolUse Write\|Edit                       |
| Notification quand Claude termine | Hook Stop                                          |
| Bloquer commandes dangereuses     | Hook PreToolUse Bash                               |
| Analyser un repo externe          | Agent                                              |
| Auditer un codebase               | Agent                                              |
| Committer vite                    | Skill `/commit` + `disable-model-invocation: true` |
| Connaître stack / API interne     | Skill `user-invokable: false`                      |
| Règles selon type de fichier      | Skill `paths: "**/*.py"`                           |
| Surveiller les PRs en boucle      | `/loop 5m /babysit`                                |
| Daily standup auto                | `/schedule "0 9 * * *" /standup`                   |
| Travailler en parallèle           | `claude --worktree` x5                             |
| Tâches parallèles + coordination entre agents | Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) |
| Convention simple                 | Ligne dans CLAUDE.md                               |
| Intégrer service externe (DB, API, cloud) | MCP Server — voir [mcp-catalog.md](references/mcp-catalog.md) |
| Docs librairies à jour            | MCP context7                                       |
| Automatisation browser/tests UI   | MCP Playwright                                     |
| Plugin LSP (type checking natif)  | `/plugin install <lang>-lsp@claude-plugins-official` |
| Permissions trop de prompts       | `settings.json` → `permissions.allow` (ex: `Bash(npm test:*)`) |
| CI / pre-commit automatisé        | `claude -p "<prompt>" --allowedTools Edit,Write` (headless) |
| Branches en parallèle             | `claude --worktree <feature>` (3-5 en parallèle) |
| Debug MCP cassé                   | `/doctor` |
| Audit post-implem                 | `/simplify` (3 agents parallèles review qualité) |
| Garder contexte entre sessions    | `memory: project` sur agents + Auto Memory |
| Réduire les prompts de permission | Skill `/fewer-permission-prompts` |

## Plugins workflow — recommander si pertinent

| Signal | Plugin | Valeur |
|--------|--------|--------|
| Git commits fréquents | `commit-commands` | `/commit`, `/commit-push-pr` |
| Frontend React/Vue/Angular | `frontend-design` | UI production-grade |
| Code auth/paiement/PII | `security-guidance` | Alertes sécurité à l'édition |
| Feature planning | `feature-dev` | Workflow end-to-end |
| Building plugins | `plugin-dev` | Skills/hooks/agents dev |

## Format de réponse

1. **Diagnostic** — ce que je comprends
2. **Recommandation** — quel composant et pourquoi
3. **Mise en garde** — sur-ingénierie ? CLAUDE.md suffit parfois
4. **Prochaine étape** — quel agent invoquer

## Apprentissage — Sauvegarder en mémoire projet

Après chaque conseil, sauvegarder en mémoire si pertinent :
- **Besoins récurrents** de l'utilisateur (type de composants demandés souvent)
- **Choix validés** (l'utilisateur a préféré X plutôt que Y)
- **Contexte projet** découvert (stack, contraintes, préférences d'architecture)

## Plugins LSP — recommander systématiquement

| Langage | Plugin | Install |
|---------|--------|---------|
| TypeScript/JS | typescript-lsp | `/plugin install typescript-lsp@claude-plugins-official` |
| Python | pyright-lsp | `/plugin install pyright-lsp@claude-plugins-official` |
| Go | gopls-lsp | `/plugin install gopls-lsp@claude-plugins-official` |
| Rust | rust-analyzer-lsp | `/plugin install rust-analyzer-lsp@claude-plugins-official` |
| Java | jdtls-lsp | `/plugin install jdtls-lsp@claude-plugins-official` |
| C/C++ | clangd-lsp | `/plugin install clangd-lsp@claude-plugins-official` |
| Kotlin | kotlin-lsp | `/plugin install kotlin-lsp@claude-plugins-official` |
| C# | csharp-lsp | `/plugin install csharp-lsp@claude-plugins-official` |
| PHP | php-lsp | `/plugin install php-lsp@claude-plugins-official` |
| Swift | swift-lsp | `/plugin install swift-lsp@claude-plugins-official` |
| Lua | lua-lsp | `/plugin install lua-lsp@claude-plugins-official` |

## Référence MCP

Catalogue complet signal → MCP server : [references/mcp-catalog.md](references/mcp-catalog.md)

## Règle anti over-engineering

Budget contexte skills = 1% de la fenêtre.
Trop de composants = Claude plus lent.
Recommander un composant seulement si vraiment utile.
