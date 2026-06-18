---
name: no-cto-orchestrator-agent
description: Éviter l'agent CTO/orchestrateur — la session principale orchestre. Raison AMENDÉE 18 juin : ce n'est plus une impossibilité technique (nesting possible v2.1.172) mais un choix de COÛT (multi-agents = +200-500% tokens).
type: feedback
---

## Éviter l'agent orchestrateur (CTO, conductor, lead) — la session principale orchestre

La session principale Claude Code reste le bon orchestrateur. Le routing se fait dans CLAUDE.md.

**Why (couche FACTUELLE amendée 18 juin 2026 — cf [[amende-vs-pivot-couche-factuelle-design]]) :**
- ⚠️ PÉRIMÉ : « un subagent ne peut pas spawner de sub-agents ». Depuis CC **v2.1.172 (10 juin 2026)**, le nesting EST possible (jusqu'à 5 niveaux). L'ancien argument « impossible by design » (issue #19077) ne tient plus.
- La reco « pas d'agent orchestrateur » RESTE valide, mais pour une raison **économique vérifiée**, pas technique : multi-agents = **+200-500% de tokens** (incidents réels documentés 8-47k$). Sur abonnement, chaque agent parallèle consomme le quota Nx plus vite.
- Le nesting est fait pour **gérer le contexte** (pousser le bruit loin de la conversation), PAS pour orchestrer. Profondeur utile réelle = 2-3, jamais 5 (verbatim Boris + retours prod, vérifié web 18 juin).
- Pour orchestrer BEAUCOUP d'agents (ex. loop multi-stories) → l'outil **Workflow** (orchestration hors-contexte), pas un arbre d'agents imbriqués.

**Why (couche DESIGN, inchangée) :** Testé 5 fois — un agent CTO avec Bash/Grep/Read fait le travail lui-même au lieu de déléguer ; sans outils il ne fonctionne pas. Boris ne l'utilise pas (session principale + CLAUDE.md).

**How to apply:**
- La session principale lit CLAUDE.md → section "Agent Routing" → dispatch aux agents
- CLAUDE.md = le "cerveau CTO" (routing, règles, workflow)
- Agents = les travailleurs spécialisés (architect, dev, debugger, etc.)
- Chaque agent a ses propres outils et skills
- Pour le routing : section dans CLAUDE.md avec tableau "utilisateur dit X → agent Y"
- Pattern Boris : CLAUDE.md + AGENTS.md lié
- `--add-dir` pour donner accès à des repos externes
