# Task

## ID

add-approved-cdc-architecture-route

## Mode

DEV

## Intake depth

DEEP

## Workflow ID

dev-change-delivery

## Workflow version

1.0.0

## Workflow readiness

READY

## Delivery path

FULL

## Type

FEATURE

## Initial risk

HIGH

## Title

Ajouter une route d'architecture depuis un CDC externe déjà approuvé

## User request

Ajouter au workflow Registry de conception produit une route réutilisable qui accepte un CDC externe déjà approuvé et son certificat d'approbation, vérifie leurs empreintes exactes, puis enchaîne l'architecture et sa revue indépendante sans refaire l'interview, le CDC ni son approbation.

## Expected outcome

Le registre installé expose une route réutilisable et validée qui échoue de manière fermée lorsque le CDC ou son approbation manque, est incohérent ou ne correspond pas aux empreintes déclarées. Après validation des preuves, la route exécute l'architecte, la revue de conception et un rework borné si nécessaire, puis atteint un état terminal avant toute phase DEV.

## Constraints

- Modifier uniquement l'infrastructure de workflow nécessaire à cette fonctionnalité, avec le diff complet minimal et les validations associées.
- La route cible appartient à `brainstorm-product-design`; ne pas créer un nouveau workflow ni inventer un agent, un mode d'agent, une phase, un statut, une transition, un artefact ou un compteur hors du contrat Registry.
- Réutiliser les agents Registry `architect_brainstorm` et `review_brainstorm` dans l'ordre demandé; la revue de conception doit rester indépendante.
- Ne pas relancer l'interview, la génération du CDC ou le gate d'approbation lorsque les preuves externes valides ont été importées et liées.
- Vérifier les empreintes SHA-256 exactes du CDC et du certificat d'approbation avant toute architecture; toute preuve absente, modifiée, non approuvée ou incohérente doit bloquer la route.
- Conserver les gates humains et l'interdiction d'auto-approbation applicables; `AUTO-RUN: YES` ne les contourne pas.
- Le cas NeoAutomatisation est une preuve en lecture seule pour cette fonctionnalité générique, pas une autorisation d'exécuter son architecture ni de démarrer son développement.
- Ne produire aucune architecture produit, ne modifier aucun code produit et n'effectuer aucune action Git de commit, push, merge ou publication.
- Ne pas modifier `.workflow.json` manuellement.
- Préserver la compatibilité des routes existantes et des workflows déjà compilés, sauf changement explicitement justifié et validé par le plan.

## Known context

- Le registre installé est `C:\Users\rapha\.codex\workflow-registry\registry.json`, version de registre `2.0.0`.
- Le workflow DEV sélectionné pour livrer ce changement est `dev-change-delivery` version `1.0.0`, readiness `READY`, route gérée `FULL`.
- La cible fonctionnelle du changement est la définition Registry courante du workflow de conception produit.
- La preuve concrète est `E:\Projets IA\Automatisation\.codex\workflows\cdc-maintenance-documentaire-rag-v2-2-officialisation`.
- Le fichier preuve `10-cdc.md` a pour SHA-256 vérifié `51E861D4F2D581143C4207C860F71699F9AB129F654F243EBF70AAFBE806E8F0`.
- Le fichier preuve `15-cdc-approval.md` a pour SHA-256 vérifié `E0A0636330BDFBBF94A9F71D0ED33A7A7087B840D2BFFA5DBEF6628C4A0C03D0`, porte le statut `APPROVED`, lie le CDC au SHA-256 attendu et référence `DEC-055`.
- La décision `DEC-055` est une décision USER de type `CDC_APPROVAL` qui approuve sans condition le même SHA-256 de CDC.
- Les artefacts d'architecture et de revue de conception sont absents de cette preuve, conformément à son arrêt après approbation du CDC.
- Le worktree contient des modifications utilisateur préexistantes sans rapport; elles doivent être préservées et exclues de ce changement.

## Source workflow bindings

None.

## Acceptance criteria

- AC-001: La définition courante de `brainstorm-product-design` déclare une route gérée réutilisable qui prend comme entrées un workflow externe, son `10-cdc.md` approuvé et son `15-cdc-approval.md`, sans exécuter les phases d'interview, de création du CDC ou d'approbation du CDC.
- AC-002: Avant d'entrer dans la phase d'architecture, la route recalcule et compare le SHA-256 du CDC avec l'empreinte déclarée et vérifie que le certificat d'approbation est explicitement `APPROVED` et lié à ce même CDC.
- AC-003: Une entrée absente, illisible, modifiée, non approuvée, liée à une autre empreinte ou présentant une incohérence de preuve conduit à un état bloqué déclaré avant tout lancement de `architect_brainstorm`.
- AC-004: Lorsque les preuves sont valides, le graphe déclaré lance séquentiellement `architect_brainstorm`, puis `review_brainstorm` pour la revue de conception, avec le handoff et les modes exacts définis par le Registry.
- AC-005: Les changements requis par la revue suivent une boucle de rework explicitement déclarée et bornée par un compteur Registry; l'épuisement du budget ou un verdict bloquant arrête le workflow sans boucle illimitée.
- AC-006: Tous les terminaux de la nouvelle route s'arrêtent avant DEV et n'autorisent ni agent de développement, ni modification de code produit, ni interprétation d'un verdict de revue comme permission d'implémenter.
- AC-007: Le cas NeoAutomatisation fourni est accepté par les validations d'import avec le SHA-256 CDC `51E861D4F2D581143C4207C860F71699F9AB129F654F243EBF70AAFBE806E8F0`, le certificat `APPROVED` et `DEC-055`, sans créer `20-architecture.md` ni `30-review.md` pendant les tests.
- AC-008: Une fixture négative obtenue par altération d'au moins une preuve ou empreinte est rejetée avant architecture par une validation automatisée observable.
- AC-009: Les routes existantes de `brainstorm-product-design` restent valides et leurs transitions, gates humains et comportements terminaux existants ne régressent pas.
- AC-010: Les validateurs Registry et d'intake pertinents acceptent la nouvelle route et rejettent les graphes, délégations, bindings ou compteurs non conformes.
- AC-011: La documentation de contrôle nécessaire explique comment référencer un workflow externe approuvé, quelles preuves et empreintes sont obligatoires, les causes de blocage et l'arrêt obligatoire avant DEV.

