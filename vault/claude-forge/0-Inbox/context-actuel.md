---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-07-09
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Optimisation du corpus skills forge (performance de déclenchement d'abord) : descriptions raccourcies, fusions arbitrées, delegate-guard corrigé pour les skills empilées.

## Derniere session (2026-07-09, poste perso)
### Decisions prises
- Arbitrage fusions forge-review (AskUserQuestion item par item + DA) : F1 cc-rag-ref→rag-design ✅, F3 web-search-canonical-source→rule ✅, F2 trio doctrine → **measure-first** (Option A), F4/F5 → KEEP. 0 KILL. Corpus : 50 → 48 skills.
- Doctrine actée (feedback tier-1) : **perf de déclenchement > budget tokens** pour tout arbitrage skills — fusion budget-only refusée.
- Doctor poste perso : `defaultMode: auto` (user scope), plugin context7 + connecteur GChat désactivés, 4 doublons mémoire locale purgés.
- Fix delegate-guard (empilement + fenêtre 80) validé et appliqué manuellement par Raphael (classifier self-modification respecté, workaround `.proposed`).

### En cours
- Rien de bloquant — chantier du jour entièrement committé/poussé (fb0163 → 739fb04 + commit /done).

### Prochaines etapes
- **F2 trio doctrine — phase 2** : A/B de déclenchement via `outcomes-test` (protocole prêt : `output/mesure-F2-fusion-doctrine.md`, hôte imposé = methode-pivoter-doctrine). Idéal sur le poste pro.
- Merge du worktree `clean-memory-2026-07` (autre session) : conflit probable sur `memory/MEMORY.md` (2 lignes ajoutées côté main) ; les ex-skills cc-rag-ref / web-search-canonical-source n'existent plus sur main → re-pointer vers [[verification-sources-canoniques]] si besoin.
- Listing skills toujours ~2,4k est. pour ~2k de budget : prochain levier = poursuivre les fusions perf-positives (F2 si mesure verte).

## Fils ouverts
- Suivi doctor : passe `/skill-evolve` non nécessaire (fait ce jour) ; `memory/MEMORY.md` repo à 3,8k tokens est. → candidat `/clean-memory` (partiellement traité dans l'autre session).
- Résidu assumé : mention historique `cc-rag-ref` dans la couche AJOUT 17 juin de [[comment-creer-skill]] (exemple daté, non réécrit).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
