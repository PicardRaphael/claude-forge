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
