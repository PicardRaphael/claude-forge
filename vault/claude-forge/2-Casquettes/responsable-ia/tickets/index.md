---
aliases:
  - tickets-ia
  - hub-tickets
  - jira-templates
  - tickets-jira
  - user-stories-ia
resume: Hub rédaction tickets dev/design/data/IA — User Stories INVEST, Gherkin, DoR/DoD, templates Jira spike/train/deploy/prompt/agent/data contract, hiérarchie Atlassian.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/tickets"
  - "#stack/atlassian"
---

# Rédaction de tickets — hub

Stack : Jira + Confluence + Figma + Bitbucket. Tous les templates sont en **Markdown Jira** (rendu natif).

## Les 12 templates canoniques (tous inline dans cette note)

| Template | Section | Pour |
|---|---|---|
| User Story DEV | [User Stories INVEST](#user-stories--invest-bill-wake-2003) | Dev classique |
| Bug Report | [Templates phares](#templates-phares--versions-inline) | Bug avec steps to reproduce |
| Design brief | inline ci-dessous | Design WCAG + breakpoints |
| Spike R&D | [Template SPIKE R&D](#template-spike-rd-le-plus-important-pour-équipe-ia) | Recherche timeboxée |
| Train model | [Template TRAIN MODEL](#template-train-model) | Entraînement baseline + cible |
| Deploy model | inline ci-dessous | Déploiement rollback plan |
| Data contract | inline ci-dessous | Pipeline SLA + schema |
| Prompt change | inline ci-dessous | Modif prompt + regression |
| Agent / outil LLM | inline ci-dessous | Agent guardrails + observability |
| Initiative/Epic/Story | [Hiérarchie Atlassian](#hiérarchie-atlassian-native) | Hiérarchie produit |
| DoR / DoD | [DoR vs DoD](#definition-of-ready-vs-definition-of-done) | Definition of Ready/Done |
| Custom fields IA | [Custom fields](#custom-fields-jira-spécifiques-ia-recommandation) | Fields Jira IA |

## User Stories — INVEST (Bill Wake, 2003)

Format canonique Mike Cohn :
```
As a <persona>, I want <action>, so that <outcome/benefit>.
```

| Lettre | Critère | Test rapide |
|---|---|---|
| **I** | Independent | Peut être livré dans n'importe quel ordre |
| **N** | Negotiable | Pas un contrat figé — base de conversation |
| **V** | Valuable | Valeur claire pour user OU business |
| **E** | Estimable | L'équipe peut estimer |
| **S** | Small | Tient dans 1 sprint (idéal : <3 jours) |
| **T** | Testable | Critères d'acceptance vérifiables |

## Job Story (Alan Klement / Intercom) — alternative

```
When <situation/trigger>, I want to <motivation>, so I can <expected outcome>.
```

| Job Story | User Story |
|---|---|
| Persona flou, action universelle | Rôles distincts (admin vs user) |
| Focus causalité, déclencheur | Focus rôle/permissions |
| Recherche/découverte, feature nouvelle | Backlog Agile classique |

**Règle Neoteem** : Job Story pour contexte IA (déclencheur), User Story pour métier.

## Acceptance Criteria — 2 styles

### Gherkin (Given/When/Then)
```gherkin
Scenario: Refus upload si > 10 Mo
  Given un utilisateur authentifié sur /upload
  When il sélectionne un fichier de 15 Mo
  Then il voit message d'erreur "Fichier trop volumineux"
  And l'upload n'est pas envoyé
```

### Checklist
```markdown
- [ ] Le bouton "Exporter CSV" apparaît dans la toolbar
- [ ] Le clic génère un fichier `export_YYYY-MM-DD.csv`
- [ ] Erreur explicite si > 50 000 lignes
```

**Combien d'AC ?** 3 à 7. Au-delà → split. Moins de 3 → sub-task probable.

## Definition of Ready vs Definition of Done

| | DoR | DoD |
|---|---|---|
| Quand | AVANT entrée sprint | APRÈS livraison |
| Officiel Scrum | Optionnel | Oui |
| Risque | Gate toxique si rigide | Non négociable |

## Hiérarchie Atlassian native

```
Initiative   "Améliorer onboarding Neoteem 2026" (trimestre+)
├── Epic    "Refonte signup flow" (2-6 sprints)
│   ├── Story    "As a new user, I want SSO Google" (1 sprint max)
│   │   ├── Sub-task   "Setup OAuth provider" (<1 jour)
│   │   └── Sub-task   "UI button + flow"
```

**Initiative** dispo uniquement Jira Premium "Plans" (ex Advanced Roadmaps).
**Limitation** : pas de niveau ENTRE Epic et Story possible.

## Template SPIKE R&D (le plus important pour équipe IA)

```markdown
h2. 🔬 [Spike] Question à trancher

h3. Hypothèse
[1 phrase falsifiable. Ex : "Embeddings OpenAI text-embedding-3-large 
améliorent recall@5 de >10% vs ada-002 sur notre corpus."]

h3. Timebox
2 jours (échéance : 2026-05-29)

h3. Success criteria
Le spike est terminé quand on peut répondre OUI/NON à :
- [ ] [Q1 — ex. recall@5 mesurable sur eval set Neoteem]
- [ ] [Q2 — ex. coût d'embedding par 1M tokens documenté]

h3. Out of scope
- Implémentation prod
- Bench autres providers

h3. Livrable
Page Confluence "Decision: embeddings v2" contenant :
- Méthode + données utilisées
- Résultats chiffrés
- Recommandation + tickets follow-up

h3. Done
- [ ] Doc Confluence publiée
- [ ] Tickets follow-up créés
- [ ] Présentation 10 min équipe
```

## Template TRAIN MODEL

```markdown
h2. 🧠 [Model] Train v[X.Y] — [objectif]

h3. Baseline
- Modèle actuel : neoteem-classifier-v2.3
- Métriques baseline : F1=0.87, latency p95=320ms

h3. Métriques cibles
|| Métrique || Baseline || Cible || Hard floor ||
| F1 macro | 0.87 | >= 0.88 | 0.85 |
| Latency p95 | 320ms | <= 200ms | 250ms |

h3. Dataset
- Train : `neoteem-train-v2026Q1` (DVC hash: abc123)
- Eval set canonique : `neoteem-eval-frozen-v1` (NE PAS MODIFIER)

h3. Compute & coût
- GPU : 1× A100 80Go, ~6h
- Budget estimé : $40

h3. Done
- [ ] Run loggé MLflow avec params + métriques
- [ ] Métriques >= hard floor sur eval set frozen
- [ ] Pas de régression sur slices critiques
- [ ] Model card mise à jour
- [ ] Modèle enregistré au Model Registry, stage = "Staging"
```

## Custom fields Jira spécifiques IA (recommandation)

| Field | Type | Pour quel ticket |
|---|---|---|
| **Dataset version** | text (DVC hash) | train, eval, data eng |
| **Model registry ID** | text | train, deploy |
| **Eval score baseline** | number | train, prompt |
| **Eval score target** | number | train, prompt |
| **Infra cost estimate** | number ($) | train, deploy, spike |
| **Risk tier IA** | select (low/med/high) | tout ticket IA |
| **Langfuse trace** | URL | bug LLM, eval |
| **Rollback plan** | text long | deploy |
| **Appetite (Shape Up)** | select (S/M/L) | story, epic |

## Erreurs classiques

1. **AC vagues** → exiger Gherkin ou checklist mesurable
2. **Bug sans steps to reproduce** → renvoyer au reporter
3. **Spike sans timebox** → devient zombie, dérive 2 semaines
4. **Story > 1 sprint** → split obligatoire
5. **DoR weaponized** → gate qui bloque tout
6. **Train ticket sans eval set frozen** → optimise un mirage
7. **Deploy sans rollback plan** → 2× plus long quand ça pète
8. **Prompt change sans regression test** → silent regressions
9. **Confondre severity et priority**
10. **Tout en "Must" MoSCoW**

## Sources

- [INVEST — Agile Alliance](https://agilealliance.org/glossary/invest/)
- [Revisiting INVEST — Maarten Dalmijn](https://mdalmijn.com/p/revisiting-invest-20-years-later)
- [Job Stories vs User Stories — Mountain Goat](https://www.mountaingoatsoftware.com/blog/job-stories-offer-a-viable-alternative-to-user-stories)
- [Agile Spikes — Mountain Goat](https://www.mountaingoatsoftware.com/blog/spikes)
- [Definition of Ready — Scrum.org](https://www.scrum.org/resources/blog/ready-or-not-demystifying-definition-ready-scrum)
- [Shape Up: Write the Pitch — Basecamp](https://basecamp.com/shapeup/1.5-chapter-06)
- [Designer's Handbook for Developer Handoff — Figma](https://www.figma.com/blog/the-designers-handbook-for-developer-handoff/)
- [Data Contracts Explained — Atlan](https://atlan.com/data-contracts/)
- [Promptfoo Tutorial](https://nerdleveltech.com/promptfoo-test-llm-prompts-ci-tutorial)
- [Epics, Stories, Initiatives — Atlassian](https://www.atlassian.com/agile/project-management/epics-stories-themes)
