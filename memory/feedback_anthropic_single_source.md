---
name: anthropic-single-source-suffit
description: "Directive Raphael 23 mai 2026 — SCOPE CLAUDE/ANTHROPIC seulement. Sur audit Claude Code, Anthropic team = single source acceptable. Sur audits thèmes larges (prompt engineering général, RAG, agents IA, fine-tuning, leaders industrie), Anthropic n'est PAS la référence — les meilleurs du domaine le sont."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 931783ff-d35c-4d9c-b53d-c30bcf6f294f
---

**Verbatim Raphael** (23 mai 2026 pendant audit thématique vault Claude Code) :
> "Tout ce que tu vois de l'équipe Anthropic sont valide pour information même si tu le valide pas par 3 4 autres personnes"

**Précision Raphael** (même session, après audit Claude Code) :
> "Tant trop pic, attention, c'est le gnostique c'était que ce qui est lié à l'entreprise [Anthropic], là c'est différent, donc ce n'est pas n'importe quoi non. Par contre, c'est toujours les meilleurs de la société, mais là, on est moins bloqué sur Anthropic"

## Règle finale corrigée

**Principe général** : provider/auteur officiel sur SON propre produit ou SA propre recherche = single source acceptable. Hors de son scope = règle 4+ sources.

### Single source suffit pour ✅ canonique

- **Anthropic team / docs / blog** sur **Claude / Claude Code / Anthropic produits**
- **OpenAI** sur **GPT / leurs produits**
- **Google** sur **Gemini / leurs produits**
- **Meta** sur **Llama / leurs produits**
- **Papers académiques peer-reviewed** (arXiv conférences ACL/EMNLP/NeurIPS/ICML)
- **Docs officielles** d'un framework (LangChain, CrewAI, Unsloth, etc.) sur LEUR produit
- **LinkedIn/X officiel d'un leader** sur son propre rôle/affiliation
- **Auteur original** d'un pattern/concept sur sa propre création (ex: Willison sur lethal trifecta, Karpathy sur LLM Wiki, Dettmers sur QLoRA)

### Externes/tiers parlant d'un sujet HORS de leur scope

- **4+ sources convergentes obligatoire**
- Couverture presse tech reconnue (Fortune, MIT Tech Review, TechCrunch) = 2+ sources convergentes
- Blogs / Medium / DEV community = 4+ sources convergentes

## Application par thème audit-vault-thematique

| Thème | Sources primaires (single source acceptable) | Sources secondaires (4+ requis) |
|-------|-----|-----|
| 01-Claude Code | Anthropic team/docs/blog | Externes (Fowler, Hashimoto, Osmani, Willison non-Anthropic) |
| 02-Prompt Engineering | Amanda Askell (Anthropic), DAIR.AI, LearnPrompting, Wei/Zhou (papers), Willison, Karpathy | Blogs tiers Medium |
| 03-RAG | Kiela, Lewis, Khattab, Reimers, Xiao, Kamradt, Chase, Liu + papers arXiv | Blogs tiers |
| 04-Agents IA | Ng, Weng, Chase, Liu, Yao, Moura, Nakajima, Wang, Fan, Shapiro + papers | Blogs tiers |
| 05-Fine-tuning | Dettmers, Hu, Han, Dao, Han Song, Gerganov, Raschka + papers arXiv | Blogs tiers (Anthropic quasi non-pertinent) |
| 06-Patterns/Context | Karpathy, Boris, Erik, Thariq, Böckeler, Fowler, Hashimoto, Osmani, Willison, Lütke + Anthropic docs context | Blogs tiers |
| 07-Leaders/Industrie | LinkedIn/X officiel du leader + datasheets providers + presse tech reconnue | Blogs tiers |
| 08-claude-forge dogfooding | Vault canoniques forge eux-mêmes | — |

## Anti-pattern à éviter

**Faire de "Anthropic single source" une règle absolue cross-thèmes** = écrabouille les sources primaires des autres domaines. Si tu audites RAG, Douwe Kiela > Anthropic sur le sujet. Si tu audites fine-tuning, Tim Dettmers > Anthropic.

## How to apply

- Avant chaque audit thématique, lire le prompt thématique qui liste explicitement ses sources primaires
- Si une claim est attribuée à Anthropic mais concerne un sujet plus large (prompt eng général, RAG, etc.) → vérifier que ce n'est pas une extrapolation forge
- Si une claim cite Anthropic + une source externe sur le même point → privilégier la source du domaine (auteur original > paraphrase Anthropic)

## Why

Audit Claude Code 23 mai a validé "Anthropic single source" pour le thème Anthropic. Mais Raphael a précisé : c'était scoped. Sur les autres thèmes, le meilleur du domaine reste la source primaire — Anthropic n'est qu'un acteur parmi d'autres.
