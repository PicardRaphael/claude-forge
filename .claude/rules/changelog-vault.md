---
description: "Update vault CHANGELOG.md after adding or modifying vault/claude-forge/ notes. Required BEFORE commit."
---

<!-- PAS de `paths:` — décision mesurée du 29 juil. 2026, ne pas « optimiser » ce
     fichier en le scopant sur `vault/**`. Le gate ne fire que sur LECTURE d'un
     fichier correspondant (« Path-scoped rules trigger when Claude reads files
     matching the pattern »), or les notes du vault s'écrivent via MCP
     forge-brain (`create_note`/`append_note`/`insert_section`) — aucun Read sur
     `vault/**` n'a lieu. Scoper cette rule la rendrait donc muette exactement
     dans le cas qu'elle existe pour attraper : le CHANGELOG oublié après un
     ajout de notes. Coût de la garder eager : ~298 tokens. -->


# Changelog vault — OBLIGATOIRE après ajout de notes

Quand tu ajoutes ou modifies des notes dans le vault forge-brain (create/update dans vault/claude-forge/), mettre à jour `vault/claude-forge/CHANGELOG.md` AVANT le commit.

## Format

```markdown
## YYYY-MM-DD — [résumé court]

- **Ajoutées** : [notes créées avec dossier]
- **Modifiées** : [notes mises à jour]
- **Leaders** : [fiches ajoutées/modifiées]
- **Source** : [ce qui a motivé les changements]
```

## Quand NE PAS mettre à jour

- Modifications automatiques (.obsidian/workspace.json, etc.)
- Corrections de typos mineures
- Pas de notes vault touchées dans le commit
