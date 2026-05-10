---
titre: "Stop words semantiques filtraient les queries d intention"
resume: "STOP_WORDS_FR contenait probleme/erreur/bug/souci — filtrait silencieusement les mots d intention dans search_brain"
aliases:
  - "erreur stop words"
  - "stop words semantiques"
  - "erreur filtrage erreur"
  - "search brain filtre mots"
type: erreur
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/erreur"
  - "#erreur/infra"
  - "#domaine/claude-code"
---

## Ce qui s est passe

`STOP_WORDS_FR` dans `database.py` contenait 4 mots d intention : "probleme", "erreur", "bug", "souci". Resultat : `search_brain("erreur edit direct skills")` supprimait silencieusement "erreur" et cherchait seulement "edit direct skills". Le dossier `Knowledge/erreurs/` et tout le workflow documente encouragent les recherches avec ces mots.

## Pourquoi c etait une erreur

Les stop words doivent filtrer le bruit syntaxique (articles, prepositions), pas les termes d intention. "Erreur" est un mot semantiquement charge dans un vault qui documente des erreurs.

## Fix

Retire les 4 mots de `STOP_WORDS_FR`. Verifie : `search_brain("erreur edit direct")` retourne maintenant `erreur-edit-direct-skills.md` en premier resultat.

## Liens

- [[critique-2026-05-10-mcp-forge-brain]]
- [[sqlite-fts5-vault]]
