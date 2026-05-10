---
titre: "update_property yaml.dump corrompt le frontmatter"
resume: "yaml.dump() round-trippe tout le YAML — reordonne les cles, re-quote les dates, wrappe les resumes, detruit les commentaires"
aliases:
  - "erreur yaml dump"
  - "yaml corruption frontmatter"
  - "update_property bug"
  - "yaml round-trip corruption"
type: erreur
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/erreur"
  - "#erreur/infra"
  - "#domaine/claude-code"
---

## Ce qui s est passe

`update_property` dans `brain.py` utilisait `yaml.safe_load()` + `yaml.dump()` pour modifier une seule propriete. Le round-trip complet corrompait silencieusement le frontmatter :
- Cles reordonnees alphabetiquement
- Dates re-quotees (`2026-05-10` → `'2026-05-10'`)
- Resumes longs wrappes sur 2 lignes
- Commentaires YAML detruits

## Pourquoi c etait une erreur

Modifier 1 propriete ne devrait pas toucher les autres. Le round-trip YAML est un anti-pattern connu — PyYAML ne preserve pas l'ordre ni le style.

## Fix

Remplace par regex ciblee : cherche `^{name}:.*$` et remplace la ligne. Si la propriete n existe pas, l ajoute a la fin du frontmatter. Zero impact sur les autres proprietes.

## Alternative consideree

`ruamel.yaml` preserve l'ordre et le style, mais ajoute une dependance externe. La regex suffit pour les cas simples (proprietes scalaires).

## Liens

- [[critique-2026-05-10-mcp-forge-brain]]
- [[sqlite-fts5-vault]]
