---
titre: "Cowork ne peut pas écrire le vault en run planifié (headless)"
resume: "Une tâche planifiée Cowork peut LIRE le vault (MCP/fichiers) mais pas y ÉCRIRE de façon fiable. La mémoire d'apprentissage doit être locale, pas en notes vault."
aliases: ["cowork write vault", "cowork headless ecriture", "cowork run planifie vault", "memoire locale cowork"]
type: technique
derniere-maj: 2026-06-01
auteur: claude
tags: ["#type/technique", "#domaine/claude-code"]
---
# Cowork ne peut pas écrire le vault en run planifié (headless)

En run planifié (headless) Cowork, les outils d'**écriture** vault (`create_note`, `append_note`)
échouent / ne sont pas fiables, alors que la **lecture** (`read_note`, `search_brain`) fonctionne.

Conséquence design : toute mémoire qui doit persister entre runs (learnings, état) va en
**fichiers locaux**, jamais en notes vault. L'écriture vault est réservée aux sessions
**interactives** (où elle fonctionne).

Cas réel : régression automatisation triage support LOJII (13 mai → 1er juin 2026) — la migration
de la mémoire locale vers des notes vault a tout cassé silencieusement (notes jamais créées,
classification sans corrections passées).

Voir [[cowork-architecture]] et [[automatisation-triage-tickets-support-suivi]].
