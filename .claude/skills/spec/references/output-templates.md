# Output Templates — M / L / XL

Templates stack-agnostic pour les fichiers générés par /spec.
Les paths spécifiques (layers hexagonaux ia_back, modules Python neo_ia) sont déterminés par les rules du repo cible.

---

## Template M — SPEC.md

```markdown
# Spec : <Nom de la feature>

**Type :** Feature | Bug | Refacto
**Taille :** M
**Date :** YYYY-MM-DD
**Statut :** Draft

## Vision

<Ce que la feature doit accomplir, en termes métier. 2-4 phrases. PAS de détails techniques.>

## Architecture

<Décision architecturale et layers touchés. Ex: "Nouveau endpoint POST + use-case + entité + repository.">

## Fichiers à créer / modifier

| Action | Fichier | Raison |
|--------|---------|--------|
| Créer | `<path>` | <raison> |
| Modifier | `<path>` | <raison> |

## Critères d'acceptation

- [ ] <Critère vérifiable>
- [ ] Tests unitaires passent
- [ ] Migration BDD appliquée sans erreur (si applicable)

## Référence BDD

Tables : `<table_a>`, `<table_b>`
Colonnes clés : `<table.colonne (type)>`
Fonctions existantes : `<nom_fonction>()` — <description>

## Approche choisie

**Pragmatic** : <Description concise. 2-3 lignes.>
Alternatives considérées : <Minimal — pourquoi écarté>
```

---

## Template M — BRIEF.md

```markdown
# Brief : <Nom de la feature>

> Ce brief décrit QUOI faire, pas COMMENT. L'architect et les rules du repo gèrent le COMMENT.

## Contexte — Ce qui existe déjà

<Résultats Phase 2 : endpoints/tools/patterns existants similaires.>

## Déjà fait (ne pas refaire)

<Registre des opérations coûteuses déjà effectuées en Phase 2 — une ligne par op, pointeur jamais contenu :>

- `search_brain "<sujet>"` → voir `SPEC.md §<n>`
- lecture `<gros fichier>` → résumé dans `<artefact>`
- audit / requête DB `<cible>` → résultat dans `<artefact>`

<L'agent consulte ce registre AVANT de relancer une recherche/lecture coûteuse.>

## À faire

1. <Action métier 1 — QUOI>
2. <Action métier 2 — QUOI>

## Fichiers à créer / modifier

(Issu de la Phase 2 — pas spéculatif)

- `<path>` — à créer
- `<path>` — à modifier

## Critères de done

- [ ] <Critère 1>
- [ ] <Critère 2>

## Référence BDD

<Tables, colonnes, fonctions PG pertinentes. Logique métier à s'inspirer — ne pas copier.>

## Implementation Notes

Maintenir `docs/implementation-notes/<feature>.md` pendant l'implémentation (pattern running-notes).
Ce fichier capture les décisions prises, les blocages rencontrés et les patterns découverts.

## Skills disponibles pour l'implémentation

- `/go` — finalise et shippe (typecheck + tests + review + commit)
- <autres skills pertinentes selon repo>

## Acceptance Tests

- **Nominal :** <happy path — ex: "endpoint retourne HTTP 200 avec champs attendus">
- **Erreur :** <cas d'erreur — ex: "id inexistant → 404 avec message clair ; invalide → 422">
- **Edge :** <cas limites — ex: "query vide, caractères spéciaux, résultat vide">
- **Niveau suggéré :** unit / integration / functional — l'architect tranche via matrice testing-mandatory.md
```

---

## Template L — Structure multi-BRIEF

```
TODO/feature-<nom>/
  SPEC.md            ← comme M + section Repos touchés + Contrat d'interface
  BRIEF-IA-BACK.md   ← contexte ia_back uniquement
  BRIEF-NEOIA.md     ← contexte neo_ia uniquement
  BRIEF-FRONT.md     ← si front touché (optionnel)
  CONTRADICTIONS.md  ← si contradictions détectées (optionnel)
```

**Additions SPEC.md L** :

```markdown
## Repos touchés

| Repo | Rôle | Ordre |
|------|------|-------|
| ia_back | Backend API | 1 |
| neo_ia | Agents LLM | 2 |

## Contrat d'interface

| Endpoint | Méthode | Payload | Réponse |
|----------|---------|---------|---------|
| `/api/v1/...` | POST | `{ field: type }` | `{ field: type }` |
```

---

## Template XL — Structure complète

```
TODO/feature-<nom>/
  00-vision.md        ← Problème métier, personas, KPIs
  01-architecture.md  ← Décisions archi, ADRs
  02-endpoints.md     ← Tous les endpoints (contrat complet)
  03-tools.md         ← Tools LLM (si agents touchés)
  04-priorites.md     ← Vagues d'implémentation (→ voir decompose-waves.md)
  BRIEF-IA-BACK.md
  BRIEF-NEOIA.md
  BRIEF-FRONT.md      ← si front touché
  EXECUTION-PLAN.md   ← Plan en vagues parallèles (Phase 5)
  CONTRADICTIONS.md   ← si contradictions détectées
```

**04-priorites.md** :

```markdown
# Priorités et ordre d'implémentation

## Vague 1 — Foundation
- [ ] <tâche indépendante 1>
- [ ] <tâche indépendante 2>

## Vague 2 — API (dépend de Vague 1)
- [ ] <tâche>

## Vague 3 — Integration (dépend de Vague 2)
- [ ] <tâche>

## Estimations
| Vague | Complexité | Estimation |
|-------|------------|------------|
| 1 | M | 1-2 jours |
```

---

## Notes de génération

1. Tout contenu vient de Phase 1 (interview) ou Phase 2 (exploration) — jamais spéculatif.
2. **QUOI faire, jamais COMMENT** — les rules du repo (architect, quality-gates) gèrent le COMMENT.
3. Si une info manque → noter "à confirmer" plutôt qu'inventer.
4. "Implementation Notes" obligatoire dans chaque BRIEF — une ligne suffit.
5. "Acceptance Tests" obligatoire dans chaque BRIEF — sans ça, test-writer doit deviner.
