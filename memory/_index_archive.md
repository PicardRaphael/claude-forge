# Memory — Index Archive (tier-2)

Feedbacks **valides** mais **sans citation entrante ni statut stratégique** (dernier clean : 2026-09-25 — dédoublonnage des 18 entrées aussi indexées dans MEMORY.md, voir journal). Déplacés ici depuis `MEMORY.md` pour alléger le chargement contexte (le pointeur dans MEMORY.md y renvoie). Ne PAS supprimer — ce sont des apprentissages valides, simplement non cités. ⚠️ Ils sont **hors rappel automatique** : `memory-recall` ne lit que les liens de MEMORY.md et exclut ce fichier. On ne les retrouve qu'en ouvrant cette page.

**Un fichier = un seul index.** Un feedback listé dans MEMORY.md (tier-1) n'apparaît pas ici, et inversement.

**Critère de retour en tier-1 (MEMORY.md) :** dès qu'un feedback ici est cité par un autre feedback ou une note vault (`[[slug]]`), ou devient un sujet stratégique, le réintégrer dans MEMORY.md section Feedback et le retirer d'ici.

**Critère d'archivage réel (vers `_archive/`) :** distinct — un tier-2 n'est archivé que si obsolète/absorbé/one-shot daté avec preuve (voir `_archive/MEMORY-archive-log.md`). Tier-2 ≠ archivé.

## Feedback (tier-2 — 16 entrées)
- [audit-completude-pointeur-vs-orphelin](feedback_audit_completude_pointeur_vs_orphelin.md) — Audit complétude index/roadmap : un wikilink non résolu localement peut pointer vers une note existante ailleurs. search_brain chaque cible avant de la compter orpheline (60→41 réels)
- [audit-prompt-adaptatif-par-couche](feedback_audit_prompt_adaptatif_par_couche.md) — Auditer des prompts d'archi adaptative par COUCHE (core toujours-chargé strict vs conditional à-la-demande tolérant), lire blueprint.py + chaque prompt en entier. Compter ≠ juger ; `_disabled` ≠ mort
- [eval-trio-angles-complementaires](feedback_eval_trio_angles_complementaires.md) — Éval forge = TRIO (skill-evolve fin / forge-review stratégique / outcomes-test rubric). Chercher 3 angles avant conclure gap
- [ia-back-postgresjs-stack-drift-pattern](feedback_drizzle_postgresjs_drift.md) — Migration code ≠ migration .claude/. Grep stack OLD vs NEW (Drizzle→postgres.js)
- [jarvis-innovator-mindset](feedback_jarvis_innovator.md) — adaptateur historique : autorité active dans AGENTS.md (Contrat Jarvis) + `Raphael-Picard` ; ne pas charger comme préférence
- [major-mistakes](feedback_major_mistakes.md) — Erreurs à ne pas refaire : agent CTO, routing CLAUDE.md, bricoler sans rechercher
- [mcp-transport-stdio-http-crashloop](feedback_mcp_transport_stdio_http_crashloop.md) — FastMCP crash loop systemd + nginx 502 = transport stdio au lieu de http. Lire les logs AVANT de soupçonner l'OAuth
- [obsidian-skills-sacred](feedback_obsidian_skills_sacred.md) — Jamais supprimer les skills Obsidian officielles. Le MCP complète, ne remplace pas
- [org-blocks-github](feedback_no_github_cloud.md) — Orga Team bloque GitHub, pas de triggers cloud, tout en local Task Scheduler
- [pas-de-wakeup-pour-agents-background](feedback_pas_de_wakeup_pour_agents_background.md) — Jamais de ScheduleWakeup pour attendre mes propres agents background (le harness notifie à leur fin). Wakeup = travail externe non-tracké uniquement
- [plugin-admin-absorbe-readonly](feedback_plugin_admin_absorbe_readonly.md) — Plugin admin (write) absorbe fonctionnellement le read-only. Désinstaller le read-only sans perte (gain tokens). Vérifier allowed-tools
- [subagent-audit-category-error](feedback_subagent_audit_category_error.md) — Sub-agent audit flagge drift sur note citant des valeurs externes. Vérifier la source de vérité réelle
- [tag-projet-nom-repo-exact](feedback_tag_projet_nom_repo_exact.md) — Tag projet = nom EXACT du repo (underscore compris), vérifier disque + git remote avant fusion
- [vault-cat-guard-faux-positif-memory](feedback_vault_cat_guard_faux_positif_memory.md) — Hook vault-cat-guard bloque cat memory/ si commande contient "vault". Edit pas Bash
- [verifier-shadow-plugin-avant-ref-morte](feedback_verifier_shadow_plugin_avant_ref_morte.md) — Skill supprimée ≠ réf morte : find le shadow plugin par nom avant de purger
- [zip-import-slash-pas-compress-archive](feedback_zip_import_slash_pas_compress_archive.md) — Zip d'import Cowork = slashes. Compress-Archive met des backslashes → casse
