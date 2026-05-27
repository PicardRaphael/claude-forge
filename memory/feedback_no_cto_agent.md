---
name: no-cto-orchestrator-agent
description: Ne JAMAIS créer d'agent CTO/orchestrateur. La session principale est l'orchestrateur. Routing dans CLAUDE.md. Un subagent ne peut pas spawner de sub-agents.
type: feedback
---

## Ne JAMAIS créer d'agent orchestrateur (CTO, conductor, lead)

La session principale Claude Code EST l'orchestrateur. Le routing se fait dans CLAUDE.md.

**Why:** Testé 5 fois avec différentes configs. Un agent CTO :
- Avec Bash/Grep/Read → fait le travail lui-même au lieu de déléguer
- Sans outils → ne peut pas fonctionner, l'outil Agent ne marche pas
- Issue GitHub #19077 : un subagent ne peut PAS spawner de sub-agents (by design)
- Boris ne l'utilise pas — session principale + CLAUDE.md

**How to apply:**
- La session principale lit CLAUDE.md → section "Agent Routing" → dispatch aux agents
- CLAUDE.md = le "cerveau CTO" (routing, règles, workflow)
- Agents = les travailleurs spécialisés (architect, dev, debugger, etc.)
- Chaque agent a ses propres outils et skills
- Pour le routing : section dans CLAUDE.md avec tableau "utilisateur dit X → agent Y"
- Pattern Boris : CLAUDE.md + AGENTS.md lié
- `--add-dir` pour donner accès à des repos externes
