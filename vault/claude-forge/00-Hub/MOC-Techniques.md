---
titre: "MOC — Techniques"
resume: "Index des techniques : prompt engineering, context engineering, patterns, anti-patterns"
aliases:
  - "MOC Techniques"
type: index
derniere-maj: 2026-05-08
auteur: claude
tags:
  - "#type/index"
  - "#domaine/techniques"
---

# Techniques

## Prompt Engineering

- [[Context Engineering]] — Paradigme dominant 2026
- [[Adaptive Thinking]] — Opus 4.7, off par défaut
- [[Effort Levels Guide]] — low/medium/high/xhigh/max
- [[System Prompt Design]] — Amanda Askell, structure optimale

## Patterns

- [[Knowledge-First Routing]] — Brain avant code
- [[Fleet Commander]] — Boris, parallélisme worktrees
- [[Document and Clear]] — Plan → .md → /clear → nouvelle session
- [[Skills as Composability]] — Thariq, skills = couche composable
- [[LLM Wiki]] — Karpathy, knowledge management plain text
- [[Karpathy Dev Discipline]] — 4 principes coding (Simplicity, Surgical, Assumptions, Verifiable Steps)
- [[config-guardian-pattern]] — Audit multi-repo 5 checks, corrections par stack, mémoire compounding Boris+Karpathy
- [[agentic-engineering-karpathy]] — Framework Karpathy : Software 3.0, vibe coding vs agentic engineering, jagged intelligence
- [[pattern-agentic-engineering]] — Checklist deploiement agentic engineering sur projet Neoteem
- [[pattern-vault-query-guard]] — Hook deterministe : agents DOIVENT consulter vault avant d'ecrire

- [[best-practices-claude-code-leaders]] — Synthese Boris, Erik, Thariq, Cat Wu, Karpathy : planification, contexte, skills, effort
- [[decoupe-agents-anti-crash]] — Max 6-8 ops/agent, decoupage par theme/repo/phase, parallelisation
- [[limites-subagents-claude-code]] — 200K ctx, 32K output, maxTurns casse, jamais parallele, bugs GitHub

## Architecture Hooks

- [[erreur-marker-ttl-blocage-agents]] — TTL sur markers = blocage, existence seule + SessionStart reset
- [[pattern-vault-query-guard]] — Hook deterministe : agents DOIVENT consulter vault avant d'ecrire
- [[pattern-architect-first-pipeline]] — SessionStart reset → architect → dev → code-reviewer → /go → pipeline-reset

## Anti-patterns

- [[Silent Assumptions]] — Karpathy anti-pattern #1
- [[Over-Engineering]] — Abstraction prématurée
- [[Drive-By Refactoring]] — Refacto non demandé
- [[erreur-pipeline-advisory-sans-hooks]] — Rules advisory ignorees, hooks marker+guard obligatoires (3 iterations)


## Neoteem Infrastructure

- [[mcp-obsidian-brain-v2]] — MCP SQLite FTS5, remplace CLI Obsidian, VM serveur
- [[SQLite FTS5 pour vault]] — Pattern : indexer un vault Obsidian dans SQLite FTS5
- [[neoteem-brain-plugins]] — 5 plugins Cowork role-based (dev/admin/support)

## Configuration

- [[claude-desktop-preferences]] — Profil, Cowork, pattern vault-first MCP pour non-devs
- [[forge-prompt-machine]] — 12 principes FORGE BellumAI x Askell, checklist, anti-patterns
- [[prompting-chat-cowork-code]] — Differences de prompting Chat vs Cowork vs Code, Opus 4.7