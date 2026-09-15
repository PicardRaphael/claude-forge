# Implementation Plan

## Status

READY_FOR_PLAN_REVIEW

## Task

- ID: enforce-brainstorm-opt-in-strict
- Type: BUG

## Classification

- Primary type: BUG
- Secondary tags: SECURITY, INFRASTRUCTURE, AI
- Risk level: HIGH
- Risk justification: le défaut traverse la frontière globale de confiance de Codex: sélection du mode, initialisation de workflows, affectation Registry et autorisation d'écriture dans tous les dépôts. Une correction trop large peut bloquer DEV ou les routes Brainstorm valides; une correction incomplète permet de créer des artefacts de décision sans gate ni acteur autorisé. Le changement reste réversible et ne touche ni données produit ni infrastructure distante, donc il n'est pas CRITICAL.

## Objective

Faire de BRAINSTORM un opt-in strict et vérifiable, conserver l'inférence des demandes DEV explicites et GENERAL en lecture seule, puis refuser par défaut toute écriture d'artefact géré qui n'est pas liée au workflow cible, à sa définition READY, à sa route, à sa phase, à son acteur et à sa write policy exacts.

## Confirmed requirements

- BRAINSTORM ne peut commencer que par une invocation explicite `$project-brainstorm` ou une ligne exacte `MODE: BRAINSTORM`; les mentions narratives de conception, CDC, exigences ou architecture ne sont pas une activation.
- Sans activation explicite, une demande clairement orientée implémentation, bug-fix, refactor, migration, test, configuration ou livraison reste DEV; une demande clairement explicative reste GENERAL; une ambiguïté matérielle impose une question de mode avant toute initialisation.
- GENERAL reste read-only. Aucun mode absent ou ambigu ne peut créer un workflow géré.
- `DISCOVERY_ONLY` et `FULL_DESIGN` commencent toujours à `brief_interview`; `cdc_brainstorm` et `10-cdc.md` restent interdits avant la dernière preuve applicable USER/BRIEF_VALIDATION dont le champ Evidence contient `brief validé` selon la normalisation Registry.
- `APPROVED_CDC_DESIGN` reste exclusivement initialisé par l'importeur snapshot explicite avec les trois hashes fournis ensemble, les bindings locaux exacts et le pré-dispatch à usage unique; aucune prose ne sélectionne cette route.
- `10-cdc.md`, `15-cdc-approval.md`, `20-architecture.md` et `30-review.md` sont fail-closed hors d'un workflow géré READY dont le chemin, la route, la phase, l'acteur et la write policy autorisent exactement la cible.
- Les définitions Registry, versions historiques, routes, phases, gates, transitions, compteurs, artefacts et terminaux existants sont préservés.
- L'installation globale est testée depuis les sources puis depuis le runtime copié. Aucun hash de confiance et aucune approbation utilisateur ne sont fabriqués ou modifiés manuellement.
- Aucun dépôt produit, artefact produit, Git, PR, déploiement ou publication n'entre dans le périmètre.

## Current behavior

- Confirmé: `C:\Users\rapha\.codex\AGENTS.md:35-41` infère actuellement BRAINSTORM à partir de prose de découverte, idée, exigences, CDC ou architecture; le prompt App `skills/task-intake-workflow/agents/openai.yaml` demande lui aussi d'inférer DEV, BRAINSTORM ou GENERAL.
- Confirmé: `hooks/scripts/user_prompt_mode.py:10-38` ne persiste que les headers `MODE`, `INTAKE`, `AUTO-RUN` et `SKIP-INTAKE`; sans mode il n'injecte aucun garde-fou, et `$project-brainstorm` n'est pas enregistré comme provenance d'opt-in.
- Confirmé: `skills/project-brainstorm/agents/openai.yaml` est déjà explicit-only (`allow_implicit_invocation: false`) et son prompt contient `MODE: BRAINSTORM`; ce contrat positif doit rester valide.
- Confirmé: `skills/task-intake-workflow/scripts/init_intake.py:54-167` accepte `--mode AUTO`, BRAINSTORM ou GENERAL et crée `00-request.md` plus `.workflow.json` avant résolution du mode.
- Confirmé: `hooks/scripts/pre_tool_guard.py:310-331` autorise, sans workflow actif, les initialiseurs mutateurs exacts du parent et laisse passer les chemins de workflow ordinaires; ses branches d'autorisation couvrent explicitement `apply_patch`, `Bash` et MCP mais pas les entrées directes `Write`/`Edit` pourtant matchées par `hooks.json`.
- Confirmé: `pre_tool_guard.py:93-106` compare seulement le nom normalisé à la politique du workflow actif choisi par `common.find_active_workflow`; il ne prouve pas que le chemin cible appartient à ce workflow. `common.py:271-285` choisit l'état de session ou le workflow actif le plus récent, pas le workflow dérivé du chemin écrit.
- Confirmé: le Registry courant `brainstorm-product-design@1.4.0` conserve `DISCOVERY_ONLY.start_phase == FULL_DESIGN.start_phase == brief_interview` avec gate USER/BRIEF_VALIDATION, et `APPROVED_CDC_DESIGN.start_phase == architecture`. L'initialiseur normal épingle 1.3.0 à `brief_interview`; l'importeur épingle 1.4.0/APPROVED_CDC_DESIGN à `architecture` avec snapshot.
- Confirmé: les SHA-256 de chaque paire `hooks/scripts/*.py` et `hooks/workflow-suite/*.py` sont actuellement identiques; `~/.codex/hooks.json` appelle `workflow-suite`, et `[features].hooks = true` est présent dans `config.toml`.
- Confirmé: l'état de confiance visible dans `config.toml` référence les hooks locaux de `claude-forge`, pas une preuve suffisante que les définitions globales modifiées ont été revues après installation. L'installateur annonce déjà le restart/review mais ne peut pas accomplir ce gate utilisateur.
- Confirmé: aucun miroir versionné de la suite globale, du Registry ou de ces Skills n'a été trouvé dans `claude-forge`; les hooks locaux `.codex/hooks/*` du dépôt sont une autre suite et restent hors périmètre.

