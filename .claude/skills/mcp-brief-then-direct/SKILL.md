---
name: mcp-brief-then-direct
description: "Use when sub-agent needs MCP/skills frontmatter access. Brief sub-agent with explicit mcp__server__tool(args) calls in body (skills frontmatter ignored in Agent Teams teammates, decorative user-scope cross-repo). Workaround documented."
effort: high
---

## Rôle

Garantir qu'un sub-agent ou agent cross-repo dispose des instructions MCP/skills nécessaires, en contournant les deux limitations silencieuses du système :
1. Skills frontmatter ignorées dans les Agent Teams teammates (limitation Anthropic)
2. Skills user-scope (`~/.claude/agents/`) non résolues cross-repo (résolues depuis scope projet uniquement)

## Étapes

### Pattern brief-then-direct

Quand un sub-agent doit appeler un outil MCP ou utiliser une skill :

**NE PAS** compter sur :
```yaml
skills: [forge-brain, subagent-creator]  # ignoré cross-repo et Agent Teams
```

**FAIRE** : mettre les appels MCP verbatim dans le body de l'agent ou du prompt de dispatch :
```markdown
Pour accéder au vault : utiliser `mcp__forge-brain__read_note(file="nom-note")` SANS max_lines.
Pour chercher : `mcp__forge-brain__search_brain(query="...", limit=10)`.
```

### Pour les agents user-scope (`~/.claude/agents/`)

Si l'agent est invoqué depuis plusieurs repos (ia_back, neo_ia, etc.) :
- Mettre les instructions MCP EN CLAIR dans le body (Phase B ou section dédiée)
- Les `skills:` frontmatter peuvent rester pour documentation mais sont décoratives cross-repo
- Valider : invoquer l'agent depuis un repo qui n'a PAS les skills en question

### Pour les sous-agents dispatch depuis forge

```python
Agent(
  subagent_type="...",
  prompt="""
  [tâche]
  
  Accès vault : mcp__forge-brain__read_note(file="comment-creer-skill") SANS max_lines.
  """
)
```

### Pour modifier un agent dans un autre repo

Dispatcher subagent-creator avec path ABSOLU :
```python
Agent(
  subagent_type="subagent-creator",
  prompt="Modifier C:/Users/raphael.picard_neote/Documents/ia_back/.claude/agents/xxx.md..."
)
```
Le classifier bloque self-modification forge → forge, mais autorise cross-repo avec path absolu.

## Gotchas

- **Double pénalité** : skills frontmatter ignorées ET dans Agent Teams teammates ET user-scope cross-repo. Toujours briefe in-body.
- **Validation empirique obligatoire** : après création d'un agent user-scope, tester depuis un repo sans les skills.
- **Self-modification forge bloquée** : subagent-creator ne peut pas modifier ses propres agents forge. Workaround = édition manuelle ou Shift+Tab.
- **JAMAIS `$ARGUMENTS` dans backticks shell** : substitution casse le quoting.

## Apprentissage

- will-auditor.md créé avec `mcp__forge-brain__read_note` verbatim dans body → fonctionnel cross-repo malgré skills décoratives
- 3/4 migrations Haiku cross-repo réussies via path absolu (ia_back, neo_ia) — seule forge→forge a échoué (self-modification)
- Pattern source canonique : [[pattern-mcp-brief-then-direct]] vault forge
