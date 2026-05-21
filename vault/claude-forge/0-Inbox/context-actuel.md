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


---
## Session 2026-05-21 (suite) — Optimisations TDD + Audit cohérence

### Décisions prises
- Pipeline ia_back passé en test-first : architect (contrats testables) → test-writer red → dev → test-writer refactor → code-reviewer
- Sprint Contract handshake bidirectionnel : test-writer valide les contrats architect AVANT d'écrire les tests (step 0)
- Rules mortes fixées : agents-color-convention + outcomes-after-architect avaient pas de frontmatter description:
- .mcp.json ia_back + settings.local.json (2 repos) untrackés de git
- DA validé : 0 bloquant, 4 avertissements (advisory step 0 OK en v1, migration Drizzle ajoutée en BYPASS)

### Audit cohérence profond
- ia_back : 43 problèmes (4 critiques, 14 warnings) — pattern #1 = skills orphelines (11 agents)
- neo_ia : 24 problèmes (5 critiques, 19 warnings) — même pattern skills orphelines (6 agents)
- Checklist 8 points créée pour réutilisation sur tout repo

### Prochaines étapes
- Batch 3 : corriger skills orphelines dans le body des agents (11 ia_back + 6 neo_ia)
- Tester le pipeline TDD complet en live sur un vrai ticket
- cc-news Tokyo (10 juin) à surveiller
- Mesurer taux de rejet Sprint Contract step 0 sur 30 jours