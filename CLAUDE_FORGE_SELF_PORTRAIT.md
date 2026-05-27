# CLAUDE_FORGE — Self-Portrait

Document d'auto-cartographie exhaustive. Date de génération : 2026-05-27 (régénéré post Mémoire Portable + DA compounding rétroactif + Audit transverse + Investigation veille). État du repo : branche `main`, 302 commits, dernier commit `39735a4` (2026-05-27 13:30).

Remarque méthodologique : les métriques (commits, tests, notes vault, outils MCP) ont été remesurées directement cette session (`git rev-list --count`, `pytest --collect-only`, `vault_stats`, grep des définitions dans `brain.py`). Les numéros de ligne des composants `.claude/` proviennent en partie de lectures par sous-agents recoupées par échantillonnage ; quand une affirmation repose sur une lecture indirecte non revérifiée caractère par caractère, c'est signalé en annexe. Les hooks, `settings.json`, le code MCP et les notes vault citées ont été lus directement.

**Identité (recentrée Phase 4, maintenue)** : claude-forge n'est PAS un agent autonome. C'est un studio de **mémoire et apprentissage parfaits en session synchrone** — Raphael travaille TOUJOURS avec Claude, jamais en le laissant tourner seul. La thèse n'est pas l'automatisation sans surveillance mais le compounding maximal sous contrôle humain : une erreur faite une fois jamais deux, une décision tracée et réutilisée, un pattern capitalisé en doctrine, le tout validé par Raphael avant écriture. C'est un outil PERSONNEL, pas un produit collaboratif ni open source — l'analogie Jarvis/Tony Stark est assumée (`CLAUDE.md` section "Contrat Jarvis"). La comparaison avec un agent autonome (Hermes) est reléguée en annexe B ; elle éclaire le positionnement mais n'est pas centrale au document.

---

## 1. Identité du projet

- **Nom** : claude-forge
- **Version** : 3.3 (déclarée `CLAUDE.md:3` — "permissions totales + doctrine effort calibrée")
- **Auteur** : Raphael Picard (`raphael.picard@neoteem.fr`). 302 commits, un seul auteur réel (284 sous "Raphael Picard", 18 sous "Raphael PICARD" — même personne, casse différente).
- **Licence** : pas de fichier LICENSE. Projet personnel non distribué publiquement.
- **Créé le** : 31 mars 2026 (`CLAUDE.md:3`) ; premier commit git 2026-04-03 (`aab5cd4` "Initial commit: claude-forge - assistant personnel Claude Code").

**Pitch en une phrase**
claude-forge est le méta-outillage Claude Code personnel de Raphael : un ensemble d'agents, skills, hooks, rules et un vault de connaissances qui conseillent, créent, optimisent et capitalisent sur l'usage de Claude Code à travers tous ses projets — au service d'une mémoire et d'un apprentissage parfaits en session synchrone, pas d'un agent qui tourne seul.

**Pitch en un paragraphe**
claude-forge est un projet "studio" qui ne produit pas d'application : il produit de la configuration Claude Code (agents, skills, hooks, CLAUDE.md) pour d'autres projets, et accumule la doctrine d'usage de Claude Code dans un vault Obsidian (`forge-brain`, 430 notes) interrogeable via un serveur MCP maison (22 outils). Sa thèse centrale est le *compounding* : chaque erreur, chaque décision, chaque technique apprise est capitalisée dans le vault ou la mémoire pour ne jamais être réapprise. Il incarne une relation "Tony Stark / Jarvis" où Claude est un partenaire proactif. Techniquement, c'est du Python (hooks + serveur MCP FastMCP/SQLite-FTS5) orchestré par des fichiers Markdown, ciblé Windows, portable cross-machine via le `py` launcher et un mécanisme de mémoire versionnée dans le repo (`@import`).

**Public cible**
- Raphael Picard, en premier lieu — outil personnel (`memory/feedback_forge_is_personal.md` : "Forge = PERSONNEL, généraliste").
- Par extension, toute personne qui utilise Claude Code intensivement sur plusieurs repos et veut industrialiser la création de composants CC + capitaliser sa doctrine.

**Pas le public cible**
- Quelqu'un qui cherche une application métier (claude-forge ne fait rien fonctionnellement, c'est un méta-outil).
- Un débutant Claude Code — la densité doctrinale (10 rules, 47 skills, doctrine datée) suppose une maîtrise préalable.
- Une équipe cherchant un framework partagé clé-en-main : beaucoup de chemins, préférences et noms de repos sont hardcodés au contexte Neoteem/Raphael.

---

## 2. Problème résolu

