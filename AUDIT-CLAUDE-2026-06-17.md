# Audit global `.claude/` — claude-forge — 2026-06-17

> Audit profond multi-axes orchestré en 4 agents Opus parallèles (skills, hooks, rules+CLAUDE.md+memory, agents), chacun appliquant la séquence canonique A→B→C→D→E avec lecture intégrale des canoniques vault. Findings = `file:line` + écart mesurable. **C'est un audit, pas un chantier** : rien n'est modifié — Raphael arbitre.

## État des lieux

| Classe | Volume | Santé |
|---|---|---|
| Agents | 5 | Solide — 0 P0 |
| Hooks | 14 actifs (+ dispatchers + tests) | Bonne — 0 P0/P1 |
| Rules | 16 (dont 2 stubs) | _(en cours)_ |
| Skills | 53 (8742 lignes cumulées) | _(en cours)_ |
| CLAUDE.md | 112 lignes | _(en cours)_ |
| Memory | 269 fichiers (WARNING saturation) | _(en cours)_ |

---

## 🟢 HOOKS — santé BONNE, 0 P0/P1

14 hooks actifs, tous conformes Windows (`py` launcher, `${CLAUDE_PROJECT_DIR}`, forward slashes, timeouts, fail-open). 5 gardes critiques toutes testées (2 suites adverses). **Doctrine 22 mai respectée** : aucun hook ne force de pipeline agentique.

| P | Hook | Finding | Evidence | Reco |
|---|---|---|---|---|
| **P2** | metrics-tracker | PostToolUse **sans matcher = tous les outils**, ~450 ms/appel → ~900 ms autour de chaque outil (avec pre-bash-guards). **Preuve non-consommation : 17 jsonl collectés, 0 daily-summary** → io-daily/io-week n'ont jamais agrégé. Overhead = pur coût. | `settings.json:36-46` ; `metrics-tracker.py:26` ; `.claude/_metrics/` | **Arbitrage** : (a) KILL si tracking inutilisé, ou (b) garder + lancer io-week pour rentabiliser. JAMAIS passer en `python` direct (viole windows-hooks). |
| **P3** | session-health | Dead code : tente de supprimer le marker `.learning-reminder-fired` que personne n'écrit (vrai marker = `claude-forge-learning-reminded` en tempdir). | `session-health.py:55` vs `learning-reminder.py:12` | Supprimer lignes 54-60 via hook-creator. Inoffensif mais trompeur. |
| **P3** | settings.json | `"once": true` sur learning-reminder **silencieusement ignoré** dans settings (honoré uniquement en frontmatter skill). Cargo-cult. L'anti-boucle réelle = marker interne du hook. | `settings.json:64` | Retirer `"once": true` (sans effet). Cosmétique. |

**Câblage settings.json : sain.** Triplet `Write|Edit|MultiEdit` complet (pas de trou MultiEdit). Tous les hooks `.py` non-test câblés (directement ou via dispatcher), sauf `code-lint-dispatch` (= PostToolUse agent code-dev cross-repo, attendu). Deux watchers memory = métriques **orthogonales** (taille MEMORY.md vs nombre de fichiers) → garder les deux. `learning-reminder` = hook le plus proche de la ligne doctrinale mais **KEEP** (ne force aucun pipeline, dismissible, institutionnalisé par CLAUDE.md).

---

## 🟢 AGENTS — santé SOLIDE, 0 P0

5 agents. Frontmatter obligatoire (model/effort/memory/permissionMode) présent partout. Sonnet/Opus split cohérent.

| Agent | model | effort | memory | permissionMode | color | read-only | verdict |
|---|---|---|---|---|---|---|---|
| code-dev | sonnet | high | project | acceptEdits | green | N/A | CONFORME |
| devils-advocate | opus | high | project | plan | red | **PARTIAL** (a `Bash`) | écart P1 |
| outcomes-grader | opus | high | project | plan | **absent** | YES (prouvable) | écart P2 |
| repo-inspector | opus | xhigh | project | plan | purple | PARTIAL (by-discipline) | conforme s/réserve |
| self-updater | sonnet | high | project | acceptEdits | cyan | N/A | écart P1 (body↔hook) |

