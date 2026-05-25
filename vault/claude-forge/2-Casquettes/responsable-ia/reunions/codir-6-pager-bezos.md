---
aliases:
  - 6-pager
  - six-pager
  - Bezos memo
  - amazon memo
  - codir-reporting
  - exec memo
resume: Format Amazon 6-pager pour CODIR — narration banissant PowerPoint, lue 20 min en silence, force la pensée structurée. Template adapté reporting IA.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/communication"
  - "#rituel/codir"
---

# CODIR / reporting direction — méthode Amazon 6-pager

## TL;DR
- **Bezos a banni PowerPoint** des comités exécutifs (2004) — remplacé par memo narratif 6 pages
- **Lu en silence 20-30 min** en début de réunion, puis discussion
- **Un bon 6-pager prend 1-2 semaines** à écrire (réécritures multiples)
- **Narration > bullets** car les bullets glissent sur les gaps de raisonnement

## Pourquoi PowerPoint a été banni

> *"PowerPoint is a sales tool. Internally, the last thing you want to do is sell. You're truth-seeking."* — Jeff Bezos

Les bullets glissent sur les gaps de raisonnement. La narration force la pensée structurée. Si tu ne peux pas écrire en phrases complètes, c'est que tu n'as pas compris le sujet.

## Structure canonique du 6-pager

1. **Introduction** — projet clair et concis, le pourquoi
2. **Goals** — métriques (revenu, coût, satisfaction, qualité)
3. **Tenets** — principes guidant les décisions
4. **State of the Business** — état actuel, SWOT, data
5. **Lessons Learned** — données de projets passés
6. **Decision asked** — qu'est-ce qu'on demande au CODIR ? (validation, arbitrage, ressource)

### Annexes (au-delà des 6 pages)
- Données détaillées
- Graphiques techniques
- Spécifications

## Test qualité Bezos

> *"Un lecteur intelligent qui ne connaît rien au sujet doit comprendre ce qui est écrit (pas ce que l'auteur voulait dire)."*

Donne ton 6-pager à quelqu'un d'extérieur. S'il pose plus de 3 questions clarification → réécrire.

## Template — 6-pager mensuel IA Neoteem (adapté Raphael)

```markdown
# [Mois YYYY] — State of AI @ Neoteem

## 1. Introduction (½ page)
Une narrative courte : où on en est, ce qu'on a fait ce mois, ce qui change.

## 2. State (1 page)
- KPIs IA : uptime, latence p95, qualité eval suite, coût mensuel infra
- Comparaison mois précédent
- 1 graphique max (en annexe sinon)

## 3. Wins (1 page)
- 2-3 features livrées
- Impact business chiffré (gain temps, conversion, satisfaction)
- Si gain non-mesuré : le dire honnêtement

## 4. Risks & blockers (1 page)
- 2-3 risques actuels (drift modèle, coût infra, sécu, talent)
- Mitigation planifiée
- Risques où le CODIR doit aider

## 5. Outlook (1 page)
- 1 mois à venir : ce qu'on va faire
- 1 trimestre à venir : ce qu'on prépare
- Hypothèses qui peuvent invalider le plan

## 6. Asks (½ page)
- Décisions demandées (avec options + recommandation)
- Ressources demandées (budget, hire)
- Arbitrages demandés (priorisation)
```

## Traduction tech → non-tech (CRITIQUE)

Remplacer chaque métrique technique par sa traduction business :

| Tech | Business |
|---|---|
| F1 0.87 sur eval suite | "1 réponse sur 8 nécessite revue humaine, vs 1 sur 3 il y a 3 mois" |
| Latency p95 1.2s | "95% des users attendent moins d'1.2 sec" |
| Hallucination rate 3% | "3 erreurs factuelles toutes les 100 requêtes" |
| Token cost $0.012/req | "Coût IA par lead traité : 1.2 cents" |
| Drift detection alert | "La qualité des réponses se dégrade silencieusement" |

## Anti-patterns 6-pager

- ❌ **Bullet points partout** → réécrire en phrases complètes
- ❌ **Jargon non vulgarisé** → "transformer", "embedding", "RAG" sans explication
- ❌ **Métriques sans business meaning** → un F1 ne dit rien à un CFO
- ❌ **Pas de "decision asked"** → la réunion n'a pas de but
- ❌ **Écrit en 2h la veille** → ça se voit, ça se sent
- ❌ **Annexes manquantes** → CFO veut le détail si question

## Le déroulement de la réunion CODIR

| Temps | Activité |
|---|---|
| 0-20 min | **Lecture silencieuse** du 6-pager (CRUCIAL — pas de pitch oral) |
| 20-25 min | Questions clarification |
| 25-50 min | Discussion sur les "asks" |
| 50-60 min | Décisions actées + owners + deadlines |

**Crucial** : si le CODIR n'a pas le temps de lire avant, on lit en réunion. Pas de "résumé verbal" qui contourne le système.

## Cadence recommandée Raphael

- **6-pager mensuel** : performance IA équipe (état)
- **6-pager trimestriel** : roadmap + résultats OKR (stratégie)
- **6-pager ad hoc** : décisions majeures (build vs buy, hire senior, refonte archi)

## Documents complémentaires Amazon

- **PR-FAQ** : Press Release imaginaire AVANT de construire (voir [[../communication/pr-faq-amazon-working-backwards]] — à venir)
- **1-pager** : version condensée pour décisions simples
- **Narratives** : 2-page memos pour réunions moins formelles

## Liens

- [[reunions/index]]
- [[../communication/parler-non-tech-vulgarisation]]
- [[../templates/template-6-pager-codir]]
- [[../priorisation/roadmap-now-next-later]]

## Sources

- [CNBC – Bezos 6-page memos](https://www.cnbc.com/2018/04/23/what-jeff-bezos-learned-from-requiring-6-page-memos-at-amazon.html)
- [Anecdote – 6-page narrative structure](https://www.anecdote.com/2018/05/amazons-six-page-narrative-structure/)
- [Visme – Amazon 6-Pager Guide](https://visme.co/blog/amazon-6-pager/)
- Bryar, Carr — "Working Backwards" (livre)
