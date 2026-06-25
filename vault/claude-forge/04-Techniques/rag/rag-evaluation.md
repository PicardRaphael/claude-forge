---
titre: "RAG Evaluation — Metriques et frameworks"
resume: "Métriques et frameworks pour évaluer un système RAG — RAGAS, DeepEval, LLM-as-judge, faithfulness, answer relevancy, context precision/recall."
aliases:
  - "rag evaluation"
  - "RAG evaluation"
  - "evaluation RAG"
  - "metriques RAG"
  - "RAGAS evaluation"
  - "DeepEval RAG"
type: technique
domaine: rag
derniere-maj: 2026-06-21
auteur: claude
sources:
  - "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/"
  - "https://github.com/confident-ai/deepeval"
tags:
  - "#type/technique"
  - "#domaine/rag"
---

## Description

L'évaluation d'un système RAG mesure deux couches distinctes : la **retrieval** (les documents trouvés sont-ils pertinents et exhaustifs ?) et la **génération** (la réponse est-elle fidèle au contexte et correcte ?). Sans évaluation systématique, impossible de détecter les régressions ou d'optimiser objectivement.

## Métriques principales

### Métriques retrieval

- **Context Precision** — ranking des documents pertinents en haut (sans ground truth, via LLM judge)
- **Context Recall** — toute l'information nécessaire à la réponse a-t-elle été retrouvée (nécessite ground truth)
- **Hit Rate** — au moins 1 document pertinent dans le top-K
- **MRR (Mean Reciprocal Rank)** — position du premier document pertinent

### Métriques génération

- **Faithfulness** — la réponse est-elle entièrement supportée par les documents retrouvés (sans hallucination) ?
- **Answer Relevancy** — la réponse adresse-t-elle la question posée (pertinence sémantique) ?
- **Answer Correctness** — la réponse est-elle factuellement correcte (nécessite ground truth)
- **Hallucination Rate** — taux de réponses contenant des affirmations non supportées

## Frameworks

### RAGAS ([docs.ragas.io](https://docs.ragas.io))

Framework open-source dominant. Métriques LLM-as-judge automatisées avec ou sans ground truth. Intégration native LangChain et LlamaIndex. La doc officielle ne prescrit **pas** de seuils canoniques — les valeurs cibles (0.8+/0.9+) sont des recommandations communauté.

### DeepEval ([github.com/confident-ai/deepeval](https://github.com/confident-ai/deepeval))

Framework pytest-native pour CI/CD. Métriques composables, gates de qualité automatiques. Particulièrement adapté à l'intégration tests de régression.

### LLM-as-judge custom

Pour des critères métiers spécifiques que les frameworks standards ne couvrent pas. Implémenter un juge avec rubric explicite + few-shot examples + audit régulier des verdicts (les juges LLM ont leurs propres biais).

## Patterns d'évaluation

### Golden set frozen

**Composition du set — pas que les pannes.** Un golden set bâti uniquement sur des tickets support mesure le SAV (ce qui a cassé), pas l'usage normal. Pour un bot « formateur » censé répondre à tout, peupler **deux familles mesurées séparément** : (A) **pannes** — questions issues de tickets hors-sample qui citent une page de résolution factuelle (cible = donnée du ticket, pas un jugement) ; (B) **usage normal** — questions dérivées du *contenu* de pages doc déjà indexées (cible = la page elle-même, par construction dans l'index → zéro problème de mapping). A et B n'ont pas le même comportement attendu (A profite du routage métier, B teste le RAG brut), d'où mesure séparée.

**Anti-fuite (in-sample).** Les variantes/phrasings qui ont *construit* le système (entrées de lexique, titres de pages reformulés) donnent un golden set tautologique. Garde programmatique : forcer chaque query à NE PAS matcher l'index lexical (`assert lexical_index.match(q) is None`) pour exercer réellement l'étage sémantique, et sourcer les questions hors-sample (tickets clos après la date de construction). Manque de matière hors-sample → signaler, jamais compléter en reformulant le canonical.

