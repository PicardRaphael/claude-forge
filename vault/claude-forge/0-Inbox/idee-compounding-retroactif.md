---
titre: "Idée — Compounding rétroactif (croisement A1+A3)"
resume: "Coupler la recherche de transcripts non capitalisés (A1) et la capitalisation proposée à /done (A3) pour rattraper le passé jamais capitalisé. Capacité qu'aucun agent (ni Hermes ni forge) n'a aujourd'hui."
aliases:
  - "compounding retroactif"
  - "retroactive compounding"
  - "idee compounding retroactif"
  - "rattraper passe non capitalise"
derniere-maj: 2026-05-27
tags:
  - "#type/idee"
  - "#projet/claude-forge"
---

# Idée — Compounding rétroactif (croisement A1+A3)

Lien : [[phase-4-comparaison-hermes-roadmap]], [[avantages-acquis-claude-forge-vs-hermes]]

## L'insight

Issue de la Phase 4 (comparaison Hermes). Le seul gap mémoire vraiment net de Hermes est `session_search` (recherche dans les transcripts bruts). En croisant les deux gaps prioritaires :

- **A1** = transcripts de sessions passées cherchables (FTS5 sur `~/.claude/projects/*.jsonl`)
- **A3** = capitalisation PROPOSÉE à `/done` (diff prêt-à-valider, humain dans la boucle)

→ **A1 × A3 = compounding rétroactif** : à `/done`, ne pas seulement proposer ce qu'on a appris CETTE session, mais **chercher dans l'historique brut les apprentissages jamais capitalisés** (décisions, erreurs, patterns présents dans d'anciens transcripts mais absents du vault/mémoire) et les proposer à la validation.

## Pourquoi c'est inédit

- **Hermes** : background review capitalise au fil de l'eau, mais n'a aucune mémoire de ce qu'il a MANQUÉ. Pas de rattrapage du passé.
- **claude-forge actuel** : capitalise ce que Raphael repère en session. Ce qui n'est pas repéré sur le moment est perdu.
- **Compounding rétroactif** : transforme l'historique brut dormant en doctrine. Aucun des deux ne le fait.

## Faisabilité (esquisse)

1. Indexer les transcripts (A1, MCP FTS5).
2. À `/done` (ou commande dédiée `/recall-uncaptured`), pour les sujets de la session : chercher dans les transcripts passés les segments riches (décision, correction, "ne plus refaire") qui n'ont pas de note vault / feedback correspondant.
3. Heuristique de détection "non capitalisé" : segment transcript sans backlink vault ni entrée mémoire sur le même sujet.
4. Proposer les blocs à valider (réutilise l'UX de A3).

## Risques / à challenger avant build

- Bruit : beaucoup de transcript n'est pas capitalisable. Heuristique de pertinence cruciale (sinon noyade sous les propositions).
- Coût : scan d'historique = volume. Limiter par fenêtre temporelle + sujet.
- Doublons : ne pas reproposer ce qui est déjà capitalisé sous un autre nom.
- À passer en devils-advocate avant tout build (proposition majeure = croisement Jarvis).

## Statut

Idée, non planifiée. Prérequis : A1 implémenté. À mûrir après A1+A3.
