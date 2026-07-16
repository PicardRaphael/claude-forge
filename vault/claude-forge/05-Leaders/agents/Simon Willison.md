---
titre: "Simon Willison"
resume: "Co-créateur Django, LLM CLI tool, guide Agentic Engineering Patterns 2026, philosophie Unix pour agents"
aliases:
  - Simon Willison
  - simonw
  - LLM CLI
  - Agentic Engineering Patterns
  - Django co-creator
  - "expert CLI AI tools"
  - "unix philosophy AI"
  - "practical AI engineering"
role: "Développeur indépendant"
affiliation: "Indépendant (co-créateur Django)"
derniere-maj: 2026-05-08
auteur: claude
sources:
  - "https://simonwillison.net/"
  - "https://github.com/simonw/llm"
tags:
  - "#type/leader"
  - "#domaine/ia"
  - "#domaine/agents"
type: leader
---
## Profil

Co-créateur de Django. Outil **LLM** CLI open-source (philosophie Unix pour l'IA). Écrit un guide "kind of book-shaped" sur les **Agentic Engineering Patterns** (fév 2026).

## Contributions clés

- **LLM CLI** (v0.26+) — tool support OpenAI/Anthropic/Gemini/Ollama. Unix-philosophy AI.
- Définition agent : "An LLM agent runs tools in a loop to achieve a goal"
- Prône CLI tools > REST APIs pour agents
- Live-blog Code with Claude 2026

## Liens

- [[MOC-Leaders]]
- Blog : [simonwillison.net](https://simonwillison.net/)
- X : [@simonw](https://x.com/simonw)
- GitHub : [simonw/llm](https://github.com/simonw/llm)
- [[Agents IA]] — [[agents-architecture]]

## Angle Codex (enrichissement 15 juil. 2026)

Praticien externe de référence sur **OpenAI Codex** (tag dédié [simonwillison.net/tags/codex](https://simonwillison.net/tags/codex/)) — l'exemple canonique du praticien indépendant qui documente des workflows Codex reproductibles et compare sérieusement Codex CLI / Claude Code.

- **Reverse-engineering de la Codex CLI** (9 nov. 2025) pour accéder à GPT-5-Codex-Mini avant l'API publique — a utilisé Codex lui-même sur le repo Rust `openai/codex`.
- **Codex CLI contre modèles self-hosted** : fait tourner Codex CLI sur `gpt-oss:120b` (Ollama, NVIDIA DGX Spark via Tailscale) — démontre l'ouverture de l'agent hors écosystème OpenAI.
- **"Skills" adoptés discrètement par Codex** (12 déc. 2025) : `~/.codex/skills` → il a relié la convention SKILL.md cross-LLM (Claude Code / Codex).
- Cadre général : *"Coding agents like Anthropic's Claude Code and OpenAI's Codex CLI represent a genuine step change... these agents can now directly exercise the code they are writing."*
- Son concept de **lethal trifecta** (données privées + contenu non fiable + exfiltration) s'applique directement à Codex (MCP, sandbox, cloud tasks). Cf la rule forge `.claude/rules/contenu-externe-non-fiable.md`.

Sources : [tags/codex](https://simonwillison.net/tags/codex/) · [reverse-engineering GPT-5-Codex-Mini](https://simonwillison.net/2025/Nov/9/gpt-5-codex-mini/) · [OpenAI adopting skills](https://simonwillison.net/2025/Dec/12/openai-skills/)