## Root cause

Le symptôme est l'initialisation ou l'écriture possible d'un workflow Brainstorm à partir d'une intention seulement supposée. La cause vérifiée est une chaîne de contrôles permissifs et contradictoires: la politique globale et le prompt d'intake autorisent l'inférence BRAINSTORM; aucun marqueur déterministe ne distingue l'opt-in; les initialiseurs peuvent écrire avant résolution; puis la garde d'outils considère le workflow actif global et un basename autorisé au lieu d'autoriser le chemin canonique du workflow ciblé avec une affectation acteur/phase complète. Les tests actuels figent même l'autorisation des utilitaires mutateurs sans workflow (`full_self_test.py:1229-1242`) et ne couvrent pas la matrice négative Write/Edit/path mismatch.

## Critical flow and blast radius

- Entry point: `UserPromptSubmit` via `hooks/workflow-suite/user_prompt_mode.py`, puis les instructions globales et l'activation App/Skill.
- Execution flow: prompt -> mode/provenance de session -> choix clarification, GENERAL ou DEV, ou initialiseur Brainstorm explicite -> `.workflow.json` hook-owned + `00-request.md` -> gate brief -> `00-task.md` Registry -> `SubagentStart` -> affectation phase/acteur -> `PreToolUse` -> résolution canonique de la cible -> write policy -> artefact.
- Upstream callers: agent parent Codex, activation App `$project-brainstorm`, headers utilisateur, initialiseurs exacts `init_intake.py` et `init_brainstorm.py`, import approuvé.
- Downstream dependencies: session state, `common.find_active_workflow`, `registry_engine` (définition/version/route/phase), hooks `SubagentStart`/`SubagentStop`, validateurs d'intake et Brainstorm, installateur global.
- Consumers and data affected: toutes les sessions/dépôts utilisant les hooks globaux; uniquement état local de workflow et fichiers sous `.codex/workflows/`.
- Intentionally unaffected areas: Registry et versions historiques, contrats des routes et gates, validateurs métier CDC/architecture, import snapshot et dispatch token, workflow DEV après intake, hooks locaux du dépôt, dépôts produit, Git et systèmes MCP externes.

## Relevant files and symbols

- `C:\Users\rapha\.codex\AGENTS.md`: `Session mode router`, `BRAINSTORM boundaries`, `Intake trigger` — autorité sémantique parent pour DEV, GENERAL, opt-in et ambiguïté.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\agents\openai.yaml`: `default_prompt` — supprime l'inférence BRAINSTORM générique.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\SKILL.md` et `references/ambiguity-and-escalation.md`: activation et règle de non-initialisation avant résolution.
- `C:\Users\rapha\.codex\skills\project-brainstorm\SKILL.md`: `Activation boundary` — distingue l'activation initiale explicite de l'usage interne du Skill par un agent déjà affecté.
- `C:\Users\rapha\.codex\agents\task_intake_compiler.toml`: `Registry selection` — interdit de sélectionner BRAINSTORM à partir de prose ou avant l'initialisation spécialisée/gate.
- `C:\Users\rapha\.codex\hooks\scripts\user_prompt_mode.py`: `MODE_RE`, `main` — persistance de la provenance explicite et contexte fail-closed lorsque le mode n'est pas résolu.
- `C:\Users\rapha\.codex\skills\task-intake-workflow\scripts\init_intake.py`: `parse_args`, `main` — refuse un mode non résolu et n'est pas un raccourci d'initialisation Brainstorm/GENERAL.
- `C:\Users\rapha\.codex\hooks\scripts\common.py`: extraction/résolution canonique des cibles de mutation, inventaire déterministe des candidats et identification exacte des utilitaires installés; supprimer le fallback « workflow actif le plus récent ».
- `C:\Users\rapha\.codex\hooks\scripts\session_context.py`: reprise de session — ne lie qu'un binding existant valide ou un candidat unique pendant une reprise explicite/déclarée.
- `C:\Users\rapha\.codex\hooks\scripts\pre_tool_guard.py`: `current_assignment`, `check_workflow_paths`, branche `not workflow`, `main` — réservation d'initialisation et autorisation fail-closed liée à chaque cible, au Registry et à l'acteur.
- `C:\Users\rapha\.codex\hooks\scripts\post_tool_review.py`: promotion ou abandon atomique du binding réservé après vérification du résultat de l'initialiseur.
- `C:\Users\rapha\.codex\hooks\installer\self_test.py`: assertions structurelles, Registry et contrats source.
- `C:\Users\rapha\.codex\hooks\installer\full_self_test.py`: cas runtime end-to-end positifs/négatifs des modes, initialiseurs, gates, acteurs, chemins et artefacts.
- `C:\Users\rapha\.codex\hooks\install.ps1`, `README.md`, `hooks.template.json`, `~/.codex/hooks.json`, `config.toml`: installation, runtime effectif et état de confiance; ne modifier install/template/config que si nécessaire au signal honnête, jamais les hashes `[hooks.state]`.
- `C:\Users\rapha\.codex\workflow-registry\workflows\brainstorm-product-design*.json`: invariants read-only à figer par tests, sans modification attendue.

## Proposed design

