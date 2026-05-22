---
titre: "Angela Jiang"
resume: "Anthropic Claude Platform, doctrine 'advisor strategy 5× cost reduction' (Code with Claude London 19 mai 2026), Haiku/Sonnet executor + Opus advisor, vision Claude self-building"
aliases:
  - "angela jiang"
  - "Angela Jiang"
  - "A. Jiang"
  - "anthropic angela"
  - "advisor strategy anthropic"
  - "angela claude platform"
derniere-maj: 2026-05-22
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

Angela Jiang est la source canonique Anthropic sur **deux doctrines majeures de mai 2026** :

1. **Advisor strategy** — pattern multi-modèles (Haiku/Sonnet executor + Opus advisor) qui a permis à Eve Legal d'obtenir "**frontier model quality at 5× lower cost**". C'est devenu la doctrine officielle Anthropic pour les déploiements production cost-sensitive.
2. **Self-building Claude** — sa vision long terme : "Claude basically being able to build itself."

Elle pilote aussi côté produit l'arsenal Managed Agents : **self-hosted sandboxes** (Daytona/Cloudflare/Vercel/Modal), **MCP tunnels** (`tunnel.anthropic.com`), multiagent orchestration.

## CONTRIBUTIONS CLÉS

### 1. Advisor strategy — Code with Claude London 19 mai 2026

**Citation canonique** (verbatim London 19 mai 2026) :

> "Advisor strategy : Haiku/Sonnet executor + Opus advisor → Eve Legal got frontier model quality at 5× lower cost."
> — Angela Jiang, Code with Claude London 19 mai 2026

**Pattern** :

| Rôle | Modèle | Job |
|------|--------|-----|
| **Executor** | Haiku 4.5 ou Sonnet 4.6 | 90-95% du travail (exécution rapide, low cost) |
| **Advisor** | Opus 4.7 | Consultation ponctuelle sur décisions critiques, edge cases, jugement |

**Résultat client** : Eve Legal a obtenu une qualité équivalente à un déploiement full-Opus pour **1/5e du coût**.

**Implications doctrinales** :
- Ne pas déployer Opus partout par défaut
- Architecture multi-modèles = pattern par défaut en prod
- L'advisor s'invoque uniquement quand l'executor signale un blocage / incertitude
- Cf. [[reference-advisor-pattern]] et [[workflow-claude-code-optimal]]

### 2. Vision self-building Claude — Code with Claude London 19 mai 2026

**Citation canonique** :

> "I think the absolute end state we're trying to get to is Claude basically being able to build itself."
> — Angela Jiang, Code with Claude London 19 mai 2026

C'est la vision long terme officielle Anthropic : Claude qui construit, déploie, teste et améliore Claude. Cohérent avec Mythos (Anthropic preview), Dreaming, et le roadmap continuous task horizon de Lisa Crofoot.

### 3. Self-hosted sandboxes (annonce London)

Annonce majeure portée par Angela Jiang à London :

- Agents tournent sur l'infra cliente (Daytona, Cloudflare, Vercel, Modal)
- Compliance + isolation + control
- Pattern : managed agents avec sandbox custom client

### 4. MCP tunnels (annonce London)

- `tunnel.anthropic.com` — gateway dans le réseau privé client
- Accès à des MCP servers internes derrière firewall
- Use-case : data warehouse, systèmes internes via firewall

Co-démontré dans la demo Counter (e-commerce fictive) à London — agent "Growthbot" sur Slack qui requête un data warehouse interne via MCP tunnel.

### 5. Webhooks et infrastructure Managed Agents

Spécification technique portée par Angela / Katelyn Lesse :

- **At-least-once delivery**
- **No ordering guarantee**
- `X-Webhook-Signature` avec **5-min replay protection**

C'est la doctrine officielle Anthropic pour intégrer Managed Agents dans une infra existante (CI, GitHub, Slack, custom backends).

## VERBATIM NOTABLES

> "Advisor strategy : Haiku/Sonnet executor + Opus advisor → Eve Legal got frontier model quality at 5× lower cost."
> — Angela Jiang, Code with Claude London 19 mai 2026

> "I think the absolute end state we're trying to get to is Claude basically being able to build itself."
> — Angela Jiang, Code with Claude London 19 mai 2026

## APPLICATION FORGE (mai 2026)

L'advisor strategy d'Angela Jiang inspire directement le **model allocation strategy** appliqué dans forge (cf. mémoire `feedback_all_opus`) :

- **Sonnet pour exécution** (most agents, effort: high)
- **Opus pour jugement** (architect, dev-lead, devils-advocate, advisor)
- Validé Raphael 21 mai 2026

Voir [[workflow-claude-code-optimal]] pour l'application complète du pattern.

## CORRECTIONS D'ATTRIBUTION (chantier 22 mai 2026)

Le verbatim "advisor strategy 5× cost reduction" était initialement attribué à **Cat Wu** dans certaines notes — correction faite le 22 mai 2026 : il s'agit bien de **Angela Jiang** à Code with Claude London 19 mai 2026.

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
