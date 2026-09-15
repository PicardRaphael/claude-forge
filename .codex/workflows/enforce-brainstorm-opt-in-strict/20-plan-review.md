# Plan Review

## Status

APPROVED

## Task

enforce-brainstorm-opt-in-strict

## Verdict

Le plan est désormais sûr, complet, proportionné et implémentable : les trois findings antérieurs sont fermés, chaque AC dispose d'un chemin d'implémentation et de vérifications observables, et les contrats Registry existants restent inchangés.

## Reviewed evidence

- `.codex/workflows/enforce-brainstorm-opt-in-strict/00-request.md`, `00-task.md`, `10-plan.md` mis à jour intégralement, précédent `20-plan-review.md` et `.workflow.json`.
- `C:\Users\rapha\.codex\AGENTS.md`, notamment le routeur de mode, les frontières DEV/BRAINSTORM/GENERAL et la politique MCP.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md`, `references/ambiguity-and-escalation.md`, `agents/openai.yaml` et `scripts/init_intake.py`.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md`, `agents/openai.yaml` et `scripts/init_brainstorm.py`.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml`.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py`, `common.py`, `pre_tool_guard.py`, `post_tool_review.py`, `session_context.py`, `subagent_start.py`, `subagent_stop.py` et `registry_engine.py`.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`, `full_self_test.py`, `hooks.template.json`, `install.ps1`, `README.md`, le runtime `hooks/workflow-suite`, `hooks.json` et `config.toml`.
- `C:\Users\rapha\.codex\workflow-registry\registry.json`, `dev-change-delivery@1.0.0` et `brainstorm-product-design@1.2.0`, `1.3.0`, `1.4.0`.
- État Git ciblé : le workflow est non suivi; les changements préexistants des autres workflows sont hors périmètre et n'ont pas été modifiés.

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

- AC-001 : fermé par la grammaire d'activation stricte, le marqueur éphémère du prompt courant et l'interdiction explicite d'initialiser un nouveau target depuis toute provenance historique (`10-plan.md:82-83`, `94`, `103-106`, `115`, `118`, `148`, `158-162`, `169-176`, `214`, `235`).
- AC-002 : fermé par la priorité header > Skill > état persistant, les headers contradictoires fail-closed, le refus des transitions incompatibles et la question parent pour toute ambiguïté (`10-plan.md:81-82`, `96-107`, `145-148`, `169-176`).
- AC-003 : les routes normales 1.2.0/1.3.0 restent à `brief_interview`; le gate USER/BRIEF_VALIDATION et `brief validé` sont figés par snapshots et e2e (`10-plan.md:28`, `43`, `151`, `161`, `186`).
- AC-004 : l'import `APPROVED_CDC_DESIGN@1.4.0`, les trois hashes, les bindings exacts et le pré-dispatch à usage unique restent explicitement préservés (`10-plan.md:29`, `43`, `83`, `89`, `151`, `161-163`, `186`).
- AC-005/AC-006 : les cibles créées ou existantes, le binding de session, le Registry READY, la route managed, la phase, l'acteur, la write policy et la règle toutes-cibles sont définis et testés (`10-plan.md:84-88`, `109-135`, `146`, `149-150`, `159-160`, `177-185`, `205-209`).
- AC-007 : l'inférence sémantique DEV reste au parent sans classifier lexical hook; GENERAL reste read-only. Les MCP distants DEV ne sont pas bloqués par la garde filesystem locale et restent soumis aux contrôles existants (`10-plan.md:26-27`, `81-83`, `105-106`, `132-135`, `150`, `160-163`, `176`, `184`, `207`, `222`, `247`).
- AC-008 : les versions 1.2.0/1.3.0/1.4.0 et leurs routes, phases initiales, gates, transitions, compteurs, artefacts et terminaux restent read-only et couverts par snapshots (`10-plan.md:31`, `43`, `77`, `89`, `151`, `163`, `186`, `204`).
- AC-009 : la matrice obligatoire couvre activations, persistance, continuation, zéro/un/deux candidats, transaction d'initialiseur, outils, cibles, phases positives, gates, routes et import (`10-plan.md:156-186`).
- AC-010 : validation source, installation officielle, validation runtime, parité SHA-256, restart/retrust et états de confiance honnêtes sont distincts (`10-plan.md:90`, `152-153`, `188-210`, `242`, `249`).
- AC-011 : Registry validator, suites source/runtime, inspection finale et exclusions Git/dépôts produit/systèmes externes sont explicites (`10-plan.md:151-154`, `188-200`, `258-262`).

## Scope assessment

Le plan représente le plus petit changement complet pour cette frontière globale : harmonisation des instructions et prompts, marqueur de mode courant, initialisation fail-before-write, binding canonique, garde multi-outils, tests et installation. Il n'ajoute ni workflow, ni route, ni phase, ni artefact, ni dépendance. Le Registry, les dépôts produit, les hooks locaux du dépôt, Git et les systèmes externes restent hors périmètre. `install.ps1` et `hooks.template.json` ne peuvent changer que si un test démontre un manque déterministe.

## Architecture assessment

- PLAN-REVIEW-001 est fermé. La persistance ne sert qu'à continuer le workflow BRAINSTORM compatible déjà lié; toute nouvelle initialisation exige `current_brainstorm_opt_in` issu du prompt courant, y compris pour l'import approuvé (`10-plan.md:82-83`, `103-106`, `115`, `118`, `148`, `174`, `214`, `235`).
- PLAN-REVIEW-002 est fermé. Le fallback mtime disparaît; les cibles absentes/existantes, parents canoniques, reparse points, binding zéro/un/deux candidats et transaction pending/promote sont spécifiés avec reprise et échec déterministes (`10-plan.md:70-73`, `84-87`, `109-122`, `149`, `157-162`, `177-180`, `206`).
- PLAN-REVIEW-003 est fermé. Write/Edit utilisent seulement `file_path`, apply_patch valide tous les headers, Bash autorise seulement les utilitaires exacts, aucun contenu MCP n'est scanné, les capacités filesystem locales échouent fermées sans adaptateur, et les connecteurs remote-only DEV poursuivent les contrôles existants (`10-plan.md:88`, `124-135`, `150`, `160-162`, `181-184`, `207`, `222`, `247`).
- La classification sémantique reste la responsabilité du parent; le hook n'introduit aucun classifier lexical DEV/BRAINSTORM fondé sur la prose.

## Tests and validation assessment

La stratégie est tests-first et falsifiable. Elle exige les matrices rouges avant correction, puis des cas positifs phase par phase. Les tests distinguent syntaxe et narration, prompt courant et provenance historique, continuation et nouvelle initialisation, cibles et contenu, workflow lié et autre task-id, MCP local et distant, gate brief et import approuvé. Les commandes ciblées couvrent Registry, suites source, installation et mêmes suites runtime sans imposer une suite de dépôt produit inutile.

## Security, compatibility, and operational assessment

Le plan échoue fermé aux frontières de mode, workflow, chemin, version/readiness, route, phase, acteur et artefact. `.workflow.json`, l'append-only, les hashes d'import et les gates humains restent protégés. La compatibilité DEV/GENERAL, les versions historiques et les connecteurs distants DEV est explicitement testée. Le rollout sépare source, runtime et trust; aucune approbation utilisateur ni aucun `[hooks.state]` n'est simulé. Le rollback restaure les actifs sauvegardés et réexécute les validations sans supprimer de workflows.

## Validations independently executed

- `py -3 -B ...\task-intake-workflow\scripts\validate_intake.py --workflow-dir ...\enforce-brainstorm-opt-in-strict --registry-root ...\workflow-registry` — réussi.
- `py -3 -B ...\change-delivery-workflow\scripts\validate_handoff.py ...\10-plan.md` — réussi.
- `py -3 -B ...\workflow-registry\validate_registry.py --registry-root ... --agents-dir ... --skills-root ...` — réussi; workflows enregistrés : `brainstorm-product-design`, `dev-change-delivery`, `general-read-only`.
- Inspection read-only des définitions : `brainstorm-product-design@1.2.0` et `@1.3.0` sont READY, avec `DISCOVERY_ONLY` et `FULL_DESIGN` managed à `brief_interview`; `@1.4.0` conserve ces routes et ajoute `APPROVED_CDC_DESIGN` managed à `architecture`.
- Inspection read-only du plan corrigé complet et des sources ciblées de mode, binding, garde, tests, installation et Registry.

## Approved implementation contract

- Implémenter uniquement les étapes 1 à 9 de `10-plan.md`, dans l'ordre tests-first déclaré.
- Exiger un opt-in BRAINSTORM du prompt courant pour tout nouveau target; la persistance autorise seulement la continuation du workflow compatible déjà lié.
- N'autoriser un artefact que pour chaque cible canonique du workflow lié, avec définition/version READY, route managed, phase, acteur et write policy exacts; aucune sélection par mtime.
- Utiliser les adaptateurs par outil et valider toutes les cibles locales; ne jamais traiter le contenu comme destination.
- Refuser les MCP mutateurs en BRAINSTORM/GENERAL; en DEV, séparer capacité filesystem locale et connector remote-only sans contourner les contrôles d'autorisation, scope, write policy ou connector existants.
- Préserver intégralement les versions/routes/gates Registry, l'import approuvé, les dépôts produit, les hooks locaux, Git, les systèmes externes et `[hooks.state]`.
- Exécuter les tests source, l'installation officielle, les mêmes tests runtime, la parité et le smoke post-restart; ne déclarer `TRUSTED_READY` qu'après confirmation humaine observable.

## Residual risks

- La classification MCP local/remote doit être dérivée d'un contrat ou schéma explicite et testé; si cette preuve n'est pas disponible pendant l'implémentation, le développeur doit bloquer plutôt que deviner une capacité.
- Le trust des hooks globaux peut rester non observable automatiquement; utiliser `TRUST_NOT_VERIFIABLE` ou `RESTART_RETRUST_REQUIRED`, jamais READY supposé.
- `.workflow.json` du workflow de revue conserve actuellement les champs Registry/route/phase à `null` malgré le `00-task.md` validé. Il est hook-owned et ne doit pas être édité manuellement; le parent doit appliquer la transition Registry valide avant de lancer l'implémentation.
