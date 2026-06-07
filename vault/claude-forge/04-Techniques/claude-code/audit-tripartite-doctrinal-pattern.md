---
titre: "Audit tripartite doctrinal — Discipline Boris / Minimalisme Will / Couverture ECC"
resume: "Pattern d'audit d'une config .claude/ sous 3 lentilles doctrinales complémentaires : Discipline (Boris Cherny — hooks lint/sécu, compounding error-driven), Minimalisme (Will — le minimum qui marche, anti-sur-ingénierie) et Couverture (ECC — setup dev maximal, agents spécialisés). Les 3 anciens auditeurs absorbés dans repo-inspector mode=audit. Trois angles qui se corrigent mutuellement, pas une hiérarchie."
aliases:
  - "audit tripartite doctrinal"
  - "trois lentilles boris will ecc"
  - "discipline minimalisme couverture audit"
  - "lentilles doctrinales repo-inspector"
  - "audit config claude trois angles"
type: pattern
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/pattern"
  - "#domaine/claude-code"
  - "#statut/canonique"
---
# Audit tripartite doctrinal

Auditer une config `.claude/` (skills, agents, hooks, rules, CLAUDE.md) sous une seule doctrine produit un verdict biaisé : la discipline pure sur-enforce, le minimalisme pur sous-équipe, la couverture pure sur-ingénierie. Le pattern croise trois lentilles complémentaires qui se corrigent mutuellement.

## Les trois lentilles

| Lentille | Source | Ce qu'elle cherche | Son biais si seule |
|----------|--------|--------------------|--------------------|
| **Discipline** | Boris Cherny | Hooks lint/sécu/scope, compounding error-driven (chaque erreur capturée une fois), règles testables | Sur-enforcement, gates partout |
| **Minimalisme** | Will (CwC London) | Le minimum qui marche, anti-sur-ingénierie, supprimer le spéculatif | Sous-équipement, manque de garde-fous |
| **Couverture** | ECC (personal dev setup) | Setup dev maximal, agents spécialisés, exhaustivité des rôles | Sur-ingénierie, prolifération de composants |

Aucune n'est « la bonne ». Le verdict utile naît de leur tension : ce que la Couverture veut ajouter, le Minimalisme le challenge ; ce que le Minimalisme veut couper, la Discipline le défend s'il porte une garantie. Trois angles, pas une hiérarchie.

## Application — absorbées dans repo-inspector

Les trois anciens auditeurs séparés (boris-auditor / will-auditor / ecc-auditor) ont été **absorbés dans un seul agent** `repo-inspector` (mode=audit). Un agent, trois passes de lecture, un rapport priorisé qui surface les tensions entre lentilles plutôt que d'imposer une doctrine. Routing : « audite à fond / sous tous les angles / 3 lentilles » → `repo-inspector` mode=audit (cf rule comportement-proactif).

## Quand l'appliquer

- Audit complet d'une config `.claude/` (« mon setup est-il bon ? », « optimise ma config »)
- Décision d'ajouter/supprimer un composant : passer la décision aux trois lentilles avant de trancher
- Pas pour un audit ciblé mono-question (une lentille suffit alors)

## Liens

- [[will-vs-ecc-deux-doctrines-anthropic]] — résolution du paradoxe minimum (Will) vs maximum (ECC) agents
- [[ecc-pattern-personal-dev-setup]] — la lentille Couverture détaillée (setup dev ECC)
- [[methode-analyser-repo]] — la méthode 6 étapes dont l'audit tripartite est une composante
- [[refonte-3-repos-26mai-2026]] — application cross-repo des trois lentilles
