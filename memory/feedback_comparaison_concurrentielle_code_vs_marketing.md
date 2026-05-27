---
name: comparaison-concurrentielle-code-vs-marketing
description: "Comparer forge à un concurrent = lire son code source, jamais le marketing. L'hypothèse de positionnement de départ est souvent fausse."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a69d9c8e-be6b-4653-abfc-532e2dc0ce5d
---

Pour toute comparaison concurrentielle (Phase 4 Hermes Agent, futures veilles), la source de vérité est le **code source cloné**, jamais les articles/tweets/SEO.

**Why:** Phase 4 (27 mai 2026) — l'hypothèse de départ "Hermes brille sur l'async, forge sur la mémoire" était fausse. Le marketing Hermes ("self-improving agent that grows with you") visait précisément les axes prioritaires de forge. Seule la lecture du code a départagé le réel du vent : background_review RÉEL (fork LLM toutes 10 itérations) mais file_safety explicitement "NOT a security boundary", GEPA = POC Phase 1/5 hors runtime, MEMORY.md plat 2200 chars (pas le store sophistiqué annoncé). Les stars "140k" SEO = 169 296 réelles via gh api.

**How to apply:**
1. Cloner les repos (`--depth 1`), vérifier stars/dates via `gh api` ou API GitHub (pattern [[stars-github-drift]]).
2. Identifier LE chemin de fichier de chaque axe AVANT d'écrire la moindre prose. Si un axe marketing n'a pas de fichier identifiable → signal #1 marketing > code.
3. Déléguer la lecture profonde à des agents Explore par axe (contexte principal propre, workflow Boris).
4. Ne PAS confirmer l'hypothèse de positionnement — la TESTER. Laisser les données décider de l'asymétrie (cf [[pas-de-symetrie-artificielle-priorisation]]).
5. Question discriminante mémoire/apprentissage : QUI décide quoi capitaliser, et l'humain peut-il auditer/corriger après coup ? (contrôle vs automatisation).
