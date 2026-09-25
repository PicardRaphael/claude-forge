# Journal d'archive mémoire

## [2026-06-17] clean-memory agressif — reference_ + project_ (21 fichiers)
- **Mode** : agressif-réversible (carte blanche Raphael), 3 agents // (clean-ref-a/b + clean-proj) ont lu les 69 fichiers en entier. Vérif vault MCP avant archive des project_ auto-déclarés doublons.
- **project_ archivés (12)** → memory/_archive/2026-06/ :
  - back_refacto, neoteem_brain, bdd_neoteem : s'auto-déclaraient « contexte stable → voir vault/1-Projets/ » → doublons vault confirmés (ia_back.md, neoteem-brain.md existent au vault). Doctrine memory-discipline : stable vit au vault.
  - session_22mai_refonte_hooks : chantier terminé (« Tâches en cours : Aucune »), capitalisé [[raisonnement-22mai-doctrine-vs-enforcement]].
  - v2_optimizations, meta_generator_pending : pending jamais concrétisés.
  - neoteem_brain_plugin, neoteem_plugin_claude : doctrine plugins capitalisée vault ([[neoteem-brain-plugins]], [[plugin-vs-skill-anatomie]]) ; plugin_claude supplanté par brain_plugin.
  - mcp_v2 (auto-aveu « à rapatrier, mal placé »), mcp_brain_remote (état OPÉRATIONNEL stable), ia_neoteem_interne (avril périmé), claude_forge_naming_collision (conditionnel dormant).
