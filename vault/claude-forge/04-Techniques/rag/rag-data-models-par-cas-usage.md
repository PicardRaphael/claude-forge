---
titre: "RAG — Data models (schémas de métadonnées) par cas d'usage"
resume: "Le data model optimal d'un chunk RAG dépend du cas d'usage. Pattern transverse = 3 couches (texte embeddé / scalaires pre-filter / payload citation). 8 schémas concrets avec exemples JSON : maintenance, immobilier/Loji, support FAQ, juridique, e-commerce, médical, code, financier."
aliases:
  - "data model RAG"
  - "schéma métadonnées RAG par cas"
  - "data model par cas d'usage RAG"
  - "structure chunk RAG"
  - "RAG metadata schema use case"
  - "meilleur data model RAG"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://www.anthropic.com/news/contextual-retrieval"
  - "https://www.pinecone.io/learn/vector-search-filtering/"
  - "https://fin.ai/research/structured-agentic-rag-for-e-commerce/"
  - "https://arxiv.org/html/2502.20364v1"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/rag"
---

## Principe — il n'y a pas UN data model RAG

Consensus industrie 2026 : **le bon data model est dicté par le type de question posée**, pas par les documents. Single-hop factuel → flat ; relationnel multi-hop → graph ; procédural → step-by-step. Concevoir le schéma = partir des questions des users (cf [[rag-data-audit-discovery]] pour l'audit amont), pas des PDF. Cette note donne 3 niveaux : (1) le pattern transverse 3-couches, (2) les 6 patterns de structuration, (3) 8 schémas concrets par cas d'usage avec JSON.

Principes transverses (métadonnées universelles, pre/post-filter, parsing, limites Pinecone 40 KB / Qdrant 10-15 index) → [[rag-metadata]]. Techniques avancées (GraphRAG, Contextual Retrieval, agentic) → [[rag-architecture]].

## Niveau 1 — la règle des 3 couches (transverse, le cœur actionnable)

Tout record de chunk se conçoit en **3 couches distinctes** (vérifié, convergent Pinecone/Qdrant/Weaviate/Anthropic) :

| Couche | Rôle | Ce qui y va |
|---|---|---|
| **Texte embeddé** (le vecteur) | Match sémantique | Prose enrichie = chunk + son contexte. Appliquer **Contextual Retrieval** (Anthropic) : préfixer 50-100 tokens situant le chunk → **-35% échecs (seul), -49% +BM25, -67% +reranking** (chiffres Anthropic, baseline 5,7%). ~1,02$/M tokens avec prompt caching |
| **Scalaires de pre-filter** | Réduire l'espace AVANT la similarité | Champs typés exacts : `equipment_type`, `criticite`, `juridiction`, `version`, `prix`, `stock`. **Pre-filter >> post-filter** (post renvoie < k résultats ~30% du temps sur 10M docs) |
| **Payload-only** | Retourné, ni filtré ni embeddé | Pointeurs de citation : `doc_id`, `page`, `url`. Affichage/traçabilité, jamais la recherche |

> [!tip] La distinction la plus sous-estimée
> Décider **dès la conception du schéma** quel champ sert à quoi : FILTRAGE (gate dur avant search) ≠ RANKING (boost doux) ≠ CITATION (sortie). Pipeline en couches : **filtrer → ranker → vérifier/citer**. « Être retrouvé ne garantit pas d'être cité. » Un champ filtré doit être indexé ; un champ de citation (page) n'a pas besoin de l'être.

## Niveau 2 — les 6 patterns de structuration

| Pattern | Idée | Quand |
|---|---|---|
| **(a) Chunk plat + métadonnées** | 1 vecteur = 1 chunk + JSON | FAQ, policy, lookup. Single-hop. Le défaut |
| **(b) Parent-child / small-to-big** | embedder de petits child (précision), renvoyer le parent (contexte) | quand le bon chunk pour matcher ≠ pour répondre. LlamaIndex `AutoMergingRetriever` |
| **(c) Entité-relation / GraphRAG** | nœuds + relations | multi-hop, dépendances, audit traçable (cf [[rag-architecture]]) |
| **(d) Q&A pairs / HyPE** | embedder la (les) **question(s)**, réponse en payload | support/FAQ — les users ne formulent jamais comme la doc |
| **(e) Procédural / step-by-step** | chunk = une procédure complète, métadonnées d'ordre+entité | maintenance, troubleshooting, manuels |
| **(f) Summary + détail (RAPTOR)** | arbre : feuilles fines + résumés par cluster | corpus large mêlant détail et thème global |

> Levier d'embedding **HyPE / Reverse-HyDE** (valable partout, vérifié) : générer 3-5 questions hypothétiques par chunk à l'ingestion, les embedder, stocker l'id du parent en métadonnée. Match question-user ↔ question-pré-générée = meilleur recall, zéro coût LLM au runtime.

## Niveau 3 — 8 schémas concrets par cas d'usage

Pour chaque cas : champ pivot de pre-filter + levier d'embedding spécifique. (V = schéma vérifié sur source publiée ; R = construit par raisonnement métier sur patterns vérifiés.)

### 1. Maintenance / diagnostic technique (R) — le cas de départ
Le modèle Symptôme → Causes → Diagnostic → Remède → Équipement → Page **est correct**, avec 2 affinements : (1) **unité-chunk = une entrée diagnostique complète** (ne jamais couper entre causes et remède) ; (2) ajouter `criticite` + `equipment_model` en pre-filter (les filtres réels du terrain).

```json
{
  "id": "maint-chaudiere-sdv-f28",
  "embedded_text": "Contexte : notice chaudière gaz Saunier Duval ThemaPlus Condens. Symptôme : mise en sécurité (code F28). Causes : pression <0,8 bar, électrode encrassée, vanne gaz fermée. Diagnostic : vérifier manomètre, arrivée gaz, électrode. Remède : remettre à 1,2 bar ; si récidive, nettoyer/remplacer l'électrode.",
  "metadata": {
    "equipment_type": "chaudiere_gaz", "equipment_model": "saunier_duval_themaplus", "criticite": "haute",
    "domaine": "CVC", "code_erreur": "F28", "langue": "fr",
    "document_id": "doc-sdv-notice-2024", "page": 47, "derniere_maj": "2024-11-03"
  }
}
```
**Gain vs chunk plat** : filtre `equipment_model` + `criticite=haute` → que les pannes graves de SON équipement + page exacte à montrer. Couche graph (c) si les causes traversent les équipements.

### 2. Immobilier / proptech — Loji/NeoDocs (R)
Spécificité : un doc est rattaché à un **lot/bail/propriétaire** et a une **échéance**. Ce sont les filtres réels.

```json
{
  "id": "immo-dpe-lot12",
  "embedded_text": "Contexte : DPE du lot 12 (T3, 68 m²), 14 rue de la Paix Paris 2e. Classe énergétique D (190 kWh/m²/an), GES C. Recommandation : isolation combles + menuiseries. Validité 10 ans.",
  "metadata": {
    "type_doc": "DPE", "lot_id": "lot-12", "bail_id": "bail-2024-0087", "proprietaire_id": "prop-441",
    "statut": "actif", "classe_energetique": "D", "date_echeance": "2034-06-01", "commune": "75002",
    "document_id": "ged-dpe-lot12", "page": 1, "url_ged": "https://ged.loji.fr/doc/ged-dpe-lot12"
  }
}
```
**Gain** : « quels lots ont un DPE F/G expirant dans 12 mois ? » = pre-filter pur (`type_doc=DPE` + `classe IN [F,G]` + `date_echeance < now+12m`) puis sémantique. C'est le levier conformité (passoires thermiques) qui justifie l'investissement métadonnées. **Champ pivot : `lot_id` + `type_doc` + `date_echeance`.**

### 3. Support client / FAQ (V)
Embedder des **questions hypothétiques** (HyPE), pas la réponse brute. `version_produit` = filtre critique (une procédure v2 ne doit pas répondre à un user v1).

```json
{
  "id": "faq-neochat-export",
  "embedded_text": "Comment exporter une conversation NeoChat en PDF ? Variantes : télécharger l'historique ? où est le bouton d'export ? sauvegarder une discussion ?",
  "metadata": {
    "produit": "neochat", "feature": "export", "categorie": "fonctionnalites", "version_produit": "2.4",
    "langue": "fr", "statut": "publie", "reponse": "Menu (...) en haut à droite → Exporter en PDF.",
    "ticket_lie": "N2-10455", "url_article": "https://help.loji.fr/neochat/export-pdf"
  }
}
```
**Champ pivot : `version_produit`.** Levier : HyPE.

### 4. Juridique / conformité / RH (V)
**Juridiction + temporalité (date d'effet, version)** = filtres durs non-négociables. Chunk ~256 tokens avec overlap (ne pas couper une clause). C'est le cas où le chunk plat est le plus **dangereux** (citer une version inapplicable = erreur juridique).

```json
{
  "id": "legal-bail-art12-v2025",
  "embedded_text": "Contexte : Article 12 (révision du loyer), bail commercial type v2025, droit FR. Révision annuelle selon l'indice ILC INSEE, dans la limite du plafonnement légal.",
  "metadata": {
    "juridiction": "FR", "type_norme": "clause_contractuelle", "date_effet": "2025-01-01",
    "date_fin_validite": null, "version": "2025.1", "statut": "en_vigueur",
    "contrat_parent_id": "bail-commercial-type-2025", "article_ref": "Art. 12",
    "references_croisees": ["Art. L145-38 Code de commerce"], "page": 4
  }
}
```
**Champ pivot : `juridiction` + `date_effet`/`version`.** Filtre temporel obligatoire (`date_effet <= date_contrat AND (date_fin IS NULL OR > date_contrat)`).

### 5. E-commerce / catalogue (V)
Feuille indexable = la **variante (SKU)**. `prix`/`stock` = pre-filter durs ; `nom`/`description` = sémantique.

```json
{
  "id": "sku-veste-cuir-M",
  "embedded_text": "Veste en cuir véritable femme, coupe ajustée, col motard, doublure. Style intemporel mi-saison.",
  "metadata": {
    "sku": "SKU-2024-VC-NOIR-M", "categorie_path": "femme/vetements/vestes/cuir", "prix": 189.00,
    "stock": 12, "marque": "AcmeWear", "taille": "M", "couleur": "noir", "note_moyenne": 4.6, "nb_avis": 213
  }
}
```
**Champ pivot : `prix` + `stock` (durs).** « Robe d'été abordable » → sémantique + `prix<50 AND stock>0`.

### 6. Médical / santé (V)
**Niveau de preuve + type de source** en métadonnée = ce qui sépare un RAG médical sérieux d'un dangereux. `pathologie_code` (CIM-10) pour filtrage exact.

```json
{
  "id": "med-hta-traitement",
  "embedded_text": "Contexte : reco HAS 2024 sur l'HTA de l'adulte. 1re intention : IEC ou ARA2 en monothérapie. Contre-indications : grossesse, sténose bilatérale, hyperkaliémie. Surveiller créatinine + kaliémie.",
  "metadata": {
    "source_type": "guideline", "niveau_preuve": "A", "pathologie_code": "I10", "population": "adulte",
    "organisme": "HAS", "langue": "fr", "date_publication": "2024-09", "page": 12
  }
}
```
**Champ pivot : `source_type` + `niveau_preuve`** (`guideline AND niveau IN [A,B]` → que des recos validées).

### 7. Code / documentation technique (V)
Chunking **par fonction/classe** (AST, pas n lignes). Embedder docstring + signature + **résumé NL du corps** (les noms de fonctions matchent mal les queries en prose).

```json
{
  "id": "code-auth-validate-token",
  "embedded_text": "Fonction validate_token(token) -> User : vérifie/décode un JWT, lève AuthError si expiré/invalide, retourne le User. Authentifie chaque requête API entrante.",
  "metadata": {
    "langage": "python", "type": "code", "version_lib": "pyjwt-2.8", "repo": "neoia-api",
    "module": "auth.security", "statut": "actif", "file_path": "src/auth/security.py",
    "function_name": "validate_token", "dependances": ["jwt", "models.User"], "lignes": "L42-L67"
  }
}
```
**Champ pivot : `langage` + `version_lib` + `statut`** (exclut le code déprécié).

### 8. Financier / rapports (V)
**Entité + période** indispensables — c'est l'exemple-pilote d'Anthropic Contextual Retrieval (« revenue grew 3% » sans contexte = inutilisable).

```json
{
  "id": "fin-acme-q2-2023-revenue",
  "embedded_text": "Contexte : 10-Q d'ACME Corp Q2 2023 ; CA du trimestre précédent = 314 M$. Le CA a progressé de 3% vs trimestre précédent, porté par le logiciel.",
  "metadata": {
    "entite": "ACME Corp", "periode": "2023-Q2", "type_doc": "10-Q", "metrique": "revenue",
    "devise": "USD", "date_publication": "2023-08-04", "document_id": "sec-acme-10q-2023q2", "page": 23
  }
}
```
**Champ pivot : `entite` + `periode`.** Contextual Retrieval **obligatoire** ici.

## Récapitulatif décisionnel

| Cas | Champ pivot pre-filter | Levier embedding | Statut |
|---|---|---|---|
| Maintenance | `equipment_model` + `criticite` | fusion symptôme→remède en 1 chunk | R |
| **Proptech (Loji)** | `lot_id` + `type_doc` + `date_echeance` | contexte lot/bail | R |
| Support FAQ | `version_produit` | HyPE (questions hypothétiques) | V |
| Juridique | `juridiction` + `date_effet`/`version` | contexte hiérarchique clause | V |
| E-commerce | `prix` + `stock` (durs) | multi-vecteur attributs | V |
| Médical | `source_type` + `niveau_preuve` | confidence score | V |
| Code | `langage` + `version_lib` + `statut` | résumé NL + docstring | V |
| Financier | `entite` + `periode` | Contextual Retrieval | V |

**Socle universel (tous les cas)** : `chunk_id, document_id, source, title, page, chunk_index, created_at/version, doc_type, tenant_id (must-filter), language` + `chunk_text` (citation) / `embedded_text` (contexte+chunk, retrieval).

**Recommandation Loji** : figer en premier (1) l'unité-chunk « symptôme→remède » pour la maintenance, (2) le pre-filter `lot_id`/`type_doc`/`date_echeance` pour NeoDocs. Appliquer **Contextual Retrieval sur TOUS les cas** — seul levier validé chiffré (-35 à -67%) et gratuit côté design.

## Liens

- [[rag-metadata]] — principes transverses (3 couches, pre/post-filter, parsing, limites)
- [[rag-architecture]] — patterns avancés (GraphRAG, Contextual Retrieval, agentic)
- [[rag-chunking]] — stratégies de découpage
- [[rag-data-audit-discovery]] — l'audit data EN AMONT (questions → entités → data model)
- [[RAG]] · [[MOC-Techniques]]
