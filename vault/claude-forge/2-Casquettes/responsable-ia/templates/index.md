---
aliases:
  - templates-responsable-ia
  - hub-templates
  - templates-prets-coller
  - confluence-templates
  - jira-templates-ia
resume: Hub templates Confluence/Jira/Markdown prêts à coller — 6-pager, PR-FAQ, ADR, DACI, CR, postmortem, spike, train model, deploy model, prompt change, data contract.
derniere-maj: 2026-05-25
tags:
  - "#type/index"
  - "#casquette/responsable-ia"
  - "#domaine/templates"
---

# Templates prêts à coller — hub

Tous les templates de la casquette responsable-ia, regroupés ici pour copier-coller direct dans Confluence/Jira.

## Communication direction

| Template | Source | Quand |
|---|---|---|
| **6-pager Amazon** | [[exec-6-pager-template]] | Décision CODIR (budget, go/no-go) |
| **PR-FAQ** | [[pr-faq-template]] | Proposer feature IA avant build |
| **Status report hebdo BLUF** | [[weekly-update-bluf-template]] | Vendredi 17h, COO direct |
| **Status report mensuel RAG** | [[status-monthly-rag-template]] | Comex mensuel |
| **Exec summary postmortem** | [[exec-postmortem-summary-template]] | Incident IA majeur |
| **Business case 1 page** | [[business-case-1-page-template]] | Demande budget |

## Réunions

| Template | Source |
|---|---|
| **CR de réunion** | [[../documentation/index]] |
| **Postmortem blameless** | [[../reunions/post-mortem-blameless-sre]] |
| **Rétrospective avec suivi N-1** | [[retro-template]] |
| **Agenda type 1:1** | [[1-on-1-agenda-template]] |

## Décisions

| Template | Source |
|---|---|
| **ADR Nygard** | [[adr-nygard-template]] |
| **MADR (avec alternatives détaillées)** | [[adr-madr-template]] |
| **Y-Statement** | [[adr-y-statement-template]] |
| **RFC** | [[rfc-template]] |
| **DACI** | [[daci-template]] |

## Tickets Jira IA

| Template | Source |
|---|---|
| **User Story** | [[../tickets/index]] |
| **Bug Report** | [[../tickets/index]] |
| **Design brief Figma** | [[../tickets/index]] |
| **Spike R&D** | [[../tickets/index]] |
| **Train model** | [[../tickets/index]] |
| **Deploy model** | [[../tickets/index]] |
| **Data contract** | [[../tickets/index]] |
| **Prompt change avec eval** | [[../tickets/index]] |
| **Agent / outil LLM** | [[../tickets/index]] |

## Documentation IA

| Template | Source |
|---|---|
| **Model card** (Mitchell et al.) | [[model-card-template]] |
| **Eval suite report** | [[eval-suite-report-template]] |
| **Experiment log** | [[experiment-log-template]] |
| **Runbook incident IA** | [[runbook-incident-ia-template]] |

## Templates phares — versions inline

### 6-pager (à dupliquer dans Confluence)

```markdown
# [Projet] — 6-pager — [Date]
Author : Raphael Picard | Decision needed by : [date]

## 1. Context (½ page)
[Pose problème, opportunité, enjeu business chiffré]

## 2. Goals & Tenets (½ page)
Goals (Q[X]) :
- Métrique 1
- Métrique 2
Tenets :
- Principe 1
- Principe 2

## 3. Approach / State of the Business (1,5 page)
Option A — [solution 1] : [pros/cons, coût, délai]
Option B — [solution 2] : [pros/cons]
Option C — [solution 3] : [pros/cons]
Recommandation : [Option X]. Justification : [3 raisons chiffrées]

## 4. Decision asked (½ page)
- Budget : [X k€]
- Arbitrage : [Y]
- Sponsor exec : [Z]

## 5. Risks & Mitigations (1 page)
| Risque | P | I | Mitigation |
|---|---|---|---|

## 6. Open Questions (½ page)
- Question 1
- Question 2

## Appendix
A. Benchmarks
B. État de l'art
C. Cas d'usage similaires
```

### Weekly update BLUF (Slack/email vendredi 17h)

```
[IA Neoteem] Semaine [N] — [date]

>> Headline : [1 phrase qui résume la semaine + impact business]

🟢 Progress
- [Win 1]
- [Win 2]
- [Win 3]

🟡 Watch
- [Risque/observation 1]
- [Risque/observation 2]

🔴 Blocked
- [Blocker 1 + qui peut débloquer]
- (sinon : "rien")

⏭ Next week
- [Top priorité 1]
- [Top priorité 2]
- [Top priorité 3]

📊 KPIs : [KPI 1] | [KPI 2] | [KPI 3]
```

### ADR Nygard (Bitbucket /docs/adr/ADR-NNN.md)

```markdown
# ADR-[NNN] : [Titre court]

## Statut
[proposed | accepted | superseded by ADR-NNN] — [date]

## Contexte
[Pourquoi cette décision est nécessaire. Forces en jeu.]

## Décision
[Phrase active claire : "Nous allons utiliser X parce que Y".]

## Conséquences
**Positives**
- [...]

**Négatives**
- [...]

**Neutres**
- [...]

## Alternatives considérées
- Option A : pourquoi rejetée
- Option B : pourquoi rejetée
- Option C (retenue) : pourquoi

## Liens
- Supersedes : [aucun ou ADR-XX]
- Lié à : [ADR-YY, ADR-ZZ]
```

