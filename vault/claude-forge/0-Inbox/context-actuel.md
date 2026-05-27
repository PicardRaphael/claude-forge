---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-05-27
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
**Hygiène permissions `settings.local.json` — LIVRÉ (2026-05-27), commits en attente validation Raphael.** Épuration du fichier perso gitignored : 48→11 entrées allow. Le brief visait `settings.json` versionné mais celui-ci est discipliné (11 hooks vivants, 0 orphelin) — la dette ad-hoc était dans le local. 25 SAFE remove + 13 MCP redondants (couverts par `enableAllProjectMcpServers:true` au niveau tool, prouvé empiriquement). Backup `.claude/_backups/` (gitignored). settings.json versionné NON touché (option 2). 319 tests baseline inchangés (audit, rien côté tests).

## Dernière session (2026-05-27) — Nettoyage permissions settings.local.json
### Décisions prises
- **Périmètre : local seul** (AskUserQuestion). Le brief désignait `settings.json` mais la cartographie A a renversé la prémisse : versionné = discipliné, dette dans `settings.local.json`. Capitalisé : [[brief-premisse-fausse-verifier-avant-executer]].
- **13 MCP retirés après test empirique** (pas par inférence) : retrait `list_notes` + appel → succès sans prompt → `enableAllProjectMcpServers:true` couvre au tool-level. Capitalisé : [[enableallprojectmcp-couvre-tool-level]].
- **Backup hors-versionné** `.claude/_backups/` (choix Raphael : incohérent d'archiver un fichier perso gitignored dans memory/ versionné).

### Faits empiriques
- Le chiffre de base réel était **48** entrées (le « 51 » de ma cartographie A était une estimation visuelle erronée, corrigée par `comm` sur le backup). Corrigé honnêtement plutôt que propagé — c'est exactement le sujet du feedback capitalisé.
- **Re-sédimentation MCP observée** : le harness ré-ajoute l'entrée tool au `allow` après chaque appel MCP (`search_brain`, `append_note` ré-apparus en cours de session). Le retrait réduit le bruit à l'instant T mais certaines repoussent à l'usage. Pas une régression (0 prompt), nettoyage périodique cosmétique.
- Les `cp outcomes-test → ia_back/neo_ia` étaient des one-shot mortes (fichiers cibles vérifiés présents = déploiement terminé).

### Prochaines étapes
1. **Validation Raphael** des modifs versionnées (.gitignore + vault CHANGELOG/log + memory) → commits groupés. settings.local.json gitignored = aucun commit.
2. **/clear**, puis suite du plan global.

## Fils ouverts (repris des sessions antérieures, toujours valides)
- **Dette tracée — Re-sédimentation MCP settings.local** : observation 1-2 sessions futures pour mesurer empiriquement. Si entrées `mcp__forge-brain__*` repoussent dans le `allow` → investigation watcher comportement harness. Si elles ne repoussent pas → soldé (effet de bord du watcher en session active). Cf [[enableallprojectmcp-couvre-tool-level]].
- **Dette MCP alias ambigu** — 5e occurrence (27 mai). Hook `mcp-alias-guard.py` ne matche que `append_note` → étendre à `insert_section`/`read_section`/`update_note`. Réactiver si 6e occurrence ou si on traite la dette PowerShell cmdlets. Cf [[feedback_mcp_alias_ambigu_chemin_exact]].
- **GAP sécu cmdlets PowerShell-natifs destructeurs** : `security-guard.py` ne couvre que POSIX/git. `Remove-Item -Recurse -Force`, `Stop-Process`, `Clear-Content` non détectés. Déclencheur : session sécu dédiée ou incident.
- **Candidature hook `doctrinal-claim-guard`** (tracée, 1re occurrence) : warning PreToolUse sur affirmation de garde non prouvée dans CLAUDE.md/vault. Réactiver à la 2e occurrence. Cf [[feedback_diagnostic_empirique_avant_affirmer_garde]].
- **Double-source mémoire transitoire** : auto-memory native encore injectée en parallèle de l'@import. Cf [[import-ajoute-pas-remplace-automemory]].
- **A1×A3 tué** : ne pas réouvrir le scan rétroactif sans donnée infirmant le 0/12. Cf [[idee-compounding-retroactif]] (TUÉE).
- **Paquet 2 Chantier A (C4-C7)** : différés, à évaluer après usage réel du pont doctrine-vivante.
- **TODO P0** : rotation password PostgreSQL prod (secret redacté mais pas tourné). Cf [[todo-rotation-password-postgres-prod]].
- **Chantier C — normalisation `handle_x`** des 80 fiches `05-Leaders/` (chantier d'auteur ~1-2h, mode dégradé en attendant). Cf [[pattern-vault-source-unique-sync-mecanique]].
- **README périmé** (21 outils / 412 notes) — session dédiée.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[pattern-maintenance-hybride-corpus-accumulatif]]
[[llm-lit-court-homogene-pas-couche-deterministe]]
[[doctrine-vivante]]