1. Définir une table de décision unique dans les instructions globales: seules les intentions de changement explicites listées restent inférées DEV; les demandes clairement read-only sont GENERAL; BRAINSTORM exige la grammaire explicite ci-dessous; tout chevauchement matériel provoque une seule question et aucune initialisation. Aligner le prompt App et les deux Skills/agent d'intake sur cette règle, sans classifier lexical Brainstorm à partir de prose.
2. Dans `user_prompt_mode.py`, analyser les contrôles du prompt courant avant l'état persistant. Un header courant valide est prioritaire; sans header, une invocation Skill courante valide est prioritaire; l'état persistant n'est consulté qu'en absence des deux. Produire pour chaque prompt un marqueur éphémère `current_brainstorm_opt_in=explicit_header|explicit_skill|none`, distinct du mode/provenance persistés qui ne servent qu'à continuer un workflow déjà lié et compatible. Une transition demandée vers un mode incompatible avec un workflow de session encore `active` ou `blocked` est refusée sans altérer le mode/binding cohérent existant et produit une instruction de fermeture, nouveau chat ou reprise conforme.
3. Dans la garde, autoriser `init_brainstorm.py` vers un nouveau target seulement pour le parent/root, par l'invocation exacte déjà parsée, et seulement si le prompt courant porte `current_brainstorm_opt_in=explicit_header` avec `MODE: BRAINSTORM` ou `explicit_skill`. Une provenance ou un mode BRAINSTORM persistés, même issus d'un ancien opt-in valide, n'autorisent jamais une nouvelle initialisation après clôture, déliaison ou absence de workflow compatible: refuser avant toute écriture et demander un nouvel opt-in courant. Continuer d'autoriser le chemin DEV établi, mais refuser `init_intake.py --mode AUTO|BRAINSTORM|GENERAL` avant toute écriture; renforcer le script lui-même pour échouer avant `mkdir` lorsqu'il n'a pas un mode DEV résolu. L'import approuvé emprunte le même initialiseur Brainstorm, exige donc lui aussi l'opt-in du prompt courant, et conserve tous ses arguments/hash checks existants.
4. Remplacer `find_active_workflow` par une résolution liée à la session et au chemin cible. Toute cible, qu'elle existe déjà ou soit en création, doit avoir pour parent canonique direct `<repo-root>/.codex/workflows/<task-id>` et pour nom un artefact direct. Rejeter `..`, sous-répertoire supplémentaire, task-id hors format, ancêtre existant hors racine, symlink ou junction/reparse point sur chaque composant existant entre le repo et la cible. Pour une cible absente, valider le plus proche ancêtre existant puis la suffixe lexicale avant toute autorisation.
5. Le binding `session_state.active_workflow`, après validation canonique, est l'unique autorité. S'il existe mais est absent, incohérent ou incompatible, échouer fermé sans fallback. Sans binding, aucune mutation directe ne choisit un workflow: la reprise à `SessionStart` ou `RESUME_WORKFLOW` peut lier exactement un candidat Registry valide; zéro candidat reste non lié, plusieurs candidats exigent une sélection utilisateur explicite du task-id. Ne jamais choisir le candidat au mtime le plus récent.
6. Traiter un initialiseur exact comme une transaction de binding en deux temps. `PreToolUse` dérive et valide son target canonique depuis les arguments, refuse tout workflow lié incompatible, puis enregistre seulement un `pending_workflow_binding` avec le binding antérieur et une empreinte de l'invocation. `PostToolUse`, ou à défaut le premier `SessionStart`/`PreToolUse`/`SubagentStart` suivant un échec, réconcilie la réservation: promouvoir le target vers `active_workflow` uniquement si les fichiers créés et métadonnées correspondent à l'initialiseur/mode attendus; sinon effacer la réservation, conserver/restaurer le binding antérieur et signaler l'échec sans supprimer un répertoire partiel. `SubagentStart` ne dispatch jamais avant cette réconciliation et la validation du binding final. Ajouter un handler d'échec dédié seulement si les fixtures du runtime prouvent que l'événement existe et est nécessaire.
7. Après binding, exiger pour chaque cible que l'ID/version résolve une définition `enabled=true/readiness=READY`, que la route existe et soit `managed=true`, que la phase courante existe, et que l'acteur de l'événement corresponde exactement à l'affectation parent ou subagent hook-owned. Autoriser ensuite seulement l'artefact exact de `allowed_artifacts`; refuser un autre task-id, sous-chemin, basename, phase, acteur ou artefact. Garder `.workflow.json` interdit et `05-decision-log.md` append-only via l'utilitaire existant.
8. Remplacer la collecte générique de chaînes par les adaptateurs par outil de la table ci-dessous. Une opération multi-cibles est atomiquement refusée si une seule cible est absente, ambiguë, non canonique ou non autorisée; un chemin présent seulement dans le contenu n'est jamais une preuve de destination.
9. Ne pas modifier le Registry. Ajouter des assertions de snapshot sur les start phases, gates, transitions, compteurs et terminaux afin que le durcissement ne puisse les déplacer. Conserver les validations d'import approuvé et de dispatch à usage unique existantes.
10. Installer uniquement après succès des tests source, via `install.ps1`, puis vérifier la parité SHA-256 source/runtime, la présence des handlers globaux et `features.hooks=true`, et relancer les mêmes suites contre `workflow-suite`. Ne jamais écrire `[hooks.state]`. Le rapport doit utiliser des états explicites: `SOURCE_VALIDATED`, `INSTALLED_RUNTIME_VALIDATED`, puis `RESTART_RETRUST_REQUIRED` tant que Raphael n'a pas redémarré/revu les hooks. `TRUSTED_READY` n'est permis qu'après confirmation humaine et smoke test post-restart; absence de mécanisme observable reste `TRUST_NOT_VERIFIABLE`, jamais READY.

