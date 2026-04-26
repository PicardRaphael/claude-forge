# Enrichissement vault — Tickets résolus des 3 derniers mois

Tu enrichis le vault neoteem-brain avec les connaissances issues des tickets SC/SD résolus récents.

**Utilise le skill `neo-brain-support`** pour chercher et écrire dans le vault.
**Utilise le skill `neo-brain`** pour le contexte technique.

## Étape 1 — Récupérer les tickets résolus

Lancer ces 2 JQL en parallèle via `searchJiraIssuesUsingJql` :

```
project = SC AND status in ("Résolu", "Fermé", "CLOTURE") AND resolved >= -90d ORDER BY resolved DESC
```
```
project = SD AND status in ("Résolu", "Fermé", "CLOTURE") AND resolved >= -90d ORDER BY resolved DESC
```

Pour chaque ticket, récupérer : `summary, description, comment, resolution, components, issuetype, issuelinks`.

## Étape 2 — Grouper par pattern

Ne PAS créer une note par ticket. Regrouper les tickets par **symptôme/sujet** :
- 5 tickets sur "erreur appel de fonds" = 1 note `pb-adf-erreur-xxx`
- 3 tickets sur "comment faire un lettrage" = 1 note `faq-lettrage-xxx`
- 2 tickets sur "correction IBAN" = 1 note `proc-correction-iban`

## Étape 3 — Vérifier les doublons dans le vault

Pour chaque pattern identifié, chercher si une note existe déjà :
```
search_brain(query="[symptôme]", limit=3, context=true)
```

| Résultat | Action |
|----------|--------|
| Note existante couvre le sujet | `append_note` avec les nouvelles infos (tickets récents, solutions trouvées) |
| Note existante incomplète | `append_note` pour compléter |
| Aucune note | `create_note` (voir format ci-dessous) |

## Étape 4 — Créer/enrichir les notes

### Bug résolu → `07-Support/problemes-connus/pb-[sujet].md`

```
create_note(path="07-Support/problemes-connus/pb-[sujet].md", content="---
titre: \"Probleme connu — [description courte]\"
resume: \"[1 ligne]\"
aliases:
  - \"[variantes du symptome]\"
domaine: [syndic|gerance|compta|transversal]
public: support
derniere-maj: [YYYY-MM-DD]
auteur: claude
sources:
  - \"[[tickets SC/SD references]]\"
tags:
  - \"#type/support-probleme\"
  - \"#domaine/[xxx]\"
---

## Symptome

[Description du probleme en langage non-technique]

## Cause

[Explication simple de la cause]

## Solution / Contournement

[Ce qui a ete fait pour resoudre — en langage support]

## Tickets concernés

- SC-XXXXX — [résumé] — résolu [date]
- SC-YYYYY — [résumé] — résolu [date]

## Voir aussi

- [[notes-liees]]
")
```

### Question récurrente → `07-Support/faq/faq-[sujet].md`

Même format que les FAQ existantes (voir vault pour le template).

### Action récurrente → `07-Support/procedures/proc-[sujet].md`

Même format que les procédures existantes.

## Étape 5 — Mettre à jour le MOC

Après toutes les créations, lire `MOC-Support` et ajouter les nouvelles notes dans la bonne section.

## Étape 6 — Résumé

```
🧠 Enrichissement vault terminé

📊 Tickets analysés : [N] (SC: [N], SD: [N])
📝 Patterns identifiés : [N]
✅ Notes créées : [N] (pb: [N], faq: [N], proc: [N])
📎 Notes enrichies : [N] (append sur notes existantes)
⏭️ Tickets sans pattern exploitable : [N]

Nouveaux sujets couverts :
- pb-[sujet] — [description courte]
- faq-[sujet] — [description courte]
- ...
```

## Règles

- Langage non-technique (reformulation neo-brain-support)
- 1 pattern = 1 note (atomique, jamais de dump)
- Ne jamais créer de doublon — toujours vérifier avant
- Mettre `derniere-maj` à aujourd'hui
- Minimum 2 tickets sur le même sujet pour créer une note (1 ticket isolé = pas assez de signal)
