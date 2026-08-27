# Memory Index

> Table des matières, pas un résumé. Une ligne = un pointeur + son déclencheur ; le détail vit dans le fichier. Chargé à CHAQUE session : ce qui est ici coûte des tokens à chaque tour, ce qui est dans un fichier ne coûte que quand on l'ouvre. Le hook `memory-recall` (UserPromptSubmit) fait remonter les fichiers pertinents via leur champ `trigger:` — donc **l'index n'a pas à porter le contenu**, seulement à cartographier. Avant de créer : un fichier existant couvre-t-il déjà le sujet ? **Enrichir > créer.**

## Feedback

### Posture & arbitrage
- [jarvis-innovator-mindset](feedback_jarvis_innovator.md) — contrat Jarvis : partenaire, anticiper, innover, franc, autonome
- [never-pure-executor](feedback_never_pure_executor.md) — jamais exécutant pur, même sur prompt directif ou QA
- [carte-blanche-commit-push](feedback_carte_blanche_commit_push.md) — « carte blanche » = exécuter direct, sans re-valider note par note
- [couper-loops-decision-fatigue](feedback_couper_loops_decision_fatigue.md) — trancher vite après validation ; cap ~3 advisor
- [present-before-build](feedback_present_before_build.md) — présenter le plan AVANT de construire
- [ecart-consigne-chiffree-surfacer](feedback_ecart_consigne_chiffree_surfacer.md) — écart à une consigne chiffrée = surfacer, jamais juger « acceptable » en silence
- [avis-franc-dans-livrable](feedback_avis_franc_ecrit_dans_livrable.md) — avis de fond + choix binaire + dangers écrits DANS le livrable
- [osef-pragmatique](feedback_osef_pragmatique_dette_conditionnelle.md) — trancher sans débat sur sujet faible levier

### Vérifier avant d'affirmer
- [brief-premisse-fausse](feedback_brief_premisse_fausse_verifier_avant_executer.md) — un brief (ou MA mémoire projet, ou MON handoff) peut poser une prémisse fausse : matérialiser avant d'exécuter
- [verify-exhaustive-claims](feedback_verify_exhaustive_claims.md) — grep de validation avant tout « zéro / tous / aucun / complet »
- [diagnostic-empirique-garde](feedback_diagnostic_empirique_avant_affirmer_garde.md) — avant d'écrire qu'une garde existe, la vérifier et citer la preuve
- [verify-avant-affirmation](feedback_verify_avant_affirmation_session.md) — « X parce que Y » sur un changement repo = git log/blame d'abord
- [stop-over-verifying](feedback_stop_over_verifying.md) — l'inverse : verdict direct si le travail vient d'être fait en session
- [regression-diff-avant-redesign](feedback_regression_diagnostic_diff_avant_redesign.md) — régression à point d'introduction connu = diff, pas redesign
- [conformite-aveugle](feedback_conformite_aveugle_regle_generique.md) — appliquer une règle générique sans juger si elle sert le contexte

### Git & multi-repo
- [commit-push-check](feedback_commit_push_check.md) — « regarde commit et push » = status + diff avant push, jamais aveugle
- [git-C-pas-cd](feedback_git_C_pas_cd.md) — toujours `git -C`, jamais `cd &&` (le CWD persiste entre Bash calls)
- [plan-commits-vs-working-tree](feedback_plan_commits_vs_working_tree_reel.md) — plan de commits ⨯ résidus hors-scope : isoler, signaler
- [merge-markers-grep](feedback_merge_markers_grep_avant_commit.md) — grep les 3 marqueurs de conflit avant commit
- [merge-ref-morte-croisee](feedback_merge_ref_morte_croisee.md) — merge divergent : vérifier la CONVERSE (réf morte qu'aucune branche seule n'avait)
- [localiser-repos-avant-fan-out](feedback_localiser_repos_avant_workflow_multi_repo.md) — localiser empiriquement chaque repo avant un workflow multi-repo
- [cross-repo-write-main-session](feedback_cross_repo_write_main_session.md) — les sub-agents sont bloqués en write cross-repo : ne pas déléguer

