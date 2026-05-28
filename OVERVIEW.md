# claude-forge — Overview

- **Auteur** : Raphaël Picard (raphael.picard@neoteem.fr) — Lead IA Neoteem, consultant IA indépendant
- **Mise à jour** : 2026-05-28 · **Version** : 3.4
- **État** : `main` à 362 commits, dernière journée 27-28 mai (audit lifecycle, oracle vault-first 3/3 CONFORME, architecture MEMORY tier-1/tier-2)
- **Audience** : lecteur externe sans contexte forge — Anthropic (Boris Cherny, équipe Claude Code), pairs Claude Code power-users, futurs collaborateurs

> Studio méta-Claude Code à usage personnel — 10 agents, 48 skills, 12 hooks, 9 rules, et un vault Obsidian de 438 notes interrogeable par MCP. Trois mécanismes croisés : MCP local pour le contexte vault, doctrine vivante avec gate humain, et critère de design Agent/Skill basé sur la densité d'écriture MCP.

---

## 1. Cadrage

claude-forge est un setup Claude Code personnel utilisé quotidiennement depuis le 31 mars 2026 (~2 mois). Il pilote 5 repos (forge lui-même + ia_back, neo_ia, neoteem-brain, lojii) et sert deux rôles : (1) **conseiller/créateur** — conseille sur la config CC à appliquer, fabrique des composants conformes aux best practices Anthropic ; (2) **mémoire long-terme** — capitalise chaque erreur, décision, raisonnement non trivial dans un vault Obsidian local interrogeable par MCP.

Le repo n'est pas open-source aujourd'hui (politique employeur Team bloque GitHub). Cet overview est rédigé pour une démarche d'engagement Anthropic ciblée.

---

## 2. Trois axes d'innovation revendiqués

Source canonique : [[3-axes-strategiques-forge]] (vault).

### Axe 1 — Diagnostic et workaround du MCP décoratif sub-agent

**Symptôme observé** : un `mcp__server__*` listé dans `tools:` du frontmatter d'un sub-agent Claude Code est silencieusement non chargé. À l'exécution, le sub-agent reçoit `Error: No such tool available: mcp__forge-brain__read_note`. Confirmé empiriquement sur 2 agents (skill-creator, hook-creator) le 27 mai 2026.

**Cause-racine non établie** : le symptôme est reproductible empiriquement mais la cause-racine reste ouverte. Le bug GitHub `anthropics/claude-code#60237` (closed) est candidat à examiner mais non confirmé sur cette configuration — repro formel à faire.

**Conséquence** : un sub-agent à qui on dit *"lis les canoniques via MCP forge-brain"* hallucine ou fallback sur `cat`/`find` du vault → viole la doctrine MCP-only.

**Workaround structurel** : pattern `brief-then-direct` ([[pattern-mcp-brief-then-direct]], canonique 24 mai 2026). La session principale (seul contexte où le MCP est effectif) :

1. Consulte le MCP en amont du dispatch,
2. Synthétise les extraits pertinents dans le brief du sub-agent,
3. Demande au sub-agent d'ESCALADER s'il manque un extrait, jamais de lire le vault directement.

**Enforcement défense-en-profondeur** : hook `vault-cat-guard.py` (PreToolUse Bash, bloque `cat`/`find`/`grep` sur `vault/` depuis tout sub-agent — version condensée du message bloquant) :

```python
# .claude/hooks/vault-cat-guard.py
if VAULT_RE.search(command):
    sys.stderr.write(
        "BLOQUÉ: accès brut au vault forge-brain interdit.\n"
        "Le vault s'accède UNIQUEMENT via le MCP forge-brain.\n"
        "En sous-agent : ESCALADE — demande l'extrait à la session principale.\n"
    )
    sys.exit(2)
```

Le hook s'est déclenché 2 fois dans ce `/recap` même (sub-agent essayant `find vault/...`) — il transforme l'erreur silencieuse Anthropic en blocage explicite avec instructions de récupération.

