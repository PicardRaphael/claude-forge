---
name: obsidian-neo-brain-pattern
description: Pattern reutilisable pour connecter n'importe quel projet au vault neoteem-brain via obsidian CLI wrapper — skill neo-brain, methode de recherche, capitalisation Knowledge
type: reference
---

## Pattern : connecter un projet au vault neoteem-brain

### Principe

Tout projet Neoteem peut interroger le vault Obsidian `neoteem-brain` via le **wrapper CLI** (`bash .claude/skills/neo-brain/scripts/obsidian-cli.sh`). Le wrapper resout `Obsidian.com` (console) au lieu de `Obsidian.exe` (GUI) sur Windows Git Bash. Pas besoin d'`additionalDirectories` — la CLI parle a l'instance Obsidian ouverte.

### Ce qu'il faut creer

**Une skill `neo-brain`** dans `.claude/skills/neo-brain/` du projet cible, avec :
- `SKILL.md` (allowed-tools: Bash)
- `scripts/obsidian-cli.sh` (wrapper Windows)
- `references/obsidian-cli-commands.md`
- `references/knowledge-conventions.md`

**Kit standalone** disponible dans `neoteem-brain/neo-brain/` (copier dans le repo cible).

### Injection dans les agents

Ajouter `neo-brain` dans `skills:` des agents qui touchent au metier ou a la BDD. Ne PAS injecter dans les agents purement techniques (code-reviewer, test-writer, validator, security-auditor, performance-engineer).

### Knowledge First (regle ia_back 2026-04-08)

Les rules imposent : neo-brain AVANT MCP PostgreSQL. Le vault donne le "pourquoi" metier, MCP donne le "quoi" technique.

### Repos connectes (2026-04-08)

| Repo | Date | Agents connectes |
|------|------|-----------------|
| ia_back | 2026-04-07 | 7 (architect, api-designer, dev, refactor-pg-function, schema-mapper, db-inspector, debugger) |

### Points cles

- La CLI utilise l'**index de recherche Obsidian** (pas le filesystem) — 70 000x moins de tokens
- `file=` resout comme un wikilink (nom seul, pas de chemin ni extension)
- Obsidian DOIT etre ouvert — pas de mode headless
- **Toujours** utiliser le wrapper, jamais `obsidian` directement
- kepano/obsidian-skills = les 5 skills officielles (obsidian-cli, obsidian-markdown, obsidian-bases, json-canvas, defuddle)

### Conventions Knowledge

- Frontmatter obligatoire (titre, type, cree, sources, auteur, repo, derniere-maj, tags)
- `repo: <nom-du-projet>` pour tracer l'origine
- Sous-dossiers : questions/ (q-), syntheses/ (s-), explorations/ (e-)
- kebab-case, wikilinks obligatoires, francais sauf noms techniques
