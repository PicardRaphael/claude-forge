---
name: project-lojii-skills-created
description: 8 skills lojii créées 2026-05-13 pour frontend Vue 3.5/Vuetify 3.7/Pinia/Vite 6 — pattern paths: pour auto-trigger, references/ pour index externe neoteem-brain
metadata:
  type: project
---

8 skills créées dans `C:/Users/raphael.picard_neote/Documents/neofront/lojii/.claude/skills/` le 2026-05-13.

**Why:** Premier setup Claude Code sur lojii (634 composants Vue 3, 914 écrans WinDev à migrer, 51 apps Vue 2).

**How to apply:** Pattern réutilisable pour des projets frontend avec vault externe.

## Skills créées

| Skill | Type | Trigger |
|-------|------|---------|
| `lojii-conventions` | auto (paths) | `src/**/*.{vue,js,scss}` |
| `lojii-design-system` | auto (paths) | `src/**/*.{vue,scss,css}` |
| `lojii-windev-mapping` | slash `/windev-map` | user-invocable + disable-model-invocation |
| `lojii-vue2-mapping` | slash `/vue2-map` | user-invocable + disable-model-invocation |
| `go` | slash `/go` | user-invocable + disable-model-invocation |
| `spec` | slash `/spec` | user-invocable + disable-model-invocation |
| `lojii-testing` | auto (paths) | `src/**/*.test.js`, `src/**/*.spec.js`, `tests/**`, `e2e/**`, `vitest.config.*`, `playwright.config.*` |
| `recap` | slash `/recap` | user-invocable + disable-model-invocation |

## Patterns appris

- **Vault externe = chemins absolus dans SKILL.md** : quand le vault est dans un autre repo (neoteem-brain), documenter le chemin absolu `C:/Users/.../neoteem-brain/` directement dans la skill. Pas de MCP disponible dans un repo projet.
- **references/ pour index externe** : `lojii-windev-mapping/references/windev-notes-index.md` construit dynamiquement depuis `os.listdir()` au moment de la création — pattern reproductible.
- **skills: frontmatter dans go/spec** : référencer `lojii-conventions` et `lojii-design-system` pour injecter le contexte dans les slash commands.
- **paths: auto-trigger** ne nécessite PAS `user-invocable: false` explicitement — mais le mettre clarifie l'intention.
- **paths: YAML array** pour lojii-testing (multi-patterns), string unique pour lojii-conventions — les deux sont valides.
- **recap + skills: [lojii-conventions]** — slash command qui injecte automatiquement les conventions dans son contexte via frontmatter skills:.
- **!backtick avec chemin absolu -C** dans recap pour éviter les surprises de cwd (`git -C "C:/..." status --short`).
