---
titre: "CC septembre 2026 — Opus 5.5 + v2.1.263 → v2.1.282"
resume: "Série 6-24 septembre 2026 : Opus 5.5 défaut Opus et Pro/Team Standard passés sur Opus (2.1.280), hooks agent-type interdits sur PermissionRequest (2.1.280), AGENTS.md lu en l'absence de CLAUDE.md (2.1.277), TaskOutput supprimé, sorties de subagents balisées anti-injection, sync des skills/plugins claude.ai (2.1.275), omitClaudeMd en frontmatter agent (2.1.271), maxEffortLevel (2.1.267), namespaces anthropic-skills/claude-ai réservés (2.1.282)."
aliases:
  - "CC v2.1.282"
  - "CC v2.1.280"
  - "CC v2.1.277"
  - "changelog CC septembre 2026"
  - "claude code 2.1.263-282"
domaine: claude-code
type: changelog
derniere-maj: 2026-09-25
auteur: claude
sources:
  - "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  - "https://www.npmjs.com/package/@anthropic-ai/claude-code"
tags:
  - "#type/changelog"
  - "#domaine/claude-code"
---

Fenêtre du 6 au 24 septembre 2026 (npm `2.1.263` → `2.1.282`, versions 262/264/279 sautées). Source : CHANGELOG officiel, sha256 `f7687fb5…2f62` au 25 sept. Sélection des changements qui touchent skills, agents, hooks, settings, modèles et sécurité ; fixes, UI et gateways d'entreprise omis. La note d'août (v2.1.221-250) reste à écrire.

## Modèles et effort

- **v2.1.280** — *« Added Claude Opus 5.5 (`claude-opus-5-5`), now the default Opus model »*. Voir [[Opus 5.5]].
- **v2.1.280** — *« Changed the default model on Pro and Team Standard plans from Sonnet to Opus, matching Max, Team Premium, and Enterprise »*.
- **v2.1.280** — un effort sauvegardé avant que `/effort` devienne par modèle ne s'applique plus aux nouveaux modèles (Opus 5.5 démarre à son défaut `medium`) ; Opus 4.7, 4.8 et Fable 5 ne maintiennent plus leur effort de lancement au-dessus de `effortLevel` (projet, managed, `--settings`, `-p`, SDK).
- **v2.1.277** — Fable toujours visible dans `/model` sur l'API Anthropic, grisé seulement si l'organisation le désactive.
- **v2.1.267** — setting **`maxEffortLevel`** (global ou par modèle sous `modelSettings`) : plafonne l'effort sur tous les providers.
- **v2.1.268** — les outils de suivi de tâches (TaskCreate/Get/Update/List, TodoWrite) ne sont plus proposés qu'aux modèles antérieurs (Claude 3.x, Opus 4.0–4.7, Sonnet 4.0–4.6, Haiku 4.5) ; `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` pour les réactiver ailleurs.

## Hooks

- **v2.1.280** — ⚠️ *« Changed `PermissionRequest` hooks: an agent-type hook no longer runs there, since its answer could never allow or deny the request; it now shows an error pointing to command or http hooks »*. Le `settings.json` forge n'en porte aucun (vérifié le 25 sept.) ; l'exemple « Hooks Boris en production » de la skill `cc-features-ref` montrait ce montage.
- **v2.1.280** — taille des sorties de hook et nombre de sorties déportées sur fichier ajoutés à l'événement OTel `hook_execution_complete`.

## Instructions projet, skills, agents

- **v2.1.277** — *« Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead »* ; étendu à Bedrock/Vertex/Foundry/gateways en v2.1.281. Sans effet sur un repo qui a un `CLAUDE.md` (forge l'importe par `@AGENTS.md`).
- **v2.1.275** — synchronisation des skills et plugins activés sur claude.ai vers les sessions terminal signées ; opt-out `syncClaudeAiSkills: false` / `syncClaudeAiPlugins: false`. En v2.1.269, ces skills sont nommées `anthropic-skills:<nom>` dans les sessions cloud.
- **v2.1.282** — dossiers de skills, commandes et workflow commands dans les namespaces `anthropic-skills` ou `claude-ai` **ne se chargent plus** ; un serveur MCP ainsi nommé ne liste plus ses skills/prompts ; les règles `Skill(anthropic-skills:*)` ne couvrent que les skills synchronisées.
- **v2.1.271** — **`omitClaudeMd`** dans le frontmatter d'agent et `--agents` JSON : le subagent tourne sans les CLAUDE.md user/project/local (les policy files managés restent chargés).
- **v2.1.271** — taille de dynamic workflow par défaut « small » sur Pro ; la taille « medium » passe de 15 à 10 agents.
- **v2.1.269** — `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS` (1–256) relève la limite d'agents concurrents d'un workflow.
- **v2.1.269** — **`claude plugin eval`** : suite d'évaluation d'un plugin, résultats JSON + rapport HTML.

## Outils

- **v2.1.277** — *« Removed the deprecated TaskOutput tool »* : la sortie d'une tâche background se lit avec `Read` ; `taskOutputMaxChars` et `TASK_MAX_OUTPUT_LENGTH` sans effet.
- **v2.1.271** — le Monitor a toujours une échéance (30 min max, 10 en `-p`) et demande à être réarmé ; l'option `persistent` disparaît.
- **v2.1.281** — « send now » (ctrl+enter) passe les outils en cours en arrière-plan au lieu d'annuler le tour.

## Sécurité et permissions

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
- **v2.1.282** — effets visuels `ultracode` retirés de `/effort` (la fonction reste).

## Liens

- [[CC juillet 2026 - Opus 5 + v2.1.212-220]] — note changelog précédente
- [[Opus 5.5]] · [[Opus 5]]
- [[comment-creer-hook]] · [[comment-creer-agent]] · [[comment-creer-skill]]
- [[MOC-Claude-Code]]
