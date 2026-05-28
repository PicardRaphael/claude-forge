---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: ["context actuel", "contexte courant", "working memory", "memoire de travail", "etat actuel"]
type: context
status: active
derniere-maj: 2026-05-28
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle

Audit lifecycle forge complet (A2) — post audit context tokens. Cartographie empirique 49 skills + 10 agents + 10 rules + 12 hooks. Etat : SAIN avec dette legere localisee. 3 KILL + 1 AMEND executes, baseline 181 maintenue.

## Audit lifecycle 2026-05-28 (A2)

### Cartographie empirique
- 49 skills forge (28 user-invokable / 21 internal) — toutes citees vault ou interne, aucune orpheline pure
- 10 agents forge + 3 user-scope auditeurs (boris/ecc/will) — frontmatter conforme
- 10 rules — 1 zero-ref (agents-color-convention) detectee
- 12 hooks fs <-> settings.json — 12/12 alignes
- agent-memory/ — 1 dir orpheline (vault-maintainer/, agent killed 27 mai)

### Actions executees
- **P0 KILL** : `.claude/agent-memory/vault-maintainer/` (residu agent killed)
- **P1 KILL** : `/forge-status` skill (42L, doublon partiel /recap + /install-forge, 0 ref active) — **KILL PRAGMATIQUE sans support doctrinal**, assume, trace CHANGELOG. Backup zip dispo si restore.
- **P1 KILL** : `.claude/rules/agents-color-convention.md` (26L, 0 ref empirique) — support canonique [[comment-creer-agent]] matrice 8 couleurs verbatim
- **P2 AMEND** : `.claude/agents/agent-creator.md` (+14L) — matrice 8 couleurs absorbee inline (compensation KILL rule)

### Validation cohérence empirique canoniques (post-hoc audit 28 mai)
- 5 canoniques lues EN ENTIER via `mcp__forge-brain__read_note` : comment-creer-agent, comment-creer-skill, pattern-mcp-brief-then-direct, 3-axes-strategiques-forge, doctrine-vivante
- 2/3 KILL supportés par canoniques (vault-maintainer + rule color)
- 1/3 KILL pragmatique assumé sans support (forge-status) → feedback `kill-pragmatique-vide-doctrinal` créé tier-1

### Dimension 2 — Workflow vault-invocation pattern (Règles 1/2/3)
Pattern déjà canonisé dans [[pattern-mcp-brief-then-direct]] — pas un trou doctrinal. AJOUT 28 mai append : grille catégories→vault-requis (4 catégories) + critère audit empirique reproductible.

### AMEND post-audit (canoniques vault)
- **`cc-advisor`** : ajout Étape 0 lecture canoniques avant recommandation (comment-creer-skill/agent/hook + mcp-vs-skills-doctrine)
- **`evolve`** : ajout Phase 0 lecture canoniques avant scan (methode-analyser-repo + comment-ecrire-claudemd + mcp-vs-skills-doctrine)

### Dette future tracée
- **Trou doctrinal `comment-creer-rule`** : note canonique absente du vault. Audit rules s'est fait sans canonique de référence (doctrine présente dans `comment-ecrire-claudemd` + `raisonnement-22mai-doctrine-vs-enforcement`, mais pas de note dédiée). Priorité P2 — peu de rules, déclencheur = prochaine création/refonte de rule.

### Backup defensif
`.claude/_backups/lifecycle-audit-2026-05-28.zip` (8 KB) — 4 cibles avant destruction

### Verification baseline
- Tests hooks : **181 PASS** (avant et apres)
- Hooks fs <-> settings.json : 12/12 alignes maintenus
- agent-creator.md : 98L -> 112L (cible 113-115 estimee, 112 OK)

### Workflows / coherence cross-composants
Aucun gap workflow detecte. Inter-skills coherents :
- audit->fix cluster, /clean-memory->git, /done, /spec->JIRA, /pivot-check, methode A->B->C->D->E

### A retenir
- Pas de capitalisation feedback nouvelle (audit confirme etat SAIN, rien de structurel a apprendre)
- 15 skills sans `model:` = legitime (heritage parent, canonique)
- 9 skills desc >250 chars = marginal (≤16 chars over), polish optionnel
- 3 skills >300L (done/clean-memory/obsidian-bases) = toutes <500L canonique

## Derniere session (2026-05-28)

### Decisions prises

