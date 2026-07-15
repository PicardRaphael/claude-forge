---
titre: "MOC — OpenAI Codex"
resume: "Index de tout le savoir OpenAI Codex : doctrine (AGENTS.md, config/profils, skills, hooks, subagents, loops, mémoire), leaders, arbitrage vs ChatGPT-app. Miroir de MOC-Claude-Code."
aliases:
  - "MOC Codex"
  - "index codex"
  - "codex doctrine"
  - "openai codex map"
  - "index openai codex"
type: index
derniere-maj: 2026-07-15
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/codex"
---
# OpenAI Codex

> Index du savoir Codex. Corpus doctrinal vérifié en sources primaires au **15 juil. 2026** (les URLs `developers.openai.com/codex/*` redirigent vers `learn.chatgpt.com/docs/*` ; le `docs/config.md` du repo est un stub). Miroir structurel de [[MOC-Claude-Code]] — Codex a ses propres mécanismes, la doctrine CC n'y est pas recopiée.

## ⭐ Doctrine actionnable — corpus 04-Techniques/codex/

- [[workflow-codex-optimal]] (MAÎTRE) — modèle défaut gpt-5.6-sol, séquence S/M/L/XL, Surface Map des 8 leviers, multitasking Sottiaux
- [[agents-md-codex]] — équivalent CLAUDE.md : cap 32 KiB (`project_doc_max_bytes`), nesting, `AGENTS.override.md`, § Review guidelines
- [[config-toml-profils-codex]] — réglages machine, **rupture profils 0.134.0** (1 fichier/profil, legacy = crash), précédence, requirements.toml
- [[comment-creer-skill-codex]] — divergences vs standard Agent Skills : name+description, 4 scopes, `.agents/skills`, sidecar `openai.yaml`, portabilité NON byte-identique
- [[comment-creer-hook-codex]] — **stable v0.124.0** (plus expérimental), 10 events, piège `Stop` inversé, gap `additionalContext`/PreToolUse, trust model par hash
- [[subagents-cloud-codex]] — subagents TOML (`developer_instructions`, max_threads=6/max_depth=1, built-ins), cloud tasks, automations RRULE
- [[loops-codex]] — `codex exec` headless, automations (équivalent natif pattern Boris), CI `openai/codex-action`
- [[loop-apprentissage-codex]] — compounding : `[memories]` auto + skills + scheduled task « scan sessions → update skills » (verbatim)
- [[memoire-optimale-codex-chatgpt]] — montage mémoire cross-tool (où ranger quel savoir)
- [[codex-vs-chatgpt-seul]] — arbitrage produit : quand Codex, quand ChatGPT-app

## ChatGPT seul (corpus séparé, court)

- [[personnalisation-chatgpt-app]] — custom instructions, Projects, mémoire native, GPTs, connectors, Assistants API (sunset 26 août 2026) → Responses API. ⚠️ provenance dégradée (403 WebFetch → paraphrase)

## Fraîcheur — état verrouillé 15 juil. 2026

- Modèle défaut CLI : `gpt-5.6-sol` (alias `gpt-5.6`, preset Power medium) depuis GA 9 juil. Famille Sol/Terra/Luna. Dépréciés : gpt-5.2, gpt-5.3-codex. Sunset legacy 23 juil.
- CLI `0.144.4` (14 juil.). Prix API (short ctx, $/1M) : Sol 5/30, Terra 2.5/15, Luna 1/6 ; GPT-5-Codex 1.25/10 (ctx 400K). Context GPT-5.6 1.05M = *à vérifier* (secondaire).

## Leaders Codex

- [[Thibault Sottiaux]] — Head of Codex, agent-first, multitasking, sandboxing agressif
- [[Michael Bolin]] — tech lead repo open-source `openai/codex` (Rust)
- [[Fouad Matin]] — release initiale CLI, sécu/sandboxing
- [[Andrew Ambrosino]] — desktop app, « taste > implementation »
- [[Gabriel Peal]] — extension VS Code + desktop
- [[Josh McKinney]] — Ratatui (TUI Rust)
- [[Shao-Qian Mah]] — researcher modèles Codex
- [[Simon Willison]] — praticien externe de référence (reverse-eng CLI, skills cross-LLM, lethal trifecta)

## Industrie

- [[OpenAI Codex]] — fiche produit (06-Industrie)
- [[MOC-Outils-IA]] — concurrents · [[MOC-Claude-Code]] — le miroir Claude Code
- [[Agent Skills Spec]] — spec ouverte adoptée par Codex + CC
