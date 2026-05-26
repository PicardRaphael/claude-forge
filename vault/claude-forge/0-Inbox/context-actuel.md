---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-26
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Post-refonte tripartite Will/ECC/Boris sur forge + ia_back + neo_ia. Doctrine effort recalibrée Anthropic officiel (xhigh sélectif, calibrage par TYPE de tâche). Agent Teams natif testé empiriquement avec 3 auditors capitalisés cross-repo.

## Dernière session (2026-05-26)

### Décisions prises

- Doctrine effort calibrée portefeuille : xhigh pour exploration multi-tours, high pour comparatif structuré, medium pour mécanique. Anthropic biais tokens illimités questionné systématiquement.
- Forge = setup dev personnel (doctrine ECC), pas projet client (doctrine Will). Justifie 11+ agents et 47 skills.
- Fusions agents (forge 13→11, ia_back 16→13, neo_ia 14→12) : repo-inspector forge, reviewer ia_back, reviewer neo_ia.
- Capitalisation 3 user-scope auditors will/ecc/boris dans `~/.claude/agents/` pour audit tripartite réutilisable cross-repo.
- Migration 3 agents inspection vers Haiku (économie ~5x sur scans répétitifs).
- Contradiction parallélisme neo_ia tranchée verbatim Google/MIT : indépendant OK, séquentiel INTERDIT.

### En cours

- Hook delegate-guard forge patché avec 4 sources bypass (agent_type, agent_id, env, transcript) + debug log — empiriquement validé sur 4 SKILL.md créés par skill-creator.
- 12/12 skills forge nouvelles capitalisées (git-multi-repo, python-script-refactor-masse, auditor-empirical-verify, windows-hooks-cross-machine, da-blocking-arbitrage, arxiv-verification, mcp-brief-then-direct, cross-repo-propagation, methode-pivoter-doctrine, audit-thematique-clusters, web-search-canonical-source, agentshield-like-scanner).
- 8 feedbacks mémoire nouveaux (sonnet effort, biais Anthropic, chaîne archi-dev, cross-repo path, audit tripartite, skills user-scope, routine remote, hook vs harness).
- Note synthèse vault `Knowledge/syntheses/refonte-3-repos-26mai-2026.md` créée comme référence anti-drift.

### Prochaines étapes

- Raphael : rotation token Google Chat ia_back (settings.json:5) + remplacer `Edit(./**)` par scopes explicites
- 5 skills ia_back/neo_ia restantes (postgres-js-migration, agentshield-ia-back, langgraph-debug-pattern, monorepo-tool-dispatch, agentshield-neo-ia)
- Pipeline AgentShield-like forge à construire (skill agentshield-like-scanner existe, dispatch 3 sub-agents Opus à câbler)
- Fusion sections ## Gotchas dupliquées dans CLAUDE.md ia_back + neo_ia (cosmétique)
- Test empirique `repo-inspector` forge sur neoteem-brain ou lojii pour valider les 3 modes (audit/analyze/scan)

## Fils ouverts

- Will Stock Pilot doctrine vs ECC : tension utile entre minimum (client) et maximum (dev personnel). Capturée [[will-vs-ecc-deux-doctrines-anthropic]].
- Agent Teams natif Anthropic : testé empiriquement OK mais skills frontmatter ignorées en teammate → workaround = MCP en clair body. Limitation Anthropic à surveiller dans futures versions.
- Hook delegate-guard : maintenant robuste avec 4 sources bypass + debug log. Pattern reproductible sur autres hooks similaires si besoin.
- Article @sairahul1 X (id 2058832033628241931) : pattern Software Factory 7 agents — communauté valide, mais Will/ECC plus précis sur le cas d'usage. Capturée [[software-factory-pattern-2026]].

## Liens

[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[Knowledge/syntheses/refonte-3-repos-26mai-2026|Synthèse refonte 26 mai]]
[[04-Techniques/claude-code/effort-opus-47-doctrine-anthropic-2026|Effort doctrine Anthropic]]
[[Knowledge/critiques/will-vs-ecc-deux-doctrines-anthropic|Will vs ECC]]
