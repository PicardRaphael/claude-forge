# Techniques Prompt — Claude (Anthropic)

_Source : docs.anthropic.com, Anthropic Engineering Blog, recherche 8 avril 2026_

## Fondamentales

| Technique | Description | Quand |
|---|---|---|
| **Zero-shot** | Instruction directe sans exemple | Taches simples |
| **Few-shot** | 2-5 exemples dans `<example>` tags | Format/structure precis |
| **Chain-of-Thought** | "Think step by step" ou `<thinking>` tags | Raisonnement complexe, maths, code |
| **Role Prompting** | Persona expert en system prompt | Specialisation domaine |
| **System Prompt** | Instructions persistantes (persona, contraintes, format) | Toujours en production |

### Few-shot — Exemple

```xml
<examples>
  <example>
    <input>Tweet client mecontent</input>
    <output>Category: complaint, Priority: high</output>
  </example>
</examples>
```

### Chain-of-Thought — 3 niveaux

1. **Basic** : "Think step by step"
2. **Guided** : decrire les etapes de raisonnement
3. **Structured** : `<thinking>` et `<answer>` tags separes

## Structurelles

| Technique | Description | Quand |
|---|---|---|
| **XML Tags** | `<instructions>`, `<context>`, `<input>`, `<output_format>` | Prompts complexes multi-sections |
| **Long Context Placement** | Documents longs EN HAUT, question EN BAS (+30% qualite) | Contexte > 20k tokens |
| **Structured Output** | `output_config.format` avec JSON schema | Production, APIs, pipelines |
| **Prefill** | Commencer le message assistant (DEPRECATED sur 4.6+) | Migrer vers Structured Output |
| **Format Control** | Dire quoi FAIRE, pas ce qu'il ne faut pas faire | Controle du format de sortie |

### XML Tags — Pattern

```xml
<instructions>Analyse le texte suivant</instructions>
<context>Document juridique de 2019</context>
<input>{{TEXT}}</input>
<output_format>JSON avec : sentiment, claims, risques</output_format>
```

## Avancees

| Technique | Description | Quand |
|---|---|---|
| **Prompt Chaining** | Plusieurs appels sequentiels (draft → critique → amelioration) | Workflows complexes avec inspection |
| **Self-Correction** | Verifier sa propre reponse avant de livrer | Code, maths, analyses critiques |
| **Context Explanation** | Expliquer POURQUOI une contrainte existe | Contraintes non evidentes |
| **Tree-of-Thought** | Explorer 3+ chemins de raisonnement en parallele | Problemes multi-strategies |
| **Parallel Decomposition** | Sous-taches independantes en parallele | Research, fichiers multiples |
| **Meta-Prompting** | Utiliser Claude pour generer/ameliorer ses propres prompts | Blank page problem |

### Context Explanation — Exemple

```
# Moins efficace
NEVER use ellipses.

# Plus efficace
Never use ellipses — this text will be read by a text-to-speech engine
that doesn't know how to pronounce them.
```

## Claude-specifiques

| Technique | Description | Quand |
|---|---|---|
| **Adaptive Thinking** | `thinking: {type: "adaptive"}` + `effort` (remplace budget_tokens) | Agents, maths, code complexe |
| **Interleaved Thinking** | Claude pense ENTRE chaque tool call (auto sur 4.6) | Workflows agentiques multi-steps |
| **Prompt Caching** | `cache_control: {type: "ephemeral"}` sur prefixes stables (-90% cout) | System prompts longs, RAG |
| **Structured Output strict** | JSON schema garanti via `output_config.format` | APIs consommant l'output |
| **Context Window Awareness** | Claude connait sa propre utilisation du contexte | Agents long-horizon |
| **Prompt Generator** | Outil Console qui genere un draft structure | Demarrer une nouvelle tache |

### Adaptive Thinking

```python
client.messages.create(
    model="claude-opus-4-7",
    thinking={"type": "adaptive"},
    output_config={"effort": "xhigh"},  # low | medium | high | xhigh | max
)
```

### Prompt Caching

```python
system=[{
    "type": "text",
    "text": "...contenu stable long...",
    "cache_control": {"type": "ephemeral"}  # TTL 5min ou 1h
}]
```

## Agents & Skills

| Technique | Description | Quand |
|---|---|---|
| **Progressive Disclosure** | Metadata → SKILL.md → references/ (3 niveaux) | Architecture agentique |
| **Skill Description Engineering** | "Use when..." + termes cles de trigger | Toute creation de skill |
| **Agent Description Engineering** | Conditions de trigger exhaustives, pas agressives | Toute creation d'agent |
| **State Management** | JSON pour l'etat, texte pour les notes, git pour le versioning | Taches multi-sessions |
| **Validate-Execute Pattern** | Plan → valider → executer → verifier | Operations irreversibles |

## Nouveautes 2026

| Technique | Description | Source |
|---|---|---|
| **Context Engineering** | Gestion deliberee de TOUT ce qui entre dans la context window, pas juste le prompt (Karpathy) | Anthropic Engineering Blog |
| **Outcome Delegation** | Definir les criteres de succes, pas les etapes. Laisser le modele choisir l'approche | The AI Corner |
| **Graph of Thoughts** | Raisonnement en graphe (pas chaine/arbre) — fusion de branches, boucles feedback (+62% vs ToT) | ETH Zurich, arXiv |
| **Reflexion** | L'agent examine sa trace apres completion, stocke les lecons en memoire | Sitepoint Agentic Patterns |
| **Dynamic Tool Loading** | Embed descriptions d'outils, retrieve top-k pertinents au lieu de tout charger | Sitepoint Agentic Patterns |
| **Context Compaction** | Prompt de compaction qui resume les traces d'execution pour agents long-horizon | Anthropic Engineering |
| **Tool Description Engineering** | Descriptions d'outils = prompt engineering. Petits refinements → gains massifs (SWE-bench) | Anthropic Engineering |
| **Adaptive Prompting** | Le modele co-auteur de ses propres prompts. Console Anthropic vise -90% du temps de prompt eng. | Alex Albert (@alexalbert__) |

### Les 3 shifts de 2026

| Avant | Apres |
|---|---|
| Prompt unique | Context window entiere a chaque step |
| budget_tokens manuel | effort parameter + adaptive thinking |
| Instructions step-by-step | Criteres de succes + delegation |

## Breaking changes

- `budget_tokens` **NON SUPPORTE** sur Opus 4.7 → `thinking: {type: "adaptive"}` + `output_config: {effort: "xhigh"}`
- `effort: xhigh` = defaut a l'ere Opus 4.7 (avril-mai 2026) ; depuis Opus 4.8 (28 mai) le defaut recommande est `high`. `high` reste defaut Sonnet 4.6
- Prefill deprecated sur claude-4.6+ → Structured Outputs
- Skills = standard ouvert (agentskills.io) adopte par OpenAI, Gemini, GitHub Copilot
- Opus 4.7 est plus litterral que 4.6 → instructions de scope explicites, parallelisme explicite
- Opus 4.7 spawn moins de subagents et fait moins de tool calls → le specifier quand necessaire
- Nouveau tokenizer Opus 4.7 : meme input = ~1.0-1.35x plus de tokens que 4.6
