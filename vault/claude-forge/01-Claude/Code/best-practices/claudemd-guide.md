---
titre: "Guide CLAUDE.md — Taille, contenu, maintenance"
resume: "Guide CLAUDE.md officiel — limite 200 lignes, hierarchie de chargement, @import, comportement compaction, nature advisory et pattern compounding"
aliases:
  - "claudemd guide"
  - "guide CLAUDE.md"
  - "CLAUDE.md best practices"
  - "taille CLAUDE.md"
  - "CLAUDE.md optimisation"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://code.claude.com/docs/en/best-practices"
  - "https://code.claude.com/docs/en/memory"
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Taille et contenu

### Officiel : < 200 lignes par fichier

Chaque ligne est un cout recurrent en tokens. Le test de Boris :

> **"Would removing this line cause Claude to make mistakes? If not, remove it."**

Inclure UNIQUEMENT :
- Regles qui corrigent des erreurs recurrentes (compounding)
- Gotchas du projet (pieges specifiques)
- Conventions non-evidentes

NE PAS inclure :
- Documentation / architecture (Claude peut lire le code)
- Standards de codage que Claude connait deja
- Erreurs one-shot (→ Auto Memory)

### Signal Lydia Hallie (docs officielles)

> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

> "If Claude asks questions answered in CLAUDE.md, the phrasing might be ambiguous."

### Quand convertir en skill

> "Create a skill when a section of CLAUDE.md has grown into a procedure rather than a fact."

CLAUDE.md = conventions (faits). Skills = domain knowledge (procedures chargees a la demande).

## Loading order (du plus large au plus specifique)

1. **Managed policy** (`/Library/Application Support/ClaudeCode/CLAUDE.md` ou Windows equivalent)
2. **User instructions** (`~/.claude/CLAUDE.md`)
3. **Project instructions** (`./CLAUDE.md` ou `./.claude/CLAUDE.md`)
4. **Local instructions** (`./CLAUDE.local.md`)

Chaque niveau s'ajoute au precedent. Le plus specifique gagne en cas de conflit.

## @import syntax

`@path/to/file` n'importe ou dans CLAUDE.md. Chemins relatifs resolus depuis le fichier importeur. Max 5 niveaux de recursion. Les commentaires HTML sont supprimes du contexte.

Compatible cross-tools : `@AGENTS.md` pour compatibilite avec Cursor, Windsurf, etc.

## Rules (.claude/rules/)

Fichiers `.md` dans `.claude/rules/`, decouverts recursivement. Supportent le frontmatter YAML avec `paths` pour le scoping :

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# Regles API
```

Rules sans `paths` = chargees inconditionnellement au demarrage.

**Les rules sont advisory** — aucun mecanisme d'enforcement. Claude peut les lire et quand meme les violer. Si une regle doit etre appliquee sans exception → hook.

## Comportement compaction

- CLAUDE.md racine du projet **survit** a la compaction (re-lu depuis le disque)
- CLAUDE.md imbriques dans les sous-dossiers **NE sont PAS re-injectes** automatiquement
- `/compact "garder le plan"` — proactif a 70% du contexte (Boris)
- `/clear` entre taches non liees > compacter du contexte irrelevant

## Compounding (pattern Boris + Karpathy)

Apres chaque erreur :
1. Ajouter au CLAUDE.md pour ne pas refaire
2. Si l'erreur est technique → vault `Knowledge/erreurs/`
3. Si l'erreur est comportementale → CLAUDE.md gotchas

Le CLAUDE.md **evolue** — auditer regulierement, supprimer le redondant.

## Nature advisory

> "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself."

Pas de garantie d'enforcement. Pour l'enforcement → [[hooks-guide]].

Utiliser l'emphase ("IMPORTANT", "YOU MUST") pour ameliorer l'adherence aux regles critiques — mais meme avec emphase, reste advisory.

## Liens

- [[hooks-guide]] — Quand les rules ne suffisent pas
- [[skills-guide]] — Quand CLAUDE.md devient trop long
- [[context-management]] — Compaction et gestion du contexte
- [[claudemd-maintenance]] — Pattern de maintenance
- [[Boris Cherny]] — ~100 lignes, litmus test