### Postmortem blameless

```markdown
# Postmortem — Incident [ID] — [titre court] — [date]

## Summary
**Date** : YYYY-MM-DD HH:MM — HH:MM UTC
**Sévérité** : SEV1 / SEV2 / SEV3
**Services impactés** : [...]
**Impact utilisateur** : [...]
**Auteur** : [...]
**Statut** : Final

## Impact
- Users impacted : [...]
- Revenue impact : [...]
- Duration : [...]

## Timeline (UTC)
| Heure | Événement |
|---|---|
| T0 | détection |
| T+15min | containment |
| T+2h | résolution |

## Root cause
[Description NON technique du root cause, focus système pas individu]

## Detection
- TTD (Time To Detect) : [...]
- TTR (Time To Resolve) : [...]

## Where we got lucky
- [...]

## Action items
| # | Action | Owner | Due | Type |
|---|---|---|---|---|
| A1 | ... | @user | YYYY-MM-DD | Prévention/Détection/Réponse/Systémique |

## Lessons learned
- [...]
```

### CR de réunion (Confluence)

```markdown
# [YYYY-MM-DD] — [Titre réunion]

**Type** : Standup | Sync | Codir | 1:1 | Décision | Rétro
**Date** : YYYY-MM-DD — HHhMM-HHhMM
**Animateur** : @raphael.picard
**Présents** : @nom1 @nom2
**Excusés** : @nom4

## Objectif (1 ligne)
[...]

## Agenda
1. [...]
2. [...]

## Décisions
| # | Décision | Décideur | Lien ADR |
|---|---|---|---|

## Actions
| # | Action | Owner | Deadline | Statut | Ticket |
|---|---|---|---|---|---|

## Points discutés
- [...]

## Parking lot
- [...]

## Prochaine réunion
YYYY-MM-DD HH:MM — même format
```

### Spike Jira

```markdown
h2. 🔬 [Spike] [Question à trancher]

h3. Hypothèse
[1 phrase falsifiable]

h3. Timebox
[X jours] (échéance : YYYY-MM-DD)

h3. Success criteria
Le spike est terminé quand on peut répondre OUI/NON à :
- [ ] [Q1]
- [ ] [Q2]

h3. Out of scope
- [...]

h3. Livrable
Page Confluence "[titre]" contenant :
- Méthode + données utilisées
- Résultats chiffrés
- Recommandation + tickets follow-up

h3. Done
- [ ] Doc Confluence publiée
- [ ] Tickets follow-up créés (s'il y a lieu)
- [ ] Présentation 10 min équipe
```

### DACI

```markdown
# Décision : [Sujet]

**Statut** : 🟡 En cours | ✅ Validée
**Driver** : @[toi]
**Approver** : @[UN SEUL]  ← UN SEUL
**Contributors** : @[noms]
**Informed** : @[noms]
**Due date** : YYYY-MM-DD
**Impact** : Faible / Moyen / Élevé

## Outcome attendu
[1 phrase]

## Options considérées (≥ 3 obligatoires)

### Option 1 — [nom]
**Pros** : ...
**Cons** : ...
**Risques** : ...

### Option 2 — [nom]
**Pros** : ...
**Cons** : ...
**Risques** : ...

### Option 3 — [nom]
**Pros** : ...
**Cons** : ...
**Risques** : ...

## Action items (validation)
| # | Action | Owner | Deadline |
|---|---|---|---|

## Décision finale
À compléter par Approver le [date].
```

### PR-FAQ Amazon

```markdown
# FOR IMMEDIATE RELEASE — [date future de lancement]

# [Nom du produit fictif] — [tagline en une phrase]

[Ville, date] — [Entreprise] annonce [produit fictif], qui transforme
[ce que ça fait pour client] en [bénéfice tangible mesurable].

[Paragraphe 1 — La promesse en 3-4 phrases]

[Paragraphe 2 — Le problème client en termes concrets]

[Paragraphe 3 — Comment ton produit le résout]

*"[Citation fictive mais crédible d'un dirigeant Neoteem]"* — [nom, titre]

*"[Citation fictive client — décris le payoff émotionnel]"* — [nom, rôle]

[Comment commencer / disponibilité]

---

## External FAQ
Q : [Question type d'un client/journaliste] ?
R : [Réponse claire]

Q : [Autre question] ?
R : [...]

## Internal FAQ
Q : Quelle est l'économie unitaire ?
R : [...]

Q : Quel est le TAM ?
R : [...]

Q : Quelles dépendances ?
R : [...]

Q : Faisabilité technique ?
R : [...]

Q : Risques majeurs ?
R : [...]
```

## Sources

- [Amazon 6-Pager Guide — Visme](https://visme.co/blog/amazon-6-pager/)
- [PR-FAQ — Coda](https://coda.io/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq)
- [ADR Templates — adr.github.io](https://adr.github.io/adr-templates/)
- [DACI template — Atlassian](https://www.atlassian.com/software/confluence/templates/decision)
- [Postmortem template — Google SRE](https://sre.google/sre-book/example-postmortem/)
- [Atlassian Meeting Notes](https://www.atlassian.com/software/confluence/templates/meeting-notes)
