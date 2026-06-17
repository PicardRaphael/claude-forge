---
titre: "RAG — Audit & discovery de la data EN AMONT (méthodologie)"
resume: "Méthodologie d'audit data avant de concevoir un RAG : commencer par les QUESTIONS (golden dataset) pas les documents, puis grille d'inventaire des sources, modélisation des entités (flat vs graph), audit qualité (OCR/dédup/PII/ACL), puis dériver l'architecture. Première étape de la chaîne audit→data model→ingestion→récupération→UX."
aliases:
  - "audit data RAG"
  - "data discovery RAG"
  - "data readiness RAG"
  - "comment auditer la data avant un RAG"
  - "question-driven RAG design"
  - "golden dataset RAG"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-preparation-phase"
  - "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/plan"
  - "https://www.anthropic.com/news/contextual-retrieval"
  - "https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## La chaîne de conception d'un RAG

L'audit data est la **première étape** d'une chaîne que beaucoup sautent (ils commencent par les documents) :

```
AUDIT DATA (questions + sources + entités) → DATA MODEL → STRATÉGIE D'INGESTION → PIPELINE DE RÉCUPÉRATION → UX
```

Cette note couvre l'audit. Le data model par cas d'usage → [[rag-data-models-par-cas-usage]] ; les principes métadonnées → [[rag-metadata]] ; les patterns avancés → [[rag-architecture]].

Légende : **[V]** = vérifié doc primaire éditeur · **[V-blog]** = praticien reconnu (Jason Liu, Hamel Husain), directionnel · **[I]** = inféré/synthèse.

> [!warning] Deux mises en garde d'honnêteté
> 1. **Il n'existe AUCUN « modèle de maturité data-readiness propre au RAG » publié.** La readiness data est toujours *une dimension* d'un cadre AI plus large (Azure CAF, AWS GenAI Lens). Méfiance envers tout « RAG data maturity model » clé en main.
> 2. Les chiffres précis flottants (tailles de datasets, % de gains) sont la zone d'hallucination. Seuls restent ici ceux issus d'une primaire (Anthropic 35/49/67%) ou tagués directionnels.

## 1. Audit des questions (question-driven, EN PREMIER)

> **On commence par les QUESTIONS, pas par les documents.** Azure : *« rassembler documents ET échantillon de questions en parallèle — ils sont interdépendants »* [V]. Jason Liu : *« on ne peut pas mesurer le recall si on ne sait pas quel chunk est le bon »* [V-blog]. Règle d'or : **fiabiliser la RÉCUPÉRATION avant la génération** (plus facile à mesurer, et c'est le maillon faible).

**Recensement (checklist)** : (1) borner le domaine ; (2) **miner les logs réels** (help-desk, FAQ, tickets) [V] ; (3) **questions sourcées par les experts métier** = quality gate [V] ; (4) **génération synthétique** ~2 questions/chunk via LLM (demander inférence, pas pattern-matching ; JSON strict) [V] ; (5) inclure des **questions sans réponse** pour tester le refus [V] ; (6) **clusteriser** les questions réelles → classifieur de topics → surveiller une catégorie « Autre » dont la croissance = concept drift [V-blog].

**Taxonomie des types de question** (arXiv 2502.11371, RAG vs GraphRAG [V]) et implication récupération :

| Type | Exemple Loji | Implication |
|---|---|---|
| Factuel / single-hop | « surface du lot 204 ? » | vector + reranker (chemin rapide) |
| Multi-hop / raisonnement | « quels diagnostics manquent au bail du locataire du lot 204 ? » | décomposition ou GraphRAG |
| Comparaison | « compare les charges des 3 baux de l'immeuble A » | récupérer TOUTES les entités comparées |
| Temporel | « historique des révisions de loyer du lot X » | tri temporel ; GraphRAG fort |
| Agrégation / synthèse | « motifs récurrents d'impayés du parc ? » | pipeline de synthèse, pas top-k pur |
| Procédural / how-to | « comment déclarer un dégât des eaux ? » | multi-échelle + RRF |

