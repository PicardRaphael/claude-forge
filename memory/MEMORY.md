# Memory Index

## Feedback
- [perf-déclenchement avant budget](feedback_perf_declenchement_avant_budget_skills.md) — fusion/kill/trim skills : routing d'abord, budget ensuite (consigne 9 juil.)
- [registre-relais-agents](feedback_registre-relais-agents.md) — HYPOTHÈSE (à valider 2-3 cas) : registre léger « op coûteuse X faite → artefact Y », 1 ligne/op, consulté AVANT op coûteuse pour éviter le doublon multi-agent. Net-neuf de la note-hub [[relais-inter-agents-fiable]] ; distinct de [[idee-compounding-retroactif]] (transcripts passés)
- [ccnews-structure-vault-provider-drift](feedback_ccnews_structure_vault_provider_drift.md) — Drift routage skill↔SCHEMA RÉSOLU 29 juin (cc-news/forge-brain/veille/vault-audit alignés convention fournisseurs). Leçon générale : lire le SCHEMA réel avant de capitaliser, pas le routage figé de la skill
- [audit-completude-pointeur-vs-orphelin](feedback_audit_completude_pointeur_vs_orphelin.md) — Audit complétude index/roadmap : un wikilink non résolu localement peut pointer vers une note existante ailleurs. search_brain chaque cible avant de la compter orpheline, sinon surcompte le backlog (60→41 réels)
- [audit-prompt-adaptatif-par-couche](feedback_audit_prompt_adaptatif_par_couche.md) — Auditer des prompts d'archi adaptative = par COUCHE (statut de chargement : core toujours-chargé strict vs L3a/conditional à-la-demande tolérant), jamais à plat. Lire blueprint.py (conditional_rules) + chaque prompt en entier. Script qui compte des balises = fausse précision (compter ≠ juger ; `_disabled` ≠ mort pour tous les agents). Skills prompt fusionnées si repo mono-provider (neo_ia 100% Gemini)
- [brief-premisse-fausse-verifier-avant-executer](feedback_brief_premisse_fausse_verifier_avant_executer.md) — Brief peut poser prémisse fausse. Vérifier matériellement avant d'exécuter, surfacer si fausse
- [capitaliser-methode-pas-que-resultat](feedback_capitaliser_methode_pas_que_resultat.md) — Après un chantier redéployable, capitaliser la MÉTHODE (recette déploiement + routage dans la skill créatrice), pas que le RÉSULTAT (note de design). Sinon un futur repo re-réinvente. Prouvé 3× (16 juin)
- [carte-blanche-commit-push-tranche-pas-revalider](feedback_carte_blanche_commit_push.md) — "Carte blanche" = exécuter direct sans re-valider note par note
- [ccnews-confronter-existant](feedback_ccnews_confronter_existant.md) — cc-news confronte chaque finding à l'existant (notes vault + skills/agents/hooks/rules) et agit, pas juste résumer
- [classification-type-ticket-jira](feedback_classification_type_ticket_jira.md) — Classer un ticket par sa NATURE (FEATURE/BUG/OPTIMISATION), jamais par mimétisme
- [commit-push-check-pattern](feedback_commit_push_check.md) — "regarde commit et push" = git status + diff avant push, jamais push aveugle
- config-repo-equipe-vs-forge — PROMU VAULT (8 juil.) : repo d'équipe ≠ machinerie forge (skills auto-portantes, hooks non-bloquants, pas de delegate-guard). Canonique : [[config-repo-equipe-vs-forge]]
- [conformite-aveugle-regle-generique](feedback_conformite_aveugle_regle_generique.md) — Garde refusée = lire son intention avant de contourner. Souvent intentionnelle
- [consolidate-searches](feedback_consolidate_searches.md) — Ne jamais chercher 2× la même info. Consolider en 1 fichier dès le 1er search
- [couper-loops-decision-fatigue](feedback_couper_loops_decision_fatigue.md) — Après validation, trancher vite. 2 signaux : boucle "es-tu parfait" + session longue. Cap 3 advisor
- [cross-repo-write-main-session-only](feedback_cross_repo_write_main_session.md) — Session forge a write cross-repo, sub-agents bloqués. Ne pas déléguer fixes cross-repo
- [creator-reorganise-design-verrouille](feedback_creator_reorganise_design_verrouille.md) — skill/agent-creator réorganise/dilue un design verrouillé avec l'user. Vérifier bloc par bloc vs design validé, briefer "ne pas réinterpréter"
- [diagnostic-empirique-avant-affirmer-une-garde](feedback_diagnostic_empirique_avant_affirmer_garde.md) — Avant d'écrire qu'une garde existe (deny/hook), la vérifier + citer la preuve
- [ia-back-postgresjs-stack-drift-pattern](feedback_drizzle_postgresjs_drift.md) — Migration code ≠ migration .claude/. Grep stack OLD vs NEW (Drizzle→postgres.js)
- [ecart-consigne-chiffree-surfacer](feedback_ecart_consigne_chiffree_surfacer.md) — Écart à consigne chiffrée = surfacer pour arbitrage, jamais juger acceptable en silence
- [ecrire-partout-invoquer-skill-creatrice](feedback_ecrire_partout_invoquer_skill_creatrice.md) — Forge écrit cross-repo MAIS invoque TOUJOURS la skill créatrice (SKILL.md/agent/hook/CLAUDE.md jamais à la main), même hors forge — le delegate-guard forge ne fire que sous forge/ (trou cross-repo). Incident migration_script 24 juin
- [edit-tool-read-obligatoire-meme-en-parallele](feedback_edit_tool_read_obligatoire.md) — Edit en // sans Read = 7/8 failures. Batch Read d'abord, puis batch Edit
- [eval-trio-angles-complementaires](feedback_eval_trio_angles_complementaires.md) — Éval forge = TRIO (skill-evolve fin / forge-review stratégique / outcomes-test rubric). Chercher 3 angles avant conclure gap
- [feedback-reviole-3x-regle-insuffisante](feedback_feedback_reviole_3x_regle_insuffisante.md) — Feedback re-violé ≥3× = règle insuffisante. Réflexe pré-action ou garde-fou structurel
- [git-C-pas-cd-multi-repo](feedback_git_C_pas_cd.md) — TOUJOURS git -C <path>, jamais cd && git. CWD persiste entre Bash calls
- [jarvis-innovator-mindset](feedback_jarvis_innovator.md) — Contrat Jarvis : partenaire, anticiper, innover, évoluer, franc, autonome, proactif
- [localiser-repos-avant-workflow-multi-repo](feedback_localiser_repos_avant_workflow_multi_repo.md) — Avant audit/workflow fan-out multi-repo, localiser empiriquement chaque repo (ls */.claude). neo_ia + ia_back sous Documents\neot-v2\, pas à la racine
- [preference-modele-opus-4-8](feedback_preference_modele_opus.md) — Raphael : Opus 4.8 préféré, 4.6 repli, JAMAIS 4.7 (jugé moyen). Défaut modèle Opus = claude-opus-4-8
- [mcp-alias-ambigu-chemin-exact](feedback_mcp_alias_ambigu_chemin_exact.md) — MCP append_note/read par alias court résout faux si stem partagé. Chemin exact
- [mcp-transport-stdio-http-crashloop](feedback_mcp_transport_stdio_http_crashloop.md) — FastMCP crash loop systemd + nginx 502 = transport stdio au lieu de http. Lire les logs AVANT de soupçonner l'OAuth (biais du dernier changement)
- [multiedit-matcher-blind-spot-hooks](feedback_multiedit_matcher_blind_spot.md) — Hooks PreToolUse Write|Edit sans MultiEdit = trou. TOUJOURS le triplet
- [never-pure-executor](feedback_never_pure_executor.md) — JAMAIS mode exécutant pur, posture Jarvis active même sur prompts directifs/QA
- [org-blocks-github](feedback_no_github_cloud.md) — Orga Team bloque GitHub, pas de triggers cloud, tout en local Task Scheduler
- [opus47-workflow-decisions](feedback_opus47_workflow.md) — xhigh RÉSERVÉ architect/dev-lead/refactor-pg. high partout ailleurs
- [ratio-empirique-doublons-memory-vault-pilote](feedback_ratio_empirique_doublons_memory_vault.md) — Pilote 29 fichiers = 38% doublons vault. Ancre seuils hook saturation (WARNING 80, CRITICAL 100) et cible ≤100 fichiers
- [plugin-admin-absorbe-readonly](feedback_plugin_admin_absorbe_readonly.md) — Plugin admin (write) absorbe fonctionnellement read-only. Desinstaller le read-only sans perte (gain tokens). Verifier allowed-tools de chaque skill
- [pas-de-wakeup-pour-agents-background](feedback_pas_de_wakeup_pour_agents_background.md) — Ne JAMAIS programmer un ScheduleWakeup pour attendre mes propres agents background (le harness notifie déjà à leur fin). Wakeup = travail externe non-tracké uniquement (CI, déploiement, poll externe)
- [present-before-build](feedback_present_before_build.md) — Présenter le plan AVANT construire, jamais créer sans validation Raphael
- [python-path-windows-hooks](feedback_python_path_windows.md) — Windows : chemin absolu Python313 dans hooks, jamais "python" seul
- [recurring-meta-anti-pattern](feedback_recurring_meta_anti_pattern.md) — Workaround ≥ 2 fois = bug. AVANT refonte structurelle, lister cran 1/2/3
- [regression-diagnostic-diff-avant-redesign](feedback_regression_diagnostic_diff_avant_redesign.md) — Régression à point d'introduction connu = diff AVANT redesign. Ne pas anchrer sur l'hypothèse user "trop gros". Asymétrie read/write runtime. Write-path résolu dans TOUS les points d'entrée
- [regle-scope-pas-universelle](feedback_regle_scope_pas_universelle.md) — Vérifier scope règle AVANT propagation. Provider sur SON produit = single source
- [single-source-of-truth](feedback_single_source_of_truth.md) — UN fichier canonique par concept, skills pointent vers doc/
- [skills-user-scope-pas-cross-repo](feedback_skills_user_scope_pas_cross_repo.md) — Skills frontmatter user-scope décoratives cross-repo. Workaround : MCP en clair dans body
- [spec-trous-structurels-langfuse-secuia-decisions](feedback_spec_trous_structurels_a_checker.md) — Audit spec : checker 3 trous (Langfuse, 4 risques sécu IA, décisions sans assignee)
- [stop-over-verifying](feedback_stop_over_verifying.md) — Verdict direct si travail fait en session, pas relire 20 fichiers pour dire oui
- [subagent-audit-category-error](feedback_subagent_audit_category_error.md) — Sub-agent audit flagge drift sur note citant valeurs externes. Vérifier source réelle
- [subagent-autocommit-violation](feedback_subagent_autocommit.md) — Sub-agents committent malgré instruction. TOP gras + git log post-agent
- [tag-projet-nom-repo-exact](feedback_tag_projet_nom_repo_exact.md) — Tag projet = nom EXACT du repo (neo_ia, ia_back, claude-forge), jamais de normalisation cosmétique du séparateur. Vérifier nom réel (disque + git remote) avant fusion
- [test-writer-systematic](feedback_test_writer_systematic.md) — RÉVISÉ 22 mai : MAX 3 tests/comportement, REFACTOR supprimée, effort high
- [use-brain-skills-not-grep](feedback_use_brain_skills.md) — Questions métier/décisions = skill `/neoteem-brain-dev-ia:neo-brain-dev-ia` (forge : MCP NeoBrain direct autorisé par Raphael), jamais grep manuel. Interroger le brain À FOND avant toute taxonomie/décision métier (domaines back-ts = Damier Lojii + 01-Domaines + MOC-BDD, 10 juin). Skill/source NOMMÉE par Raphael = l'invoquer VISIBLEMENT dès le 1er tool call, même en plan mode — jamais « je le ferai à l'exécution »
- [verify-exhaustive-claims](feedback_verify_exhaustive_claims.md) — Grep de validation AVANT toute déclaration exhaustive (zéro, tous, aucun, complet)
- [zero-dette-technique-nettoyer-completement](feedback_zero_dette_technique.md) — Dette/drift/réf morte découverte = nettoyage COMPLET immédiat, jamais plus tard

