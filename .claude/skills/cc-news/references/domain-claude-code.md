# Domaine — Claude Code & Écosystème Anthropic

Couvre : Claude Code lui-même, l'équipe officielle, les frameworks ecosystem (LangChain, MCP, DSPy).
Nombre de queries : 18 — **Découper sur 2 agents** (Agent A + Agent B)

## Sources officielles

1. `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. `https://docs.anthropic.com/en/release-notes/claude-code`
3. `https://code.claude.com/docs/en/changelog`
4. `https://howborisusesclaudecode.com`

<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->

## Leaders canonisés (15) — vault 05-Leaders/claude-code/

| Personne | Rôle | Sources |
|----------|------|---------|
| **Affaan Mustafa** | Affaan Mustafa — Grand Prize Anthropic Hacker Marathon 2026 avec Everything Claude Code… | — |
| **Alex Albert** | Head of Claude Relations | — |
| **Angela Jiang** | Anthropic Claude Platform, keynote Code with Claude London 19 mai 2026, vision Self-bui… | www.youtube.com, www.technologyreview.com |
| **Boris Cherny** (@bcherny) | Creator of Claude Code | howborisusesclaudecode.com, x.com |
| **Brad Abrams** (@brada) | Product Management Lead Claude chez Anthropic, ex-Google/Microsoft. Créateur de l'Advis… | www.linkedin.com, x.com |
| **Cat Wu** (@_catwu) | Head of Product Claude Code + Cowork chez Anthropic, co-pilote du produit avec Boris Ch… | www.youtube.com, every.to |
| **Daisy Hollman** | Member of Technical Staff (MTS) | www.youtube.com, www.youtube.com |
| **Erik Schluntz** (@ErikSchluntz) | Member of Technical Staff & Co-founder | youtube.com, x.com |
| **Jeremy Hadfield** | Anthropic — Claude Code team | www.youtube.com, www.technologyreview.com |
| **Justin Young** | Member of Technical Staff (MTS) | www.anthropic.com, github.com |
| **Lisa Crofoot** | Research PM Anthropic, doctrine 'scaffolding holds Claude back' (Code with Claude Londo… | www.youtube.com, www.technologyreview.com |
| **Lydia Hallie** (@lydiahallie) | Claude Code team | x.com, frontendmasters.com |
| **Mitchell Hashimoto** | Co-founder HashiCorp, créateur Ghostty. A popularisé le terme 'harness engineering' (5… | mitchellh.com, ghostty.org |
| **Noah Zweben** | Anthropic — Engineering | Code with Claude London, 19 mai 2026 |
| **Thariq Shihipar** (@trq212) | Skills Author, Claude Code team | x.com, linkedin.com |

> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer la fiche dans `05-Leaders/claude-code/` puis relancer `py scripts/sync-leaders.py`.
> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.

<!-- SYNC:leaders:end -->

## Watchlist signaux non canonisés

> Cibles suivies par cc-news mais sans fiche vault dédiée. Section éditable à la main, **jamais touchée par le sync**. Promouvoir en fiche `05-Leaders/claude-code/` quand mérité.

| Personne | Rôle | Sources |
|----------|------|---------|
| **Jarred Sumner** (@jaraboron) | Bun creator, acquis par Anthropic | x.com/jaraboron |
| **Felix Rieseberg** (@felixrieseberg) | Claude Code contributor | x.com/felixrieseberg |

## Écosystème & frameworks

| Source | Handle | Domaine |
|--------|--------|---------|
| **LangChain** | @LangChainAI | Framework agents/RAG |
| **Claude officiel** | @AnthropicAI | Compte officiel Anthropic |
| **Claude Code Log** | @ClaudeCodeLog | Changelog et tips Claude Code communautaires |
| **Claude Devs** | @ClaudeDevs | Communauté développeurs Claude |
| **Google AI Studio** | @GoogleAIStudio | Gemini platform |
| **HuggingFace** | — | Transformers, PEFT, TRL |
| **DSPy** | @lateinteraction | Programmable foundation models |
| **MCP Protocol** | — | Model Context Protocol |

## Queries à exécuter (6-8 par run)

### Agent A — Officiel + Équipe
```
Claude Code changelog site:github.com/anthropics/claude-code
Claude Code deprecated OR breaking
@bcherny Claude Code
@_catwu Claude Code
@lydiahallie Claude Code
@noahzweben OR @trq212 OR @jaraboron Claude Code
@ClaudeCodeLog OR @ClaudeDevs Claude Code
```

### Agent B — Plugins + Écosystème
```
site:github.com/anthropics claude-code-setup plugin update
@LangChainAI LangChain LangGraph new features changelog
@AnthropicAI Claude announcements
HuggingFace transformers PEFT TRL new release
DSPy new features update
MCP protocol model context protocol update
Claude Cowork OR Dispatch new features
anthropic Agent Teams claude code
```

### Agent C — Équipe élargie Anthropic (postent moins souvent)
```
Brad Abrams Anthropic Claude product
@ErikSchluntz Claude Code agents
@alexalbert__ Claude Code
Angela Jiang OR Lisa Crofoot Anthropic Code with Claude
Jeremy Hadfield OR Daisy Hollman OR Justin Young Anthropic
Mitchell Hashimoto harness engineering Ghostty
Affaan Mustafa Everything Claude Code ECC
```

## Note agent
Si $ARGUMENTS est fourni, ajouter une query spécifique :
```
Claude Code $ARGUMENTS
```
Vérifier aussi les plugins officiels :
```
Read("~/.claude/plugins/cache/claude-plugins-official/claude-code-setup/*/. claude-plugin/plugin.json")
```
(adapter le chemin selon l'OS : $HOME/.claude sur Unix, %USERPROFILE%\.claude sur Windows)