- **Step 1** : purge auto-memory user-scope (240 fichiers -> 1), migration 4 valides vers memory/ projet (bras-droit, neoteem-brain-pipeline, tests-adverses-obligatoires, tests-adverses-ratio-3-1)
- **Step 2** : cap 9 skills desc > 250 chars selon formule directive Anthropic, via dispatch skill-creator + verif empirique
- **Step 3** : forge-brain-proactive.md condense 2 592 -> 738 tokens (-72%) par deport vers vault canonique
- **Step 4** : sequence-canonique-modification.md condense 2 403 -> 1 122 tokens (-53%)
- **Step 5** : CLAUDE.md condense 2 780 -> 2 473 tokens (Workflow Git + Vault + Gotchas), version 3.4
- **Step 6** : audit plugins 4 repos via AskUserQuestion structure, decisions arbitrees Raphael
- **Step 7** : edit direct ~/.claude/settings.json user-scope (6 plugins retires) + neo_ia/ia_back/.claude/settings.json (neoteem-brain-dev read-only retire)

### Etat final plugins

User-scope enabledPlugins : `neoteem-brain-dev-ia`, `neoteem-brain-dev-admin`, `neoteem-brain-support-admin` + `plugin-dev:false`
Project-scope neo_ia/ia_back : `superpowers`, `feature-dev`, `claude-hud`, `plugin-dev`, `neoteem-brain-dev-ia`

### En cours

Rien d'actif. Tous les Steps 1-7 livres et mesures empiriquement.

### Prochaines etapes

- Verifier mesure /context reelle en nouvelle session (re-tirer le tokenizer Claude effectif)
- Si gain confirme > 15k tokens, considerer enchainer sur scenario AGRESSIF (refonte memory/MEMORY.md tier-1 strict, refonte rules check-before-create + delegate-to-specialists + sequence-canonique en 1 fichier maitre)
- Sinon : laisser stabiliser 1-2 semaines, observer si dérive ou regression

## Fils ouverts

- `obsidian@obsidian-skills` charge via marketplace auto-discovery (pas dans enabledPlugins) — mecanisme non desactivable sans retirer Plugin:* permissions ou la declaration marketplace. A surveiller si tokens cost devient genant
- `feedback-triage` desinstalle global — verifier que Cowork remote routines fonctionnent encore (pas teste cette session)
- Backup `_auto_memory_backup_pre_purge_2026-05-28.zip` dans `memory/` — supprimer apres 7-30 jours sans regret

## Liens

[[Raphael-Picard]]
[[Claude-Forge]]
[[feedback_plugin_admin_absorbe_readonly]]
[[feedback_plugin_suffixe_ia_pas_readonly]]
[[feedback_askuserquestion_arbitrage_destructif]]
[[reference_plugins_scoping_mecanisme]]
[[reference_self_modification_user_scope_passe]]


## Session 2026-05-28 (suite) — Bilan global 27-28 + test oracle vault-first

### Livrables

- **[[journee-27-28-mai-2026]]** — note synthèse bilan 2 jours créée Knowledge/syntheses/
- **Test empirique oracle vault-first** : 3 scénarios CONFORME (skills/prompt-eng/capitalisation)
- **AMEND** [[CC mai 2026 - Code with Claude]] : section "AJOUT 28 mai 2026 — Champs settings.json avancés" (v2.1.128/136/143 + helpers auth + skills avancés + drop-in + sandbox détaillé)

### Verdict oracle vault-first

3/3 CONFORME. Séquence type observée :
- S1 : 1× search_brain + 1× read_note entier
- S2 : 2× search_brain + 1× read_note entier
- S3 : 1× WebFetch + 3× search_brain (non-doublon) + 1× append_note AMEND

Aucune réponse "depuis savoir interne sans vault". Pattern "vérif non-doublon AVANT capitaliser" appliqué (S3 a amendé canonique existante au lieu de créer doublon).

### Chiffres empiriques vérifiés (vs brief mémoire)

- 113 commits 2 jours (110 le 27 + 3 le 28) ≠ "~2 jours" approximatif du brief — déséquilibre normal (27 = vague structurelle, 28 = audits)
- 48 skills (pas 49 mentionné dans context-actuel précédent) — écart -1, marginal
- 10 agents + 9 rules + 12 hooks confirmés
- Baseline 181 tests PASS maintenue

### Cycle git exécuté

2 commits livrés (working tree clean post-/done) :
1. `b364c51` — docs(vault): bilan journee 27-28 mai + AMEND CC mai 2026 (test oracle vault-first 3/3 CONFORME)
2. `10e4124` — docs(vault): context-actuel + CHANGELOG + log post bilan global 27-28

Branch `main` à +3 commits d'origin/main (push GitHub bloqué orga Team, traces locales OK).

### Prochaine étape

- Valider `/context` empirique en nouvelle session (gain estimé > 15k tokens)
- Si confirmé : déclencher scénario AGRESSIF (refonte memory tier-1 strict + fusion rules check-before-create/delegate/sequence-canonique)
- Sinon : laisser stabiliser 1-2 semaines

## 2026-05-28 — SELF_PORTRAIT régénéré (condensé 151L)