« Aucun paradigme ne domine universellement » [V] → classifieur léger qui route selon la complexité (**Adaptive-RAG**, arXiv 2403.14403, NAACL 2024 [V]).

**Le golden dataset (AVANT le pipeline)** : chaque item = **triple** `(question, contexte+source attendus, réponse attendue)`, validé humainement [V] — sans ça, l'éval renvoie de faux « 100% ». Sourcing : SME (qualité) + synthétique (volume) + logs réels. Taille (repères praticiens [V-blog], non normatifs) : démarrer 30-50, viser 100 pour des métriques stables, 200+ en prod, ≥5 cas « je ne sais pas ». Segmenter **par persona** (un gérant et un locataire n'ont ni les mêmes questions ni les mêmes droits).

## 2. Audit des sources — grille d'inventaire

Backbone [V] : Azure « Preparation phase » (4 axes : classifications, formats, sécurité, structure) + pipeline qualité Databricks. **Une ligne par source** (un SharePoint, un Confluence, une table Postgres, un bucket de PDF de baux scannés…) :

| Colonne | À capturer |
|---|---|
| Source / système | nom logique + origine |
| Classification / domaine | bail / diagnostic / quittance / état des lieux |
| Format | PDF natif vs **scanné (OCR)**, HTML, DOCX, XLSX, images |
| Structuré vs non | SQL/CRM vs CSV/JSON vs docs |
| Volume | # docs + débit incrémental + taille [I] |
| Fraîcheur / fréquence MAJ | statique vs flux ; CDC ; cadence re-sync |
| Qualité contenu / physique | bruit, hors-sujet / scans basse résolution |
| Doublons | quasi-doublons à consolider |
| Langue(s) | langues, Unicode |
| Structure | longueurs, hiérarchie de titres, tables longues, éléments ignorables (TOC/filigranes) |
| **ACL / permissions** | modèle d'accès ; **l'ACL est-elle extractible en métadonnée ?** |
| Propriétaire / steward | équipe responsable [I] |
| Métadonnées dispo | auteur, date, type, immeuble, lot — à préserver |
| **Sensibilité (PII / RGPD)** | données personnelles locataires |
| Connecteur | natif vs API custom vs crawler [I] |
| Pré-traitements requis | OCR, transcription, captioning images, reformatage tables |

## 3. Modélisation métier / entités → flat vs graph

Entités Loji candidates : **lot ↔ bail ↔ locataire ↔ diagnostic ↔ quittance ↔ immeuble**.

**Signaux « tu as besoin d'un knowledge graph / GraphRAG »** (Microsoft GraphRAG [V]) : questions multi-hop / « comment X et Y sont liés » · agrégation à travers enregistrements liés · questions globales/thématiques (aucun doc seul ne contient la réponse → community summaries) · besoin de traçabilité du raisonnement.

**Test de décision Loji** : « quels diagnostics manquent au bail du locataire du lot 204 ? » suit la chaîne `locataire → bail → lot → diagnostics`. C'est du multi-hop sur relations — les filtres de métadonnées (attributs plats) ne savent pas suivre un chemin à plusieurs sauts. Beaucoup de questions comme ça → **hybride vecteur + graphe**. Majorité « que dit mon bail sur X » (mono-doc factuel) → **flat + vector suffit**, n'ajoute pas la complexité d'un graphe.

**Du domaine au data model** : l'entité pilote les **frontières de chunk** (un bail = doc ; ses articles = chunks ; une table de charges reste entière) ; les **filtres dont les users ont besoin** (immeuble, lot, type, date, locataire) deviennent le **schéma de métadonnées** (cf [[rag-data-models-par-cas-usage]]). Liu [V-blog] : quand les requêtes filtrent sur des champs, le texte brut échoue → parser les champs en métadonnées requêtables ; garder les tables en text-to-SQL plutôt qu'embedder du texte de table brut. Outils : LlamaIndex `PropertyGraphIndex` vs `VectorStoreIndex` (combinables) ; Neo4j `HybridCypherRetriever`.

