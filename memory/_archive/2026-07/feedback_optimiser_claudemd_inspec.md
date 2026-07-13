---
name: optimiser-claudemd-inspec
description: Optimiser CLAUDE.md in-spec (< 200L) ≠ réduire mécaniquement — appliquer le test "Would removing this cause mistakes?" ligne par ligne, pas un objectif de %-réduction
metadata:
  type: feedback
---

Ne pas traiter "optimise mon CLAUDE.md" comme un objectif de réduction de lignes si le fichier est déjà in-spec (< 200 lignes).

**Why:** Session 6 juin 2026 — proposition initiale de coupes -30% invalidée par advisor. Erreur : classer les incidents datés ("40 tours sans vault") comme "bruit" alors qu'ils sont la raison qui donne du mordant à la règle (canonique : "la raison est ce qui permet de généraliser"). Classer l'index notes canoniques comme "over-specified" alors que c'est un routing map protecteur. Les deux coupes affaiblissaient l'adhérence sans gagner de signal.

**How to apply:** Avant tout audit CLAUDE.md, vérifier `wc -l` — si < 200 lignes, l'objectif n'est pas la réduction mais le test "Would removing this cause mistakes? If not, cut it." appliqué ligne par ligne. Coupes sûres = info datée en dur, sections entièrement couvertes par des rules chargées à chaque session, bullets d'impl non-évidents absents. Coupes risquées = incidents-raison, index de routing, anti-patterns compounding.
