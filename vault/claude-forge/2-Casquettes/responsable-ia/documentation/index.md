---
aliases:
  - documentation-manager
  - hub-documentation
  - cr-decisions
  - confluence-docs
  - ADR-RFC-DACI
resume: Hub documentation manager IA — CR de réunion, decision log, ADR Nygard, RFC, action items SMART, DACI/RACI/RAPID, status reports RAG, handbook GitLab-style.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/documentation"
---

# Documentation manager IA — hub

> Doc-then-discuss : si ça n'est pas écrit, ça n'existe pas.

## Les 14 frameworks

| Framework | Note atomique | Quand l'utiliser |
|---|---|---|
| CR de réunion | [[cr-meeting-template]] | Tracer réunion (Confluence) |
| Decision Register | [[decision-register-index]] | Tracer décisions chronologiquement |
| ADR (Architecture Decision Record) | [[adr-michael-nygard]] | Décision code-near (Bitbucket) |
| MADR / Y-Statement | [[adr-madr-y-statement]] | Variantes ADR |
| RFC process | [[rfc-process-rust-python-oxide]] | Proposer changement substantiel |
| Action items SMART | [[action-items-smart-wwwf]] | Suivi actions réunion |
| DACI | [[daci-decision-framework]] | Décision avec 1 Approver |
| RACI | [[raci-execution-operationnelle]] | Exécution projet standard |
| RAPID | [[rapid-bain-decisions-strategiques]] | Décisions stratégiques avec veto |
| Status reports RAG | [[status-report-rag-watermelon]] | Hebdo/mensuel équipe |
| Confluence best practices | [[confluence-structure-espace]] | Hygiène vault Confluence |
| Team handbook | [[team-handbook-gitlab-style]] | Documentation équipe |
| Model cards IA | [[model-cards-mitchell]] | Documenter modèle prod |
| Postmortem blameless | [[../reunions/post-mortem-blameless-sre]] | Incident |

## Quel doc pour quel besoin

| Besoin | Outil | Stockage |
|---|---|---|
| Tracer une réunion | CR meeting notes | Confluence |
| Tracer décision code-near | ADR Nygard/MADR | Bitbucket `/docs/adr/` |
| Tracer décision produit/process | DACI | Confluence |
| Proposer un changement substantiel | RFC | Confluence ou Bitbucket |
| Suivre des tâches | Action items SMART | Jira (source vérité) + lien Confluence |
| Décider à plusieurs avec veto | RAPID | Confluence |
| Reporter au codir | 1-pager BLUF/SCQA | Confluence |
| Reporter à l'équipe | RAG status hebdo | Confluence |
| Documenter l'équipe | Handbook | Confluence (GitLab-style) |
| Documenter modèle IA | Model card | Confluence ou repo |
| Postmortem incident | Blameless template | Confluence |
| Rétrospective équipe | Rétro template | Confluence |

## ADR — Format Nygard (le plus important)

```markdown
# ADR-014 : Choix du vector store pour NeoChat RAG

## Statut
Accepted — 2026-05-25

## Contexte
[Pourquoi cette décision est nécessaire. Forces en jeu.]

## Décision
[Phrase active claire : "Nous allons utiliser X parce que Y".]

## Conséquences
**Positives** : ...
**Négatives** : ...
**Neutres** : ...

## Alternatives considérées
- Option A : pourquoi rejetée
- Option B : pourquoi rejetée
- Option C (retenue) : pourquoi
```

**États** : `proposed` → `accepted` → `superseded` (jamais modifié, supersédé).

**Quand créer ADR** : décisions qui (a) modifient frontières archi, (b) affectent qualité, (c) créent contraintes long terme, (d) coûteuses à inverser. **Pas** pour naming, upgrade dépendance mineure.

## DACI — Decision Framework Atlassian

| Rôle | Description |
|---|---|
| **D**river | Pilote, organise, propose |
| **A**pprover | **UN SEUL** — décide final |
| **C**ontributors | Apportent expertise |
| **I**nformed | À tenir au courant |

**Règle d'or** : UN seul Approver. Sinon blocage politique garanti.

## RAPID — Bain (décisions stratégiques)

