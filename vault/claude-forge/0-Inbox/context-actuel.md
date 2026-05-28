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


## 2026-05-28 (nuit) — Phase 1 optimisations post-validation externe 4 sources + OVERVIEW chirurgical

**Phase 1 livrée — commit `f4dd26a` (ff-merge main, branche supprimée, pas de push)** :

- **L1 mesure I/O outils (MVP minimal abonnement Claude Code)** :
  - Hook PostToolUse `metrics-tracker.py` (~55L) fail-open, log JSONL `.claude/_metrics/YYYY-MM-DD.jsonl`
  - Skills `/io-daily` (91L) + `/io-week` (94L) — top outils freq/tokens, tendances 7j, bottlenecks >20%
  - 5 tests pytest (2 nominaux + 3 adverses) — 5/5 verts. Baseline 186 hooks verts maintenue
  - `settings.json` appliqué manuellement par Raphael (classifier hard-block)
  - Décisions : drop attribution skill/agent (non triviale), drop calcul tokens API (impossible depuis hook — proxy I/O seulement)

- **L2 sources PIVOT vault doctrine-vivante** : arXiv 2605.11225 (Zhang/Popa/Xu/Song/Dimitriadis, mai 2026) vérifié empirique via WebFetch. Section "Sources d'inspiration" ajoutée : PIVOT (PLAN/INSPECT/EVOLVE/VERIFY) + ADR (Nygard 2011) + 4 adaptations forge-spécifiques tracées

- **L3 SKIP search_brain snippets** : vérifié empirique que `context: true` par défaut renvoie déjà highlights `>>> term <<<`. ~1h économisée

- **L4 rule read-section-preference** : `.claude/rules/read-section-preference.md` créée (préférence ciblée vs entière, pas dogme). cc-advisor ligne 22 amendée avec wikilink

**Méthode validée empiriquement** : advisor AVANT proposition a détecté 2 blockers conceptuels (L1 mesure tokens ≠ I/O outils, L2 arXiv non vérifié). Pattern existant `feedback_advisor_da_mandatory` + `feedback_arxiv_id_yymm_format` + `feedback_brief_premisse_fausse_verifier_avant_executer` ont tenu. Pas de nouveau feedback à créer, patterns existants ont fonctionné.

**OVERVIEW.md — suppression chirurgicale 5 claims faux (non-commité, ta main)** :
- "Intégration cohérente non documentée publiquement ailleurs" (TL;DR) → supprimé
- Paragraphe "top 1-3% mondial sourcé LLM" (§1) → supprimé
- "Cause-racine plausible #60237 / La corrélation est forte" → dégradé "Cause-racine non établie, candidat à examiner, repro à faire"
- "Position vs autres setups / Boris destinataire naturel" → dégradé "Repro formel à faire avant prétention cause-racine"
- "L'audit s'est auto-appliqué... test du test du test" → supprimé
- "vision expert IA reconnu" (§9) → supprimé
- Diff propre 5 insertions / 7 deletions sur 6 emplacements. Bug #60237 conservé comme hypothèse ouverte (sinon axe 1 perd structure)

**Capitalisations /done (2 blocs tier-2 reference)** :
- [[reference_posttooluse_hook_limitations]] — Hook PostToolUse voit I/O outils, PAS tokens API ni attribution skill/agent
- [[reference_search_brain_context_default]] — search_brain renvoie déjà context+highlights par défaut

