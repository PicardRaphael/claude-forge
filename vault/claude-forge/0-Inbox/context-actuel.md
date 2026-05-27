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
**Système de maintenance MEMORY.md — LIVRÉ (2026-05-27).** Chantier A (fondation + dette) + Chantier B (skill `/clean-memory`) + run réel (3 fusions). Couche Python Jaccard initialement prévue puis **coupée** (verdict advisor + preuve : 10 orphelins détectés sans Jaccard = enforcement-théâtre sur corpus court/homogène). MEMORY.md 246→243L, feedbacks racine 196→193, 10 fichiers archivés dans `_archive/2026-05/`. Mergé sur main (`116246a`), branche `chantier-memory-maintenance` supprimée. 319 tests verts (176 hooks + 143 MCP) inchangés. Note canonique [[pattern-maintenance-hybride-corpus-accumulatif]] créée.

## Dernière session (2026-05-27) — Maintenance MEMORY.md
### Décisions prises
- **Couper la couche Python Jaccard** (Q1) : sur corpus court+homogène, le LLM regroupe sémantiquement mieux qu'une heuristique lexicale. Chantier C (Python) tracé conditionnel — réactiver SEULEMENT si l'usage de `/clean-memory` montre que le LLM rate systématiquement des clusters. Capitalisé : [[llm-lit-court-homogene-pas-couche-deterministe]].
- **Architecture archive 3 niveaux** : `MEMORY.md` (canonique vivante) + `_archive/YYYY-MM/` (append-only sacré, `git mv`) + `MEMORY-archive-log.md` (journal append-only, rollback par opération).
- **Skill `/clean-memory`** (309L, 0 script) : analyse LLM 4 sections (A doublons / B amendements / C ambigus à NE PAS fusionner / D dormants) + gate humain `[v]/[m]/[i]` par section (`[m]` anti tout-ou-rien). Section D : non-cité = nécessaire mais NON suffisant (57% du vault non wikilinké = la norme).
- **3 fusions validées** : A1 `verifier-claims-empiriquement` (audit-claims + sub-agent-claim, aliases pour 8+2 backlinks), A2 `tests-adverses-hooks-secu` (obligatoires + ratio-3-1, 3 backlinks), A3 `jarvis-innovator` absorbe `bras-droit`. A4 ignoré (parent/spécialisation), C1/C2 séparés (3 angles distincts / prescriptions opposées).
- **10 orphelins traités** (Chantier A) : 5 archivés (obsolètes doctrine 22 mai + cross-repo + hook supprimé) + 5 ré-indexés.

### Faits empiriques
- En mémoire `memory/`, pas de résolveur Obsidian : un `[[slug]]` est du texte. « Préserver un backlink » = mettre l'ancien slug en `aliases:` du méta (findability par grep/recall), pas une vraie résolution.
- `Measure-Object -Line` (PowerShell) peut sous-compter vs `wc -l` (SKILL.md : 219 vs 309). La "2e occurrence sub-agent-claim-sans-empirie" annoncée s'est révélée un FAUX POSITIF de ma part (le sub-agent avait raison, 309L) — instance de [[subagent-audit-category-error]]. Rien à tracker.

### Prochaines étapes
1. **/clear**, puis bilan suite du plan global.
2. `/clean-memory` réutilisable à la demande (ou périodiquement) sur MEMORY.md.

## Fils ouverts (repris des sessions antérieures, toujours valides)
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
