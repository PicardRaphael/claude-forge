---
name: 5-lignes-karpathy-ouverture-claudemd
description: "Tout CLAUDE.md forge commence par 5 lignes Karpathy en tête (avant Critiques < ligne 25), verbatim non-paraphrasables, tradeoff italique en dessous."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Cf [[comment-ecrire-claudemd]] (doctrine : 5 lignes Karpathy verbatim en tête de tout CLAUDE.md forge, avant les Critiques < ligne 25 ; bloc exact, mapping forge⨯Karpathy, pas de ligne tradeoff italique, ne pas étendre à 6+, hors budget < ligne 25, 8 éléments additionnels au corps).

**Cas empirique(s) :**
- Décision 24 mai 2026 (pas de ligne italique tradeoff) : vérifié sur claude-forge + ia_back + neo_ia (3 CLAUDE.md modifiés sans la ligne).
- Décision Raphael 24 mai 2026, validation advisor 2 tours.
- Sub-agent `claudemd-optimizer` bloqué par auto-mode classifier pour cette modif (cas observé 24 mai) → édition manuelle Raphael possible si bypass classifier refuse.
- Repos non-code (vault Obsidian comme neoteem-brain) : NE PAS propager mécaniquement les 5 lignes — adapter ou omettre. (Nuance/divergence vs la canonique vault qui liste neoteem-brain parmi les repos gouvernés.)
