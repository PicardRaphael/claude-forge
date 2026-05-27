---
name: skills-user-scope-pas-cross-repo
description: "Skills listées en frontmatter d'un agent user-scope (~/.claude/agents/) ne se résolvent QUE depuis forge où elles existent. Cross-repo = décoratives. Workaround = instructions MCP en clair dans body OU miroir skills dans ~/.claude/skills/."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Découverte 26 mai 2026 lors capitalisation will/ecc/boris-auditor en `~/.claude/agents/` user-scope.

**Why** : un agent user-scope (`~/.claude/agents/will-auditor.md`) avec `skills: [cc-agents-ref, forge-brain]` en frontmatter charge les skills depuis le scope projet UNIQUEMENT. Quand l'agent est invoqué depuis ia_back ou neo_ia (qui n'ont pas ces skills), les skills frontmatter sont silencieusement décoratives.

**Cumul avec gotcha teammate** : skills frontmatter ignorées aussi en teammate Agent Teams (limitation Anthropic documentée). Double pénalité pour les agents cross-repo réutilisables.

**How to apply** :
1. **Workaround par défaut** : mettre les instructions MCP en CLAIR dans le body de l'agent ("Utiliser mcp__forge-brain__read_note(...) SANS max_lines") — fonctionne partout
2. **Workaround structurel** : mirorer skills critiques dans `~/.claude/skills/` (scope user) pour qu'elles soient dispo cross-repo
3. **Anti-pattern** : compter sur skills frontmatter user-scope pour cross-repo
4. **Detection** : si agent user-scope cite skills non présentes dans le repo cible, vérifier que body inclut les instructions équivalentes en clair

**Validation empirique** : will-auditor.md créé avec body Phase B incluant `mcp__forge-brain__read_note` verbatim → fonctionnel cross-repo malgré skills décoratives.

Liens : [[anti-reentrance-sub-agents]], [[delegate-guard-env-var-blocked]]