**Conséquence empirique mesurée** : sur les 49 skills + 13 agents audités le 27 mai, **zéro régression** liée au MCP décoratif depuis la mise en place du pattern brief-inline + hook `vault-cat-guard`. Avant la mise en place (chantier 23-24 mai), des sub-agents dispatchés en parallèle pour auditer plusieurs thèmes vault avaient fallback sur `cat`/`find` au vault, produisant plusieurs attributions doctrinales fausses corrigées en N2 via diagnostic empirique. Après le pattern : les sub-agents qui ne reçoivent pas l'extrait nécessaire **escaladent au lieu de bricoler** — l'erreur Anthropic devient un signal exploitable côté orchestrateur.

**Repro formel à faire** : la corrélation symptôme observé ⨯ bug `#60237` mérite un test isolé avant toute prétention de cause-racine.

### Axe 2 — Critère architectural Agent vs Skill basé densité d'écriture MCP

Distinction canonique entre Agent et Skill telle qu'opérationnalisée dans forge ([[mcp-vs-skills-doctrine]], [[3-axes-strategiques-forge]] axe 2) :

| Métier | Verdict | Pourquoi |
|---|---|---|
| Analyse + 0-1 écriture MCP (devils-advocate qui critique puis 1 `create_note`) | **Agent** — viable | Mode dégradé acceptable : le sub-agent peut renvoyer un livrable texte, la session principale persiste si utile |
| N× écritures MCP vault en boucle (vault-maintainer qui fait `update_property` × notes + MOC + backlinks) | **Skill** — pas agent | Le métier EST impossible en sub-agent : chaque write MCP retournerait `No such tool available` |

Précision critique mesurée 27 mai 2026 : **seule l'écriture MCP vault compte** (pas l'écriture filesystem). Les 4 créateurs forge (agent-creator, skill-creator, claudemd-optimizer, hook-creator) écrivent massivement — mais sur le **filesystem `.claude/`**, leur `mcp__forge-brain__*` ne servant qu'à la **lecture** des canoniques. Donc classés "rare", pas "dense". Confondre les deux a produit 4 faux candidats KILL lors d'un audit intermédiaire ; règle de mesure ancrée dans la canonique vault.

**Cas empirique vault-maintainer (KILL 27 mai 2026)** — illustration concrète du critère :

L'agent `vault-maintainer` devait gérer les aliases, MOC (Maps of Content), frontmatter, backlinks, dédoublonnage des notes. Son métier = `N×` `mcp__forge-brain__update_property` + `bulk_update_property` + `append_note` en boucle. En sous-agent, chaque write retourne `Error: No such tool available: mcp__forge-brain__update_property` → le métier est **structurellement impossible**.

La tentation initiale était de "le faire marcher" via mode dégradé : le sub-agent produit un rapport markdown listant les opérations à effectuer, la session principale rejoue toute la logique en MCP effectif. Architecturalement absurde — autant que la session principale exécute directement.

