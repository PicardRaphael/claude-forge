---
name: Convention nommage changelog CC vault
description: Convention exacte des noms de fichiers et wikilinks pour les changelogs Claude Code
type: reference
---

## Convention

Format fichier : `CC v2.1.XXX.md` (avec espaces — "CC espace v2.1.XXX")
Wikilink : `[[CC v2.1.XXX]]`
Dossier : `vault/claude-forge/01-Claude/Code/changelog/`

## Exemples existants (vérifiés 2026-05-10)

- `CC v2.1.129.md`, `CC v2.1.128.md`, `CC v2.1.126.md`, etc.
- Format MOC : `- [[CC v2.1.136]] — description courte (date)`

## Frontmatter standard changelog

```yaml
titre: "Claude Code v2.1.XXX"
resume: "date — features clés en une ligne"
aliases:
  - "CC 2.1.XXX"        # sans "v"
  - "v2.1.XXX"          # sans "CC"
  - "claude code 2.1.XXX"
  - "<feature principale>" # terme mémorable
  - "CC XXX"            # numéro seul
domaine: claude-code
type: changelog
```

**Why:** Uniformité avec les 15+ notes changelog existantes. Les wikilinks cassent si le nom diffère.
