---
name: cc-skills-ref
description: ALWAYS load this reference when creating or modifying a Claude Code skill. Covers YAML frontmatter, $ARGUMENTS, !backtick, context fork, paths, 9 Thariq categories, 9 principles, builtin skills. Do NOT create skills without loading this first.
user-invocable: false
---

# Référence — Skills Claude Code (= Commands depuis v2.1.0)

**Mis à jour : 14 mai 2026**

## Format complet

```yaml
---
name: ma-skill # OBLIGATOIRE — kebab-case = nom du dossier
description: Ce que ça fait. Use when [triggers]. # OBLIGATOIRE — UNE SEULE LIGNE
argument-hint: "[fichier ou texte]"
allowed-tools: Read, Bash
when_to_use: Use when the user asks to X
model: sonnet
effort: high # low|medium|high|xhigh|max
user-invocable: true
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
shell: bash # bash (défaut) ou powershell pour les blocs !command
settings:
  skillOverrides:
    ma-skill: off # on | name-only | user-invocable-only | off — surcharge sans toucher SKILL.md
---
```

## Règles critiques

- Description **UNE SEULE LIGNE en anglais** — jamais `>-` ni `|`
- `name` = nom exact du dossier
- Pas de `README.md` dans le dossier
- SKILL.md < 500 lignes → déporter dans `references/`
- **`commands/` est DÉPRÉCIÉ** → utiliser `skills/` à la place. Les deux marchent mais skills est le standard.
- Skills métier doivent avoir une section **Apprentissage** pour sauvegarder en mémoire
- Skills métier doivent intégrer des **méthodes** (le comment bien faire) dans chaque étape, pas seulement les gotchas
- Skills injectées en ENTIER dans le contexte des subagents → garder courtes
- Plugin skills utilisent le `name` du frontmatter (plus le basename du dossier) depuis v2.1.94
- `disableSkillShellExecution` : setting pour bloquer l'exécution shell dans les skills

## Description — activation et limites

- `description` + `when_to_use` combinés sont **tronqués à 1 536 caractères** dans le skill listing
- `description` seul : **max 1 024 caractères**
- **Formule directive** : "ALWAYS invoke when [trigger]. DO NOT [action concurrente] without invoking first."
- **73 % des skills communautaires** avec une description passive ne s'activent jamais (audit 214 skills)
- Écrire en 3e personne : "Processes X and generates Y" — pas "I can..." ni "You should..."

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

## `user-invocable` vs `disable-model-invocation`

|                      | `user-invocable: false` | `disable-model-invocation: true` |
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

## 9 principes (Thariq)

1. Ne pas énoncer l'évident
2. **Section Gotchas** ← la plus importante
3. Un skill = un dossier avec scripts/, references/, assets/
4. Laisser de la flexibilité à Claude
5. Config dans `config.json` si setup nécessaire
6. Description = déclencheur pour le modèle
7. Mémoire possible via log, JSON, SQLite
8. Itérer sur un cas difficile → extraire → élargir
9. **Méthodes intégrées** — chaque étape inclut le "comment bien faire", pas juste le "quoi faire"

## Références (progressive disclosure)

- `references/complete-guide-summary.md` — résumé clé du guide Anthropic (structure, description, 5 patterns, testing, troubleshooting)
- `references/anthropic-skill-patterns.md` — patterns des 17 skills officielles (scripts validation, subagent fresh-eyes, boucle optimisation)
- `references/complete-guide.pdf` — guide complet original (33 pages)

## Best practices Anthropic officielles (platform.claude.com)

- **Description en 3eme personne** : "Processes Excel files and generates reports" — pas "I can..." ni "You can..."
- **Include trigger conditions** : "Use when working with PDF files or when the user mentions PDFs"
- **Feedback loops** : run validator → fix → repeat. Pattern plan-validate-execute
- **Checklist pattern** pour workflows complexes : Claude copie et coche
- **Avoid deeply nested references** : max 1 niveau depuis SKILL.md
- **Fichiers longs (>100 lignes)** : table des matieres en haut
- **Tester avec haiku, sonnet ET opus** — ce qui marche sur opus peut manquer de detail pour haiku
- **Naming : gerund form** prefere (processing-pdfs) ou action-oriented (process-pdfs)
- **Avoid time-sensitive info** — "old patterns" section si deprecation
- **MCP tools : fully qualified names** (ServerName:tool_name)
- **Process methods** : skills should include HOW to do each step well, not just list steps — synthesize best practices into the workflow

## Budget et performance

- `skillListingBudgetFraction` (setting) : fraction du context window allouée au listing des skills (défaut 1 %)
- `/doctor` : diagnostique un dépassement de budget skill
- Après auto-compaction : CC ré-attache jusqu'à **5 000 tokens par skill**, max **25 000 combinés**
- Skills plus anciennes dans la session peuvent être **complètement abandonnées** après compaction → garder SKILL.md court

## Skills builtin

`/simplify`, `/batch`, `/debug`, `/loop`, `/voice`, `/btw`, `/branch`, `/compact`

## .claude/rules/ — alternative aux skills pour comportements obligatoires

Les rules (`rules/*.md`) sont chargées automatiquement à chaque session. Utiliser pour :
- Routing agents (qui appeler quand)
- Règles obligatoires (DB, sécurité, conventions)
- Workflows (skill-navigator)

Les skills sont pour les workflows invocables à la demande. Les rules sont toujours actives.

## Vault

[[comment-creer-skill]], [[cowork-skills-reliability]] — diagnostic activation et fiabilité
