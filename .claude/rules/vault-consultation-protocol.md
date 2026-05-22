# Protocole consultation vault — Single source of truth

Cette rule centralise le protocole de consultation du vault forge-brain pour les agents. Elle est référencée par chaque agent au lieu d'être copiée-collée. Objectif : DRY + facilité de mise à jour.

## Vault check (auto-skip if marker fresh)

Le hook `vault-query-guard` BLOQUE les Write si le vault n'a pas été consulté récemment. Si le prompt d'invocation contient déjà des infos du vault, l'étape est satisfaite automatiquement (marker fresh).

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
| Analyseurs (project-auditor, project-analyzer) | Systématique — référentiel pour juger |
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

Consulter le vault selon `.claude/rules/vault-consultation-protocol.md` (auto-skip if marker fresh).
```
