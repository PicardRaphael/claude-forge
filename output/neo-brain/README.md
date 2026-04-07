# neo-brain — Installation

Skill generique pour connecter n'importe quel repo Neoteem au vault `neoteem-brain` via la CLI Obsidian.

## Prerequis

1. **Obsidian** installe et ouvert avec le vault `neoteem-brain`
2. **CLI Obsidian** (kepano) dans le PATH : `npm install -g obsidian-cli`
3. Le vault `neoteem-brain` doit etre synchronise (git pull)

## Installation

Copier le dossier `neo-brain/` dans `.claude/skills/` du repo cible :

```
mon-repo/
  .claude/
    skills/
      neo-brain/
        SKILL.md
        references/
          obsidian-cli-commands.md
          knowledge-conventions.md
```

## Configuration selon le repo

### Cas 1 : Repo avec agents (.claude/agents/)

Ajouter `neo-brain` dans le `skills:` des agents qui touchent au metier ou a la BDD :

```yaml
---
name: mon-agent
skills:
  - neo-brain
---
```

**Ne PAS injecter** dans les agents purement techniques (test-writer, code-reviewer, validator, security-auditor).

### Cas 2 : Repo sans agents (CLAUDE.md uniquement)

Ajouter cette section dans le `CLAUDE.md` du repo :

```markdown
## Base de connaissances

Le vault Obsidian `neoteem-brain` contient la documentation metier, BDD, et decisions archi.
Utiliser la skill `neo-brain` quand tu as besoin de contexte metier avant de coder.

Protocole :
1. Avant toute modification touchant au metier ou a la BDD → consulter le brain
2. Si tu decouvres une regle metier non documentee → capitaliser dans Knowledge/
3. Mettre `repo: NOM-DU-REPO` dans le frontmatter des notes creees
```

Remplacer `NOM-DU-REPO` par le nom reel du repo.

### Permissions Bash

Si le repo a des permissions restrictives dans `.claude/settings.json`, autoriser la CLI :

```json
{
  "permissions": {
    "allow": [
      "Bash(obsidian vault=\"neoteem-brain\" *)"
    ]
  }
}
```

## Verification

Tester que la connexion fonctionne :

```bash
obsidian vault="neoteem-brain" search query="test" limit=3
```

Si erreur "vault not found" → ouvrir Obsidian avec le vault `neoteem-brain`.

## Repos deja connectes

| Repo | Date | Methode |
|---|---|---|
| `back2.0` | 2026-04-07 | agents (7 agents connectes) |

Mettre a jour ce tableau quand un nouveau repo est connecte.
