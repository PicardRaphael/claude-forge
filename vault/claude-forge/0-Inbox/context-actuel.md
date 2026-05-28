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
