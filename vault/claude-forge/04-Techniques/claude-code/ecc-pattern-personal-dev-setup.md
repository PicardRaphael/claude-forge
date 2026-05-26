---
aliases:
  - ECC pattern
  - Everything Claude Code pattern
  - personal dev setup pattern
  - pattern 47 agents
  - hackathon winner architecture
  - production claude code setup
resume: "Pattern ECC (Affaan Mustafa, hackathon winner Anthropic) — 28-47 agents + 119-181 skills + 60-79 commands pour DEV personnel avec Claude Code. Différent du pattern 'agent client minimum' de Will."
derniere-maj: 2026-05-26
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Pattern ECC — Personal Dev Setup avec Claude Code

## Source

[[affaan-mustafa-ecc-hackathon-winner]] — Grand Prize Anthropic Hacker Marathon 2026.

Repo : `affaan-m/everything-claude-code` — 154K stars, jury Anthropic (Boris Cherny, Cat Wu, Thariq Shihpar, etc.)

## Pattern central

Pour DÉVELOPPER avec Claude Code de façon productive, viser :

| Composant | ECC v1.9.0 | Forge actuel (mai 2026) |
|-----------|------------|-------------------------|
| Agents | 28-47 | 16 |
| Skills | 119-181 | ~30 |
| Slash commands | 60-79 | ~15 |
| Hooks | présents | 14 |
| MCP configs | présents | 4 |
| Memory persistence | oui | oui (MEMORY.md + vault) |
| Security scanner | AgentShield | hooks delegate-guard |

## Couches

1. **Skills** : how-to production-ready packagés
2. **Rules** : conventions du repo
3. **Hooks** : automation lifecycle events
4. **Agent definitions** : sub-agents spécialisés
5. **MCP configurations** : data access
6. **Legacy command shims** : compatibilité
7. **Memory persistence** : continuité sessions

## AgentShield — pattern sécurité

CLI dédié `npx ecc-agentshield scan` qui audite EN PRODUCTION :
- CLAUDE.md
- settings.json
- MCP configs
- hooks
- agent definitions
- skills

Pipeline `--opus` :
- **Red team agent Opus** : trouve exploit chains
- **Blue team agent Opus** : évalue protections
- **Auditor agent Opus** : synthétise en priorities

→ Pattern transposable à forge pour audit `.claude/` cross-repo.

## Différence Will (talk CwC London) vs ECC

| Axe | Will Stock Pilot | ECC personal dev |
|-----|------------------|------------------|
| Audience | Agent LIVRÉ à un client | Setup PERSONNEL pour dev |
| Objectif | Minimiser tokens/latency en prod | Maximiser productivité dev |
| Agents | 1 orchestrateur + 1 sub-agent forecasting | 28-47 spécialisés |
| Skills | Skills > tools, progressive disclosure | Skills nombreuses + tools nombreux |
| Sub-agents | Minimum (frontier models can manage) | Beaucoup, par spécialité |

**Résolution du paradoxe** : pas la même chose. Les deux sont vrais dans leur contexte.

## Implications pour forge

1. **Forge ressemble à ECC, pas à Stock Pilot**. C'est un setup dev personnel multi-projet (ia_back, neo_ia, neoteem-brain, lojii).
2. **Trajectoire 10 mois Affaan → 47 agents**. Forge est en 6 mois → 16 agents. Cohérent.
3. **Sous-dimensionné en skills** : 30 vs 119-181 ECC. Gap potentiel à investiguer.
4. **AgentShield → inspiration pour audit forge** : pipeline red/blue/auditor.

## Anti-patterns à éviter

- ❌ Confondre les 2 patterns ("Will dit minimum d'agents" appliqué à un setup dev = erreur)
- ❌ Empiler agents sans threshold mesuré (cf [[google-mit-scaling-agent-systems-2025]] : si single agent > 45% success, sub-agent inutile)
- ❌ Sequential coordination sur tâches dépendantes (dégrade 39-70% selon Google/MIT)

## Liens

- [[affaan-mustafa-ecc-hackathon-winner]]
- [[google-mit-scaling-agent-systems-2025]] — threshold 45%
- [[software-factory-pattern-2026]] — pattern intermédiaire communauté
- [[will-vs-ecc-deux-doctrines-anthropic]] — critique résolutive
- [[agent-teams-natif-anthropic]] — orchestrateur officiel

## Référence

- [GitHub ECC](https://github.com/affaan-m/everything-claude-code)
- [Augment Code analyse](https://www.augmentcode.com/learn/everything-claude-code-github)
