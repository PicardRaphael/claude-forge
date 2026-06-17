---
name: industry-competitors-april-2026
description: Concurrents AI coding (Gemini CLI, Codex, Copilot, Cursor, xAI) + leaders (Karpathy, LeCun, Altman, Musk) — snapshot 8 mai 2026.
type: reference
originSessionId: 16ee3ed4-640e-4e12-aa29-c8156e56b4f6
---
## Concurrents AI Coding — Avril 2026

### Gemini CLI
- **v0.37.1** (9 avril) : Sandbox dynamique, worktrees, Chapters, browser agent
- **v0.37.2** (13 avril) : Fix UTF-8 multi-byte, fuites mémoire, OOM gros flux
- **v0.38.0-preview.0** (~14 avril) : Pre-release publiée
- **v0.38.1** (16 avril) : Bugfixes (MCP progress leak, Ctrl+G shortcut), Gemini 3 dispo pour tous
- **Subagents** (14-15 avril) : Délégation à agents spécialisés, YAML frontmatter (même pattern que CC), `~/.gemini/agents`, remote via A2A, YOLO mode par défaut, 1M+ tokens/agent (5x CC)
- **Code Customization** étendue au CLI et Agent Mode (repos privés indexés)
- Code Assist : Gemini 3.1 Pro + 3.0 Flash, inline diff GA, Next Edit Predictions, mémoire persistante GitHub

### OpenAI Codex CLI
- Sandbox Windows avec egress OS-level, ChatGPT device-code sign-in headless
- `codex exec` prompt+stdin, MCP accéléré
- **14 avril** : Retrait définitif anciens modèles (gpt-5.2-codex, 5.1-*, gpt-5). Restent : gpt-5.4, 5.4-mini, 5.3-codex, 5.2
- **Codex CLI v0.121.0** alpha.6-9 (13-14 avril) : Stabilité Windows/Linux, fixes MCP
- **GPT-5.3 Instant Mini** : Nouveau fallback ChatGPT
- **Hook `userpromptsubmit`** ajouté à Codex CLI (copie du pattern CC)
- OpenAI : $122B levée à $830B valorisation (2 avril)
- **17 avril — MEGA UPDATE** ciblant Claude Code :
  - Multi-agent workflows (write/debug/test en parallèle)
  - Computer Use sur macOS (contrôle desktop apps)
  - Mémoire inter-sessions (contexte persistant)
  - Navigateur intégré avec commenting + image gen (gpt-image-1.5)
  - **111 plugins** (skills + MCP server connections)
  - **GPT-5.3-Codex** + **Codex-Spark** (partenariat Cerebras) en preview
  - 3M utilisateurs/semaine, +1M/mois

