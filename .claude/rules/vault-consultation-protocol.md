---
description: "Centralizes vault forge-brain consultation protocol referenced by agents. MCP tools, format obsidian-markdown, conditional consultation per agent type."
---

# Protocole consultation vault — Single source of truth

Cette rule centralise le protocole de consultation du vault forge-brain pour les agents. Elle est référencée par chaque agent au lieu d'être copiée-collée. Objectif : DRY + facilité de mise à jour.

## Vault check (advisory)

Avant Write/Edit substantiel sur un composant `.claude/` ou une note vault, consulter le vault via MCP forge-brain. Pas d'enforcement par hook : la doctrine 22 mai 2026 réserve les hooks à lint/test/security ([[raisonnement-22mai-doctrine-vs-enforcement]]). Si le prompt d'invocation contient déjà des infos du vault, l'étape est satisfaite.

## Outils MCP à utiliser

- `mcp__forge-brain__search_brain(query="<sujet>", limit=10)` — chercher erreurs passées et best practices
- `mcp__forge-brain__search_brain(query="erreur <topic>", limit=5)` — chercher erreurs passées spécifiques
- `mcp__forge-brain__read_note(file="<nom note>")` — lire une note trouvée
- `mcp__forge-brain__update_property(file="<note>", name="derniere-maj", value="YYYY-MM-DD")` — après modification

Lire les résultats pertinents. Appliquer les leçons aux modifications en cours.

## Format d'écriture vault

Quand tu crées ou modifies des notes dans le vault, utiliser la skill **obsidian-markdown** pour la syntaxe Obsidian (wikilinks `[[Note]]`, callouts, properties/frontmatter).

## Quand consulter — par type d'agent

| Type d'agent | Vault |
|---|---|
| Créateurs (skill/agent/hook/claudemd) | Systématique au démarrage — best practices vivent dans le vault |
| Analyseurs (repo-inspector tous modes) | Systématique — référentiel pour juger |
| Exécutants (python-dev, self-updater) | Si sujet nouveau ou doute sur prior art |
| devils-advocate | Voir son propre prompt (conditionnel ciblé, max 2 requêtes) |

## Anti-patterns

- Scanner le vault par réflexe sans en avoir besoin → perte de temps, pollution contexte
- Skipper le vault sur un créateur "parce que la tâche paraît simple" → régression qualité silencieuse
- Bash heredoc pour écrire des notes vault → boucle Windows quoting (cf bug DA 22 mai 2026)

## Référence dans les agents

Chaque agent référence ce protocole en 2 lignes au lieu de copier-coller 20 lignes :

```markdown
## Vault check

Consulter le vault selon `.claude/rules/vault-consultation-protocol.md` (advisory, pas de hook bloquant).
```
