# Memory — Index Archive (tier-2)

Feedbacks **valides** mais **sans citation entrante ni statut stratégique** (dernier clean : 2026-07-09, grand nettoyage — 64 fichiers archivés avec preuve, voir journal). Déplacés ici depuis `MEMORY.md` pour alléger le chargement contexte (le pointeur dans MEMORY.md y renvoie). Ne PAS supprimer — ce sont des apprentissages actifs, simplement non cités.

**Critère de retour en tier-1 (MEMORY.md) :** dès qu'un feedback ici est cité par un autre feedback ou une note vault (`[[slug]]`), ou devient un sujet stratégique, le réintégrer dans MEMORY.md section Feedback.

**Critère d'archivage réel (vers `_archive/`) :** distinct — un tier-2 n'est archivé que si obsolète/absorbé/one-shot daté avec preuve (voir `_archive/MEMORY-archive-log.md`). Tier-2 ≠ archivé.

## Feedback (tier-2 — 35 entrées)
- [5-lignes-karpathy-ouverture-claudemd](feedback_5_lignes_karpathy_ouverture.md) — Tout CLAUDE.md forge commence par 5 lignes Karpathy verbatim. ⚠ Porte une divergence vs canonique vault (ne PAS propager aux repos non-code type neoteem-brain) — à replier dans [[comment-ecrire-claudemd]] puis archiver
- [audit-completude-pointeur-vs-orphelin](feedback_audit_completude_pointeur_vs_orphelin.md) — Audit complétude index/roadmap : un wikilink non résolu localement peut pointer vers une note existante ailleurs. search_brain chaque cible avant de la compter orpheline (60→41 réels)
- [audit-prompt-adaptatif-par-couche](feedback_audit_prompt_adaptatif_par_couche.md) — Auditer des prompts d'archi adaptative par COUCHE (core toujours-chargé strict vs conditional à-la-demande tolérant), lire blueprint.py + chaque prompt en entier. Compter ≠ juger ; `_disabled` ≠ mort
- [autonomy-initiative-rule](feedback_autonomy_rule.md) — Si advisor+DA valident → agir sans demander. Proposer innovations proactivement
- [avis-franc-ecrit-dans-livrable](feedback_avis_franc_ecrit_dans_livrable.md) — Avis de fond franc + choix binaire net + dangers noir sur blanc DANS le livrable
- [conformite-aveugle-regle-generique](feedback_conformite_aveugle_regle_generique.md) — Garde refusée = lire son intention avant de contourner. Souvent intentionnelle
- [consolidate-searches](feedback_consolidate_searches.md) — Ne jamais chercher 2× la même info. Consolider en 1 fichier dès le 1er search
- [creator-reorganise-design-verrouille](feedback_creator_reorganise_design_verrouille.md) — skill/agent-creator réorganise/dilue un design verrouillé avec l'user. Vérifier bloc par bloc vs design validé, briefer "ne pas réinterpréter"
- [doc-pro-coherence-multi-docs](feedback_doc_pro_coherence_multi_docs.md) — Pack de docs liés : relire mot à mot la cohérence inter-docs avant de livrer
- [emphasis-prompt-vs-skill](feedback_emphasis_distinction.md) — Emphasis OK dans skills/rules/agents, réduire uniquement dans tool descriptions
- [eval-trio-angles-complementaires](feedback_eval_trio_angles_complementaires.md) — Éval forge = TRIO (skill-evolve fin / forge-review stratégique / outcomes-test rubric). Chercher 3 angles avant conclure gap
- [ia-back-postgresjs-stack-drift-pattern](feedback_drizzle_postgresjs_drift.md) — Migration code ≠ migration .claude/. Grep stack OLD vs NEW (Drizzle→postgres.js)
- [major-mistakes](feedback_major_mistakes.md) — Erreurs à ne pas refaire : agent CTO, routing CLAUDE.md, bricoler sans rechercher
- [mcp-transport-stdio-http-crashloop](feedback_mcp_transport_stdio_http_crashloop.md) — FastMCP crash loop systemd + nginx 502 = transport stdio au lieu de http. Lire les logs AVANT de soupçonner l'OAuth
- [merge-markers-grep-avant-commit](feedback_merge_markers_grep_avant_commit.md) — Conflit résolu = grep 0 marqueur AVANT commit (marqueur committé 10 juin)
- [obsidian-skills-sacred](feedback_obsidian_skills_sacred.md) — Jamais supprimer les skills Obsidian officielles. Le MCP complète, ne remplace pas
- [org-blocks-github](feedback_no_github_cloud.md) — Orga Team bloque GitHub, pas de triggers cloud, tout en local Task Scheduler
- [osef-pragmatique-dette-conditionnelle](feedback_osef_pragmatique_dette_conditionnelle.md) — OSEF assumé sur sujet faible levier + dette conditionnelle tracée (≠ couper loops)
- [pas-dogmatique-patterns-externes](feedback_pas-dogmatique-patterns-externes.md) — Adapter un pattern externe à forge, jamais par mimétisme (agent-first)
- [pas-de-wakeup-pour-agents-background](feedback_pas_de_wakeup_pour_agents_background.md) — Jamais de ScheduleWakeup pour attendre mes propres agents background (le harness notifie à leur fin). Wakeup = travail externe non-tracké uniquement
- [plan-commits-vs-working-tree-reel](feedback_plan_commits_vs_working_tree_reel.md) — git status AVANT, isoler le hors-scope dans un commit dédié, signaler l'écart
- [plugin-admin-absorbe-readonly](feedback_plugin_admin_absorbe_readonly.md) — Plugin admin (write) absorbe fonctionnellement le read-only. Désinstaller le read-only sans perte (gain tokens). Vérifier allowed-tools
- [preference-modele-opus-4-8](feedback_preference_modele_opus.md) — Ordre Opus (MAJ 27 juil.) : défaut `claude-opus-5` (mapping CLAUDE.md, surveiller) ; repli 4.8 (préférence validée) puis 4.6 ; JAMAIS 4.7 (jugé moyen)
- [present-before-build](feedback_present_before_build.md) — Présenter le plan AVANT construire, jamais créer sans validation Raphael
- [raphael-pas-mise-en-avant-cadrage-client](feedback_raphael_pas_mise_en_avant_cadrage_client.md) — Docs Neoteem : ne pas mettre Raphaël en avant ; cadrage = décision client
- [regle-scope-pas-universelle](feedback_regle_scope_pas_universelle.md) — Vérifier scope règle AVANT propagation. Provider sur SON produit = single source
- [secu-calibrage-pragmatique](feedback_secu_calibrage_pragmatique.md) — Risque sécu base test OK si remédiation coûteuse. JAMAIS secret commité
- [single-source-of-truth](feedback_single_source_of_truth.md) — UN fichier canonique par concept, skills pointent vers doc/
- [subagent-audit-category-error](feedback_subagent_audit_category_error.md) — Sub-agent audit flagge drift sur note citant des valeurs externes. Vérifier la source de vérité réelle
- [tag-projet-nom-repo-exact](feedback_tag_projet_nom_repo_exact.md) — Tag projet = nom EXACT du repo (underscore compris), vérifier disque + git remote avant fusion
- [ton-vault-forge-pas-neoteem](feedback_ton_vault_forge_pas_neoteem.md) — « Ton vault » = forge-brain (mon cerveau), JAMAIS le vault Neoteem métier
- [vault-cat-guard-faux-positif-memory](feedback_vault_cat_guard_faux_positif_memory.md) — Hook vault-cat-guard bloque cat memory/ si commande contient "vault". Edit pas Bash
- [verifier-shadow-plugin-avant-ref-morte](feedback_verifier_shadow_plugin_avant_ref_morte.md) — Skill supprimée ≠ réf morte : find le shadow plugin par nom avant de purger
- [verify-empirique-avant-affirmation-session](feedback_verify_avant_affirmation_session.md) — Avant d'affirmer "X parce que Y" sur changement filesystem/repo : git log/diff/blame d'abord. Distinct de diagnostic-empirique-avant-affirmer-une-garde (scopes différents — NON-fusion canonique)
- [zip-import-slash-pas-compress-archive](feedback_zip_import_slash_pas_compress_archive.md) — Zip d'import Cowork = slashes. Compress-Archive met des backslashes → casse
