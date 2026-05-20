# Stack Conventions — ia_back (TS/Bun) et neo_ia (Python)

Conventions spécifiques à chaque stack. Consultées lors du déploiement de /spec sur un repo.
Le SKILL.md master est stack-agnostic — ces détails s'appliquent repo par repo.

---

## ia_back — TypeScript / Bun

### Runtime et tests
- **Runtime** : Bun (`bun run`, pas `npm run`)
- **Tests** : `bun:test` (pas jest, pas vitest)
- Mentionner dans les Acceptance Tests si le runner doit être précisé

### Architecture hexagonale

```
core/
  entities/       ← Types + validation (Zod)
  ports/          ← Interfaces repository
  use-cases/      ← Business logic
infra/
  repositories/   ← Implémentations Drizzle / postgres.js
  db/schema/      ← Schémas Drizzle (noms colonnes peuvent différer du PG)
api/
  routes/         ← Handlers Hono
  schemas/        ← Validation Zod des payloads
  middleware/     ← Auth, error handling
```

### SQL et BDD
- **Queries complexes** : postgres.js tagged template (`sql\`...\``) — PAS Drizzle ORM
- **Drizzle** : schémas et migrations uniquement
- **Fonctions PG** : lire dans `bdd/sql/` — logique métier à s'inspirer, pas à copier
- **Attention** : noms de colonnes Drizzle peuvent différer du DDL PG — vérifier `infra/db/schema/`

### Frameworks et libs
- **HTTP** : Hono
- **Validation** : Zod
- **Auth** : JWT via middleware Hono (userId extrait du token, jamais passé dans le body)

### Conventions BDD (Neoteem)
- Champ "auteur/créé par" → souvent `TEXT email`, pas `UUID acteur_id`
- Jointures documents/GED → tableau UUID avec opérateur `&&`, pas FK simple
- Table tâches → `t_dossier_action` (pas `t_tache`)
- Schémas Drizzle dans `infra/db/schema/` — source de vérité côté TypeScript

---

## neo_ia — Python / FastAPI

### Runtime et tests
- **Runtime** : Python 3.11+
- **Tests** : pytest + DeepEval pour les agents LLM
- Niveau functional (DeepEval) pour modifications de prompts purs — bypass unit/integration

### Architecture

```
apps/
  neochat/        ← Agent NeoChat
  neomail/        ← Agent NeoMail
  neodoc/         ← Agent NeoDoc
packages/
  shared/         ← Libs partagées (client ia_back, utils)
  tools/          ← Tools agents réutilisables
```

### Agents et tools
- Lire le `config.yaml` de l'agent recommandé avant de l'utiliser — vérifier tools déclarés
- Lire `capabilities.py` pour les catégories existantes
- Client ia_back : vérifier que les champs supposés disponibles sont dans le mapping de réponse

### Conventions BDD cross-repo
- Fonctions PG : référence uniquement — neo_ia appelle ia_back, jamais la BDD directement
- Champs via client ia_back : vérifier `packages/shared/clients/ia_back_client.py`
- Si un champ manque dans le client → ajouter sous-tâche "étendre le client"

---

## Cross-repo — ia_back ↔ neo_ia

### Contrat d'interface
- ia_back = source de vérité pour les IDs persistants
- neo_ia appelle ia_back via Bearer token dans le header Authorization
- Convention nommage à vérifier au cas par cas (snake_case vs camelCase peut varier)

### Exploration cross-repo depuis /spec
- Depuis ia_back : `Glob/Read READ-ONLY` sur `${NEOT_V2_ROOT}/neo_ia`
- Depuis neo_ia : `Glob/Read READ-ONLY` sur `${NEOT_V2_ROOT}/ia_back`
- Les agents d'un repo ne sont PAS accessibles depuis l'autre repo
- `neo-brain-dev-ia` et `mcp__postgres__query` sont disponibles dans les deux repos

### Chemin des repos
- **Variable d'environnement** : `${NEOT_V2_ROOT}` pointe vers `neot-v2/`
- ia_back : `${NEOT_V2_ROOT}/ia_back`
- neo_ia : `${NEOT_V2_ROOT}/neo_ia`
- bdd : `${NEOT_V2_ROOT}/bdd` (lecture seule — jamais de tâche de dev)