### GitHub Copilot
- **Remote CLI Sessions** (13 avril) : `copilot --remote`, pilotage web/mobile, streaming temps réel, QR code
- **Data Residency US+EU + FedRAMP Moderate** (13 avril) : Endpoints certifiés, modèles GPT-5.4 / Claude Sonnet-Opus 4.6
- **Model Selection** (14 avril) : Choix modèle Claude/Codex au lancement sur github.com
- **Claude Opus 4.7** disponible (7.5x premium multiplier jusqu'au 30 avril)
- **Auto model selection GA** en CLI
- **Autopilot** (autonomous agent sessions, public preview). Nested subagents
- **`gh skill`** command : discover/install/publish agent skills cross-platform (spec ouverte CC/Cursor/Codex/Gemini)
- Image/video dans chat
- **20 avril** : **Plans individuels (Student/Pro/Pro+) nouvelles inscriptions suspendues**
- "Rubber Duck" expérimental : Claude + GPT-5.4 combo dans Copilot CLI

### Cursor
- **Cursor 3** (2 avril) : Agents Window, Design Mode, `/worktree`, `/best-of-n`, browser intégré
- **Cursor 3.1** (13 avril) : Panneaux splitables (tiled layout), drag-and-drop agents, keybindings
- **Canvases** (15 avril) : Artefacts interactifs (dashboards, diagrammes, charts, tables, diffs, to-do) dans panneau latéral durable
- **Bugbot** (8 avril) : Auto-amélioration via feedback PR, 80% résolution

### xAI / Grok
- `grok-code-fast-1` à $0.20/M tokens
- Grok Build (upcoming) : CLI local + web coding avec crédits
- Grok 5 en training (Colossus 1.5GW), Q2 2026 attendu
- Musk admet "Grok is currently behind in coding". Grok 4.3 Beta en itération rapide
- Plugins Microsoft Office teased. Layoffs ordonnés par Musk
- 2 poaches de Cursor. 4 divisions : Grok main, Coding, Imagine, Macrohard

## Leaders & Visionnaires

### Sam Altman / OpenAI
- **GPT-5.5 Instant** lance 5 mai 2026
- Partenariat AWS Bedrock annonce (OpenAI disponible hors Azure)
- Déclare AGI atteint selon la définition OpenAI. Prochaine cible = ASI ("AI CEO/President")
- "New Deal for AI" — wealth fund, robot tax, 4-day workweek
- Attaque cocktail Molotov résidence SF (suspect arrêté)
- OpenAI revenue: $25B annualisé. IPO prévu fin 2026/début 2027
- Closure de Sora, Disney annule $1B d'investissement
- **Anthropic annonce $30B annualisé, dépassant OpenAI pour la première fois**

### Andrej Karpathy
- "LLM wikis" : knowledge management, 100+ articles, 400K mots
- AutoResearch (21K GitHub stars), "agentic engineering"
- **Sequoia AI Ascent 2026** (mai) : Framework **Vibe Coding → Agentic Engineering**. 80% de son code AI-generated depuis dec 2025. "Jagged intelligence" = IA spike dans certains domaines. Software 3.0 = programming through context. "Don't ask what AI can help you build faster — ask what AI makes unnecessary"

### Yann LeCun
- Project Tapestry (AI Alliance) — modèles frontier open-source fédérés
- AMI Labs $1B+ pour world models
- Conférence Brown University (~14 avril, propos déjà connus)

### Elon Musk / xAI
- Grok Heavy surpasse Claude Opus (claims xAI)
- **30 avril** : Musk admet sous serment distillation Grok sur modeles OpenAI
- xAI absorbe par SpaceX ("SpaceXAI")
- Musk classe Anthropic n.1 devant OpenAI
- Deal Anysphere/Cursor a $60B

## Stanford AI Index (13 avril)
- **Anthropic #1 Arena** (community ranking), suivi xAI, Google, OpenAI
- Meilleurs modèles > 50% sur "Humanity's Last Exam"
- IA booste productivité : +14% support client, +26% dev logiciel
- IA agentique = "gains les plus extrêmes"
- Adoption IA plus rapide que PC ou Internet

### GitHub Copilot (post-16 avril)
- **24 avril** : Données d'interaction entraîneront les modèles (opt-in Free/Pro/Pro+)
- Ships Claude Opus 4.6 et Sonnet 4.6 comme options de modèle
- "Rubber Duck" expérimental requiert spécifiquement un modèle Claude

## Mai 2026 — Updates

### Anthropic
- **Claude Mythos Preview** — SWE-bench 93.9%, zero-day autonome (FreeBSD 17 ans, OpenBSD 27 ans). Acces restreint Project Glasswing (~40 partenaires). $100M credits. White House oppose extension.
- **Claude Security** — Beta publique enterprise 1er mai. Scans planifies, triage, exports, webhooks. Propulse Opus 4.7. Partenaires : CrowdStrike, Microsoft Security, Palo Alto, SentinelOne, Wiz. Services : Accenture, BCG, Deloitte, Infosys, PwC.
- **Bun acquis** — Jarred Sumner rejoint Anthropic. CC atteint $1B ARR en 6 mois. Revenue ARR >$30B.
- **$1.5B JV** (5 mai) : Blackstone + Goldman Sachs + Hellman & Friedman + Apollo + Sequoia — firme enterprise AI-native mid-market
- **Funding round** en cours : valorisation potentielle **$900B** (~$50B capital). Dépasserait OpenAI $852B.
- **Code with Claude** — 1ere conference dev : SF 6 mai, Extended 7 mai, Londres 19 mai, Tokyo 10 juin.
- **Computer Use dans CC** — Research preview macOS + Windows. Dispatch integration.
- **Excel & PowerPoint** — Skills support, context sharing (Felix)
- **Voice STT** — 10 nouvelles langues (20 total)

### OpenAI Codex (mai)
- **GPT-5.3-Codex** — premier modele instrumentalisé dans sa propre creation, 25% plus rapide, SWE-Bench Pro + Terminal-Bench records
- **Codex-Spark** (research preview, Cerebras) — Pro only, 128k context, hardware basse latence
- **"Codex for Almost Everything"** — computer use background (Mac), in-app browser, memory cross-sessions, scheduling multi-jours, 90+ plugins (Atlassian, CircleCI, CodeRabbit, GitLab, Microsoft Suite, Neon, Remotion, Render)
- **Advanced Account Security** avec protection Codex
- Bedrock first-class, deny-read glob policies
- Pro $100 = 2x usage jusqu'au 31 mai
- 3M+ utilisateurs/semaine

### GitHub Copilot (mai)
- **Usage-based billing 1er juin** — AI Credits par tokens. Preview bill en mai.
- Cloud agent sessions depuis IDE, Debugger agent, model picker
- CLI v1.0.40 : `/fleet` dispatch parallele, ACP session controls, `client_credentials` OAuth MCP
- **Opus retire des plans Pro** (reste Pro+)
- Plusieurs modeles deprecies le 1er juin

### Cursor (mai)
- **v3.2** : Multitask, Worktrees, Multi-root Workspaces, Cursor SDK
- **Security Review** beta Teams/Enterprise (Security Reviewer + Vulnerability Scanner)
- **Interactive Canvases** dans Agents Window (React-based) — dashboards, PR reviews, eval analysis
- **BugBot learned rules** — apprend du feedback PR, resolution ~80%
- **Model Controls** enterprise (4 mai) : blocklists provider/model, soft limits, alertes 50/80/100%
- **Team Marketplace** (1er mai) : plugins Default Off/On/Required sans repo
- Vuln RCE fixee v2.5 (repo Git malveillant → code execution)
- 1M+ devs, 360K payants, 64% Fortune 500

### Gemini (mai)
- **Gemini CLI GitHub Actions** beta — agent autonome sur issues/PRs, full repo context
- **Gemini 2.5 Pro/Flash GA**. Gemini 3 models avec 1M context
- Code Assist Agent Mode VS Code : inline diff, batched tool approvals, persistent history, real-time shell output
- CLI 60 req/min + 1000 req/jour gratuit
- Standard JSON Schema support (Zod 4, Valibot, ArkType)
- Public roadmap Gemini CLI v1

### LangChain/LangGraph (mai)
- **Deep Agents** — subagents async, plan-use-file-system
- LangGraph 1.0 GA : durable execution, HITL, comprehensive memory
- Node Caching, Deferred Nodes, Pre/Post Model Hooks
- Conference Interrupt 13-14 mai SF (Harrison Chase, Andrew Ng)

## How to apply
GitHub suspend les plans individuels (pricing pressure?). `gh skill` = spec ouverte cross-platform, convergence skills CC/Cursor/Codex/Gemini. Copilot Autopilot = réponse directe aux worktrees CC. Anthropic $30B > OpenAI $25B = renversement historique des revenus. Musk admet le retard coding de Grok et restructure agressivement (4 divisions). Claude Design dans Cowork = nouveau vecteur non-coding. **Piebald-AI** = repo public system prompts CC, utile pour comprendre le context engineering interne.

**Mai 2026** : Convergence massive vers security scanning integre (Claude Security, Cursor Security Review, Copilot security). Copilot bascule usage-based billing — impact potentiel sur adoption enterprise. Anthropic lance sa 1ere conference dev (Code with Claude). Claude Mythos = moment watershed cybersecurite IA. Codex deprecie --full-auto = shift vers permissions explicites (meme direction que CC auto mode classifier). Anthropic potentiellement valorise $900B (depasse OpenAI $852B). GPT-5.3-Codex = premier modele auto-instrumentalise. Karpathy framework Vibe Coding → Agentic Engineering devient reference industrie. Convergence computer use : CC, Codex, Copilot tous offrent controle desktop.