| # | P | Agent | Finding | Evidence | Reco |
|---|---|---|---|---|---|
| 1 | **P1** | devils-advocate | Read-only NON prouvable : disallowedTools Write/Edit mais `Bash` présent → peut écrire. Bash sans usage positif dans le body. | `devils-advocate.md:4,8,57` | **Retirer `Bash` de tools** → read-only prouvable + "JAMAIS heredoc" devient structurel. |
| 2 | **P1** | self-updater | Body↔hook contradictoire : étape 3 = Read+Edit direct des SKILL.md cc-*-ref, mais delegate-guard bloque (exit 2) tout SKILL.md non-kepano. | `self-updater.md:41-44` vs `delegate-guard.py:7,62` | Réécrire étape 3 → **déléguer à skill-creator** (déjà en frontmatter). |
| 3 | **P1** | 4 agents | `obsidian-markdown` en `skills:` jamais citée dans aucun body = orpheline **préchargée en contenu complet** → coût tokens récurrent. | `code-dev.md:12`, `devils-advocate.md:6`, `repo-inspector.md:14`, `self-updater.md:14` | Retirer `obsidian-markdown` des agents qui n'écrivent pas de notes. |
| 4 | **P2** | outcomes-grader | `color` absent (seul agent sans couleur). | `outcomes-grader.md:1-18` | Ajouter `color: yellow`. |
| 5 | **P2** | repo-inspector | `cc-advisor` en `skills:` jamais citée = orpheline préchargée. | `repo-inspector.md:12` | Retirer `cc-advisor`. |
| 6 | **P3** | devils-advocate | Méta-commentaire daté dans body ("vérifié 27 mai", "bug 22 mai"). | `devils-advocate.md:57` | Strip dates, garder l'instruction. |
| 7 | **P3** | repo-inspector | Read-only by-discipline (Bash+Agent requis, `Agent` intentionnel AMENDE 16 juin). | `repo-inspector.md:9,216` | Laisser tel quel. |
| 8 | **P3** | code-dev | `skills: forge-brain` non invoquée via outil Skill (body pointe vers rule). | `code-dev.md:11,46` | Aligner avec #3 si jamais invoquée. |

**Arbitrages** : repo-inspector `xhigh` justifié par doctrine CLAUDE.md 26 mai (exploration agentique multi-tours, nomme project-analyzer) > canonique plus ancienne — à confirmer. outcomes-grader `high` défendable (scoring nuancé = jugement). repo-inspector 3 modes JUSTIFIÉ (socle partagé, scinder = dupliquer ×3).

---

## 🟢 RULES + CLAUDE.md + MÉMOIRE — santé 16/20, 0 P0

16 rules cohérentes, CLAUDE.md 112 L (<200), 2 stubs propres (refs entrantes valides), zéro pointeur vault mort, aucun drift pré-22-mai résiduel.

| P | Cible | Finding | Evidence | Reco |
|---|---|---|---|---|
| **P1** | git-multi-repo.md | Pointeur mémoire **mort** : cite `feedback_git_C_pas_cd_multi_repo.md`, fichier réel = `feedback_git_C_pas_cd.md`. | `git-multi-repo.md:46` | Corriger → `feedback_git_C_pas_cd.md`. |
| **P1** | MEMORY.md | 3 feedbacks **archivés** (`_archive/2026-06/`) toujours en **tier-1**, chargés chaque session alors qu'absorbés. | `MEMORY.md:16,35,91` (arxiv-url-swap, da-bash-write, tweet-hype-paraphrase) | Les retirer du tier-1. Gain contexte net. |
| **P2** | comportement-proactif ↔ sequence-canonique | Séquence A→E **restituée inline** (5 étapes) PUIS pointeur. Single-source partiellement violé. | `comportement-proactif.md:60-69` vs `sequence-canonique-modification.md:8-20` | Réduire l'inline à 1-2 L + pointeur. Garder le "Brief minimum" verbatim (unique). |
| **P3** | rules + CLAUDE.md | Méta-commentaire justification-incident daté ("40 tours", "vérifié 27 mai"). | `check-before-create.md:17`, `delegate-to-specialists.md:41`, `memory-discipline.md:65`, `CLAUDE.md:14,27` | Strip date/incident, garder règle nue. KEEP ancres "doctrine 22 mai". |
| **P3** | feedback_consolidate_searches.md | Vieux format (accents ASCII), jamais cité, recoupe CLAUDE.md "Priorité des sources". | fichier entier | Candidat tier-2 ou suppression. |