### Grammaire et priorité d'activation

Une invocation Skill est valide seulement si, après un éventuel BOM et des lignes vides initiales, le premier token non blanc du prompt est exactement `$project-brainstorm`, terminé par whitespace ou fin de ligne. La ligne ne doit être ni une citation Markdown (`>` comme premier marqueur), ni une liste, ni dans un fenced code block (backticks ou tildes); `` `$project-brainstorm` ``, `\$project-brainstorm`, une mention inline, une négation ou une invocation située après une première ligne de prose sont narratives. Les headers `MODE:` sont reconnus uniquement sur une ligne autonome hors citation/fenced code. Plusieurs headers identiques se réduisent à un; plusieurs valeurs contradictoires rendent le prompt ambigu et interdisent toute initialisation.

| Contrôles du prompt courant | Mode persistant | Workflow lié actif/bloqué | Résultat |
|---|---|---|---|
| Header unique `MODE: X`, avec ou sans Skill | quelconque | absent ou mode X | X gagne; provenance `explicit_header`; si X != BRAINSTORM, ne jamais lancer Brainstorm. |
| Header `MODE: DEV|GENERAL` + première invocation `$project-brainstorm` | quelconque | absent | Le header gagne; Skill ignoré pour l'activation; aucun workflow Brainstorm créé. |
| Header unique `MODE: X` | quelconque | workflow d'un autre mode | Refus de transition; conserver mode et binding cohérents; aucune initialisation; demander fermeture/nouveau chat. |
| Aucun header + première invocation `$project-brainstorm` | DEV ou GENERAL | absent/clos | BRAINSTORM remplace le mode persistant; provenance `explicit_skill`. |
| Aucun header + première invocation `$project-brainstorm` | quelconque | workflow DEV/GENERAL actif ou bloqué | Refus de transition; aucune initialisation; binding existant inchangé. |
| Aucun header ni Skill valide | BRAINSTORM persistant | workflow BRAINSTORM compatible déjà lié `active|blocked` | Continuer uniquement ce workflow lié; `current_brainstorm_opt_in=none`; aucun initialiseur ni nouveau target n'est autorisé. |
| Aucun header ni Skill valide | BRAINSTORM persistant | aucun workflow compatible lié, workflow clos ou session déliée | Conserver au plus le contexte informatif du mode; refuser `init_brainstorm.py`, ne créer aucun target et demander un nouvel `$project-brainstorm` ou `MODE: BRAINSTORM` dans le prompt courant. |
| Aucun header ni Skill valide | DEV ou GENERAL persistant | workflow compatible ou absent | Réutiliser le mode persistant dans ses limites existantes; aucune inférence ni initialisation BRAINSTORM. |
| Aucun header ni Skill valide | aucun | aucun | Appliquer la politique parent: DEV seulement si intention de changement explicite, GENERAL si clairement read-only, sinon poser une question; aucune initialisation pendant l'ambiguïté. |
| Headers MODE contradictoires | quelconque | quelconque | Ambiguïté fail-closed; ne modifier ni mode ni binding; aucune initialisation. |

### Binding et résolution du workflow cible

| État de session/candidats | Opération autorisée |
|---|---|
| Binding canonique valide vers workflow compatible `active|blocked` | Autoritaire pour dispatch et mutations; toute autre cible est refusée. |
| Binding présent mais chemin/métadonnées/Registry invalides | Fail-closed; aucun scan/fallback; demander réparation ou nouvelle session. |
| Aucun binding, zéro candidat valide | Aucune mutation directe ni dispatch; seul un initialiseur exact autorisé par le prompt courant peut réserver un nouveau target. Un ancien mode/provenance BRAINSTORM ne suffit pas. |
| Aucun binding, un candidat valide | Aucune mutation directe avant binding; `SessionStart` de reprise ou `RESUME_WORKFLOW` le lie explicitement et l'annonce, puis les contrôles ordinaires s'appliquent. |
| Aucun binding, plusieurs candidats valides | Fail-closed; demander le task-id à reprendre; jamais de tri par mtime. |
| Initialiseur exact réussi | Après preuve de l'opt-in BRAINSTORM dans le prompt courant et vérification post-tool des fichiers/métadonnées, promouvoir la réservation; le target devient le binding autoritaire avant dispatch. |
| Initialiseur exact échoué ou état créé invalide | Effacer la réservation et conserver/restaurer l'ancien binding; aucun dispatch; ne pas supprimer automatiquement les restes partiels. |
| Initialiseur vers autre target alors qu'un workflow incompatible est lié | Refus PreToolUse; aucun pending binding ni changement d'état. |

Un « candidat valide » est un enfant direct canonique au task-id valide, sans reparse point, avec `.workflow.json`, lifecycle `active|blocked`, définition/version READY résolue et route managed valide. Les workflows clos ne sont pas candidats automatiques; leur reprise exige une action conforme à leur route, pas une sélection implicite.

### Adaptateurs de cibles par outil

