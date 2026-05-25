---
aliases:
  - "vulgarisation IA"
  - "parler non-tech"
  - "expliquer IA direction"
  - "analogies IA"
  - "communication non-technique"
  - "outcome over mechanics"
resume: "Vulgariser l'IA auprès d'une direction non-tech : règle outcome > mécanique, table d'analogies validées, hiérarchie de persuasion."
derniere-maj: 2026-05-25
tags:
  - "#type/technique"
  - "#domaine/communication"
  - "#casquette/responsable-ia"
---

## TL;DR

- **Outcome > mécanique** : parle du résultat business, pas du transformer ni de l'attention
- Une analogie validée vaut 10 schémas techniques
- Une démo 90s convainc plus qu'un slide deck de 20 pages
- Jargon = signal d'insécurité, pas d'expertise

## Règle d'or

> Personne en Comex ne te demandera comment fonctionne un alternateur.
> Personne ne te demandera comment fonctionne un LLM.

Ton job : connecter capacité IA → outcome Loji → métrique business.

## Table d'analogies validées

| Concept tech | Analogie pour COO/CEO | Source |
|--------------|----------------------|--------|
| LLM | "Un stagiaire ultra-lu mais sans mémoire long terme" | Cassie Kozyrkov |
| RAG | "Un moteur de recherche sur **nos** documents internes" | Ethan Mollick |
| Fine-tuning | "Former un stagiaire avec **notre** manuel interne" | Mollick |
| Embeddings | "Une carte sémantique où les concepts proches sont voisins" | Karpathy |
| Hallucination | "Un commercial junior qui invente une réponse pour ne pas dire 'je ne sais pas'" | Kozyrkov |
| Agent | "Un stagiaire qui clique dans nos outils à notre place" | Lenny Rachitsky |
| Eval set | "Le BTS de notre IA — épreuves notées avant de la mettre en prod" | adapté Anthropic |
| Prompt engineering | "Rédiger une consigne précise au stagiaire" | Mollick |
| Context window | "Combien de pages le stagiaire peut lire d'un coup" | Karpathy |
| Tool calling | "Donner les clés des outils internes au stagiaire" | Anthropic |

## Hiérarchie de persuasion non-tech

```
1. Démo 90s sur LE cas client      ← niveau max
2. Schéma 1 page outcome-oriented
3. UN chiffre marquant
4. Tableau comparatif avant/après
5. Récit d'usage réel (alpha tester)
   ........................
   JAMAIS : jargon, équations, schéma archi
```

## Exemple Neoteem — Aurore expliquée 3 niveaux

### Niveau exec (30s)

> "Aurore lit les pièces d'un dossier — bail, état des lieux, RIB — et
> remplit la fiche mandat à la place du gérant. Lui n'a plus qu'à valider.
> 45 min → 90 s. Sur 800 mandats, ça rend 2 ETP au commercial."

### Niveau ops (2 min)

> "On utilise GEMINI couplé à NeoDocs. Le gérant upload les pièces,
> Aurore extrait les champs structurés, pré-remplit la fiche Loji, et
> propose à validation. Le gérant peut corriger, et chaque correction
> nourrit notre eval set pour améliorer le modèle."

### Niveau tech (5 min, équipe data)

> "Pipeline NeoDocs → OCR Document AI → chunks 512 tokens → embeddings
> text-embedding-005 → recherche hybride BM25+vector dans pgvector →
> top-5 chunks injectés dans le prompt GEMINI 2.5 Pro → output structuré
> validé par schema JSON → écriture Drizzle → Cloud Run."

Tu **n'utiliseras jamais** le niveau tech en Comex.

## Phrases de cadrage

| Quand l'exec dit... | Tu réponds... |
|---------------------|---------------|
| "C'est de la magie ?" | "Non, c'est de la stat. Le modèle prédit la suite la plus probable." |
| "Pourquoi c'est cher ?" | "Le compute représente 15-20% du coût total. Le reste c'est talent et data." |
| "ChatGPT le fait gratuit" | "ChatGPT ne lit pas nos baux. Aurore oui — c'est notre RAG." |
| "Et si ça se trompe ?" | "On mesure. Aujourd'hui 1.5% d'erreur, cible 1%. Le gérant valide toujours." |

## Anti-patterns

- Dire "c'est un transformer" → 0 info pour exec
- Dire "on utilise GPT-4" → date dans 3 mois, dit rien sur la valeur
- Sortir un schéma d'archi → ils décrochent en 5s
- Promettre 100% → tu vas le payer
- Sous-estimer le COO → ils ont lu Lenny et Mollick aussi
- "C'est trop technique pour t'expliquer" → fin de ta crédibilité

## Sources

- Cassie Kozyrkov — *Decision Intelligence* https://kozyrkov.medium.com/
- Ethan Mollick — *Co-Intelligence* (2024) https://www.oneusefulthing.org/
- Lenny Rachitsky — *AI for product managers* https://www.lennysnewsletter.com/
- Andrej Karpathy — *Intro to LLMs* https://www.youtube.com/watch?v=zjkBMFhNj_g

## Liens

- [[index]]
- [[../index]]
- [[hype-ia-cadrage-kozyrkov]]
- [[../reunions/reunion-client-hype-management]]
