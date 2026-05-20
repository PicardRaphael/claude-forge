# Vagues parallèles — Phase 5 (conditionnel XL)

Logique de découpage en vagues pour les features XL. Appelée uniquement depuis Phase 5 de /spec.

---

## Principe des vagues

**Règle d'or** : deux tâches dans la même vague ne touchent jamais le même fichier et aucune ne dépend du résultat de l'autre.

**Test de validation** : peut-on ouvrir N terminaux, coller chaque prompt, et les lancer simultanément sans collision ? Si non, revoir les vagues.

---

## Logique de dépendance standard (couches Neoteem)

- **bdd** : LECTURE SEULE — jamais de tâche de dev dans bdd. Cité en "Référence BDD" dans les prompts.
- **Vague 1** : tâches backend indépendantes + tâches LLM indépendantes (ex: modification de prompt, config agent)
- **Vague 2** : tâches qui dépendent de vague 1 (endpoints créés, tools qui appellent ces endpoints)
- **Vague 3** : intégrations qui dépendent de vague 1 et 2

Exception : si un outil LLM existant peut être adapté sans attendre le backend, il passe en vague 1.

---

## TDD dans chaque vague

Toute tâche touchant du code source suit le pipeline TDD du repo cible :

```
architect (plan + matrice tests)
  → test-writer --phase=red (tests qui échouent)
  → dev (code jusqu'à green)
  → test-writer --phase=refactor (edge cases + coverage)
  → code-reviewer
```

Chaque prompt CC doit fournir des Acceptance Tests (nominaux + erreur + edge) pour que test-writer puisse écrire les tests rouges sans ambiguïté.

---

## Format du prompt de session CC

Chaque tâche = un prompt autonome et suffisant (QUOI faire, pas COMMENT) :

```
Repo cible : [ia_back|neo_ia|autre]
Chemin de travail : ${NEOT_V2_ROOT}/[repo]
Contexte : [CU-XX] - [titre]
Existant : [ce qui existe déjà — noms de fichiers exacts]
Référence BDD : [fonctions PG pertinentes — logique métier à s'inspirer, jamais à copier]
Skills disponibles : [skills utiles dans ce repo]
À faire : [description fonctionnelle précise — QUOI, pas COMMENT]
Critères de done : [CA liés à cette tâche]
Acceptance Tests :
  - Nominal : [happy path]
  - Erreur : [cas d'erreur — ex: "id inexistant → 404 avec message clair"]
  - Edge : [cas limites — ex: "query vide, caractères spéciaux, résultat vide"]
Niveau de tests suggéré : [unit / integration / functional — l'architect tranche via matrice testing-mandatory.md]
```

**Ne PAS inclure** : patterns, conventions, architecture — le workflow du repo s'en charge.

---

## Format EXECUTION-PLAN.md

```markdown
# Plan d'exécution : <Feature>

## Points ouverts

### PO-1 : [Question]
**Réponse trouvée :** [code/vault source]
**Recommandation :** [proposition argumentée]
**Statut :** ✅ Résolu | ⚠️ À confirmer → Bloque : Tâche X.Y

> Si aucun PO : *Aucun point ouvert. Démarrage immédiat possible.*

---

## Existant détecté

| Couche | Ce qui existe | Source |
|--------|---------------|--------|
| bdd (réf) | `f_get_X()` | `sql/X.sql:L42` |
| backend | `GET /endpoint` | `routes/X.ts` |
| LLM | — | — |

---

## Vague 1 — Foundation (N tâches parallèles)

> Pas de dépendances inter-tâches. Lancer simultanément.

### Tâche 1.1 — [titre fonctionnel] (repo: X)

**CU lié :** CU-01
**Dépend de :** Non

**Prompt session CC :**
[voir format ci-dessus]

---

## Vague 2 — [description] (dépend de Vague 1)

> Attendre que toutes les tâches de Vague 1 soient mergées.

[...]

---

## Mapping CA → Tâches

| CA | Description | Tâche(s) |
|----|-------------|----------|
| CA-01 | [description] | 1.1 + 2.1 |
```

---

## Anti-patterns

- **Tâches croisées dans une vague** : deux tâches qui modifient le même fichier → séparer en sous-tâches ou vague séquentielle.
- **Générer du code dans le plan** : non. Le plan contient des prompts CC, pas le code lui-même.
- **Dépendances implicites** : un outil LLM qui mock un endpoint inexistant crée une dette cachée.
- **PO listés sans réponse** : chercher activement dans le vault/repos avant d'exposer un PO.
- **Acceptance Tests absents** : sans eux, test-writer doit deviner → tests arbitraires → hook tdd-guard bloque.
- **Session dev sans tests** : toujours architect → test-writer red → dev. Sauf bypass explicite S triviale (typo, config, doc).
- **Limiter à 3 vagues max** : si plus de 3 vagues nécessaires → subdivision du ticket.
- **Une tâche = une session CC de ~30 min** : si trop grosse, subdiviser.
