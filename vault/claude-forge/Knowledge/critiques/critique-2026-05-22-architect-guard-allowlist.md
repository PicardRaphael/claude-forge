---
titre: "Critique - Refonte architect-guard blocklist vers allowlist"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - "critique architect-guard allowlist 22 mai"
  - "da refonte hook architect blocklist vers allowlist"
  - "verdict allowlist exhaustive 2 repos"
tags:
  - "#type/critique"
  - "#projet/neo_ia"
  - "#projet/ia_back"
  - "#technique/hooks"
  - "#domaine/claude-code"
sources:
  - "DA 22 mai 2026 - declencheur 12 mocks bloques"
  - "[[raisonnement-kill-tdd-strict-hooks-mai-2026]]"
  - "[[critique-2026-05-21-refonte-hooks-16-vers-6]]"
  - "Commit ia_back 2ae36a3 (purge Drizzle 17 fichiers, 22 mai)"
---

## Devils Advocate - Refonte architect-guard blocklist vers allowlist (ia_back + neo_ia)


**Intention declaree :** Passer le hook architect-guard d une blocklist prefixe (src/double-star, apps/double-star + packages/double-star) a une allowlist stricte de fichiers critiques (env, schemas DB, middleware, auth, routers/dispatchers) avec exemption tests par-pattern, pour debloquer l edition de tests et baisser la friction.

---

### Verdict

**Bloquants :** 4 | **Avertissements :** 8 | **Nitpicks :** 3

**Decision recommandee : BLOQUER la refonte ce soir. LIVRER un fix minimal (exemption tests par-pattern sur le hook actuel) + diagnostic du vrai probleme. Refonte allowlist seulement si recurrence en session fraiche.**

**Limite d evidence explicite :** je n ai PAS lu le code des hooks actuels (architect-guard.py neo_ia, architect-guard.ts ia_back - repos externes, non globbes) ni architect.md ligne 32 (la liste critique source). La critique se fonde sur la proposition + le prior art vault (raisonnement du 21 mai). Sur les 4 bloquants, 2 sont structurels (pattern, doctrine), 2 sont factuels qui pourraient etre leves par lecture des fichiers.

---

### Si je devais le faire marcher malgre mes objections

**Plan en 3 temps, pas refonte d un bloc :**

**Temps 1 - Ce soir (5 minutes, debloque l incident immediat) :**

1. Sur le hook actuel ia_back et neo_ia, AJOUTER uniquement l exemption tests par-pattern :
   - ia_back : double-star/__tests__/double-star, double-star/star.test.ts, double-star/star.spec.ts
   - neo_ia : double-star/tests/double-star, double-star/test_star.py, double-star/star_test.py
2. Garder la blocklist prefixe actuelle (src/double-star et apps/double-star + packages/double-star).
3. Tester en session fraiche : reprendre l incident des 12 mocks, verifier que Edit src/api/routes/__tests__/foo.test.ts PASSE.
4. Capturer 1 cas adverse : Edit src/db/schema/users.ts qui DOIT bloquer.
5. Commit, dormir.

**Temps 2 - Diagnostic prealable AVANT refonte structurelle (30 min, demain en session fraiche) :**

- Lire le hook actuel (architect-guard.py et .ts) pour confirmer la semantique exacte.
- Lire architect.md ligne 32 et confirmer la liste critique source.
- Compter sur 30 jours d historique git combien de bypass par-agent ont ete utilises sur les repertoires guardes. Si plus de 5 occurrences recurrentes hors-tests, preuve d un vrai sur-blocage. Si l incident des mocks est isole, l exemption tests du Temps 1 suffit.
- Decider documente dans le vault : refonte ou pas.

**Temps 3 - Refonte allowlist (seulement si Temps 2 valide) :**

- Refondre 1 repo a la fois (ia_back d abord, plus simple, pas de monorepo).
- Avec une couche dynamique : le hook PARSE un bloc balise dans architect.md (GUARDED-START / GUARDED-END en commentaire HTML) plutot que dupliquer la liste en code. Single source of truth reelle.
- DA fresh sur la version repo 1.
- Test PASS/FAIL en session fraiche (au moins 5 cas : 2 critique vers BLOCK, 2 tests vers ALLOW, 1 fichier ordinaire vers ALLOW).
- 24h d observation production sur repo 1.
- SEULEMENT alors, propager a repo 2.

Pas de propagation simultanee sur 2 repos d un changement structurel. C est feedback_propagate_decisions_cross_repo qui dit propagation explicite, pas propagation simultanee d un changement non eprouve.


---

### Angle Technique - Qu est-ce qui se casse ?

**Objections :**

