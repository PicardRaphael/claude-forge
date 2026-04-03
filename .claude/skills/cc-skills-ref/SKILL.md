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
effort: high # low|medium|high|max
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

- Description **UNE SEULE LIGNE** — jamais `>-` ni `|`
- `name` = nom exact du dossier
- Pas de `README.md` dans le dossier
- SKILL.md < 500 lignes → reste dans `references/`

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

## Référence complète

Pour les cas complexes, consulter `references/complete-guide.pdf`

## Skills builtin

`/simplify`, `/batch`, `/debug`, `/loop`, `/voice`
