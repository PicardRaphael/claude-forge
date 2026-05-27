# CLAUDE_FORGE — Self-Portrait

Document d'auto-cartographie exhaustive. Date de génération : 2026-05-27. État du repo : branche `main`, 245 commits, dernier commit `8277279` (2026-05-26).

Remarque méthodologique : les numéros de ligne des composants `.claude/` ont été relevés en grande partie par sous-agents de lecture puis recoupés par échantillonnage (spot-check). Quand une affirmation provient d'une lecture indirecte non revérifiée caractère par caractère, c'est signalé. Les hooks, le `settings.json`, le code MCP et les métriques git ont été lus directement.

---

## 1. Identité du projet

- **Nom** : claude-forge
- **Version** : 3.3 (déclarée dans `CLAUDE.md:3` — "permissions totales + doctrine effort calibrée")
- **Auteur** : Raphael Picard (`raphael.picard@neoteem.fr` / `raphael@neoteem.fr`). 245 commits, un seul auteur réel (227 sous "Raphael Picard", 18 sous "Raphael PICARD" — même personne, casse différente).
- **Licence** : Pas de fichier LICENSE détecté. Projet personnel non distribué publiquement.
- **Créé le** : 31 mars 2026 (`CLAUDE.md:3`) ; premier commit git 2026-04-03 (`aab5cd4` "Initial commit: claude-forge - assistant personnel Claude Code").

**Pitch en une phrase**
claude-forge est le méta-outillage Claude Code personnel de Raphael : un ensemble d'agents, skills, hooks, rules et un vault de connaissances qui conseillent, créent, optimisent et capitalisent sur l'usage de Claude Code à travers tous ses projets.

**Pitch en un paragraphe**
claude-forge est un projet "studio" qui ne produit pas d'application : il produit de la configuration Claude Code (agents, skills, hooks, CLAUDE.md) pour d'autres projets, et accumule la doctrine d'usage de Claude Code dans un vault Obsidian (`forge-brain`, 412 notes) interrogeable via un serveur MCP maison. Sa thèse centrale est le *compounding* : chaque erreur, chaque décision, chaque technique apprise est capitalisée dans le vault ou la mémoire pour ne jamais être réapprise. Il incarne une relation "Tony Stark / Jarvis" (`CLAUDE.md` section "Contrat Jarvis") où Claude est un partenaire proactif, pas un exécutant. Techniquement, c'est du Python (hooks + serveur MCP FastMCP/SQLite-FTS5) orchestré par des fichiers Markdown, ciblé Windows, portable cross-machine via le `py` launcher.

**Public cible**
- Raphael Picard, en premier lieu — c'est un outil personnel (`memory/feedback_forge_is_personal.md` : "Forge = PERSONNEL, généraliste").
- Par extension, toute personne qui utilise Claude Code intensivement sur plusieurs repos et veut industrialiser la création de composants CC + capitaliser sa doctrine d'usage.

**Pas le public cible**
- Quelqu'un qui cherche une application métier (claude-forge ne fait rien fonctionnellement, c'est un méta-outil).
- Un débutant Claude Code — la densité doctrinale (10 rules, 47 skills, doctrine datée "22 mai 2026") suppose une maîtrise préalable.
- Une équipe cherchant un framework partagé clé-en-main : beaucoup de chemins, de préférences et de noms de repos sont hardcodés au contexte Neoteem/Raphael.

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
- **SQLite FTS5** : index du vault (`mcp-forge-brain/forge-brain.db`, ~8,9 Mo).
- **Batch Windows** : `install.bat`, `scripts/*.bat`, `mcp-forge-brain/start.bat`.
- **Outils CLI externes** (installés par `install.bat`) : Node.js, `defuddle-cli` (npm), `yt-dlp`, `fastmcp`, `pyyaml`, `ffmpeg` (optionnel), `faster-whisper` (optionnel), `deno` (optionnel).
- **MCP** : un seul serveur configuré, `forge-brain` (HTTP local port 8091).
- **Modèles** : `sonnet` (claude-sonnet-4-6) pour l'exécution, `opus` (claude-opus-4-7) pour le jugement, `haiku` (claude-haiku-4-5) pour le rapide (`CLAUDE.md` "Règles de génération absolues").

**Architecture globale (schéma textuel)**

```
claude-forge/
├── CLAUDE.md                  Contrat + doctrine (source d'autorité, ~190L)
├── .mcp.json                  Déclare le serveur MCP forge-brain (HTTP :8091)
├── install.bat                Setup des prérequis CLI (Windows)
├── README.md                  Doc historique (partiellement obsolète)
│
├── .claude/
│   ├── settings.json          Permissions + câblage des 9 hooks
│   ├── .skill-triggers.json   Map mots-clés → skill (lu par skill-activation.py)
│   ├── agents/                11 agents (.md)
│   ├── skills/                47 skills (dossiers SKILL.md + assets)
│   ├── hooks/                 9 hooks Python + tests/
│   ├── rules/                 10 rules (routing + doctrine, injectées via CLAUDE.md)
│   ├── scripts/               apply-edit.py, news-check.ps1
│   ├── agent-memory/          mémoire par agent (project scope)
│   └── secrets/               cookies x-read (gitignored)
│
├── mcp-forge-brain/           Serveur MCP maison (FastMCP + SQLite FTS5)
│   ├── src/                   server.py, database.py, indexer.py, watcher.py,
│   │                          git_sync.py, usage_log.py, tools/brain.py (21 outils)
│   ├── tests/                 9 fichiers de tests pytest
│   ├── config.yaml            vault_path, port, poids FTS
│   └── start.py / start.bat   Launcher
│
├── vault/claude-forge/        Le "cerveau" — vault Obsidian, 412 notes
│   (raw/ + wiki layers 00-Hub..07-Prompts + Knowledge + SCHEMA.md/index.md/log.md)
│
├── ia-lead-neoteem/           Plugin Cowork (7 skills Responsable IA)
├── scripts/                   .bat de tâches planifiées (cc-news, forge-review, vault-audit)
├── output/                    Livrables ad-hoc générés pour d'autres repos (gitignored)
└── data/                      Sortie twitter-api-client (gitignored)
```

