---
name: test-echoue-hypothese-vs-bug
description: "Test qui échoue ≠ toujours bug. Souvent c'est l'assert qui encode une hypothèse erronée du testeur sur l'ordre/le comportement du code. Vérifier le code AVANT de le 'réparer'."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f598fcbc-1e1f-4161-bd42-75eddf13fbdf
---

Quand un test que JE viens d'écrire échoue, distinguer deux cas avant d'agir :
- L'assert encode une **exigence** (le code DOIT faire X) → si le code ne le fait pas, c'est un bug à fixer.
- L'assert encode une **hypothèse** sur le fonctionnement interne (je SUPPOSE que le code fait X) → si le code fait Y de façon cohérente, c'est mon test qui a tort. Corriger le test pour pinner le comportement réel (caractérisation), pas "réparer" le code.

**Why:** Validé 27 mai (Phase 3). `test_resolve_prefix` a échoué : j'avais supposé que `resolve_note` testait le tier 3 (préfixe `name-%`) avant le tier 2 (substring `%-name%`). Le code fait l'inverse (tier 2 d'abord, ligne 246 avant 254). Aucun bug — juste mon hypothèse sur l'ordre. J'ai renommé le test en `test_resolve_tier2_beats_tier3` pour pinner l'ordre RÉEL.

**How to apply:**
- Test rouge sur du code existant non touché → lire le code AVANT de conclure "bug". Souvent l'assert est faux, pas le code.
- Si le comportement réel est cohérent et sensé → corriger l'assert + docstring "characterization, pins behavior X".
- Si le comportement réel est incohérent/dangereux → là c'est un bug : caractériser (cf [[bug-caracterise-fix-trivial-vs-couteux]]).
- Ne JAMAIS modifier le code source pour faire passer un test dont l'assert était une hypothèse non vérifiée.
