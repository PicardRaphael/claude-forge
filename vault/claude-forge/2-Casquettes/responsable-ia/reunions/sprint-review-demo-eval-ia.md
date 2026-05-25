---
aliases:
  - sprint review
  - demo IA
  - démo IA
  - sprint demo
  - revue sprint
  - eval suite demo
resume: Sprint review équipe IA — démo eval > démo UI, table avant/après métriques, cas adverses inclus. Transparence > marketing.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/agile"
  - "#rituel/sprint"
---

# Sprint Review / Demo — démos d'IA, pas de slides

## TL;DR
- **La démo UI ment** — elle montre un happy path. Toujours montrer l'eval suite.
- **Table avant/après métriques** : precision, recall, F1, hallucination rate, latence, coût
- **Démo adverse obligatoire** : 2-3 prompts hostiles montrant les bordures
- **Transparence > marketing** — la confiance stakeholder s'érode si on cache les limites

## Objectifs canoniques

Inspecter l'incrément, recueillir feedback stakeholders, adapter le backlog.

**Pas** un comité de validation — une **conversation**.

## Format générique (60 min)

| Temps | Activité |
|---|---|
| 0-5 min | Rappel sprint goal + ce qui a été tenté |
| 5-50 min | Démos LIVE des items "Done" |
| 50-55 min | Feedback stakeholders (questions ouvertes, pas validation/rejet) |
| 55-60 min | État du backlog, prochaines priorités candidates |

## Spécificité IA : démo eval, pas démo UI

Pour une feature IA (RAG, agent, classification), **la démo UI ment** — elle montre un happy path. Format Neoteem recommandé en 4 volets :

### 1. Avant/après métriques
Table comparant l'eval suite du sprint précédent vs courant :

| Métrique | Sprint N-1 | Sprint N | Delta |
|---|---|---|---|
| Precision | 0.82 | 0.87 | +6% |
| Recall | 0.76 | 0.81 | +6.5% |
| F1 | 0.79 | 0.84 | +6% |
| Hallucination rate | 5.2% | 3.1% | -40% |
| Latence p95 | 1.4s | 1.1s | -21% |
| Coût/req | $0.018 | $0.012 | -33% |

### 2. Démo adverse
2-3 prompts hostiles montrant les bordures du système :
- Question hors scope ("quel est ton menu de la cantine ?")
- Question piégée (info inexistante demandée comme vraie)
- Question multilingue / accent / typos
- Question manipulation (prompt injection light)

**Pourquoi** : transparence > marketing. Le stakeholder qui découvre les limites en prod = stakeholder perdu.

### 3. Démo business
1 cas client réel anonymisé, avec :
- Le contexte d'usage
- L'output IA
- La **métrique business mesurable** (temps gagné, conversion, satisfaction)

### 4. Eval drift tracker
Si certaines métriques regressent, dire pourquoi **sans détour** :
- "Recall a baissé de 3% car on a élargi le scope queries"
- "Coût a augmenté car nouveau modèle plus performant mais plus cher"

## Anti-patterns

- ❌ **UI polishée d'un agent qui hallucine 30% du temps** → erosion immédiate de la confiance
- ❌ **Démo cherrypicked** : 3 cas parfaits, jamais les ratés
- ❌ **Métriques sans contexte business** : un F1 ne parle à personne au CODIR
- ❌ **Live demo qui crash** : tester 10 fois avant
- ❌ **"Validation" demandée aux stakeholders** : le rôle est feedback, pas approval

## Audience à inviter (équipe IA Neoteem)

| Rôle | Présence |
|---|---|
| Équipe IA (devs, data) | Obligatoire |
| Product Owner | Obligatoire |
| Stakeholders métier | Recommandé (varier selon features) |
| Direction (CTO/CEO) | Mensuel/trim, pas chaque sprint |
| Clients ou users beta | Sur invitation, items finis |

## Préparation (J-1)

1. **Tester les démos** au moins 3 fois
2. **Préparer l'eval suite** : régénérer les métriques à jour
3. **Lister les cas adverses** à montrer
4. **Préparer plan B** si démo live crash (vidéo Loom backup)
5. **Envoyer pre-read** : 1 page résumé des changements + métriques

## Liens

- [[reunions/index]]
- [[sprint-planning-ia-spike]]
- [[retrospective-formats-rotation]]
- [[../strategie/eval-suites-ia]] (à venir)

## Sources

- [Atlassian – What is a Sprint Review](https://www.atlassian.com/agile/scrum/sprint-reviews)
- [Label Studio – ML Evaluation Metrics](https://labelstud.io/learningcenter/machine-learning-evaluation-metrics-what-really-matters/)
- [Lucid – Sprint Review Guide](https://lucid.co/all-access-agile/sprint-review)