### Composants & délégation
- [ecrire-partout-invoquer-skill-creatrice](feedback_ecrire_partout_invoquer_skill_creatrice.md) — SKILL.md/agent/hook/CLAUDE.md : toujours via la skill créatrice, même hors forge
- [creator-reorganise-design-verrouille](feedback_creator_reorganise_design_verrouille.md) — un créateur peut diluer un design déjà verrouillé : vérifier le livrable
- [subagent-autocommit](feedback_subagent_autocommit.md) — les sub-agents committent malgré l'instruction : `git log` post-agent
- [edit-read-obligatoire](feedback_edit_tool_read_obligatoire.md) — Edit en parallèle sans Read = 7/8 échecs. Batch Read puis batch Edit
- [python-path-windows](feedback_python_path_windows.md) — hooks Windows : launcher `py`, jamais `python` nu ni chemin absolu
- [allocation-modele-effort](feedback_allocation_modele_effort.md) — Sonnet exécution / Opus jugement ; `high` au départ sur Opus 5, `xhigh` = step-up mesuré (⚠️ « xhigh par défaut » PÉRIMÉ)
- [preference-modele-opus](feedback_preference_modele_opus.md) — défaut opus-5 ; repli 4.8 ; jamais 4.7
- [test-writer-systematic](feedback_test_writer_systematic.md) — max 3 tests/comportement, REFACTOR supprimée, effort high

### Mémoire, vault & doctrine
- [correction-in-place-vault](feedback_correction_in_place_vault.md) — claim périmée = réécrire le CORPS en place, jamais bannière + addendum
- [single-source-of-truth](feedback_single_source_of_truth.md) — un concept = un fichier canonique ; les autres pointent
- [use-brain-skills-not-grep](feedback_use_brain_skills.md) — questions métier = MCP NeoBrain, jamais grep manuel ; une source nommée s'invoque visiblement
- [ton-vault-forge-pas-neoteem](feedback_ton_vault_forge_pas_neoteem.md) — « ton vault » = forge-brain, jamais le vault métier
- [consolidate-searches](feedback_consolidate_searches.md) — ne jamais chercher deux fois la même info
- [mcp-alias-ambigu](feedback_mcp_alias_ambigu_chemin_exact.md) — MCP par alias court résout faux si le stem est partagé : chemin exact
- [capitaliser-methode](feedback_capitaliser_methode_pas_que_resultat.md) — capitaliser la MÉTHODE réutilisable, pas que le résultat
- [regle-scope-pas-universelle](feedback_regle_scope_pas_universelle.md) — une règle validée sur un thème n'est pas universelle : vérifier avant de propager
- [pas-dogmatique-patterns-externes](feedback_pas-dogmatique-patterns-externes.md) — adapter un pattern externe, jamais l'appliquer par mimétisme
- config-repo-equipe-vs-forge — **promu vault** (8 juil.) : [[config-repo-equipe-vs-forge]]

### Méta — quand la règle ne suffit plus
- [feedback-reviole-3x](feedback_feedback_reviole_3x_regle_insuffisante.md) — re-violé ≥3× = la règle écrite ne suffit pas, il faut un garde-fou structurel
- [recurring-meta-anti-pattern](feedback_recurring_meta_anti_pattern.md) — workaround ≥2× = bug ; lister cran 1/2/3 avant refonte
- [zero-dette-technique](feedback_zero_dette_technique.md) — dette/drift découverte = nettoyage complet immédiat
- [perf-declenchement-avant-budget](feedback_perf_declenchement_avant_budget_skills.md) — skills : routing d'abord, budget ensuite
- [registre-relais-agents](feedback_registre-relais-agents.md) — HYPOTHÈSE à valider : registre « op coûteuse → artefact »