- Renommage `CLAUDE_FORGE_SELF_PORTRAIT.md` (631L, 27/05) → `SELF_PORTRAIT.md` (151L, 28/05)
- Réduction ~76% : suppression annexes Hermes, doctrine détaillée (déléguée wikilinks), exemples concrets (déjà dans canoniques)
- Chiffres remesurés empiriquement : 48 skills (+1), 10 agents forge (-1), 12 hooks Python (+1 inline), 9 rules (-1 KILL), 453 notes vault (+23), 181 tests verts (143 mcp + 38 hooks), MEMORY.md 24,6k + archive 16,6k
- Structure : identité / chiffres / archi / composants vivants / doctrine wikilinks / edge mondial 3 axes / validations 27-28 / dettes tracées / engagement Anthropic
- Tonalité : factuelle pure, wikilinks vault au lieu de duplication, écarts vs ancien doc signalés en 1 ligne discrète
- Cycle git proposé : 1 commit `docs(repo): SELF_PORTRAIT final condensé 28 mai (151L vs 631L)`


## 2026-05-28 (soir) — OVERVIEW.md Anthropic livré + correction chiffre tests 324

**Livrables** :
- `OVERVIEW.md` créé (230L) — présentation externe destinée Anthropic / Boris Cherny / pairs CC. 9 sections : cadrage, 3 axes innovation, architecture défensive avec snippet `vault-cat-guard.py`, mécanismes anti-drift, méthodologie, validations empiriques, limitations honnêtes, travail en cours, contact.
- `README.md` aligné : chiffres mis à jour (10 agents, 48 skills, 12 hooks, 9 rules, 438 notes), paragraphe 3 axes ajouté, double pointeur OVERVIEW (externe) + SELF_PORTRAIT (interne).
- `SELF_PORTRAIT.md` patch : 3 occurrences chiffre tests obsolète corrigées.

**Découverte forensique bug GitHub #60237** : closed, titre exact *"Sub-agent frontmatter `tools:` array silently drops first and last positions at spawn time"*. Ne concerne PAS le frontmatter MCP/skills (hypothèse initiale). C'est une **cause-racine plausible** du symptôme "MCP décoratif sub-agent" observé empiriquement : sur tous sub-agents forge, `mcp__forge-brain__*` est en position 1 du `tools:` array → corrélation forte avec le drop position 1 documenté. Repro formel pas fait → noté §8 OVERVIEW comme travail-en-cours avec disclaimer honnête.

**Correction chiffre tests 181 → 324 (capté par advisor avant commit)** : SELF_PORTRAIT portait "181 verts (143 mcp + 38 hooks)" depuis ≥1 session. Mesure empirique au moment de la validation : 143 (mcp-forge-brain) + **181** (hooks, pas 38 — confusion fichiers vs cas de tests) = **324**. Brief Raphael étape 5 relayait passivement le chiffre obsolète. Fix appliqué : 3 occurrences OVERVIEW + 2 occurrences SELF_PORTRAIT corrigées même commit. Feedback `chiffre-baseline-brief-verifier-empiriquement` amendé section "Renforcement 2e occurrence" — pattern observé dans 2 chantiers distincts (clean-memory 28 mai matin + OVERVIEW 28 mai soir) = règle insuffisante seule, candidat garde-fou structurel (verification empirique automatique avant relais chiffre SELF_PORTRAIT).

**Discipline mesurer-avant-proclamer appliquée jusqu'au bout** : 2 chiffres SELF_PORTRAIT non re-vérifiables (`2,68s session_messages eager-boot`, `4 attributions doctrinales fausses`) → généralisés dans OVERVIEW ("auto-start fiable au SessionStart", "plusieurs attributions doctrinales corrigées via diagnostic empirique"). OVERVIEW destiné Boris = aucun chiffre précis non vérifié.

**Dette tracée** :
- Push GitHub bloqué orga Team (sauvegarde externalisée à arranger)
- Repro formel bug #60237 sur config forge (corrélation forte, test isolé manquant)
- Repo public vs privé à arbitrer avant DM Boris (inclut vault/ ? memory/ ?)


## 2026-05-28 (post-OVERVIEW) — /done 3 capitalisations

**Livrables** :
- Note canonique [[bug-tools-array-first-last-drop]] créée (04-Techniques/claude-code) — bug GitHub #60237 verbatim issue + workaround padding + lien plausible MCP décoratif observé forge. Sort la découverte forensique de working memory vers note canonique réutilisable + référençable
- Feedback `mcp_alias_ambigu_chemin_exact` amendé section "Extension 28 mai 2026 — `update_property` non couvert (6e violation)". `mcp-alias-guard.py` actuel ne matche que `append_note` ; 6 autres outils MCP forge-brain prenant `file=<alias>` restent à découvert (`update_property`, `insert_section`, `read_section`, `update_note`, `delete_note`, `move_note`, `bulk_update_property`). Règle de mesure : tout outil `file=` peut écrire silencieusement sur le mauvais fichier sur stem ambigu. Workaround définitif : `read_note_by_path` + `Read`/`Edit` filesystem direct
- Feedback tier-2 `surface_plutot_que_padder_ou_tronquer` créé — variante longueur de [[feedback_ecart_consigne_chiffree_surfacer]]. Capture la préférence Raphael chantier OVERVIEW (230L vs cible 280-320L assumé sans padding ni troncature)

