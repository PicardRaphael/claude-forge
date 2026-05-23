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
derniere-maj: 2026-05-23
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
- [[comment-creer-skill]] — 9 catégories Thariq (post Anthropic mars 2026), frontmatter trigger 3e personne, règle ~250 chars auto-trigger
- [[comment-creer-agent]] — 2-agent Justin Young (sans split modèles), Sonnet/Opus split doctrine forge (Cat Wu + Brad Abrams), convention 8 couleurs
- [[comment-creer-hook]] — **29 events officiels**, timeouts 600s/30s/60s par type, doctrine "rule 100% → hook", Böckeler Guides+Sensors
- [[workflow-claude-code-optimal]] — routines Boris + **Advisor Strategy Brad Abrams** + leaf nodes Erik
- [[methode-analyser-repo]] (META) — grille 6 étapes + pipeline architect→dev→reviewer→test
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / Bash exploration, lethal trifecta = Willison
- [[pattern-vault-llm-karpathy]] — 3-layers raw/wiki/schema, qmd Tobi Lütke
- [[trail-of-bits-config]] — setup entreprise sécu publique (anti-rationalization Stop hook + 3-tier sandbox)
- [[methode-pivoter-doctrine]] — checklist 5 étapes pour pivot doctrinal sans régression silencieuse
- [[comparaison-skill-anthropic-claude-code-setup]] — vault forge vs skill officielle (15× plus profond, 3 bits utiles repris)

## ⚙️ Rules transverses

- `.claude/rules/sequence-canonique-modification.md` — séquence A→B→C→D→E obligatoire pour création/modification/optimisation

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

### Leaders ajoutés audit 23 mai 2026

- [[Brad-Abrams]] — Product Lead Anthropic, créateur Advisor Strategy (CwC SF avec Mario Rodriguez GitHub)
- [[Mitchell-Hashimoto]] — popularisateur "harness engineering" (5 fév 2026)