## Investigation targets

- La définition courante et la version map de `brainstorm-product-design` dans le Registry installé, afin d'identifier les phases, artefacts, statuts, transitions, gates et compteurs existants à réutiliser.
- La source de vérité du registre et son mécanisme d'installation ou de synchronisation, afin de modifier les fichiers maintenus plutôt qu'un artefact dérivé lorsque le dépôt prévoit cette distinction.
- Le Skill et les validateurs de `brainstorm-product-design`, notamment les contrats des handoffs d'architecture, de revue et de rework.
- Les mécanismes actuels de binding SHA-256, d'import de workflow externe, de résolution de chemin, de validation d'approbation et d'invalidation des preuves.
- Les hooks ou contrôles déterministes qui initialisent `.workflow.json`, lient la phase courante et appliquent les transitions Registry.
- Les tests existants du registre, de l'intake, des transitions, des gates humains et des boucles bornées auxquels ajouter les scénarios positif et négatif.
- La compatibilité avec les versions historiques et les workflows déjà compilés lorsque la définition courante reçoit une nouvelle route ou un changement de version.

## Material unknowns

- PLAN_VALIDATION: déterminer le nom de route, les identifiants de phase, les statuts, les modes d'agent et le compteur de rework exacts en réutilisant uniquement les conventions et contrats déjà déclarés.
- PLAN_VALIDATION: déterminer si l'import conserve des références vers le workflow source ou matérialise des copies liées, sans affaiblir la détection de modification après approbation.
- PLAN_VALIDATION: déterminer les règles sûres de résolution des chemins absolus et relatifs, y compris pour une preuve située dans un autre dépôt.
- PLAN_VALIDATION: déterminer si `15-cdc-approval.md` et son binding CDC suffisent comme preuve générique ou si le journal de décision doit aussi être requis et lié; ne pas ajouter cette exigence sans preuve Registry.
- PLAN_VALIDATION: déterminer la stratégie de versioning et de compatibilité nécessaire pour la définition, le Skill, les validateurs et l'état hook-owned.
- IMPLEMENTATION_VALIDATION: confirmer les commandes de validation natives et les fixtures minimales permettant de tester le cas fourni sans produire d'artefact d'architecture produit.

## Delegation directive

Exécuter séquentiellement (`sequential execution`) la route Registry `dev-change-delivery/FULL` et valider chaque handoff avant transition:

1. Phase `architecture`: déléguer à `architect_feature_bug` en mode `ARCHITECTURE`; sortie autorisée `10-plan.md`.
2. Phase `plan_review`: déléguer à `reviewer_feature_bug` en mode `PLAN_REVIEW`; sortie autorisée `20-plan-review.md`.
3. Si la transition l'exige et si le budget le permet, phase `plan_correction`: déléguer à `architect_feature_bug` en mode `PLAN_CORRECTION`; mettre à jour uniquement `10-plan.md`, puis revenir à `plan_review`.
4. Après approbation du plan, phase `implementation`: déléguer à `lead_developer` en mode `INITIAL_IMPLEMENTATION`; modifications limitées au périmètre confirmé et rapport `30-implementation-report.md`.
5. Phase `code_review`: déléguer à `reviewer_feature_bug` en mode `CODE_REVIEW`; sortie autorisée `40-code-review.md`.
6. Si la transition l'exige et si le budget le permet, phase `review_correction`: déléguer à `lead_developer` en mode `REVIEW_CORRECTION`; corriger le périmètre confirmé et mettre à jour `30-implementation-report.md`, puis revenir à `code_review`.
7. Phase parent `final_report` en mode `FINAL_INTEGRATION`: produire uniquement `50-final-report.md` après validation de tous les handoffs et des vérifications finales.

Aucune phase ne peut être sautée, auto-approuvée ou exécutée en parallèle. Une transition bloquée, un compteur épuisé, une preuve matérielle manquante ou une décision produit non résolue impose l'arrêt et l'escalade au parent.

## Human gates

None.

## Loop budget

- plan_correction_cycles: 2
- code_correction_cycles: 2
- repeated_finding_threshold: 2
- automatic_continuation: YES
- Plan correction cycles: 2
- Code correction cycles: 2
- Repeated-finding threshold: 2
- Automatic continuation: YES

## Open questions

None material at intake. Les inconnues d'implémentation listées ci-dessus doivent être résolues par preuves lors de l'architecture du changement; toute découverte qui modifie un gate humain, le contrat de preuve, la compatibilité ou le périmètre doit être escaladée au parent.

## Out of scope

- Exécuter l'architecture ou la revue du produit NeoAutomatisation.
- Créer `20-architecture.md`, `30-review.md` ou tout autre artefact dans le workflow preuve.
- Implémenter NeoAutomatisation ou modifier un autre code produit.
- Refaire l'interview, le CDC ou l'approbation du cas fourni.
- Démarrer automatiquement un workflow DEV à partir d'un verdict de conception.
- Ajouter une publication, un déploiement, un commit, un push, une pull request ou un merge.
- Refondre les workflows, agents, Skills ou hooks sans lien direct avec la nouvelle route.
