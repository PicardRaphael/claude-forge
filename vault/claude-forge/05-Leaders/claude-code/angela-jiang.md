---
titre: "Angela Jiang"
resume: "Anthropic Claude Platform, keynote Code with Claude London 19 mai 2026, vision Self-building Claude, Self-hosted sandboxes Managed Agents, MCP tunnels, Webhooks spec"
aliases:
  - "angela jiang"
  - "Angela Jiang"
  - "A. Jiang"
  - "anthropic angela"
  - "self-building claude"
  - "angela claude platform"
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=AgQ4cwL5eOM"
  - "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
  - "https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/"
type: "leader"
tags:
  - "#type/leader"
  - "#domaine/claude-code"
  - "#org/anthropic"
---

## QUI

- **Rôle** : Anthropic — Claude Platform / Managed Agents (advisor strategy, multiagent orchestration)
- **Org** : Anthropic
- **Période active** : 2025 → présent (référence canonique mai 2026)
- **Apparitions publiques majeures** :
  - Keynote d'ouverture Code with Claude London 19 mai 2026 (9-10am BST) aux côtés de Boris Cherny, Cat Wu, Lisa Crofoot, Katelyn Lesse
  - Talk "Advisor strategy" Code with Claude SF (6-7 mai 2026) avec Brad Abrams + Katelyn Lesse

## POURQUOI ELLE EST PERTINENTE

Angela Jiang est la source canonique Anthropic sur **trois doctrines majeures de mai 2026** :

1. **Self-building Claude** — sa vision long terme : "Claude basically being able to build itself."
2. **Self-hosted sandboxes Managed Agents** — Daytona/Cloudflare/Vercel/Modal (annonce London).
3. **MCP tunnels + Webhooks spec** — `tunnel.anthropic.com`, at-least-once delivery, X-Webhook-Signature.

⚠️ **L'Advisor Strategy n'est PAS d'elle** — c'est Brad Abrams (CwC SF avec Mario Rodriguez). Coquille corrigée 23 mai 2026 : cf [[Brad-Abrams]] et [[workflow-claude-code-optimal]].

Elle pilote aussi côté produit l'arsenal Managed Agents : **self-hosted sandboxes** (Daytona/Cloudflare/Vercel/Modal), **MCP tunnels** (`tunnel.anthropic.com`), multiagent orchestration.

## CONTRIBUTIONS CLÉS

### 1. Vision self-building Claude — Code with Claude London 19 mai 2026

**Citation canonique** :

> "I think the absolute end state we're trying to get to is Claude basically being able to build itself."
> — Angela Jiang, Code with Claude London 19 mai 2026

C'est la vision long terme officielle Anthropic : Claude qui construit, déploie, teste et améliore Claude. Cohérent avec Mythos (Anthropic preview), Dreaming, et le roadmap continuous task horizon de Lisa Crofoot.

### 2. Self-hosted sandboxes (annonce London)

Annonce majeure portée par Angela Jiang à London :

- Agents tournent sur l'infra cliente (Daytona, Cloudflare, Vercel, Modal)
- Compliance + isolation + control
- Pattern : managed agents avec sandbox custom client

### 3. MCP tunnels (annonce London)

- `tunnel.anthropic.com` — gateway dans le réseau privé client
- Accès à des MCP servers internes derrière firewall
- Use-case : data warehouse, systèmes internes via firewall

Co-démontré dans la demo Counter (e-commerce fictive) à London — agent "Growthbot" sur Slack qui requête un data warehouse interne via MCP tunnel.

### 4. Webhooks et infrastructure Managed Agents

Spécification technique portée par Angela / Katelyn Lesse :

- **At-least-once delivery**
- **No ordering guarantee**
- `X-Webhook-Signature` avec **5-min replay protection**

C'est la doctrine officielle Anthropic pour intégrer Managed Agents dans une infra existante (CI, GitHub, Slack, custom backends).

## VERBATIM NOTABLES

> "I think the absolute end state we're trying to get to is Claude basically being able to build itself."
> — Angela Jiang, Code with Claude London 19 mai 2026

## APPLICATION FORGE (mai 2026)

Le model allocation strategy de forge (Sonnet exécution / Opus jugement) suit la doctrine **Brad Abrams** Advisor Strategy (PAS Angela Jiang, coquille corrigée 23 mai) — cf [[Brad-Abrams]] et [[workflow-claude-code-optimal]].

Angela Jiang contribue par ailleurs à la vision Self-building Claude qui motive le compounding forge (CLAUDE.md évolutif).

## CORRECTIONS D'ATTRIBUTION (audit dogfooding 23 mai 2026)

**Avant 22 mai** : l'Advisor Strategy "5× cost reduction" était attribuée à tort à Cat Wu.
**22 mai (correction partielle)** : forge a re-attribué à Angela Jiang sur foi d'une mention Simon Willison "Angela Kiang" — interprétation erronée.
**23 mai (correction définitive)** : source canonique = **Brad Abrams** (CwC SF avec Mario Rodriguez GitHub), verbatim "close to Opus-level intelligence at much lower prices" (pas de "5×" verbatim). Cf [[Brad-Abrams]].

## WIKILINKS

- [[Boris Cherny]] — co-keynote London 19 mai 2026
- [[cat-wu]] — co-keynote London 19 mai 2026
- [[lisa-crofoot]] — co-keynote London 19 mai 2026 (scaffolding)
- [[comment-ecrire-claudemd]] — CLAUDE.md doit refléter le pattern advisor
- [[comment-creer-skill]] — skills peuvent appeler advisor pattern
- [[comment-creer-agent]] — agents = exécuteurs vs advisors (Opus)
- [[workflow-claude-code-optimal]] — advisor strategy = pattern central
- [[methode-analyser-repo]] — audit du pattern advisor dans repos

## SOURCES

### Sources primaires (Anthropic / équipe Claude Code)

- [Code with Claude London 2026 — full livestream YouTube AgQ4cwL5eOM](https://www.youtube.com/watch?v=AgQ4cwL5eOM) — keynote 19 mai 2026 (advisor strategy + self-building)

### Sources secondaires

- [MIT Tech Review — coding's future](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
- [Fortune — London as AI-coding goes mainstream](https://fortune.com/2026/05/21/claude-code-london-anthropic-ai-software-engineering/)

### Notes internes chantier 22 mai 2026

- `recherche-youtube-talks.md` §1.2 + §1.3 + §2.3 (advisor strategy)
- `recherche-youtube-watch-vibe-coding.md` (corroboration)
- `audit-qualite-rapports-chantier.md` (citations confirmées)
- `PLAN-EXECUTION-FINAL.md` §4 (corrections d'attribution)