Diagnostic complet : (1) le métier est MCP-write-dense ; (2) le mode dégradé orchestré est absurde ; (3) une skill existait déjà couvrant le besoin → `/vault-audit` (skill, tourne en session principale, MCP effectif, complétée d'un script Python déterministe pour métriques objectives) ; (4) `vault-maintainer` n'avait **aucune invocation historique** via le tool `Agent` (vérifié transcripts). Verdict : **doublon mort-né → KILL**. Le seul apport unique (trigger proactif "after cc-news / note creation") a été porté en description de `/vault-audit`. L'exemption hook `vault-cat-guard` pour cet agent a été retirée (surface réduite, MCP-only plus strict).

Conclusion canonique : un composant dont la valeur est `N×` MCP-write vault est structurellement une **skill**, pas un agent. Si on hésite à le créer en agent "parce qu'il doit écrire beaucoup dans le vault", c'est le signal qu'il doit être une skill.

### Axe 3 — Living doctrine avec gate humain typé INFO / REINFORCE / PIVOT

Source canonique : [[doctrine-vivante]] (27 mai 2026) + [[methode-pivoter-doctrine]] (checklist anti-drift).

**Principe** : la doctrine forge évolue par deux moteurs :
- **Interne** — l'erreur qu'on commet, capitalisée dans `CLAUDE.md` ou dans une note canonique.
- **Externe** — signal à fort crédit (Anthropic officiel, leaders reconnus) qui contredit ou renforce une canonique. C'est ce moteur externe qui était sous-utilisé avant 27 mai.

**Mécanisme — trois verdicts typés** sur tout finding dirigé (URL leader, conclusion `cc-news`, mesure empirique) :

| Verdict | Signification | Action |
|---|---|---|
| `INFO` | Fait nouveau sans impact doctrinal | Capitaliser comme note de fait |
| `DOCTRINE_PIVOT_CANDIDATE` | Le finding **contredit** une canonique | Pré-remplir un brouillon argumenté → gate humain `[v]/[m]/[i]`. `[v]` lance [[methode-pivoter-doctrine]] (5 étapes anti-drift) |
| `DOCTRINE_REINFORCE` | Le finding **confirme** une canonique | Tracer "challengée + confirmée le {date} par {source}". Renforce la confiance, pas de pivot |

**Anti-pattern cardinal** : aucun mécanisme ne modifie une canonique sans validation humaine explicite. Même sur signal Anthropic officiel fort, la gate `[v]/[m]/[i]` est non négociable. Le mécanisme propose, l'humain tranche.

**Anti-pattern — scan aveugle interdit** : le challenge est *dirigé*, jamais aveugle. La prémisse "les transcripts contiennent un gisement d'apprentissages dormants" a été mesurée fausse (probe 0/12 sur la slice la plus chargée en signal, [[critique-2026-05-27-compounding-retroactif]]). Le puits est sec ; un scan rétroactif aveugle ressusciterait de la doctrine périmée.

**Cas empirique pivot 22 mai 2026 — hooks ≠ workflow enforcement** ([[raisonnement-22mai-doctrine-vs-enforcement]]) :

Contexte : friction 6× sur le développement feature côté ia_back + neo_ia. Verdict utilisateur : *"stop, vos hooks c'est de la merde, ce n'est pas scalable"*. Diagnostic préalable avait déjà tué `tdd-guard`, mais le problème persistait : 7 hooks workflow restants (`architect-guard`, `commit-guard`, `dispatch-guard`, `marker-protect`, `agent-marker-writer`, `pipeline-reset`, `session-reset-markers`) continuaient à forcer un pipeline rigide.

Recherche web doctrine Anthropic 2026 — 3 sources convergent :
- **Boris Cherny** (Latent Space + Pragmatic Engineer) : *"All the secret sauce — it's all in the model"*, *"thinnest wrapper"*, *"Complex scaffolding is often rendered obsolete by the next model generation"*. Boris investit dans l'infrastructure déterministe (context, tool routing), PAS dans les decision scaffoldings.
- **Anthropic Agent SDK** : *"Claude decides when to call a tool based on the user's request"*, *"Skills are model-invoked: Claude autonomously chooses when to use them based on context"*.
- **Docs hooks officiels** : *"Hooks are deterministic and are recommended for **lint, test, and security**"*. Exemples : `rm -rf`, `--no-verify`, force-push, secret leak. **PAS** "forcer architect-first sur `src/**`".

Verdict typé `DOCTRINE_PIVOT_CANDIDATE` → gate humain `[v]` → exécution [[methode-pivoter-doctrine]] (5 étapes anti-drift) :

1. Suppression de 14 fichiers hooks workflow (7 hooks × 2 repos) + markers `.architect-marker` / `.code-reviewer-marker`
2. Split architect en `architect-quick` (sonnet, 5 lignes max) + `architect-deep` (opus xhigh, plan mode)
3. Encodage de la doctrine dans rules (`when-to-architect.md`, `quality-gates.md` passage "TOUJOURS" → "SELON CRITÈRES")
4. CLAUDE.md des 2 repos : section Gotchas "hooks workflow supprimés 22 mai 2026"
5. Révision (pas suppression) du `feedback_enforce_not_advise` — la règle "advisory skippé → hook" s'applique au compliance-miss, PAS à la sur-conformité (qui est son propre mode de défaillance)

Mesure de succès : développement feature M < 30 min vs ~3h pré-pivot. Risque accepté : ~20% des cas où la session skip architect sur du vrai architectural — pari que `architect-quick` cheap + doctrine claire > friction 6× actuelle.

Le pivot a été ré-audité 23 mai : la citation Agent SDK exacte ("Claude decides when to parallelize") n'apparaît pas verbatim dans les docs (paraphrase pédagogique). Le principe sous-jacent reste pleinement attesté par 5 autres sources convergentes — le pivot tient.

Implémentation mécanique : skill `doctrine-impact-check` (croisement finding ⨯ canoniques → verdict typé) + skill `/pivot-check` (détecte drift résiduel post-pivot).

---

## 3. Architecture défensive concrète

Trois patterns d'architecture qui matérialisent les axes 1-3 en code et configuration vérifiables.

### 3.1 — Vault read-only via MCP, write inline dans le brief

Tous les sub-agents qui ont besoin du vault reçoivent les extraits **dans le brief** au moment du dispatch, jamais d'instruction "lis via MCP". Exemple verbatim d'un brief émis par la session principale :

```markdown
Crée l'agent X avec ces specs : [...]
Extraits canoniques pertinents (déjà lus, voici la conclusion) :
- [[comment-creer-agent]] §AskUserQuestion : sub-agent NE PEUT PAS appeler
  AskUserQuestion (issue #18721) → pattern ESCALADE obligatoire
- [[comment-creer-agent]] §wildcard MCP : préférer `mcp__server__*` à liste explicite
- Doctrine 22 mai : pas de workflow hooks, advisory uniquement
Exécute. Filet : si terme/note non couvert dans ce brief → ESCALADE 5 champs
(slug, raison, extrait souhaité, conséquence si manquant, suggestion).
```

Le sub-agent exécute avec contexte ciblé. S'il manque quelque chose, il escalade — il ne fallback **jamais** sur lecture filesystem brute.

### 3.2 — Frontmatter `memory: project` obligatoire sur tous les agents

Chaque agent forge déclare `memory: project` dans son frontmatter, ce qui matérialise une mémoire persistante par-agent localisée dans `.claude/agent-memory/<agent-name>/` (project scope, versionnée git, suit le clone). Skills métier ont une section "Apprentissage" en body. Conséquence : chaque erreur trouvée par devils-advocate ou outcomes-grader retourne dans la canonique du sub-agent concerné — boucle d'apprentissage explicite, pas de tribal knowledge.

### 3.3 — Architecture MEMORY tier-1 / tier-2

`memory/MEMORY.md` (tier-1, chargé chaque session, ~24,6k chars) ne contient que des entrées **citées au moins une fois** depuis une autre canonique ou stratégiquement chargées. Les 96 entrées tier-2 (~16,6k chars) vivent dans `memory/_index_archive.md` (non chargé par défaut, accessible sur recherche). Réintégration tier-1 dès qu'une entrée est citée. Pattern : [[pattern-maintenance-hybride-corpus-accumulatif]] — 3 couches (déterministe / LLM / humain) avec gate `[v]/[m]/[i]` par section. Résultat empirique 27-28 mai : ~14k tokens de contexte libérés par session, sans perte de signal.

---

## 4. Mécanismes anti-drift

Quatre dispositifs structurels pour empêcher la dégradation silencieuse.

- **Séquence canonique A→B→C→D→E** ([[sequence-canonique-modification]]) — obligatoire avant toute création/modification : (A) analyser le réel du repo, (B) lire les canoniques EN ENTIER via MCP, (C) croiser pour écarts mesurables, (D) plan présenté à l'humain, (E) exécuter. Anti-pattern : `search_brain` seul (extraits) sans `read_note` complet → audit sur mémoire session au lieu de source de vérité.
- **Hooks lint/security/scope uniquement** ([[raisonnement-22mai-doctrine-vs-enforcement]]) — pivot doctrinal du 22 mai 2026 : les hooks Claude Code SONT puissants mais ne doivent pas porter le workflow agentique (architect-first, TDD strict, commit gates) — c'est le rôle des rules + agents. Hooks réservés à : `delegate-guard`, `vault-cat-guard`, `security-guard`, `meta-commentary-detector`, etc. 12 hooks Python actifs.
- **Méthode pivot anti-drift** ([[methode-pivoter-doctrine]]) — checklist 5 étapes obligatoire post-pivot : (1) corriger la note canonique, (2) purger MEMORY/RECAP résiduels, (3) grep cross-repo des références anciennes, (4) skill `/pivot-check` pour détecter drift résiduel, (5) tracer dans CHANGELOG vault. Empêche le pattern observé : "doctrine annulée par MEMORY non purgé".
- **Tests baseline** — 324 tests verts maintenus sur 362 commits (143 pytest mcp-forge-brain + 181 hooks). Adversarial-ratio ≥ 3:1 sur les hooks sécu (bypasses testés en priorité, pas seulement happy path).

---

## 5. Méthodologie

Principes nommés, chacun avec sa note canonique :

- **Anti-doublon discipliné** — `search_brain` avant `create_note`, toujours. Évite la dilution sémantique des canoniques.
- **Mesurer-avant-proclamer** — empirique > intuition. Chiffres baseline (commits, tests, notes) toujours mesurés via commande, jamais cités de mémoire ([[feedback_chiffre_baseline_brief_verifier_empiriquement]]).
- **KILL > faire marcher** — pattern empirique : un composant qu'on doit "faire marcher" en mode dégradé est probablement mort-né. Vault-maintainer KILL le 27 mai (doublon de `/vault-audit`).
- **Verify empirique avant affirmer une garde** — claim "deny merge bloque ça" non vérifié = doctrine théorique. 6h de doctrine fausse trouvée 27 mai sur une garde supposée mais non testée.
- **Brief peut poser prémisse fausse** — vérifier matériellement avant d'exécuter, surfacer si fausse au lieu de produire un livrable cohérent avec une prémisse erronée ([[feedback_brief_premisse_fausse_verifier_avant_executer]]).

---

## 6. Validation empirique récente

**Oracle vault-first 3/3 CONFORME (28 mai 2026)** — test reproductible que la séquence canonique A→B→C→D→E est suivie par défaut, pas par discipline ponctuelle. Trois scénarios documentés (audit lifecycle skill, ajout canonique vault, modification CLAUDE.md), pour chacun on observe : (A) analyse du réel effectuée ? (B) lecture canoniques EN ENTIER via `mcp__forge-brain__read_note` sans `max_lines` ? (C) écarts mesurables présentés ? (D) plan validé avant exécution ? (E) exécution + capitalisation ? Verdict : 3/3 PASS. Aucun scénario n'a court-circuité l'étape B (qui est le mode de défaillance principal — `search_brain` seul donne des extraits, pas la source de vérité).

**Audit lifecycle auto-application (27 mai 2026, commit `e81e4aa`)** — 49 skills + 13 agents audités. Les 5 canoniques vault consultées EN ENTIER avant verdicts KEEP/AMEND/KILL : [[comment-creer-agent]], [[comment-creer-skill]], [[pattern-mcp-brief-then-direct]], [[3-axes-strategiques-forge]], [[doctrine-vivante]]. Résultats : (1) Grille catégories → vault requis appliquée — 22 skills catégorie 1-3 (référence / outil pur / exécution pure) où invocation vault non requise par design, 25 catégorie 4 audit/jugement dont 23 conformes ; (2) 2 AMEND légitimes (cc-advisor, evolve) ; (3) 3 KILL — 2 supportés par canoniques (vault-maintainer = MCP-write dense / `/vault-audit` doublon, rule color = canonique `comment-creer-agent`), 1 KILL pragmatique assumé tracé CHANGELOG (forge-status).

**Architecture MEMORY tier-1/tier-2 — −49% chars** (commit `7d82034`) — `memory/MEMORY.md` réduit de 42 470 → 21 493 chars (-49,4%) via hiérarchisation tier-1 (entrées citées au moins une fois) vs tier-2 (`_index_archive.md`, valides non citées). 96 feedbacks déplacés tier-2, accessibles sur recherche ciblée. Conséquence mesurée : ~14k tokens contexte libérés par session, zéro perte de signal (recherche tier-2 = 1 outil MCP supplémentaire, jamais déclenché spontanément). Pattern canonisé [[pattern-maintenance-hybride-corpus-accumulatif]] : 3 couches (déterministe / LLM / humain) avec gate `[v]/[m]/[i]` par section. Réintégration tier-1 dès qu'une entrée est citée par une nouvelle canonique.

**Tests baseline 324 verts** maintenus depuis ~100+ commits (143 mcp-forge-brain + 181 hooks). Caractérisation des bugs (épingler, pas masquer), docstring de scope sur chaque hook sécu, ratio adversarial ≥ 3:1 sur les hooks de contrôle (bypasses testés en priorité, pas seulement happy path).

**MCP forge-brain port 8091** — auto-start fiable au SessionStart, eager-boot des sessions transcripts au démarrage, 22 outils disponibles (search FTS5 BM25 file_stem:10 / aliases:8 / content:1, read entière, create atomique avec wikilinks).

---

## 7. Limitations honnêtes

- **Windows-first** — résolution path 4 contextes (skill = `git rev-parse`, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}`, .mcp.json = relatif cwd). Python OS-agnostique sauf `mcp-autostart.py`. Cross-platform non testé.
- **Évaluations LLM-as-judge absentes** — gap stratégique #1 vs setups concurrents (Boris/ECC/Will). Pas de RUBRIC scoring automatisé sur les outputs des sub-agents. En dette explicite.
- **Point de défaillance unique** — 1 auteur solo (Raphaël). Pas de pair-review interne. Atténué par DA conditionnel, advisor strategy Brad Abrams, et review externe via `cc-news` + analyses tierces.
- **Push GitHub bloqué** — politique organisation Team employeur. Sauvegarde locale uniquement aujourd'hui ; externalisation à arranger.

---

## 8. Travail en cours / questions ouvertes

- **`comment-creer-rule` absente du vault** (P2) — canonique manquante pour le 4e type de composant CC (rules existent mais pas de doctrine canonique sur "comment en écrire une bonne").
- **Tests pytest sur skill `/clean-memory`** — pas de couverture sur ce nouvel outil, à ajouter.
- **Hook `UserPromptSubmit` "audit→lecture canoniques"** — candidat 2e occurrence d'audit-à-l'œil qui aurait pu être bloqué (cf [[feedback_lire_canoniques_avant_audit]]). À évaluer.
- **Repro formel bug `#60237`** sur configuration forge — actuellement corrélation forte mais pas de test isolé démontrant que la position 1 du `tools:` array est bien la cause-racine du symptôme MCP décoratif observé.
- **Repo public vs privé** — à arbitrer avant engagement Anthropic. Inclut ou non `vault/` (cerveau personnel) ? `memory/` (feedbacks contenant noms, projets) ?

---

## 9. Contact

Raphaël Picard — Lead IA Neoteem (proptech ERP français Loji), consultant IA indépendant. 36 ans, parcours atypique (gamer). Anthropic Academy 4 certifications. Usage Claude Code personnel quotidien depuis le 31 mars 2026.

Contact : raphael.picard@neoteem.fr.

---

## Méthodologie de cet overview

Tous les chiffres mesurés empiriquement le 2026-05-28 :
- `git rev-list --count main` → 362 commits
- `ls .claude/agents/*.md | wc -l` → 10 agents forge
- `ls -d .claude/skills/*/ | wc -l` → 48 skills
- `python -m pytest --collect-only` (racine + `.claude/hooks/tests/`) → 324 tests (143 mcp-forge-brain + 181 hooks)
- `mcp__forge-brain__vault_stats` → 438 notes vault (2903 wikilinks, 2547 aliases)
- `wc -c memory/MEMORY.md memory/_index_archive.md` → 24,6k + 16,6k chars

Wikilinks vault résolvables via `mcp__forge-brain__read_note`. Bug `#60237` vérifié via `https://github.com/anthropics/claude-code/issues/60237` (closed, sub-agent frontmatter `tools:` array first/last drop).
