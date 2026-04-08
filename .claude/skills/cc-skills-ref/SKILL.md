---
name: cc-skills-ref
description: Référence complète du format YAML des skills Claude Code — champs frontmatter, $ARGUMENTS, !backtick, context fork, paths, 9 catégories Thariq, 8 principes, skills builtin. Charger quand on crée ou modifie une skill.
user-invokable: false
---

# Référence — Skills Claude Code (= Commands depuis v2.1.0)

## Format complet

```yaml
---
name: ma-skill # OBLIGATOIRE — kebab-case = nom du dossier
description: Ce que ça fait. Use when [triggers]. # OBLIGATOIRE — UNE SEULE LIGNE
argument-hint: "[fichier ou texte]"
allowed-tools: Read, Bash
when_to_use: Use when the user asks to X
model: sonnet
effort: high # low|medium|high (max supprimé v2.1.91)
user-invokable: true
disable-model-invocation: true # slash command manuelle uniquement
context: fork
agent: Explore
paths: "**/*.py"
version: "1.0.0"
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
          once: true
metadata:
  author: MonEquipe
---
```

## Règles critiques

- Description **UNE SEULE LIGNE en anglais** — jamais `>-` ni `|`
- `name` = nom exact du dossier
- Pas de `README.md` dans le dossier
- SKILL.md < 500 lignes → déporter dans `references/`
- **`commands/` est DÉPRÉCIÉ** → utiliser `skills/` à la place. Les deux marchent mais skills est le standard.
- Skills métier doivent avoir une section **Apprentissage** pour sauvegarder en mémoire
- Skills injectées en ENTIER dans le contexte des subagents → garder courtes
- Plugin skills utilisent le `name` du frontmatter (plus le basename du dossier) depuis v2.1.94
- `disableSkillShellExecution` : setting pour bloquer l'exécution shell dans les skills

## Injection dynamique

### `$ARGUMENTS`

```markdown
Crée un composant nommé $ARGUMENTS.
```

### `!backtick` — injection shell

```markdown
!`git status --short`
!`git diff --cached | head -100`
```

## `user-invokable` vs `disable-model-invocation`

|                      | `user-invokable: false` | `disable-model-invocation: true` |
| -------------------- | ----------------------- | -------------------------------- |
| `/skill` utilisateur | ❌                      | ✅                               |
| Claude charge auto   | ❌                      | ❌                               |
| Usage                | Connaissance pure       | Slash command contrôlée          |

## 9 catégories (Thariq, Anthropic)

1. Library & API Reference
2. Product Verification ← investir 1 semaine dessus
3. Data Fetching & Analysis
4. Business Process
5. Code Scaffolding
6. Code Quality (adversarial-review)
7. CI/CD & Deployment (babysit-pr)
8. Operations
9. Knowledge Base

## 8 principes (Thariq)

1. Ne pas énoncer l'évident
2. **Section Gotchas** ← la plus importante
3. Un skill = un dossier avec scripts/, references/, assets/
4. Laisser de la flexibilité à Claude
5. Config dans `config.json` si setup nécessaire
6. Description = déclencheur pour le modèle
7. Mémoire possible via log, JSON, SQLite
8. Itérer sur un cas difficile → extraire → élargir

## Références (progressive disclosure)

- `references/complete-guide-summary.md` — résumé clé du guide Anthropic (structure, description, 5 patterns, testing, troubleshooting)
- `references/anthropic-skill-patterns.md` — patterns des 17 skills officielles (scripts validation, subagent fresh-eyes, boucle optimisation)
- `references/complete-guide.pdf` — guide complet original (33 pages)

## Skills builtin

`/simplify`, `/batch`, `/debug`, `/loop`, `/voice`, `/btw`, `/branch`, `/compact`

## .claude/rules/ — alternative aux skills pour comportements obligatoires

Les rules (`rules/*.md`) sont chargées automatiquement à chaque session. Utiliser pour :
- Routing agents (qui appeler quand)
- Règles obligatoires (DB, sécurité, conventions)
- Workflows (skill-navigator)

Les skills sont pour les workflows invocables à la demande. Les rules sont toujours actives.
