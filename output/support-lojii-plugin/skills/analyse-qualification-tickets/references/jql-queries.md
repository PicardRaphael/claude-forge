# Requêtes JQL — Support SC/SD

Lancer ces requêtes en parallèle à l'étape 2 de la Phase 1. Remplacer `[mots-clés]` par les termes extraits du titre et de la description du ticket analysé.

---

## Recherche Jira

### Tickets SC/SD similaires résolus (trouver des réponses déjà apportées)

```jql
project in (SC, SD) AND status in ("Résolu", "Fermé", "CLOTURE") AND created >= "2024-12-31" AND text ~ "[mots-clés]" ORDER BY created DESC
```

### Tickets SC/SD ouverts sur le même sujet (détecter une vague en cours)

```jql
project in (SC, SD) AND status NOT IN ("Résolu", "Fermé", "CLOTURE") AND created >= "2024-12-31" AND text ~ "[mots-clés]" ORDER BY created DESC
```

### Tickets N2 résolus liés au sujet (trouver corrections passées)

```jql
project = N2 AND text ~ "[mots-clés]" AND status in ("REPONSE SUPPORT", "CLOTURE", "D.O.R", "EN_COURS") ORDER BY updated DESC
```

### N2 EN COURS sur le même sujet — vérification doublon (OBLIGATOIRE avant création)

```jql
project = N2 AND text ~ "[mots-clés]" AND status NOT IN ("CLOTURE", "Fermé", "REPONSE SUPPORT") ORDER BY updated DESC
```

### Trouver le Module parent N2

```jql
project = N2 AND issuetype = Module AND status not in (CLOTURE, Fermé) AND summary ~ "[mots-clés]" ORDER BY updated DESC
```

### Responsable d'un sujet (remonter au Module/Epic)

```jql
project = N2 AND text ~ "[sujet]" AND issuetype in ("Story fonctionnelle", "Module") ORDER BY updated DESC
```

---

## Requêtes pour la création N2 (Phase 2)

### Sprint en cours (projet N2)

```jql
project = N2 AND sprint in openSprints() ORDER BY updated DESC
```

→ Lire un ticket de ce sprint pour récupérer l'ID numérique du sprint et l'ID de fixVersion.

### Sprints futurs (pour BUG — identifier N+1, N+2, N+3)

```jql
project = N2 AND sprint in futureSprints() ORDER BY startDate ASC
```

→ Le 1er résultat = N+1, le 2ème = N+2, le 3ème = N+3.
→ Lire un ticket dans chaque sprint cible pour récupérer les IDs nécessaires.

---

<!-- Confluence supprimé — le vault neoteem-brain contient déjà ces connaissances -->

---

## Custom fields du Module parent (à récupérer via getJiraIssue)

```
fields: ["summary", "customfield_10081", "customfield_10082", "customfield_10085"]
```

| Champ | Rôle |
|-------|------|
| customfield_10085 | PO Responsable → Intervention BDD |
| customfield_10081 | FRONT Dév Responsable → BUG/BLOQUANT front |
| customfield_10082 | BACK Dév Responsable → BUG/BLOQUANT back |

---

## Champs annuaire complets du Module (pour la recherche de responsables)

| Champ Jira | Rôle |
|------------|------|
| assignee | Assigné (ne pas utiliser pour affecter un N2) |
| customfield_10391 | Responsable du module |
| customfield_10085 | PO (Product Owner) |
| customfield_10081 | FRONT Dév Responsable |
| customfield_10082 | BACK Dév Responsable |
| customfield_10084 | QUALITÉ Responsable |
| customfield_10086 | SUPPORT Responsable |
| customfield_10083 | CONSULTANT Responsable |
| customfield_10001 | Team (équipe rattachée) |
| customfield_10358 | Sous-module |
| customfield_10359 | Domaine fonctionnel |