- **BLOQUANT 1 - drizzle/ dans GUARDED_PREFIXES ia_back alors que Drizzle est PURGE.** La proposition contient litteralement le commentaire inline mentionnant le doute (// migrations Drizzle mais on est sur postgres.js maintenant?) - l auteur de la proposition signale lui-meme le probleme. Le commit 2ae36a3 du 22 mai (purge Drizzle 17 fichiers) + le feedback memoire ia-back-postgresjs-stack-drift-pattern confirment que drizzle/ n a plus de raison d etre dans le hook. Si le repertoire existe encore, on protege un fossile. S il n existe plus, on protege du vide. Allowlist faussement exhaustive. A retirer ou remplacer par src/db/migrations/ apres verif filesystem.

- **BLOQUANT 2 - Ordre d evaluation glob non specifie, donc indetermine.** Cas src/api/routes/__tests__/FooRouter.test.ts : il matche double-star/__tests__/double-star (exemption tests) ET double-star/starRouter.ts ? La proposition ne dit pas si exemption tests gagne sur GUARDED_PATTERNS_GLOB ou l inverse. C est un bloquant d implementation, pas une finesse. Le resultat sera ca marche par accident sur les fichiers que j ai testes.

- **BLOQUANT 3 - Glob patterns case-sensitive et hyphens-sensitive.** double-star/starRouter.ts matche appRouter.ts mais rate :
  - app-router.ts (kebab, pratique TS standard)
  - myrouter.ts (lowercase)
  - Router.ts tout court
  - router.handler.ts

  Idem double-star/dispatcherstar.py rate event_dispatcher.py, route-dispatcher.py. Faux negatifs garantis. Soit regex insensible, soit liste explicite, pas glob naif.

- **AVERTISSEMENT 1 - Allowlist neo_ia : trous critiques probables non listes.** Sans lire la liste source dans architect.md, voici ce que je verifierais empiriquement avant de signer :
  - apps/star/agents/ (configs core agents)
  - alembic/ ou apps/star/db/migrations/ (migrations Alembic, equivalent Python du drizzle)
  - Entrypoints FastAPI : apps/star/main.py, apps/star/app.py
  - apps/star/config/settings.py ou apps/star/core/config.py (config Pydantic)
  - apps/star/api/dependencies.py (FastAPI deps : auth, DB sessions)
  - Dockerfile, docker-compose.yml, Makefile, uv.lock, poetry.lock

  Une allowlist exhaustive n a pas le droit d etre approximative. Si on rate un seul fichier, on a converti la blocklist (un peu trop large) en allowlist (trouee). C est strictement pire : on perd la protection ET on n a pas la liberte qu on cherchait.

- **AVERTISSEMENT 2 - Exemption tests par-pattern = bypass si quelqu un nomme migration.test.ts.** Faible probabilite (pas d attaquant ici), MAIS le risque reel est l erreur honnete : src/db/schema/users.test.ts co-localise qui patche les SCHEMAS au lieu des tests parce que l IA confond import et touche le mauvais fichier. Un fichier .test.ts peut faire fs.writeFile et muter. Le hook protege PreToolUse Write/Edit, pas la semantique du code. Acceptable pragmatiquement, mais a documenter.

- **AVERTISSEMENT 3 - Pas de bypass diff size (option B abandonnee).** Sur des fichiers critiques (src/db/schema/users.ts, 1 caractere typo), on rebloque. Legitime si TOUT changement schema DOIT passer par architect, regression si typos moins de 5 lignes sont safe. A documenter consciemment : pas de bypass taille, pas meme pour les typos. Sinon le 2e incident en session fatiguee declenche un nouvel elargissement et on est en cycle.

- **AVERTISSEMENT 4 - Triplet exemption test + GUARDED_PATTERNS + EXEMPT_PREFIXES : ordre d evaluation a 3 couches.** Cas apps/api/middleware/auth_middleware_test.py : c est un test (allow) ET dans apps/star/api/middleware/ (block). Lequel gagne ? Si exemption tests gagne, on a une voie d edition de middleware sous un nom test. Documenter l ordre canonique : EXEMPT_PREFIXES superieur exemption tests superieur GUARDED_PATTERNS superieur GUARDED_PREFIXES superieur GUARDED_EXACT. Et le coder dans cet ordre, pas dans l ordre ou on y a pense.

- **NITPICK 1 - src/lib/auth (prefixe) capture aussi src/lib/authentication-helpers.ts qui peut etre innocent.** Preferer src/lib/auth/ avec slash terminal, ou liste explicite.

- **NITPICK 2 - apps/star/api/auth non termine par slash : matche apps/api/authority.py si present.**
