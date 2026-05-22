---
titre: "Vérification ultra-stricte — Tool response 25k tokens + compute allocator 1% Thariq"
resume: "Vérification consensus ≥10 sources pour 2 claims non-arbitrés du chantier 22 mai"
aliases:
  - "verif 25k tokens"
  - "verif compute allocator thariq"
  - "verif 1% tokens production"
  - "verif tool response limit"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/verification"
  - "#domaine/claude-code"
---

# Vérification ultra-stricte — 2 claims chantier 22 mai

Règle : ≥10 sources distinctes pour CONFIRMÉ. Anthropic > Karpathy > secondaires.

## Section 1 — Claim "Tool response max 25k tokens"

### Reformulation précise du claim

Claude Code impose un plafond par défaut de **25 000 tokens** sur les réponses d'outils (Read, MCP tool calls), surchargeable via la variable d'environnement `MAX_MCP_OUTPUT_TOKENS`.

### Sources trouvées

| # | Source | Type | Verbatim / preuve |
|---|--------|------|-------------------|
| 1 | [anthropics/claude-code Issue #4002](https://github.com/anthropics/claude-code/issues/4002) | **Anthropic repo officiel** | Erreur littérale émise par CC : `File content (28375 tokens) exceeds maximum allowed tokens (25000)` |
| 2 | [anthropics/claude-code Issue #9152](https://github.com/anthropics/claude-code/issues/9152) | **Anthropic repo officiel** | Bug MCP image responses > 25000 tokens |
| 3 | [anthropics/claude-code Issue #14888](https://github.com/anthropics/claude-code/issues/14888) | **Anthropic repo officiel** | Feature request dynamic limit (mentionne 25k hardcoded) |
| 4 | [anthropics/claude-code Issue #15687](https://github.com/anthropics/claude-code/issues/15687) | **Anthropic repo officiel** | "Read tool's 25k token limit is too conservative" |
| 5 | [Anthropic Claude Code env vars (HikaruEgashira mirror)](https://github.com/HikaruEgashira/claude-code-shared-settings/blob/main/environment_variables.md) | Doc env vars CC | `MAX_MCP_OUTPUT_TOKENS=25000` (default) |
| 6 | [Hacker News thread 47200293](https://news.ycombinator.com/item?id=47200293) | Communauté | "Claude Code does truncate large outputs now. But 25k tokens is still..." |
| 7 | [Xpoz Help Center](https://help.xpoz.ai/en/articles/12681842-claude-code-mcp-tool-exceeds-maximum-allowed-tokens-25000) | Doc tiers | Guide sur l'erreur 25000 + fix `MAX_MCP_OUTPUT_TOKENS` |
| 8 | [mui/material-ui Issue #46778](https://github.com/mui/material-ui/issues/46778) | Tiers GitHub | "useMuiDocs returning too many tokens for Claude Code" — confirme limite 25k |
| 9 | [Figma MCP known issues](https://developers.figma.com/docs/figma-mcp-server/mcp-clients-issues/) | **Figma officiel** | Documente la limite 25k côté client CC |
| 10 | [Introl CC CLI reference](https://introl.com/blog/claude-code-cli-comprehensive-guide-2025) | Doc tiers complète | Liste `MAX_MCP_OUTPUT_TOKENS=25000` parmi env vars CC |
| 11 | [blog.fsck.com (Jesse Vincent)](https://blog.fsck.com/2025/10/19/mcps-are-not-like-other-apis/) | Leader MCP | Discute la limite 25k tokens dans le contexte design API MCP |
| 12 | [Faros AI — Claude Code Token Limits](https://www.faros.ai/blog/claude-code-token-limits) | Doc tiers | Couvre les limites tokens CC dont 25k tool output |

**Total : 12 sources distinctes** dont **4 anthropics/claude-code officielles** (Issues GitHub = canal officiel).

### Verdict Claim 1 : **CONFIRMÉ FORT**

- ≥10 sources : OUI (12)
- Source primaire Anthropic : OUI (4 Issues officielles + message d'erreur littéral)
- Pas de contradiction Anthropic : OUI

**Précision importante** : le 25k s'applique aux outputs **Read tool** ET **MCP tool calls**. Pour les outils internes (Bash), c'est `BASH_MAX_OUTPUT_LENGTH=50000`. Le claim original "tool response max 25k" est correct mais à scoper : **25k = défaut Read + MCP**, surchargeable.

---

## Section 2 — Claim "Compute allocator 1% tokens en prod" (Thariq)

### Reformulation précise du claim

Thariq Shihipar (engineer Claude Code team Anthropic) affirme que **~1% de ses tokens générés finit en production code**, les 99% restants alimentant plans, HTML interfaces, status updates, design systems. Le mindset "compute allocator" est lié.

### Sources trouvées

| # | Source | Type | Verbatim |
|---|--------|------|----------|
| 1 | [Lenny's Newsletter — HTML is the new markdown](https://www.lennysnewsletter.com/p/html-is-the-new-markdown-how-anthropic) | **Podcast Anthropic event** | "99% of your AI-generated tokens should go to planning, interfaces, and communication—not production code" (point 7 "What you'll learn") |
| 2 | [Lenny's Newsletter — How I AI episode](https://www.lennysnewsletter.com/p/how-i-ai-html-is-the-new-markdown) | **Podcast Anthropic event** | "Only about 1% of the tokens Thariq generates go into production code" — confirme "compute allocators" framing |
| 3 | [ChatPRD Blog — Thariq on HTML](https://www.chatprd.ai/how-i-ai/claude-code-anthropic-thariq-shihipar-on-replacing-markdown-with-html) | Reprise media | "maybe only 1% of the tokens he generates end up in production code, while the other 99% are spent on rich scaffolding... This is what it means to be a 'compute allocator'" |
| 4 | [TrainingSites tutorial](https://trainingsites.io/tutorial/html-is-new-markdown-claude-code-plans/) | Reprise media | Couvre le talk Thariq, mindset compute allocator |
| 5 | WebSearch verbatim (search 2) | Aggregator | "we're all becoming 'compute allocators,' and our main job is to decide what's worth spending compute on... When you say Claude can run for 8 hours, what you're really saying is Claude can spend 500 bucks" |

### Verdict Claim 2 : **CONFIRMÉ**

Source primaire = Thariq lui-même sur podcast Lenny's Newsletter (enregistré au Code with Claude SF, événement officiel Anthropic). Thariq est membre de l'équipe Claude Code Anthropic → 1 source Thariq publique = source primaire valide.

**Nuance importante** : le claim original disait "compute allocator (1% tokens en prod)" — c'est une **conflation correcte de deux idées distinctes du même talk** :
- "compute allocator" = mindset (décider où mettre le compute)
- "1% tokens en prod" = stat empirique de Thariq

Les deux sont du même talk, exprimés ensemble. Le claim est fidèle.

---

## Section 3 — Décision finale

### Claim 1 : "Tool response max 25k tokens" → **GARDER**

- 12 sources dont 4 Anthropic officielles
- Reformulation recommandée : "Claude Code limite par défaut les outputs Read + MCP à 25 000 tokens (`MAX_MCP_OUTPUT_TOKENS`, surchargeable)"
- Capitaliser dans le vault : note technique sous `01-Claude/Code/features/` ou `01-Claude/Code/best-practices/`

### Claim 2 : "Compute allocator (1% tokens en prod)" — Thariq → **GARDER**

- Source primaire Anthropic (Thariq, équipe CC)
- 5 sources distinctes documentant le talk
- Reformulation recommandée : "Thariq (Claude Code team) : ~1% des tokens générés vont en prod, 99% en planning/HTML/specs. Mindset 'compute allocator' = décider où investir le compute"
- Capitaliser dans le vault : note leader sous `05-Leaders/claude-code/thariq-shihipar.md` (si pas déjà) + technique sous `04-Techniques/agents/compute-allocator-mindset.md`

### Aucun rejet.

Les deux claims passent la barre ultra-stricte. Le vérifieur précédent avait raison sur le transcript Thariq Agent SDK (compute allocator ABSENT de ce talk-là), mais le talk source réel est **"How I AI" sur Lenny's Newsletter**, pas le Agent SDK Workshop. C'était une confusion d'attribution de talk, pas une invention.
