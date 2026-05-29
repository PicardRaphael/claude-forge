# BRIEF fixes audit — ia_back

> À coller dans une session Claude Code ouverte **DANS** `C:\Users\raphael.picard_neote\Documents\neot-v2\ia_back`.
> Issu de l'audit `.claude/` multi-repo du 29 mai 2026. Stack : TypeScript / postgres.js.
> Rien n'a été modifié dans ia_back depuis forge — TOUS les fixes ci-dessous restent à faire.

## P1 — à corriger

### FIX 1 — `.claude/hooks/guard-core-imports.ts:32` : triplet MultiEdit incomplet (garde contournable)

**Problème** : le hook matche `Write|Edit|MultiEdit` mais le corps ne lit que `content ?? new_string` (L32). Pour **MultiEdit**, le contenu vient de `edits[]` (jamais lu) → `newContent` vide → `exit` L33. Donc la garde architecturale (core ne doit pas importer `@infra/postgres`) est **contournable via MultiEdit**.

**Référence interne** : `.claude/hooks/meta-commentary-detector.ts:156-171` gère correctement MultiEdit — s'en inspirer pour itérer sur `edits[]` et concaténer les `new_string`.

**Fix** : dans `guard-core-imports.ts`, gérer le cas MultiEdit en lisant tous les `edits[].new_string`. Ajouter un test adverse (édit core important @infra/postgres via MultiEdit → doit bloquer).

### FIX 2 — référence morte « agent sql-optimizer » (fusionné dans skill `sql-optimization`)

L'agent `sql-optimizer` n'existe plus (fusionné dans la skill `sql-optimization`). Fichiers à corriger :
- `.claude/skills/migrate-function/SKILL.md:74,114` — « passer à l'agent `sql-optimizer` » / « déléguer à l'agent sql-optimizer »
- `.claude/skills/update-endpoint/SKILL.md:47,108` — idem (×2)

**Fix** : remplacer les refs « agent sql-optimizer » par la skill `sql-optimization` (ou l'agent `performance-engineer` qui la consomme — vérifier lequel est le bon point d'entrée dans ce repo).
**Bonus** `update-endpoint/SKILL.md:15` — mention « Stack (TypeScript ou Go) » : retirer « ou Go » (résidu template, ia_back = TS).

### FIX 3 — 3 agents : description > 300 chars (auto-trigger dégradé)

Via l'agent-creator du repo (delegate-guard). Condenser sous ~250-300 chars, une seule ligne :
- `.claude/agents/reviewer.md:3` — 399 chars
- `.claude/agents/architect-deep.md:3` — 377 chars
- `.claude/agents/repo-functions-analyzer.md:3` — 329 chars
(surveiller aussi `api-designer.md:3` = 308 et `schema-mapper.md:3` = 300, limite haute)

## P2 optionnels

- `.claude/skills/sql-optimization/SKILL.md:4`, `mapper-test-pattern/SKILL.md:54`, `route-test-pattern/SKILL.md:72` — méta-commentaire « doctrine 22 mai forge » dans le corps (le « pourquoi » devrait vivre dans le vault, pas le SKILL.md). Nettoyage léger.

## Méthode

Pour chaque fix : Read le fichier en entier d'abord, vérifie le réel, applique le diff minimal. Les hooks/skills/agents passent par les agents spécialisés du repo (delegate-guard ia_back). Tests adverses sur le hook FIX 1.