### Rédaction & livrables métier
- [classification-type-ticket-jira](feedback_classification_type_ticket_jira.md) — classer par NATURE (FEATURE/BUG/OPTIM), jamais par mimétisme
- [spec-trous-structurels](feedback_spec_trous_structurels_a_checker.md) — audit spec : Langfuse, 4 risques sécu IA, décisions sans assignee
- [raphael-pas-mise-en-avant](feedback_raphael_pas_mise_en_avant_cadrage_client.md) — docs Neoteem : le cadrage est une décision client
- [doc-pro-coherence-multi-docs](feedback_doc_pro_coherence_multi_docs.md) — pack de docs liés : relire la cohérence inter-docs
- [5-lignes-karpathy](feedback_5_lignes_karpathy_ouverture.md) — tout CLAUDE.md forge ouvre sur les 5 lignes Karpathy verbatim
- [emphasis-distinction](feedback_emphasis_distinction.md) — emphase OK en skills/rules, à réduire en tool descriptions (overtriggering)
- [secu-calibrage-pragmatique](feedback_secu_calibrage_pragmatique.md) — risque accepté sur base test si fix > impact ; jamais de nouveau secret committé

### Archive tier-2 (35 feedbacks)
> Valides mais sans citation entrante → [memory/_index_archive.md](_index_archive.md). Critère tier-1 : cité ≥1 OU stratégique ; réintégrer dès qu'un tier-2 est cité. Archives prouvées (obsolète/absorbé/one-shot) : `_archive/` + journal `MEMORY-archive-log.md`.

## Project
- [forge-review-journal](project_forge_review.md) — journal des verdicts KILL/EVOLVE/FUSION et leur suivi
- [neoteem-back-ts](project_neoteem_back_ts.md) — monorepo backend Loji ; 5 epics Jira FIGÉS (jamais en créer)
- [neo-ia](project_neo_ia.md) — monorepo Python NeoChat/NeoDoc/NeoMail, aligné sur back-ts
- [neo-ia-tool-selection](project_neo_ia_tool_selection.md) — HybridToolSelector : état prod + plan Lazy Expansion
- [dossier-strategique-ia](project_dossier_strategique_ia_neoteem.md) — dossier CODIR 17/20, roadmap V2 à venir
- [spec-unification-3repos](project_spec_unification_3repos.md) — /spec identique ×3 repos ; reste la normalisation des tickets Jira
- [deploy-methods-other-repos](project_deploy_methods_other_repos.md) — probablement absorbé par l'alignement de juin, à confirmer puis archiver

## User
- [raphael-picard-full-profile](user_raphael_profile.md) — profil holistique : rôle, parcours, vision, préférences de travail

## Reference
- [techniques-cheatsheet](reference_techniques_cheatsheet.md) — meilleure technique par besoin
- [workarounds-session-forge](reference_workarounds_session_constraints.md) — `gh` absent, x.com 402, HEREDOC Windows, fins de ligne via `git ls-files --eol`
- [creer-workflow-cc](reference_creer_workflow_cc.md) — 8 règles de design `.claude/workflows/` (à promouvoir vault au 2e-3e build)
- [subagent-permissions](reference_subagent_permissions.md) — worktree+MCP OK, `permissions.allow` toujours non hérité
- [agents-dir-chatgpt-adapters](reference_agents_dir_chatgpt_mirror.md) — `.agents/` + `AGENTS.md` = adaptateurs Codex d'une doctrine commune
- [repo-scope-guard-hook](hook_repo_scope_guard.md) — triplet auth-detector + repo-scope-guard + auth-cleanup
- [transcrire-video-native-x](reference_transcrire_video_native_x.md) — pipeline x-read → MP4 → ffmpeg → whisper (`/watch` ne couvre pas X)
- [bashrc-bind-warnings](reference_bashrc_bind_warnings.md) — warnings readline sans garde interactive
- [discord-webhook](reference_discord_webhook.md) · [gchat-webhooks](reference_gchat_webhooks.md) — webhooks notifications (JAMAIS committer les URLs)
