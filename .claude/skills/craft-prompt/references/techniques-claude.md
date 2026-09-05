# Techniques Prompt — Claude (Anthropic)

_Source : docs.anthropic.com, Anthropic Engineering Blog — verifie le 5 septembre 2026._
_Les regles de prompting Claude different PAR MODELE, pas par generation : [[doctrine-par-modele-opus5-fable5]]._

## Fondamentales

| Technique | Description | Quand |
|---|---|---|
| **Zero-shot** | Instruction directe sans exemple | Taches simples |
| **Few-shot** | 2-5 exemples dans `<example>` tags | Format/structure precis |
| **Thinking adaptatif** | `thinking: {type: "adaptive"}` + `output_config.effort` | Raisonnement complexe — se regle en configuration, jamais en prose |
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

### Thinking — regler la profondeur, ne pas la prescrire

Le thinking est natif et toujours actif sur Opus 5 et Fable 5.1. La profondeur se regle
par `output_config.effort` (`low` a `max`) ; ecrire « think step by step » est redondant.

Ne jamais demander au modele de **restituer son raisonnement dans sa reponse**
(« montre ton raisonnement », `<thinking>` et `<answer>` separes) : sur Fable 5.1 c'est le
declencheur du refus `reasoning_extraction`, qui provoque un fallback silencieux vers Opus 4.8.
Pour lire le raisonnement, utiliser les blocs `thinking` de l'API — `display: "summarized"`,
ou `"updates"` pour les notes de progression entre appels d'outils.

## Structurelles

| Technique | Description | Quand |
|---|---|---|
| **XML Tags** | `<instructions>`, `<context>`, `<input>`, `<output_format>` | Prompts complexes multi-sections |
| **Long Context Placement** | Documents longs EN HAUT, question EN BAS (+30% qualite) | Contexte > 20k tokens |
| **Structured Output** | `output_config.format` avec JSON schema | Production, APIs, pipelines |
| **Prefill** | Commencer le message assistant — renvoie **400** sur Fable 5/5.1, Opus 5/4.8/4.7/4.6, Sonnet 5/4.6 | Structured Outputs (`output_config.format`) |
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
| **Verification d'un tiers** | Controler un rapport de sous-agent ou une source volatile | Sortie d'agent, chiffre date — **pas** son propre output frais : Opus 5 s'auto-verifie, l'instruire cause de la sur-verification |
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
    model="claude-opus-5",
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # low | medium | high | xhigh | max — defaut recommande : high
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

- `budget_tokens` renvoie **400** sur Fable 5/5.1, Opus 5/4.8/4.7 et Sonnet 5 → `thinking: {type: "adaptive"}` + `output_config: {effort: …}`
- `temperature` / `top_p` / `top_k` renvoient **400** sur Fable 5/5.1, Opus 5/4.8/4.7 et Sonnet 5 — toujours acceptes sur Opus 4.6 / Sonnet 4.6
- Prefill renvoie **400** sur Fable 5/5.1, Opus 5/4.8/4.7/4.6 et Sonnet 5/4.6 → Structured Outputs
- Defaut recommande : `effort: high`. `xhigh` = step-up mesure, jamais par defaut
- Skills = standard ouvert (agentskills.io) adopte par OpenAI, Gemini, GitHub Copilot
- Opus 5 suit les instructions litteralement → cadrer le scope explicitement
- **Opus 5 sur-delegue** (inverse d'Opus 4.8) → plafonner le nombre de sous-agents ; ne pas ecrire de consigne « delegue plus »
- **Opus 5 s'auto-verifie** → retirer les instructions de re-verification, elles causent de la sur-verification
- Opus 5 redige des reponses et des livrables Markdown plus longs → calibrer la longueur explicitement
- **Fable 5.1 delegue bien**, en asynchrone → l'encourager plutot que le brider : la consigne de delegation est conditionnelle au modele
- Fable 5.1 sous-formate et sous-narre → ne jamais ajouter de regle anti-formatage ni de suppresseur de narration
- Sur Fable 5.1, `low`/`medium` depassent souvent le `xhigh` des modeles anterieurs — mais **jamais `low` sur une tache de veille** (le modele repond de memoire)
- Tokenizer inchange depuis Opus 4.7 (Fable 5.1 inclus)
