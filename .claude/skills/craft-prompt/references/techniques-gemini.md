# Techniques Prompt — Google Gemini

_Source : ai.google.dev, Kaggle whitepaper, Google Cloud, recherche 8 avril 2026_

## Differences cles vs Claude

| Aspect | Claude | Gemini |
|--------|--------|--------|
| Structure | XML tags natifs | XML tags aussi (recommande Gemini 3) |
| System prompt | Champ `system` | `system_instruction` (champ dedie, REMPLACE le defaut) |
| Thinking | Adaptive (`effort: low/medium/high`) | `thinking_level` (MINIMAL/LOW/MEDIUM/HIGH) |
| Output structure | Structured Output + JSON schema | `response_schema` + `response_mime_type` natif |
| Grounding | Non (via MCP/tools) | Google Search integre (first-party) |
| Code exec | Via tool use (Bash) | `code_execution` sandbox Python natif |
| Prefill | Deprecated sur 4.6 | Non supporte |
| Context window | 200K (1M en option) | 1M par defaut |
| Multimodal | Images + PDF | Images + Video + Audio + PDF |
| Temperature | Pas de reco specifique | `1.0` obligatoire sur Gemini 3 |
| Consistance | Stable | Variable — exige system instructions solides |
| Fichier projet | `CLAUDE.md` (additionnel) | `GEMINI.md` (remplace le system prompt) |
| Forced tool use | `tool_choice: {type: "tool", name: "..."}` | `mode: ANY` + `allowed_function_names` |
| Enums | Instructions textuelles | `text/x.enum` mime type natif |

## Structure recommandee (whitepaper Google)

4 blocs canoniques :

```
Role       → "You are a senior real estate accountant."
Context    → "This is for a SaaS platform managing 500 properties."
Instruction → "Analyze the following charges breakdown."
Output Format → "Return JSON: {items[], total, alerts[]}"
```

**Si un bloc manque (surtout Role et Output Format), la qualite chute.** Claude infere mieux le contexte implicite.

## System Instructions

```python
model = genai.GenerativeModel(
    model_name="gemini-3.1-pro-preview",
    system_instruction="""
    You are a code review assistant for TypeScript/Node.js projects.
    Always respond with valid JSON.
    Schema: { "issues": [{ "line": number, "severity": "error|warning|info", "message": string }] }
    Today's date: 2026-04-08.
    """
)
```

### Regles critiques

