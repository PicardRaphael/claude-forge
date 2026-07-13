# Memory Index

## Feedback
- [perf-déclenchement avant budget](feedback_perf_declenchement_avant_budget_skills.md) — fusion/kill/trim skills : routing d'abord, budget ensuite (consigne 9 juil.)
- [registre-relais-agents](feedback_registre-relais-agents.md) — HYPOTHÈSE (à valider 2-3 cas) : registre léger « op coûteuse X faite → artefact Y », 1 ligne/op, consulté AVANT op coûteuse pour éviter le doublon multi-agent. Cf [[relais-inter-agents-fiable]]
- [allocation-modele-effort-doctrine](feedback_allocation_modele_effort.md) — Sonnet exécution / Opus jugement · xhigh RÉSERVÉ architect/dev-lead/refactor-pg, high ailleurs · calibrer par TYPE + mesurer avant bump (biais tokens Anthropic) · pipeline projet architect-first + code-reviewer séparé. Consolidé 9 juil. (ex opus47/all-opus/biais-full-thune)
- [brief-premisse-fausse-verifier-avant-executer](feedback_brief_premisse_fausse_verifier_avant_executer.md) — Brief peut poser prémisse fausse. Vérifier matériellement avant d'exécuter, surfacer si fausse
- [capitaliser-methode-pas-que-resultat](feedback_capitaliser_methode_pas_que_resultat.md) — Après un chantier redéployable, capitaliser la MÉTHODE (recette déploiement + routage dans la skill créatrice), pas que le RÉSULTAT. Prouvé 3× (16 juin)
- [carte-blanche-commit-push-tranche-pas-revalider](feedback_carte_blanche_commit_push.md) — "Carte blanche" = exécuter direct sans re-valider note par note
- [classification-type-ticket-jira](feedback_classification_type_ticket_jira.md) — Classer un ticket par sa NATURE (FEATURE/BUG/OPTIMISATION), jamais par mimétisme
- [commit-push-check-pattern](feedback_commit_push_check.md) — "regarde commit et push" = git status + diff avant push, jamais push aveugle
- config-repo-equipe-vs-forge — PROMU VAULT (8 juil.) : repo d'équipe ≠ machinerie forge (skills auto-portantes, hooks non-bloquants, pas de delegate-guard). Canonique : [[config-repo-equipe-vs-forge]]
- [couper-loops-decision-fatigue](feedback_couper_loops_decision_fatigue.md) — Après validation, trancher vite. 2 signaux : boucle "es-tu parfait" + session longue. Cap 3 advisor
- [cross-repo-write-main-session-only](feedback_cross_repo_write_main_session.md) — Session forge a write cross-repo, sub-agents bloqués. Ne pas déléguer fixes cross-repo
- [diagnostic-empirique-avant-affirmer-une-garde](feedback_diagnostic_empirique_avant_affirmer_garde.md) — Avant d'écrire qu'une garde existe (deny/hook), la vérifier + citer la preuve
- [ecart-consigne-chiffree-surfacer](feedback_ecart_consigne_chiffree_surfacer.md) — Écart à consigne chiffrée = surfacer pour arbitrage, jamais juger acceptable en silence
- [ecrire-partout-invoquer-skill-creatrice](feedback_ecrire_partout_invoquer_skill_creatrice.md) — Forge écrit cross-repo MAIS invoque TOUJOURS la skill créatrice (SKILL.md/agent/hook/CLAUDE.md jamais à la main), même hors forge — delegate-guard ne fire que sous forge/. Incident 24 juin
- [edit-tool-read-obligatoire-meme-en-parallele](feedback_edit_tool_read_obligatoire.md) — Edit en // sans Read = 7/8 failures. Batch Read d'abord, puis batch Edit
- [feedback-reviole-3x-regle-insuffisante](feedback_feedback_reviole_3x_regle_insuffisante.md) — Feedback re-violé ≥3× = règle insuffisante. Réflexe pré-action ou garde-fou structurel
- [git-C-pas-cd-multi-repo](feedback_git_C_pas_cd.md) — TOUJOURS git -C <path>, jamais cd && git. CWD persiste entre Bash calls
- [jarvis-innovator-mindset](feedback_jarvis_innovator.md) — Contrat Jarvis : partenaire, anticiper, innover, évoluer, franc, autonome, proactif
- [localiser-repos-avant-workflow-multi-repo](feedback_localiser_repos_avant_workflow_multi_repo.md) — Avant audit/workflow fan-out multi-repo, localiser empiriquement chaque repo (ls */.claude). neo_ia + ia_back sous Documents\neot-v2\
- [mcp-alias-ambigu-chemin-exact](feedback_mcp_alias_ambigu_chemin_exact.md) — MCP append_note/read par alias court résout faux si stem partagé. Chemin exact
- [merge-ref-morte-croisee](feedback_merge_ref_morte_croisee.md) — Merge de branches divergentes : vérifier la CONVERSE (un côté référence-t-il un fichier que l'autre supprime/archive ?) — réf morte qu'aucune branche seule n'avait, angle mort de commit-push-check
- [never-pure-executor](feedback_never_pure_executor.md) — JAMAIS mode exécutant pur, posture Jarvis active même sur prompts directifs/QA
- [python-path-windows-hooks](feedback_python_path_windows.md) — Windows : chemin absolu Python313 dans hooks, jamais "python" seul
- [recurring-meta-anti-pattern](feedback_recurring_meta_anti_pattern.md) — Workaround ≥ 2 fois = bug. AVANT refonte structurelle, lister cran 1/2/3
- [regression-diagnostic-diff-avant-redesign](feedback_regression_diagnostic_diff_avant_redesign.md) — Régression à point d'introduction connu = diff AVANT redesign, pas d'ancrage sur l'hypothèse user. Write-path résolu dans TOUS les points d'entrée
- [spec-trous-structurels-langfuse-secuia-decisions](feedback_spec_trous_structurels_a_checker.md) — Audit spec : checker 3 trous (Langfuse, 4 risques sécu IA, décisions sans assignee)
- [stop-over-verifying](feedback_stop_over_verifying.md) — Verdict direct si travail fait en session, pas relire 20 fichiers pour dire oui
- [subagent-autocommit-violation](feedback_subagent_autocommit.md) — Sub-agents committent malgré instruction. TOP gras + git log post-agent
- [test-writer-systematic](feedback_test_writer_systematic.md) — RÉVISÉ 22 mai : MAX 3 tests/comportement, REFACTOR supprimée, effort high
- [use-brain-skills-not-grep](feedback_use_brain_skills.md) — Questions métier/décisions = skill `neo-brain-dev-ia` (forge : MCP NeoBrain direct OK), jamais grep manuel — interroger le brain À FOND avant taxonomie/décision. Skill/source NOMMÉE par Raphael = l'invoquer VISIBLEMENT dès le 1er tool call, même en plan mode
- [verify-exhaustive-claims](feedback_verify_exhaustive_claims.md) — Grep de validation AVANT toute déclaration exhaustive (zéro, tous, aucun, complet)
- [zero-dette-technique-nettoyer-completement](feedback_zero_dette_technique.md) — Dette/drift/réf morte découverte = nettoyage COMPLET immédiat, jamais plus tard

### Archive de référence — tier-2 (35 feedbacks)
> Feedbacks valides mais sans citation entrante (ou non stratégiques), déplacés vers [memory/_index_archive.md](_index_archive.md) pour alléger le chargement. Accès via recherche/lecture directe si besoin. Critère tier-1 : cité ≥1 OU sujet stratégique. Réintégrer ici un tier-2 dès qu'il est cité. Archives prouvées (obsolète/absorbé/one-shot daté) : `_archive/` + journal `MEMORY-archive-log.md` (grand nettoyage 2026-07-09 : 64 fichiers).

## Project
- [forge-review-journal](project_forge_review.md) — Journal des reviews stratégiques : 9 juil. = 0 KILL, 2 fusions appliquées (cc-rag-ref→rag-design, web-search-canonical-source→rule), F2 trio doctrine en measure-first (output/mesure-F2-fusion-doctrine.md, hôte = methode-pivoter-doctrine 34 backlinks), delegate-guard.py.proposed en attente validation Raphael
- [neoteem-back-ts-project](project_neoteem_back_ts.md) — Monorepo backend Loji (ia_back→neoia-api + Drizzle + MCP par domaine). E0 + durcissement livrés, note 17,5/20. Hiérarchie Jira = 5 epics permanents FIGÉS (jamais en créer) ; story S1 = N2-111278 ([IA] FEATURE, parent N2-68082). Skill spec dans les repos cibles + plugin PO (copies forge supprimées 24 juin). Phase = 12 sous-tâches à rédiger au go
- [dossier-strategique-ia-neoteem](project_dossier_strategique_ia_neoteem.md) — Dossier Stratégique IA CODIR audité 17/20 (29 mai), roadmap V2 à venir, sortir volet salaire
- [neo-ia-project](project_neo_ia.md) — Monorepo Python NeoChat/NeoDoc/NeoMail, 12 agents, 36 skills, 18 rules, 18 hooks. Aligné modèle back-ts 10 juin (/feature, Default-FAIL, memory/, PR develop + git-guard). CI GitHub Actions était MORTE → bitbucket-pipelines.yml créé (activation humaine en attente)
- [neo-ia-tool-selection-state](project_neo_ia_tool_selection.md) — HybridToolSelector : expansion+reranking OFF en prod, Lazy Expansion + OATS validé
- [deploy-methods-other-repos](project_deploy_methods_other_repos.md) — Déployer 9e principe + skill-evolve all sur neo_ia et ia_back (probablement absorbé par alignement 10-11 juin — à confirmer puis archiver)
- [spec-unification-3repos](project_spec_unification_3repos.md) — Chantier 26 juin : /spec IDENTIQUE ×3 repos (SKILL unifié + repo-explorer + hook validation structure template + script sync), Phase 1+2 poussées. RESTE : normaliser 23 tickets Jira existants (IA-7/16/27 + Stories + sous-tâches) par editJiraIssue, prochaine session

## User
- [raphael-picard-full-profile](user_raphael_profile.md) — Profil holistique : Lead IA Neoteem, 36 ans, parcours atypique, gamer, vision expert IA reconnu

## Reference
- [bashrc-bind-warnings-non-interactive](reference_bashrc_bind_warnings.md) — Warnings bind readline sans garde `[[ $- == *i* ]]`
- [subagent-permissions-limitation](reference_subagent_permissions.md) — v2.1.101 : worktree+MCP OK, permissions.allow toujours non hérité
- [discord-webhook-jarvis](reference_discord_webhook.md) — Webhook Discord #veille-tech pour notifications Jarvis (JAMAIS commit)
- [gchat-webhooks](reference_gchat_webhooks.md) — Webhooks Google Chat ia_back + neo_ia + neoteem-brain
- [techniques-cheatsheet](reference_techniques_cheatsheet.md) — Cheat sheet : meilleure technique par besoin
- [workarounds-contraintes-session-forge](reference_workarounds_session_constraints.md) — Machine forge : gh absent, x.com 402, HEREDOC Windows
- [repo-scope-guard-hook](hook_repo_scope_guard.md) — Triplet auth-detector+repo-scope-guard+auth-cleanup : repos neot-v2/
- [transcrire-video-native-x](reference_transcrire_video_native_x.md) — Vidéo native X (pas YouTube) : x-read JSON → URLs MP4 → curl → ffmpeg WAV 16k → faster-whisper small. /watch ne couvre pas X
