---
name: search-brain-large-avant-creer-note
description: Avant de créer une note vault, search_brain sur le CONCEPT SEUL (terme large), pas sur la requête composée du contexte courant. Une requête étroite rate la note existante → doublon. Le hook mcp-alias-guard (stem ambigu) est le dernier filet, pas le premier.
metadata:
  type: feedback
---

Run cc-news 16 juin 2026 : j'ai créé `04-Techniques/claude-code/harness-engineering.md` alors qu'une note canonique `04-Techniques/agents/harness-engineering.md` existait déjà (formalisée Böckeler, plus complète). Doublon détecté SEULEMENT au moment d'éditer un wikilink — le hook `mcp-alias-guard` a bloqué sur le stem ambigu « harness-engineering » (2 notes).

**Cause racine** : mon `search_brain` au moment de la capitalisation portait sur `"harness engineering recursive language models RLM"` (requête composée du contexte du run) — trop étroite, elle n'a pas remonté la note `harness-engineering` seule. Un `search_brain("harness engineering")` nu l'aurait trouvée immédiatement (FTS file_stem:10).

**Why** : la doctrine « enrichir avant créer » ([[memory-discipline]] + rule) suppose un search_brain EFFICACE. Une requête étroite donne un faux négatif « aucun foyer » → doublon mécanique. C'est une RÉCURRENCE du pattern doublon (déjà noté session S3 dans CHANGELOG vault).

**How to apply** :
1. Avant `create_note`, faire `search_brain` sur le **concept seul** (1-3 mots du sujet de la note), PAS la phrase de contexte du run.
2. Si le sujet a un nom propre / terme établi (« harness engineering », « RLM »), chercher CE terme isolément.
3. Le hook `mcp-alias-guard` (blocage stem ambigu) est le DERNIER filet de sécurité, pas le premier — ne pas compter dessus pour rattraper un doublon.
4. Rattrapage propre quand doublon créé : lire l'existant EN ENTIER → enrichir l'existant du seul contenu neuf → supprimer le doublon (via un alias UNIQUE du doublon, car `delete_note` par stem ambigu échoue).

Cf [[memory-discipline]] (enrichir avant créer, chercher activement tous les foyers) + [[feedback_mcp_alias_ambigu_chemin_exact]] (le delete par alias unique).
