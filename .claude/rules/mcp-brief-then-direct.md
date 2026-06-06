---
description: Pattern doctrinal — skills frontmatter ignorées en sub-agent/Agent Teams. Toujours briefe les appels MCP verbatim dans le body du prompt. Workaround pour MCP décoratif.
---

# MCP brief-then-direct — Pattern doctrinal

## Problème

Deux limitations silencieuses du système :
1. **Skills frontmatter ignorées** dans les Agent Teams teammates (limitation Anthropic)
2. **Skills user-scope** (`~/.claude/agents/`) non résolues cross-repo (résolues depuis scope projet uniquement)

Résultat : un sub-agent avec `skills: [forge-brain]` en frontmatter n'a PAS accès au vault MCP.

## Solution : brief verbatim dans le body

**NE PAS** compter sur :
```yaml
skills: [forge-brain, subagent-creator]  # ignoré cross-repo et Agent Teams
```

**FAIRE** : mettre les appels MCP verbatim dans le body de l'agent ou du prompt de dispatch :
```markdown
Pour accéder au vault : utiliser `mcp__forge-brain__read_note(file="nom-note")` SANS max_lines.
Pour chercher : `mcp__forge-brain__search_brain(query="...", limit=10)`.
```

## Dispatch depuis forge (pattern Agent)

```python
Agent(
  subagent_type="...",
  prompt="""
  [tâche]
  
  Accès vault : mcp__forge-brain__read_note(file="comment-creer-skill") SANS max_lines.
  """
)
```

## Agents user-scope cross-repo

Si l'agent est invoqué depuis plusieurs repos (ia_back, neo_ia, etc.) :
- Mettre les instructions MCP EN CLAIR dans le body (Phase B ou section dédiée)
- Les `skills:` frontmatter restent pour documentation mais sont décoratives cross-repo
- Valider : invoquer l'agent depuis un repo qui n'a PAS les skills en question

## Modifier un agent dans un autre repo

```python
Agent(
  subagent_type="subagent-creator",
  prompt="Modifier C:/Users/raphael.picard_neote/Documents/ia_back/.claude/agents/xxx.md..."
)
```

## Gotchas

- **Double pénalité** : skills frontmatter ignorées EN Agent Teams teammates ET user-scope cross-repo — toujours brief in-body
- **Validation empirique obligatoire** : après création agent user-scope, tester depuis un repo sans les skills
- **Self-modification forge bloquée** : subagent-creator ne peut pas modifier ses propres agents forge. Workaround = édition manuelle ou Shift+Tab
- **JAMAIS `$ARGUMENTS` dans backticks shell** : substitution casse le quoting

Source canonique : [[pattern-mcp-brief-then-direct]] vault forge
