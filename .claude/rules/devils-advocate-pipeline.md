---
description: "Run devils-advocate agent CONDITIONALLY on major deliverables (architecture decisions, reusable skills, orchestrating agents) — NOT systematically post-22 mai doctrine"
---

# Devil's Advocate — CONDITIONNEL (doctrine 22 mai 2026)

## Doctrine post-pivot 22 mai

**DA n'est PAS un gate systématique.** Le hook `devil-advocate-stop` qui forçait DA en fin de session = anti-pattern doctrinal (workflow hooks supprimé). DA reste conditionnel ciblé.

Référence : [[critique-2026-05-22-8-canoniques-chantier]] + [[raisonnement-22mai-doctrine-vs-enforcement]].

## Quand invoquer (ciblé)

| Livrable | Devil's advocate ? |
|----------|-------------------|
| **Décision d'architecture** majeure | OUI — session principale lance DA |
| **Skill réutilisée cross-repos** ou skill métier complexe | OUI |
| **Agent orchestrant** ou sécu critique | OUI |
| **Proposition Jarvis** (croisement inédit) | OUI |
| Refonte structurelle vault / composants | OUI |
| Nouvelle skill basique | NON — DA = overhead |
| Nouvel agent simple | NON |
| Nouveau hook lint/format | NON |
| Modification de CLAUDE.md | NON |
| Fix de bug / correction mineure | NON |
| Recherche / synthèse informative | NON |
| Création de fiches vault / batch de notes | NON |
| Audit / restructuration vault | NON — utiliser vault-audit |

## Comment l'intégrer

1. Terminer le livrable normalement (via agents spécialisés)
2. Lancer `devils-advocate` avec le livrable en contexte (si applicable selon tableau)
3. Présenter à Raphael : livrable + critique + ta réponse
4. DA sauvegarde sa critique dans `Knowledge/critiques/`

## Anti-patterns

- ❌ **Invoquer DA sur tout** → fatigue, on l'ignore. Réservé aux livrables MAJEURS uniquement.
- ❌ **Gate systématique** par hook → workflow hooks = anti-pattern doctrine 22 mai
- ❌ **Ignorer les objections BLOCKING** → autant ne pas l'avoir
- ❌ **Ne pas sauvegarder dans le vault** → on perd l'apprentissage

## Ce que le DA consulte dans le vault

AVANT de critiquer, le DA cherche (conditionnel ciblé, max 2 requêtes MCP) :
- `Knowledge/erreurs/` — erreurs passées similaires
- `Knowledge/critiques/` — critiques précédentes sur le même sujet
- `Knowledge/raisonnements/` — raisonnements validés pertinents

## Référence canonique

Source de vérité : [[comment-creer-agent]] (DA conditionnel) + [[workflow-claude-code-optimal]].
