---
name: test-everything-after-creating
description: TOUJOURS tester ce qu'on crée — hooks, agents, skills, MCP. Ne JAMAIS dire "ça marche" sans preuve.
type: feedback
originSessionId: be761cf9-3fd0-4016-adb8-3e189b4efb1f
---
## Tester TOUT après création — OBLIGATOIRE

Ne JAMAIS livrer un composant sans l'avoir testé en conditions réelles.

**Why:** Session 2026-05-09 — le devil's advocate PostToolUse hook a été créé, déclaré fonctionnel, mais ne fonctionnait PAS en pratique (stdout PostToolUse Agent pas visible dans le contexte). L'erreur a été découverte seulement quand Raphael a demandé "pourquoi je ne vois pas le devil's advocate". De plus, le bug "subagents ne peuvent pas spawner d'autres agents" était DÉJÀ dans la mémoire (feedback_major_mistakes.md erreur #1) mais n'a pas été consulté.

**How to apply:**
- Après création d'un hook → le tester avec un vrai agent/tool, pas juste `echo | python`
- Après création d'un agent → le spawner et vérifier qu'il produit le résultat attendu
- Après création d'une skill → l'invoquer avec `/skill` et vérifier
- Après création d'un MCP tool → appeler l'outil depuis un subagent pour vérifier l'héritage
- Si le test échoue → corriger AVANT de déclarer "c'est fait"
- RELIRE la mémoire (feedback_major_mistakes) AVANT de concevoir — les erreurs passées sont documentées
