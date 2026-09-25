---
name: consolidate-searches-immediately
description: Une recherche couvre toutes les sources en une passe et n'est pas refaite dans la même session ; le fait distillé se refile au vault, pas dans un fichier mémoire ; une info datée se revérifie.
trigger: cherche, recherche, search, retrouve, deja cherche
type: feedback
originSessionId: 7344c917-42fa-4a63-8a92-bc680e8d28e4
---
Quand tu fais une recherche (web, vault, best practices, features CC, industrie), couvre toutes les sources pertinentes dès la première passe, en parallèle, au lieu d'enchaîner des recherches partielles.

**Why:** Raphaël a dû me demander trois fois de chercher les best practices Boris/Thariq parce que je faisais des recherches partielles. Perte de temps et de tokens.

**How to apply:**
1. Premier search = toutes les sources en parallèle (web search + fetch, `search_brain`).
2. Dans une même session, ne pas refaire une recherche déjà faite. Avant un fan-out d'agents, leur transmettre ce qui a déjà été cherché (registre des opérations coûteuses de `.claude/rules/comportement-proactif.md`).
3. Consolider le fait distillé dans le foyer vault qui couvre le sujet (refile, cf `.claude/rules/forge-brain-proactive.md`), pas dans un fichier mémoire.
4. D'une session à l'autre, lire d'abord le vault. Une information potentiellement datée (version, prix, feature) se revérifie à la source au lieu d'être tenue pour acquise.
