# Interview Bank — Questions par type

Banque de questions pour la Phase 1 de /spec. Max 8-10 questions totales, max 4 par appel AskUserQuestion.

---

## Questions universelles (toujours poser 2-3 parmi celles-ci)

1. **Type** : feature / bug / refacto ?
2. **Repos touchés** : un seul ? ia_back + neo_ia ? Front aussi ?
3. **Critères de succès** : Comment saurons-nous que c'est done ?
4. **Contraintes connues** : Délai, compatibilité, contrainte technique déjà identifiée ?

---

## Feature

### Batch 1 — Scope
- Quel est le besoin métier exact ? (en termes utilisateur, pas technique)
- Quels types d'utilisateurs sont concernés ? (rôles, permissions)
- Y a-t-il déjà quelque chose de similaire dans le code ?

### Batch 2 — Données & Intégration
- Quelles tables BDD sont impliquées (même approximativement) ?
- Est-ce que ça doit s'intégrer avec des agents LLM ou des tools ?
- Y a-t-il un flux de données entrant depuis l'extérieur (webhooks, imports, fichiers) ?

### Batch 3 — Edge cases & tests
- Que se passe-t-il si la donnée n'existe pas ?
- **Cas d'erreur à couvrir** : input invalide, timeout, auth manquante, payload vide ?
- **Critères mesurables** (si LLM) : perf, qualité réponse, tool selection accuracy ?

---

## Bug

### Batch 1 — Diagnostic
- Comportement observé ? Comportement attendu ?
- Reproductible ? Séquence exacte ?
- Depuis quand ? (commit récent, régression ?)

### Batch 2 — Périmètre
- Tous les utilisateurs ou un subset ?
- Logs d'erreur disponibles ?
- Problème en base, dans l'API, ou dans le LLM ?

### Questions de calibration bug
- Le fix implique une migration BDD ? (→ L minimum)
- Le fix touche plusieurs services ? (→ L)

---

## Refacto

### Batch 1 — Motivation
- Pourquoi refactorer maintenant ? (perf, maintenabilité, dette, conformité archi ?)
- Périmètre exact (fichiers, fonctions, patterns) ?
- Tests existants qui couvrent ce code ?

### Batch 2 — Risques
- Code en production active ?
- Dépendances externes (autres services appellent ces endpoints ?) ?
- Rétrocompatibilité API requise ?

---

## Questions de calibration taille (après Phase 2)

- Combien de fichiers distincts à toucher ?
- Migrations BDD à écrire ?
- Modification de plusieurs repos en parallèle ?

---

## Détection format Jira structuré

Si l'argument contient l'un de ces marqueurs, **raccourcir l'interview** aux points non couverts :

| Marqueur | Signification |
|----------|--------------|
| `### Détail métier` | Contexte métier couvert |
| `### Règles de gestion` + `RG-X` | RG formalisées — ne pas réécrire |
| `### Critères d'acceptation` + `CA-X` | CA formalisés — ne pas réécrire |
| `### Contexte technique` | Fichiers/endpoints identifiés — à vérifier (peuvent être périmés) |

---

## Anti-patterns à éviter

- Ne pas demander "Quelle est la priorité ?" — non actionnable pour /spec
- Ne pas demander les détails d'implémentation (COMMENT) — rôle de l'architect
- Ne pas poser > 4 questions dans un seul AskUserQuestion
- Ne pas re-poser une question dont la réponse est dans $ARGUMENTS
