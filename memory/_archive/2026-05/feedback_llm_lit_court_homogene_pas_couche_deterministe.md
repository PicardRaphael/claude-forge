---
name: llm-lit-court-homogene-pas-couche-deterministe
description: Construire une couche déterministe (Python, Jaccard, regex clustering, ML léger) par-dessus une lecture LLM possible d'un corpus COURT et HOMOGÈNE (ex MEMORY.md 244L, format de puces uniforme) = enforcement-théâtre + dette de tests, sans signal nouveau. Le LLM lit le corpus entier en un coup et regroupe SÉMANTIQUEMENT mieux que la machinerie. Mesurer empiriquement que le LLM RATE des clusters AVANT de construire l'aide ; sinon ne pas construire.
metadata:
  type: feedback
---

Quand un plan propose une couche déterministe (script Python, similarité Jaccard/cosine sur titres, regex de clustering, seuils à tuner) pour détecter des doublons / candidats dans un corpus **court et homogène**, challenger AVANT de construire : un LLM qui lit le corpus entier en un coup regroupe sémantiquement mieux que la machinerie déterministe.

**Why:** 27 mai 2026 — chantier "système de compaction MEMORY.md". Plan validé en amont incluait `scripts/compact-memory.py` à similarité Jaccard 0.5 sur slugs/titres + tests + dry-run. Advisor a tranché : sur 244 lignes ultra-homogènes (format `- [slug](fichier.md) — résumé`), le LLM avale tout. Jaccard sur slugs kebab-case de 3-5 mots = faux positifs (mots vides communs) ET faux négatifs (`frontmatter-fait-foi` ≈ `pas-de-meta-commentaire-doctrine` : 0 mot commun, concept proche). **Preuve empirique fournie en séance** : les 10 orphelins (fichiers feedback sans entrée index) + leur classification obsolète/valide ont été détectés avec un simple `grep` d'orphelins + lecture LLM des descriptions — zéro Jaccard nécessaire. La couche Python aurait ajouté script + tests (dette permanente) + seuil à tuner pour aucun signal que le LLM ne capte déjà.

**How to apply:**
- Corpus court (< ~quelques centaines de lignes) ET homogène (format fixe) → le LLM lit en un coup. Couche déterministe = suspect.
- Avant de coder la détection : mesurer que le LLM RATE systématiquement des clusters (instance de [[measure-before-optimize-tests]]). Si pas mesuré → ne pas construire, garder en option conditionnelle différée.
- La détection déterministe a sa place sur du VOLUMINEUX (milliers d'items, pas de format exploitable) ou quand on veut un oracle reproductible hors-LLM — pas sur un index de 244L.
- Distinct de [[recurring-meta-anti-pattern]] (workaround répété = bug) : ici c'est construire une aide AVANT d'avoir mesuré le besoin. Lié à [[enforce-not-advise]] (hooks = lint/sécu/scope, pas machinerie de jugement que le LLM fait mieux).
