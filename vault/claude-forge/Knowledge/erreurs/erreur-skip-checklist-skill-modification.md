---
titre: "Erreur — Skip checklist lors de modification de skill"
resume: "Modification de skill sans passer par la checklist check-before-create — produit des composants non conformes par manque de verification prealable."
aliases:
  - "erreur skip checklist"
  - "skip checklist skill"
  - "erreur modification sans checklist"
  - "oubli check-before-create"
type: erreur
domaine: claude-code
derniere-maj: 2026-05-15
auteur: claude
sources: []
tags:
  - "#type/erreur"
  - "#erreur/skill"
  - "#domaine/claude-code"
---

## Ce qui s'est passe

Modification d'une skill sans passer par la checklist `check-before-create` (memoire, vault, references, skill de reference, delegation). Produit des composants non conformes.

## Pourquoi c'est une erreur

La checklist existe pour eviter de repeter les erreurs passees. La sauter revient a ignorer l'apprentissage accumule.

## Quoi faire a la place

Toujours suivre la checklist dans l'ordre : memoire → vault → references → skill ref → delegation agent specialise.

## Liens

- [[MOC-Techniques]]
- [[pattern-vault-query-guard]]
