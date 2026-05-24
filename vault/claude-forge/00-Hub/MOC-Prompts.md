---
titre: "MOC — Prompts"
resume: "Index de tous les prompts, system prompts, agent prompts, skill prompts et templates réutilisables"
aliases:
  - "MOC Prompts"
  - "index prompts"
  - "prompts référence"
  - "system prompts collection"
  - "templates prompts"
type: index
derniere-maj: 2026-05-24
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/prompt-engineering"
---
# Prompts

## System Prompts

- [[System Prompt Amanda Askell]] — Structure optimale system prompt Claude
- [[System Prompt Claude Code]] — Piebald-AI, context engineering dynamique
- System Prompt Gemini CLI — Pattern Gemini, comparaison avec CC (à documenter)

## Agent Prompts

Prompts des agents Claude Code — descriptions, triggers, instructions.

## Skill Prompts

Prompts des skills — triggers, descriptions, instructions SKILL.md.

## Templates Prompts

Prompts réutilisables pour tâches courantes.

## Principes

- Prompt vs Skill vs Rule — Quand utiliser chaque format (à documenter)
- Description Trigger Pattern — "Use PROACTIVELY when..." (Thariq, à documenter)
- [[Context Engineering]] — Paradigme dominant 2026
- [[outcome-first-prompting]] — Outcome + critères de succès + contraintes dures uniquement (GPT-5.5, 2026)
- [[over-specification-paradox]] — Seuil S*=0.509 : moins de specs = meilleures performances sur frontier
- [[deprecated-techniques-2026]] — Techniques 2023-2025 désormais contre-productives

## Par modèle cible

| Modèle | Notes |
|--------|-------|
| Claude | System prompts, agent prompts, CLAUDE.md patterns |
| Gemini | GEMINI.md, agents Gemini CLI |
| GPT | Codex agents, ChatGPT custom instructions |
| Tout LLM | Principes universels, techniques cross-model |

## Liens



## Prompts d'audit

- [[self-audit-doctrine-session]] — Self-audit post-mortem session : check Claude a respecté doctrine forge (7 checks evidence-based)
