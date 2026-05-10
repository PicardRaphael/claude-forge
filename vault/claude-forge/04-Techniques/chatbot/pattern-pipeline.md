---
titre: "Pattern Pipeline — Chaine sequentielle"
resume: "Pattern multi-agent sequentiel : chaque agent traite et passe au suivant dans un ordre fixe. Prompt chaining, evaluator-optimizer, content pipeline"
aliases:
  - pattern pipeline
  - pipeline pattern
  - prompt chaining
  - sequential agents
  - evaluator optimizer
  - chaine sequentielle
domaine: ia
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://www.anthropic.com/research/building-effective-agents"
  - "https://github.com/anthropics/anthropic-cookbook/blob/main/patterns/agents/evaluator_optimizer.ipynb"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/chatbot"
  - "#domaine/patterns"
---

## Definition

Chaine d'agents en sequence fixe. Chaque agent recoit la sortie du precedent, la transforme/enrichit, et passe au suivant. L'ordre est deterministe, defini au design-time (pas par le LLM).

Deux variantes principales :
- **Prompt chaining** : A → B → C → output (lineaire)
- **Evaluator-optimizer** : Generator ⟷ Evaluator (boucle iterative)

Difference cle avec [[pattern-orchestrateur]] : pas de routing dynamique. Chaque step est predetermine.

## Architecture

```
┌─────────── Prompt Chaining (lineaire) ──────────┐
│                                                   │
│  Input → [Classify] → [Enrich] → [Generate] →    │
│          gate ✓/✗     gate ✓/✗    → Output       │
│                                                   │
│  Gate = validation programmatique entre steps     │
└───────────────────────────────────────────────────┘

┌─────────── Evaluator-Optimizer (boucle) ────────┐
│                                                   │
│  Input → Generator → output                      │
│              ↑           ↓                        │
│              └── Evaluator ──→ OK? → Output      │
│                  (feedback)    Non → re-generer   │
│                                                   │
│  Max iterations pour eviter boucle infinie        │
└───────────────────────────────────────────────────┘

┌─────────── Parallelisation ─────────────────────┐
│                                                   │
│  Input ──┬──→ [Sentiment] ──┐                     │
│          ├──→ [Entities]  ──┼──→ Merge → Output  │
│          └──→ [Summary]   ──┘                     │
│                                                   │
│  Sous-taches independantes executees en parallele │
└───────────────────────────────────────────────────┘
```

## Code pattern

### Prompt Chaining (Anthropic)

```python
# Step 1 : Classifier l'intention
classify_response = client.messages.create(
    model="claude-haiku-4-5",
    system="Classifie l'intention : billing / tech / faq / escalation",
    messages=[{"role": "user", "content": user_query}],
)
intent = parse_intent(classify_response)

# Gate programmatique
if intent == "escalation":
    return escalate_to_human(user_query)

# Step 2 : Enrichir avec contexte
context = retrieve_context(intent, user_query)

# Step 3 : Generer la reponse
response = client.messages.create(
    model="claude-sonnet-4-6",
    system=f"Reponds en tant que specialiste {intent}.",
    messages=[{"role": "user", "content": f"{user_query}\n\nContexte:\n{context}"}],
)
```

### Evaluator-Optimizer

```python
MAX_ITERATIONS = 3

draft = generate_response(query, context)

for i in range(MAX_ITERATIONS):
    evaluation = client.messages.create(
        model="claude-sonnet-4-6",
        system="""Evalue cette reponse sur :
        - Exactitude (factuel ?)
        - Completude (repond a la question ?)
        - Ton (professionnel et empathique ?)
        Score 1-10. Si < 8, donne un feedback specifique.""",
        messages=[{"role": "user", "content": f"Question: {query}\nReponse: {draft}"}],
    )
    score, feedback = parse_evaluation(evaluation)
    if score >= 8:
        break
    draft = regenerate_with_feedback(query, context, draft, feedback)
```

### LangGraph Pipeline

```python
graph = StateGraph(PipelineState)

graph.add_node("classify", classify_intent)
graph.add_node("enrich", enrich_with_context)
graph.add_node("generate", generate_response)
graph.add_node("evaluate", evaluate_quality)

graph.add_edge("classify", "enrich")
graph.add_edge("enrich", "generate")
graph.add_conditional_edges("evaluate", lambda s: "generate" if s["score"] < 8 else END)
graph.add_edge("generate", "evaluate")

graph.set_entry_point("classify")
app = graph.compile()
```

### Parallelisation

```python
import asyncio

async def analyze_parallel(text):
    sentiment, entities, summary = await asyncio.gather(
        analyze_sentiment(text),
        extract_entities(text),
        generate_summary(text),
    )
    return merge_results(sentiment, entities, summary)
```

## System prompt chatbot — Pipeline

Chaque step a son propre system prompt specialise :

**Classificateur** (Haiku — rapide, pas cher) :
```
Classifie l'intention du client en UNE categorie :
billing, tech, faq, complaint, escalation.
Reponds UNIQUEMENT avec la categorie, rien d'autre.
```

**Generateur** (Sonnet — qualite) :
```
Tu es specialiste [domaine]. Genere une reponse au client.
Utilise le contexte fourni. Sois concis (2-3 phrases).
```

**Evaluateur** (Sonnet — jugement) :
```
Evalue cette reponse de support client.
Criteres : exactitude, completude, ton, actionabilite.
Score 1-10. Si < 8, donne un feedback SPECIFIQUE et ACTIONABLE.
```

## Specificites chatbot

### Quand le pipeline bat les autres patterns
- **Moderation de contenu** : chaque message passe par classify → moderate → respond (gates strictes)
- **Reponse haute qualite** : evaluator-optimizer affine iterativement
- **Classification + routing deterministe** : pas besoin de LLM pour router

### Latence
Pipeline ajoute de la latence (N appels sequentiels). Attenuer avec :
- Modele leger pour les steps de classification (Haiku, GPT-4.1 Nano)
- Streaming du dernier step pendant que les gates precedentes sont passees
- Parallelisation quand les steps sont independantes

### Garde-fous programmatiques
Les gates entre steps sont du CODE, pas du LLM. Si le classifieur dit "escalation", le code route vers un humain sans appeler de LLM supplementaire.

## Couts et quand utiliser

| Variante | Appels LLM | Cout relatif |
|----------|-----------|--------------|
| Prompt chaining (3 steps) | 3 | Moyen |
| Evaluator-optimizer (3 iter) | 6 | Eleve |
| Parallelisation (3 branches) | 3 (parallele) | Moyen |

**Optimisation** : utiliser Haiku ($1/MTok) pour classify/evaluate, Sonnet ($3/MTok) pour generate.

### Quand utiliser
- Process non-negociable (compliance, moderation, validation)
- Qualite de reponse critique (evaluator-optimizer)
- Steps clairement decomposes et testables independamment

### Quand eviter
- Conversation dynamique (le routing doit s'adapter au contexte)
- Latence critique (N appels sequentiels)
- Sous-taches impredictibles → [[pattern-orchestrateur]]

## Liens

- [[agents-architecture]] — Pattern Pipeline (theorie)
- [[pattern-orchestrateur]] — Alternative avec routing dynamique
- [[pattern-single-agent-multi-tool]] — Alternative sans multi-agent
- [[architecture-claude-api]] — Prompt chaining Anthropic (canonique)
