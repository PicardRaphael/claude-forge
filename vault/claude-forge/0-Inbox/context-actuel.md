---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-22
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle

Calibrage doctrine claude-forge : passage de "OBLIGATOIRE partout" à "intelligent + conditionnel" pour les agents. Fix DA bouclant 5 min + DRY 8 agents sur consultation vault.

## Dernière session (2026-05-22 soir)

### Décisions prises
- DA : étape 2 vault conditionnelle (max 2 requêtes ciblées), sauvegarde non bloquante, interdit Bash heredoc
- Nouvelle rule `vault-consultation-protocol.md` = single source of truth
- 8 agents DRY : bloc Étape 0 vault remplacé par référence (3 lignes)
- Critiques DA des refontes structurelles rejetées sauvegardées dans le vault
- Commit `e8e08b1` (14 fichiers, +279/-143) — uniquement les changements de cette session, pas les fichiers parallèles d'un autre agent
- Pas de modifs sur neo_ia/ia_back (autre agent en cours)

### En cours
- Un autre agent finit des modifs sur ia_back + neo_ia en parallèle (Raphael a précisé)
- Critique DA `architect-guard-allowlist` : verdict BLOQUER refonte allowlist, livrer uniquement exemption tests par-pattern si récurrence

### Prochaines étapes
- Tester en session fraîche que le DA ne boucle plus (relancer DA sur une proposition triviale, vérifier sortie < 2 min sans tentative Bash)
- Si Raphael relance "refonte massive de quelque chose", PENSER au feedback_recurring_meta_anti_pattern AVANT de proposer
- Le fix DRY claude-forge ne se généralise PAS à neo_ia/ia_back (leurs OBLIGATOIRE sont métier, pas du copié-collé)

## Fils ouverts

- Si latence créateurs encore trop forte → baker best practices critiques directement dans leur prompt (au lieu de les faire chercher) — chantier futur, pas ce soir
- Couplage architect.md ↔ architect-guard hook (AVERTISSEMENT 5 du DA matin) : à traiter quand on touchera vraiment la doctrine architect
- Si même les 4 créateurs paraissent trop lents après ce fix → mesurer 2 semaines avant de toucher davantage

## Liens

[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[raisonnement-kill-tdd-strict-hooks-mai-2026]]
[[critique-2026-05-22-architect-guard-allowlist]]
[[critique-2026-05-22-vault-doctrine-renversement]]
