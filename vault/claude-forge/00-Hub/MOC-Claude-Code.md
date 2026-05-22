---
titre: "MOC — Claude Code"
resume: "Index de tout le savoir Claude Code : features, changelog, hooks, skills, best practices"
aliases:
  - "MOC Claude Code"
  - "CC index"
  - "claude code features"
  - "index claude code"
  - "CC features map"
type: index
derniere-maj: 2026-05-22
auteur: claude
sources: []
tags:
  - "#type/index"
  - "#domaine/claude-code"
---

# Claude Code

## ⭐ Notes canoniques chantier 22 mai 2026 (source de vérité actionnable)

Quand on demande "analyse ce repo, propose-moi la config CC", la doctrine se trouve ici :

- [[comment-ecrire-claudemd]] — target 200L, 5 anti-patterns Anthropic, compounding Boris
- [[comment-creer-skill]] — 9 catégories Thariq, frontmatter trigger 3e personne
- [[comment-creer-agent]] — 2-agent Justin Young, Sonnet/Opus split, convention 8 couleurs
- [[comment-creer-hook]] — 25+ events, doctrine "rule 100% → hook", Fowler Guides+Sensors
- [[workflow-claude-code-optimal]] — routines Boris + advisor 5× Angela Jiang + leaf nodes Erik
- [[methode-analyser-repo]] (META) — grille 6 étapes pour transformer repo en config CC
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / Bash exploration
- [[pattern-vault-llm-karpathy]] — 3-layers raw/wiki/schema, qmd Tobi Lütke
- [[trail-of-bits-config]] — setup entreprise sécu publique (anti-rationalization Stop hook + 3-tier sandbox)

## Changelog (consolidé par mois)

- [[CC mai 2026 - Code with Claude]] — Desktop GUI, web UI, v2.1.126→v2.1.136, cache TTL fix, memory leak fix
- [[CC avril 2026]] — Opus 4.7, Auto Mode, CLI binaire natif, Windows sans Git Bash, v2.1.110→v2.1.123

## Features (notes existantes)

- [[Computer Use CC]]
- [[Claude Security]]
- [[claude-desktop-preferences]] — Profil, Cowork, pattern vault-first MCP pour non-devs
- [[mcp-obsidian-brain-v2]] — MCP SQLite FTS5 autonome, déployé sur VM, accessible via VPN
- [[cowork-architecture]] — Architecture Cowork, Dispatch, Plugin Marketplace, Agent Teams

## Features (à documenter)

Auto Mode · Effort Levels · Worktrees · Skills System · Hooks System · Agent Teams · Routines · Session Sharing · Remote Control · Dynamic Loop · Plugin Marketplace

## Best Practices

- [[workflow-claude-code-optimal]] — Fleet commander, 5 terminaux, worktrees
- [[delegate-guard-pattern]] — Hook PreToolUse forge-only : bloque edits directs, redirige vers agents spécialisés
- [[methode-analyser-repo]] — 3 rules obligatoires tout projet : check-before-create, quality-gates, learn-from-mistakes
- [[comment-ecrire-claudemd]] — Consensus Boris + Anthropic : 100-200L max, monthly audit
- [[workflow-claude-code-optimal]] — Synthèse Boris, Erik, Thariq, Cat Wu, Karpathy
- [[mcp-vs-cli-vs-skills]] — Quand MCP, quand CLI, quand skill : matrice de décision

## Agents forge (fiches)

- [[Agent — agent-creator]] — Crée/modifie les agents Claude Code
- [[Agent — claudemd-optimizer]] — Optimise les CLAUDE.md
- [[Agent — hook-creator]] — Crée/modifie les hooks
- [[Agent — skill-creator]] — Crée/modifie les skills
- [[Agent — project-analyzer]] — Analyse de projet complet
- [[Agent — project-auditor]] — Audit config .claude/
- [[Agent — self-updater]] — Mise à jour skills de référence

## Dépréciations

- [[Deprecation Haiku 3]]
- [[Deprecation Sonnet 4 Opus 4]]
- [[Deprecation 1M Context Beta]]
- [[Deprecation budget_tokens]]

## Liens


### Ajouts mai 2026

- [[Code with Claude 2026]] — Conférence SF 6 mai : SpaceX, Dreaming, Outcomes, Multi-agent, Routines
- [[Memory Managed Agents]] — Memory = filesystem, permission scopes, optimistic concurrency, version history
- [[Dreaming Managed Agents]] — Review cross-sessions, déduplication, vérification, enrichissement mémoire
- [[workflow-claude-code-optimal]] — Boris setup mai 2026 : mobile-first, /loop partout, 150 PRs/jour