---
name: techniques-cheatsheet
description: Cheat sheet des meilleures techniques CC, prompt engineering et workflow — consulter quand Raphael demande "meilleure approche pour X"
trigger: meilleure approche, quelle technique, comment faire
type: reference
originSessionId: 16ee3ed4-640e-4e12-aa29-c8156e56b4f6
---
## Workflow (Boris + équipe, validé avril 2026)

| Besoin | Technique |
|--------|-----------|
| Productivité max | 3-5 worktrees parallèles (`claude -w feature`) |
| Garder contexte propre | `/clear` entre tâches, `/compact "garder le plan"` à 70% |
| Question rapide | `/btw` (coût zéro) ou Side Chat `Cmd+;` (Desktop) |
| Session longue | `/recap` au retour, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0` pour désactiver |
| Monitoring CI/PRs | `/loop` sans intervalle (Dynamic Loop) — Claude auto-programme |
| Tâche récurrente locale | `/loop 5m /skill` ou Task Scheduler Windows (orga bloque cloud) |
| Paralléliser du travail | `/batch migrer X vers Y` ou agents en worktrees isolés |
| Vérifier son output | Toujours donner à Claude un moyen de vérifier (tip #1 Boris) |
| CLAUDE.md efficace | Chaque ligne : "si je l'enlève, Claude fait des erreurs ?" sinon couper |
| Garantie 100% | Hooks (déterministe) > CLAUDE.md (~80% compliance) |
| Code review | `/review` ou multi-agents (Team/Enterprise), "Ultra Review" existe |
| Forcer le thinking | `effort: high` (défaut). Keyword `ultrathink` pour ponctuel |
| Éviter hallucinations | Attention adaptive thinking peut allouer 0 tokens → `effort: high` safe |
| Compaction intelligente | Hook `PreCompact` (v2.1.110) pour protéger contexte critique |
| Prompt optimal | 150-300 mots (~3000 tokens max), au-delà le raisonnement se dégrade |

## Prompt Engineering (2026)

| Technique | Quand l'utiliser |
|-----------|-----------------|
| Context Engineering (Karpathy) | Toujours — gérer TOUT ce qui entre dans la context window |
| Outcome Delegation | Tâches complexes — donner critères de succès, pas les étapes |
| Graph of Thoughts | Raisonnement complexe (+62% vs Tree of Thoughts) |
| Réflexion | Agents long-horizon — examiner sa trace, stocker leçons |
| Dynamic Tool Loading | Beaucoup d'outils — embed descriptions, retrieve top-k |
| Adaptive Prompting | Console Anthropic — modèle co-auteur de ses prompts |
| Tool Description Engineering | Descriptions outils = prompt engineering (gains SWE-bench) |

## Emphasis (règle clé)

| Contexte | Emphasis OK ? |
|----------|--------------|
| CLAUDE.md / rules / skills | OUI — "IMPORTANT", "YOU MUST" améliore l'adhérence |
| Tool descriptions | NON — cause overtriggering sur Claude 4.5+/4.6 |
| Safety-critical | NON — utiliser hooks (déterministe), pas prompts |

## API (2026)

| Technique | Détail |
|-----------|--------|
| Prompt Caching | "Everything" (Thariq) — tout le harness CC est construit autour |
| Cache 1h | `ENABLE_PROMPT_CACHING_1H` (v2.1.108) |
| Advisor Tool | Sonnet consulte Opus mid-generation, 1 appel API, -11.9% coût vs Opus seul |
| Adaptive Thinking | Défaut sur 4.6, 4 niveaux (low/medium/high/max). `effort` remplace `budget_tokens` |
| Structured Outputs | Remplace prefill (deprecated sur 4.6+) |

## Spécifique Neoteem

| Besoin | Approche |
|--------|----------|
| Automatisation récurrente | Task Scheduler Windows (orga bloque GitHub cloud) |
| Knowledge base | neoteem-brain Obsidian vault → skill neo-brain |
| Feedback triage | Skill feedback-triage → MCP BDD + Jira |
| Notifs équipe | Google Chat webhooks (pas Slack) |
| Multi-repo | `additionalDirectories` dans settings.json |
| Nouveau projet CC | Analyser → kit composants (agents + skills + hooks + rules + CLAUDE.md) |

## Sources fiables

- **Boris Cherny** : workflow, context management, hooks
- **Thariq Shihipar** : skills architecture, prompt caching
- **Noah Zweben** : Dynamic Loop, Monitor tool, cloud features
- **Cat Wu** : limites modèles, product direction
- **Amanda Askell** : personnalité Claude, system prompts
- **Karpathy** : context engineering, LLM wikis, agentic engineering
- **Stanford AI Index** : Anthropic #1 Arena (avril 2026)

_Dernière mise à jour : 16 avril 2026_

---
_Règle de maintenance : fichier cumulatif. Ajouter les nouvelles techniques, mettre à jour celles qui évoluent, marquer "→ remplacé par X" celles qui deviennent obsolètes. Ne jamais supprimer._
