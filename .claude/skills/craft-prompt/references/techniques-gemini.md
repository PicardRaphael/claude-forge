# Techniques Prompt — Google Gemini

_Source : ai.google.dev, Google AI documentation, recherche 8 avril 2026_
_Note : sera complete quand la recherche Gemini revient_

## Differences cles vs Claude

| Aspect | Claude | Gemini |
|--------|--------|--------|
| Structure | XML tags natifs | Markdown ou JSON (pas de XML) |
| System prompt | Dans le champ `system` | `system_instruction` (champ dedie) |
| Thinking | Adaptive thinking (`effort`) | "Think step by step" manuel |
| Output structure | Structured Output + JSON schema | `response_schema` + JSON mode natif |
| Grounding | Non (pas de search integre) | Google Search grounding integre |
| Code exec | Via tool use (Bash) | `code_execution` natif |
| Prefill | Deprecated sur 4.6 | Non supporte |
| Caching | `cache_control` ephemeral | Context Caching (different) |
| Multimodal | Images, PDF | Images, video, audio, PDF |

## Structure recommandee Gemini

```
System instruction:
[Role + regles globales + contraintes]

User prompt:
[Contexte specifique + tache + format attendu]
```

### System instruction — Best practices Google

```
You are a senior real estate accountant specialized in French property management.

Rules:
- Always respond in French
- Use precise financial terms
- Show your calculations step by step
- If data is missing, list what you need instead of guessing
```

## Techniques Gemini-specifiques

### Grounding avec Google Search

```python
tools=[{"google_search": {}}]
```

Gemini peut verifier ses reponses contre des resultats Google Search en temps reel. Utile pour les faits recents. Claude n'a pas d'equivalent natif.

### Code Execution

```python
tools=[{"code_execution": {}}]
```

Gemini peut executer du Python dans un sandbox pour calculer, generer des graphiques, analyser des donnees. Plus integre que le tool use Claude (pas besoin de Bash).

### JSON Mode natif

```python
generation_config={
    "response_mime_type": "application/json",
    "response_schema": {
        "type": "object",
        "properties": {
            "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
            "confidence": {"type": "number"}
        }
    }
}
```

Plus strict que Claude : le schema est GARANTI. Equivalent de Structured Output chez Claude.

### Enum constraints

```python
"response_schema": {
    "type": "string",
    "enum": ["syndic", "gerance", "compta", "tech"]
}
```

Force une valeur parmi une liste fermee. Tres utile pour la classification.

## Quand utiliser Gemini vs Claude

| Cas d'usage | Meilleur choix | Pourquoi |
|---|---|---|
| Code generation | Claude | Meilleur reasoning, tool use plus riche |
| Analyse de video | Gemini | Multimodal natif (video + audio) |
| Faits recents | Gemini | Grounding Google Search |
| Agents complexes | Claude | Agent Teams, skills, progressive disclosure |
| Data analysis | Gemini | Code execution natif |
| Prompts structures | Claude | XML tags + adaptive thinking |
| Batch classification | Les deux | JSON mode natif chez les deux |
| Long documents (1M+) | Gemini 2.5 Pro | 1M context + caching |

## Template prompt Gemini

```python
import google.generativeai as genai

model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction="""Tu es un expert en gestion immobiliere.
    Reponds toujours en francais.
    Structure tes reponses en sections claires.
    Si tu n'es pas sur, dis-le explicitement.""",
    tools=[{"google_search": {}}, {"code_execution": {}}],
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": {...}
    }
)

response = model.generate_content("Analyse cette situation...")
```

## Gotchas Gemini

- Pas de XML tags — Gemini les ignore ou les traite comme du texte brut
- `system_instruction` est un champ API separe, pas dans le prompt
- Le grounding ajoute du latency (Google Search call)
- Code execution limité au Python (pas de Node, pas de Bash)
- Temperature par defaut plus haute que Claude — preciser `temperature: 0` pour les taches deterministes
- Gemini est plus verbeux que Claude par defaut — ajouter "Be concise" explicitement
