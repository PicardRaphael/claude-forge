---
titre: "CC septembre 2026 — Opus 5.5 + Sonnet 5.5 + v2.1.263 → v2.1.285"
resume: "Série 6-29 septembre 2026 : Opus 5.5 défaut Opus et Pro/Team Standard passés sur Opus (2.1.280), Sonnet 5.5 défaut Sonnet sur l'API Anthropic (2.1.284), auto mode par défaut sans permissions.defaultMode (2.1.283-284), Ultracode devenu toggle séparé de l'effort (2.1.284), /doctor prompt-audit (2.1.283), hooks agent-type interdits sur PermissionRequest (2.1.280), AGENTS.md lu en l'absence de CLAUDE.md (2.1.277), omitClaudeMd (2.1.271), maxEffortLevel (2.1.267), namespace anthropic-skills réservé (2.1.282, réservation claude-ai annulée en 2.1.283)."
aliases:
  - "CC v2.1.285"
  - "CC v2.1.284"
  - "CC v2.1.282"
  - "CC v2.1.280"
  - "CC v2.1.277"
  - "changelog CC septembre 2026"
  - "claude code 2.1.263-282"
  - "claude code 2.1.263-285"
domaine: claude-code
type: changelog
derniere-maj: 2026-09-30
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://www.npmjs.com/package/@anthropic-ai/claude-code"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

Fenêtre du 6 au 29 septembre 2026 (npm `2.1.263` → `2.1.285`, versions 262/264/279 sautées). Source : CHANGELOG officiel, sha256 `f7687fb5…2f62` au 25 sept. (jusqu'à 2.1.282), puis `0937ba0c…f217` au 30 sept. (2.1.283 → 2.1.285, publiées les 25, 28 et 29 sept.). Sélection des changements qui touchent skills, agents, hooks, settings, modèles et sécurité ; fixes, UI et gateways d'entreprise omis. La note d'août (v2.1.221-250) reste à écrire.

## Modèles et effort

- **v2.1.284** — *« Added Claude Sonnet 5.5 (`claude-sonnet-5-5`), now the default Sonnet model on the Anthropic API — 1M context, $2/$10 per Mtok with $0.20/Mtok cache reads »*. Sonnet 5 devient legacy (voir [[Sonnet 5]]).
- **v2.1.284** — *« Changed Ultracode into its own toggle in `/effort` (Tab, or `/effort ultracode [on|off]`): it no longer forces xhigh effort and stays on at any effort level »*. Keybindings `effortSlider:decreaseEffort` / `increaseEffort` / `toggleUltracode`.
- **v2.1.283** — managed settings **`deniedModels`** (bloque des modèles même autorisés par `availableModels`) et **`availableModelsMatch: "exact"`** (une entrée n'autorise que la version nommée, les nouvelles sorties restent bloquées jusqu'à inscription). **v2.1.285** — **`allowedProviders`** limite les providers d'API utilisables sur une machine.
- **v2.1.285** — derrière un `ANTHROPIC_BASE_URL` custom, sessions en fenêtre 1M pour les modèles qui l'ont (Opus 4.7+, Sonnet 5+, Fable) ; `/autocompact 200k` si la gateway plafonne à 200K.
- **v2.1.280** — *« Added Claude Opus 5.5 (`claude-opus-5-5`), now the default Opus model »*. Voir [[Opus 5.5]].
- **v2.1.280** — *« Changed the default model on Pro and Team Standard plans from Sonnet to Opus, matching Max, Team Premium, and Enterprise »*.
- **v2.1.280** — un effort sauvegardé avant que `/effort` devienne par modèle ne s'applique plus aux nouveaux modèles (Opus 5.5 démarre à son défaut `medium`) ; Opus 4.7, 4.8 et Fable 5 ne maintiennent plus leur effort de lancement au-dessus de `effortLevel` (projet, managed, `--settings`, `-p`, SDK).
- **v2.1.277** — Fable toujours visible dans `/model` sur l'API Anthropic, grisé seulement si l'organisation le désactive.
- **v2.1.267** — setting **`maxEffortLevel`** (global ou par modèle sous `modelSettings`) : plafonne l'effort sur tous les providers.
- **v2.1.268** — les outils de suivi de tâches (TaskCreate/Get/Update/List, TodoWrite) ne sont plus proposés qu'aux modèles antérieurs (Claude 3.x, Opus 4.0–4.7, Sonnet 4.0–4.6, Haiku 4.5) ; `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` pour les réactiver ailleurs.

## Hooks

- **v2.1.285** — un hook synchrone qui lance un process en arrière-plan (`some-daemon &`) ne fige plus Claude Code : il se termine peu après la sortie de son propre process. Les hooks et callbacks SDK voient désormais le plan à jour sur ExitPlanMode.
- **v2.1.284** — `{"decision":"block"}` renvoyé par les hooks Elicitation / ElicitationResult décline enfin l'élicitation MCP (comme l'exit 2) ; les hooks en échec loggent leur stderr et leur code de sortie.
- **v2.1.280** — ⚠️ *« Changed `PermissionRequest` hooks: an agent-type hook no longer runs there, since its answer could never allow or deny the request; it now shows an error pointing to command or http hooks »*. Le `settings.json` forge n'en porte aucun (vérifié le 25 sept.) ; l'exemple « Hooks Boris en production » de la skill `cc-features-ref` montrait ce montage.
- **v2.1.280** — taille des sorties de hook et nombre de sorties déportées sur fichier ajoutés à l'événement OTel `hook_execution_complete`.