**Principes de design structurants** (cités du repo)
1. **Compounding error-driven** : "après chaque erreur, ajouter ici ou mémoire ou vault Knowledge" (`CLAUDE.md` Workflow Boris). Le dossier `Knowledge/erreurs/` (34 notes) est le plus gros sous-dossier de Knowledge.
2. **Doctrine hooks = lint/security/scope, JAMAIS workflow** (pivot du 22 mai 2026, `CLAUDE.md` "Doctrine pivot 22 mai 2026"). Un hook ne doit pas forcer un workflow agentique (architect-first, TDD strict, gates de commit).
3. **Délégation forcée aux spécialistes** : on ne crée/modifie pas un SKILL.md / agent / CLAUDE.md à la main — un hook (`delegate-guard.py`) bloque et force le passage par skill-creator / agent-creator / claudemd-optimizer.
4. **MCP pour la donnée, Skills pour le savoir-faire** (`mcp-vs-skills-doctrine`). Le vault n'est accessible QUE par MCP forge-brain, jamais Grep/Read brut.
5. **Effort calibré par type de tâche** : `xhigh` réservé à l'exploration agentique profonde (repo-inspector), `high` partout ailleurs, `max` jamais en frontmatter (`CLAUDE.md`).
6. **Sonnet exécute, Opus juge** (`memory/feedback_all_opus.md`).
7. **5 lignes Karpathy en ouverture de tout CLAUDE.md** (`memory/feedback_5_lignes_karpathy_ouverture.md`).
8. **Pas de méta-commentaire dans les composants** : la justification ("Source: X", attributions d'auteur) vit dans le vault, pas dans le hook/agent/skill. Enforced par `meta-commentary-detector.py`.

**Diagramme de flux — lancement d'une session Claude Code dans claude-forge**

```
1. SessionStart
   ├─ session-reminder.py   → nettoie les markers de session précédente,
   │                          affiche un extrait de MEMORY.md
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
- OS : Windows (cible primaire — voir hooks `py` launcher, `install.bat`). Le repo est conçu Windows-first mais le code Python est portable.
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
::    via la skill /install-forge OU manuellement :
xcopy /E /I .claude %USERPROFILE%\.claude
```

Note : le README (`README.md:39`) propose `cp -r .claude/* ~/.claude/` — instruction Unix, à adapter sous Windows (`xcopy` ou la skill `install-forge` qui gère le diff). C'est l'une des zones où la doc est datée.

**Configuration post-install**
- Le serveur MCP démarre automatiquement à chaque SessionStart via `mcp-autostart.py` (port 8091). Aucune action manuelle.
- `.mcp.json` déclare le serveur : `{"forge-brain": {"type":"http","url":"http://localhost:8091/mcp"}}`.
- `mcp-forge-brain/config.yaml` configure `vault_path: vault/claude-forge`, `port: 8091`, poids FTS (`file_stem:10`, `aliases:8`, `content:1`), `auto_commit: false`.
- Secrets x-read : déposer `.claude/secrets/x-cookies.json` (gitignored) si on utilise la skill `x-read`.

**Vérifier que ça marche**
```bat
:: Le MCP répond ?
python -c "import socket; socket.create_connection(('127.0.0.1',8091),timeout=1); print('MCP OK')"

:: Cohérence interne du studio
::   → skill /self-check (descriptions une ligne, name=dossier, SKILL.md<500L, JSON valide)

:: Dashboard source vs installé
::   → skill /forge-status

:: Tests du serveur MCP
cd mcp-forge-brain && python -m pytest    :: 9 fichiers de tests
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

Tous les agents portent `memory: project`. Tableau de synthèse, puis détail.

| Agent | Fichier | Lignes | Model | Effort | Color | permissionMode | Skills frontmatter |
|---|---|---|---|---|---|---|---|
| agent-creator | `.claude/agents/agent-creator.md` | 101 | sonnet | high | pink | acceptEdits | cc-agents-ref, forge-brain, obsidian-markdown |
| claudemd-optimizer | `.claude/agents/claudemd-optimizer.md` | 99 | sonnet | high | pink | acceptEdits | cc-features-ref, forge-brain, obsidian-markdown |
| devils-advocate | `.claude/agents/devils-advocate.md` | 177 | opus | high | red | acceptEdits | forge-brain, obsidian-markdown |
| hook-creator | `.claude/agents/hook-creator.md` | 74 | sonnet | high | pink | acceptEdits | cc-hooks-ref, cc-features-ref, forge-brain, obsidian-markdown |
| outcomes-grader | `.claude/agents/outcomes-grader.md` | 93 | opus | high | yellow | plan | (aucune) |
| python-dev | `.claude/agents/python-dev.md` | 98 | sonnet | high | green | acceptEdits | python-ref, forge-brain, obsidian-markdown |
| repo-inspector | `.claude/agents/repo-inspector.md` | 299 | opus | xhigh | purple | plan | 10 skills (cc-advisor, cc-*-ref, cc-news, forge-brain, obsidian-markdown) |
| responsable-ia | `.claude/agents/responsable-ia.md` | 120 | opus | high | pink | acceptEdits | forge-brain, obsidian-markdown, craft-prompt, cc-prompt-ref |
| self-updater | `.claude/agents/self-updater.md` | 63 | sonnet | high | cyan | acceptEdits | cc-news, cc-features-ref, cc-hooks-ref, cc-agents-ref, cc-skills-ref, forge-brain, obsidian-markdown |
| skill-creator | `.claude/agents/skill-creator.md` | 117 | sonnet | high | pink | acceptEdits | cc-skills-ref, forge-brain, obsidian-markdown |
| vault-maintainer | `.claude/agents/vault-maintainer.md` | 177 | sonnet | high | cyan | acceptEdits | forge-brain, obsidian-markdown |

**agent-creator** (`.claude/agents/agent-creator.md`)
- Rôle : crée/modifie des subagents en posant 10 questions séquentielles puis valide une checklist de 9 points avant livraison.
- Déclenche : "crée un agent qui", "j'ai besoin d'un agent pour", recommandation de cc-advisor.
- Inputs : objectif, déclencheur, format de sortie, accès, modèle, effort, mémoire. Outputs : fichier agent `.md` (frontmatter complet + system prompt structuré).
- Dépendances : MCP forge-brain (`read_note` sur `comment-creer-agent`, `workflow-claude-code-optimal`) ; skill cc-agents-ref.
- Particularité : 3 interdictions absolues (jamais d'agent orchestrateur/CTO, jamais d'agent doc, jamais pré-créer les fichiers que l'agent générera). Note la dépréciation de `effort: max` depuis v2.1.91.
- Exemple : "Crée un agent qui vérifie les migrations avant chaque PR."

**claudemd-optimizer** (`.claude/agents/claudemd-optimizer.md`)
- Rôle : rédige/optimise un CLAUDE.md vers un template cible ~100-200 L, supprime le filler, convertit les règles ignorées en hooks.
- Déclenche : "optimise mon CLAUDE.md", "améliore mon CLAUDE.md", ou projet sans CLAUDE.md.
- Dépendances : MCP (`comment-ecrire-claudemd`, `erreur-meta-commentaires-composants`).
- Bloqué en édition directe par delegate-guard (CLAUDE.md est protégé).

**devils-advocate** (`.claude/agents/devils-advocate.md`)
- Rôle : critique adversariale d'un livrable majeur avant ship, verdict structuré (BLOCKING / WARNING / NITPICK) + sauvegarde dans `Knowledge/critiques/`.
- Déclenche : PROACTIVEMENT quand un livrable majeur est prêt (agent, skill, hook, archi). Conditionnel ciblé (pas systématique) — voir rule `devils-advocate-pipeline.md`.
- Inputs : texte complet de la proposition ou chemin fichier. Outputs : rapport 5 sections + note critique.
- Read-only : `disallowedTools: Write, Edit`. `maxTurns: 25`.
- Particularité vérifiée (`devils-advocate.md:62-82`) : pattern STOP + ESCALADE — ne peut pas appeler AskUserQuestion (limitation sub-agents, issue #18721), donc retourne un bloc `## AMBIGUÏTÉ DÉTECTÉE — escalade session principale` structuré (Contexte / Ambiguïté / Options / Recommandation / Question / État). Interdiction explicite du fallback Bash heredoc (cause du bug du 22 mai 2026, boucle quoting Windows).

**hook-creator** (`.claude/agents/hook-creator.md`)
- Rôle : crée/modifie des hooks en appliquant la doctrine 22 mai (lint/security/scope uniquement).
- Déclenche : besoin de formatage auto, notification, blocage. Suggère `/loop` ou `/schedule` si plus approprié qu'un hook.
- Dépendances : MCP (`comment-creer-hook`, `raisonnement-22mai-doctrine-vs-enforcement`).
- Particularité : impose chemin absolu Python Windows + matcher triplet `Write|Edit|MultiEdit` ; liste 6 anti-patterns (dont events inventés PreEdit/PostEdit).

**outcomes-grader** (`.claude/agents/outcomes-grader.md`)
- Rôle : note un livrable contre un RUBRIC.md, PASS/FAIL/PARTIAL par critère, score pondéré (MUST gate + SHOULD 65% + NICE 35%).
- Déclenche : utilisé EXCLUSIVEMENT par la skill `outcomes-test`.
- Le plus restrictif : `permissionMode: plan`, `disallowedTools: Write, Edit, Bash, Agent`. Aucune skill, aucun MCP — autonome et isolé.
- Règle d'or : "le doute → PARTIAL, pas PASS".

**python-dev** (`.claude/agents/python-dev.md`)
- Rôle : implémente du Python en TDD strict, tâche par tâche, avec vérification de régression.
- Déclenche : toute implémentation/debug/refactor Python.
- Particularité : seul agent avec un **hook inline** dans son frontmatter (PostToolUse `py_compile` sur chaque fichier écrit). Gotchas Windows (forward slashes Git Bash, `python -m pytest`, interdiction `python -c` multi-ligne car bloqué par hook global). Reporting `[TASK N DONE]` / `[PLAN COMPLETE]`.

**repo-inspector** (`.claude/agents/repo-inspector.md`)
- Rôle : audite / analyse / scanne un repo en 3 modes (`mode=audit` = `.claude/` vs canoniques ; `mode=analyze` = analyse complète + reco CC ; `mode=scan` = patterns du code applicatif).
- Déclenche : "audite mon repo", "analyse mon projet", "scan le code", "propose config CC", étapes de `methode-analyser-repo`.
- Le plus gros agent (299 L), seul en `effort: xhigh`, seul avec le tool `Agent` (orchestrateur effectif) + WebFetch/WebSearch. Read-only (`disallowedTools: Write, Edit`).
- Issu de la **fusion** de project-analyzer + project-auditor + codebase-scanner (supprimés le 2026-05-26, commit `8277279`). Voir section 12.

**responsable-ia** (`.claude/agents/responsable-ia.md`)
- Rôle : assiste Raphael dans tous ses actes de Lead IA Neoteem (CODIR/6-pager, roadmap RICE/WSJF/OKR, AI Act/FRIA, 1:1, build vs buy, archi RAG/agents Loji, tickets Jira).
- Déclenche : 17 déclencheurs explicites ("prépare CODIR", "6-pager", "priorise", "OKR", "AI Act", "FRIA", "build vs buy", "agent Loji"…).
- Particularité : ancré dans le contexte Neoteem ; catalogue de 25 tâches × framework × wikilink vault ; posture franc-parler (détecte AI Act Annexe III, PII sans RGPD, promesse impossible). Sources : `2-Casquettes/responsable-ia/` + plugin Cowork `ia-lead-neoteem`. C'est l'agent "métier" du corpus (les autres sont méta-CC).

**self-updater** (`.claude/agents/self-updater.md`)
- Rôle : détecte les nouvelles features CC via cc-news et met à jour les skills de référence `cc-*-ref` en citant la source.
- Déclenche : PROACTIVEMENT après que cc-news trouve des changements. Agent le plus simple (63 L).
- Règle : ne modifie QUE les skills cc-*, ajoute sans supprimer, "en cas de doute → marquer non confirmée".

**skill-creator** (`.claude/agents/skill-creator.md`)
- Rôle : crée/optimise des skills (9 questions + checklist 10 points), impose description directive "ALWAYS invoke when…" et section Gotchas.
- Déclenche : "crée une skill", "optimise cette skill", "j'ai besoin d'une commande /X".
- Dépendances : MCP (`comment-creer-skill`, `mcp-vs-skills-doctrine`). Donnée empirique citée : "73% des skills passives ne se déclenchent jamais".

**vault-maintainer** (`.claude/agents/vault-maintainer.md`)
- Rôle : maintient la qualité des notes vault après modification (7 champs frontmatter, ≥4 aliases, wikilinks, MOC, backlinks).
- Déclenche : PROACTIVEMENT après modifs vault, capitalisation cc-news, création de note.
- Input : liste de chemins OU contexte trigger (fallback `git diff`). Scope strict : jamais le vault entier. Ne corrige PAS l'orphelinat automatiquement (risque de lien hors contexte → décision laissée à Raphael).

### Skills (47)

Conventions : `user-invokable: true` = slash command ; `false` = référence passive non invocable manuellement (chargée par description) ; `disable-model-invocation: true` = slash pure sans inférence modèle. Toutes dans `.claude/skills/<nom>/SKILL.md`.

**Skills de référence Claude Code (knowledge bases, `user-invokable: false`)**
| Skill | Lignes | Rôle | Assets |
|---|---|---|---|
| cc-agents-ref | 117 | Format YAML agent complet | — |
| cc-skills-ref | 154 | Format YAML skill (9 catégories Thariq, $ARGUMENTS, !backtick) | `references/anthropic-skill-patterns.md`, `complete-guide.pdf`, `complete-guide-summary.md` |
| cc-hooks-ref | 216 | 29 events, exit codes, hookSpecificOutput | — |
| cc-features-ref | 251 | Features CC 2026 (loop, schedule, worktrees, Agent Teams) | — |
| cc-cowork-ref | 298 | Cowork / Dispatch / Agent Teams / plugins | — |
| cc-prompt-ref | 197 | Prompt engineering pour composants CC | — |
| python-ref | 183 | Python 3.11+, pytest, FastMCP, FTS5 | — |

**Skills slash command (`user-invokable: true`)**
| Skill | Lignes | Rôle | Assets |
|---|---|---|---|
| analyze-project | 91 | `/analyze-project <path>` — analyse + propose composants CC | — |
| cc-advisor | 96 | Recommande le bon composant CC pour un besoin flou | `references/mcp-catalog.md` |
| cc-news | 159 | Veille IA/CC, orchestre des agents par domaine, capitalise vault | `references/domain-*.md` (7 domaines) + `format-reponse.md` |
| config-guardian | 98 | Audit drift multi-repo vs baseline | `references/baseline-rules.md`, `scripts/scan.py` |
| craft-prompt | 148 | Génère un prompt optimisé (Claude/Gemini/tout LLM) | `references/techniques-{claude,gemini,universelles}.md` |
| done | 303 | Métacognition fin de session → vault + mémoire + context-actuel | — |
| evolve | 227 | Propose évolutions produit/archi d'un projet (3 buckets) | — |
| expand | 48 | Transforme un prompt brut en spec précise | — |
| forge-review | 255 | Review stratégique mensuelle KILL/EVOLVE/KEEP/MISSING | `references/baseline.md` |
| forge-status | 42 | Dashboard source vs installé (`disable-model-invocation`) | — |
| git-multi-repo | 57 | Impose `git -C <path>` cross-repo | — |
| install-forge | 50 | Copie `.claude/*` → `~/.claude/` (`disable-model-invocation`) | — |
| notes | 134 | `/notes <slug>` — init notes d'implémentation Thariq | — |
| outcomes-test | 138 | Évalue un livrable vs RUBRIC.md via grader dédié | `references/rubric-templates.md` |
| pivot-check | 131 | Détecte drift doctrinal Type 1 post-correction canonique | — |
| python-script-refactor-masse | 77 | Template refactor >10 fichiers via regex | — |
| reasoning-cache | 186 | Capture une chaîne de raisonnement réussie en note vault | — |
| recap | 180 | Snapshot contexte projet <10 s | — |
| self-check | 45 | Valide cohérence interne forge (`disable-model-invocation`) | — |
| skill-evolve | 245 | Analyse+propose optims d'une skill (4 axes) | `references/{scoring-rubric,analyse-axes,cross-pollination-patterns}.md` |
| spec | 201 | Ticket/idée → dossier `TODO/feature-X/` (s'arrête au gate) | `references/{interview-bank,output-templates,contradiction-prompt,decompose-waves,cross-validation,stack-conventions}.md` |
| vault-audit | 163 | Audit qualité notes vault + fix déterministe | `scripts/{audit,fix}.py` |
| watch | 205 | Transcrit/analyse vidéos YouTube (yt-dlp + Whisper fallback) | `scripts/clean_subs.py` |
| auditor-empirical-verify | 59 | Checklist vérif empirique post-dispatch sub-agent | — |
| windows-hooks-cross-machine | 54 | Portabilité hooks Windows (`py` launcher, `${CLAUDE_PROJECT_DIR}`) | — |
| x-read | 134 | Lit X/Twitter via cookies, formate vault-ready | `reader.py`, `references/cookie-setup.md`, `install.{ps1,sh}`, `requirements.txt`, `downloads/` |

**Skills auto-trigger (champ `user-invokable` absent — chargées par description)**
| Skill | Lignes | Rôle | Assets |
|---|---|---|---|
| agentshield-like-scanner | 121 | Pipeline audit sécu red/blue/auditor (3 sous-agents Opus) | — |
| arxiv-verification | 56 | Vérifie citations arXiv (format YYMM, swap URL, venues) | — |
| audit-thematique-clusters | 126 | Audit multi-composants par clusters thématiques | — |
| configure-claude-desktop | 87 | Génère profil Claude Desktop pour un membre Neoteem | `references/best-practices.md` |
| cross-repo-propagation | 50 | Propage une décision naming/structure aux autres repos | — |
| da-blocking-arbitrage | 92 | Arbitrage obligatoire si verdict DA BLOCKING ≥ 1 | — |
| defuddle | 42 | Extrait markdown propre d'une page web (CLI Defuddle) | — |
| forge-brain | 194 | Interface vault via MCP (21 outils, templates, règles) | `scripts/obsidian-cli.sh` |
| mcp-brief-then-direct | 72 | Contourne limitations skills frontmatter sub-agents | — |
| methode-pivoter-doctrine | 99 | Checklist 5 étapes pivot doctrinal anti-drift | — |
| web-search-canonical-source | 93 | Hiérarchie de sources canoniques | — |

**Skills externes / upstream Obsidian (adaptées, exemptées de delegate-guard)**
| Skill | Lignes | Origine | Assets |
|---|---|---|---|
| json-canvas | 244 | Spec jsoncanvas.org 1.0 / obsidianmd | (référence EXAMPLES.md non présente) |
| obsidian-markdown | 213 | help.obsidian.md + surcouche MCP forge | `references/{CALLOUTS,EMBEDS,PROPERTIES}.md` |
| obsidian-bases | 376 | help.obsidian.md/bases | `references/{FUNCTIONS_REFERENCE,COMPLETE_EXAMPLES}.md` |

Ces 3 + `defuddle` sont listées dans `EXEMPT_SKILL_DIRS` du hook delegate-guard (copies read-only, non protégées). Aucune ne porte de champ `author` ni de credit kepano explicite dans le frontmatter.

**Exemples d'usage concrets**
- `/recap` au début d'une session → snapshot git + vault + mémoire.
- "Crée une skill /commit" → skill-creator pose 9 questions, génère le dossier.
- `/forge-review` → verdict KILL/EVOLVE/KEEP/MISSING sur le setup.
- Partage d'une URL YouTube → skill `watch` transcrit et résume.

### Hooks (9)

Tous en Python, câblés dans `.claude/settings.json`, invoqués via `py "${CLAUDE_PROJECT_DIR}/.claude/hooks/<nom>.py"`. Tous fail-open (exit 0 sur erreur de parsing). Tests : `.claude/hooks/tests/test_meta_commentary_detector.py`.

**security-guard.py** — PreToolUse `Bash`
- Intercepte les commandes shell. Bloque (exit 2) : `rm -rf /` / `rm -fr /`, `git push --force` / `-f`, `git reset --hard` sans cible, `git clean -f`.
- 6 patterns regex. Effet : refuse l'exécution des commandes destructives. Code complet ~30 L, lu intégralement.

**delegate-guard.py** — PreToolUse `Edit|Write|MultiEdit`
- Intercepte les éditions de fichiers protégés DANS claude-forge uniquement : `SKILL.md` → skill-creator, `CLAUDE.md` → claudemd-optimizer, `.claude/agents/*.md` → agent-creator.
- Bypass (premier match gagne) : fichier hors forge ; `agent_type`/`agent_id` = spécialiste ; `CLAUDE_AGENT` env var (legacy dead code) ; parsing du transcript révélant un sous-agent actif ; edit < 20 chars (typo pass-through, warning) ; toute erreur (fail-open).
- `EXEMPT_SKILL_DIRS` : json-canvas, defuddle, obsidian-cli, obsidian-markdown, obsidian-bases.
- Effet : exit 2 + message "BLOCKED: Direct edit of … Required agent: …". Debug log dans `<tempdir>/delegate-guard-debug.log`.

**meta-commentary-detector.py** — PreToolUse `Write|Edit|MultiEdit`
- Intercepte le contenu écrit dans les composants forge (CLAUDE.md, agents/, skills/SKILL.md, rules/, hooks/). Exclut vault/, Knowledge/, references/, RECAP.md, CHANGELOG.md.
- Bloque 11 patterns de méta-commentaire : tradeoff en italique après une puce, `Source:` en texte libre, `Cf doctrine`, `D'après`, `= tip #N Nom`, `— Prénom Nom` en fin de ligne, citations `(arXiv:…)` / `(UCL …)`, justification historique `(depuis <date>)`, `(validé N mois)`.
- Applique l'édition en mémoire avant scan (Write/Edit/MultiEdit). Frontmatter YAML et wikilinks nus exemptés. Self-test intégré (`--self-test`).
- Effet : exit 2 + "BLOQUÉ: meta-commentaire interdit … Doctrine: voir vault [[erreur-meta-commentaires-composants]]". Le plus sophistiqué des hooks (~470 L).

**session-health.py** — UserPromptSubmit
- Compteur de tours scopé par `session_id`. Tours 1-2 : tip /recap. Tous les 20 : rappel /compact ou /clear (pattern Document & Clear). Tous les 40 : rappel urgent. Sortie via `additionalContext`. Non bloquant.

**skill-activation.py** — UserPromptSubmit
- Matche le prompt (word-boundary regex) vs `.claude/.skill-triggers.json`. Injecte un `additionalContext` recommandant la/les skill(s) pertinente(s). Bypass préfixes `* / # !`. Tracker de session pour ne pas re-recommander. Non bloquant.

**session-reminder.py** — SessionStart
- Nettoie les markers de la session précédente (learning-reminded, proactivity-reminded, devil-advocate-*, vault-queried, skill-recommendations-session, vault-write-count). Affiche un extrait (500 chars) du `MEMORY.md` le plus récent.

**mcp-autostart.py** — SessionStart (async)
- Teste le port 8091 (socket). Si mort, lance `mcp-forge-brain/start.py` en process détaché Windows (`DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`). Toujours exit 0.

**learning-reminder.py** — Stop (`once: true`)
- 1×/session : bloque le Stop (`decision: block`) avec un rappel en 5 points (mémoire projet, vault Knowledge, section Apprentissage des skills, CLAUDE.md, /reasoning-cache). Marker dans `%TEMP%` empêche la boucle. Nettoyé par session-reminder.

**proactivity-reminder.py** — Stop (`once: true`)
- 1×/session si ≥5 tours : bloque le Stop avec "as-tu fait une proposition Jarvis ?". Garde `stop_hook_active` contre la boucle infinie.

Note : le hook inline `py_compile` de python-dev (frontmatter de l'agent, pas dans settings.json) est un 10e point d'interception, scopé à cet agent.

### MCP (1 serveur configuré)

**forge-brain** — `http://localhost:8091/mcp` (`.mcp.json`)
- Serveur HTTP local, code maison dans `mcp-forge-brain/` (FastMCP + SQLite FTS5). Self-contained (2 deps : fastmcp, pyyaml). Auto-start au SessionStart.
- Backend : `forge-brain.db` (SQLite FTS5, poids BM25 file_stem:10 / aliases:8 / content:1). Watcher (`watcher.py`) ré-indexe le vault toutes les 30 s. `git_sync.py` présent mais `auto_commit: false`.
- **21 outils exposés** (recensés dans `register_tools`, `mcp-forge-brain/src/tools/brain.py`) :
  - Lecture : `search_brain`, `read_note`, `read_note_by_path`, `read_section`, `read_note_resolved`, `get_backlinks`, `get_tags`, `get_property`, `list_notes`, `vault_stats`, `find_by_property`, `usage_stats`, `lint_vault`
  - Écriture : `create_note`, `append_note`, `update_note`, `insert_section`, `update_property`, `bulk_update_property`
  - Move/Delete : `move_note` (réécrit les wikilinks), `delete_note` (refuse si backlinks > 0 sauf force)
- Auth/credentials : aucun (HTTP localhost, pas d'authentification — confiance machine locale).
- Discordance documentaire à corriger : `CLAUDE.md` dit "21 outils", `forge-brain-proactive.md` dit "19 outils v1.3". Le code en expose 21 — c'est le chiffre exact.

Note : d'autres serveurs MCP (langfuse, Atlassian, neoteem-brain) apparaissent comme outils déférés dans l'environnement de session, mais ne sont PAS déclarés dans le `.mcp.json` de claude-forge — ils viennent de la config Claude Code globale / d'autres projets, pas de forge.

---

## 6. Vault interne (forge-brain)

**Stats** : 412 notes, 225 tags, 2691 wikilinks, 2433 aliases (≈5,9 aliases/note). Pattern Karpathy LLM Wiki (3 layers).

**Structure (notes par dossier)**

| Dossier | Notes | Contenu |
|---|---|---|
| 04-Techniques | 109 | claude-code/, agents/, rag/, prompt-engineering/, fine-tuning/, patterns/, context-engineering/ |
| Knowledge | 81 | erreurs/(34), critiques/(23), syntheses/(10), raisonnements/(7), explorations/, questions/, tests/, evolutions/, reviews/ |
| 05-Leaders | 80 | claude-code/, agents/, rag/, fine-tuning/, prompt/, industrie/ |
| 2-Casquettes | 41 | responsable-ia/ (12 sous-dossiers) + Famille, Gaming, Raphael-Picard |
| 01-Claude | 30 | Code/features/, Code/changelog/, Code/best-practices/, Cowork/ |
| 1-Projets | 21 | Claude-Forge/, Neoteem/ (ia_back, neo_ia, neoteem-brain, bdd), lojii/ |
| 00-Hub | 8 | Home.md + 7 MOC |
| 06-Industrie | 8 | News (événements, funding) |
| raw | 8 | Sources immuables (2026-05-22-chantier/) |
| 03-Modeles | 7 | anthropic/, openai/, google/, xai/ |
| 07-Prompts | 7 | system-prompts/, techniques/ |
| 02-Concurrents | 5 | cursor/, copilot/, openai/, google/, xai/ |
| 0-Inbox | 1 | Capture temporaire (context-actuel.md) |

**Convention de nommage**
Deux régimes : notes de référence/leaders en **Title Case avec espaces** (`Boris Cherny.md`, `RAG.md`, `Opus 4.7.md`), notes canoniques et Knowledge en **kebab-case**. Préfixes : `comment-creer-*`, `comment-ecrire-*`, `methode-*`, `pattern-*`, `erreur-*`, `critique-YYYY-MM-DD-*`, `raisonnement-*`, `_index.md` (un par sous-dossier Knowledge).

**Top 15 notes les plus importantes** (résumés du contenu réel, via lecture MCP)
1. **methode-analyser-repo** — META 6 étapes pour transformer un repo en config CC. Cœur = ordre canonique A→B→C→D→E (analyser le réel → lire canoniques en entier → croiser → plan d'écarts → exécuter).
2. **comment-ecrire-claudemd** — target <200 L, 5 lignes Karpathy en ouverture, test "Would removing this cause mistakes?", 5 anti-patterns Anthropic.
3. **comment-creer-skill** — 9 catégories Thariq, progressive disclosure, description <250 chars, SKILL.md <500 L.
4. **comment-creer-agent** — "Agent = Model + Harness", split Sonnet/Opus, 8 couleurs, pattern 2-agent.
5. **comment-creer-hook** — 29 events, exit 0/1/2, "if a rule must hold every time, make it a hook", lint/security/scope OUI workflow NON.
6. **workflow-claude-code-optimal** — 7 pratiques (Routines Boris, Advisor Strategy, leaf nodes, multi-clauding, /loop, Sonnet/Opus split, compounding).
7. **mcp-vs-skills-doctrine** — "MCP connects data; Skills teach how-to", lethal trifecta (Willison).
8. **pattern-vault-llm-karpathy** — 3 layers (raw/wiki/schema), 3 ops (Ingest/Query/Lint), index.md + log.md obligatoires.
9. **raisonnement-22mai-doctrine-vs-enforcement** — pivot doctrinal : suppression de 7 hooks workflow ×2 repos. Hooks = lint/test/security uniquement.
10. **mcp-vault-llm-design** — design d'un MCP servant un vault à un LLM (9 ops, base forge-brain v1.3).
11. **methode-pivoter-doctrine** — checklist 5 étapes anti-drift résiduel.
12. **Home** (00-Hub) — porte d'entrée vault, pointe vers index/SCHEMA/log + 9 canoniques + 7 MOC.
13. **comparaison-skill-anthropic-claude-code-setup** — référence comparative skill Anthropic vs forge.
14. **anti-reentrance-sub-agents-pattern-escalade** — pattern STOP+ESCALADE pour sous-agents.
15. **trail-of-bits-config** — setup entreprise sécu publique (Stop hook anti-rationalization).

**Comment Claude lit le vault** : EXCLUSIVEMENT via MCP forge-brain (21 outils, `search_brain` / `read_note` / etc.). Grep/Read/Glob brut sur le vault sont interdits (`forge-brain-proactive.md`). La skill `forge-brain` documente la matrice de décision des outils.

**Comment Claude écrit le vault** : via MCP (`create_note`, `append_note`, `insert_section`, `update_note`, `update_property`, `bulk_update_property`), avec la skill `obsidian-markdown` pour la syntaxe. Jamais de Bash heredoc (cause documentée du bug du 22 mai).

**Qui décide d'écrire et quand** : la session principale et certains agents (devils-advocate → critiques, vault-maintainer → corrections, responsable-ia → casquette). Déclencheurs : après cc-news (capitalisation), après une erreur significative (`Knowledge/erreurs/`), après un raisonnement multi-étapes (`/reasoning-cache`), en fin de session (`/done`).

**Fréquence d'écriture observée (git log du vault)** : les fichiers vault les plus modifiés sont `CHANGELOG.md` (40 modifs), `0-Inbox/context-actuel.md` (37), `00-Hub/MOC-Techniques.md` (21), `00-Hub/MOC-Claude-Code.md` (13), `log.md` (12). Le vault est écrit à presque chaque session de travail substantielle.

**Patterns capitalisés (par thème)**
- Claude Code (dominant) : features, changelog, best-practices, doctrine 2026 (`#doctrine/2026`).
- Techniques IA : agents (52 tags), RAG (37), prompt-engineering (32), fine-tuning (28), context-engineering.
- Leaders : 80 fiches (Karpathy, Boris Cherny, Thariq, Amanda Askell, Willison, Hashimoto).
- Apprentissage/compounding : erreurs (34), critiques (23), synthèses (10), raisonnements (7).
- Casquette responsable-ia : management, communication, réunions, priorisation, gouvernance (BLUF, OKR, RICE, AI Act, RGPD).
- Sécurité : lethal trifecta, prompt-armor, agents-securite.

---

## 7. Usage réel

**Workflows typiques**

1. *Mardi matin, reprise de contexte.* `/recap` → snapshot git + vault stats + dernière mémoire + date cc-news + suggestion de contexte. En 10 s, Claude sait où on en est.

2. *"J'ai besoin d'automatiser X" (besoin flou).* La session principale invoque `cc-advisor` qui analyse le besoin et recommande un composant (hook ? skill ? agent ? rule ?), puis dispatche le créateur approprié.

3. *Création d'un composant.* "Crée un agent qui audite mon codebase" → `agent-creator` (questions + checklist) → optionnellement `devils-advocate` si livrable majeur → présentation à Raphael. L'édition directe est bloquée par `delegate-guard.py`.

4. *Analyse d'un repo externe.* "Analyse neofront et propose une config CC" → `repo-inspector` (mode analyze/scan/audit) suit la méthode 6 étapes `methode-analyser-repo` : scan archi + code réel + audit `.claude/` en parallèle.

5. *Fin de session, capitalisation.* `/done` → métacognition (décisions, faits, préférences, erreurs) → mise à jour mémoire + vault + `context-actuel.md`. Renforcé par le hook `learning-reminder.py` qui bloque le Stop si rien n'a été capitalisé.

6. *Veille.* `cc-news` orchestre des agents par domaine (CC, RAG, agents, fine-tuning, concurrents, prompt) et capitalise les découvertes en notes atomiques ; `self-updater` met à jour les skills `cc-*-ref` si une feature CC change.

**Commandes/skills les plus fréquentes** (git log comme proxy de l'activité) : cc-news (20 modifs du SKILL), forge-brain (10), cc-hooks-ref (12), cc-features-ref (11), cc-skills-ref (10). Côté agents : les créateurs (skill-creator, agent-creator, claudemd-optimizer, hook-creator) et devils-advocate sont les plus retouchés.

**Combinaisons agent + skill les plus utiles**
- `cc-advisor` (skill) → `agent-creator`/`skill-creator`/`hook-creator` (agents) → `devils-advocate` → `da-blocking-arbitrage` (skill).
- `repo-inspector` (mode analyze) → délégation aux créateurs pour appliquer les fixes.
- `spec` (skill) → décomposition en vagues → `python-dev` (agent) en TDD.

**Anti-patterns à éviter (du repo)**
- Éditer directement un SKILL.md / agent / CLAUDE.md (bloqué par hook ; `delegate-to-specialists.md`).
- Utiliser Grep/Read brut sur le vault au lieu du MCP forge-brain.
- Créer un agent orchestrateur/CTO (`memory/feedback_no_cto_agent.md`).
- Mettre du routing dans CLAUDE.md plutôt que dans `.claude/rules/`.
- Sessions fourre-tout multi-chantiers (`memory/feedback_session_multi_chantiers.md` : "JAMAIS 4+ chantiers indépendants").
- Bash heredoc pour écrire des notes vault (boucle quoting Windows).
- Hooks de workflow agentique (architect-first, TDD strict) — interdits par la doctrine 22 mai.

---

## 8. Self-improvement

**Comment claude-forge apprend de ses sessions**
La boucle de feedback est explicite et outillée :
1. **Détection** : hook `learning-reminder.py` (Stop) force la question "as-tu appris quelque chose ?" 1×/session.
2. **Classification** (frontière mémoire ↔ vault, `memory-discipline.md`) : feedback relation/préférence → `memory/feedback_*` / `user_*` ; référence technique → `memory/reference_*` ou vault ; erreur → les DEUX ; savoir réutilisable → vault.
3. **Capitalisation** : `/done` (métacognition fin de session), `/reasoning-cache` (raisonnement multi-étapes), `devils-advocate` (→ `Knowledge/critiques/`), `cc-news` (→ notes atomiques), `/skill-evolve` (→ `Knowledge/evolutions/`), `/forge-review` (→ `Knowledge/reviews/`).
4. **Application** : la mémoire (`MEMORY.md`, ~166 entrées de feedback) est rechargée à chaque session (hook `session-reminder.py` + injection MEMORY.md), les canoniques vault sont lus par les créateurs/analyseurs.

**Mécanismes de capitalisation en place**
- `MEMORY.md` + fichiers `feedback_*.md` / `project_*.md` / `reference_*.md` (mémoire Claude Code native).
- Vault `Knowledge/` (erreurs, critiques, raisonnements, synthèses, tests, evolutions, reviews).
- CLAUDE.md (section Gotchas — erreurs comportementales) qui "DOIT évoluer".
- Rules `.claude/rules/` (doctrine de routing et de comportement).

**Patterns capitalisés à ce jour (échantillon de MEMORY.md)**
- Workflow : spec→forge→Jira, refactor de masse par script Python, git -C cross-repo, quartet d'analyse multi-repo, fix en 3 vagues parallèles.
- Doctrine : hooks lint/sécu/scope (pivot 22 mai), DA conditionnel, advisor avant travail, Sonnet exécute/Opus juge, effort calibré.
- Gotchas techniques : MultiEdit matcher blind spot, regex lookahead greedy trap, Python path Windows, AskUserQuestion impossible en sous-agent, classifier bloque self-modification.
- Méta-relation : posture Jarvis, franc-parler, never pure executor, anti-glissement exécutant en sessions longues.

**Ce qui déclenche une mise à jour**
- Vault : recherche web/cc-news, erreur significative, raisonnement multi-étapes, décision majeure, modification de note (→ vault-maintainer).
- Skill : `/skill-evolve [nom]` ou sweep `/skill-evolve all`.
- Agent : nouveau besoin via agent-creator, ou correction après audit.
- CLAUDE.md : après chaque erreur comportementale, audit mensuel via `/forge-review`.

---

## 9. Portabilité

**Entre machines (Windows / Linux / Mac)**
- Cible primaire **Windows**. Les hooks utilisent le `py` launcher (jamais un chemin Python en dur — `windows-hooks-cross-machine.md`) et `${CLAUDE_PROJECT_DIR}` (jamais de chemin absolu utilisateur). C'est ce qui les rend portables entre postes Windows.
- Le code Python (hooks + MCP) est OS-agnostique sauf `mcp-autostart.py` qui utilise des flags Windows (`DETACHED_PROCESS`…) — à adapter pour Linux/Mac.
- `install.bat` et les `scripts/*.bat` sont Windows-only ; il faudrait des équivalents `.sh` pour Unix (la skill x-read a déjà `install.ps1` + `install.sh`).

**Entre missions (Neoteem, ArcelorMittal, futurs clients)**
- **Portable** : les agents/skills méta-CC (créateurs, références cc-*, vault, hooks de garde), la doctrine canonique du vault, les patterns de workflow.
- **Non portable tel quel** : tout ce qui est ancré Neoteem — agent `responsable-ia`, plugin `ia-lead-neoteem`, skills `config-guardian` / `cross-repo-propagation` (noms de repos hardcodés : ia_back, neo_ia, neoteem-brain, lojii), `configure-claude-desktop`, les notes `1-Projets/Neoteem/` et `2-Casquettes/`.
- Le `output/` contient des livrables ad-hoc générés pour d'autres repos (claude-switcher, feedback-triage-plugin, support-lojii-plugin) — illustration que forge sert de "fabrique" de config pour l'écosystème Neoteem.

**Stratégie de versioning** : git, branche `main`, versioning sémantique manuel dans l'en-tête de CLAUDE.md (v3.3). Pas de tags git détectés, pas de releases GitHub (l'orga Team bloque GitHub cloud — `memory/feedback_no_github_cloud.md`).

**Mécanisme de sync entre instances** : déploiement par copie `.claude/* → ~/.claude/` (skill `install-forge`), comparaison via `/forge-status`. `mcp-forge-brain/git_sync.py` existe mais `auto_commit: false` (pas de sync automatique du vault). Une seule instance réelle (poste de Raphael).

---

## 10. Configuration & sécurité

**Permissions `.claude/settings.json` — allow** (pas de bloc `deny` ni `ask` dans le fichier ; les interdits vivent dans CLAUDE.md) :
- `Read`, `Write`, `Edit`
- `Bash(git *)`, `Bash(git -C *)`, `Bash(ls *)`, `Bash(taskkill *),` (la virgule finale est une coquille)
- `Edit(.claude/agents/**)`, `Edit(.claude/skills/**)`, `Edit(./**)`
- `MultiEdit(.claude/agents/**)`, `MultiEdit(.claude/skills/**)`, `MultiEdit(./**)`

Le CLAUDE.md précise le périmètre réel : permissions cross-repo TOTALES (Read/Write/Edit/Bash/MCP partout), **INTERDIT sauf demande explicite** : `rm -rf`, `git branch -D`, suppression de branches, force push sur main. Ces interdits sont partiellement enforced par `security-guard.py` (rm -rf /, push --force, reset --hard, clean -f).

**env** : `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50"` (compaction à 50% du contexte), `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` (Agent Teams activé).

**Modèles et stratégie** : Sonnet (claude-sonnet-4-6) pour l'exécution, Opus (claude-opus-4-7) pour le jugement, Haiku pour le rapide. `effort: high` par défaut, `xhigh` réservé à repo-inspector, `max` jamais en frontmatter. Les agents Opus : devils-advocate, outcomes-grader, repo-inspector, responsable-ia.

**Sandbox / containment** : Windows direct, pas de WSL ni devcontainer. Le serveur MCP tourne en local (localhost:8091). Les hooks fail-open (ne bloquent jamais la session sur erreur). `permissionMode: acceptEdits` sur la plupart des agents, `plan` sur les read-only (outcomes-grader, repo-inspector).

**Secrets management** : cookies x-read dans `.claude/secrets/x-cookies.json` (gitignored, `.gitignore:22-24`). `data/` (sortie twitter) gitignored. Pas de credentials en clair dans `.mcp.json` (le MCP local n'a pas d'auth). Règle `memory/feedback_secret_in_mcp_json.md` : "JAMAIS credentials en clair dans .mcp.json/configs versionnés".

**Risques résiduels identifiés**
- Permissions très larges (`Bash(git *)` + Write/Edit cross-repo) — repose sur la discipline et `security-guard.py`, dont la couverture est limitée à 6 patterns.
- MCP forge-brain sans authentification (acceptable car localhost machine personnelle, mais tout process local peut l'interroger).
- `delegate-guard.py` a plusieurs voies de bypass (typo < 20 chars, fail-open sur erreur) — protection "best effort", pas étanche.
- La coquille `Bash(taskkill *),` (virgule) peut rendre la règle inopérante selon le parsing.

---

## 11. Points forts

- **Compounding outillé, pas seulement déclaré** : la boucle erreur→capitalisation→rechargement est matérialisée par des hooks (learning-reminder), des skills (/done, /reasoning-cache) et un vault interrogeable par MCP. Peu de setups CC vont aussi loin.
- **Délégation forcée par construction** : `delegate-guard.py` empêche physiquement la dérive "j'édite vite à la main et c'est non conforme" — réponse directe à une erreur réelle documentée (2026-04-26).
- **Doctrine versionnée et datée** : le pivot 22 mai (hooks ≠ workflow) est tracé dans le vault (`raisonnement-22mai-doctrine-vs-enforcement`) avec une méthode pour pivoter sans drift résiduel (`methode-pivoter-doctrine` + skill `pivot-check`). La doctrine est un artefact de premier ordre, pas un implicite.
- **MCP maison optimisé pour LLM** : 21 outils pensés pour un agent (read_section économise 30× les tokens, find_by_property = Dataview, bulk_update évite les round-trips), avec 9 fichiers de tests pytest. C'est de l'ingénierie réelle, pas un wrapper trivial.
- **Méta-commentary-detector** : enforcement automatique du principe "le pourquoi vit dans le vault" — pattern peu courant et cohérent avec la séparation composant/doctrine.
- **Séquence canonique A→B→C→D→E** : tout créateur/analyseur doit observer le réel avant de lire la doctrine avant de prescrire — anti-biais de perception structuré.

---

## 12. Points faibles / zones floues

- **[RÉSOLU 2026-05-26, commit `8277279` + fix conformité] Drift documentaire — agents fantômes** : `project-analyzer`, `project-auditor` et `codebase-scanner` ont été fusionnés dans `repo-inspector` (modes analyze/audit/scan). Les rules `comportement-proactif.md`, `sequence-canonique-modification.md`, `vault-consultation-protocol.md` et `forge-review/references/baseline.md` ont été corrigées ; les dossiers `agent-memory/project-analyzer/` et `project-auditor/` migrés vers `repo-inspector/`. Plus aucune référence aux agents supprimés dans les fichiers vivants.
- **[RÉSOLU 2026-05-26] Discordance du nombre d'outils MCP** : `forge-brain-proactive.md` aligné sur 21 outils (cohérent avec CLAUDE.md et le code).
- **[RÉSOLU 2026-05-26] README obsolète** : réécrit — 11 agents / 47 skills, install Windows (xcopy), pointeur vers ce self-portrait, plus aucune mention de `project-analyzer` ni `/batch`.
- **[RÉSOLU 2026-05-27, P2.6] Skills `cc-*-ref` en `user-invokable: false`** : décision = MAINTENIR. Investigation : les 6 skills `cc-*-ref` (+ `python-ref`) ne sont PAS orphelines — chacune est référencée dans 2 à 4 agents créateurs (agent-creator, skill-creator, hook-creator, claudemd-optimizer, self-updater, repo-inspector) à la fois en frontmatter `skills:` ET dans le body avec instruction d'usage, plus auto-trigger via descriptions fortes ("ALWAYS load when…"). `user-invokable: false` est le réglage canonique correct pour une bibliothèque de référence chargée par un parent — les basculer en `true` serait une régression (l'utilisateur ne tape pas `/cc-agents-ref`). Doctrine déjà capitalisée dans `comment-creer-skill` + `mcp-vs-skills-doctrine`.
- **[RÉSOLU 2026-05-27, P1.4] Asset référencé manquant** : `json-canvas/SKILL.md` L239 référençait `references/EXAMPLES.md`, absent de notre copie. Restauré verbatim depuis l'upstream `kepano/obsidian-skills` (6476 octets, identique) — pas de fabrication locale.
- **[RÉSOLU 2026-05-27, P0.2] Coquille permissions** : virgule parasite `Bash(taskkill *),` retirée dans settings.json.
- **[RÉSOLU 2026-05-27, P0.1] Incohérence frontmatter devils-advocate** : le body affirmait `effort: xhigh` contre `effort: high` en frontmatter. Lignes de body supprimées (le frontmatter fait foi). Règle "frontmatter vs body : alignement obligatoire" capitalisée dans `comment-creer-agent`.
- **[FAUX POSITIF — non reproduit 2026-05-27] `.pyc` versionnés** : `git ls-files` ne retourne aucun `.pyc`. Les fichiers `__pycache__` du snapshot initial étaient déjà dé-trackés (staged `D`) puis poussés dans `2cef483`. Le `.gitignore` couvre `__pycache__/` et `*.pyc`. Rien à faire.
- **Dépendances minimes, pas obsolètes** : fastmcp>=2.0, pyyaml>=6.0 — récentes. Pas de dette de dépendances détectée.
- **[RÉSOLU 2026-05-27, P3.7] `data/` et `output/`** : les deux sont gitignorés (`.gitignore` L19, L26) — **jetables/régénérables, jamais versionnés**. `output/` = livrables de travail ad-hoc que forge fabrique pour d'autres repos de l'écosystème (claude-switcher, feedback-triage-plugin, support-lojii-plugin, audits, scripts de vérif) ; on peut les déplacer vers leur repo cible ou les supprimer une fois livrés. `data/` = répertoire de sortie par défaut du twitter-api-client (skill `x-read`) : IDs de tweets et comptes téléchargés, purgeable à tout moment.

---

## 13. Métriques (git)

- **Commits total** : 245
- **Premier commit** : 2026-04-03 (`aab5cd4`)
- **Dernier commit** : 2026-05-26 (`8277279`)
- **Période** : ~8 semaines
- **Fréquence par mois** : avril 2026 = 58 commits, mai 2026 = 187 commits (accélération forte en mai)
- **Auteurs** : Raphael Picard uniquement (227 "Raphael Picard" + 18 "Raphael PICARD" = 245)
- **Fichiers les plus modifiés** :
  1. `vault/claude-forge/CHANGELOG.md` (40)
  2. `vault/claude-forge/0-Inbox/context-actuel.md` (37)
  3. `CLAUDE.md` (29)
  4. `.claude/settings.json` (26)
  5. `vault/claude-forge/00-Hub/MOC-Techniques.md` (21)
  6. `.claude/skills/cc-news/SKILL.md` (20)
  7. `.claude/agents/project-analyzer.md` (20, désormais supprimé)
  8. `.claude/agents/project-auditor.md` (17, désormais supprimé)
  9. `.claude/agents/hook-creator.md` (17)
- **Agents les plus modifiés récemment** : les créateurs (skill-creator 16, claudemd-optimizer 15, agent-creator 15, devils-advocate 11) — cœur actif du studio.
- **Skills les plus modifiées** : cc-news (20), cc-hooks-ref (12), cc-features-ref (11), cc-skills-ref/forge-brain (10).

---

## 14. Glossaire

- **forge / claude-forge** : le projet lui-même, studio méta-Claude Code personnel.
- **forge-brain** : le vault Obsidian interne (412 notes) + le serveur MCP qui le sert.
- **Jarvis / contrat Jarvis** : posture relationnelle (Claude = partenaire proactif de Raphael = "Tony Stark"). Anticiper, protéger, innover, évoluer, être franc, autonome.
- **Canonique** : note vault faisant autorité sur un sujet (statut `#statut/canonique`). À lire EN ENTIER avant toute prescription.
- **Compounding** : capitalisation cumulative — chaque erreur/décision est sauvegardée pour ne jamais être réapprise (concept Boris Cherny).
- **Doctrine 22 mai 2026** : pivot où les hooks de workflow agentique sont interdits (hooks = lint/security/scope uniquement).
- **Séquence A→B→C→D→E** : Analyser le réel → lire canoniques en entier → croiser → plan d'écarts → exécuter. Obligatoire pour tout créateur/analyseur.
- **delegate-guard** : hook qui bloque l'édition directe des fichiers protégés (force le passage par les agents spécialistes).
- **meta-commentaire** : justification/source/attribution dans un composant — interdit ("le pourquoi vit dans le vault").
- **Pattern Karpathy / LLM Wiki** : organisation du vault en 3 layers (raw immuable / wiki LLM-owned / schema), avec index.md + log.md.
- **STOP + ESCALADE** : pattern pour sous-agents non-réentrants — au lieu d'inventer, retourner un bloc structuré à la session principale (qui seule peut appeler AskUserQuestion).
- **DA (devil's advocate)** : critique adversariale conditionnelle avant ship d'un livrable majeur.
- **MOC** : Map Of Content — note d'index thématique du vault (7 dans 00-Hub).
- **Quartet** : (déprécié, références résiduelles) pattern d'analyse multi-repo à 4 agents, désormais absorbé par repo-inspector.
- **Casquette** : aire de responsabilité de vie dans le vault (`2-Casquettes/`), ex. responsable-ia.
- **ia-lead-neoteem** : plugin Cowork (7 skills) pour la casquette Responsable IA.
- **context-actuel.md** : note vault (0-Inbox) réécrite par `/done` à chaque fin de session — état courant.

---

## 15. FAQ anticipée

**"C'est quoi claude-forge en 30 secondes ?"**
Le méta-outillage Claude Code personnel de Raphael : 11 agents, 47 skills, 9 hooks et un vault de 412 notes interrogeable par MCP, qui conseillent et fabriquent de la config Claude Code conforme pour tous ses projets, et capitalisent chaque leçon apprise pour ne jamais la réapprendre.

**"Pourquoi ne pas juste utiliser Claude Code sans claude-forge ?"**
Claude Code seul n'a pas de mémoire doctrinale structurée ni de garde-fous de conformité. Forge ajoute : la délégation forcée aux créateurs spécialisés (conformité par construction), une doctrine versionnée et datée, et une boucle de compounding outillée. Sans forge, on recrée des composants non conformes et on réapprend les mêmes erreurs.

**"Quelle est la skill la plus utile de claude-forge ?"**
Difficile d'en désigner une seule, mais `cc-news` (20 modifs) et `forge-brain` (interface du vault, omniprésente) sont les plus sollicitées par l'activité. Pour le quotidien : `/recap` (reprise) et `/done` (capitalisation) encadrent chaque session. Pour la production de composants : `cc-advisor` est le point d'entrée.

**"Comment je contribue à claude-forge ?"**
On ne contribue pas en éditant directement les composants (bloqué par `delegate-guard.py`). On passe par les agents : skill-creator pour une skill, agent-creator pour un agent, claudemd-optimizer pour CLAUDE.md, hook-creator pour un hook. La séquence A→B→C→D→E (observer le réel → lire les canoniques → croiser → planifier → exécuter) est obligatoire. Tout apprentissage se capitalise dans le vault ou la mémoire.

**"claude-forge marche-t-il sur Windows direct ou faut WSL ?"**
Windows direct, pas de WSL. Les hooks utilisent le `py` launcher et `${CLAUDE_PROJECT_DIR}` pour la portabilité cross-poste Windows. `mcp-autostart.py` utilise des flags de process Windows. Linux/Mac demanderaient des adaptations (équivalents `.sh` de `install.bat`, flags subprocess de mcp-autostart).

**"Est-ce que claude-forge fonctionne sans MCP ?"**
Partiellement. Le MCP forge-brain est le SEUL accès autorisé au vault — sans lui, toute la lecture/écriture du vault (cœur du compounding) tombe. Les agents/skills/hooks de création fonctionnent encore, mais privés de la consultation des canoniques. Un fallback Read/Glob direct est prévu uniquement si le MCP crashe (`forge-brain-proactive.md`), considéré comme un cas exceptionnel.

**"Combien de temps pour onboarder un nouveau dev sur claude-forge ?"**
Non trivial. La densité doctrinale (10 rules, 47 skills, ~166 entrées de mémoire, doctrine datée) suppose une lecture de CLAUDE.md + des 9 canoniques du vault. Le README étant obsolète, le présent document (CLAUDE_FORGE_SELF_PORTRAIT.md) est probablement le meilleur point d'entrée. Compter une demi-journée pour comprendre la philosophie (compounding, délégation forcée, doctrine hooks), davantage pour maîtriser l'inventaire complet.

---

## Annexe — Ce que je ne comprends pas / n'ai pas pu vérifier

- **Numéros de ligne via sous-agents** : la majorité des line refs des agents/skills proviennent de lectures par sous-agents, recoupées par échantillonnage (devils-advocate:62-82 vérifié exact). Non revérifiées caractère par caractère pour les 11 agents et 47 skills.
- **README `/batch`** : commande mentionnée dans le README ; pas de skill `batch` dans forge (le mot apparaît dans plusieurs SKILL.md mais comme concept, pas comme commande définie). Probablement une commande Claude Code native référencée en avril, ou obsolète.
- **`output/` et `data/`** : cycle de vie désormais documenté (section 12, P3.7) — répertoires jetables/régénérables gitignorés. Contenu non analysé fichier par fichier (hors périmètre versionné).
- **Incohérence effort devils-advocate** : RÉSOLUE 2026-05-27 (confirmée par lecture directe, body corrigé). Cf section 12.
- **`ia-lead-neoteem`** : plugin Cowork inventorié (7 skills) mais le contenu de ses SKILL.md n'a pas été lu en détail.
- **Tests** : 9 fichiers de tests pytest dans `mcp-forge-brain/tests/` + 1 dans `.claude/hooks/tests/`, non exécutés ici (état pass/fail non vérifié).
