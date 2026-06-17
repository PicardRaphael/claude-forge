---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-17
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Config `.claude/` forge auditée à fond (17 juin) et durcie — setup mûr, 0 P0.

## Derniere session (2026-06-17)
### Decisions prises
- Audit global `.claude/` (4 agents Opus parallèles : 53 skills / 14 hooks / 16 rules / 5 agents). Verdict : config saine, 0 P0, 0 kill imposé.
- Fixes P1+P2 appliqués (commit fc8f9b9) : devils-advocate read-only prouvable (Bash retiré), self-updater délègue à skill-creator, 4 orphelines `obsidian-markdown`/`cc-advisor` retirées, 3 désyncs allowed-tools↔MCP, descriptions directives, pointeur mémoire mort, 3 archives sorties du tier-1.
- KILL metrics-tracker : settings + disque + 17 .jsonl + io-daily + io-week (cascade orpheline). Skills : 53 → 51.
- Réflexe DA capitalisé : « le LIVRABLE déclenche, pas l'activité » — audit→plan structurel = DA AVANT application. Hiérarchie de pointeurs CLAUDE.md (nu) / dispatch (trigger+discriminateur) / rule (détail) + carve-out collision carte-blanche (commit 534a3b6).

### En cours
Rien — chantier clos. Tout commité/poussé (main @ 534a3b6), working tree propre.

### Prochaines etapes
- `/clean-memory` : 271 fichiers memory/ > WARNING 250 (~29 candidats archive max, plancher ~240).
- P3 cosmétiques non traités (choix explicite P1+P2) : session-health.py:55 dead code, méta-commentaires datés rules/CLAUDE.md, inline A→E comportement-proactif.

## Fils ouverts
- Rapport durable de l'audit : `AUDIT-CLAUDE-2026-06-17.md` à la racine du repo (référence pour un futur passage P3).

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]