# Template livrable RAG design

À copier dans `docs/rag-design/<slug>.md` et remplir au fil des 6 étapes. Une section reste vide tant que son étape n'est pas abordée.

```markdown
# Conception RAG — <nom du système / cas d'usage>

> Statut : <brouillon | validé> · Date : <ISO> · Cas d'usage : <proptech/support/juridique/...>
> Ancrage : <Loji NeoDocs / NeoChat / autre>

## 1. Audit des questions (golden dataset)

- **Personas** : <gérant, locataire, syndic...> (droits différents = ACL)
- **Types de questions dominants** : <factuel / multi-hop / comparaison / temporel / agrégation / procédural> + proportion multi-hop relationnel
- **Golden dataset** : <N triples (question, source attendue, réponse attendue)>, dont <K> cas « je ne sais pas »
- **Décision pilotée par l'audit** : <flat vs graph signalé ici>

## 2. Sources, entités & data model

### Grille d'inventaire des sources
| Source | Format | Struct? | Volume | Fraîcheur | Qualité | Doublons | Langue | ACL | PII/RGPD | Connecteur | Pré-traitements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| <...> | | | | | | | | | | | |

### Entités & relations
- Entités : <lot, bail, locataire, diagnostic, quittance, immeuble...>
- Questions multi-hop relationnelles : <oui/non + exemples> → **data model : <flat+vector | hybride graphe+vecteur>**

### Data model (règle des 3 couches)
- **Texte embeddé** : <chunk + contexte ; Contextual Retrieval oui/non>
- **Scalaires pre-filter** : <champs typés — champ pivot : ...>
- **Payload citation** : <doc_id, page, url>
- **Pattern de structuration** : <(a) flat | (b) parent-child | (c) graph | (d) Q&A/HyPE | (e) procédural | (f) RAPTOR>

## 3. Stratégie d'ingestion

- **Chunking** : <stratégie + taille + overlap>
- **Embeddings** : <modèle, dimension, Matryoshka?>
- **Contextual Retrieval** : <oui/non + format du préfixe>
- **Fraîcheur** : <batch / CDC + suppressions / content_hash>
- **PII/RGPD** : <redaction, tag sensibilité, anti-injection>

## 4. Pipeline de récupération

- **Store** : <pgvector / Qdrant / Neo4j / text-to-SQL> + justification
- **Pipeline** : pré-filtre <champs> → vector search (top-<N>) → reranker <modèle> → top-<K>
- **ACL** : <comment filtrer par identité à la récupération>
- **Query handling** : <query expansion / Adaptive-RAG / routage par type>

## 5. UX & génération

- **Format réponse** : <...>
- **Citations** : <source/page affichées>
- **Refus** : <comportement quand pas de contexte>
- **Feedback** : <thumbs → cas de test>
- **Garde injection** : <contenu récupéré ≠ instructions>

## 6. Évaluation

- **Golden set frozen** : <N triples, segmenté par persona>
- **Métriques retrieval** : Context Precision/Recall, Hit Rate, MRR — cibles <...>
- **Métriques génération** : Faithfulness, Answer Relevancy/Correctness — cibles <...>
- **Framework** : <RAGAS / DeepEval> + cadence de re-mesure
- **Grading livrable** : RUBRIC dérivé du golden set → /outcomes-test

## Suite

- [ ] Passer en tickets via /spec
- [ ] Arbitrage CODIR/conformité restant via responsable-ia
```
