# Code Review

## Status

APPROVED

## Task

enforce-brainstorm-opt-in-strict

## Reviewed evidence

- `00-task.md`, plan approuvé, plan review et `30-implementation-report.md` final en mode `REVIEW_CORRECTION`.
- Sources `C:\Users\rapha\.codex\hooks\scripts\common.py` et `pre_tool_guard.py`, copies runtime, tests fast/full et documentation MCP associée.
- Reproductions ciblées source et runtime des capacités exactes MCP, sans appel externe.
- Preuves des rounds précédents pour canonicalisation, junction, file symlink et regular target, plus maintien direct du code et des tests correspondants.
- Registry, parité SHA-256, configuration hooks/trust, sauvegardes et état Git réel.

## Review scope assessment

La troisième correction est strictement limitée à CODE-REVIEW-004 : suppression de l'heuristique de verbes, classification exhaustive de chaque `mcp__*` par ID exact, tests et copie runtime. Les corrections CODE-REVIEW-001 à 003 restent présentes. Aucun changement Registry, dépôt produit, hook projet, Git ou système externe n'a été introduit.

## Finding summary

| Severity | Count |
|---|---:|
| BLOCKING | 0 |
| IMPORTANT | 0 |
| SUGGESTION | 0 |

## Blocking findings

None.

## Important findings

None.

## Suggestions

None.

## Requirement and plan compliance

- CODE-REVIEW-004 est fermé : `pre_tool_guard.py` classifie désormais tout `mcp__*` avant toute décision; un ID inconnu ou conflictuel est refusé dans tous les modes.
- `MUTATING_TOOL_HINTS` et `mutating_mcp_tool()` sont absents des sources et du runtime.
- Les outils read-only exacts sont autorisés; les mutations remote exactes exigent DEV et conservent les contrôles de phase/write policy; les mutations filesystem-local restent désactivées faute d'adaptateur exact.
- CODE-REVIEW-001 reste fermé par la canonicalisation avant classification, les aliases/casse/Win32 refusés et l'adaptateur commun Write/Edit/apply_patch.
- CODE-REVIEW-003 reste fermé par `lstat` de chaque composant jusqu'au fichier, refus reparse et contrôle de résolution directe; le cas fichier régulier reste positif.
- Les AC-001 à AC-011 disposent maintenant d'une implémentation et d'une validation proportionnées. Registry, gates Brainstorm, import approuvé, DEV et GENERAL restent inchangés.

## Functional assessment

Les reproductions qui contournaient les reviews précédentes sont désormais refusées. L'opt-in Brainstorm, la provenance du prompt courant, les bindings déterministes, la transaction pending/promote, le gate de brief et l'import hash-bound n'ont pas régressé. La classification MCP exacte offre quatre résultats fermés : read-only, remote mutation, filesystem-local mutation désactivée, ou unclassified/conflict deny.

## Test assessment

Les tests ciblés couvrent les IDs neutres `modify`, `execute_action` et `apply_operation`, les champs `path`/`destination`, listes et leurres, un read-only exact, une mutation remote DEV exacte et un conflit de contrats. Les full suites source/runtime post-correction sont tracées PASS dans le rapport et l'audit parent; elles n'ont pas été relancées inutilement dans ce round. Le fast runtime a également repassé côté parent. Aucun test valide n'a été affaibli.

## Security, compatibility, and operational assessment

Le default deny s'applique désormais à toute capacité MCP inconnue, indépendamment de son verbe ou de son payload. Les read-only et remote mutations ne sont autorisés que par ID exact non conflictuel; BRAINSTORM/GENERAL continuent de refuser toute mutation classifiée. Les protections de chemins/reparse restent actives. Source/runtime sont identiques, Registry valide, et l'état opérationnel reste honnêtement `RESTART_RETRUST_REQUIRED` avec zéro trust global observable.

## Architecture and maintainability assessment

Une seule autorité, `mcp_tool_capability()`, remplace les deux mécanismes concurrents du round précédent. Les ensembles built-in, enregistrements exacts et table d'adaptateurs vide sont explicites, petits et testables. Le changement reste proportionné sans nouvelle dépendance ni modification du modèle Registry.

## Validations independently executed

| Command or inspection | Result | Notes |
|---|---|---|
| `mcp__filesystem__modify` source/runtime | PASS | Refusé comme capacité non classifiée. |
| `mcp__filesystem__execute_action` source/runtime | PASS | Refusé comme capacité non classifiée. |
| `mcp__filesystem__apply_operation` source/runtime | PASS | Refusé comme capacité non classifiée. |
| `mcp__memory__search` source/runtime | PASS | Read-only exact autorisé. |
| Remote mutation enregistrée en DEV source/runtime | PASS | `mcp__workflow_test_remote__update_record` autorisé sans deny. |
| Contrat read-only + remote conflictuel source/runtime | PASS | Refusé comme unclassified/conflict. |
| Scan `MUTATING_TOOL_HINTS|mutating_mcp_tool` | PASS | Aucune occurrence dans source ou runtime. |
| CODE-REVIEW-001/003 | PASS | Code inchangé; reproductions antérieures et fast tests alias/junction/symlink/regular conservés. |
| Registry validator | PASS | Workflows enregistrés inchangés. |
| Parité source/runtime | PASS | 14 sources, 14 runtime, 0 mismatch. |
| Hooks/trust/scope | PASS with human gate | `hooks.json` égale la dernière sauvegarde, hooks activés, 0 trust global, 10 entrées projet préservées; état `RESTART_RETRUST_REQUIRED`. |

## Review blockers

None.

## Required corrections

None.

## Residual risks

- Le restart/review utilisateur puis un smoke test post-restart restent nécessaires avant de déclarer `TRUSTED_READY`.
- PreToolUse demeure un guardrail et conserve la fenêtre TOCTOU documentée avant l'ouverture filesystem réelle; le sandbox et le moindre privilège restent requis.
- Les nouveaux MCP doivent être enregistrés explicitement comme read-only ou remote mutation, ou recevoir un adaptateur local testé; l'inconnu est volontairement refusé.