## Instructions projet, skills, agents

- **v2.1.283** — **`/doctor prompt-audit`** (alias `/checkup prompt-audit`) : audite CLAUDE.md, skills, agents et commandes à la recherche de motifs de prompt écrits pour des modèles plus anciens ; chemins et commandes périmés et fichiers d'instructions contradictoires en tête du rapport.
- **v2.1.283** — *« Reverted the 2.1.282 reservation of the `claude-ai` name »* : skills, commandes, workflows et serveurs MCP nommés `claude-ai` se chargent de nouveau, et `Skill(claude-ai:*)` redevient une règle de préfixe ordinaire. La réservation de `anthropic-skills` (2.1.282) n'est pas annulée.
- **v2.1.284** — le chargement de l'auto-memory neutralise les caractères invisibles et les balises qui imitent le balisage de Claude Code dans `MEMORY.md` et les notes rappelées. Des règles symlinkées dans `.claude/rules` depuis l'extérieur du projet déclenchent désormais la demande d'approbation des imports externes.
- **v2.1.285** — les fork subagents héritent du mode de permission du parent (plan, `dontAsk`) et ne peuvent pas sortir du plan mode ; en auto mode, un subagent s'arrête dès qu'il a rendu son rapport.
- **v2.1.282** — dossiers de skills, commandes et workflow commands dans le namespace `anthropic-skills` **ne se chargent plus** ; un serveur MCP ainsi nommé ne liste plus ses skills/prompts ; les règles `Skill(anthropic-skills:*)` ne couvrent que les skills synchronisées. (La même réservation sur `claude-ai` a été annulée en 2.1.283.)
- **v2.1.277** — *« Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead »* ; étendu à Bedrock/Vertex/Foundry/gateways en v2.1.281. Sans effet sur un repo qui a un `CLAUDE.md` (forge l'importe par `@AGENTS.md`).
- **v2.1.275** — synchronisation des skills et plugins activés sur claude.ai vers les sessions terminal signées ; opt-out `syncClaudeAiSkills: false` / `syncClaudeAiPlugins: false`. En v2.1.269, ces skills sont nommées `anthropic-skills:<nom>` dans les sessions cloud.
- **v2.1.271** — **`omitClaudeMd`** dans le frontmatter d'agent et `--agents` JSON : le subagent tourne sans les CLAUDE.md user/project/local (les policy files managés restent chargés).
- **v2.1.271** — taille de dynamic workflow par défaut « small » sur Pro ; la taille « medium » passe de 15 à 10 agents.
- **v2.1.269** — `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (1–256) relève la limite d'agents concurrents d'un workflow.
- **v2.1.269** — **`claude plugin eval`** : suite d'évaluation d'un plugin, résultats JSON + rapport HTML.

## Outils

- **v2.1.285** — les commandes Bash et PowerShell lancées en arrière-plan s'arrêtent à leur limite de temps (`timeout` avec `run_in_background`, défaut 30 min, max 2 h) ; Claude est notifié de l'arrêt. `CLAUDE_CODE_DISABLE_WEB_FETCH` coupe l'outil WebFetch.
- **v2.1.284** — `/mcp reconnect all` relance d'un coup tous les serveurs MCP en échec ou en attente d'authentification ; un appel d'outil MCP dans une session reprise attend jusqu'à 10 s que son serveur se connecte.
- **v2.1.283** — les images renvoyées par un outil MCP sont aussi écrites sur disque (lisibles par Read/Bash) ; `/context` compte désormais les instructions des serveurs MCP.
- **v2.1.277** — *« Removed the deprecated TaskOutput tool »* : la sortie d'une tâche background se lit avec `Read` ; `taskOutputMaxChars` et `TASK_MAX_OUTPUT_LENGTH` sans effet.
- **v2.1.271** — le Monitor a toujours une échéance (30 min max, 10 en `-p`) et demande à être réarmé ; l'option `persistent` disparaît.
- **v2.1.281** — « send now » (ctrl+enter) passe les outils en cours en arrière-plan au lieu d'annuler le tour.

## Sécurité et permissions

- **v2.1.283 / 2.1.284** — sessions interactives terminal et VS Code démarrent en **auto mode** quand aucun mode de permission n'est configuré, sur tous les plans et providers (2.1.285 : idem pour `claude -p` et le SDK Python sur providers tiers ou sans télémétrie). `permissions.defaultMode` l'emporte toujours — forge pose `"defaultMode": "default"` dans `.claude/settings.json` (vérifié le 30 sept.), donc sans effet sur forge.
- **v2.1.284** — sous `allowManagedPermissionRulesOnly`, seuls les plugins de source Anthropic officielle ou avalisée par les managed settings gardent la pré-approbation de leurs `allowed-tools`.
- **v2.1.285** — les settings projet ne peuvent plus élargir ni désactiver un sandbox exigé par l'admin. Correctif sécurité PowerShell : le contrôle de permission sautait les règles deny/ask si son parser ne démarrait pas (**v2.1.283** : `cmd /c rd|rmdir|del|erase` ne peut plus effacer une racine de disque ou le dossier home).
- **v2.1.277** — *« Changed subagent results to reach the main agent under a header marking them as subagent output … so text in a subagent's result cannot pass as the session's own instructions »*. Même logique pour les prompts `agent()` des workflows sur Bedrock/Vertex/Foundry.
- **v2.1.278 / 2.1.281 / 2.1.282** — auto mode : classifier côté serveur par défaut (API, Enterprise, puis connexion directe sans télémétrie), sans surcoût ; opt-out `CLAUDE_CODE_AUTO_MODE_SERVER=0`. En v2.1.281, les commandes shell read-only et sandboxées attendent aussi sa revue.
- **v2.1.271** — auto mode : les commandes `!` inline des skills suivent les règles du mode par défaut ; un subagent rend la main via un appel dédié revu par le classifier.
- **v2.1.275** — plugins npm récupérés avec `npm pack --ignore-scripts` et vérifiés en intégrité.
- **v2.1.280** — marketplaces imitant un nom réservé refusées.
- **v2.1.282** — `settings.json` projet/local ignorent les variables OpenTelemetry qui activent l'export ou capturent du contenu.

## Settings divers

- **v2.1.281** — `"attribution": false` masque toute attribution de commit/PR (les anciennes CLI ignorent un fichier qui le contient : garder la forme objet dans un fichier partagé).
- **v2.1.282** — `maxProseWidth` plafonne la largeur de la prose dans un terminal large.
- **v2.1.280** — `CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH` change le plafond de 2 048 caractères des descriptions d'outils MCP.
- **v2.1.282** — effets visuels `ultracode` retirés de `/effort` (la fonction reste ; devenue toggle séparé en 2.1.284).
- **v2.1.285** — Windows : l'`env` des settings projet/local ne peut plus fixer `ALLUSERSPROFILE`, `SystemDrive` ni les variables `CommonProgramFiles`.

## Liens

- [[CC juillet 2026 - Opus 5 + v2.1.212-220]] — note changelog précédente
- [[Opus 5.5]] · [[Opus 5]] · [[Sonnet 5]]
- [[comment-creer-hook]] · [[comment-creer-agent]] · [[comment-creer-skill]]
- [[MOC-Claude-Code]]
