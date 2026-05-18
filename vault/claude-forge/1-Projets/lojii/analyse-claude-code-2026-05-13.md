---
titre: "Analyse Claude Code — Lojii (2026-05-13)"
resume: "Recommandations agents, skills, hooks, rules et CLAUDE.md pour le projet lojii Vue 3 / Vuetify 3"
aliases:
  - analyse lojii claude code
  - recommandations lojii
  - setup claude code lojii
type: analyse
derniere-maj: 2026-05-13
auteur: claude
tags:
  - "#type/analyse"
  - "#projet/lojii"
  - "#outil/claude-code"
---

## Recommandations Claude Code pour [[lojii]]

### Agents recommandés

| Agent | Modèle | Rôle | Priorité |
|-------|--------|------|----------|
| `vue-dev` | opus, xhigh | Dev Vue 3 spécialisé lojii (conventions, API, _bibliotheque) | P1 |
| `code-reviewer` | opus, high | Review Vue/Vuetify, vérifie Composition API + conventions | P1 |
| `options-api-migrator` | opus, xhigh | Migration Options API → Composition API (258 fichiers) | P2 |
| `ticket-resolver` | opus, xhigh | Réalise un ticket Jira dans le contexte lojii | P2 |
| `design-fixer` | opus, high | Correction design pixel-perfect Vuetify | P3 |

### Skills recommandées

| Skill | Type | Rôle |
|-------|------|------|
| `lojii-conventions` | auto-trigger | Stack, API pattern, conventions, _bibliotheque, gotchas |
| `lojii-pinia-patterns` | invocable | Templates stores Pinia, migration legacy store |
| `lojii-migrate-options` | invocable | Guide migration Options API → Composition API |

### Rules recommandées

| Rule | Scope | Contenu |
|------|-------|---------|
| `vue-conventions.md` | `src/**/*.vue` | Composition API obligatoire, _bibliotheque, rem, scoped SCSS |
| `quality-gates.md` | global | Pipeline dev → review → test |
| `api-patterns.md` | `src/**/*.js` | neoteem.query, gestion erreurs, auth |

### Hooks recommandés

| Hook | Event | Action |
|------|-------|--------|
| format-and-lint | PostToolUse Write/Edit | Prettier + ESLint sur fichiers modifiés |
| protect-env | PreToolUse | Bloquer édits .env.* (exit 2) |

### CLAUDE.md — Plan de nettoyage

1. Réduire de 330L à ~100L
2. Supprimer références aux composants fantômes (skills, agents, commands inexistants)
3. Déporter détails modules/patterns dans `rules/`
4. Garder : stack, dev commands, conventions nommage, gotchas critiques

### Corrections immédiates

1. Supprimer `eslint.config.mjs` (garder `.js`)
2. Corriger `Bash(find:*)` → `Bash(find *)` dans settings.local.json
3. Décider : `.claude/` dans `.gitignore` ou non