| Outil | Source autoritative des cibles | Contrat fail-closed |
|---|---|---|
| `Write` | Champ réel observé `tool_input.file_path` uniquement. | Champ absent/non-string/dupliqué par un alias inconnu: deny pour une écriture gérée. Le contenu n'est jamais scanné comme chemin. |
| `Edit` | Champ réel observé `tool_input.file_path` uniquement. | Même règle que Write; `old_string`/`new_string` ne sont jamais des cibles. |
| `apply_patch` | Tous les headers `*** Add File:`, `*** Update File:`, `*** Delete File:` du patch. | Parser chaque header; refuser header malformé, opération gérée sans cible prouvée ou patch dont une cible échoue. Add valide aussi les parents absents; Delete passe la même policy que Update. |
| `Bash` | Uniquement les utilitaires installés reconnus par `parse_exact_workflow_utility` et les parseurs spécialisés existants (`append_decision`, approved-CDC pre-dispatch). | Aucune écriture shell directe d'un artefact géré n'est nécessaire: elle est refusée, y compris `Set-Content`, redirection, commande chaînée, expansion ou destination calculée. Les artefacts passent par Write/Edit/apply_patch ou l'utilitaire exact. Les utilitaires multi-chemins valident chaque source/target déclaré. |
| MCP mutateur avec capacité filesystem locale | Classifier la capacité depuis le contrat/schéma enregistré de l'outil, jamais depuis une chaîne arbitraire ni l'absence de chemin; allowlist d'adaptateurs locaux initiale vide et aucun `collect_strings`. Une future entrée exige un couple exact `(tool_name, champs de chemin)` avec fixtures versionnées. | BRAINSTORM/GENERAL restent deny intégral. En DEV, aucun MCP ne peut créer/modifier un artefact local géré sans adaptateur local exact; outil filesystem local inconnu, cible locale absente/ambiguë ou artefact géré non prouvé: deny. Une chaîne de chemin dans le contenu n'est jamais une cible. |
| MCP mutateur distant sans capacité filesystem locale | Classification remote-only explicite issue du contrat/schéma enregistré; l'absence d'un champ local ne suffit pas à cette classification. | BRAINSTORM/GENERAL restent deny intégral. En DEV, ne pas refuser l'appel seulement parce qu'il n'expose aucun chemin local: le laisser suivre les contrôles existants d'autorisation utilisateur, scope, write policy et politique connector. Une capacité non classifiée ne peut jamais servir à autoriser l'écriture d'un artefact local géré, mais n'élargit ni ne remplace la décision existante pour une mutation externe. |

Les adaptateurs ne doivent pas élargir les écritures source DEV ordinaires: ils produisent une liste de destinations prouvées pour la garde d'artefacts; l'autorisation finale reste Registry/phase/acteur par cible.

## Alternatives considered

- Corriger seulement `AGENTS.md`: rejeté, car un appel d'initialiseur ou un outil mutateur resterait techniquement autorisé hors workflow.
- Corriger seulement le hook: rejeté, car la classification sémantique DEV/GENERAL/ambiguïté appartient au parent et un hook lexical ne peut pas interpréter sûrement toute prose.
- Ajouter une nouvelle route ou modifier `brainstorm-product-design@1.4.0`: rejeté; les routes actuelles expriment déjà les bons gates et le défaut est en amont et dans l'autorisation d'écriture.
- Protéger uniquement quatre substrings dans les commandes: rejeté; contournable par chemins relatifs/alternatifs et susceptible de faux positifs. L'autorisation doit partir d'un chemin canonique et de la politique Registry du workflow cible.

## Implementation sequence

1. Ajouter d'abord dans `self_test.py` et `full_self_test.py` les cas rouges des quatre matrices ci-dessous: grammaire/priorité de mode, binding zéro/un/deux candidats, transaction d'initialiseur et adaptateurs par outil/toutes-cibles. Vérifier que chaque échec démontre le défaut attendu, pas une fixture invalide. Couvre PLAN-REVIEW-001/002/003 et AC-001/002/005/006/007/009.
2. Aligner `AGENTS.md`, les prompts App, les Skills et `task_intake_compiler.toml` sur la table de décision stricte, sans changer les responsabilités ni les routes. Ajouter des assertions textuelles ciblées évitant le retour de « infer BRAINSTORM ». Couvre AC-001/002/007.
3. Implémenter la grammaire, la priorité header > Skill > persistant, le marqueur éphémère du prompt courant et la règle « persistance = continuation du seul workflow compatible déjà lié, jamais nouvelle initialisation » dans `user_prompt_mode.py`; tester toutes les transitions avant de toucher aux initialiseurs. Couvre PLAN-REVIEW-001 et AC-001/002/007.
4. Remplacer la sélection par mtime dans `common.py`/`session_context.py`, ajouter validation canonique des cibles absentes ou existantes, binding/reprise déterministes et transaction pending/promote dans `pre_tool_guard.py`/`post_tool_review.py`; faire refuser `SubagentStart` sans binding final. Verrouiller ensuite `init_intake.py`. Couvre PLAN-REVIEW-002 et AC-001/002/005/006/009.
5. Implémenter les adaptateurs stricts Write/Edit/apply_patch/Bash et la séparation MCP filesystem-local/remote-only; appliquer la policy à toutes les cibles locales avant une décision allow sans court-circuiter les contrôles connector DEV existants. Exécuter d'abord leur matrice négative, puis les créations/modifications positives phase par phase. Couvre PLAN-REVIEW-003 et AC-005/006/007/009.
6. Renforcer les snapshots Registry et conserver intégralement les scénarios e2e existants `brief validé` et `APPROVED_CDC_DESIGN`; aucune définition JSON ni logique import/dispatch ne change sauf nécessité démontrée par un test. Couvre AC-003/004/008/009.
7. Mettre à jour `hooks/README.md` avec la frontière d'activation, le binding/recovery et les états installation/trust. Ne modifier `install.ps1` ou `hooks.template.json` que si une vérification déterministe manque; ne pas toucher manuellement `hooks.json`, `config.toml` ou `hooks.state`. Couvre AC-010.
8. Après validation source, sauvegarder les fichiers globaux affectés pour rollback, exécuter l'installateur officiel, vérifier handlers/config/parité et exécuter les tests runtime. Produire le rapport d'installation honnête, demander le restart/retrust sans le simuler, puis ne déclarer le runtime trusted-ready qu'après confirmation et smoke post-restart. Couvre AC-010/011.
9. Inspecter les seuls fichiers globaux affectés et les artefacts du workflow DEV; confirmer qu'aucun dépôt produit, hook local `claude-forge`, Registry, Git ou système externe n'a été modifié. Couvre AC-011.

