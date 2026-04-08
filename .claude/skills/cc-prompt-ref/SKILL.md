---
name: cc-prompt-ref
description: Best practices for writing agent descriptions, skill triggers, CLAUDE.md rules, and prompts. Use when creating or improving agents, skills, rules, or any prompt that Claude will interpret.
user-invokable: false
---

# Reference — Prompt Engineering pour Claude Code

_Patterns valides de Boris, Thariq, et l'equipe Claude Code_

## Descriptions d'agents — Le champ le plus important

La `description` du frontmatter est ce que Claude utilise pour router les taches vers les agents. Une mauvaise description = agent jamais invoque.

### Pattern obligatoire

```
Use when [TRIGGER]. [Ce que fait l'agent en 1 phrase].
```

### Exemples

```yaml
# BON — trigger clair
description: Use when asked to analyze a code repository or generate technical documentation from source code. Deep-analyzes repos and writes comprehensive docs.

# MAUVAIS — decrit le fonctionnement, pas le trigger
description: Deep-analyzes code repositories and writes comprehensive technical documentation in the Obsidian vault
```

### Checklist description agent

- [ ] Commence par "Use when"
- [ ] Decrit la SITUATION (pas le fonctionnement)
- [ ] En anglais
- [ ] UNE SEULE LIGNE
- [ ] Pas de `>-` ni `|` en YAML

## Descriptions de skills — Quand Claude charge automatiquement

Pour les skills `user-invokable: false`, la description determine si Claude charge la skill dans son contexte.

### Pattern

```
[Ce que la skill couvre]. Use when [situations de declenchement]. Do NOT use for [exclusions].
```

### Exemples

```yaml
# BON — situations + exclusions
description: Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.

# MAUVAIS — trop vague
description: Obsidian Bases skill for creating views
```

## CLAUDE.md — Concis et actionnable

### Principe Boris

> Pour chaque ligne du CLAUDE.md, pose-toi la question : "si je l'enleve, Claude fait des erreurs ?"
> Si non → couper.

### Structure recommandee

```markdown
# Nom du projet

## Role
[1-2 phrases — qui est Claude dans ce projet]

## Stack
[Liste concise]

## Regles critiques
[UNIQUEMENT ce qui cause des erreurs si absent]

## Conventions
[Patterns specifiques au projet]
```

### Anti-patterns

| Anti-pattern | Pourquoi c'est mauvais |
|---|---|
| CLAUDE.md de 500+ lignes | Dilue les regles importantes dans le bruit |
| Copier la doc du framework | Claude connait deja — gaspille du contexte |
| Lister tous les fichiers | Glob/Read font ca mieux |
| Regles evidentes ("ecris du code propre") | Bruit sans signal |

## Rules — Modulaires et conditionnelles

### Quand utiliser rules vs CLAUDE.md

| | CLAUDE.md | Rules |
|---|---|---|
| Charge | Toujours | Toujours (sans globs) ou conditionnellement (avec globs) |
| Usage | Identite du projet, stack, regles globales | Routing agents, conventions par dossier, workflows |
| Taille | Court (50-100 lignes) | Autant que necessaire |

### Pattern rules conditionnelles

```yaml
---
description: TypeScript API conventions for endpoint files
globs: src/api/**/*.ts
---

# Regles specifiques aux endpoints
- Zod schema sur chaque route
- Pas de logique metier dans les handlers
```

→ Charge UNIQUEMENT quand Claude touche un fichier dans `src/api/`

## Prompts pour subagents — Briefer comme un collegue

### Pattern Boris

> Brief the agent like a smart colleague who just walked into the room.
> It hasn't seen this conversation, doesn't know what you've tried.

### Structure prompt subagent

```
1. Ce qu'on veut accomplir (objectif)
2. Ce qu'on sait deja (contexte)
3. Ce qu'on a essaye / elimine
4. Forme attendue de la reponse
```

### Anti-patterns prompts

| Anti-pattern | Fix |
|---|---|
| "Based on your findings, fix the bug" | Decrire le bug, donner fichier + ligne |
| "Implement it" sans contexte | Donner le plan exact |
| Instruction trop prescriptive | Donner l'objectif, laisser l'agent choisir |

## Section Gotchas — La plus importante (Thariq)

Dans chaque skill, la section Gotchas est ce que Claude retient le mieux. Y mettre :

1. Les erreurs que tout le monde fait
2. Les cas limites non evidents
3. Les incompatibilites connues
4. Les "ne JAMAIS faire X"

### Exemple

```markdown
## Gotchas

- `file=` resout comme un wikilink (nom seul), `path=` est le chemin exact — ne pas confondre
- Obsidian doit etre lance — la CLI parle a l'instance ouverte
- Ne JAMAIS appeler `obsidian` directement sur Windows (voir wrapper)
```

## Progressive disclosure (Thariq)

Ne pas tout mettre dans le SKILL.md. Pointer vers des fichiers :

```
SKILL.md (< 500 lignes)
  ├── references/guide-complet.md (detail)
  ├── references/api-reference.md (reference)
  └── scripts/validate.sh (execution)
```

Claude lit le SKILL.md, puis Read les references A LA DEMANDE.

## Hooks vs CLAUDE.md (Boris)

> CLAUDE.md = advisory (~80% compliance). Hooks = deterministe (100%).

| Besoin | Outil |
|--------|-------|
| "Ne jamais importer X dans Y" | Hook PreToolUse exit 2 |
| "Preferer les imports absolus" | CLAUDE.md |
| "Formater apres chaque edit" | Hook PostToolUse |
| "Documenter les fonctions publiques" | CLAUDE.md |

**Regle :** si c'est critique et que la violation cause un bug → hook. Si c'est une preference → CLAUDE.md/rules.

## Verification — Tip #1 Boris

> "Give Claude a way to verify its output."

Toujours inclure dans les skills/agents un moyen de verifier :
- `bun run typecheck` apres ecriture TS
- `ruff check` apres ecriture Python  
- `obsidian search` pour verifier qu'une note existe
- Tests automatiques apres implementation

Sans verification, Claude peut "halluciner" qu'il a bien fait.
