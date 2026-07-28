# Plan Review

## Status

APPROVED

## Task

add-approved-cdc-architecture-route

## Verdict

Le plan corrigé est sûr, complet, proportionné et prêt pour implémentation. Il préserve les versions `1.2.0` et `1.3.0`, ajoute une route `1.4.0` strictement bornée à l'architecture et à sa revue indépendante, ferme la frontière de confiance CDC/certificat/décision/hash avant dispatch, conserve les clarifications USER append-only, ne rend jamais le staging visible aux hooks et s'arrête avant DEV. Les cinq findings de la revue précédente sont fermés avec des corrections observables et des tests dédiés.

## Reviewed evidence

- `.codex/workflows/add-approved-cdc-architecture-route/{00-request.md,00-task.md,10-plan.md,20-plan-review.md,.workflow.json}`
- `C:\Users\rapha\.codex\workflow-registry\{registry.json,validate_registry.py,workflows/brainstorm-product-design-1.2.0.json,workflows/brainstorm-product-design.json}`
- `C:\Users\rapha\.codex\skills\project-brainstorm\{SKILL.md,references/handoff-contracts.md,references/pipeline.md,references/workflow-states.md,scripts/init_brainstorm.py,scripts/validate_handoff.py,scripts/append_decision.py}`
- `C:\Users\rapha\.codex\skills\task-intake-workflow\{SKILL.md,references/compiled-task-contract.md,references/routing-and-depth.md,scripts/validate_intake.py}`
- `C:\Users\rapha\.codex\skills\change-delivery-workflow\{SKILL.md,references/handoff-contracts.md,references/workflow-states.md,scripts/validate_handoff.py}`
- `C:\Users\rapha\.codex\agents\{task_intake_compiler.toml,architect_brainstorm.toml,review_brainstorm.toml}`
- `C:\Users\rapha\.codex\hooks\scripts\{common.py,registry_engine.py,pre_tool_guard.py,subagent_start.py,workflow_status.py}`
- `C:\Users\rapha\.codex\hooks\installer\{self_test.py,full_self_test.py}`
- Preuve en lecture seule `E:\Projets IA\Automatisation\.codex\workflows\cdc-maintenance-documentaire-rag-v2-2-officialisation\{.workflow.json,00-task.md,05-decision-log.md,10-cdc.md,15-cdc-approval.md}`
- État Git courant, utilisé uniquement pour confirmer et exclure les nombreuses modifications utilisateur préexistantes sans rapport.

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

## Required changes

None.

## Requirement and acceptance-criteria coverage

- AC-001: couvert par `APPROVED_CDC_DESIGN`, qui commence à `architecture`, réutilise les snapshots locaux et n'inclut aucune phase d'interview, CDC ou approbation.
- AC-002: couvert par la lecture unique des trois preuves, le recalcul des hashes, le statut certificat `APPROVED` et les bindings croisés CDC/certificat/DEC.
- AC-003: couvert par le pré-dispatch parent/root obligatoire avant `spawn_agent`, l'état bloqué observable et la défense en profondeur indépendante de `SubagentStart`.
- AC-004: couvert par les phases existantes `architect_brainstorm/ARCHITECTURE_DESIGN`, `review_brainstorm/DESIGN_REVIEW` et `architect_brainstorm/ARCHITECTURE_REWORK_REVIEW`, exécutées séquentiellement.
- AC-005: couvert par `architecture_rework_cycles`, `repeated_finding_threshold`, l'épuisement fail-closed et `REWORK_CDC -> BLOCKED`.
- AC-006: couvert par les terminaux Brainstorm existants, l'absence totale de phase/agent DEV et la documentation explicite que `GO_DEV*` est seulement un avis.
- AC-007: couvert par la validation read-only de la preuve NeoAutomatisation et les assertions avant/après d'absence de `20-architecture.md` et `30-review.md`.
- AC-008: couvert par les fixtures négatives de preuve, hash, certificat, décision, chemin, prefix et tampering après intake, toutes vérifiées avant spawn.
- AC-009: couvert par l'immutabilité côte à côte `1.2.0/1.3.0`, les tests exact-version et les régressions `DISCOVERY_ONLY`/`FULL_DESIGN`, brief, CDC approval et clarification.
- AC-010: couvert par les extensions génériques et tests négatifs Registry/intake sur ownership, graphe, inputs/outputs, délégation, bindings, version, route et compteurs.
- AC-011: couvert par les mises à jour bornées Registry, Project Brainstorm, Task Intake et hooks, avec commandes Windows exactes, causes de blocage, snapshot/prefix et arrêt avant DEV.

