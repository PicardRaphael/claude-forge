---
titre: "Erreur : recherche vault filtrée mentalement par dossier"
resume: "search:context est global mais Claude filtre les résultats par dossier et dit 'pas trouvé' alors que des notes techniques matchent"
aliases:
  - vault search scope filter
  - aucune note vault faux négatif
  - neo-brain-support search bug
  - "recherche vault filtre mental"
  - "faux negatif recherche obsidian"
type: erreur
auteur: claude
derniere-maj: 2026-04-23
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
---

# Erreur : recherche vault filtrée mentalement par dossier

## Ce qui s'est passé

La skill `neo-brain-support` présentait un flux de recherche séquentiel :
1. Chercher dans 07-Support/ → trouvé ? → répondre
2. Sinon Knowledge/ → trouvé ? → reformuler
3. Sinon vault structure → trouvé ? → reformuler
4. Sinon escalade

Le problème : `search:context` cherche dans **tout le vault d'un coup** (850+ notes). Le flux séquentiel donnait l'impression de chercher dossier par dossier. Claude interprétait "Chercher dans 07-Support/" comme un scope, filtrait mentalement les résultats, ne trouvait rien dans 07-Support/ (105 notes seulement), et concluait "Aucune note vault" — alors que des notes pertinentes existaient dans 02-BDD/ (196), 03-Apps/ (248), Knowledge/ (111).

## Pourquoi c'était une erreur

- Budget trop serré : "1 search + 1-2 reads" = pas assez pour le contexte ticket-triage
- Flux séquentiel ambigu : semblait dire "cherche ICI d'abord" alors que la recherche est globale
- Pas de retry avec termes alternatifs : un seul essai avant "pas trouvé"
- Résultat : faux négatifs systématiques sur les notes techniques pertinentes

## Fix appliqué

1. **Principe fondamental ajouté** : "la recherche est GLOBALE, les dossiers sont un ordre de préférence pour UTILISER les résultats"
2. **Flux ticket-triage** ajouté : 2 recherches minimum (fonctionnelle + technique) + MOC fallback avant "Aucune note vault"
3. **Gotcha ajouté** : "Aucune note vault est un dernier recours, pas un premier réflexe"
4. **Mapping symptôme → termes** de recherche ajouté dans neo-brain-support ET dans triage-tickets

## Leçon générale

Quand on écrit un flux de recherche pour une skill qui utilise un index global (Obsidian search, Elasticsearch, etc.), les "priorités par dossier" doivent être clairement identifiées comme un **tri des résultats**, pas comme un **scope de recherche**. Sinon Claude interprète littéralement et restreint sa recherche.

## Liens

- [[neo-brain-support]]
- [[triage-tickets]]