- **reference_ archivés (9)** → memory/_archive/2026-06/ :
  - opus47_best_practices (Opus 4.7 déprécié, courant 4.8), cc_updates_april2026 (428L changelog daté, absorbé cc-news/cc-features-ref), industry_april2026 (snapshot concurrents volatil périmé), cowork_dispatch (absorbé skill cc-cowork-ref), skills_guide (absorbé skill-creator/cc-skills-ref), audit_06_findings (corrections d'attribution → vault), vibe_coding_setup (doctrine modèle divergente + absorbé vault).
  - agent_team_workflow (doctrine pré-22-mai : CTO + gates systématiques, contredit le pivot), mcp_stdio_restart_impossible (prémisse stdio périmée, forge-brain = HTTP, contredit par lifecycle_gotchas à jour).
- **Index** : 12 lignes tier-1 retirées de MEMORY.md (166→154 lignes). 0 pointeur orphelin (vérifié).
- **GARDÉS notables** (mode agressif mais pas aveugle) : neoteem_back_ts/neo_ia/dossier_strategique/tool_selection (phases actives), lojii/deploy_methods (actions ouvertes), subagent_permissions (fait « non hérité » peut-être encore vrai), 37 reference_ valides.
- **NON FAIT (laissé pour session dédiée)** : fusions reference_ proposées (stdio→lifecycle déjà archivé ; obsidian_cli+query_brain ; prompt_engineering→techniques_cheatsheet) — fusion = plus risqué qu'archive. Drifts internes signalés à corriger (workarounds L89 CLAUDE_AGENT, python_dev_agent dernière ligne, claude_code_architecture nesting, forge_brain_vault ontologie).
- **Rollback** : pour chaque fichier, `git -C <repo> mv memory/_archive/2026-06/<f>.md memory/<f>.md` + restaurer ligne index.

## [2026-06-17] archive — delegate-guard-scope-tout-skillmd (feedback FAUX)
- **Fichier** : feedback_delegate_guard_scope_tout_skillmd → memory/_archive/2026-06/
- **Raison** : factuellement faux sur l'état courant. Disait « delegate-guard ne bloque plus SKILL.md depuis 6 juin (hard block retiré) ». Contredit par le code (`delegate-guard.py:47,122` — SKILL.md dans PROTECTED) ET par l'expérience directe du 17 juin (Edit io-daily/SKILL.md bloqué → skill-creator requis). Le pivot 6 juin documenté n'a pas pris effet / été annulé. 0 citation entrante.
- **Index** : ligne retirée de _index_archive.md (était tier-2)
- **Rollback** : git mv memory/_archive/2026-06/feedback_delegate_guard_scope_tout_skillmd.md memory/, restaurer ligne _index_archive.md

## [2026-06-17] fusion — Suffixe plugin ≠ niveau d'accès
- **Fichier** : feedback_plugin_suffixe_ia_pas_readonly → memory/_archive/2026-06/
- **Raison** : doublon — même audit 28 mai, le fichier EST la section « Cas inverse » de feedback_plugin_admin_absorbe_readonly sortie en fichier séparé (pointe lui-même vers le survivant). Contenu déjà présent dans le survivant.
- **Survivant** : feedback_plugin_admin_absorbe_readonly (contient la section « Cas inverse »)
- **Index** : ligne retirée de _index_archive.md (était tier-2)
- **Rollback** : git mv memory/_archive/2026-06/feedback_plugin_suffixe_ia_pas_readonly.md memory/, restaurer ligne _index_archive.md

## [2026-06-17] séparation + wikilink (PAS archive) — famille « diagnostiquer la couche avant de patcher »
- **Fichiers** : feedback_deny_global_ecrase_allow_projet + feedback_hook_vs_harness_permission_distinction (tous deux EN PLACE)
- **Décision** : NE PAS fusionner (angles distincts : précédence deny>allow vs ordre harness/hook). Wikilink réciproque ajouté pour marquer la parenté sans perdre la nuance.

## [2026-06-01] fusion — Brief prémisse fausse + chiffre baseline
- **Fichiers** : feedback_chiffre_baseline_brief_verifier_empiriquement → memory/_archive/2026-06/
- **Raison** : doublon conceptuel — le chiffré se déclarait lui-même "variante chiffrée" du général
- **Absorbé dans** : feedback_brief_premisse_fausse_verifier_avant_executer (section "Cas particulier — chiffre baseline")
- **Index** : entrée chiffre-baseline retirée de MEMORY.md (le général y reste, ligne 17)
- **Rollback** : git mv memory/_archive/2026-06/feedback_chiffre_baseline_brief_verifier_empiriquement.md memory/, retirer la section absorbée, restaurer ligne index

## [2026-06-01] fusion — Couper loops perfectionnisme + session fatigue
- **Fichiers** : feedback_couper_loops_perfectionnisme + feedback_session_fatigue_decision → memory/_archive/2026-06/
- **Raison** : doublon — même session 23 mai, même remède (trancher vite, cap 3 advisor), 2 triggers distincts
- **Meta-feedback** : feedback_couper_loops_decision_fatigue.md (créé)
- **Index** : 2 entrées retirées de MEMORY.md, 1 entrée meta ajoutée
- **Rollback** : git mv les 2 depuis _archive/, supprimer le meta, restaurer les 2 lignes index

## [2026-06-01] fusion — git -C + cd sous-dossier
- **Fichiers** : feedback_cd_sous_dossier_fausse_chemins_relatifs → memory/_archive/2026-06/
- **Raison** : doublon — même cause racine (CWD persiste entre Bash calls)
- **Absorbé dans** : feedback_git_C_pas_cd (section "Cas connexe — diagnostic de structure")
- **Index** : entrée retirée de _index_archive.md (le général reste tier-1 MEMORY.md)
- **Rollback** : git mv depuis _archive/, retirer section, restaurer ligne _index_archive

## [2026-06-01] fusion — skills referenced in body + non-invokable orphan
- **Fichiers** : feedback_non_invokable_skills_orphan → memory/_archive/2026-06/
- **Raison** : doublon — cas particulier (user-invokable:false) de la règle générale
- **Absorbé dans** : feedback_skills_referenced_in_body (section "Cas particulier — user-invokable: false")
- **Index** : entrée retirée de MEMORY.md (le général reste, ligne 73→72)
- **Rollback** : git mv depuis _archive/, retirer section, restaurer ligne index

## [2026-06-01] fusion — anthropic single source + regle scope pas universelle
- **Fichiers** : feedback_anthropic_single_source → memory/_archive/2026-06/
- **Raison** : doublon — anthropic-single-source = cas d'origine de la règle générale de scope (se cross-référençaient)
- **Absorbé dans** : feedback_regle_scope_pas_universelle (section "Cas d'origine — Anthropic single source")
- **Index** : entrée retirée de MEMORY.md (le général reste, ligne 70→69)
- **Note** : la grande table par thème d'audit (datée audit 23 mai terminé) condensée au principe essentiel
- **Rollback** : git mv depuis _archive/, retirer section, restaurer ligne index

## [2026-06-01] nettoyage (pas archive) — major_mistakes
- **Fichier** : feedback_major_mistakes.md — NON archivé (9 leçons toujours valides)
- **Action** : retiré 2 mentions de fixes hooks obsolètes post-pivot 22 mai (#9 vault-query-guard retiré, addendum hook obsolète en tête). Les 9 leçons fondatrices gardées.
- **Raison** : l'agent workflow a confondu "contient marque de révision" avec "obsolète". Faux positif corrigé.

## [2026-06-05] archive (5 dormants) — absorption par skills/agents canoniques
- **Fichiers** → memory/_archive/2026-06/ :
  - feedback_arxiv_url_swap_papers_similaires.md — absorbé par `.claude/skills/arxiv-verification/SKILL.md` Check 2 + exemple MCP-Zero↔OATS L53
  - feedback_venues_inventees_pattern.md — absorbé par `.claude/skills/arxiv-verification/SKILL.md` Check 3 + exemples TOOLQP/LoRA/JudgeBench L51-54
  - feedback_tweet_hype_paraphrase_pattern.md — absorbé par `.claude/skills/web-search-canonical-source/SKILL.md` (table 4 patterns + cite ce feedback en source L83)
  - feedback_x_articles_inaccessibles_empirique.md — absorbé par `.claude/skills/x-read/SKILL.md` L104 + `web-search-canonical-source/SKILL.md` L64
  - feedback_da_bash_write.md — absorbé par `.claude/agents/devils-advocate.md` L57 (JAMAIS heredoc Bash, create_note ou texte)
- **Raison** : dormants avec PREUVE d'absorption (vérifiée matériellement par grep des skills absorbantes, pas juste "non cité"). Critère décisif de la skill /clean-memory satisfait.
- **Index** : 3 lignes tier-1 MEMORY.md (arxiv, da-bash-write, tweet) remplacées par pointeurs vers l'archive+skill ; x-articles repointé dans _index_archive.md (était tier-2) ; venues était orphelin d'index (rien à retirer).
- **Méthode** : 6 sous-agents analyse parallèle par cluster thématique (176 feedbacks). Résultat global : 0 fusion, 0 amendement, 5 dormants prouvés, ~165 EN PLACE. Corpus déjà très propre (passes 27-29 mai).
- **Rollback** : pour chaque fichier, `git -C <repo> mv memory/_archive/2026-06/<f>.md memory/<f>.md`, restaurer la ligne d'index originale (retirer le pointeur).

## [2026-06-05] réconciliations (pas archive) — 3 corrections doctrinales
- **feedback_analyse_repo_includes_code.md** : frontmatter `name: ""` (vide) → `analyse-repo-includes-code-scan` (slug référencé dans MEMORY.md). Bug data-quality.
- **feedback_all_opus.md** : ligne périmée `test-writer = opus xhigh` corrigée → `opus high` (révisé 22 mai, aligné [[feedback_opus47_workflow]] qui fait foi + MEMORY.md tier-1 "xhigh RÉSERVÉ architect/dev-lead/refactor-pg").
- **feedback_cross_repo_write_main_session.md** : note de réconciliation ajoutée sur la contradiction empirique 22 mai (bloqué) vs 26 mai (path absolu marche). Arbitrage Raphael 2026-06-05 : le 26 mai fait foi. Distinction = bypass CLAUDE_AGENT (ne traverse pas) vs path absolu explicite dans prompt agent-creator (traverse). Cross-link mutuel ajouté.

## [2026-07-09] fusion — doctrine allocation modèle/effort (3 → 1)
- **Fichiers** → memory/_archive/2026-07/ : feedback_all_opus, feedback_opus47_workflow, feedback_anthropic_doctrine_biais_full_thune
- **Raison** : amendements successifs (21 mai → 22 mai → 26 mai), chacun désignant le suivant « fait foi » ; résumé canonique déjà dans CLAUDE.md § « Effort calibré (doctrine 26 mai 2026) »
- **Meta-feedback** : feedback_allocation_modele_effort.md (tier-1) — spécifiques repos projet + anti-biais Anthropic + pointeur test-writer
- **Index** : ligne opus47 tier-1 remplacée par allocation-modele-effort ; lignes all_opus + anthropic retirées de _index_archive ; lien mis à jour dans feedback_test_writer_systematic
- **Rollback** : git mv les 3 depuis _archive/2026-07/, supprimer le meta, restaurer lignes index + lien test_writer

## [2026-07-09] archives prouvées passe 1 (6 dormants/absorbés/résolus)
- **Fichiers** → memory/_archive/2026-07/ :
  - feedback_sante_wikilinks_vault_chantier — chantier TERMINÉ (lint_vault 2026-07-09 : 1 wikilink brisé vs 131 baseline) ; gotcha « une écriture MCP à la fois » canonisé au vault [[limite-mcp-lock-inter-ecritures]]
  - feedback_commit_full_main_defaut — absorbé par CLAUDE.md § Workflow Git (FULL MAIN verbatim) ; le wikilink CLAUDE.md [[commit-full-main-defaut]] pointe désormais vers cette archive
  - feedback_skills_user_scope_pas_cross_repo — absorbé par rule mcp-brief-then-direct.md (problème + workaround verbatim)
  - feedback_multiedit_matcher_blind_spot — absorbé par rule windows-hooks.md (gotcha « Triplet Write|Edit|MultiEdit »)
  - feedback_ccnews_confronter_existant — absorbé par skill cc-news étape 7 L136 (« Confronter chaque finding MAJEUR à l'existant », gravé 2 juin)
  - feedback_ccnews_structure_vault_provider_drift — RÉSOLU 29 juin (auto-déclaré dans le fichier, zéro occurrence ancienne convention vérifiée)
- **Rollback** : git mv depuis _archive/2026-07/, restaurer lignes index

## [2026-07-09] rétrogradations tier-1 → tier-2 (18) + réparations index
- **Critère** : 0 citation entrante (graphe recalculé sur memory + CLAUDE.md + rules + skills + agents), hors sujets stratégiques, non pinned. Fichiers INCHANGÉS, seul l'index bouge.
- **Rétrogradés** : audit_completude, audit_prompt_adaptatif, conformite_aveugle, consolidate_searches, creator_reorganise, drizzle_postgresjs, eval_trio, mcp_transport_stdio, no_github, pas_de_wakeup, plugin_admin, preference_modele_opus, present_before_build, ratio_empirique (archivé ensuite passe 2), regle_scope, single_source, subagent_audit_category, tag_projet
- **Gardés tier-1 malgré 0 citation (justifié)** : capitaliser_methode (axe stratégique living doctrine), use_brain_skills (re-violé 2×, coût relation élevé)
- **Réparations** : 2 orphelins hors index résolus (sante_wikilinks, commit_full_main → archivés) ; réf morte `reference_python_windows_cross_machine.md` retirée de rules/windows-hooks.md ; compteurs d'index corrigés (« 125/129 » → réels)

## [2026-07-09] GRAND NETTOYAGE passe 2 (55 fichiers) — directive Raphael « supprime les erreurs qu'on ne verra plus »
- **Méthode** : 4 agents parallèles (lots A/B/C feedbacks + reference/project), lecture INTÉGRALE de chaque fichier, absorptions vérifiées par grep. Arbitrage final session principale : 55/56 propositions acceptées, 1 refus (5_lignes_karpathy gardé tier-2 — nuance non absorbée flaggée par l'agent).
- **Fichiers** → memory/_archive/2026-07/ (catégorie — raison courte) :
  - **Absorbés par canoniques** : forge_skills_priority (CLAUDE.md § Priorité des sources), coach_proactif (comportement-proactif.md Posture Jarvis), glissement_jarvis_executant (never-pure-executor + jarvis-innovator), quality (sequence-canonique § lecture partielle), read_references_first (check-before-create.md), read_note_conditionnel (CLAUDE.md L14), mv_shell_contourne_classifier (CLAUDE.md L14 .proposed), propagate_decisions_cross_repo (rule cross-repo-propagation intégrale), optimiser_claudemd_inspec (claudemd-creator + vault), neoteem_brain_pipeline (rules du repo neoteem-brain), agent_creator_path_absolu (mcp-brief-then-direct.md), skills_referenced_in_body (mcp-brief-then-direct + checklist subagent-creator), repo_autonomy (vault [[config-repo-equipe-vs-forge]]), roadmap_implementable (CLAUDE.md Document & Clear), tests_adverses_hooks_secu (vault [[comment-creer-hook]] étape 5), test_everything (skill /verify + post-dispatch-verify.md), webfetch_avant_subagents (vault [[audit-thematique-claims-vault]]), cartographie_exhaustive (verify-exhaustive-claims + post-dispatch-verify), doctrine_pushback (CLAUDE.md Contrat Jarvis « Être franc »), dispatch_analyse_vs_audit (comportement-proactif.md ; agents cibles supprimés), recap_find_vault_bloque_prebash (bug FIXÉ : recap/SKILL.md utilise find_by_property), sub_agent_invente_classifier (diagnostic-empirique + post-dispatch-verify), design_collegue_flow_first (CLAUDE.md code minimum + check-before-create)
  - **One-shot datés / périmés** : 80_percent_confidence_ship, auto_violation_doctrine, backup_zip_avant_purge, bash_permission_format (propagation résolue), brief_prescrit_travail_deja_fait, dispatch_clusters_priority_check, dont_prefill_files, git_log_before_resume, proposed_files_antipattern, renommer_skill_3_endroits (borderline assumé), agent_tools_restriction + agent_vs_skill (composants morts), db_immutable (contrainte repo cible + stack driftée), loop_brain_check (niche repo mort), ratio_empirique_doublons (seuils supersédés par memory-discipline.md), repo_audit_workflow, repo_scope_read_libre (hook_repo_scope_guard fait foi), schema_mapper_location, self_modification_agent_cross_dispatch (creators devenus skills), superpowers_decision (config settled), support_tokens (config settled neo_ia — borderline assumé), surface_plutot_que_padder (subsumé par ecart_consigne tier-1)
  - **project_** : desktop_profiles (absorbé skill configure-claude-desktop), lojii (contexte stable au vault [[lojii]])
  - **reference_** : acceptedits_bug (snapshot v2.1.139, courant v2.1.202, workaround standing), anthropic_skills_plugin (inventaire périmé), boris_thariq_bestpractices (drift doctrine pré-pivot 22 mai + absorbé canoniques vault), eliott_meunier_prisme (inspiration implémentée), forge_brain_vault (absorbé forge-brain-proactive.md + structure périmée), obsidian_cli_windows + obsidian_query_brain (supersédés par MCP), python_dev_agent (agent code-dev.md = source de vérité, hook existe)
- **Fixes connexes** : drift L89 de reference_workarounds corrigé (bypass CLAUDE_AGENT supprimé) ; ligne Source de cross-repo-propagation.md repointée vers l'archive
- **Reliquat signalé** (non exécuté ici) : replier la nuance « Karpathy ≠ repos non-code » dans la note vault [[comment-ecrire-claudemd]] puis archiver feedback_5_lignes_karpathy ; confirmer le déploiement skill-evolve neo_ia/ia_back puis archiver project_deploy_methods_other_repos
- **Rollback** : pour chaque fichier, `git -C <repo> mv memory/_archive/2026-07/<f>.md memory/<f>.md` + restaurer la ligne d'index correspondante (MEMORY.md pour ex-tier-1, _index_archive.md pour ex-tier-2)

## [2026-09-25] clean-memory — 6 projets expirés + dédoublonnage tier-2 (arbitrage Raphael « OPTIMISE »)
- **Fichiers** → memory/_archive/2026-09/ :
  - **project_neo_ia** : phase de juin promue au foyer vault [[neo_ia]] § « Alignement sur neoteem-back-ts » (workflow PR, CI Bitbucket, MCP Langfuse v2, 6 epics Jira, actions humaines ouvertes au 12 juin). Restes machine (plugins, caches) non promus : volatils, à revérifier sur place.
  - **project_spec_unification_3repos** : chantier livré le 26 juin. Pattern « skill identique ×N + sync fichiers entiers + hook de format gaté par footer » promu dans [[pattern-vault-source-unique-sync-mecanique]] ; le hook footer-gate était déjà dans [[comment-creer-hook]], la correction ADF déjà dans [[jira-rendu-adf-mcp-atlassian]].
  - **project_dossier_strategique_ia_neoteem** : trilogie, verdict A/B du 30 mai, 3 dangers, 5 trous et TODO trame d'interview promus dans [[comprendre-neoteem-vue-responsable-ia]] ; charte + gotchas PDF déjà dans [[pdf-chrome-headless]] (pointeur repointé).
  - **project_forge_review** : journal du 9 juillet promu en [[forge-review-2026-07-09]] (Knowledge/reviews, qui n'avait aucun journal).
  - **project_deploy_methods_other_repos** : absorbé par l'alignement de juin (reliquat signalé le 9 juillet).
  - **feedback_5_lignes_karpathy_ouverture** : contredit par la canonique [[comment-ecrire-claudemd]] § Ouverture (« Aucune formule externe ni bloc de cinq lignes n'est obligatoire universellement »), qui porte déjà la nuance repos non-code. Reliquat du 9 juillet soldé.
  - **feedback_autonomy_rule** : absorbé par AGENTS.md § Contrat Jarvis (pas de validations multipliées sous carte blanche) + feedback_carte_blanche_commit_push tier-1.
- **Renouvelé** : project_neo_ia_tool_selection → `status: active`, `expires: 2026-10-25`. project_neoteem_back_ts inchangé (expire le 30 sept.).
- **Reformulé** : feedback_consolidate_searches — « jamais dans une session future » retiré (contredisait la revérification des infos datées) ; consolidation au vault (refile), pas dans un fichier mémoire ; renvoi au registre des opérations coûteuses.
- **Index** : 18 feedbacks listés à la fois dans MEMORY.md et _index_archive.md → retirés de _index_archive (règle « un fichier = un seul index » ajoutée à son en-tête) ; compteur tier-2 34 → 16 réels. jarvis_innovator passe en tier-2 malgré une citation entrante, parce que son propre corps dit de ne pas le charger comme préférence (adaptateur de compatibilité). agent-flow ajouté en Reference (il n'était lié nulle part, donc invisible pour memory-recall).
- **Non fait (non validé)** : rétrogradation des ~24 tier-1 sans citation entrante.
- **Rollback** : `git -C <repo> mv memory/_archive/2026-09/<f>.md memory/<f>.md` + restaurer la ligne d'index ; les enrichissements vault restent valables indépendamment.

## [2026-09-25] décision — rétrogradation des tier-1 non cités écartée (carte blanche Raphael)
- **Constat vérifié** : `.claude/hooks/memory-recall.py` ne rappelle que les fichiers liés depuis MEMORY.md (`_INDEX_PATH`) et exclut `_index_archive.md` (`_EXCLUDED`). Rétrograder = couper tout rappel automatique.
- **Cause des 18 doublons** : commit `0f98f0f` (29 juil., restructuration MEMORY.md en 7 sous-sections) — il a réindexé 19 fichiers tier-2 précisément pour les rendre rappelables, sans les retirer de `_index_archive.md`. Ce n'était pas `/done`.
- **Décision** : les ~24 tier-1 sans citation entrante restent tier-1 ; le critère « citation ≥1 » mesure le maillage, pas la valeur du rappel. Skill clean-memory (`.claude` + `.agents`) corrigée : la section E affiche le coût réel d'une rétrogradation et impose « un fichier = un seul index ». En-tête de `_index_archive.md` aligné.
- **Rollback** : revert du commit de cette entrée.
