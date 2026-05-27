---
name: 5-lignes-karpathy-ouverture-claudemd
description: "Tout CLAUDE.md forge commence par 5 lignes Karpathy en tête (avant Critiques < ligne 25), verbatim non-paraphrasables, tradeoff italique en dessous."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Tout CLAUDE.md sous gouvernance forge (claude-forge, ia_back si créé, neo_ia si créé, bdd si créé) DOIT commencer par 5 lignes verbatim Karpathy en tête, AVANT toute autre section. Format exact :

```
- Si ambigu : Demande. Ne choisis pas en silence.
- Diff minimal. Touche uniquement ce qui est demandé.
- Définis `<done>` avant de commencer (1 ligne suffit).
- Vérifie dans le code latest. Jamais d'hypothèse.
- Code minimum ; pas de feature spéculative.
```

**Décision 24 mai 2026** : PAS de ligne italique tradeoff en dessous ("ces 5 lignes biaisent vers la prudence..."). Bruit visuel sans gain — Claude applique déjà du jugement sur tâches triviales. La soupape vit dans le jugement runtime, pas dans la doctrine écrite. Vérifié sur claude-forge + ia_back + neo_ia (3 CLAUDE.md modifiés sans la ligne).

**Why :** Karpathy a documenté les failure modes universels des LLM agents le 26 jan 2026 (silent assumptions, overcomplication, edits adjacents non-autorisés). Forrest Chang a distillé en 4 principes (repo [[multica-ai/andrej-karpathy-skills]] = 100K+ stars). Forge a condensé en 5 lignes francophones avec extension "vérifie code latest" (anti-doctrine-drift forge). Décision Raphael 24 mai 2026, validation advisor 2 tours.

**How to apply :**
- Position : après H1 + ligne meta, AVANT `## ⚠️ Critiques (< ligne 25)`. Premier contenu lu.
- Verbatim non-paraphrasable : modifier le wording = perdre le signal. Soit verbatim, soit pas du tout.
- Ne PAS étendre à 6/7/8 lignes (limite cognitive). Nouvelles règles universelles → nouveau bloc plus bas.
- AUCUNE ligne italique tradeoff en dessous (décision 24 mai 2026).
- Ne comptent PAS dans budget "Critiques < ligne 25" — règle implicite, pas besoin de l'expliciter dans chaque CLAUDE.md cible.
- Sub-agent `claudemd-optimizer` peut être bloqué par auto-mode classifier pour cette modif (cas observé 24 mai) → édition manuelle Raphael possible si bypass classifier refuse.
- Repos non-code (vault Obsidian comme neoteem-brain) : NE PAS propager mécaniquement — adapter ou omettre.
- 6 éléments Karpathy additionnels (match style, dead code orphelin vs unrelated, plan format `[Step] → verify`, transformations tâches→goals, critère succès auto-évaluable) vivent dans le CORPS du CLAUDE.md niveau avancé, pas dans les 5 lignes.

**Source canonique vault :** [[comment-ecrire-claudemd]] section "5 LIGNES D'OUVERTURE OBLIGATOIRES".