**Recouvrements rules : tous NON-MERGE sauf l'inline A→E (P2).** CLAUDE.md ↔ git-multi-repo = complémentaires (politique branche vs convention CWD). check-before-create ↔ sequence-canonique = single-source intentionnel (rappel court→canonique). forge-brain-proactive ↔ memory-discipline = frontière propre (délégation explicite). CLAUDE.md = **orchestrateur sain** : pointeurs = routing, aucune section ne réimplémente une rule. **Stubs KEEP** (vraiment vides, refs entrantes confirmées par grep — anti-référence-cassée).

**Mémoire** : architecture tier-1/tier-2 en place, seuils MEMORY.md = ceux du hook. 269 fichiers > WARNING 250, mais plancher ~240 quasi-irréductible → **~29 candidats archive max, levier pas crise**. Frontière memory↔vault respectée (échantillon). Tous les wikilinks vault cités → existent (vérifiés search_brain).

---

## 🟢 SKILLS — santé TRÈS BONNE, 0 P0

53 skills. 0 BOM, 0 SKILL.md > 500L (max 376 = kepano), 0 description > 1024 chars, `user-invocable` correct 53/53, toutes les `references/` présentes citées dans leur body.

> **Prémisse de mon brief corrigée par l'agent** : le seuil "300 chars = risque troncature" est PÉRIMÉ. La vraie limite canonique est 1024 chars spec / 1536 combiné. Les 7 skills > 300 chars ne sont ni tronquées ni cassées. Le vrai levier d'activation = **phrasé passif**, pas longueur. Total 53 descriptions ≈ 12 971 chars (~3 200 tokens) — acceptable.

| # | P | Skill | Finding | Evidence | Reco |
|---|---|---|---|---|---|
| 1 | **P1** | cc-prompt-ref | 3 refs "mortes" (`guide-complet.md`, `api-reference.md`, `validate.sh`) absentes du disque — mais ce sont des **noms fictifs dans un bloc d'EXEMPLE** de structure, pas des refs chargées → pas un bug fonctionnel, juste trompeur. | `cc-prompt-ref/SKILL.md:167-169` | Remplacer par `<detail>.md` ou annoter "exemple". |
| 2 | P2 | cc-advisor | Désync : appelle `mcp__forge-brain__read_note` mais allowed-tools sans MCP. | `cc-advisor/SKILL.md:5` vs `:16,22` | Ajouter `mcp__forge-brain__*`. |
| 3 | P2 | evolve | Désync : Phase 0+3 appellent forge-brain mais allowed-tools sans MCP. | `evolve/SKILL.md:6` vs `:21,120` | Ajouter `mcp__forge-brain__*`. |
| 4 | P2 | cc-rag-ref | Body cite `mcp__forge-brain__` mais **aucun** allowed-tools déclaré. | `cc-rag-ref/SKILL.md` | Ajouter `allowed-tools: Read, mcp__forge-brain__*`. |
| 5 | P2 | cc-advisor | Pointeur vers stub absorbé `[[read-section-preference]]`. | `cc-advisor/SKILL.md:22` | Repointer vers `forge-brain-proactive.md` § read_section. |
| 6 | P2 | descriptions passives | Phrasé passif → auto-trigger ~77% vs ~100% directif. Concernées : evolve, recap, done, cc-cowork-ref, cc-prompt-ref, outcomes-test, spec, craft-prompt, cc-advisor. **Atténuation** : recap/done/io-* surtout déclenchées par /slash → impact faible. | frontmatters | Reformuler les ~4 à auto-trigger réel : evolve, outcomes-test, craft-prompt, cc-advisor. |
| 7 | P3 | io-daily/io-week | Parsing JSONL dupliqué. | les 2 SKILL.md | Merge optionnel `/io [day\|week]`, gain faible. Laisser. |
| 8 | P3 | evolve/skill-evolve | Collision noms → risque auto-trigger croisé (atténué par exclusions "NOT for"). | noms | Surveiller. |

