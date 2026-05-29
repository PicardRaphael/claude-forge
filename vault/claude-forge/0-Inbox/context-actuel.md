---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: ["context actuel", "contexte courant", "working memory", "memoire de travail", "etat actuel"]
type: context
status: active
derniere-maj: 2026-05-29
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Veille + optimisation `.claude/` forge. Drop majeur Anthropic capitalisé (Opus 4.8 + Dynamic Workflows). Team tripartite d'audit (boris/ecc/will) rapatriée du global et câblée sans conflit. Tout forge poussé sur `origin/main`.

## Dernière session (2026-05-29)

### Décisions prises
- **Mapping modèle** : `opus` → `claude-opus-4-8` (mappings doc vivants seulement : CLAUDE.md L73 + cc-agents-ref. Agents via alias `opus` = bump transparent). Préférence Raphael : 4.8 > 4.6, **jamais 4.7**.
- **2 Stop hooks forge** : `proactivity-reminder` SUPPRIMÉ (workflow-agentique = drift 22 mai) ; `learning-reminder` GARDÉ (filet /done non fiable, exception assumée tracée [[decision-garder-learning-reminder-hook]]).
- **3 auditeurs (boris/ecc/will)** : rapatriés global → forge (versionnés), GARDÉS (pas de fusion), câblés en complémentarité avec repo-inspector.
- **Routing audit** : « audite » nu → repo-inspector seul ; « à fond / 3 lentilles / mon setup est bon » → tripartite auto (session orchestre + synthétise). Câblé dans `comportement-proactif.md` + `audit-thematique-clusters` (mode tripartite).
- **Fixes neo_ia / ia_back** : faits en SESSIONS DÉDIÉES par repo (Raphael gère), pas pilotés cross-repo depuis forge. Briefs dans `.claude/_briefs_audit/`.

### Livrables forge (7 commits poussés sur origin/main)
- `bb909fe` bump opus 4-8 + pref modèle · `4cab95b` 2 feedbacks mémoire · `07432c5` veille Opus 4.8/Dynamic Workflows (vault) · `91f91cb` fixes conformité forge · `c23fa58` briefs audit · `5293921` rapatriement auditeurs · `026e010` câblage tripartite anti-conflit
- Note vault [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] + [[decision-garder-learning-reminder-hook]]
- cc-news date référence → 29 mai (v2.1.156)

### En cours
Rien d'actif côté forge. neo_ia/ia_back gérés par Raphael en sessions dédiées.

### Prochaines étapes
- Tester la team tripartite en vrai (« audite forge à fond ») pour valider le câblage end-to-end
- Settings.json global : réactiver le warning workflow (ligne `skipWorkflowUsageWarning` → false) si Raphael veut le garde-fou anti-lancement accidentel
- neo_ia : committer les edits déjà faits (drift agents = /go réparé) depuis sa session + fix #4 (spec-brief-boundary gate→advisory)
- ia_back : 3 fixes du brief (garde MultiEdit, réf morte sql-optimizer, descriptions >300)

## Fils ouverts
- **Dynamic Workflows = fragile pour l'audit** : 1er run réel a gelé sur 2 finders (prompt permission en background, ~46 min). Verdict : sub-agents classiques plus robustes pour un audit aujourd'hui ; Dynamic Workflows réservé aux fan-out massifs. (Non capitalisé — session 29 mai, /done blocs [i].)
- **Global ~/.claude propre** : 0 agent/skill/hook/rule. Seul settings.json reste (préférences machine, sain).
- Dette 28 mai toujours ouverte : extension `mcp-alias-guard.py` aux 7 outils MCP ; repro bug #60237 ; 242 fichiers memory/ à auditer.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]]
[[decision-garder-learning-reminder-hook]]