**Prochaines étapes** :
- Commit OVERVIEW.md séparé (suppression chirurgicale 5 claims) si Raphael valide
- Mesure `/context` post-Phase 1 en nouvelle session (les vrais gains tokens viendront des décisions futures éclairées par les métriques `/io-daily` `/io-week`, pas immédiatement)
- Activer hook metrics-tracker en lançant la prochaine session (après application manuelle settings.json déjà faite)
- Décider extension `mcp-alias-guard.py` aux 7 outils MCP forge-brain restants (dette tracée 28 mai matin, conditionnel post-repro #60237)


## 2026-05-28 (suite) — AMEND CLAUDE.md L14 doctrine read_note session principale

**Vérification empirique** (3 read_note EN ENTIER : pattern-mcp-brief-then-direct + erreur-vault-jamais-consulte-session-principale + CLAUDE.md complet) avant action :

- Pattern `search_brain → read_note EN ENTIER avant audit/jugement` était canonisé dans `pattern-mcp-brief-then-direct` AJOUT 28 mai (grille 4 catégories) mais **CLAUDE.md L14 ne couvrait que "proposition / recherche web / refonte"** — pas "audit / jugement / recommandation". Sous-gap doctrinal session principale confirmé.
- Note `erreur-vault-jamais-consulte-session-principale` (27 mai) explicite mais en Knowledge/erreurs/, pas brief permanent.

**AMEND CLAUDE.md L14 livré** via claudemd-optimizer (delegate-guard hook a bloqué l'édit direct → conformité doctrine `delegate-to-specialists`) :
- Scope élargi : + "audit / jugement / recommandation"
- Pattern explicite : "`search_brain` pour trouver, puis **`read_note` EN ENTIER** des canoniques pertinentes"
- Anti-pattern nommé : "search_brain extraits ~10 lignes = INSUFFISANT pour audit/jugement"
- Wikilink : `[[pattern-mcp-brief-then-direct]]` grille 4 catégories
- Diff minimal 1 puce raffinée, bloc Critiques (<L25) intact, 8 puces maintenues

**Sweep empirique Option A (drift cc-advisor + evolve + tous composants .claude depuis 28 mai)** :
- `cc-advisor/SKILL.md` : 3 marqueurs (read_note L16 + read_section L22 + wikilink [[pattern-mcp-brief-then-direct]] L24) — CONFORME, AMEND 28 mai en place
- `evolve/SKILL.md` : 2 marqueurs (read_note EN ENTIER L21 + wikilink L30) — CONFORME, AMEND 28 mai en place
- `git log --since=2026-05-28 -- .claude/skills .claude/agents` : **vide** → zéro touche `.claude/` depuis audit lifecycle 28 mai → zéro drift possible
- Le dernier commit touchant `.claude/` est `e81e4aa` (audit lifecycle 28 mai) qui contient déjà les AMEND

**Apprentissages capitalisés** :
- Feedback tier-1 `brief-prescrit-travail-deja-fait-veille` créé (memory/) — distinct de `brief-premisse-fausse-verifier-avant-executer` (obsolescence ≠ fausseté factuelle). Pattern : brief auto-mode peut prescrire création/audit déjà fait 24-72h avant → search_brain + AJOUT récents canoniques AVANT Phase 1
- Sous-gap session principale comblé : la grille 4 catégories de `pattern-mcp-brief-then-direct` audite skills/agents via 3 marqueurs body. La session principale n'a pas de body — son brief permanent est CLAUDE.md → l'AMEND L14 est l'équivalent fonctionnel de la grille appliquée à elle-même

**Cycle git proposé (NON commité, attente validation Raphael)** :
- `chore(claudemd): élargir doctrine read_note canoniques EN ENTIER avant audit/jugement (session principale)`
- `chore(memory): feedback brief-prescrit-travail-deja-fait-veille tier-1`
- `docs(vault): context-actuel + CHANGELOG + log post AMEND L14`


## 2026-05-28 (suite 2) — AMEND L14 v2 : nuance "si pas déjà en contexte"

Raphael surface tension implicite entre CLAUDE.md L14 (read_note EN ENTIER) et L19 (tokens/contexte = ressource ultra-précieuse).

**Diff v2** : ajout de **`si pas déjà en contexte`** ligne 14 entre "canoniques pertinentes" et "(search_brain extraits...". 5 mots, garde-fou anti-double-pay tokens, pas dérogation à la doctrine.

**Capitalisation** :
- Feedback tier-1 `read-note-conditionnel-si-pas-deja-contexte` créé + indexé MEMORY.md
- Logique : canonique déjà `read_note` dans transcript courant = citer + wikilink ; canonique citée via search_brain (extraits 10L) = read_note EN ENTIER obligatoire ; canonique jamais touchée = read_note EN ENTIER

**Cohérence doctrinale** : la nuance répond à une question implicite que L14 v1 laissait ouverte. Sans cette nuance, l'AMEND L14 v1 risquait de muter en "re-lire systématiquement par sécurité" — re-violation L19. Avec la nuance, les deux règles sont compatibles structurellement.

**Cycle git proposé mis à jour** :
1. `chore(claudemd): élargir doctrine read_note canoniques EN ENTIER (si pas déjà en contexte) avant audit/jugement (session principale)` — CLAUDE.md L14 v2
2. `chore(memory): 2 feedbacks tier-1 (brief-prescrit-travail-deja-fait + read-note-conditionnel-si-pas-deja-contexte)` — memory/ + MEMORY.md
3. `docs(vault): context-actuel + CHANGELOG + log post AMEND L14 v2`


## 2026-05-28 (nuit suite 3) — Doctrine architecture cognitive 3-acteurs + hook saturation + pilote 29 fichiers

**Phase A — AMEND vault canonique** : `pattern-maintenance-hybride-corpus-accumulatif` (section nouvelle "Architecture cognitive — trois acteurs") :
- Triade `MEMORY.md` ≤50 / vault canoniques pas plafond / `memory/*.md` ≤100
- Workflow décision 4 étapes (search_brain → POINTEUR si canonique existe → feedback si cas empirique précis → promouvoir vault si pattern récurrent 2-3 incidents)
- Template pointeur 1 ligne + 4 exemples PASS/FAIL + cibles empiriques mesurées
- 2 aliases ajoutés + 2 wikilinks ([[memory-discipline]], [[decision-memoire-dans-le-repo]])

**Phase B — AMEND rule `.claude/rules/memory-discipline.md`** : section "Triade memory/vault/memory-physique (3 acteurs)" — workflow 4 étapes inline + anti-patterns + pointeur vers pattern vault pour détails.

**Phase C — Hook + amend /done** :
- `.claude/hooks/memory-saturation-watcher.py` (~85L, fail-open, WARNING 80 / CRITICAL 100, exclut MEMORY.md/_index_archive.md)
- 5 tests pytest verts (2 nominaux + 3 adverses) — baseline hooks 191 maintenue (était 186, +5 saturation)
- `settings.json` ajout SessionStart (3e hook)
- `/done` SKILL.md amendé via skill-creator (delegate-guard hook a bloqué Edit direct = conformité) — callout doctrinal 3-acteurs + workflow 4 étapes ~9L inséré entre `## Etape 2` et `### 2a`

**Phase D' — Application pilote 29 fichiers (3 PURGE + 8 POINTEURS + 18 KEEP)** :
- Backup défensif `.claude/_backups/memory-pilote-pre-purge-2026-05-28.tar.gz` (573 KB)
- **3 PURGE COMPLETS** : `feedback_audit_coherence_pattern`, `feedback_audit_repo_method`, `feedback_auditor_false_positives` (doublons confirmés `audit-claude-folder-pattern`)
- **8 POINTEURS 1 ligne (~11-20L body)** : claim_security, gotchas_line_numbers, x_articles_inaccessibles, advisor_da_mandatory, da_bash_write, da_failure_options, audit_qualite_design_transverse, repo_audit_workflow
- Index `MEMORY.md` et `_index_archive.md` synchronisés (3 entrées retirées)

**Compte empirique post-pilote** : 274 → **271 fichiers** memory/ (-3), MEMORY.md 161 → **158** tier-1 (-2 -1 absorption faux positif _index_archive), _index_archive 103 → **102** tier-2 (-1). Hook live confirme CRITICAL: 271 fichiers.

**Brief-prémisse-fausse appliqué** :
- Brief annonçait baseline tests 324 → mesure empirique 334 (191 hooks + 143 mcp), écart +10 = chiffre baseline brief = hypothèse 27 mai obsolète. Aucune régression test cette session.
- `pattern-maintenance-hybride-corpus-accumulatif` couvrait déjà 60% de la doctrine 3-acteurs → AMEND chirurgical retenu vs création doublon (cohérent feedback tier-1 single-source-truth)

**Dette curative explicite tracée** :
- 242 fichiers memory/ restants à auditer (271 - 29 pilote)
- 18 KEEP du pilote re-classification possible promotion vault si pattern récurrent émerge
- Déclencheur réactivation : (a) hook CRITICAL chaque session OU (b) `/clean-memory` périodique OU (c) plage tranquille weekend
- Restant à >100 fichiers, hook continuera CRITICAL — c'est volontaire (visibilité dette continue)

**Cycle git proposé** (3 commits, **NON exécuté**, validation Raphael obligatoire) :
1. `feat(doctrine): AMEND pattern-maintenance-hybride architecture cognitive 3-acteurs + AMEND rule memory-discipline triade` (+ hook memory-saturation-watcher + 5 tests + amend /done workflow)
2. `chore(memory): pilote nettoyage 29 fichiers (3 PURGE + 8 POINTEURS + 18 KEEP). Doublons vault ↔ memory 38% mesuré empiriquement`
3. `docs(vault): capitalisation feedback ratio empirique + context-actuel + CHANGELOG + log. Dette curative 242 fichiers tracée`


---

## Audit MCP forge-brain vs MCP brain — 28 mai 2026 (post audit lifecycle)

### Verdict empirique
forge-brain mieux conçu tokens/Karpathy serveur : 6 gains, 1 perte (inapplicable forge), 7 égalités.

### Livraisons
- Note canonique vault : [[comparaison-mcp-forge-brain-vs-mcp-brain-28mai2026]] (14 critères + extraits code preuve)
- AMEND `.claude/skills/forge-brain/SKILL.md` (197L → 292L) :
  - A1 — Pattern Karpathy opérationnel 3 temps SEARCH/SELECT/READ + N=3 + 4 modes + anti-patterns ❌/✅
  - A2 — Priorisation tools "search_brain = dernier recours" (find_by_property > read_section > read_note > search_brain)
  - A3 — Pagination autoguidée 500L par passes (header serveur `[suite : offset=N]`)

### Recommandations P3 brain ← forge (à transmettre Raphaël pour décision séparée — repo neoteem-brain global, hors plugin)

Optimisations possibles côté `mcp-obsidian-brain` :

- **P3a — Pagination autoguidée serveur** : `brain.py` retourne tout d'un coup, pas de pagination. Sur notes > 5000L = exploser contexte ou tronquer. Ajouter mécanisme `offset/limit_chars` avec header `[suite : offset=N]` (porter de `forge-brain/brain.py:210-218`). Effort estimé 1-2h port + tests.

- **P3b — read_section ciblée** : brain n'a pas. Gain documenté 30x sur grosses notes (62k → 2k chars). Ajouter outil `read_section(file, heading, include_subsections)` (porter `forge-brain/brain.py:550-594`). Effort estimé 2-3h port + tests.

- **P3c — usage_log + usage_stats** : brain pas d'observabilité. Sans données, impossible savoir quels outils valent garder/retirer. Ajouter `usage_log.log_call()` décorateur + `usage_stats(days)` (porter `forge-brain/brain.py:867+1097` + `usage_log.py`). Effort estimé 1-2h port + tests.

- **P3d — read_note_resolved (embeds inlined)** : brain n'a pas. Pour MOC = doit faire N appels au lieu de 1. Ajouter résolution récursive `![[X#H]]` avec cycle detection et markers `<!-- EMBED -->` (porter `forge-brain/brain.py:596-637`). Effort estimé 2h port + tests.

À transmettre Raphaël pour décision séparée propagation vers neoteem-brain repo global.

### Statut
- Phase A (note canonique) — OK
- Phase B/C/D (AMEND skill A1+A2+A3) — OK
- Phase E (P3 tracés) — OK
- Phase F (CHANGELOG + log) — en cours
- Phase G (2 commits groupés) — STOP attente validation Raphaël


## 2026-05-28 (session suivante) — Commentaire ticket comparatif devis + 3 notes archi Neoteem

**Contexte** : Rédaction d'un commentaire Jira sur le ticket "Comparatif devis" (étapes 1-5 + actions post-comparaison, spec très chargée). 14 itérations V1→V14 pour caler l'archi avant que les sections du commentaire soient justes.

**Livrables vault (3 nouvelles notes dans `1-Projets/Neoteem/`)** :
- [[archi-backs-neoteem]] — Contrats d'exposition front : neo_ia front IA uniquement, ia_back jamais front, métier hors scope des deux (webservices Jérôme)
- [[stockage-fichiers-neoteem]] — Pas de S3 chez Neoteem. Stockage = BDD JSON ou Drive client (via webservices Jérôme). Exception GCS NeoDoc
- [[webservices-jerome]] — 3 webservices métier réutilisables (Correspondance / AG / Drive). Checklist intégration. À solliciter pour toute feature touchant ces actions

**Livrable memory** :
- `feedback_archi_clarifier_avant_livrable_cross_stack` (tier-2, ajouté `_index_archive.md` → 98 entrées) — clarifier archi en V1 via AskUserQuestion sur livrables cross-stack, pas après 6 itérations correctives

**Apprentissage méthodologique** : pour tout livrable cross-stack Neoteem (commentaire Jira, /spec, BRIEF, doc archi), première action = clarifier archi via AskUserQuestion. Coût observé d'une archi non clarifiée en V1 = ×4 en itérations.

**Décisions PO encore à arbitrer (à reprendre dans ticket)** :
- Maquette écran de saisie côté front (manquante)
- Persistance résultat : 3 options (BDD JSON / Drive PDF / combo)
- Pré-remplissage automatique champs déductibles du contexte
- Spec précise webservices Jérôme (URLs, contrats, auth, couverture CA)
- Edge cases : timeout neo_ia, rate limit, PDF illisible, 1 seul devis exploitable

**Statut commentaire Jira** : V14 finale, à copier-coller manuellement par Raphael (pas d'accès Jira depuis session)

**Pas de cycle git** sur cette tranche — vault + memory uniquement, pas de touches .claude/.


## 2026-05-28 (suite 6) — AMEND CLAUDE.md L14 v3 + capitalisation 2e occurrence vault-jamais-consulté

**Déclencheur** : Raphael remonte que la session principale ne consulte pas le vault sur les demandes d'assistance rédactionnelle (rédaction commentaire/ticket/spec). Diagnostic empirique : la session récente du ticket "Comparatif devis" = 14 itérations V1→V14 sans une seule consultation vault. Or des notes pertinentes existaient.

**Cause-racine identifiée** : L14 CLAUDE.md v2 listait 6 catégories ("proposition / recherche web / refonte / audit / jugement / recommandation"). "Aide-moi à écrire X" n'était dans aucune → trou doctrinal de scope, pas violation.

**Fix appliqué (livré)** :
- **AMEND CLAUDE.md L14 v3** (via claudemd-optimizer, vérif empirique post-agent OK) — scope élargi à "toute réponse substantielle à une question Raphael", exemple explicite "rédaction d'un ticket/commentaire/spec/explication", clause "si aucune note pertinente → répondre quand même mais avoir cherché d'abord", 2e anti-pattern daté ajouté (28 mai 14 itérations), wikilink `[[erreur-vault-jamais-consulte-session-principale]]` ajouté.
- **Append note canonique** [[erreur-vault-jamais-consulte-session-principale]] — section "2e occurrence — 28 mai 2026" avec contexte, cause-racine scope, conséquences, fix, pattern transverse, déclencheur réactivation (3e occurrence → Option B hook ou Option C skill).
- **CHANGELOG vault** — entrée "suite 5" complète.

**Trade-off doctrinal arbitré** : Option A (AMEND L14) retenue vs Option B (hook session-health) et Option C (skill vault-reflex auto-trigger). Raison : 2 occurrences en 4 jours ne justifient pas encore un hook (doctrine 22 mai : lint/sécu/scope, pas workflow) ni une nouvelle skill (overhead). AMEND sémantique gratuit suffit. 3e occurrence = déclencheur réévaluation.

**Cycle git proposé** (1 commit groupé) :
- `feat(doctrine): AMEND CLAUDE.md L14 v3 scope ouvert assistance rédactionnelle + amend note canonique vault (2e occurrence skip vault session principale)`

**Apprentissage méta** : la règle de consultation vault doit avoir un scope **ouvert** (toute réponse substantielle) avec clause d'**échappatoire explicite** (si rien → répondre quand même). Sinon le LLM cherche un alibi pour ne pas chercher en classant la demande hors des catégories listées.
