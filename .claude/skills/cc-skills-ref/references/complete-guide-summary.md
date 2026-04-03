# Complete Guide to Building Skills — Résumé clé

Source : complete-guide.pdf (33 pages, Anthropic)

## Structure d'une skill

```
skill-name/
├── SKILL.md              # OBLIGATOIRE — instructions principales
├── scripts/              # Optionnel — code exécutable (Python, Bash)
├── references/           # Optionnel — documentation chargée à la demande
└── assets/              # Optionnel — templates, fonts, icons
```

## Progressive Disclosure (3 niveaux)

1. **YAML frontmatter** → toujours chargé dans le system prompt (description = déclencheur)
2. **SKILL.md body** → chargé quand Claude pense que c'est pertinent
3. **Fichiers liés** (references/, scripts/) → Claude navigue et découvre à la demande

## Description — la partie la plus importante

Structure : `[Ce que ça fait] + [Quand l'utiliser] + [Capabilities clés]`

```yaml
# BON — spécifique et actionnable
description: Manages Linear project workflows including sprint planning,
  task creation, and status tracking. Use when user mentions "sprint",
  "Linear tasks", "project planning", or asks to "create tickets".

# MAUVAIS — trop vague
description: Helps with projects.

# MAUVAIS — pas de triggers
description: Creates sophisticated multi-page documentation systems.
```

- Sous 1024 caractères
- Pas de XML tags (< >)
- Pas "claude" ou "anthropic" dans le name
- Inclure des phrases déclencheurs que l'utilisateur dirait
- Être "pushy" — encourager activement le triggering

## 3 Catégories de skills (Anthropic)

1. **Document & Asset Creation** — créer des outputs cohérents (docs, présentations, code)
2. **Workflow Automation** — processus multi-étapes avec méthodologie consistante
3. **MCP Enhancement** — guide de workflow sur un MCP existant

## 5 Patterns validés

1. **Sequential Workflow Orchestration** — étapes dans un ordre précis avec dépendances
2. **Multi-MCP Coordination** — workflows qui span plusieurs services
3. **Iterative Refinement** — draft → quality check → refinement loop → finalization
4. **Context-Aware Tool Selection** — même outcome, outils différents selon le contexte
5. **Domain-Specific Intelligence** — connaissance métier au-delà de l'accès outils

## Testing — 3 niveaux

1. **Triggering tests** — la skill se charge au bon moment ? (positifs ET négatifs)
2. **Functional tests** — outputs corrects, API OK, edge cases couverts
3. **Performance comparison** — avant/après (tokens, messages, erreurs API)

Tip : itérer sur UNE SEULE tâche difficile jusqu'au succès, puis extraire dans une skill.

## Métriques de succès

- Trigger sur 90% des requêtes pertinentes
- Complete le workflow en X tool calls
- 0 appels API échoués par workflow
- L'utilisateur n'a pas besoin de guider les étapes suivantes

## Troubleshooting courant

| Problème | Cause | Solution |
|----------|-------|---------|
| Skill ne trigger pas | Description trop vague | Ajouter des trigger phrases spécifiques |
| Skill trigger trop | Description trop large | Ajouter des triggers négatifs ("Do NOT use for...") |
| Instructions pas suivies | Trop verbeux ou ambigu | Concis, bullet points, scripts déterministes |
| Contexte lent | SKILL.md trop gros | Progressive disclosure : max 5000 mots, reste en references/ |
| MCP fail | Noms d'outils incorrects | Vérifier la doc MCP, noms case-sensitive |

## Technique avancée — Scripts > instructions

> "For critical validations, consider bundling a script that performs the checks
> programmatically rather than relying on language instructions.
> Code is deterministic; language interpretation isn't."

## Distribution

- GitHub public avec README (hors du dossier skill)
- Plugin marketplace Anthropic (`/plugin marketplace add`)
- `/v1/skills` API endpoint pour usage programmatique
- Skills = standard ouvert, portable cross-outils (Claude, Cursor, Gemini CLI, Codex)
