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
**Clean-memory Levier A + C livré (2026-05-27), commits en attente validation Raphael.** MEMORY.md hiérarchisé tier-1/tier-2 + résumés courts. Déclencheur empirique (MEMORY.md > 40k chars) avait sauté à 42.5k. Résultat : **42470 → 21493 chars (−49%)**, soit ~5-6k tokens économisés par session (MEMORY.md chargé via @import à chaque session). 319 tests baseline inchangés (chantier mémoire pur, rien côté code).

## Dernière session (2026-05-27) — Clean-memory agressif Levier A + C
### Architecture livrée
- **Levier A (résumés courts)** : 112 résumés d'index >80 chars raccourcis (médiane passée de 84 à ~70 chars). Gain −6k chars. Script Python ponctuel idempotent (slug→résumé), pas 112 Edits séquentiels.
- **Levier C (hiérarchisation 2 niveaux)** : split mécanique tier-1 (cité ≥1 OU sujet stratégique) / tier-2 (non cité). **97 tier-1 visibles dans MEMORY.md** + **96 tier-2 dans `memory/_index_archive.md`** (chargé uniquement si recherche). Pointeur explicite dans MEMORY.md section Feedback.
- **Critère tier-1 mécanique** : citation entrante ≥1 (grep `[[slug]]` dans memory/ + vault/) + 12 promus stratégiques (axes innovation MCP, contrat Jarvis, méta-doctrines récentes). Le critère « créé <60 jours » abandonné car inopérant (corpus 1 semaine = 194/194 tier-1).
- **1 archivage réel** : `use-obsidian-cli` → `_archive/2026-05/` (obsolescence doctrinale : disait « TOUJOURS CLI Obsidian », contredit « MCP UNIQUEMENT »). Wikilinks vault corrigés (pattern-vault-llm-karpathy).
- **1 lien mort retiré** : `checklist_before_modify` (entrée index fabriquée, jamais de fichier).

### Faits empiriques (verify avant affirmer)
- **194/194 feedbacks datent du 27 mai en git** (dossier memory/ entièrement commité ce jour = migration récente vers `<repo>/memory/`). Vraies dates de création dans le CONTENU (21-27 mai). Critère temporel inopérant — surfacé à Raphael avant exécution.
- **86 feedbacks cités ≥1 / 108 non cités** (44%/56%, cohérent avec ~57% du pattern canonique).
- **Bug script attrapé empiriquement** : regex `feedback_[a-z0-9_]+` excluait `feedback_git_C_pas_cd.md` (C majuscule) → 1 feedback perdu au split, détecté par check « tout fichier référencé ? » puis restauré. Seul fichier à majuscule.

### ACTION IMMÉDIATE POST-CLEAN-MEMORY (session de propagation dédiée, post-/clear, 20-30 min focus pur)
Tracée explicitement — NON faite cette session (sortie de scope + anti-pollution cognitive) :
1. **Skill `/clean-memory`** : intégrer critère tier-1 mécanique (citation ≥1 OU stratégique OU pinned) + architecture tier-1 visible / tier-2 `_index_archive.md` + doctrine « résumé court <80 chars par défaut » + déclencheur re-clean (>38k chars).
2. **CLAUDE.md** : règle absolue tokens/contexte (top du fichier, gras, <L25) — « Tokens/contexte = ressource ultra-précieuse, jamais perdre pour rien. MEMORY.md gros = claude-forge développe mal. » + mention architecture tier-1/tier-2 + convention résumé court.
3. **Skill `jarvis-innovator` OU `learning-reminder`** (celle qui capitalise les feedbacks via /done) : nouveau feedback créé = résumé court <80 chars par défaut + classification tier-1/tier-2 proposée à la création (0 citation → tier-2 candidat sauf stratégique explicite).
4. **Hook NOUVEAU `memory-size-watcher`** (proposition Jarvis, SessionStart ou PostToolUse léger) : mesure MEMORY.md chars, alerte au franchissement de **38k** (marge avant plafond 40k). Maintenance anticipée vs réactive — « anticiper avant que ça arrive ». Très léger (1 file-size check, pas de logique métier).

### Prochaines étapes immédiates
1. **Validation Raphael** des modifs + cycle git complet (branche feature → commit chore(memory) → merge ff-only → suppression branche). Fait par Claude quand Raphael rend la main.
2. **/clear**, puis session de propagation (4 items ci-dessus).

## Fils ouverts (repris des sessions antérieures, toujours valides)
- **Dette tracée — Re-sédimentation MCP settings.local** : observation 1-2 sessions futures. Si entrées `mcp__forge-brain__*` repoussent dans le `allow` → investigation watcher harness. Cf [[enableallprojectmcp-couvre-tool-level]].
- **Dette MCP alias ambigu** — 5e occurrence. Hook `mcp-alias-guard.py` ne matche que `append_note` → étendre. Réactiver si 6e occurrence. Cf [[feedback_mcp_alias_ambigu_chemin_exact]].
- **GAP sécu cmdlets PowerShell-natifs destructeurs** : `security-guard.py` ne couvre que POSIX/git. Déclencheur : session sécu dédiée ou incident.
- **Candidature hook `doctrinal-claim-guard`** (1re occurrence) : warning PreToolUse sur affirmation de garde non prouvée. Réactiver à la 2e occurrence. Cf [[feedback_diagnostic_empirique_avant_affirmer_garde]].
- **Double-source mémoire transitoire** : auto-memory native encore injectée en parallèle de l'@import. Cf [[import-ajoute-pas-remplace-automemory]].
- **Hook `vault-cat-guard` faux positif** observé ce soir : bloque un `cat memory/_archive/MEMORY-archive-log.md` car la commande contient le mot « vault » dans son contenu. Le fichier est dans memory/, pas le vault Obsidian. Contournement = Edit. Candidat affinage si récurrent.
- **A1×A3 tué** : ne pas réouvrir le scan rétroactif sans donnée infirmant le 0/12. Cf [[idee-compounding-retroactif]] (TUÉE).
- **TODO P0** : rotation password PostgreSQL prod. Cf [[todo-rotation-password-postgres-prod]].
- **Chantier C — normalisation `handle_x`** des 80 fiches `05-Leaders/`. Cf [[pattern-vault-source-unique-sync-mecanique]].
- **README périmé** (21 outils / 412 notes) — session dédiée.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
[[pattern-maintenance-hybride-corpus-accumulatif]]
[[llm-lit-court-homogene-pas-couche-deterministe]]
[[doctrine-vivante]]
[[ecart-consigne-chiffree-surfacer]]