**Méthode /done appliquée** : extraction brute (4 catégories) → filtre obligatoire → vérification doublons (1 amendement feedback existant, 1 note vault nouvelle, 1 tier-2) → validation [v] item par item → écriture mémoire + vault + CHANGELOG + log.md + cycle git groupé

**Dette structurelle nouvelle tracée** :
- Hook `mcp-alias-guard.py` doit étendre son matcher à 7 outils MCP forge-brain (actuellement `append_note` seul) — `update_property`, `insert_section`, `read_section`, `update_note`, `delete_note`, `move_note`, `bulk_update_property`. Pattern garde existante à élargir, pas un nouveau hook (~30min via hook-creator + tests adverses 3:1).
- **Déclencheur de réactivation** (validation externe Claude #1 28 mai, doctrine "fix ce qui a le plus de levier") : reporté car repo bug #60237 (2-4h, indispensable avant DM Boris) prime. Reactiver SI : (a) repro bug #60237 terminé, OU (b) 3e violation guard ambigu (compteur actuel : 6 violations historiques sur `append_note`/`insert_section`/`update_property`, 7e = déclenchement automatique), OU (c) décision arbitrage repo public/privé prise. Proposition Jarvis 28 mai marquée [i] ignore avec raison tracée.


## 2026-05-28 (soir) — Vérification empirique 3 claims Gemini deep research

**Méthode** : WebFetch direct sur GitHub + howborisusesclaudecode.com + XDA + CHANGELOG raw, en parallèle. Pas d'action structurelle avant rapport.

**Verdicts** :
- **Claim 1 collision nom claude-forge** : CONFIRMÉ. 4 repos GitHub homonymes, dont `sangrokjung/claude-forge` 715⭐ MIT (framework plugin oh-my-zsh-style, 11 agents/36 commands/15 skills). 3 autres marginaux (HatmanStack 13⭐, CristianDArrigo 3⭐, martimramos 1⭐).
- **Claim 2 bug #60237 fixé v1.21.1/v1.22** : FAUX sur versions / VRAI sur fix. Ces versions n'existent pas (CC versionné v2.1.x). Fix réel = **v2.1.147** verbatim CHANGELOG : *"Fixed plugin agents that declare multiple Agent(...) types in tools: frontmatter dropping all but the last entry"*. Local 2.1.153 ⇒ fix déjà déployé chez moi.
- **Claim 3 Boris 5-15 worktrees parallèles** : CONFIRMÉ. Site Boris (*"5 instances of Claude Code simultaneously"*, *"5-10 additional sessions on claude.ai/code"*, *"dozens of Claudes running at all times"*) + XDA (*"He runs 10 to 15 sessions at a single time"*).

**Capitalisations** :
- `feedback_llm_deep_research_version_numbers.md` (tier-1) — pattern transverse : claims numériques précis LLM = à WebFetch avant action
- `project_claude_forge_naming_collision.md` (tier-1) — inventaire 4 repos GitHub homonymes

**Arbitrage Raphael collision nom** : OSEF — usage perso, garde `claude-forge` localement. Dette **conditionnelle** : si publication publique un jour (gist Boris, repo public, blog) → rename obligatoire (options : `forge-jarvis`, `claude-jarvis-forge`, `neoteem-forge`, `forge-perso`). Pas avant.

**Dette priorité haute tracée pour OVERVIEW.md** (NE PAS modifier maintenant — restructuration cohérente attendra retour Gemini deep research #2 sur positionnement état de l'art mondial) :
- Retirer claim "diagnostic bug #60237 = cause-racine MCP décoratif" du §8 : fix natif Anthropic v2.1.147, obsolète. Garder éventuellement comme anecdote forensique mais sans positionnement "découverte".
- Reformuler Axe 1 (actuel = "diagnostic bug #60237") en **"pattern brief-then-direct + hook enforcement défensif"** — axe canonique réutilisable indépendant du bug spécifique.
- Arbitrage collision nom = OSEF maintenant, voir condition publication ci-dessus.

**Méta-apprentissage validation externe** : Gemini deep research fiable sur faits qualitatifs (collision existe, Boris fait des worktrees) mais hallucine systématiquement les chiffres précis (versions, étoiles, dates). WebFetch source primaire reste obligatoire avant relais.