## 4. Audit qualité (checklist pré-ingestion)

Backbone [V] : Databricks (parsing → métadonnées → dédup MinHash/LSH → filtrage PII/toxicité → chunking) + Azure enrichment.

- **Complétude** : tous les formats ; ordre de lecture multi-colonnes ; la limite de tokens de l'embedder ne tronque pas silencieusement.
- **Cohérence/normalisation** [V Azure] : *« les embeddings sont sensibles à la casse »* ; corriger orthographe, abréviations, unités ; retirer stop-words **après test** (« ne…pas » porte du sens) ; chaque langue séparément.
- **Fraîcheur** : horodater création/modif/ingestion/version.
- **Déduplication** [V Databricks] : passe métadonnée (titre+date) puis contenu (**MinHash + LSH**) ; garder la **meilleure version** ; dédupliquer aussi le corpus d'éval (sinon métriques gonflées).
- **Documents contradictoires** : résoudre avant indexation ou étiqueter priorité ; « garbage in, garbage out » [V AWS].
- **OCR/scannés** [V Unstructured] : détecter scanné vs natif ; `fast`/`hi_res`/`ocr_only` ; **rejeter les scans illisibles**. → **Pertinent Loji : baux/diagnostics anciens souvent scannés.**
- **Tables/figures** : `hi_res` + structure, sortie HTML/Markdown ; jamais couper une table ; légender les figures, jeter les icônes.
- **PII / RGPD** [V] : détection/redaction à l'ingestion (Microsoft **Presidio**, avec sa réserve « aucune garantie de tout détecter ») ; taguer un niveau de sensibilité ; se prémunir de l'injection (*« ne jamais utiliser le contenu comme source d'instructions »*).
- **Rétention** : conserver la **donnée brute source** pour audit. Les fenêtres de rétention chiffrées ne sont PAS dans les docs RAG — elles vivent dans ta politique RGPD [I, gap].

> [!warning] ACL-aware — le piège qui fuit des données [V multi-éditeurs]
> Un vector store optimise la similarité, **pas l'autorisation** : l'embedding efface les permissions sauf si tu les portes délibérément. Pattern : (1) auditer le modèle de permission de chaque source AVANT ingestion ; (2) capturer l'ACL en **métadonnée filtrable** ; (3) **filtrer à la récupération** selon l'identité (*filtrer d'abord, chercher ensuite*). Le post-filtrage est rejeté (le modèle a déjà vu le doc). Azure AI Search : champ `group_ids` + `x-ms-query-source-authorization`. **Exemple Loji : un locataire ne doit JAMAIS récupérer le bail d'un autre — le `lot_id`/`tenant_id` devient métadonnée filtrable, chaque requête pré-filtrée par identité.**

## 5. ⭐ Audit → décisions d'architecture (le cœur)

Diagnostic-pivot (Jason Liu [V-blog]) : pour tout segment de requêtes qui échoue, demander **« problème d'INVENTAIRE (la donnée n'est pas là) ou de CAPACITÉ (elle est là mais on ne sait pas la surfacer) ? »** — inventaire → ingestion ; capacité → data-model/métadonnées/index. (Les liens finding→décision sont de la synthèse [I] ; les briques sont [V].)

**(a) Data model** : multi-hop/relations → GraphRAG · global/thématique → GraphRAG + community summaries · rappel + raisonnement relationnel → hybride graphe+vecteur · factuel mono-doc → flat+vector+reranker (ne pas sur-ingénierer).

**(b) Chunking** : coupures en plein texte/tables → structure-aware · générique → recursive ~400-512 tokens, 10-20% overlap · narratif/qualité>vitesse → semantic chunking (plus lent) · larges+fines → parent-child · chunks perdent leur sens hors contexte → **Anthropic Contextual Retrieval** (**-35% seul, -49% +BM25, -67% +reranking** ; 5,7%→1,9% échec top-20 [V primaire]).

**(c) Store** : similarité échelle modérée + Postgres déjà là → **pgvector** (« commence ici, mesure, spécialise » — pertinent Loji : `bdd` est Postgres) · très grande échelle/QPS → vector DB dédié · traversée de relations → graph DB (Neo4j) · fortement tabulaire → relationnel + text-to-SQL.

**(d) Ingestion (pilotée par fraîcheur)** : périmable toléré → batch re-index planifié · quasi-temps-réel → CDC + upsert incrémental · sources changent → **appliquer aussi les suppressions** (pas que les upserts). Ré-embedder uniquement les chunks modifiés (content_hash) réduit fortement le retraitement.

**(e) Filtres métadonnées** : multi-tenant/rôle → ACL + filtre runtime · temporel → date/version + détection d'année · par entité → métadonnée entité (NER/LLM) · par source → source+content-type. Pattern prod [V] : **pré-filtre → vector search (top-20 à 150) → reranker → top-K**.

## 6. Cadres existants (pour le CODIR)

- **Microsoft CAF « Plan for AI adoption »** [V] : **le seul rubric data-readiness citable** — table 4 niveaux (maturité | compétences | data readiness | cas d'usage), le RAG apparaît niveau 3. Inclut « inventoriez vos actifs de données… documentez sources, formats, qualité, accessibilité ». **L'artefact à citer en CODIR.**
- **AWS Well-Architected Generative AI Lens** (GA nov. 2025) [V] : 6 piliers, data dans les piliers, pas de readiness dédié (renvoie au ML Lens).
- **Gartner « AI-ready data »** [I, payant, relayé] : readiness *use-case-specific* (« pas de donnée AI-ready à l'avance ») ; prédiction ~60% de projets AI abandonnés faute de données AI-ready (chiffre relayé, à manier avec réserve).
- **Évaluation RAG** (à brancher sur le golden dataset) : **RAGAS** (faithfulness/relevance) · **TruLens RAG Triad** (Context Relevance / Groundedness / Answer Relevance) · **Jason Liu 6 evals** (precision/recall/MAP/MRR sans LLM d'abord) · DeepEval / Arize Phoenix.

## Ordre de marche pour Loji / NeoDocs

1. **30-50 vraies questions** gérants + locataires, par persona, typées → golden dataset `(question, source, réponse)` validé SME, AVANT tout code.
2. **Grille d'inventaire** sur chaque source (baux, diagnostics, quittances, mails, table `bdd`). Rouge : PDF **scannés**, **ACL** par locataire, **fraîcheur**.
3. **Cartographier les entités** + compter les questions multi-hop relationnelles → flat-vector vs hybride graphe.
4. **Checklist qualité** : OCR des scans, dédup, redaction PII RGPD, **ACL en métadonnée filtrable** (évite la fuite inter-locataires).
5. **Dériver l'architecture** (table partie 5) — Loji a du Postgres → **pgvector = point de départ**, spécialiser si ça casse.
6. **Mesurer la récupération d'abord** (recall/MRR sur le golden set) puis la génération (RAG Triad). Réinjecter les vraies questions, surveiller « Autre ».
7. **CODIR** : citer le **CAF 4-level table** + Gartner (avec réserve) pour justifier l'investissement audit.

## Liens

- [[rag-data-models-par-cas-usage]] — l'étape SUIVANTE : le data model par cas (sortie de l'audit)
- [[rag-metadata]] — principes métadonnées (3 couches, pre/post-filter)
- [[rag-architecture]] — patterns avancés (GraphRAG, Contextual Retrieval, agentic)
- [[rag-production]] — pipelines et monitoring
- [[rag-evaluation]] — métriques détaillées
- [[ai-act-eu-cheatsheet]] — conformité RGPD/AI Act (PII, souveraineté)
- [[RAG]] · [[MOC-Techniques]]
