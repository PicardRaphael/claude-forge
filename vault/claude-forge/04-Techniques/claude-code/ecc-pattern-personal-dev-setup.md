---
aliases:
  - ECC pattern
  - Everything Claude Code pattern
  - personal dev setup pattern
  - pattern 47 agents
  - hackathon winner architecture
  - production claude code setup
resume: "Pattern ECC (Affaan Mustafa, hackathon winner Anthropic) — 28-47 agents + 119-181 skills + 60-79 commands pour DEV personnel avec Claude Code. Différent du pattern 'agent client minimum' de Will. Forge s'en est écarté délibérément : la volumétrie ECC est un point de comparaison, pas une cible."
derniere-maj: 2026-09-05
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#statut/canonique"
---

# Pattern ECC — Personal Dev Setup avec Claude Code

## Source

[[affaan-mustafa-ecc-hackathon-winner]] — Grand Prize Anthropic Hacker Marathon 2026.

Repo : `affaan-m/everything-claude-code` — jury Anthropic (Boris Cherny, Cat Wu, Thariq Shihpar, etc.)

## Pattern central

Volumétrie du setup ECC, en regard de forge **mesuré le 5 septembre 2026** :

| Composant | ECC v1.9.0 | Forge (5 sept. 2026) |
|-----------|------------|----------------------|
| Agents | 28-47 | **5** (+ 4 côté Codex) |
| Skills | 119-181 | **51** (+ 59 adaptateurs `.agents/`) |
| Slash commands | 60-79 | **0** — tous convertis en skills |
| Hooks | présents | **20** |
| Rules | — | **12** |
| MCP configs | présents | **2** |
| Memory persistence | oui | oui (MEMORY.md + vault) |
| Security scanner | AgentShield | hooks delegate-guard + security-guard |

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

→ Pattern transposé à forge : skill `agentshield-like-scanner`.

## Différence Will (talk CwC London) vs ECC

| Axe | Will Stock Pilot | ECC personal dev |
|-----|------------------|------------------|
| Audience | Agent LIVRÉ à un client | Setup PERSONNEL pour dev |
| Objectif | Minimiser tokens/latency en prod | Maximiser productivité dev |
| Agents | 1 orchestrateur + 1 sub-agent forecasting | 28-47 spécialisés |
| Skills | Skills > tools, progressive disclosure | Skills nombreuses + tools nombreux |
| Sub-agents | Minimum (frontier models can manage) | Beaucoup, par spécialité |

**Résolution du paradoxe** : pas la même chose. Les deux sont vrais dans leur contexte.

## Implications pour forge — la volumétrie ECC n'est PAS une cible

L'ancienne lecture de cette note (mai 2026) traitait l'écart avec ECC comme un retard à combler :
« forge est en 6 mois → 16 agents, cohérent » et « sous-dimensionné en skills : 30 vs 119-181, gap à
investiguer ». **Les deux conclusions sont infirmées par ce que forge a mesuré depuis.**

1. **Sur les agents, forge a divergé volontairement.** Le pivot du 6 juin 2026 a fait l'inverse
   d'accumuler : créateurs convertis en skills du thread principal, trois auditeurs fusionnés dans
   `repo-inspector`. 16 → 5. Le plafond de délégation forge (un sous-agent à la fois, fan-out justifié
   par des périmètres disjoints) rend une flotte de 47 agents contraire à la doctrine, pas en retard
   sur elle.
2. **Sur les skills, le volume a un coût mécanique.** Le budget de listing (`skillListingBudgetFraction`,
   1 % du contexte) fait **droper des descriptions entières** des skills les moins utilisées au-delà du
   seuil — ordre de grandeur confortable : 15-25 skills à 200K. Viser 119-181 dégraderait la découverte
   de tout le corpus. Cf [[comment-creer-skill]].
3. **Sur les commands, la migration est terminée** : 0 slash command legacy, tout est skill.
4. **Ce qui reste valide d'ECC** : les couches (skills/rules/hooks/agents/MCP/mémoire) comme grille de
   lecture d'un setup, et le pipeline red/blue/auditor d'AgentShield.

## Anti-patterns à éviter

- ❌ Confondre les 2 patterns ("Will dit minimum d'agents" appliqué à un setup dev = erreur)
- ❌ **Traiter une volumétrie observée chez un tiers comme un objectif** — c'est l'erreur que portait
  cette note. Un compte d'agents ou de skills se justifie par des périmètres et un budget de contexte,
  jamais par comparaison
- ❌ Empiler agents sans threshold mesuré (cf [[google-mit-scaling-agent-systems-2025]] : si single agent > 45% success, sub-agent inutile)
- ❌ Sequential coordination sur tâches dépendantes (dégrade 39-70% selon Google/MIT)

## Liens

- [[affaan-mustafa-ecc-hackathon-winner]]
- [[google-mit-scaling-agent-systems-2025]] — threshold 45%
- [[software-factory-pattern-2026]] — pattern intermédiaire communauté
- [[will-vs-ecc-deux-doctrines-anthropic]] — critique résolutive
- [[agent-teams-natif-anthropic]] — orchestrateur officiel
- [[comment-creer-skill]] — budget de listing, pourquoi le volume de skills se paie

## Référence

- [GitHub ECC](https://github.com/affaan-m/everything-claude-code)
- [Augment Code analyse](https://www.augmentcode.com/learn/everything-claude-code-github)