| Rôle | Description |
|---|---|
| **R**ecommend | Propose la décision |
| **A**gree | **VETO** possible |
| **P**erform | Exécute |
| **I**nput | Donne avis non bloquant |
| **D**ecide | **UN SEUL** — décide final |

**Différence avec DACI** : le rôle **Agree** = veto formalisé. Utile pour cross-département avec legal/sécu.

## Action items SMART

| Composant | Règle |
|---|---|
| **S**pecific | Verbe d'action ("Bencher", "Décider", "Livrer") |
| **M**easurable | Mesurable ("doc < 5 pages avec 3 benchs") |
| **A**ssignable | **1 seul owner** (pas "@team") |
| **R**ealistic | Réaliste |
| **T**ime-bound | Deadline absolue (date), pas "ASAP" |

**Source of truth** : Jira pour exécution, Confluence avec lien Jira pour traçabilité réunion.

## Status report RAG (Red/Amber/Green)

Critères objectifs (à fixer une fois) :
- 🟢 Green : tous KPIs dans la cible, pas de risque ouvert sévérité haute
- 🟡 Amber : 1+ KPI hors cible OU 1+ risque non mitigé
- 🔴 Red : date de livraison à risque OU dépassement budget > 15%

**Piège connu** : "watermelon project" (vert dehors, rouge dedans). Forcer critères objectifs.

## Confluence — structure espace IA Neoteem

```
📁 Espace : IA Neoteem
├── 📄 Home (BLUF équipe + liens clés)
├── 📁 1. Décisions
│   ├── 📄 Decision Register
│   ├── 📁 ADRs (mirror Bitbucket /docs/adr/)
│   └── 📁 RFCs
├── 📁 2. Réunions
│   ├── 📁 Codir IA
│   ├── 📁 Sprint reviews
│   ├── 📁 1:1 (par membre)
│   └── 📁 Rétrospectives
├── 📁 3. Status reports
├── 📁 4. Handbook équipe
├── 📁 5. Documentation IA
│   ├── 📁 Model cards
│   ├── 📁 Prompt registry
│   ├── 📁 Eval suites
│   └── 📁 Experiment logs
└── 📁 6. Postmortems
```

**Labels obligatoires** : `decision`, `adr`, `rfc`, `meeting-notes`, `status-report`, `runbook`, `postmortem`, `model-card`, `onboarding`.

## Async communication — hiérarchie canaux

| Besoin | Canal | Délai réponse |
|---|---|---|
| Doc référence durable | Confluence | — (libre) |
| Décision tracée | ADR/DACI | 48-72h |
| Discussion d'idée | RFC | 1-2 semaines |
| Question rapide | Slack DM | 4h ouvrées |
| Annonce équipe | Slack channel | 24h |
| Urgent prod | Slack alerts + @here | 15 min |
| Explication > 5 min | Loom + Confluence | 24h |

## Erreurs classiques

- Notes prises sans owner explicite → action perdue
- Pas de label → notes invisibles 1 mois plus tard
- CR > 1 page sans BLUF → personne ne lit
- ADR édité après "Accepted" → casse l'historique
- "Considered alternatives" vide
- Multi-Approver dans DACI → décision repoussée
- Doc créé puis jamais mis à jour
- Nommer des personnes dans postmortem → tue la culture blameless

## Sources

- [Michael Nygard ADR template](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md)
- [ADR Templates — adr.github.io](https://adr.github.io/adr-templates/)
- [MADR Primer — Olaf Zimmermann](https://www.ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html)
- [DACI Decision template — Atlassian](https://www.atlassian.com/team-playbook/plays/daci)
- [GitLab Handbook-First](https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/)
- [Oxide RFD 1](https://oxide.computer/blog/rfd-1-requests-for-discussion)
- [Rust RFC Process](https://github.com/rust-lang/rfcs/blob/master/text/0002-rfc-process.md)
- [Google SRE — Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [RAPID Decision — Bain](https://www.bain.com/insights/rapid-decision-making/)
- [Model Cards for Model Reporting — Mitchell et al. 2019](https://arxiv.org/abs/1810.03993)
- [BLUF — Wikipedia](https://en.wikipedia.org/wiki/BLUF_(communication))
- [Pyramid Principle — Think Insights](https://thinkinsights.net/strategy/pyramid-principle/)
