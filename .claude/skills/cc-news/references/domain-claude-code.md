# Domaine — Claude Code & Écosystème Anthropic

Couvre : Claude Code lui-même, l'équipe officielle, les frameworks ecosystem (LangChain, MCP, DSPy).
Nombre de queries : 18 — **Découper sur 2 agents** (Agent A + Agent B)

## Sources officielles

1. `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. `https://docs.anthropic.com/en/release-notes/claude-code`
3. `https://code.claude.com/docs/en/changelog`
4. `https://howborisusesclaudecode.com`

## Équipe Claude Code

| Personne | Rôle | Sources |
|----------|------|---------|
| **Boris Cherny** (@bcherny) | Créateur de Claude Code | x.com/bcherny, threads.com/@boris_cherny |
| **Cat Wu** (@_catwu) | Head of Product Claude Code | x.com/_catwu |
| **Lydia Hallie** (@lydiahallie) | Claude Code team | x.com/lydiahallie |
| **Noah Zweben** (@noahzweben) | Claude Code team | x.com/noahzweben |
| **Thariq Shihipar** (@trq212) | Skills author, Claude Code team | x.com/trq212, linkedin.com/in/thariq |
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
