---
aliases:
  - ADR
  - architecture decision record
  - RFC
  - request for comments
  - design review
  - decision document
resume: Réunions techniques inter-équipes — ADR Michael Nygard pour capturer les décisions, RFC pour proposer/discuter. Stockés in-repo, versionnés.
derniere-maj: 2026-05-25
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/architecture"
  - "#rituel/technique"
---

# Réunions techniques inter-équipes — ADR & RFC

## TL;DR
- **ADR** = Architecture Decision Record, capture UNE décision et sa rationale (1-3 pages markdown)
- **RFC** = Request for Comments, propose un changement et récolte feedback AVANT décision
- **In-repo, versionné** (`doc/adr/` Markdown) — pas Confluence
- **Workflow** : RFC ouvert 1 semaine → Decision Meeting → ADR rédigé

## ADR (Architecture Decision Record)

### Définition
Document court (1-3 pages) capturant **UNE** décision architecturale et sa rationale.

**Stockage** : dans le repo (`doc/adr/`), en Markdown, versionné Git.

### États
- `proposed` — proposé, en cours de discussion
- `accepted` — accepté, en application
- `superseded` — remplacé par un autre ADR (jamais modifié, supersédé)
- `deprecated` — plus pertinent mais pas remplacé

### Template minimal (Michael Nygard)

```markdown
# ADR-NNN: [Titre court de la décision]

## Status
accepted | proposed | superseded by ADR-NNN

## Context
Pourquoi cette décision est nécessaire. Quelle problématique on adresse.
Quelles forces sont en jeu (techniques, business, équipe).

## Decision
Ce qui est décidé. Phrase active claire : "Nous allons utiliser X parce que Y".

## Consequences
- Positives : ce qui s'améliore
- Négatives : ce qui devient plus difficile
- Neutres : ce qui change sans être bon ni mauvais

## Alternatives considered
- Option A : pourquoi rejetée
- Option B : pourquoi rejetée
- Option C (retenue) : pourquoi
```

### Quand créer un ADR
Décisions qui :
- (a) modifient les frontières d'architecture
- (b) affectent qualité (sécu, perf, scalabilité)
- (c) créent contraintes long terme
- (d) sont coûteuses à inverser

**Pas** d'ADR pour :
- Choix de naming
- Upgrade dépendance mineure
- Refacto local

### Exemples ADR équipe IA

- ADR-001: Choix Mistral Large vs Claude Sonnet pour chatbot prod
- ADR-002: Architecture RAG (BM25 + embedding hybride)
- ADR-003: Build vs Buy reranker (Cohere vs custom)
- ADR-004: Stratégie eval — eval suite vs LLM-as-judge
- ADR-005: Versioning des prompts (semantic vs date)
- ADR-006: Politique fine-tuning vs RAG selon use case

## RFC (Request for Comments)

### Définition
Plus large que l'ADR. Sert à **proposer** un changement et **récolter feedback** avant décision.

- L'**ADR** documente *ce qui a été décidé*
- Le **RFC** documente *ce qu'on propose*

### Template RFC

```markdown
# RFC-NNN: [Titre de la proposition]

## Summary
1-2 phrases résumant la proposition.

## Motivation
Pourquoi changer ? Quel problème on résout ?

## Detailed design
Le cœur de la proposition. Architecture, code, schémas si pertinent.

## Drawbacks
Pourquoi ne PAS faire ça. Coûts. Risques.

## Alternatives
Autres options considérées. Pourquoi celle-ci.

## Open questions
Ce qui n'est pas tranché. Sur quoi on demande feedback.

## Unresolved
Ce qu'on laisse pour un futur RFC.
```

## Workflow canonique 2025

```
1. RFC ouvert (PR ou Confluence)
       ↓
   Commentaires async pendant 1 semaine
       ↓
2. Decision Meeting (30-45 min) — tous ont lu, on tranche
       ↓
3. ADR rédigé qui capture la décision finale
       ↓
   ADR mergé dans `doc/adr/` du repo concerné
```

## Pour Neoteem (multi-repo)

Repos : ia_back, neo_ia, neoteem-brain, bdd, lojii.

- **1 dossier `doc/adr/` par repo**
- **ADR cross-repo** (ex: format API entre ia_back ↔ neo_ia) → dans le repo "leader" + lien depuis l'autre
- **Index ADR** : `doc/adr/README.md` listant tous les ADR du repo
- **Numérotation** : ADR-001, ADR-002... par repo (pas global)

## Design Review meeting

Réunion synchrone 1h max sur RFC déjà lu.

| Temps | Activité |
|---|---|
| 0-10 min | Q&R clarification sur le RFC |
| 10-40 min | Discussion options + objections |
| 40-55 min | Décision (vote ou consensus) |
| 55-60 min | Next steps : qui écrit l'ADR, dans quel repo, deadline |

## Sources d'inspiration externe

- **Rust RFC** : github.com/rust-lang/rfcs (process exemplaire open source)
- **Python PEP** : peps.python.org (numérotation globale)
- **Oxide RFD** : oxide.computer/blog/rfd-1-requests-for-discussion
- **Square RFC** : developer.squareup.com/blog/how-square-writes-rfcs

## Anti-patterns

- ❌ **ADR sans alternatives considered** → décision arbitraire
- ❌ **ADR modifié après acceptance** → casse l'historique. Créer un nouvel ADR qui supersède.
- ❌ **RFC fermé sans décision** → le sujet revient sans cesse
- ❌ **Decision meeting où personne n'a lu** → reporter
- ❌ **Pas d'index ADR** → personne ne sait ce qui existe

## Liens

- [[reunions/index]]
- adr-michael-nygard (à venir, deep dive)
- rfc-process-rust-python (à venir)

## Sources

- [adr.github.io](https://adr.github.io/) — ADR canonical
- [Martin Fowler – ADR](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [AWS Prescriptive Guidance – ADR Process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [ITNEXT – RFCs and ADRs](https://itnext.io/how-to-make-architecture-decisions-rfcs-adrs-and-getting-everyone-aligned-ab82e5384d2f)