- **Pas de contraintes negatives ouvertes** — "Do not infer" casse la logique
- **Inclure la date du jour** — sinon Gemini cherche des infos de son training
- **`GEMINI.md`** remplace completement le system prompt (≠ CLAUDE.md qui s'ajoute)

```
# Mauvais
"Do not use information outside the provided context."

# Bon
"Base all deductions exclusively on the provided context."
```

## Thinking Level (Gemini 3)

Remplace `thinking_budget` de Gemini 2.5 :

| Niveau | Cas d'usage | Equiv. Claude |
|--------|-------------|---------------|
| `MINIMAL` | Extraction, classification simple | `effort: low` |
| `LOW` | Summarization, Q&A | `effort: low` |
| `MEDIUM` | Analyse de code, raisonnement modere | `effort: medium` |
| `HIGH` (defaut) | Agentic, debug complexe | `effort: high` |

```python
generation_config = genai.GenerationConfig(
    thinking_level="LOW",
    temperature=1.0  # TOUJOURS 1.0 sur Gemini 3
)
```

## Structured Output (JSON Mode)

### response_schema — Methode principale

```python
from pydantic import BaseModel

class ReviewResult(BaseModel):
    sentiment: str
    score: float
    tags: list[str]

response = model.generate_content(
    "Analyze this review...",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=ReviewResult,
    ),
)
```

### Enum-only (classification pure)

```python
import enum

class Sentiment(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

generation_config=genai.GenerationConfig(
    response_mime_type="text/x.enum",
    response_schema=Sentiment,
)
# Retourne directement: "negative"
```

### Pieges JSON Gemini

- Proprietes triees **alphabetiquement** par defaut → `propertyOrdering` pour controler
- Schemas complexes = erreur 400 → aplatir, reduire les noms
- Structured output degrade la qualite sur modeles **fines** → eviter la combinaison

## Grounding (Google Search)

```python
tools = [genai.Tool(google_search=genai.GoogleSearch())]
```

Gemini execute 1-N requetes Search automatiquement. Retourne `groundingMetadata` avec sources.

```
# Forcer le grounding recent
"Use Google Search to find the current quarterly earnings of Nvidia.
My knowledge cutoff is January 2025 — search for info published after that date."
```

**Grounding + Structured Output** combinables en une seule requete (Claude ne peut pas).

## Code Execution

```python
tools = [genai.Tool(code_execution=genai.CodeExecution())]
```

- Python uniquement (sandbox)
- Calculs multi-etapes + graphiques
- Combinable avec Grounding : search → Python → JSON

## Function Calling

```python
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location."""
    pass

tools = [get_weather]  # Schema genere depuis la docstring
```

### Parallel function calling

Gemini retourne N function calls simultanement. **Gemini 3 : toujours passer le `id`** dans le response.

### Forced tool use

```python
tool_config = genai.ToolConfig(
    function_calling_config=genai.FunctionCallingConfig(
        mode="ANY",  # Force appel
        allowed_function_names=["get_weather"]
    )
)
```

### Limite : 10-20 outils actifs max

Au-dela la selection se degrade → dynamic tool loading.

## Multimodal

| Modalite | Limite par requete | Placement |
|----------|-------------------|-----------|
| Images | 3 600 | EN PREMIER, texte apres |
| Video | 1 heure | EN PREMIER |
| Audio | 8,4 heures | EN PREMIER |

- **Audio** : preciser "transcribe verbatim, do not summarize"
- **Video** : ajouter metadonnees projet pour corriger noms/titres
- **Multi-images** : interleaver images et texte selon la logique narrative

Claude ne traite pas audio/video dans l'API.

## Placement du contexte long

**Regle Gemini** : donnees EN PREMIER, question EN DERNIER.

```
[document de 100 pages]

Based on the information above, identify all clauses related to liability.
```

Claude gere bien les deux ordres. Gemini degrade si question avant donnees.

## Few-shot Gemini

```xml
<examples>
  <example>
    <input>The product arrived damaged.</input>
    <output>{"sentiment": "negative", "issues": ["product_quality"]}</output>
  </example>
</examples>

<task>Analyze: "Great value but packaging could be better."</task>
```

Few-shot + thinking mode = amplification de la precision.

## Quand utiliser Gemini vs Claude

| Cas d'usage | Meilleur | Pourquoi |
|---|---|---|
| Code generation | Claude | Meilleur reasoning, tool use riche |
| Analyse video/audio | Gemini | Multimodal natif |
| Faits recents | Gemini | Grounding Google Search |
| Agents complexes | Claude | Agent Teams, skills, progressive disclosure |
| Data analysis | Gemini | Code execution natif |
| Prompts structures | Claude | XML tags + adaptive thinking |
| Classification batch | Les deux | JSON mode natif chez les deux |
| Long documents (1M+) | Gemini | 1M natif + caching |
| Taches ambigues | Claude | Meilleur instruction-following nuance |
| Determinisme | Gemini | response_schema + enum garanti |

## Template prompt Gemini complet

```python
import google.generativeai as genai

model = genai.GenerativeModel(
    model_name="gemini-3.1-pro-preview",
    system_instruction="""Tu es un expert en gestion immobiliere.
    Reponds toujours en francais.
    Structure tes reponses en sections claires.
    Date du jour : 2026-04-08.
    Si tu n'es pas sur, dis-le explicitement.""",
    tools=[
        genai.Tool(google_search=genai.GoogleSearch()),
        genai.Tool(code_execution=genai.CodeExecution()),
    ],
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema={...},
        thinking_level="MEDIUM",
        temperature=1.0,
    )
)

response = model.generate_content("Analyse cette situation...")
```

## Gotchas Gemini

- `temperature=1.0` obligatoire sur Gemini 3 (optimise pour cette valeur)
- `GEMINI.md` REMPLACE le system prompt (≠ CLAUDE.md qui s'ajoute)
- Proprietes JSON triees alphabetiquement par defaut
- Grounding ajoute du latency (Google Search call)
- Code execution limite au Python
- Plus verbeux que Claude → ajouter "Be concise"
- Pas de contraintes negatives ouvertes ("do not infer" casse tout)
- `thinking_level` ne peut PAS etre desactive sur Gemini 2.5 Pro
- `id` obligatoire dans function response sur Gemini 3 (sinon perd le mapping)
- Structured output degrade les modeles fines