### Archive de référence — tier-2 (125 feedbacks)
> Feedbacks valides mais sans citation entrante (ou non stratégiques), déplacés vers [memory/_index_archive.md](_index_archive.md) pour alléger le chargement. Accès via recherche/lecture directe si besoin. Critère tier-1 : cité ≥1 OU sujet stratégique. Réintégrer ici un tier-2 dès qu'il est cité.

## Project
- [forge-review-journal](project_forge_review.md) — Journal des reviews stratégiques : 9 juil. = 0 KILL, 2 fusions appliquées (cc-rag-ref→rag-design, web-search-canonical-source→rule), F2 trio doctrine en measure-first (output/mesure-F2-fusion-doctrine.md, hôte = methode-pivoter-doctrine 34 backlinks), delegate-guard.py.proposed en attente validation Raphael
- [neoteem-back-ts-project](project_neoteem_back_ts.md) — Monorepo backend Loji (ia_back→neoia-api + Drizzle + MCP par domaine). E0 + durcissement livrés, note 17,5/20. Hiérarchie Jira = 5 epics permanents FIGÉS (jamais en créer) ; story S1 = N2-111278 ([IA] FEATURE, parent N2-68082). Skill spec dans les repos cibles + plugin PO (copies forge supprimées 24 juin). Phase = 12 sous-tâches à rédiger au go
- [dossier-strategique-ia-neoteem](project_dossier_strategique_ia_neoteem.md) — Dossier Stratégique IA CODIR audité 17/20 (29 mai), roadmap V2 à venir, sortir volet salaire
- [claude-desktop-profiles](project_desktop_profiles.md) — Config Claude Desktop par rôle Neoteem, skill dédiée, output/
- [neo-ia-project](project_neo_ia.md) — Monorepo Python NeoChat/NeoDoc/NeoMail, 12 agents, 36 skills, 18 rules, 18 hooks. Aligné modèle back-ts 10 juin (/feature, Default-FAIL, memory/, PR develop + git-guard). CI GitHub Actions était MORTE → bitbucket-pipelines.yml créé (activation humaine en attente)
- [neo-ia-tool-selection-state](project_neo_ia_tool_selection.md) — HybridToolSelector : expansion+reranking OFF en prod, Lazy Expansion + OATS validé
- [deploy-methods-other-repos](project_deploy_methods_other_repos.md) — Déployer 9e principe + skill-evolve all sur neo_ia et ia_back
- [lojii-project](project_lojii.md) — Frontend Vue 3/Vuetify 3 gestion immo, 634 composants, migration Composition API
- [spec-unification-3repos](project_spec_unification_3repos.md) — Chantier 26 juin : /spec IDENTIQUE ×3 repos (SKILL unifié + repo-explorer + hook validation structure template + script sync), Phase 1+2 poussées. RESTE : normaliser 23 tickets Jira existants (IA-7/16/27 + Stories + sous-tâches) par editJiraIssue, prochaine session

