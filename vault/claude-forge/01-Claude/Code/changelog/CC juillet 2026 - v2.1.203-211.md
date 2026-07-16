---
titre: "CC juillet 2026 — v2.1.203 → v2.1.211"
resume: "Série 7-15 juillet post-Sonnet 5 : auto mode par défaut Bedrock/Vertex/Foundry (2.1.207), screen reader mode + transcripts -79x (2.1.208), hardening anti prompt-injection du tool Agent (2.1.210), fix billing prompt-caching gateways (2.1.211)"
aliases:
  - "CC v2.1.211"
  - "CC v2.1.208"
  - "CC v2.1.207"
  - "changelog CC mi-juillet 2026"
  - "claude code 2.1.203-211"
domaine: claude-code
type: changelog
derniere-maj: 2026-07-16
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://github.com/anthropics/claude-code/releases"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

Suite de [[CC juillet 2026 - Sonnet 5 + v2.1.198]]. Fenêtre 7-15 juillet 2026, 9 versions.

## v2.1.203 (7 juil.)

- Warning avant expiration de login (protège les sessions background) ; badge ⏸ en mode permission manuel
- Working directories additionnels exposés à MCP `roots/list`
- Gros lot de fixes background agents : PATH hérité stale du daemon, stall macOS 15-20s, `ANTHROPIC_BASE_URL` droppé, crash-loop si working dir supprimé
- Sub-agents moins enclins à re-déléguer leur tâche entière à un autre sub-agent
- Binaire -7 MB, startup -7 MB RAM

## v2.1.204-205 (8 juil.)

- Fix hook events `SessionStart` non streamés en headless (idle-reap des remote workers en plein hook)
- Règle auto mode anti-tampering des fichiers de transcript de session
- **`/doctor` devient un checkup complet** (diagnose + fix, alias `/checkup`)
- **Fix Windows worktree removal qui supprimait des fichiers HORS du worktree** si junction NTFS/symlink présent (grave)
- Auto mode demande confirmation avant `rm -rf` sur une variable non résolue
- Notifications de tâches background précisent explicitement qu'aucun input humain n'a eu lieu

## v2.1.206 (9 juil.)

- `/commit-push-pr` auto-autorise `git push` vers le remote configuré
- **`/doctor` propose de trimmer les CLAUDE.md commités** (signal Anthropic pro-CLAUDE.md court — renforce [[comment-ecrire-claudemd]])
- `EnterWorktree` demande confirmation hors de `.claude/worktrees/`
- Background agents s'auto-upgradent après un update CC
- Amélioration qualité `/code-review` sur claude-opus-4-8 (tous efforts)

## v2.1.207 (10-11 juil.)

- **Auto mode disponible sans opt-in `CLAUDE_CODE_ENABLE_AUTO_MODE` sur Bedrock, Vertex AI et Foundry** (désactivable `disableAutoMode`)
- Bedrock/Vertex/Claude Platform AWS passent par défaut à Opus 4.8
- Sécu plugins : `${user_config.*}` rejeté dans les commandes shell-form ; `pluginConfigs` plus lu depuis `.claude/settings.json` projet
- Fix faux warnings prompt-injection sur updates système bénignes
- Auto mode ne lit plus `autoMode` depuis `.claude/settings.local.json`

## v2.1.208 (13 juil.)

- **Screen reader mode** (rendu plain-text opt-in) ; `vimInsertModeRemaps` (ex. `jj` → Escape)
- `CLAUDE_CODE_PROCESS_WRAPPER` : launcher corporate obligatoire pour tous les self-spawns
- **Transcripts de session réduits jusqu'à 79x** (sessions edit-heavy) ; gros fixes memory leaks (stderr MCP stdio jusqu'à 64 MB/serveur, LSP docs en LRU cap 50, cache edit borné 16 MB)
- Commandes catastrophiques (`rm -rf ~`) dans `$(…)`/backticks/`<(…)` déclenchent désormais un prompt
- Fix Edit tool qui échouait sur fichier modifié après lecture quand le texte cible restait unique
- Agents view : Ctrl+X ne détruit plus de commits non pushés ; background agents complétés restent dans `/tasks`

## v2.1.209-210 (14 juil.)

- **Fix `isolation: 'worktree'` : les sub-agents pouvaient exécuter des commandes git-mutantes contre le checkout principal**
- Fix mot-clé `ultracode` déclenché par des inputs non-humains (webhooks)
- **Hardening du tool Agent contre l'injection indirecte via contenu lu par un sub-agent**
- Auto mode : le classifier de permissions passe à Sonnet 5 par défaut (sessions externes, épinglé par session)
- Fix placeholders `$1`/`$2` non appariés silencieusement strippés dans skills/commands
- Écriture mémoire laissant l'index MEMORY.md au-dessus de sa limite de lecture → erreur explicite (fini la troncature silencieuse)
- Fix timeout de hook rapporté à tort comme rejet utilisateur
- Dataviz : validation couleurs en OKLab perceptuel

## v2.1.211 (15 juil.)

- `--forward-subagent-text` / `CLAUDE_CODE_FORWARD_SUBAGENT_TEXT` : inclure le texte des sub-agents
- **Règles « always allow » sauvegardées à la racine du repo** (plus au niveau dossier courant)
- Fix nested `.claude/rules/*.md` chargées même quand les sources de settings excluaient le projet
- Fix sub-agents avec override de modèle qui revenaient au modèle parent au resume
- Fix `/loop` masquant la session de `/resume` après un seul usage ; fix `/clear` ne réinitialisant pas le compteur de coût
- **Fix régression prompt-caching sur Bedrock/Vertex/Mantle/Foundry** qui facturait le dernier bloc système en input frais
- Env vars entières acceptent la notation scientifique

## Dépréciations liées (fenêtre juillet)

- [[claude-mythos-preview]] (`claude-mythos-preview`) : retrait **21 juillet 2026**
- Opus 4.1 : retrait **5 août 2026**

## Liens

- [[CC juillet 2026 - Sonnet 5 + v2.1.198]] — épisode précédent
- [[auto-mode-classifier]] — évolution classifier Sonnet 5
- [[MOC-Claude-Code]]
