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
dispatch-guard déployé sur ia_back + neo_ia. Enforcement déterministe du pattern CTO (session principale ne code plus directement).

## Dernière session (2026-05-21)
### Décisions prises
- dispatch-guard basé sur agent_type/subagent_type JSON stdin (pas CLAUDE_AGENT env var = dead code)
- Multi-field fallback pour couvrir variations inter-versions CC
- tdd-guard neo_ia refactorisé : glob + remontée parent pour tests aplatis/préfixés
- Dispatch-guard en premier dans la chaîne PreToolUse (avant architect-guard et tdd-guard)

### En cours
- Vérification empirique en live du champ exact injecté par le runtime CC (agent_type vs subagent_type)
- Fix findTestFile ia_back (pattern basique .test.ts colocalisé, suffisant pour l'instant)
- Hook Bash heredoc guard optionnel (fuite cat > file.py contourne dispatch-guard)

### Prochaines étapes
- Lancer un vrai subagent dev qui fait un Write, dumper le JSON stdin pour confirmer le champ runtime
- Tester /outcomes-test sur un vrai livrable dev
- cc-news Tokyo (10 juin) à surveiller

## Fils ouverts
- MCP Tunnels → évaluer pour brain Neoteem quand GA
- Outcomes rubric hook enforcement (rule advisory insuffisante selon vault)
- Bash heredoc guard (fuite documentée, risque faible court terme)
- Exemptions dispatch-guard hardcodées → risque divergence entre les 2 repos
- Template rubric "spec" à créer si on utilise /spec sur les repos projet

## Liens
[[Raphael-Picard]]
[[Claude-Forge]]
[[erreur-claude-agent-env-var-dead-code]]
[[raisonnement-hook-agent-detection-method]]
[[critique-2026-05-21-dispatch-guard-livraison]]
