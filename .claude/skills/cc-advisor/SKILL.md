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

## Format de réponse

1. **Diagnostic** — ce que je comprends
2. **Recommandation** — quel composant et pourquoi
3. **Mise en garde** — sur-ingénierie ? CLAUDE.md suffit parfois
4. **Prochaine étape** — quel agent invoquer

## Règle anti over-engineering

Budget contexte skills = 1% de la fenêtre.
Trop de composants = Claude plus lent.
Recommander un composant seulement si vraiment utile.
