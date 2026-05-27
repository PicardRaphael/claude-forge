---
aliases: ["phase-3-renforcement", "audit renforcement claude-forge", "phase 3 audit", "renforcement absolu forge", "matrice priorisation phase 3"]
resume: "Audit 5 axes de renforcement claude-forge (vitrine, tests, portabilité, versioning, ADR) avant comparaison Hermes — matrice de priorisation et source de vérité des décisions."
derniere-maj: 2026-05-27
tags: ["#type/synthese", "#projet/claude-forge"]
---

# Phase 3 — Audit de renforcement (état au 2026-05-27)

Renforcer claude-forge dans l'absolu — pas par rapport à un concurrent. Séquence A→B→C→D→E appliquée. Advisor consulté : un seul P0 sans ambiguïté, le reste P2/P3 capitalisé (pas de symétrie artificielle entre axes).

## Faits observés (étape A)

- **Hooks** : 9 fichiers, 3 testés (security-guard, delegate-guard, meta-commentary-detector). 6 non testés : skill-activation (149L), session-health (116L), mcp-autostart (70L), proactivity-reminder (77L), session-reminder (48L), learning-reminder (50L).
- **MCP forge-brain** : 69 tests sur 9 fichiers. Trous réels : `search()` (4 stratégies FTS5/BM25 + STOP_WORDS_FR + nettoyage) = ZÉRO test direct ; `watcher.py`, `server.py`, `git_sync.py` = zéro test ; `create_note`/`append_note`/`insert_section`/`resolve_note`/`suggest_notes`/`get_tags`/`get_property` non testés directement.
- **Portabilité** : install.bat Windows-only, mcp-autostart flags Windows (DETACHED_PROCESS, CREATE_NO_WINDOW). Cible déclarée = Windows.
- **Versioning vault** : aucun git tag, aucun snapshot. log.md (append-only) + CHANGELOG.md (narratif) tracent l'historique. Reconstruction d'état à une date = uniquement via git log manuel.
- **ADR** : doctrine 22 mai = note dédiée complète ([[raisonnement-22mai-doctrine-vs-enforcement]]). Jarvis, A→B→C→D→E, MCP-vs-RAG, délégation forcée = tracés mais éparpillés (rules, techniques, casquette) ; pas d'ADR dédié pour la délégation forcée.

## Matrice de priorisation (étapes C+D)

| Axe | État | Écart vers irréprochable | Effort | Impact | Priorité |
|-----|------|--------------------------|--------|--------|----------|
| **2a — Tests MCP cœur** (`search` + alias + resolve) | search/db non testés | Régression silencieuse du cœur produit = LLM reçoit faux résultats | Bas | Maximal | **P0** |
| 2b — Tests hooks skill-activation + session-health | non testés | Logique regex/session non pinnée | Bas-moyen | Moyen | P1 |
| 2c — Tests hooks reminders (×3) | non testés | Side-effects simples, fail-open | Bas | Faible | P3 |
| 2d — Tests infra MCP (watcher/server/git_sync) | non testés | I/O + subprocess, fragiles à mocker | Moyen-haut | Moyen | P2 |
| 1 — README + Mermaid | clair, à jour | Schéma archi visuel manquant | Bas | Faible | P3 |
| 3 — Portabilité Linux/Mac | Windows-only | install.sh + flags subprocess cross-OS | Moyen | Faible (cible Win) | P3 |
| 4 — Versioning vault | git seul | Pas de "snapshot daté" requêtable | Bas (tag) | Faible | P3 |
| 5 — ADR délégation forcée | éparpillé | Une note ADR manque | Bas | Faible-moyen | P2 |

## Décisions

- **P0 exécuté** : tests `search()` (4 stratégies), `_alias_expansion`, `_merge_alias_hits`, `_like_variants`, `resolve_note`, `suggest_notes`, `get_tags`, `get_property`. Approche (a) : corpus fixture minimal (3-5 notes), tests paramétriques déterministes. Pas de corpus réel (fragile, retest à chaque évolution vault).
- **P1 exécuté** : tests skill-activation (regex word-boundary, bypass prefixes, session tracker) + session-health.
- **P2 différé + capitalisé** : tests infra MCP (watcher/server/git_sync), ADR délégation forcée.
- **P3 différé + capitalisé** : reminders, README Mermaid, portabilité, versioning vault.

## Déclencheurs de réactivation (pour les P2/P3)

- **Portabilité** → un collaborateur non-Windows veut forker, OU intégration partner network Anthropic.
- **Versioning vault** → besoin de mesurer le compounding dans le temps (comparer état T0 vs T1) OU reproductibilité demandée.
- **README Mermaid** → présentation à un tiers (recruteur, partenaire).
- **Tests infra MCP** → un bug watcher/git_sync observé en production.
- **ADR (4 pivots)** → onboarding d'un contributeur tiers qui doit comprendre le "pourquoi".

Voir [[decision-renforcements-differes-phase-3]] pour le détail des P2/P3.