## User
- [raphael-picard-full-profile](user_raphael_profile.md) — Profil holistique : Lead IA Neoteem, 36 ans, parcours atypique, gamer, vision expert IA reconnu

## Reference
- [bashrc-bind-warnings-non-interactive](reference_bashrc_bind_warnings.md) — Warnings bind readline sans garde `[[ $- == *i* ]]`
- [neo-brain-pattern](reference_obsidian_query_brain.md) — Pattern neo-brain : wrapper CLI + skill + knowledge-first routing
- [subagent-permissions-limitation](reference_subagent_permissions.md) — v2.1.101 : worktree+MCP OK, permissions.allow toujours non hérité
- [discord-webhook-jarvis](reference_discord_webhook.md) — Webhook Discord #veille-tech pour notifications Jarvis (JAMAIS commit)
- [forge-brain-vault](reference_forge_brain_vault.md) — Vault Obsidian forge-brain, priority 1 des sources
- [acceptedits-bug-anthropic-since-v2179](reference_acceptedits_bug.md) — Bug acceptEdits prompte depuis v2.1.79. Workaround = Auto mode
- [anthropic-skills-plugin](reference_anthropic_skills_plugin.md) — 16 skills officielles (pdf, skill-creator, mcp-builder, etc.)
- [obsidian-cli-windows](reference_obsidian_cli_windows.md) — Windows Git Bash résout Obsidian.exe au lieu de .com, wrapper obligatoire
- [gchat-webhooks](reference_gchat_webhooks.md) — Webhooks Google Chat ia_back + neo_ia + neoteem-brain
- [techniques-cheatsheet](reference_techniques_cheatsheet.md) — Cheat sheet : meilleure technique par besoin
- [code-dev-agent](reference_python_dev_agent.md) — Agent code-dev (remplace python-dev) : multi-stack, hook PostToolUse code-lint-dispatch. Pattern TDD + 4 modes conservé
- [boris-thariq-bestpractices](reference_boris_thariq_bestpractices.md) — Best practices Boris+Thariq+Anthropic : agents, skills, rules, CLAUDE.md
- [workarounds-contraintes-session-forge](reference_workarounds_session_constraints.md) — Machine forge : gh absent, x.com 402, HEREDOC Windows
- [eliott-meunier-prisme-one](reference_eliott_meunier_prisme.md) — Prisme One : ontologie par utilité, /done, contexte holistique
- [repo-scope-guard-hook](hook_repo_scope_guard.md) — Triplet auth-detector+repo-scope-guard+auth-cleanup : repos neot-v2/
- [transcrire-video-native-x](reference_transcrire_video_native_x.md) — Vidéo native X (pas YouTube) : x-read JSON → URLs MP4 → curl → ffmpeg WAV 16k → faster-whisper small. /watch ne couvre pas X
