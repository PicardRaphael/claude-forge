---
titre: "Critique — Roadmap Jarvis 2026-07"
type: knowledge
domaine: claude-code
derniere-maj: 2026-07-07
auteur: claude
aliases:
  - "critique roadmap jarvis 2026-07"
  - "DA roadmap forge juillet"
  - "purge agent-memory bloquant"
  - "rules conditionnelles mismatch"
  - "critique 35 items forge"
tags:
  - "#type/critique"
  - "#domaine/claude-code"
---

# Devils Advocate — Roadmap Jarvis 2026-07 (35 items)

**Intention déclarée :** rendre forge « exceptionnel » via P0 dette + P1/P2 adoption features CC + P2/P3 proactivité/sécurité.

## Verdict
Bloquants : 2 | Avertissements : 5 | Nitpicks : 3. Décision : LIVRER AVEC CORRECTIONS — flipper #7 et #20 avant exécution.

## BLOQUANT 1 — #7 purge agent-memory (score 88, présomption inversée)
`.claude/agent-memory/` n'est PAS un vestige. Preuves décisives : (1) l'agent devils-advocate ACTIF est configuré pour y écrire ; (2) écritures du 27 juin ; (3) exemption `vault-write-guard.py` « Raphael's mandate ». Contient repo-inspector/ (analyses neo_ia+lojii) + devils-advocate/ (feedbacks). 6 composants en dépendent (config-guardian baseline 0=WARN, pivot-check, forge-review, vault-write-guard, methode-pivoter-doctrine, vault-audit) ; seul repo-inspector.md:111 dit « obsolète » = l'outlier. Rationale « agents utilisent memory:project natif » = FAUX doctrinalement (CLAUDE.md : memory dans repo/memory versionné, PAS ~/.claude/projects). Purger = perte mémoire vivante + config-guardian s'alarme contre sa propre baseline. FIX : garder #6 (dé-indexer du vault MCP, hygiène OK), flipper #7 → corriger repo-inspector.md:111. « toute injection résiduelle » = reversal doctrine versionnée, exige arbitrage explicite.

## BLOQUANT 2 — #20 rules conditionnelles (score 82, mécanisme inadapté)
Même en accordant que conditional rules marchent à v2.1.198, les règles choisies sont topic/action-triggered, pas path-triggered. `coaching-lead-ia` fire sur une question management (zéro lecture de fichier ; son job = dire QUELS fichiers lire → no-op circulaire). `changelog-vault` fire sur écriture MCP (pas un Read de path matchant). 3-4 des 5 règles cesseraient silencieusement de charger quand nécessaires = régression de correction déguisée en gain tokens. Le gain réel : ~1% d'un contexte 1M, cacheable — pas le « levier #1 ». FIX : raccourcir les règles, ou ne conditionaliser que les vraies path-scoped.

## AVERTISSEMENTS
- Infra spéculative #21 (Dynamic Workflows, 1000 sous-agents/plan Max non confirmé, pour fan-outs de 4 agents = bazooka), #24 vérité brutale, #25 autonomie graduée, #26 golden-set : aucune incidence forge citée, coût maintenance solo → viole « pas de feature spéculative ». Build on-demand, pas maintenant.
- #12 checkpoint /rewind rangé en Vague 2 APRÈS la chirurgie vault destructive P0 (Vague 1). /rewind existe déjà → l'appliquer PENDANT P0.
- Pas de `<done>` / condition d'arrêt pour une roadmap anti-bloat de 35 items = méta-bloat.
- #15 Notification hook : champs `agent_completed`/`agent_needs_input` non vérifiés (cc-features-ref daté juin s'arrête à v2.1.160).
- Angle mort : le P0 a trouvé 101 wikilinks vault cassés mais raté les réfs mortes `.claude/` (forge-review → skill-creator/MEMORY.md inexistant ; contradiction repo-inspector:111 vs config-guardian). « Info fausse servie » vit aussi dans .claude/.

## NITPICKS
- #29 mcp_tool SessionStart : injecte des notes à CHAQUE session (coût tokens) et redondant avec /recap conservé.
- #23/#24/#28 supposent repos pro + Jira présents sur la machine d'exécution — confirmer.
- #22c sonde injection LLM avant capitalisation : détection prompt-injection par LLM peu fiable = fausse confiance ; garder advisory, pas bloquant.

## CE QUI EST SOLIDE (ne pas y toucher)
- Ordre sécu-avant-autonomie CORRECT : Vague 3 fait #22 en premier, « préalable à toute montée en autonomie ».
- P0 vault (#1-6 hors présomption #7) : dette réelle, evidence-based, à livrer.
- Séparation P0 evidence / P2-P3 spéculatif : structure saine.
