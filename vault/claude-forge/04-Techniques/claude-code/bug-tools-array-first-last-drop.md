---
titre: "Bug #60237 — Sub-agent tools: array drop first/last position au spawn"
resume: "Issue GitHub anthropics/claude-code#60237 (closed) : positions 1 et N du tools: array frontmatter sub-agent silencieusement droppées au spawn. Cause-racine plausible du symptôme MCP décoratif observé forge."
aliases:
  - "bug 60237"
  - "tools array first last drop"
  - "frontmatter sub-agent tools drop"
  - "MCP décoratif cause-racine plausible"
  - "padder tools array workaround"
type: technique
derniere-maj: 2026-05-28
auteur: claude
sources:
  - "https://github.com/anthropics/claude-code/issues/60237 (closed)"
  - "[[pattern-mcp-brief-then-direct]] AJOUT 27 mai (symptôme observé)"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
  - "#domaine/mcp"
---

# Bug #60237 — Sub-agent `tools:` array drop first/last position

## Description verbatim issue

**Titre** : *"[BUG] Sub-agent frontmatter `tools:` array silently drops first and last positions at spawn time"*

**Statut** : Closed

**Comportement** : Lors du spawn d'un sub-agent via le système de plugins Claude Code, les outils déclarés en **première et dernière position** du tableau `tools:` dans le frontmatter YAML sont silencieusement supprimés du runtime. Seuls les outils en positions intermédiaires survivent.

Exemple : `tools: [Read, Write, Bash]` → seul `Write` accessible à l'exécution. `Read` et `Bash` retournent `Error: No such tool available: <Tool>. <Tool> exists but is not enabled in this context.`

**Workaround documenté** : padder le tableau avec des outils jetables aux positions 1 et N pour que les vrais outils occupent les positions intermédiaires. Ex : `tools: [Glob, Read, Write, Bash, Grep]` au lieu de `tools: [Read, Write, Bash]`.

## Lien avec le symptôme MCP décoratif observé forge

Cause-racine **plausible** du symptôme [[pattern-mcp-brief-then-direct]] (AJOUT 27 mai) : *"le `mcp__server__*` listé dans le `tools:` d'un sub-agent est décoratif. Le serveur MCP n'est PAS connecté dans le contexte d'exécution"*.

Corrélation forte mais pas démontrée :
- Sur tous les sub-agents forge où le symptôme a été observé, `mcp__forge-brain__*` est en **position 1** du `tools:` array
- Le bug #60237 documente le drop position 1
- Donc l'effet observé (MCP introuvable au runtime) = cohérent avec un drop position 1 silencieux

## Repro formel à faire

- Créer 2 sub-agents identiques sauf position du `mcp__forge-brain__*` dans `tools:` (position 1 vs position 3 par padding)
- Mesurer la disponibilité de l'outil au runtime via probe `mcp__forge-brain__search_brain(query="test")`
- Si position 3 fonctionne et position 1 retourne `No such tool available` → bug #60237 confirmé comme cause-racine

Tant que ce repro n'est pas fait, le rattachement reste plausible mais pas démontré.

## Wikilinks

- [[pattern-mcp-brief-then-direct]] — symptôme observé empiriquement
- [[anti-reentrance-sub-agents-pattern-escalade]] — pattern jumeau (limitation contextuelle sub-agent)
- [[3-axes-strategiques-forge]] — axe 1 (MCP décoratif sub-agent)