**Le problème**
Utiliser Claude Code sur 6+ repos (forge, ia_back, neo_ia, neoteem-brain, lojii, bdd) crée trois douleurs récurrentes :
1. Re-créer à la main des agents/skills/hooks non conformes aux best practices (et les refaire après coup).
2. Réapprendre les mêmes leçons (mêmes erreurs de quoting Windows, mêmes anti-patterns d'agents orchestrateurs, mêmes oublis de `memory: project`).
3. Perdre le contexte et la doctrine entre sessions — Claude Code repart de zéro à chaque `/clear`.

**Avant claude-forge**
Création ad-hoc de composants `.claude/` par édition directe, doctrine éparpillée dans la tête de l'utilisateur, et répétition d'erreurs documentées nulle part. `memory/feedback_major_mistakes.md` et la rule `check-before-create.md` ("2026-04-26 : 6 skills + 14 agents édités à la main sans vérification, tous non conformes") attestent de cet état initial.

**Pourquoi les solutions existantes ne suffisaient pas**
- Claude Code seul n'a pas de mémoire persistante structurée au-delà de CLAUDE.md et de l'Auto Memory.
- Les plugins externes (superpowers, plugins Anthropic) sont génériques et ne capitalisent pas la doctrine personnelle.
- La priorité des sources (`CLAUDE.md`) est explicite : Forge Brain > Mémoire > Skills forge > Plugins externes > Web. claude-forge existe précisément pour que la connaissance personnelle prime sur le générique.

**Ce que ça change dans une journée de dev**
- Un besoin flou ("j'ai besoin d'automatiser mes PRs") déclenche `cc-advisor` qui recommande le bon composant.
- "Crée un agent qui X" est délégué à `agent-creator` qui applique automatiquement frontmatter, couleurs, `memory: project`, taille — conformité garantie par construction (hook `delegate-guard.py` bloque l'édition directe).
- Toute erreur en fin de session est capturée par le hook `learning-reminder.py` et capitalisée dans le vault ou la mémoire.
- Le contexte projet se récupère en 10 s via `/recap`.

---

## 3. Vue d'ensemble technique

**Stack**
- **Markdown** : agents, skills, rules, CLAUDE.md, vault (le "code" du studio est essentiellement déclaratif/textuel).
- **Python ≥ 3.11** : 9 hooks (`.claude/hooks/*.py`) + serveur MCP (`mcp-forge-brain/`). Dépendances MCP : `fastmcp>=2.0`, `pyyaml>=6.0` (`mcp-forge-brain/pyproject.toml`).
- **SQLite FTS5** : deux index — vault (`forge-brain.db`) + transcripts de session (table `session_messages` séparée, ajoutée en A1).
- **Batch Windows** : `install.bat`, `scripts/*.bat`, `mcp-forge-brain/start.bat`.
- **Outils CLI externes** (installés par `install.bat`) : Node.js, `defuddle-cli`, `yt-dlp`, `fastmcp`, `pyyaml`, `ffmpeg` (optionnel), `faster-whisper` (optionnel), `deno` (optionnel).
- **MCP** : un seul serveur configuré, `forge-brain` (HTTP local port 8091).
- **Modèles** : `sonnet` (claude-sonnet-4-6) exécution, `opus` (claude-opus-4-7) jugement, `haiku` (claude-haiku-4-5) rapide (`CLAUDE.md` "Règles de génération absolues").

**Architecture globale (schéma textuel)**

```
claude-forge/
├── CLAUDE.md                  Contrat + doctrine + @memory/MEMORY.md (L100). ~200L
├── .mcp.json                  Déclare le serveur MCP forge-brain (HTTP :8091)
├── install.bat                Setup des prérequis CLI (Windows)
├── README.md                  Doc courte (pointe vers ce self-portrait ; chiffres MCP/notes périmés)
│
├── .claude/
│   ├── settings.json          Permissions + câblage des 9 hooks + env (autocompact 50%, Agent Teams)
│   ├── .skill-triggers.json   Map mots-clés → skill (lu par skill-activation.py)
│   ├── agents/                11 agents (.md)
│   ├── skills/                47 skills (dossiers SKILL.md + assets)
│   ├── hooks/                 9 hooks Python + tests/ (5 fichiers de tests)
│   ├── rules/                 10 rules (routing + doctrine, injectées via CLAUDE.md)
│   ├── scripts/               apply-edit.py, news-check.ps1
│   ├── agent-memory/          mémoire par agent (project scope)
│   └── secrets/               cookies x-read (gitignored)
│
├── memory/                    Mémoire versionnée portable (chargée via @import CLAUDE.md)
│   ├── MEMORY.md              Index (~229L) — chargé entier à chaque session
│   ├── feedback_*.md          193 fichiers de feedback
│   └── private/               items confidentiels (gitignored)
│
├── mcp-forge-brain/           Serveur MCP maison (FastMCP + SQLite FTS5)
│   ├── src/                   server.py, database.py, indexer.py, watcher.py, config.py,
│   │                          git_sync.py, usage_log.py, sessions_db.py,
│   │                          sessions_indexer.py, sessions_watcher.py, tools/brain.py (22 outils)
│   ├── tests/                 13 fichiers de tests pytest (143 tests)
│   ├── config.yaml            vault_path, port, poids FTS
│   └── start.py / start.bat   Launcher
│
├── vault/claude-forge/        Le "cerveau" — vault Obsidian, 430 notes
│   (raw/ + wiki layers 00-Hub..07-Prompts + Knowledge + SCHEMA.md/index.md/log.md)
│
├── ia-lead-neoteem/           Plugin Cowork (7 skills Responsable IA)
├── scripts/                   .bat de tâches planifiées (cc-news, forge-review, vault-audit)
├── output/                    Livrables ad-hoc générés pour d'autres repos (gitignored)
└── data/                      Sortie twitter-api-client (gitignored)
```

**Principes de design structurants** (cités du repo)
1. **Compounding error-driven** : "après chaque erreur, ajouter ici ou mémoire ou vault Knowledge" (`CLAUDE.md` Workflow Boris). `Knowledge/erreurs/` (34 notes) est le plus gros sous-dossier de Knowledge.
2. **Doctrine hooks = lint/security/scope, JAMAIS workflow** (pivot du 22 mai 2026). Un hook ne doit pas forcer un workflow agentique (architect-first, TDD strict, gates de commit).
3. **Délégation forcée aux spécialistes** : on ne crée/modifie pas un SKILL.md / agent / CLAUDE.md à la main — `delegate-guard.py` bloque et force le passage par skill-creator / agent-creator / claudemd-optimizer.
4. **MCP pour la donnée, Skills pour le savoir-faire** (`mcp-vs-skills-doctrine`). Le vault n'est accessible QUE par MCP forge-brain, jamais Grep/Read brut.
5. **Effort calibré par type de tâche** : `xhigh` réservé à l'exploration agentique profonde (repo-inspector), `high` partout ailleurs, `max` jamais en frontmatter.
6. **Sonnet exécute, Opus juge** (`memory/feedback_all_opus.md`).
7. **5 lignes Karpathy en ouverture de tout CLAUDE.md** (`memory/feedback_5_lignes_karpathy_ouverture.md`).
8. **Pas de méta-commentaire dans les composants** : la justification (source, attribution d'auteur, historique) vit dans le vault, pas dans le hook/agent/skill. Enforced par `meta-commentary-detector.py`.
9. **Mémoire dans le repo, portable par git** : la mémoire est versionnée dans `<repo>/memory/` et chargée via `@memory/MEMORY.md` dans le CLAUDE.md versionné (`decision-memoire-dans-le-repo`).

**Diagramme de flux — lancement d'une session Claude Code dans claude-forge**

```
1. SessionStart
   ├─ session-reminder.py   → nettoie les markers de session précédente,
   │                          affiche un extrait de <repo>/memory/MEMORY.md (résout via __file__)
   └─ mcp-autostart.py      → vérifie port 8091 ; si mort, lance mcp-forge-brain
                              en process détaché (async)

2. UserPromptSubmit (à chaque message utilisateur)
   ├─ session-health.py     → compteur de tours ; tip /recap (tours 1-2),
   │                          rappel /compact (tous les 20), urgent (tous les 40)
   └─ skill-activation.py   → matche le prompt vs .skill-triggers.json,
                              injecte additionalContext recommandant une skill

3. PreToolUse
   ├─ Bash      → security-guard.py            (bloque rm -rf /, push --force, …)
   ├─ Edit|Write|MultiEdit → delegate-guard.py (bloque édit direct SKILL.md /
   │                          agents/*.md / CLAUDE.md hors agent spécialiste)
   └─ Write|Edit|MultiEdit → meta-commentary-detector.py (bloque méta-commentaires
                              dans les composants forge)

4. PostToolUse (uniquement dans l'agent python-dev)
   └─ py_compile sur chaque fichier Python écrit (hook inline frontmatter)

5. Stop (fin de tour)
   ├─ rundll32 MessageBeep   → bip sonore
   ├─ learning-reminder.py   → 1×/session : "as-tu appris quelque chose ?"
   └─ proactivity-reminder.py→ 1×/session si ≥5 tours : "as-tu fait une proposition Jarvis ?"
```

---

## 4. Build & installation

**Prérequis**
- OS : Windows (cible primaire — hooks `py` launcher, `install.bat`). Le code Python est portable, sauf flags Windows de `mcp-autostart.py`.
- Node.js (pour `defuddle-cli`).
- Python ≥ 3.11 avec le `py` launcher (PEP 514).
- Git.
- Claude Code (CLI v2.1.x — `CLAUDE.md` mentionne "CC v2.1.138").
- Optionnels : ffmpeg + faster-whisper (skill `watch`), deno.

**Étapes de setup**

```bat
:: 1. Cloner le repo
git clone <repo-url> claude-forge
cd claude-forge

:: 2. Installer les outils CLI (vérifie prérequis + installe defuddle, yt-dlp, fastmcp, ffmpeg…)
install.bat

:: 3. Installer les dépendances du serveur MCP
cd mcp-forge-brain
pip install -e .

:: 4. (Optionnel) Déployer globalement dans ~/.claude/ pour avoir forge dans tous les projets
::    via la skill /install-forge OU manuellement (xcopy sous Windows)
xcopy /E /I .claude %USERPROFILE%\.claude
```

**Configuration post-install**
- Le serveur MCP démarre automatiquement à chaque SessionStart via `mcp-autostart.py` (port 8091). Aucune action manuelle.
- `.mcp.json` déclare le serveur : `{"forge-brain": {"type":"http","url":"http://localhost:8091/mcp"}}`.
- `mcp-forge-brain/config.yaml` : `vault_path: vault/claude-forge`, `port: 8091`, poids FTS (`file_stem:10`, `aliases:8`, `content:1`), `auto_commit: false`.
- **Mémoire portable** : à la 1re session après clone, Claude Code affiche un dialogue d'approbation des imports (`@memory/MEMORY.md`). Ne PAS décliner — sinon les imports sont désactivés silencieusement et la mémoire ne se charge plus. Documenté dans `install-forge` + CLAUDE.md section Mémoire.
- Secrets x-read : déposer `.claude/secrets/x-cookies.json` (gitignored) si on utilise la skill `x-read`.

**Vérifier que ça marche**
```bat
:: Le MCP répond ?
python -c "import socket; socket.create_connection(('127.0.0.1',8091),timeout=1); print('MCP OK')"

:: Cohérence interne du studio → skill /self-check
:: Dashboard source vs installé → skill /forge-status
:: Tests du serveur MCP
cd mcp-forge-brain && python -m pytest    :: 143 tests
:: Tests des hooks
python -m pytest .claude/hooks/tests/     :: 101 tests
```

**Désinstaller proprement**
- Arrêter le serveur MCP (`taskkill` sur le process Python du port 8091).
- Supprimer `%USERPROFILE%\.claude\` (composants déployés) — attention à ne pas supprimer la config Claude Code globale légitime.
- Supprimer le dossier `claude-forge`.
- Retirer la déclaration `forge-brain` de tout `.mcp.json` global.
Pas de désinstalleur fourni — opération manuelle.

---

## 5. Inventaire détaillé

### Agents (11)

Tous portent `memory: project`. Tableau de synthèse, puis détail.

| Agent | Fichier | Lignes | Model | Effort | Color | permissionMode | Skills frontmatter |
|---|---|---|---|---|---|---|---|
| agent-creator | `.claude/agents/agent-creator.md` | 101 | sonnet | high | pink | acceptEdits | cc-agents-ref, forge-brain, obsidian-markdown |
| claudemd-optimizer | `.claude/agents/claudemd-optimizer.md` | 99 | sonnet | high | pink | acceptEdits | cc-features-ref, forge-brain, obsidian-markdown |
| devils-advocate | `.claude/agents/devils-advocate.md` | 177 | opus | high | red | acceptEdits | forge-brain, obsidian-markdown |
| hook-creator | `.claude/agents/hook-creator.md` | 74 | sonnet | high | pink | acceptEdits | cc-hooks-ref, cc-features-ref, forge-brain, obsidian-markdown |
| outcomes-grader | `.claude/agents/outcomes-grader.md` | 93 | opus | high | yellow | plan | (aucune) |
| python-dev | `.claude/agents/python-dev.md` | 98 | sonnet | high | green | acceptEdits | python-ref, forge-brain, obsidian-markdown |
| repo-inspector | `.claude/agents/repo-inspector.md` | 299 | opus | xhigh | purple | plan | 10 skills |
| responsable-ia | `.claude/agents/responsable-ia.md` | 120 | opus | high | purple | acceptEdits | forge-brain, obsidian-markdown, craft-prompt, cc-prompt-ref |
| self-updater | `.claude/agents/self-updater.md` | 63 | sonnet | high | cyan | acceptEdits | cc-news, cc-features-ref, cc-hooks-ref, cc-agents-ref, cc-skills-ref, forge-brain, obsidian-markdown |
| skill-creator | `.claude/agents/skill-creator.md` | 117 | sonnet | high | pink | acceptEdits | cc-skills-ref, forge-brain, obsidian-markdown |
| vault-maintainer | `.claude/agents/vault-maintainer.md` | 177 | sonnet | high | cyan | acceptEdits | forge-brain, obsidian-markdown |

Note : `responsable-ia` est `color: purple` (corrigé 2026-05-27 lors de l'audit transverse — pink est réservé aux méta-créateurs forge). `devils-advocate` est `effort: high` en frontmatter, body aligné (corrigé 2026-05-27).

**agent-creator** — crée/modifie des subagents via 10 questions séquentielles + checklist 9 points. Déclenche "crée un agent qui". Dépend de MCP (`comment-creer-agent`, `workflow-claude-code-optimal`) + cc-agents-ref. 3 interdictions absolues (jamais d'agent orchestrateur/CTO, jamais d'agent doc, jamais pré-créer les fichiers que l'agent générera).

**claudemd-optimizer** — rédige/optimise un CLAUDE.md vers ~100-200 L, supprime le filler, convertit les règles ignorées en hooks. Bloqué en édition directe par delegate-guard (CLAUDE.md protégé).

**devils-advocate** — critique adversariale d'un livrable majeur avant ship, verdict structuré (BLOCKING / WARNING / NITPICK) + sauvegarde dans `Knowledge/critiques/`. Conditionnel ciblé (rule `devils-advocate-pipeline.md`). Read-only (`disallowedTools: Write, Edit`), `maxTurns: 25`. Pattern STOP + ESCALADE (`devils-advocate.md:62-82`) : ne peut pas appeler AskUserQuestion (limitation sub-agents), retourne un bloc `## AMBIGUÏTÉ DÉTECTÉE` structuré. Interdiction explicite du fallback Bash heredoc (cause du bug du 22 mai 2026).

**hook-creator** — crée/modifie des hooks selon la doctrine 22 mai (lint/security/scope uniquement). Suggère `/loop` ou `/schedule` si plus approprié. Impose chemin absolu Python Windows + matcher triplet `Write|Edit|MultiEdit`.

**outcomes-grader** — note un livrable contre un RUBRIC.md, PASS/FAIL/PARTIAL par critère (MUST gate + SHOULD 65% + NICE 35%). Utilisé EXCLUSIVEMENT par la skill `outcomes-test`. Le plus restrictif : `permissionMode: plan`, `disallowedTools: Write, Edit, Bash, Agent`, aucune skill, aucun MCP.

**python-dev** — implémente du Python en TDD strict, tâche par tâche. Seul agent avec un **hook inline** (PostToolUse `py_compile`). Reporting `[TASK N DONE]` / `[PLAN COMPLETE]`. C'est l'agent qui a implémenté `search_sessions` (A1).

**repo-inspector** — audite / analyse / scanne un repo en 3 modes (`audit` = `.claude/` vs canoniques ; `analyze` = analyse complète + reco CC ; `scan` = patterns du code). Le plus gros agent (299 L), seul en `effort: xhigh`, seul avec le tool `Agent` + WebFetch/WebSearch. Read-only. Issu de la fusion de project-analyzer + project-auditor + codebase-scanner (supprimés le 2026-05-26, commit `8277279`).

**responsable-ia** — assiste Raphael dans tous ses actes de Lead IA Neoteem (CODIR/6-pager, roadmap RICE/WSJF/OKR, AI Act/FRIA, 1:1, build vs buy, archi RAG/agents Loji, tickets Jira). 17 déclencheurs explicites. Ancré contexte Neoteem ; catalogue de 25 tâches × framework × wikilink vault. C'est l'agent "métier" du corpus (les autres sont méta-CC).

**self-updater** — détecte les nouvelles features CC via cc-news et met à jour les skills `cc-*-ref`. Le plus simple (63 L). Ne modifie QUE les skills cc-*, ajoute sans supprimer.

**skill-creator** — crée/optimise des skills (9 questions + checklist 10 points), impose description directive "ALWAYS invoke when…" et section Gotchas. Donnée citée : "73% des skills passives ne se déclenchent jamais". A implémenté l'enrichissement de `/done` (A3).

**vault-maintainer** — maintient la qualité des notes vault après modification (7 champs frontmatter, ≥4 aliases, wikilinks, MOC). Scope strict : jamais le vault entier. Ne corrige PAS l'orphelinat automatiquement.

### Skills (47)

Conventions : `user-invokable: true` = slash command ; `false` = référence passive non invocable manuellement (chargée par description) ; `disable-model-invocation: true` = slash pure sans inférence modèle.

**Skills de référence Claude Code (`user-invokable: false`)** — cc-agents-ref (117), cc-skills-ref (154), cc-hooks-ref (216), cc-features-ref (251), cc-cowork-ref (298), cc-prompt-ref (197), python-ref (183). Ces 7 ne sont PAS orphelines : chacune est référencée en frontmatter `skills:` ET dans le body de 2 à 4 agents créateurs, plus auto-trigger par description forte. `false` est le réglage canonique pour une bibliothèque de référence chargée par un parent (les basculer en `true` serait une régression — l'utilisateur ne tape pas `/cc-agents-ref`).

**Skills slash command (`user-invokable: true`)** — analyze-project (91), cc-advisor (96), cc-news (159), config-guardian (98), craft-prompt (148), done (303+, enrichi A3), evolve (227), expand (48), forge-review (255), forge-status (42, `disable-model-invocation`), git-multi-repo (57), install-forge (50, `disable-model-invocation`), notes (134), outcomes-test (138), pivot-check (131), python-script-refactor-masse (77), reasoning-cache (186), recap (180), self-check (45, `disable-model-invocation`), skill-evolve (245), spec (201), vault-audit (163), watch (205), auditor-empirical-verify (59), windows-hooks-cross-machine (54), x-read (134).

**Skills auto-trigger (`user-invokable` absent — chargées par description)** — agentshield-like-scanner (121), arxiv-verification (56), audit-thematique-clusters (126), configure-claude-desktop (87), cross-repo-propagation (50), da-blocking-arbitrage (92), defuddle (42), forge-brain (194), mcp-brief-then-direct (72), methode-pivoter-doctrine (99), web-search-canonical-source (93).

**Skills externes / upstream Obsidian (exemptées de delegate-guard)** — json-canvas (244, asset `references/EXAMPLES.md` restauré verbatim upstream le 2026-05-27), obsidian-markdown (213), obsidian-bases (376). Ces 3 + `defuddle` sont dans `EXEMPT_SKILL_DIRS` du hook delegate-guard (copies read-only).

**Exemples d'usage concrets**
- `/recap` au début d'une session → snapshot git + vault + mémoire.
- "Crée une skill /commit" → skill-creator pose 9 questions, génère le dossier.
- `/forge-review` → verdict KILL/EVOLVE/KEEP/MISSING sur le setup.
- `/done` en fin de session → métacognition + propose des blocs de capitalisation à valider (`[v]/[m]/[i]`).
- Partage d'une URL YouTube → skill `watch` transcrit et résume.

### Hooks (9)

Tous en Python, câblés dans `.claude/settings.json`, invoqués via `py "${CLAUDE_PROJECT_DIR}/.claude/hooks/<nom>.py"`. Tous fail-open (exit 0 sur erreur de parsing). Tests : 5 fichiers dans `.claude/hooks/tests/` (101 tests).

**security-guard.py** — PreToolUse `Bash`. Bloque (exit 2) : `rm -rf /` / `rm -fr /`, `git push --force` / `-f`, `git reset --hard` sans cible, `git clean -f`. 6 patterns regex. `main()` gardé (corrigé Phase 2 pour testabilité par import).

**delegate-guard.py** — PreToolUse `Edit|Write|MultiEdit`. Bloque les éditions de fichiers protégés DANS claude-forge : `SKILL.md` → skill-creator, `CLAUDE.md` → claudemd-optimizer, `.claude/agents/*.md` → agent-creator. Bypass : fichier hors forge ; `agent_type`/`agent_id` = spécialiste (exact-match depuis Phase 2, le substring match était un bug corrigé) ; parsing du transcript révélant un sous-agent actif ; edit < 20 chars (typo) ; toute erreur (fail-open). `EXEMPT_SKILL_DIRS` : json-canvas, defuddle, obsidian-cli, obsidian-markdown, obsidian-bases.

**meta-commentary-detector.py** — PreToolUse `Write|Edit|MultiEdit`. Le plus sophistiqué (~470 L). Bloque 11 patterns de méta-commentaire dans les composants forge (tradeoff italique, `Source:`, `Cf doctrine`, `= tip #N Nom`, `— Prénom Nom` en fin de ligne, citations `(arXiv:…)`, `(depuis <date>)`, `(validé N mois)`). Exclut vault/, Knowledge/, references/, RECAP.md, CHANGELOG.md. Applique l'édition en mémoire avant scan. Self-test intégré (`--self-test`). Utilisé en oracle de classification lors de l'audit transverse (passé en scan sur tout son scope).

**session-health.py** — UserPromptSubmit. Compteur de tours scopé par `session_id`. Tours 1-2 : tip /recap. Tous les 20 : rappel /compact ou /clear. Tous les 40 : rappel urgent. Non bloquant.

**skill-activation.py** — UserPromptSubmit. Matche le prompt vs `.skill-triggers.json`, injecte un `additionalContext` recommandant la skill. Bypass préfixes `* / # !`. Tracker de session anti-répétition. Non bloquant.

**session-reminder.py** — SessionStart. Nettoie les markers de la session précédente. Affiche un extrait (500 chars) du `<repo>/memory/MEMORY.md` — résout le chemin via `__file__` (robuste au cwd, ne dépend pas de `${CLAUDE_PROJECT_DIR}`, cf doctrine 4-contextes).

**mcp-autostart.py** — SessionStart (async). Teste le port 8091 ; si mort, lance `mcp-forge-brain/start.py` en process détaché Windows (`DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`). Toujours exit 0. Imports orphelins retirés 2026-05-27.

**learning-reminder.py** — Stop (`once: true`). 1×/session : bloque le Stop avec un rappel en 5 points (mémoire projet, vault Knowledge, section Apprentissage, CLAUDE.md, /reasoning-cache). Marker dans `%TEMP%`, nettoyé par session-reminder.

**proactivity-reminder.py** — Stop (`once: true`). 1×/session si ≥5 tours : "as-tu fait une proposition Jarvis ?". Garde `stop_hook_active` contre la boucle.

Note : le hook inline `py_compile` de python-dev (frontmatter de l'agent) est un 10e point d'interception, scopé à cet agent.

### MCP (1 serveur configuré)

**forge-brain** — `http://localhost:8091/mcp` (`.mcp.json`). Serveur HTTP local maison (FastMCP + SQLite FTS5), 2 deps (fastmcp, pyyaml). Auto-start au SessionStart.

- **Backend vault** : `forge-brain.db` (FTS5, poids BM25 file_stem:10 / aliases:8 / content:1). Watcher (`watcher.py`) ré-indexe le vault.
- **Backend sessions** (ajouté en A1) : table FTS5 séparée `session_messages`, indexe `~/.claude/projects/*.jsonl` (243 transcripts, 15858 messages, subagents exclus configurables). `sessions_indexer.py` + `sessions_db.py` + `sessions_watcher.py` (incrémental mtime), eager au boot (scan 2,68 s mesuré).
- **22 outils exposés** (comptés dans `mcp-forge-brain/src/tools/brain.py`) :
  - Lecture (14) : `search_brain`, `search_sessions`, `read_note`, `read_note_by_path`, `read_section`, `read_note_resolved`, `get_backlinks`, `get_tags`, `get_property`, `list_notes`, `vault_stats`, `find_by_property`, `usage_stats`, `lint_vault`
  - Écriture (6) : `create_note`, `append_note`, `update_note`, `insert_section`, `update_property`, `bulk_update_property`
  - Move/Delete (2) : `move_note` (réécrit les wikilinks), `delete_note` (refuse si backlinks > 0 sauf force)
- Auth/credentials : aucun (HTTP localhost, confiance machine locale).
- Cohérence documentaire : CLAUDE.md, `forge-brain-proactive.md` et le code disent tous 22 outils (la discordance 19/21 de versions antérieures est résolue).

Note : d'autres serveurs MCP (langfuse, Atlassian, neoteem-brain) apparaissent comme outils déférés dans l'environnement de session, mais ne sont PAS déclarés dans le `.mcp.json` de claude-forge — ils viennent de la config Claude Code globale / d'autres projets.

---

## 6. Vault interne (forge-brain)

**Stats** (via `vault_stats` 2026-05-27) : **430 notes, 234 tags, 2819 wikilinks, 2533 aliases** (≈5,9 aliases/note). Pattern Karpathy LLM Wiki (3 layers).

**Structure (notes par dossier)**

| Dossier | Notes | Contenu |
|---|---|---|
| 04-Techniques | 113 | claude-code/, agents/, rag/, prompt-engineering/, fine-tuning/, patterns/, context-engineering/ |
| Knowledge | 91 | erreurs/(34), critiques/(23+), syntheses/, raisonnements/, explorations/, questions/, tests/, evolutions/, reviews/, drafts/ |
| 05-Leaders | 80 | claude-code/, agents/, rag/, fine-tuning/, prompt/, industrie/ |
| 2-Casquettes | 41 | responsable-ia/ (12 sous-dossiers) + Famille, Gaming, Raphael-Picard |
| 01-Claude | 30 | Code/features/, Code/changelog/, Code/best-practices/, Cowork/ |
| 1-Projets | 21 | Claude-Forge/, Neoteem/ (ia_back, neo_ia, neoteem-brain, bdd), lojii/ |
| raw | 8 | Sources immuables (2026-05-22-chantier/) |
| 06-Industrie | 8 | News (événements, funding) |
| 00-Hub | 8 | Home.md + 7 MOC |
| 07-Prompts | 7 | system-prompts/, techniques/ |
| 03-Modeles | 7 | anthropic/, openai/, google/, xai/ |
| 02-Concurrents | 5 | cursor/, copilot/, openai/, google/, xai/ |
| 0-Inbox | 5 | Captures (context-actuel.md + 4 inbox de travail) |
| .claude | 2 | notes techniques |

**Convention de nommage** : deux régimes — notes de référence/leaders en **Title Case avec espaces** (`Boris Cherny.md`, `RAG.md`, `Opus 4.7.md`), notes canoniques et Knowledge en **kebab-case**. Préfixes : `comment-creer-*`, `comment-ecrire-*`, `methode-*`, `pattern-*`, `erreur-*`, `critique-YYYY-MM-DD-*`, `raisonnement-*`, `adr-*`, `_index.md`.

**Top notes canoniques** (lecture MCP directe)
1. **methode-analyser-repo** — META 6 étapes, cœur = ordre canonique A→B→C→D→E (analyser le réel → lire canoniques en entier → croiser → plan d'écarts → exécuter).
2. **comment-ecrire-claudemd** — target <200 L, 5 lignes Karpathy en ouverture, test "Would removing this cause mistakes?".
3. **comment-creer-skill** — 9 catégories Thariq, description <250 chars, SKILL.md <500 L, pattern "skill qui propose un diff à valider" (ajouté A3).
4. **comment-creer-agent** — "Agent = Model + Harness", split Sonnet/Opus, 8 couleurs, frontmatter↔body alignement obligatoire.
5. **comment-creer-hook** — 29 events, exit 0/1/2, lint/security/scope OUI workflow NON.
6. **workflow-claude-code-optimal** — 7 pratiques (Routines Boris, Advisor Strategy, leaf nodes, multi-clauding, /loop, Sonnet/Opus split, compounding).
7. **mcp-vs-skills-doctrine** — "MCP connects data; Skills teach how-to", lethal trifecta (Willison).
8. **pattern-vault-llm-karpathy** — 3 layers, index.md + log.md obligatoires.
9. **raisonnement-22mai-doctrine-vs-enforcement** — pivot doctrinal (suppression de 7 hooks workflow ×2 repos).
10. **resolution-path-3-contextes** — doctrine 4-contextes de résolution de path (skill = git rev-parse, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}`, .mcp.json = relatif au cwd).
11. **decision-memoire-dans-le-repo** — ADR mémoire portable via @import (accepté 2026-05-27).
12. **methode-pivoter-doctrine** — checklist 5 étapes anti-drift résiduel.
13. **critique-2026-05-27-compounding-retroactif** — verdict DA (c) sur le scan rétroactif à /done (tué, probe 0/12).
14. **phase-4-comparaison-hermes-roadmap** — matrice comparative vs Hermes Agent + roadmap A1/A2/A3.

**Comment Claude lit le vault** : EXCLUSIVEMENT via MCP forge-brain (22 outils). Grep/Read/Glob brut interdits (`forge-brain-proactive.md`).

**Comment Claude écrit le vault** : via MCP (`create_note`, `append_note`, `insert_section`, `update_note`, `update_property`, `bulk_update_property`), avec la skill `obsidian-markdown`. Jamais de Bash heredoc (bug 22 mai). Gotcha tracé : `append_note` par alias court ambigu résout vers le mauvais fichier (`mcp-alias-ambigu-chemin-exact`, re-violé 3× → feedback `feedback-reviole-3x-regle-insuffisante`).

**Qui décide d'écrire et quand** : la session principale et certains agents (devils-advocate → critiques, vault-maintainer → corrections, responsable-ia → casquette). Déclencheurs : après cc-news, après une erreur, après un raisonnement multi-étapes (`/reasoning-cache`), en fin de session (`/done`).

**Fréquence d'écriture (git log du vault)** : fichiers les plus modifiés — `CHANGELOG.md` (40+), `0-Inbox/context-actuel.md` (37+), `00-Hub/MOC-Techniques.md` (21), `log.md` (append-only). Le vault est écrit à presque chaque session substantielle.

---

## 7. Usage réel

**Workflows typiques**

1. *Reprise de contexte.* `/recap` → snapshot git + vault stats + dernière mémoire + date cc-news + suggestion de contexte. En 10 s, Claude sait où on en est.

2. *Besoin flou.* La session principale invoque `cc-advisor` qui recommande un composant (hook ? skill ? agent ? rule ?), puis dispatche le créateur approprié.

3. *Création d'un composant.* "Crée un agent qui audite mon codebase" → `agent-creator` (questions + checklist) → optionnellement `devils-advocate` si livrable majeur → présentation à Raphael. L'édition directe est bloquée par `delegate-guard.py`.

4. *Analyse d'un repo externe.* "Analyse neofront et propose une config CC" → `repo-inspector` (mode analyze/scan/audit) suit la méthode 6 étapes `methode-analyser-repo`.

5. *Fin de session, capitalisation.* `/done` → métacognition (décisions, faits, préférences, erreurs) → **propose des blocs prêts-à-écrire validés par item** (`[v]/[m]/[i]`) → mise à jour mémoire + vault + `context-actuel.md`. Renforcé par `learning-reminder.py`.

6. *Veille.* `cc-news` orchestre 11 agents par domaine et capitalise les découvertes ; `self-updater` met à jour les skills `cc-*-ref` si une feature CC change. (Voir section 8bis.)

7. *Travail cross-machine.* Raphael bosse le matin sur le PC boulot (écrit feedbacks via /done, commit, push), le soir sur le PC perso il pull et retrouve toute la mémoire. La mémoire suit le git (section 9).

**Anti-patterns à éviter (du repo)**
- Éditer directement un SKILL.md / agent / CLAUDE.md (bloqué par hook).
- Grep/Read brut sur le vault au lieu du MCP forge-brain.
- Créer un agent orchestrateur/CTO (`feedback_no_cto_agent.md`).
- Routing dans CLAUDE.md plutôt que dans `.claude/rules/`.
- Sessions fourre-tout multi-chantiers (`feedback_session_multi_chantiers.md` : "JAMAIS 4+ chantiers indépendants").
- Bash heredoc pour écrire des notes vault (boucle quoting Windows).
- Hooks de workflow agentique (interdits par la doctrine 22 mai).
- `append_note` par alias court ambigu (résout vers le mauvais fichier).

---

## 8. Self-improvement

**La boucle de feedback est explicite et outillée**
1. **Détection** : hook `learning-reminder.py` (Stop) force la question "as-tu appris quelque chose ?" 1×/session.
2. **Classification** (frontière mémoire ↔ vault, `memory-discipline.md`) : feedback relation/préférence → `memory/feedback_*` / `user_*` ; référence technique → `memory/reference_*` ou vault ; erreur → les DEUX ; savoir réutilisable → vault.
3. **Capitalisation** : `/done` (métacognition + propose des blocs à valider), `/reasoning-cache`, `devils-advocate` (→ critiques), `cc-news` (→ notes atomiques), `/skill-evolve` (→ evolutions), `/forge-review` (→ reviews).
4. **Application** : la mémoire (`memory/MEMORY.md` + 193 fichiers feedback) est rechargée à chaque session (hook `session-reminder.py` + `@import`), les canoniques vault sont lus par les créateurs/analyseurs.

**Trois changements doctrinaux livrés (issus de la comparaison Hermes, Phase 4)**
- **A3 — Capitalisation proactive à /done (LIVRÉ 2026-05-27)** : `/done` ne fait plus que de la métacognition — il **génère des blocs concrets prêts-à-écrire** (feedback mémoire au format `name:/description:/Why:/How to apply:`, note vault frontmatter+body, ou ADR) et les présente avec leur chemin cible. Raphael valide par item (`[v]alider / [m]odifier / [i]gnorer`). Aucune écriture sans validation. Différence clé vs un agent autonome : la proposition est un diff que Raphael relit, pas un overwrite silencieux. Capitalisé : `feedback_capitalisation_proposee_pas_auto`, amendement `comment-creer-skill` ("skill qui propose un diff à valider").
- **A1 — Recherche transcripts session (LIVRÉ 2026-05-27)** : 22e outil MCP `search_sessions(query, limit, project, role, since)`. Indexe l'historique conversationnel brut (`~/.claude/projects/*.jsonl`) dans une table FTS5 séparée. Répond à "qu'a-t-on dit la semaine dernière sur X" — un besoin que le vault capitalisé ne couvre pas. 37 tests (~60% adverse).
- **A1×A3 — Compounding rétroactif : TUÉE (verdict DA 2026-05-27)** : l'idée de croiser A1 et A3 pour scanner les transcripts passés à chaque `/done` et proposer les apprentissages jamais capitalisés a été **tuée** par le devils-advocate (verdict (c), pas (b)). Probe empirique : sur les 12 messages les plus chargés en signal (slice la plus favorable), **0/12 capitalisable ET nouveau** — la prémisse "il y a un gisement non capitalisé" est empiriquement fausse. Plus une circularité by-design (le scan remonterait les blocs `/done` proposés et les `feedback_*.md` cités comme s'ils étaient nouveaux). **Pivot retenu non encore implémenté** : `/recall-uncaptured <topic>` on-demand (Raphael fournit le topic → scope étroit → sidestep le bruit et la circularité), à valider empiriquement sur ~5 invocations réelles avant tout build. Cf `critique-2026-05-27-compounding-retroactif`.

**Mécanismes de capitalisation en place** : `memory/MEMORY.md` + fichiers `feedback_*.md` / `project_*.md` / `reference_*.md` ; vault `Knowledge/` (erreurs, critiques, raisonnements, synthèses, tests, evolutions, reviews) ; CLAUDE.md (Gotchas comportementaux) ; rules `.claude/rules/`.

**Ce qui déclenche une mise à jour** : recherche web/cc-news, erreur significative, raisonnement multi-étapes, décision majeure (vault) ; `/skill-evolve` (skill) ; agent-creator (agent) ; audit mensuel `/forge-review` (CLAUDE.md).

**Contrôle vs autonomie** : la différence de fond avec un agent self-improving autonome est doctrinale — claude-forge place **Raphael dans la boucle avant écriture**. Conséquences : capitalisation tracée (git, diff, CHANGELOG, log.md append-only), correctible en amont, avec le *pourquoi* et un *déclencheur de réactivation*. Le prix : pas de couverture automatique (ce que Raphael oublie de capitaliser n'est pas rattrapé). A3 réduit ce gap en *proposant* (pas en auto-appliquant) ; le rattrapage rétroactif aveugle a été mesuré inutile (0/12) et tué.

---

## 8bis. Système de veille (cc-news)

La veille IA et Claude Code est outillée par la skill `cc-news` (`.claude/skills/cc-news/SKILL.md`, 159 L) et l'agent `self-updater`.

**Architecture de la veille**
- **Tier 0** (`SKILL.md:16-26`) : 5 queries fixes exécutées en premier quel que soit le domaine demandé (changelog CC, annonces Anthropic, releases frontier OpenAI/Google/Claude, déprécations/breaking, + le sujet si fourni).
- **Vault d'abord** : `search_brain` sur le sujet pour ne pas re-chercher ce qui est documenté avec un `derniere-maj` récent.
- **Orchestration complète** : 11 agents parallèles couvrant **6 spécialités** (Claude Code, RAG, agents, fine-tuning, concurrents, prompt-engineering ; les 4 plus denses sont scindés en 2 agents chacun pour respecter le budget de 6-8 queries/agent). Un 7e agent "Discovery" cherche le hors-radar. Chaque agent lit son fichier `references/domain-*.md` et exécute ses queries.
- **Capitalisation obligatoire** (étape 7) : 1 concept = 1 note atomique, rangée selon l'ontologie (modèle → `03-Modeles/`, concurrent → `02-Concurrents/`, technique → `04-Techniques/`, leader → `05-Leaders/`, industrie → `06-Industrie/`). Si nouvelle version CC découverte → mise à jour de la date de référence dans le SKILL.md lui-même.
- **Fallback X/Twitter** : Defuddle/WebFetch échouent sur X (DOM JS / HTTP 402) → délégation à la skill `x-read` (cookies du compte authentifié) ou copier-coller manuel.

**Base de leaders** : le vault contient **80 fiches de leaders** (`05-Leaders/`, 6 sous-dossiers : claude-code, agents, rag, fine-tuning, prompt, industrie — Karpathy, Boris Cherny, Thariq, Amanda Askell, Willison, Hashimoto…). En parallèle, les fichiers `references/domain-*.md` de cc-news contiennent des listes de leaders **hardcodées** dans les queries (ex. "Jonas Roman RAG production").

**Deux gaps majeurs identifiés (investigation 2026-05-27)** — ce sont les chantiers de l'évolution vers le tier Jarvis :

- **Chantier A — Pont automatique veille → doctrine (priorité HAUTE).** Aujourd'hui, cc-news capitalise les découvertes en notes atomiques, mais **rien ne relie automatiquement une découverte de veille à la doctrine canonique** : si un changelog CC contredit une note canonique forge (ex. une feature dépréciée, un nouveau comportement), aucun mécanisme ne le détecte ni ne propose un pivot. Le saut qualitatif serait un équivalent du "/done propose à valider" appliqué à la veille : détection de contradiction doctrinale + gate humaine. C'est le différenciateur vers le tier Jarvis (la veille nourrit la doctrine, pas seulement l'archive).

- **Chantier C — Synchronisation des 2 listes de leaders (priorité MOYENNE).** Les 80 fiches du vault (`05-Leaders/`) et les listes de noms hardcodées dans les `references/domain-*.md` de cc-news sont **deux sources désynchronisées**. Ajouter un leader au vault ne met pas à jour les queries de veille, et inversement. Source unique de vérité visée = le vault ; les queries de domaine devraient en dériver.

- **Chantier B — Checklist vendredi (priorité BASSE).** Rituel manuel de veille hebdomadaire. Pas d'automatisation possible côté forge vu la config machine pro (orga Team bloque GitHub cloud / triggers planifiés distants — `feedback_no_github_cloud.md`). Reste un déclencheur manuel.

---

## 9. Portabilité

**Mémoire portable cross-machine (architecture @import)**
C'était la dernière faille de portabilité : la mémoire vivait dans `~/.claude/projects/<encoded>/memory/`, hors de l'arbre git, perdue sur une nouvelle machine. Résolu 2026-05-27 (ADR `decision-memoire-dans-le-repo`, accepté) :
- Mémoire versionnée dans **`<repo>/memory/`** (symétrique avec `vault/`).
- **Lecture** : ligne `@memory/MEMORY.md` dans le CLAUDE.md **versionné** (`CLAUDE.md:100`). Verbatim doc Anthropic : *"Relative paths resolve relative to the file containing the import."* Chaque repo charge donc SA mémoire — pas de fusion en multi-repos. Zéro setup machine, zéro settings global, zéro classifier.
- **Écriture** : `/done` écrit dans `<repo>/memory/` (chemin dérivé de `git rev-parse --show-toplevel`). Lecture et écriture pointent la MÊME cible (sinon split-brain).
- Le mécanisme se généralise à tout repo (ajouter `@memory/MEMORY.md` à son CLAUDE.md).
- Pourquoi pas `autoMemoryDirectory` : il est user-scope global et n'expanse pas les variables → en chemin absolu il fusionnerait toutes les mémoires (cassé en multi-repos). `@import` est orthogonal : il s'ajoute au défaut sans l'écraser. Insight clé (`architecture-decision-memoire-portable-import`) : *un mécanisme validé sur un seul repo peut être faux sur le workflow réel multi-repos.*

**Doctrine 4-contextes de résolution de path** (`resolution-path-3-contextes`, vérifiée empiriquement)
La variable `${CLAUDE_PROJECT_DIR}` n'est PAS universelle. Le mécanisme correct dépend du contexte :

| Contexte | `${CLAUDE_PROJECT_DIR}` ? | Mécanisme correct |
|---|---|---|
| Skill (Bash) | ❌ vide | `$(git rev-parse --show-toplevel)` |
| Hook (Python) | ❌ non peuplé dans le process | `os.path.dirname(os.path.abspath(__file__))` puis remonter |
| settings.json (string `command`) | ✅ expansé par le harness | `${CLAUDE_PROJECT_DIR}` directement |
| .mcp.json (args/env) | ❌ pas de variable CC | paths relatifs au cwd |

Nuance : l'expansion de `${CLAUDE_PROJECT_DIR}` dans la string `command` de settings.json ne signifie PAS que `os.environ["CLAUDE_PROJECT_DIR"]` soit peuplé dans le process Python lancé — les deux sont indépendants. C'est pourquoi un hook utilise `__file__`, pas `os.environ`.

**Entre machines (Windows / Linux / Mac)** : cible primaire **Windows**. Hooks via `py` launcher + `${CLAUDE_PROJECT_DIR}`. Le code Python est OS-agnostique sauf `mcp-autostart.py` (flags Windows). `install.bat` et `scripts/*.bat` sont Windows-only.

**Entre missions** : portable = agents/skills méta-CC, doctrine canonique du vault, patterns de workflow, mémoire portable. Non portable tel quel = agent `responsable-ia`, plugin `ia-lead-neoteem`, skills `config-guardian`/`cross-repo-propagation`/`configure-claude-desktop` (noms de repos Neoteem hardcodés), notes `1-Projets/Neoteem/` et `2-Casquettes/`.

**Versioning** : git, branche `main`, versioning sémantique manuel dans l'en-tête de CLAUDE.md (v3.3). Pas de tags ni releases GitHub (l'orga Team bloque GitHub cloud).

**Sync entre instances** : déploiement par copie `.claude/* → ~/.claude/` (skill `install-forge`), comparaison via `/forge-status`. La mémoire et le vault suivent le git (pull/push). `mcp-forge-brain/git_sync.py` existe mais `auto_commit: false`.

---

## 10. Configuration & sécurité

**Permissions `.claude/settings.json` — allow** (pas de bloc `deny` ni `ask` dans le fichier ; les interdits vivent dans CLAUDE.md) : `Read`, `Write`, `Edit`, `Bash(git *)`, `Bash(git -C *)`, `Bash(ls *)`, `Bash(taskkill *)`, `Edit(.claude/agents/**)`, `Edit(.claude/skills/**)`, `Edit(./**)`, `MultiEdit(...)`. La coquille `Bash(taskkill *),` (virgule parasite) a été corrigée 2026-05-27.

Le CLAUDE.md précise le périmètre réel : permissions cross-repo TOTALES (Read/Write/Edit/Bash/MCP partout), **INTERDIT sauf demande explicite** : `rm -rf`, `git branch -D`, suppression de branches, force push sur main. Partiellement enforced par `security-guard.py` (6 patterns).

**env** : `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50"` (compaction à 50%), `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`.

**Modèles** : Sonnet exécution, Opus jugement, Haiku rapide. `effort: high` par défaut, `xhigh` réservé à repo-inspector, `max` jamais en frontmatter. Agents Opus : devils-advocate, outcomes-grader, repo-inspector, responsable-ia.

**Sandbox / containment** : Windows direct, pas de WSL ni devcontainer. MCP local (localhost:8091). Hooks fail-open. `permissionMode: acceptEdits` sur la plupart des agents, `plan` sur les read-only (outcomes-grader, repo-inspector).

**Secrets** : cookies x-read dans `.claude/secrets/x-cookies.json` (gitignored). `data/` (sortie twitter) gitignored. `memory/private/` + `memory/*-private.md` gitignored. Pas de credentials en clair dans `.mcp.json` (MCP local sans auth). **Audit confidentialité pré-migration mémoire (2026-05-27)** : 1 secret PostgreSQL prod trouvé dans 3 notes vault et **redacté** (commit `926af82`). Action de suivi tracée : rotation du mot de passe (`todo-rotation-password-postgres-prod`, P0 — voir section 12).

**Tests** : **244 verts** (101 hooks + 143 MCP), 0 régression. Mesuré 2026-05-27 (`pytest --collect-only`).

**Risques résiduels identifiés**
- Permissions très larges (`Bash(git *)` + Write/Edit cross-repo) — repose sur la discipline et `security-guard.py` (6 patterns seulement).
- MCP forge-brain sans authentification (acceptable car localhost machine personnelle, mais tout process local peut l'interroger).
- `delegate-guard.py` a des voies de bypass (typo < 20 chars, fail-open) — protection "best effort", pas étanche.
- `search_sessions` indexe l'historique conversationnel brut, qui peut contenir des secrets non redactés tapés en session. Index local non chiffré.

---

## 11. Points forts

- **Compounding outillé, pas seulement déclaré** : la boucle erreur→capitalisation→rechargement est matérialisée par des hooks (learning-reminder), des skills (/done qui propose des blocs à valider, /reasoning-cache) et un vault interrogeable par MCP.
- **Délégation forcée par construction** : `delegate-guard.py` empêche physiquement la dérive "j'édite vite à la main et c'est non conforme" — réponse directe à une erreur réelle documentée (2026-04-26).
- **Mémoire portable par git** : la mémoire suit le clone (`@import`), single mechanism cross-machine sans setup. Doctrine 4-contextes de résolution de path capitalisée.
- **Doctrine versionnée et datée** : pivot 22 mai tracé (`raisonnement-22mai-doctrine-vs-enforcement`), méthode anti-drift (`methode-pivoter-doctrine` + skill `pivot-check`). La doctrine est un artefact de premier ordre.
- **MCP maison optimisé pour LLM** : 22 outils pensés pour un agent (read_section économise 30× les tokens, find_by_property = Dataview, bulk_update évite les round-trips, search_sessions cherche l'historique brut), avec 143 tests pytest.
- **Honnêteté méthodologique** : DA qui tue une idée par probe empirique (compounding rétroactif, 0/12) plutôt que de la garder par optimisme ; bugs caractérisés ET fixés ; dette tracée avec déclencheurs.
- **meta-commentary-detector** : enforcement automatique du principe "le pourquoi vit dans le vault".
- **Séquence canonique A→B→C→D→E** : tout créateur/analyseur observe le réel avant de lire la doctrine avant de prescrire — anti-biais de perception structuré.

---

## 12. Points faibles / dettes tracées

**Dettes actives (avec déclencheur de réactivation)**

- **Double-source mémoire (transitoire).** L'`@import` `@memory/MEMORY.md` AJOUTE une source mémoire mais ne REMPLACE PAS l'auto-memory native. Le harness injecte TOUJOURS `~/.claude/projects/<encoded>/memory/MEMORY.md` en parallèle (tronquée à ~25 Ko, donc divergente de la version repo complète à 193 feedbacks). Visible dans le contexte de session courant (la 2e MEMORY.md est étiquetée *"Only part of it was loaded"*). **Pas la single source visée.** Étape manquante = désactiver/vider l'auto-memory native, ce qui exige une clé settings global (hard-block classifier → modification manuelle par Raphael). **Déclencheur** : différé tant que la divergence reste bénigne ; à traiter si un feedback important n'apparaît que dans une source. Cf `import-ajoute-pas-remplace-automemory`.

- **Rotation password PostgreSQL prod (P0).** Un secret prod a été trouvé et redacté du vault (commit `926af82`), mais le mot de passe lui-même n'est pas encore tourné. **Déclencheur** : à faire dès que possible (le secret a été exposé en clair dans l'historique git du vault avant redaction). Cf `todo-rotation-password-postgres-prod`.

- **Pont veille → doctrine absent (Chantier A, P-haute).** cc-news capitalise mais ne détecte pas les contradictions doctrinales. Voir section 8bis.

- **Listes de leaders dupliquées (Chantier C, P-moyenne).** 80 fiches vault vs `domain-*.md` hardcodés, désynchronisés. Voir section 8bis.

- **Feedback re-violé ≥3× (méta-dette).** `mcp-alias-ambigu-chemin-exact` re-violé 3× malgré présence en contexte → la règle écrite ne suffit pas. Candidat : garde-fou hook scope sur `append_note(stem multi-dossier)`. Cf `feedback-reviole-3x-regle-insuffisante`.

**Résolus récemment (trace condensée)**
- [2026-05-26, `8277279`] Agents fantômes (project-analyzer/auditor/codebase-scanner) fusionnés dans repo-inspector ; rules et baseline corrigées, agent-memory migrée.
- [2026-05-27] Discordance outils MCP (19/21 → 22, aligné code+doc).
- [2026-05-27, audit transverse] 5 non-conformités triviales corrigées : wikilink mort agent-creator, couleur responsable-ia (pink→purple), attribution-source dans notes/SKILL.md, `(validé 26 mai)` dans mcp-brief-then-direct, imports orphelins mcp-autostart.py. 73/78 composants conformes d'emblée.
- [2026-05-27] Asset json-canvas `EXAMPLES.md` restauré verbatim upstream.
- [2026-05-27] Coquille permissions `Bash(taskkill *),` retirée.
- [2026-05-27] Incohérence frontmatter↔body devils-advocate (effort) alignée.
- [Phase 2] 2 bugs caractérisés ET fixés : `security-guard.py` sans `main()` gardé (non testable) ; `delegate-guard.py` substring match sur `agent_id` (bypass indu) → exact-match + regression guard.

**Zones floues**
- Dépendances minimes, pas obsolètes (fastmcp>=2.0, pyyaml>=6.0).
- `data/` et `output/` gitignorés, jetables/régénérables (livrables ad-hoc pour d'autres repos, sortie twitter-api-client).

---

## 13. Métriques (git)

- **Commits total** : 302 (`git rev-list --count HEAD`)
- **Premier commit** : 2026-04-03 (`aab5cd4`) — **dernier** : 2026-05-27 13:30 (`39735a4`)
- **Période** : ~8 semaines (avril : 58 commits ; mai : 244 commits — accélération forte)
- **Tests** : **244 verts** (101 hooks + 143 MCP), 0 régression. Progression : 90 (Phase 1) → 207 (Phase 3) → 244 (post A1). Mesuré 2026-05-27.
- **Vault forge-brain** : 430 notes, 234 tags, 2819 wikilinks, 2533 aliases.
- **Mémoire** : 193 fichiers `feedback_*.md`, 249 fichiers `memory/*.md` total, index `MEMORY.md` ~229 L.
- **Inventaire** : 11 agents, 47 skills, 9 hooks, 10 rules, 22 outils MCP.
- **Auteurs** : Raphael Picard uniquement (casse variable = même personne).
- **Fichiers les plus modifiés** : `vault/CHANGELOG.md` (40+), `0-Inbox/context-actuel.md` (37+), `CLAUDE.md` (29+), `.claude/settings.json` (26+), `MOC-Techniques.md` (21), `cc-news/SKILL.md` (20). Agents les plus retouchés : les créateurs (skill-creator, agent-creator, claudemd-optimizer, hook-creator) + devils-advocate.

---

## 14. Glossaire

- **forge / claude-forge** : le projet, studio méta-Claude Code personnel.
- **forge-brain** : le vault Obsidian interne (430 notes) + le serveur MCP qui le sert.
- **Jarvis / contrat Jarvis** : posture relationnelle (Claude = partenaire proactif de Raphael = "Tony Stark"). Anticiper, protéger, innover, évoluer, être franc, autonome.
- **Canonique** : note vault faisant autorité (`#statut/canonique`). À lire EN ENTIER avant toute prescription.
- **Compounding** : capitalisation cumulative — chaque erreur/décision sauvegardée pour ne jamais être réapprise (Boris Cherny).
- **Compounding rétroactif** : idée (TUÉE) de scanner les transcripts passés à /done pour rattraper les apprentissages non capitalisés. Prémisse fausse (probe 0/12) + circularité by-design. Pivot retenu : `/recall-uncaptured` on-demand.
- **Doctrine 22 mai 2026** : pivot où les hooks de workflow agentique sont interdits (hooks = lint/security/scope).
- **Doctrine 4-contextes (résolution de path)** : skill = git rev-parse, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}`, .mcp.json = relatif au cwd. `${CLAUDE_PROJECT_DIR}` n'est pas universel.
- **@import** : ligne `@path` dans CLAUDE.md qui charge un fichier (path relatif au CLAUDE.md). Mécanisme de la mémoire portable (`@memory/MEMORY.md`).
- **Mémoire portable** : mémoire versionnée dans `<repo>/memory/`, chargée via @import, suit le git clone cross-machine.
- **Séquence A→B→C→D→E** : Analyser le réel → lire canoniques en entier → croiser → plan d'écarts → exécuter. Obligatoire pour tout créateur/analyseur.
- **Audit transverse** : audit ponctuel de conformité doctrinale sur tous les composants (9 critères), distinct des hooks (gardes en écriture). Le hook meta-commentary-detector y sert d'oracle de classification (passé en scan sur tout son scope).
- **search_sessions** : 22e outil MCP, recherche FTS5 dans les transcripts de session bruts (`~/.claude/projects/*.jsonl`).
- **delegate-guard** : hook qui bloque l'édition directe des fichiers protégés.
- **meta-commentaire** : justification/source/attribution dans un composant — interdit ("le pourquoi vit dans le vault").
- **Pattern Karpathy / LLM Wiki** : organisation du vault en 3 layers (raw / wiki / schema), avec index.md + log.md.
- **STOP + ESCALADE** : pattern pour sous-agents non-réentrants — au lieu d'inventer, retourner un bloc structuré à la session principale.
- **DA (devil's advocate)** : critique adversariale conditionnelle avant ship d'un livrable majeur.
- **MOC** : Map Of Content — note d'index thématique du vault (7 dans 00-Hub).
- **Casquette** : aire de responsabilité de vie dans le vault (`2-Casquettes/`), ex. responsable-ia.
- **context-actuel.md** : note vault (0-Inbox) réécrite par `/done` à chaque fin de session — état courant.

---

## 15. FAQ anticipée

**"C'est quoi claude-forge en 30 secondes ?"**
Le méta-outillage Claude Code personnel de Raphael : 11 agents, 47 skills, 9 hooks et un vault de 430 notes interrogeable par MCP (22 outils), qui conseillent et fabriquent de la config Claude Code conforme pour tous ses projets, et capitalisent chaque leçon pour ne jamais la réapprendre.

**"Pourquoi ne pas juste utiliser Claude Code sans claude-forge ?"**
Claude Code seul n'a pas de mémoire doctrinale structurée ni de garde-fous de conformité. Forge ajoute la délégation forcée aux créateurs (conformité par construction), une doctrine versionnée et datée, et une boucle de compounding outillée. Sans forge, on recrée des composants non conformes et on réapprend les mêmes erreurs.

**"La mémoire suit-elle quand je change de machine ?"**
Oui. La mémoire est versionnée dans `<repo>/memory/` et chargée via `@memory/MEMORY.md` dans le CLAUDE.md versionné. Le matin sur le PC boulot j'écris des feedbacks via /done, je commit, je push ; le soir sur le PC perso je pull et tout est là. Friction unique : à la 1re session après clone, approuver le dialogue d'import (sinon imports désactivés silencieusement). Dette connue : l'auto-memory native coexiste encore en parallèle (section 12).

**"Pourquoi le 'compounding rétroactif' n'a-t-il pas été construit ?"**
Parce que la mesure l'a tué. L'idée était de scanner les transcripts passés à chaque /done pour rattraper les apprentissages oubliés. Le devils-advocate a fait une probe empirique : sur les 12 messages les plus chargés en signal, 0 était capitalisable ET nouveau — le puits est sec. Plus une circularité by-design (le scan remonterait les propositions /done elles-mêmes). Pivot retenu : `/recall-uncaptured <topic>` à la demande, pas un scan systématique. Non encore implémenté, à valider empiriquement.

**"Comment marche la veille ?"**
La skill `cc-news` : 5 queries fixes (Tier 0) + consultation du vault + 11 agents parallèles sur 6 spécialités (Claude Code, RAG, agents, fine-tuning, concurrents, prompt), puis capitalisation obligatoire en notes atomiques. Deux gaps identifiés : pas de pont automatique veille→doctrine (Chantier A, P-haute) et listes de leaders dupliquées entre le vault et les fichiers de domaine (Chantier C, P-moyenne). Voir section 8bis.

**"claude-forge marche-t-il sur Windows direct ou faut WSL ?"**
Windows direct, pas de WSL. Hooks via `py` launcher et `${CLAUDE_PROJECT_DIR}`. `mcp-autostart.py` utilise des flags de process Windows. Linux/Mac demanderaient des adaptations (équivalents `.sh`, flags subprocess).

**"Est-ce que claude-forge fonctionne sans MCP ?"**
Partiellement. Le MCP forge-brain est le SEUL accès autorisé au vault — sans lui, lecture/écriture du vault (cœur du compounding) tombe. Les agents/skills/hooks de création fonctionnent encore mais privés des canoniques. Fallback Read/Glob prévu uniquement si le MCP crashe (cas exceptionnel).

**"Combien de temps pour onboarder quelqu'un ?"**
Non trivial. La densité doctrinale (10 rules, 47 skills, ~193 feedbacks, doctrine datée) suppose la lecture de CLAUDE.md + des canoniques du vault. Ce document est le meilleur point d'entrée. Compter une demi-journée pour la philosophie, davantage pour l'inventaire complet. Mais : claude-forge est un outil PERSONNEL, l'onboarding tiers n'est pas un objectif.

---

## Annexe A — Ce que je n'ai pas pu vérifier

- **Numéros de ligne via sous-agents** : la majorité des line refs des agents/skills proviennent de lectures par sous-agents recoupées par échantillonnage (devils-advocate:62-82 vérifié exact ; responsable-ia color, devils-advocate effort, settings env vérifiés direct cette session). Non revérifiées caractère par caractère pour les 11 agents et 47 skills.
- **README périmé (hors scope cette session)** : `README.md:29` dit "21 outils", `README.md:30` dit "~412 notes" — chiffres dépassés (22 outils, 430 notes). Je n'ai pas touché le README (scope = SELF_PORTRAIT uniquement). À corriger lors d'une session dédiée (délégation claudemd-optimizer non requise, README hors delegate-guard).
- **Triple chiffre de notes dans l'ancien portrait** : l'ancienne version affichait 412 / 412 / 417 dans trois sections différentes (symptôme de patches multiples). Cette version unifie tout sur `vault_stats` du 2026-05-27 = **430**.
- **Double-source mémoire** : la coexistence auto-memory native / @import est observée empiriquement (contexte de session), mais le comportement exact du harness (quelle source prime en cas de conflit) n'est pas documenté côté Anthropic. Dette tracée, non résolue.
- **`ia-lead-neoteem`** : plugin Cowork inventorié (7 skills) mais le contenu de ses SKILL.md n'a pas été lu en détail.
- **search_sessions / sécurité** : l'index des transcripts peut contenir des secrets tapés en session ; non audité ligne à ligne. Index local non chiffré.
- **Tests** : exécutés via `pytest --collect-only` = **244 collectés** (101 hooks + 143 MCP). Le pass effectif (vert) n'a pas été relancé intégralement cette session — le compte est celui de la collecte ; les sessions précédentes rapportent 0 régression.

---

## Annexe B — Comparaison Hermes Agent (condensée)

Comparaison sur code source réel (2026-05-27) avec Hermes Agent (Nous Research, 169 296 stars, MIT, agent autonome multi-canal). Matrice complète et roadmap dans `[[phase-4-comparaison-hermes-roadmap]]`.

**Verdict** : sur les axes prioritaires (mémoire / apprentissage / compounding / conformité), claude-forge gagne 8 axes, Hermes 3, 1 égalité doctrinale. claude-forge est strictement supérieur sur la mémoire structurée (vault 430 notes / 2819 wikilinks vs MEMORY.md plat 2200 chars), la conformité par construction (delegate-guard bloquant exit 2, zéro équivalent Hermes), la doctrine versionnée + anti-drift, la traçabilité (git + log append-only) et la capitalisation décisionnelle (règle + pourquoi + déclencheur). Hermes mise sur l'automatisation autonome (background review qui écrit sans validation) ; forge sur le contrôle structuré, cohérent avec le use case synchrone de Raphael.

**Les gaps pertinents identifiés en Phase 4 sont désormais comblés ou tués** : A1 (recherche transcripts, `session_search`) LIVRÉ via `search_sessions` ; A3 (capitalisation proposée à /done) LIVRÉ ; A1×A3 (compounding rétroactif) TUÉ par probe empirique (0/12). Reste A2 (lifecycle/usage tracking des skills) à faire en P2, et l'extension `lint_vault` pour la détection de contradictions (gap léger, non priorisé).

**Gaps Hermes déclinés** (déclencheurs de réactivation dans `[[adr-gaps-hermes-declines-phase-4]]`) : triggers async, background review autonome, self-evolution GEPA, Skills Hub public, sécurité supply-chain, communauté/onboarding tiers. Tous structurellement non pertinents pour un outil personnel synchrone — asymétrie assumée, pas un déficit.
