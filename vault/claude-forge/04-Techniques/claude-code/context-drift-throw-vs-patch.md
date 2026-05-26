---
aliases:
  - context drift
  - throw vs patch rule
  - clean session vs patched session
  - silent killer Claude Code
  - wrong assumption rule
  - Sairahul context drift
resume: "Règle context drift : typo → corriger inline. Mauvaise assumption architecturale → JETER la session et recommencer avec la bonne assumption baked-in. Patcher = floutent silencieux des concepts."
derniere-maj: 2026-05-26
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Context Drift — Throw vs Patch

## Le silent killer

La plupart des sessions Claude Code ne fail pas dramatiquement. **Elles drift**.

Une wrong assumption entre dans le contexte. Le modèle build dessus. Tu remarques 10 fichiers plus tard.

## Exemple canonique

> Tu demandes à Claude de build subscription management.
> Claude designs : `User → Subscription`.
> Tu te souviens : subscriptions belong to **company**, not user.

Deux réactions possibles :

### ❌ Patcher (anti-pattern)

> "Non, subscriptions belong to companies"

Claude patche. Maintenant tu as :
- `user.subscriptionId` (fantôme du design initial)
- `company.subscriptionId` (le nouveau)

Les deux flottent dans le contexte. Confusion persiste. Code généré ensuite va probablement référencer les deux.

### ✅ Throw away (bonne réaction)

`/clear` la session.

Redémarrer avec le bon contexte dès le premier prompt :
> "Build subscription management. Subscriptions belong to companies (not users)."

Clean mental model dès le départ. Pas de fantôme.

## La règle

| Type d'erreur | Action |
|---------------|--------|
| Typo / nom de variable / petit oubli | Corriger inline |
| Wrong assumption architecturale | `/clear` + restart avec assumption baked-in dès prompt 1 |
| Wrong assumption sur les données | `/clear` + restart |
| Wrong assumption sur business rules | `/clear` + restart |

**Test rapide** : si l'erreur est *structurelle* (DB schema, hiérarchie d'entités, flow de données), throw away. Si c'est *cosmétique* (nom, format, typo), patcher.

## Pourquoi ça marche

Contexte LLM = un seul fil d'inférence. Tout ce qui est dedans influence la suite. Un fantôme architectural qui survit à plusieurs tours = polluant pour TOUTES les générations suivantes.

Une clean session avec le bon mental model **beats** a patched session every time.

## Croisement avec workflow Boris

Boris Cherny (créateur Claude Code) prêche le même pattern via `/clear` et "Document & Clear" :
- Dump le plan dans un .md
- `/clear`
- Nouvelle session lit le .md

C'est la version disciplinée du throw-away.

## Implications forge

1. Ajouter cette règle à [[workflow-claude-code-optimal]] (déjà mentionne /clear, mais pas la distinction typo vs architecture)
2. Possible hook : détecter "non, en fait..." après >5 tours → suggérer `/clear`
3. Skill `/recap` existante = parfait pour faire le bridge entre sessions throwed-away

## Liens

- [[workflow-claude-code-optimal]] — déjà mentionne /clear
- [[recap]] — skill de bridge entre sessions
- [[software-factory-pattern-2026]] — source originale de la formulation

## Référence

- Sairahul (@sairahul1) — article X 25 mai 2026 (formulation explicite)
- Pattern relayé par FCC, dev.to, Anthropic docs (`/clear` recommandation)
- [Boris Cherny workflow](https://www.youtube.com/@borischerny)