## Closure of previous findings

- `PLAN-REVIEW-001`: fermé. Le nouveau champ générique `parent_append_only_artifacts` déclare `05-decision-log.md` au niveau route; le validateur conserve toutes les contraintes existantes de self-loop, ownership USER/CLARIFICATION, required input et handoff hash. Les tests négatifs refusent ownership absent, mutable ou subagent.
- `PLAN-REVIEW-002`: fermé. Le pré-dispatch parent/root devient l'autorité avant tout appel `spawn_agent`; un échec produit un workflow bloqué avec zéro spawn et zéro événement `SubagentStart`. Le hook post-lancement n'est plus présenté comme une annulation et reste une défense contre contournement ou mutation intercalaire.
- `PLAN-REVIEW-003`: fermé. Seul un `Actor: USER`, `Type: CDC_APPROVAL`, décision affirmative non ambiguë contenant exactement le hash CDC capturé est accepté. `APPROVAL`, rejet/refus, hash absent, différent ou concurrent sont explicitement testés et rejetés.
- `PLAN-REVIEW-004`: fermé. `00-task.md` contient les compteurs registry-native et leurs libellés legacy; les deux validateurs ainsi que la validation complète du workflow réussissent sur le même artefact.
- `PLAN-REVIEW-005`: fermé. Le staging se fait sous `.codex/.workflow-staging/<random-id>`, hors du répertoire inspecté par `workflow_candidates`; la publication est un rename same-volume exclusif et les reruns comparent requête, contrôles, metadata, provenance, prefix et octets de preuve. Les scénarios concurrents et progressés sont couverts.

## Scope assessment

Le plan reste le plus petit changement complet. Il ajoute une route au workflow existant, une extension de schéma Registry justifiée par l'ownership parent sans phase artificielle, un helper d'import partagé, un pré-dispatch parent et les validations/tests/documentations correspondants. Il n'ajoute aucun agent, mode d'agent, phase métier, statut, handoff produit, compteur, workflow DEV ou dépendance externe. Aucun refactor opportuniste n'est inclus.

## Architecture assessment

Le versioning côte à côte correspond au mécanisme exact-version actuel: `1.3.0` est figée byte-for-byte avant mutation et le courant passe à `1.4.0`. Le snapshot local ferme les changements ultérieurs de la source et permet la poursuite si celle-ci devient indisponible. Le champ route-level parent append-only résout proprement le besoin de clarification sans réintroduire un gate d'interview ou d'approbation. La revue demeure indépendante parce que seul `review_brainstorm` possède `30-review.md`, après une architecture validée, et chaque rework retourne ensuite à cette même revue.

## Tests and validation assessment

La stratégie tests-first est suffisante et observable. Elle commence par des attentes `1.4.0` qui échouent sur le Registry actuel, puis couvre parsing de preuves, bindings exacts, chemins et reparse points Windows, lecture/copie des mêmes octets, staging invisible, concurrence, intake, pré-dispatch zéro-spawn, bypass direct de `SubagentStart`, clarification initiale et rework, revue indépendante, compteurs, terminaux et compatibilité historique. Les tests de la preuve réelle restent strictement read-only et ne simulent pas une architecture NeoAutomatisation.

## Security, compatibility, and operational assessment