**Verdict = rescues vs régressions, pas hit@1.** Quand un boost de score sature le ranking (une cible présente dans le pool saute rank 1 mécaniquement), hit@1/MRR sur l'arm « avec » est tautologique. Mesure honnête = matrice **rescues** (baseline ratait → trouve) **moins régressions** (baseline trouvait → perd par drift d'expansion) à fire-rate donné. Critère de validation = rescues ≥ N× régressions (0 régression n'est pas l'objectif — régressions et rescues viennent souvent du même levier d'enrichissement).
Un jeu de référence (50-200 queries + réponses attendues + documents pertinents annotés) gelé dans le temps. Recalculer toutes les métriques à chaque release.

### A/B testing production
Compare deux configurations (chunking, embedding, reranker) sur traffic réel. Plus représentatif que benchmarks synthétiques.

### Drift detection
Re-embed le golden set régulièrement (hebdomadairement). Mesurer le shift cosinus pour détecter dégradation silencieuse.

### Feedback loops
Thumbs up/down utilisateur → cas de tests automatiques. [[rag-metadata#Feedback loops]] détaille les boucles RAGE.

## Pitfalls

- **Golden set monoculture (que les pannes)** — un set issu seulement de tickets support ne mesure jamais l'usage normal qu'un bot « formateur » doit couvrir. Cf section « Golden set frozen » → composition deux familles.
- **Set in-sample tautologique** — questions dérivées des variantes/titres ayant construit le système → score gonflé sans valeur. Garde anti-fuite + sourcing hors-sample obligatoires.

- **Sur-optimiser une métrique** au détriment des autres (faithfulness vs answer relevancy peuvent s'opposer)
- **Juge LLM biaisé** par le modèle générateur (utiliser un juge d'une autre famille)
- **Golden set obsolète** par rapport au corpus actuel (refresh trimestriel minimum)
- **Pas de séparation retrieval vs génération** dans les métriques (impossible de diagnostiquer)

## Liens

- [[MOC-Techniques]]
- [[RAG]]
- [[rag-production]] — monitoring continu en production
- [[rag-metadata]] — métriques cibles et observabilité
- [[agents-evaluation]]

### Faible rescue ≠ boost inutile — séparer les trois causes du no-gain

Quand le verdict rescues/régressions revient avec **peu de rescues**, ne pas conclure « le boost ne sert à rien ». Le nombre de rescues dépend autant de la **force de la baseline** que du boost. Décomposer chaque cible en trois causes mutuellement exclusives :

1. **Gap sémantique** — baseline ratait (le client décrit le symptôme sans le mot-clé), boost rattrape → **vrai rescue**, c'est là que le boost gagne sa valeur.
2. **Redondance** — baseline trouvait déjà (la query contient un signal fort : code d'erreur, nom d'écran capté par le full-text) → boost « inchangé », **pas un échec** : redondant par nature, attendu, ne le compter ni comme gain ni comme perte.
3. **Trou de contenu** — aucune note ne porte l'information → ni baseline ni boost ne peuvent trouver. C'est un problème de **couverture**, pas de retrieval. À router vers l'enrichissement de la source, jamais vers le réglage du boost.

Conséquence opérationnelle : sur un corpus où les requêtes portent souvent un signal lexical fort (codes d'erreur explicites), un boost sain affiche **peu de rescues et 0 régression** — c'est le signe que le levier d'amélioration est ailleurs (couverture / phrasings sous le seuil), pas que le boost est cassé. Le sur-optimiser est le piège classique du « cap perfection » : effort sur le mauvais levier. Cas empirique : routing support neo_ia, 1 rescue / 0 régression sur 7 paires, 6/7 déjà captées par le full-text → diagnostic = enrichir la couverture du lexique, pas toucher au boost (2026-06-21).
