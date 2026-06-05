# Journal d'archive mémoire

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
