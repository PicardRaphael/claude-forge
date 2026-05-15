---
titre: "Index — Erreurs documentees"
resume: "Dossier d'index pour les erreurs significatives documentees. Capture les patterns a eviter, bugs rencontres et lecons apprises."
aliases:
  - "erreurs index"
  - "index erreurs"
  - "erreurs documentees vault"
  - "erreurs techniques"
type: index
domaine: technique
derniere-maj: 2026-05-15
auteur: claude
tags:
  - "#type/index"
  - "#type/erreur"
---

## Description

Ce dossier contient les erreurs significatives documentees — bugs, mauvaises pratiques et patterns a eviter, decouverts en production.

## Quand creer une note ici

- Erreur significative commise et comprise
- Pattern dangereux identifie (a eviter)
- Bug subtil avec workaround documente

## Format des notes

Template : `Templates/knowledge.md`

## Navigation

- [[MOC-Techniques]] — index des techniques
- [[Knowledge/questions/_index]] — questions resolues (quand une erreur devient une FAQ)

## Notes

- [[e-descriptions-keyword-stuffing]] — Keyword stuffing dans les descriptions YAML
- [[erreur-advisory-rules-insuffisantes]] — Rules advisory ignorées ~20% du temps
- [[erreur-auto-mode-classifier-self-modification]] — Subagent auto-mode qui tente d'éditer ses propres skills
- [[erreur-da-heredoc-bash-silencieux]] — DA utilisant bash heredoc au lieu de MCP create_note
- [[erreur-devils-advocate-tronque]] — Résultat DA tronqué annoncé comme "validé"
- [[erreur-edit-direct-skills]] — Édits directs sans passer par agents spécialisés
- [[erreur-hooks-bash-quoting-windows]] — Quoting bash cassé sur Windows
- [[erreur-marker-ttl-blocage-agents]] — TTL sur markers = blocage agents
- [[erreur-mcp-stopwords-semantiques]] — Stop words filtrant les queries d'intention
- [[erreur-mcp-yaml-dump-corruption]] — yaml.dump corrompt le frontmatter
- [[erreur-settings-paths-hardcodes-multi-poste]] — Chemins durs cassant la portabilité
- [[erreur-skill-monolithique-sans-references]] — Skill > 500L sans references/
- [[erreur-skip-checklist-skill-modification]] — Skip checklist lors de modification de skill

## Liens