La frontière externe est traitée comme non fiable: chemins canoniques, noms fixes, containment, hashes fournis, bytes capturés, certificat `APPROVED`, USER `CDC_APPROVAL` exact, décision/hash unique, snapshot immuable et revalidation avant dispatch. L'ownership append-only reste appliqué par le Registry et `PreToolUse`; l'utilitaire parent ancré demeure la seule mutation autorisée pendant une clarification. Les erreurs n'exposent pas les contenus. Les routes historiques, le brief USER, le gate CDC, les hooks Git/MCP et les terminaux avant DEV sont explicitement testés. Le rollout en unité et le maintien du mapping `1.4.0` pendant un rollback préservent les workflows déjà compilés.

## Validations independently executed

- `task-intake-workflow/scripts/validate_intake.py --workflow-dir .codex/workflows/add-approved-cdc-architecture-route`: succès.
- `change-delivery-workflow/scripts/validate_handoff.py .codex/workflows/add-approved-cdc-architecture-route/00-task.md`: succès.
- `change-delivery-workflow/scripts/validate_handoff.py .codex/workflows/add-approved-cdc-architecture-route/10-plan.md`: succès.
- `change-delivery-workflow/scripts/validate_handoff.py --workflow-dir .codex/workflows/add-approved-cdc-architecture-route`: succès avant remplacement du présent handoff.
- `workflow-registry/validate_registry.py --registry-root ... --agents-dir ... --skills-root ...`: succès sur le Registry courant.
- `project-brainstorm/scripts/validate_handoff.py --workflow-dir <preuve NeoAutomatisation>`: succès (`VALID`).
- Hashes recalculés sur la preuve:
  - `05-decision-log.md`: `42F3685B23421FEE16A46F30712EB551CBBA46115CFDD3EAB4FD25838B232383`
  - `10-cdc.md`: `51E861D4F2D581143C4207C860F71699F9AB129F654F243EBF70AAFBE806E8F0`
  - `15-cdc-approval.md`: `E0A0636330BDFBBF94A9F71D0ED33A7A7087B840D2BFFA5DBEF6628C4A0C03D0`
- Inspection de la preuve: certificat `APPROVED`, binding vers le hash CDC attendu, `DEC-055` USER `CDC_APPROVAL` affirmatif avec le même hash; `20-architecture.md` et `30-review.md` absents.
- Hashes de référence observés avant implémentation:
  - `brainstorm-product-design-1.2.0.json`: `E283342E8FCA0272379BB9030FBD6AEAA0E5246B3CD5497F5137FFC6DC90AFA1`
  - définition courante `brainstorm-product-design.json` (`1.3.0`): `3DA4124D8235F6C1C515AE2E88AA50EDEDDCD5FB83B4160CE95F09AB53690BEC`

## Approved implementation contract

- Implémenter uniquement le design et la séquence de `10-plan.md`.
- Figer `1.3.0` avant toute mutation et conserver la résolution exacte `1.2.0/1.3.0/1.4.0`.
- N'autoriser l'architecture importée qu'après validation complète et succès immédiat du pré-dispatch parent; conserver `SubagentStart` comme défense en profondeur.
- Autoriser `05-decision-log.md` uniquement par le contrat route-level parent append-only et l'utilitaire ancré existant.
- Garder le staging hors de `.codex/workflows`, publier atomiquement et ne jamais écraser un workflow différent ou progressé.
- Exécuter les tests-first, les deux validateurs d'intake, le validateur Registry, les self-tests rapides/complets, les compile checks et la validation read-only de la preuve.
- Ne créer aucun artefact d'architecture/revue dans la preuve NeoAutomatisation; ne modifier aucun code produit et n'effectuer aucune action Git de publication.

## Residual risks

- Les fichiers de contrôle globaux sont hors du worktree du dépôt; le développeur doit conserver les checksums/diffs avant-après et une source de rollback effective, puis le code reviewer doit vérifier le scope réel directement sur ces fichiers.
- La robustesse du rename atomique, des reparse points et des chemins cross-drive dépend du comportement Windows réel; les tests prévus doivent être exécutés sur cet environnement, pas uniquement simulés.
- Le parent/root et la décision USER restent la racine de confiance pour les hashes attendus; le snapshot garantit ensuite leur intégrité, pas une identité cryptographique externe.
