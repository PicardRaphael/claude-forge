---
name: opus-47-best-practices
description: Guide complet Opus 4.7 — effort levels, adaptive thinking, 9 changements comportement, prompts controle, benchmarks, workflow Boris. Sources croisees blog Anthropic + Boris thread + d4m1n.
type: reference
originSessionId: 7344c917-42fa-4a63-8a92-bc680e8d28e4
---
## Opus 4.7 — Fiche complète (16 avril 2026)

Model ID : `claude-opus-4-7`
Prix : $5/M input, $25/M output
Tokenizer : nouveau, ~1.0-1.35x plus de tokens que 4.6 pour le même input
Vision : max 2576px / 3.75MP, recommandé 1080p, 720p si cost-sensitive

## Effort Levels

| Niveau | Usage | Notes |
|--------|-------|-------|
| `low` / `medium` | Coût/latence, scope serré | Le modèle fait exactement ce qu'on demande, rien de plus |
| `high` | Sessions concurrentes, ratio qualité/coût | Bon équilibre |
| `xhigh` **(défaut CC)** | La plupart du coding et travail agentique | Recommandé Boris pour presque tout |
| `max` | Problèmes très durs, evals | Diminishing returns, prone overthinking. Session-only (non sticky) |

"Effort is more important for this model than for any prior Opus."
À `max`/`xhigh` : mettre max_tokens à 64k+ minimum.

## Adaptive Thinking

- `budget_tokens` **NON SUPPORTÉ** sur Opus 4.7
- Utiliser `thinking: {type: "adaptive"}` + `output_config: {effort: "..."}`
- Le modèle décide quand raisonner profondément vs répondre directement

### Prompts de contrôle thinking

Plus de thinking :
```
Think carefully and step-by-step before responding; this problem is harder than it looks.
```

Moins de thinking :
```
Prioritize responding quickly rather than thinking deeply. When in doubt, respond directly.
```

Contraindre le triggering (gros system prompts) :
```
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

### Migration API

```python
# AVANT (extended thinking, modèles <= 4.6)
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)

# APRÈS (adaptive thinking, Opus 4.7)
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "..."}],
)
```

## 9 Changements de Comportement (vs Opus 4.6)

1. **Longueur calibrée** — moins verbeux, proportionnel à la complexité. Pour verbosité spécifique → le dire.
2. **Moins de tool calls** — plus de raisonnement d'abord. Pour forcer → augmenter effort ou le spécifier.
3. **Moins de subagents** — plus sélectif. Pour parallèle agressif → le demander explicitement.
4. **Instructions plus littérales** — ne généralise plus, ne devine plus. Scope = toujours explicite.
5. **Ton plus direct** — opinionated, moins d'emoji, moins de validation-forward.
6. **Meilleurs progress updates** — retirer le scaffolding "résume tous les N tool calls" si présent.
7. **House style design** — cream (#F4F1EA), serif (Georgia/Playfair), terracotta/amber. Override nécessaire pour SaaS/dashboards.
8. **Code review** — +11pp recall. MAIS suit "don't nitpick" littéralement → revoir les prompts de review.
9. **Computer use** — 2576px max, 1080p recommandé.

## Prompts de Contrôle Clés

### Subagents parallèles
```
Do not spawn a subagent for work you can complete directly in a single response.
Spawn multiple subagents in the same turn when fanning out across items or reading multiple files.
```

### Code review (coverage max)
```
Report every issue you find, including ones you are uncertain about or consider low-severity.
Do not filter for importance or confidence at this stage — a separate verification step will do that.
Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug.
For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

### Code review (single pass, filtré)
"Report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences."

### Frontend override (anti-house-style)
```xml
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

### Ton warm (si nécessaire)
```
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### Verbosité réduite
```
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

## Stratégie de Session Optimale

1. **First-turn specificity** : intent + contraintes + critères d'acceptation + fichiers pertinents → TOUT dans le premier message
2. **Minimiser les tours** : chaque tour = reasoning overhead. Batacher questions + contexte complet
3. **Auto mode** (`Shift+Tab`) : pour tâches longues, contexte complet upfront. Max, Teams, Enterprise
4. **Notifications** : demander à Claude de jouer un son à la fin

"Because Claude Opus 4.7 is more autonomous than prior models, this usage pattern helps to maximize performance. Ambiguous or underspecified prompts conveyed progressively over multiple user turns tend to reduce token efficiency and sometimes performance."

## Workflow Boris Cherny

- 5 terminaux + 5-10 sessions cloud en parallèle
- Chacun dans son worktree git
- Effort `xhigh` pour la plupart, `max` pour les plus durs
- `/go` skill : self-test → `/simplify` → ouvrir PR
- Vérification = tip #1 (2-3x résultats)
- `/recap` pour retrouver le contexte après pause
- "Take time to adjust workflow — nice improvement with old patterns, significant leap once adjusted"

## Benchmarks

| Benchmark | Opus 4.7 | vs 4.6 |
|-----------|----------|--------|
| CursorBench | 70% | 58% |
| XBOW visual-acuity | 98.5% | 54.5% |
| Bug-finding (Anthropic PRs) | +11pp recall | — |
| Rakuten-SWE-Bench | 3x tâches | — |
| Notion Agent | +14% | 1/3 tool errors |
| Databricks OfficeQA | -21% erreurs | — |
| BigLaw Bench (high effort) | 90.9% | — |
| Factory Droids | +10-15% | — |
| Hexagon 93-task | +13% | — |
| Bolt | +10% sur tâches longues | — |
| Mosaic General Finance | 0.813 | 0.767 |

## Pièges à Éviter

- Ne JAMAIS copier des env vars de Twitter sans vérifier la doc (cf. tweet satirique @d4m1n)
- `max` effort = diminishing returns, overthinking fréquent — utiliser `xhigh` par défaut
- Ne pas sous-estimer le surcoût tokenizer (~35% worst case)
- Si review harness dit "don't nitpick" → Opus 4.7 obéit littéralement, masque des bugs
- Prompts vagues multi-tours = anti-pattern. Tout dans le premier tour.

## Audit Neoteem (17 avril 2026)

Repos ia_back + neo_ia audites et confirmes alignes sur TOUS les points 4.7 :
- Plan-driven (architect-first) = plan IS the prompt ✓
- xhigh planning (session) + high execution (subagents) ✓
- Explicit parallelism dans rules ✓
- Literal instructions (tables, workflows numerotes, gates) ✓
- Adaptive thinking (pas de budget_tokens) ✓
- Verification gates (test-writer → code-reviewer → validator) ✓
- Positive framing dominant ✓
- Seul bonus non implemente : skill `/go` (test → simplify → PR)

## Liens Officiels

- Blog : claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code
- Migration : platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-to-claude-opus-4-7
- What's new : platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7
- Adaptive thinking : platform.claude.com/docs/en/build-with-claude/adaptive-thinking
- Effort : platform.claude.com/docs/en/build-with-claude/effort
- Auto mode : claude.com/blog/auto-mode
- Frontend design skill : github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md
