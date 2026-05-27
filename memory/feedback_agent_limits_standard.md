---
name: agent-limits-every-repo
description: Rule agent-limits.md obligatoire sur tout nouveau repo — empêche les sous-agents de crasher par surcharge
type: feedback
originSessionId: b83cf0a3-7f05-46e9-9772-44ba96f1eaef
---
Toujours déployer `.claude/rules/agent-limits.md` sur chaque nouveau repo configuré pour Claude Code.

**Why:** Les sous-agents crashent silencieusement quand la tâche est trop lourde (contexte saturé, timeout, boucle). Ça produit "Tool result missing due to internal error" sans retry. Même avec un architect qui planifie le découpage, il faut un filet de sécurité car architect n'est pas toujours appelé.

**How to apply:**
- Tout nouveau repo : copier `agent-limits.md` dans `.claude/rules/`
- Repos avec architect : architect a la section "Découpage des sous-agents" dans son plan + rule en backup
- Repos sans architect (vault, brain, docs) : la rule est le seul garde-fou
- Limites : 6-8 ops lourdes max, 5 fichiers max, scope précis par agent
- Double couverture = standard Neoteem
- JAMAIS d'agents en parallèle dans un seul turn (bug GitHub #39830 — résultats perdus)
- Séquencer : Agent 1 → consolider → Agent 2
- Limites techniques CC : 200K ctx subagent, 32K output hardcodé, maxTurns non enforcé, Task() sans timeout
- Boris parallélise avec des worktrees/sessions, PAS avec des sub-agents empilés
- Bloquer le nesting : ne JAMAIS mettre Agent/Task dans les tools d'un agent, seule la session principale orchestre
- Session principale = chef d'orchestre, agents = exécutants légers et focalisés
- Vérifier avec `grep "^tools:" .claude/agents/*.md` — aucun ne doit avoir Agent ou Task
