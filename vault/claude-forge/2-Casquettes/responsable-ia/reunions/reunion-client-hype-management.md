---
aliases:
  - réunion client
  - meeting client
  - pitch client
  - hype management IA
  - honest AI communication
  - client meeting IA
resume: Réunion client équipe IA — gérer la hype, l'honnêteté radicale gagne (75% projets IA ratent ROI). Cadrer par le problème, montrer les limites en premier.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/communication"
  - "#rituel/client"
---

# Réunions client — hype management

## TL;DR
- **L'honnêteté radicale gagne** : 75% des projets IA n'atteignent pas leur ROI (IBM)
- **Cadrer par le problème, pas la techno** : "réduire temps de traitement 40%" > "mettre du GPT"
- **Présenter les limites EN PREMIER** : taux hallucination, edge cases, coût
- **Augmenter > remplacer** : positionner IA comme outil humain, plus crédible

## Préparation

- **Agenda diffusé 48h avant**. Objectif explicite (info / décision / co-construction)
- **Pre-read** : 1 doc résumé < 2 pages diffusé avant. Si pas lu → on lit ensemble en début (style Bezos, voir [[codir-6-pager-bezos]])
- **Rôles clairs** : qui pilote, qui répond technique, qui prend les notes/actions
- **Démos testées** au moins 3 fois (cf [[sprint-review-demo-eval-ia]])

## Gérer la hype IA (le piège principal)

### Le contexte 2026
- Aspire 2025 : **50% des entreprises déploient de l'IA**, **< 20% rapportent un impact business clair**
- IBM : **75% des projets IA n'atteignent pas leur ROI attendu**
- Gartner Hype Cycle : trough of disillusionment pour LLM en cours

### Posture Neoteem recommandée — l'honnêteté radicale gagne

#### 1. Cadrer par le problème, pas la techno
- **Bon** : "Vous voulez réduire le temps de traitement des dossiers locataires de 40%"
- **Mauvais** : "On va mettre du GPT"

#### 2. Présenter les limites EN PREMIER
- Taux d'hallucination
- Edge cases connus
- Coût par requête
- Latence
- Dépendances vendor (Anthropic, OpenAI, Mistral)

Le client qui les découvre en prod = client perdu.

#### 3. Trois métriques de ROI obligatoires
- **(a) Gain temps mesurable** (heures économisées/mois)
- **(b) Qualité** (eval suite, taux d'erreur)
- **(c) Coût TCO** incluant supervision humaine, infra, talent

#### 4. Augmenter > remplacer
Positionner l'IA comme **outil humain**, pas remplacement.
- Plus crédible auprès des stakeholders
- Empiriquement plus de ROI (moins de défaillances coûteuses)
- Moins d'angoisse interne (RH, syndicats)

#### 5. Phasage strict
**Pilot mesurable → eval → scale**.

Jamais "scale d'abord, mesure ensuite". Le pilot doit avoir success criteria définis AVANT.

## Anti-patterns clients

- ❌ **Promettre 100% d'automatisation** — chaque % au-delà de 80% coûte exponentiellement plus
- ❌ **Démos cherrypickées sans cas adverses** — perte de confiance dès le premier raté prod
- ❌ **Confondre POC démo et production-grade** — ratio 1:10 au minimum
- ❌ **Vendre "l'IA"** comme produit — vendre la solution au problème
- ❌ **Sur-promettre les délais** — l'IA est imprévisible, surtout R&D

## Agenda type réunion client (1h)

| Temps | Activité |
|---|---|
| 0-5 min | Recap contexte + objectif réunion |
| 5-10 min | Lecture silencieuse pre-read si non lu |
| 10-25 min | Démo (eval + adverse + business — cf [[sprint-review-demo-eval-ia]]) |
| 25-45 min | Discussion : besoins, limites, fit |
| 45-55 min | Next steps, owners, deadlines |
| 55-60 min | Q&A ouvert |

## Cas client difficile : la hype-driven demand

**Situation** : un client demande "tu peux mettre ChatGPT dans notre process X" sans avoir analysé le problème.

**Réponse type** :
1. **Reformuler** : "Si je comprends bien, vous voulez réduire le temps que prend X de Y à Z. C'est bien ça ?"
2. **Proposer un cadrage** : "Avant de choisir la techno, on peut faire un atelier 2h pour mapper le process actuel et identifier les leviers ? L'IA est un outil parmi d'autres."
3. **Documenter** : ADR de la décision si on accepte le scope hype ou si on cadre autrement.

## Sales enablement — armer les commerciaux

Document interne Neoteem à produire :
- **Questions à poser au prospect** : volume, criticité, SLA, dataset existant, budget, baseline humaine
- **Réponses aux objections** : "et si ça hallucine ?", "et le RGPD ?", "et le coût ?"
- **Démos cadrées** : qu'est-ce qu'on montre, qu'est-ce qu'on évite

## Communication crise client

Si incident en prod chez client (cf [[post-mortem-blameless-sre]]) :
1. **Notifier dans l'heure** — pas attendre lundi
2. **Format SCQA** : Situation / Complication / Question / Answer
3. **Plan d'action concret** avec owner + ETA
4. **Post-mortem partagé** (version client-friendly, pas d'attribution interne)
5. **Follow-up à J+7** : "voilà ce qu'on a fait"

## Liens

- [[reunions/index]]
- [[../communication/parler-non-tech-vulgarisation]]
- [[../communication/communication-crise-ia]] (à venir)
- [[../strategie/roi-ia-mesure]] (à venir)

## Sources

- [Aspire – AI Hype vs Reality ROI](https://www.aspireccs.com/the-ai-hype-vs-reality-gap-why-most-companies-arent-seeing-roi-from-customer-communications-ai/)
- [IBM – How to maximize AI ROI 2026](https://www.ibm.com/think/insights/ai-roi)
- [CIO – ROI of AI: Impact > Hype](https://www.cio.com/article/4001889/the-roi-of-ai-why-impact-hype.html)
