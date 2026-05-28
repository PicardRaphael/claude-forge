---
name: chiffre-baseline-brief-verifier-empiriquement
description: "Chiffre baseline dans brief = hypothese, jamais fait. Mesurer empiriquement avant de raisonner dessus"
metadata:
  type: feedback
---

Tout chiffre baseline annonce dans un brief utilisateur (ex: "baseline tests 319", "fichier 500 lignes", "30 agents") est une **hypothese contextuelle**, jamais un fait verifie. Mesurer empiriquement (`wc -l`, `pytest --collect-only`, `ls | wc -l`) AVANT de raisonner ou propager le chiffre. Si ecart constate, signaler au lieu de relayer.

**Why:** Observe 28 mai 2026 sur propagation post-clean-memory. Brief annoncait "baseline tests 319 → 324 attendu". Mesure empirique = **176 → 181** (ecart 143 tests). Le chiffre 319 venait probablement d'une autre suite/repo confondue dans le contexte du brief. Si j'avais relaye 324 sans verifier, j'aurais pollue le bilan final avec un faux fait.

**How to apply:** Avant toute affirmation chiffree dans un livrable (bilan, rapport, plan d'ecart), verifier la valeur empiriquement meme si le brief la fournit. Variante chiffree de [[feedback_brief_premisse_fausse_verifier_avant_executer]] : memes reflex, applique aux valeurs numeriques. Le chiffre brief = point de depart pour mesurer, pas valeur a propager.

**Pattern de surface** : "le brief dit X, je mesure Y" — toujours signaler l'ecart explicitement, pas le masquer.
