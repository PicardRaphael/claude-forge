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

**Renforcement 2e occurrence — 28 mai 2026 (chantier OVERVIEW Anthropic)** : chiffre "181 tests baseline (143 mcp + 38 hooks)" porte de session en session dans `SELF_PORTRAIT.md` depuis au moins 1 session. Brief Raphael etape 5 "Tests 181 verts confirmes" relayait passivement le chiffre obsolete. Mesure empirique au moment de la validation : `python -m pytest --collect-only` racine = 143 (mcp-forge-brain), `.claude/hooks/tests/` = 181 (pas 38 — confusion fichiers vs cas de tests). Vrai total = **324 verts** (143 + 181). Pris par advisor avant commit OVERVIEW destine Boris Cherny — un doc qui preche "mesurer-avant-proclamer" §5 et "deux analyses triangulees" §1 ne pouvait pas porter un chiffre faux. Fix : 3 occurrences OVERVIEW + 2 occurrences SELF_PORTRAIT corrigees meme commit.

**Lecon** : un chiffre baseline cite dans SELF_PORTRAIT/CLAUDE.md/RECAP = a remesurer a chaque cycle git majeur, jamais relaye sur foi du document source. Le SELF_PORTRAIT n'est pas une mesure, c'est un snapshot date. Chiffre numerique > 2 sessions sans re-mesure = candidat verification automatique.