**Aucune skill à tuer, aucun merge imposé.** Tous les candidats recouvrement (doctrine-impact-check/methode-pivoter-doctrine/pivot-check ; evolve/skill-evolve ; recap/done ; 4 creators ; cluster IA 5 skills) = **frontières intentionnelles balisées bidirectionnellement**, pas du recouvrement. Setup dev perso → la richesse se tolère. Skills kepano intouchables (mémoire). `memory:`/`permissionMode` absents de skills = non-problème (champs agent-only).

---

## 🎯 SYNTHÈSE TRANSVERSE

**Verdict global : config MÛRE et SAINE. Aucun P0 sur les 4 classes. 0 composant à tuer, 0 merge imposé.** L'audit confirme un setup discipliné — single-source tenu, doctrine 22 mai propre partout, frontières inter-composants explicites.

### Les fixes à fort levier (P1) — 6 au total, tous rapides
1. **devils-advocate** : retirer `Bash` de tools → read-only **prouvable par construction** (aujourd'hui contournable). _(subagent-creator)_
2. **self-updater** : étape 3 documente un Edit direct de SKILL.md que delegate-guard **bloque** → réécrire en délégation skill-creator. _(subagent-creator)_
3. **4 agents** : `obsidian-markdown` orpheline **préchargée en contenu complet** = coût tokens récurrent → retirer des agents qui n'écrivent pas de notes. _(subagent-creator)_
4. **git-multi-repo.md** : pointeur mémoire mort `feedback_git_C_pas_cd_multi_repo.md` → `feedback_git_C_pas_cd.md`. _(claudemd-creator/Edit rule)_
5. **MEMORY.md** : 3 feedbacks archivés encore en tier-1 (chargés chaque session) → retirer. _(Edit)_
6. **cc-prompt-ref** : 3 refs d'exemple trompeuses → annoter. _(skill-creator)_

### Le seul vrai arbitrage à impact (P2) — metrics-tracker
Le hook `metrics-tracker` tourne sur **chaque outil** (~900 ms autour de chaque appel avec les dispatchers) et **preuve empirique : 17 fichiers .jsonl collectés, 0 daily-summary** → io-daily/io-week n'ont **jamais** agrégé. L'overhead est un pur coût. → **KILL** (si tu n'utilises pas le tracking I/O) **ou** lancer io-week pour le rentabiliser. Jamais le passer en `python` direct (viole windows-hooks).

### Les désyncs allowed-tools (P2 skills) — 3 rapides
cc-advisor, evolve, cc-rag-ref appellent `mcp__forge-brain__*` sans le déclarer en allowed-tools → ajouter (pré-approbation, pas restrictif, mais cohérence).

### Le reste = polish cosmétique (P3)
Méta-commentaire daté dans rules/CLAUDE.md/devils-advocate, color outcomes-grader, descriptions passives (sélectif), io-daily/io-week merge optionnel, inline A→E dans comportement-proactif. **Mémoire 269 fichiers** : levier (~29 candidats archive max), pas crise — plancher ~240 assumé.

### Ce qui est explicitement SAIN (ne pas toucher)
Câblage settings.json, triplet Write|Edit|MultiEdit complet, doctrine 22 mai sur tous les hooks, 2 stubs rules, 4 creators distincts, cluster IA 5 skills, frontmatter obligatoire agents, 0 BOM/0 dépassement taille skills, learning-reminder (proche de la ligne mais KEEP justifié).

