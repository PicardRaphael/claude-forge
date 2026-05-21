---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-21
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle
Les 2 repos (neo_ia + ia_back) sont à 100% conformité Boris/Thariq/Karpathy. Pipeline TDD test-first, Sprint Contract, 67 problèmes corrigés, blueprint vault complet.

## Dernière session (2026-05-21)
### Décisions prises
- Pipeline TDD test-first sur les 2 repos : architect (contrats testables) → test-writer RED → dev → test-writer REFACTOR → code-reviewer
- Sprint Contract bidirectionnel : test-writer valide contrats architect AVANT d'écrire les tests
- 21 agents corrigés (skills orphelines → instructions body)
- 5 rules créées/fixées (frontmatter, learn-from-mistakes)
- Credentials sortis du git (.mcp.json, settings.local.json)
- Note vault pattern-agentic-engineering = guide canonique tous cas d'usage
- Préférence : analyse-first (pas questionnaire) pour setup repos

### En cours
- Mesurer taux de rejet Sprint Contract step 0 sur 30 jours
- Tester pipeline TDD en live sur un vrai ticket

### Prochaines étapes
- Tester le blueprint sur un repo vierge (lojii-front = bon candidat)
- cc-news Tokyo (10 juin) à surveiller

## Fils ouverts
- MCP Tunnels → évaluer pour brain Neoteem quand GA
- Bash heredoc guard (fuite documentée, risque faible court terme)
- Rotation mot de passe PG Cloud SQL ia_back (dans historique git)
- Batch cosmétique restant : pipeline-reset orphelin (référence dans /go, pas un hook)

## Liens
[[Raphael-Picard]]
[[Claude-Forge]]
[[pattern-agentic-engineering]]
[[synthese-audit-coherence-neo-ia-ia-back]]
[[critique-2026-05-21-tdd-optimizations-handshake]]