## Tests-first strategy

- First failing test: dans un dépôt temporaire et un état de session vierge, soumettre une prose « conçois l'architecture/CDC » sans header ni Skill, puis tenter l'initialiseur Brainstorm et chacun des quatre artefacts via `apply_patch` et `Write`; attendre absence de workflow et décisions `deny`. Le test courant échoue parce que l'utilitaire et les écritures hors workflow sont permis.
- Unit coverage: grammaire exacte des headers/Skill hors quote/code; priorité et transitions; rejet sans effet de `init_intake --mode AUTO|BRAINSTORM|GENERAL`; target créé/existant; Windows/Unix relatif/absolu, `..`, task-id, sous-chemin, symlink/junction et plus proche ancêtre; définition/version/readiness/route/phase/acteur/write policy invalides; extraction par champs autoritatifs uniquement.
- Integration coverage: hooks `UserPromptSubmit -> PreToolUse -> PostToolUse -> SubagentStart` sur flux normal 1.3.0; distinction continuation liée/nouvelle initialisation après ancien opt-in; binding initialiseur réussi/échoué; reprise zéro/un/deux candidats; créations puis modifications positives de `10-cdc`, `15-cdc-approval`, `20-architecture`, `30-review` à leur phase exacte; refus avant/après phase, autre chemin ou cible partiellement autorisée; décisions MCP local/distant; source et runtime installés.
- End-to-end coverage when justified: conserver et étendre `full_self_test.py` pour `DISCOVERY_ONLY`/`FULL_DESIGN` avec brief gate, puis `APPROVED_CDC_DESIGN` snapshot + pre-dispatch + review terminal; smoke DEV intake et GENERAL sans workflow.
- Edge and failure cases: mention narrative/négative/échappée, inline/fenced code, blockquote, header+Skill et doubles headers contradictoires; opt-in historique après clôture/déliaison; continuation sans nouvel initialiseur d'un workflow compatible lié; workflow actif incompatible; zéro/un/deux candidats; pending binding; `.workflow.json` absent/altéré; version inconnue, readiness non-READY, route non-managed/inconnue, phase inexistante, agent ID/type discordant; path traversal/reparse; leurre dans contenu, cible absente/ambiguë, deux cibles dont une interdite; MCP filesystem local inconnu et connector DEV remote-only; import hash absent/incohérent/altéré.
- Compatibility checks: snapshots exacts des trois routes; version 1.2.0/1.3.0 toujours résolues; DEV `DIRECT/FULL` et bridge Brainstorm-to-DEV toujours valides; hooks projet locaux inchangés.

### Matrice de tests obligatoire

| Groupe | Fixture minimale | Résultat attendu |
|---|---|---|
| Activation positive Skill | Lignes vides puis `$project-brainstorm Design it`; aucun header/workflow | mode BRAINSTORM, provenance `explicit_skill`, initialiseur spécialisé autorisable. |
| Activation narrative | `Explique $project-brainstorm`, `Ne lance pas $project-brainstorm`, `\$project-brainstorm`, inline code, blockquote, liste et fenced code | aucune provenance Skill, aucune inférence BRAINSTORM, aucun workflow créé. |
| Priorité header | Première invocation Skill + `MODE: DEV`, puis + `MODE: GENERAL`, puis + `MODE: BRAINSTORM` | header gagne respectivement DEV/GENERAL/BRAINSTORM; les deux premiers n'initialisent pas Brainstorm. |
| Headers invalides | Deux headers de valeurs différentes hors code | mode/binding antérieurs inchangés, clarification, aucune initialisation. |
| Persistance sans workflow | Skill courant face à DEV/GENERAL persistant; header DEV/GENERAL face à BRAINSTORM persistant | contrôle courant prioritaire, ancien mode remplacé, provenance mise à jour. |
| Ancien opt-in et nouveau target | Activer une fois par header puis par Skill, clore/délier le workflow, envoyer un nouveau prompt narratif sans marqueur et tenter `init_brainstorm.py`; en parallèle, prompt sans marqueur avec workflow BRAINSTORM compatible déjà lié | Après clôture/déliaison, refus avant écriture et aucun nouveau target pour les deux provenances historiques; avec binding compatible, continuation autorisée sans nouvel initialiseur. |
| Transition incompatible | mêmes prompts avec workflow d'un autre mode `active` puis `blocked` | refus, mode/binding cohérents conservés, aucune création. |
| DEV/GENERAL sans contrôle | requête d'implémentation explicite; requête d'explication claire; requête architecture ambiguë | parent choisit DEV; parent choisit GENERAL read-only; ambiguë demande le mode sans workflow. |
| Binding absent | zéro, un, deux candidats valides | zéro: deny; un: binding seulement à SessionStart/RESUME annoncé; deux: deny + demande task-id; jamais mtime. |
| Binding autoritaire | deux candidats, binding explicite sur l'un | dispatch/écriture seulement sur celui lié; autre task-id refusé. |
| Initialiseur | exact réussi, exact échoué sans fichiers, échoué avec état partiel, target incompatible déjà lié | promotion après validation; sinon pending supprimé et ancien binding conservé; incompatibilité refusée avant appel. |
| Cible canonique | artefact absent puis existant; parent direct; sous-répertoire; `..`; task-id invalide; symlink et junction; relatifs/absolus Windows/Unix | créations/modifications directes valides seulement pour le parent canonique; tous contournements refusés. |
| Write/Edit | `file_path` valide; path leurre uniquement dans contenu; champ absent/alias; deux appels ciblant workflow lié/autre workflow | seul `file_path` est lu; absence/alias et autre workflow refusés. |
| apply_patch | Add/Update/Delete uniques; trois headers valides; deux headers dont un interdit; header malformé | toutes les cibles sont extraites et doivent passer; une seule invalide refuse le patch entier. |
| Bash | utilitaire exact valide; utilitaire altéré/chaîné; Set-Content/redirection vers artefact; destination calculée | seul l'utilitaire exact passe selon mode/phase; toutes les écritures shell directes d'artefacts sont refusées. |
| MCP | mutateur quelconque en BRAINSTORM/GENERAL; outil filesystem local synthétique inconnu visant un artefact géré; chemin local seulement dans le contenu; connector synthétique explicitement remote-only en DEV sans champ filesystem | BRAINSTORM/GENERAL refusés; local inconnu et leurre de contenu n'autorisent aucune écriture d'artefact; le connector DEV n'est pas refusé au seul motif qu'il n'expose pas de chemin local et continue vers les contrôles d'autorisation/scope/write policy existants. Aucun appel externe réel. |
| Phases positives | créer puis modifier chaque `10-cdc`, `15-cdc-approval`, `20-architecture`, `30-review` au workflow/phase/acteur exacts via Write et apply_patch | allow uniquement à la phase exacte; autre artefact, acteur, phase ou chemin deny. |
| Gates/routes | gate brief invalide/valide; import snapshot absent/altéré/valide; trois snapshots Registry | comportements existants conservés exactement, y compris start phases et pré-dispatch. |

- Repository-derived commands:
  - `py -3 C:\Users\rapha\.codex\workflow-registry\validate_registry.py --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents --skills-root C:\Users\rapha\.codex\skills`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `py -3 C:\Users\rapha\.codex\hooks\installer\full_self_test.py --scripts C:\Users\rapha\.codex\hooks\scripts --delivery-skill-root C:\Users\rapha\.codex\skills\change-delivery-workflow --intake-skill-root C:\Users\rapha\.codex\skills\task-intake-workflow --brainstorm-skill-root C:\Users\rapha\.codex\skills\project-brainstorm --registry-root C:\Users\rapha\.codex\workflow-registry --agents-dir C:\Users\rapha\.codex\agents`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\rapha\.codex\hooks\install.ps1`
  - Relancer les deux suites ci-dessus avec `--scripts C:\Users\rapha\.codex\hooks\workflow-suite`, puis comparer par SHA-256 chaque `hooks/scripts/*.py` à son homologue runtime et inspecter `~/.codex/hooks.json`/`config.toml` en lecture seule.

## Rollout and rollback

- Rollout local en deux gates: tests source complets, puis sauvegarde des fichiers globaux affectés et installation officielle source -> `workflow-suite`; tests runtime avant tout signal de readiness.
- Le restart/review/retrust Codex est un gate utilisateur distinct. L'agent fournit la commande et l'état, mais ne renseigne jamais les trusted hashes et ne prétend jamais avoir accepté le dialogue.
- Rollback: restaurer les copies pré-changement des instructions, Skills, agents et scripts source, restaurer la sauvegarde `hooks.json.backup-*` produite par l'installateur si nécessaire, réinstaller l'ancien runtime, relancer les tests et redémarrer/revoir à nouveau. Ne pas supprimer de workflows ni réécrire leur `.workflow.json`.
- Trigger de rollback: régression DEV/GENERAL, route Registry déplacée, flux Brainstorm valide bloqué, écriture inter-workflow encore permise, source/runtime divergents ou test runtime non déterministe.

## Architecture fitness checks

- Registry validator et snapshots exacts des routes/gates/transitions/compteurs/terminaux.
- Matrice d'autorisation par `(target workflow, definition readiness, route, phase, actor, artifact)` avec default deny.
- Invariant exécutable: aucun chemin d'exécution ne sélectionne un workflow par mtime; un pending binding invalide restaure le binding antérieur avant tout dispatch.
- Fixtures par adaptateur prouvant que contenu et champs inconnus ne deviennent jamais des destinations, que toutes les cibles locales d'une opération passent ensemble et qu'un connector DEV explicitement remote-only n'est pas bloqué par la garde d'artefacts locaux.
- Parité SHA-256 entre sources `hooks/scripts` et runtime `hooks/workflow-suite`.
- Test sans effet de bord: une activation refusée ne crée ni `.codex/workflows/<id>` ni artefact.
- Vérification distincte `installed`, `runtime validated`, `retrust required`, `trusted ready` dans le rapport final.

## Data and migration impact

Aucune migration ni donnée produit. Le seul état évolutif est le JSON local de session auquel s'ajoutent une provenance persistée de continuation et un marqueur éphémère du prompt courant. Tout état BRAINSTORM, avec ou sans ancienne provenance explicite, ne peut continuer que le workflow compatible déjà lié; sans ce binding, une nouvelle activation explicite courante est exigée, sans réécrire les workflows existants.

## Security and privacy impact

- Le changement ferme une élévation de privilège logique: un basename autorisé dans un workflow ne doit pas autoriser le même artefact ailleurs.
- Les chemins, prompts, arguments d'outils et métadonnées restent non fiables. Toute extraction ambiguë d'une cible gérée est refusée plutôt qu'interprétée.
- L'acteur est vérifié contre l'affectation hook-owned et l'événement, pas seulement contre le mode de session.
- Aucun payload, secret, contenu CDC ou hash de confiance n'est journalisé au-delà des preuves de test synthétiques.
- Les appels MCP mutateurs restent interdits en BRAINSTORM/GENERAL. En DEV, la garde protège les artefacts filesystem locaux; un connector explicitement remote-only reste soumis aux contrôles d'autorisation/scope/write policy existants et n'est pas bloqué pour absence de chemin local.

## Performance and operational impact

Le coût est borné à quelques résolutions de chemins et lectures de petits JSON Registry/métadonnées par mutation. Aucun cache, parallélisme ou nouvelle dépendance n'est justifié. Le principal impact opérationnel est le restart/retrust explicite après installation et la possibilité voulue qu'un ancien état BRAINSTORM sans provenance doive être réactivé.

## Documentation impact

Mettre à jour uniquement les contrats globaux `AGENTS.md`, les Skills/prompts d'intake et Brainstorm concernés, ainsi que `hooks/README.md` pour documenter l'opt-in, la question d'ambiguïté, le fail-closed des artefacts et les états d'installation/trust. Aucun document produit ou documentation du dépôt `claude-forge` n'est modifié.

## Risks

- Faux positif sur une mention de `$project-brainstorm`: atténué par un token d'activation syntaxique testé, pas une recherche de substring.
- Réutilisation d'un ancien opt-in pour ouvrir un nouveau workflow: supprimée en séparant le marqueur du prompt courant de la provenance persistée, laquelle ne vaut que pour la continuation du workflow compatible déjà lié.
- Transition de mode pendant un workflow actif: atténuée par la priorité du prompt courant mais refus de toute transition incompatible tant que le binding actif/bloqué n'est pas fermé.
- Blocage d'un flux DEV naturel: atténué en conservant l'autorisation de l'initialiseur DEV explicite et les tests `DIRECT/FULL`/bridge.
- Confusion entre workflow actif et workflow ciblé: supprimée en dérivant la cible du chemin et en exigeant son égalité avec l'affectation de session.
- Reprise du mauvais workflow parmi plusieurs: supprimée en abolissant le fallback mtime et en exigeant binding existant, candidat unique lors d'une reprise annoncée, ou sélection utilisateur.
- Contournement par Write/Edit/chemin relatif: atténué par un extracteur commun multi-outils et des cas adverses Windows/Unix.
- Régression des gates/import: atténuée par snapshots Registry et maintien des e2e existants, sans modification Registry planifiée.
- Faux READY après copie: atténué par états de readiness séparés et gate utilisateur explicite; l'incertitude de trust reste visible.

## Assumptions

- Les hooks Codex fournissent pour Write/Edit un champ de chemin explicite dans `tool_input`; l'implémentation vérifiera les formes réellement utilisées par les fixtures existantes et refusera toute mutation d'artefact géré dont la cible ne peut être prouvée.
- La classification MCP filesystem-local ou remote-only provient d'un contrat/schéma explicite et testé; un outil non classifié ne peut pas autoriser un artefact local, tandis que les mutations externes DEV continuent d'être décidées par la politique connector existante.
- Les fichiers sous `C:\Users\rapha\.codex\hooks\scripts` sont la source d'installation et `hooks\workflow-suite` le runtime, confirmé par `install.ps1` et les hashes actuels.
- L'absence d'API locale documentée attestant le trust impose une confirmation utilisateur/post-restart; cette absence ne doit pas être transformée en succès supposé.
- Les hooks locaux `.codex/hooks` de `claude-forge` sont indépendants de la suite globale et restent hors périmètre.

## Blocking questions

None.

## Out of scope

- Modifier le contenu ou la version des définitions Registry, ajouter une route/phase/artefact/statut/compteur.
- Reconcevoir les validateurs CDC, architecture ou import approuvé au-delà des tests de non-régression nécessaires.
- Modifier les hooks locaux de `claude-forge`, un dépôt produit, un CDC/approval/architecture/review produit ou `.workflow.json`.
- Automatiser ou simuler le restart, l'acceptation du dialogue de trust ou l'écriture de `[hooks.state]`.
- Commit, push, branche, PR, déploiement, release ou action MCP externe.

## Reviewer checklist

- [ ] AC-001 à AC-011 sont chacune reliées à une étape et à une preuve exécutable.
- [ ] L'autorité sémantique et l'enforcement déterministe sont séparés sans trou entre eux.
- [ ] PLAN-REVIEW-001 est fermé par la grammaire hors quote/code, la priorité header > Skill > persistant, le marqueur éphémère du prompt courant et l'interdiction d'initialiser un nouveau target depuis toute provenance historique; la persistance ne sert qu'à continuer un workflow compatible déjà lié.
- [ ] PLAN-REVIEW-002 est fermé pour cibles absentes/existantes, parent canonique/reparse, binding zéro/un/deux candidats et transaction d'initialiseur sans fallback mtime.
- [ ] PLAN-REVIEW-003 est fermé par les champs autoritatifs Write/Edit, tous les headers apply_patch, Bash exact-only, MCP filesystem-local sans allowlist d'adaptateur et connector DEV remote-only renvoyé vers ses contrôles existants, plus la règle toutes-cibles locales.
- [ ] `$project-brainstorm`/`MODE: BRAINSTORM` restent positifs, mais aucune prose seule ne peut initialiser.
- [ ] DEV naturel, GENERAL read-only et ambiguïté sans workflow sont explicitement testés.
- [ ] Chaque artefact est autorisé uniquement au workflow, chemin, Registry, phase, acteur et write policy exacts.
- [ ] Les trois routes Brainstorm, le gate `brief validé` et l'import snapshot hash-bound sont inchangés.
- [ ] Installation, runtime, trust et readiness sont rapportés séparément sans gate humain simulé.
- [ ] Le périmètre exclut Registry, dépôts produit, hooks locaux, Git et publication.
