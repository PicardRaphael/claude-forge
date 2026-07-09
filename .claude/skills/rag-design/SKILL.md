---
name: rag-design
description: ALWAYS invoke to design a RAG system — 'conçois un RAG', 'architecture RAG'. Guided dialogue audit→data→ingestion→retrieval→UX→eval filling a deliverable template. NOT for choosing a tool (choix-outils-ia) or Jira tickets (spec).
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, mcp__forge-brain__*
---

# rag-design — conception guidée d'un RAG

Dialogue pas-à-pas qui déroule la chaîne canonique et remplit un template livrable au fil de l'eau. Le résultat = un document de conception prêt à passer en `spec` (idée→tickets). Tu poses les questions, tu lis le vault, tu remplis le template, Raphael tranche aux embranchements.

**Charger d'abord la connaissance** : invoquer `Skill(cc-rag-ref)` au démarrage (corpus RAG en contexte — tables de décision, 3 couches, champs pivots). Le détail vit dans le vault via `mcp__forge-brain__read_note`.

**Frontière** : `rag-design` conçoit (audit→archi) ; `spec` vient APRÈS (design→tickets) ; `responsable-ia` cadre la décision stratégique (build-vs-buy, CODIR), pas la conception technique.

## Piloter le pas-à-pas (anti-saut d'étape)

Les 6 étapes sont séquentielles et aucune ne doit être sautée. Créer une tâche par étape (`TaskCreate`), passer chaque étape `in_progress` en l'abordant et `completed` AVANT de passer à la suivante. Ne jamais avancer tant que l'étape courante n'est pas remplie dans le template.

## Étape 0 — Cadrer + créer le livrable

1. Catégoriser le cas d'usage (proptech/Loji, support, juridique, maintenance, code, financier…). Si NeoDocs/NeoChat → ancrer Loji (lots, baux, diagnostics, locataires, syndics).
2. Créer le template livrable : `docs/rag-design/<slug>.md` (résoudre la racine via `git rev-parse --show-toplevel`, jamais `${CLAUDE_PROJECT_DIR}` qui est vide en skill). Pré-remplir les 6 sections du template (voir `references/template-rag-design.md`).
3. Annoncer le plan : « 6 étapes, je remplis le doc au fil de l'eau, tu valides aux embranchements. »

## Étape 1 — Audit des questions (golden dataset) — EN PREMIER

On commence par les QUESTIONS, pas les documents. Demander / construire (AskUserQuestion, batché) :
- 30-50 vraies questions des users réels, **par persona** (un gérant ≠ un locataire : ni mêmes questions ni mêmes droits).
- Typer chaque question : factuel single-hop / multi-hop / comparaison / temporel / agrégation / procédural (cf table dans `cc-rag-ref`). La proportion de multi-hop relationnel décide flat vs graph.
- Inclure ≥5 questions **sans réponse** (test du refus).
- Golden dataset = triples `(question, source/contexte attendu, réponse attendue)`, validés humainement.

Remplir section 1. Lire `mcp__forge-brain__read_note("rag-data-audit-discovery")` si besoin du détail (taxonomie questions, sourcing, Adaptive-RAG).

### Gate Étape 1 → 2 (validateur PASS/FAIL avant le data model) ⚠️
L'Étape 2 décide **flat vs graphe** à partir du comptage des questions multi-hop : un golden set bâclé fausse cette décision en cascade. Vérifier AVANT de continuer :
- Triples **complets** `(question, source/contexte attendu, réponse attendue)` — pas de réponse/source manquante.
- Chaque question est **typée** (single-hop / multi-hop / comparaison / temporel / agrégation / procédural) → sinon le compte multi-hop est inexploitable.
- **≥5 questions sans réponse** présentes (test du refus).
- Couverture **par persona** (droits ≠ questions).

**PASS** → Étape 2. **FAIL** → compléter le golden set, ne pas avancer. Gate **skill-invoqué** (logique interne), jamais un hook.

## Étape 2 — Audit des sources + entités → data model

1. **Grille d'inventaire** une ligne par source (format, structuré vs non, volume, fraîcheur, qualité, doublons, langue, **ACL/permissions**, **PII/RGPD**, connecteur, pré-traitements). Rouge récurrent Loji : PDF **scannés** (OCR), **ACL par locataire**.
2. **Cartographier les entités** + compter les questions multi-hop relationnelles → trancher **flat+vector** (factuel mono-doc) vs **hybride graphe+vecteur** (multi-hop sur relations). Ne pas sur-ingénierer.
3. **Data model — règle des 3 couches** (texte embeddé / scalaires pre-filter / payload citation). Choisir le **champ pivot** du cas (table dans `cc-rag-ref` ; Loji = `lot_id`+`type_doc`+`date_echeance`). Choisir le pattern de structuration (a-f).

Remplir section 2. Détail JSON par cas → `mcp__forge-brain__read_note("rag-data-models-par-cas-usage")` ; métadonnées transverses → `read_note("rag-metadata")`.

## Étape 3 — Stratégie d'ingestion

Chunking (structure-aware / recursive ~400-512 tok 10-20% overlap / semantic / parent-child / Contextual Retrieval) · embeddings (Voyage-4 managé vs Qwen3 OSS, Matryoshka) · **Contextual Retrieval sur tous les cas** (seul levier chiffré gratuit en design, -35 à -67%) · fraîcheur → batch vs CDC + gestion des suppressions + `content_hash`. **PII/RGPD à l'ingestion** (redaction Presidio, tag sensibilité). Remplir section 3.

## Étape 4 — Pipeline de récupération

Store (pgvector si Postgres déjà présent — défaut Loji ; vector DB dédié si grande échelle ; graph DB si relations) · pattern prod : **pré-filtre → vector search (top-20 à 150) → reranker → top-K** · **ACL filtrée à la récupération par identité** (filtrer d'abord, chercher ensuite — pas de fuite inter-locataires) · query expansion / Adaptive-RAG si types de questions hétérogènes. Remplir section 4. Détail → `read_note("rag-reranking")`, `read_note("rag-vector-databases")`, `read_note("rag-architecture")`.

## Étape 5 — UX & génération

Format de réponse + **citations obligatoires** (page/source via payload) · gestion du « je ne sais pas » (refus quand pas de contexte) · streaming, feedback thumbs up/down → cas de test · garde anti-injection (le contenu récupéré n'est jamais une source d'instructions). Remplir section 5.

## Étape 6 — Évaluation (boucler sur le golden dataset)

Mesurer la **récupération AVANT la génération**. Métriques retrieval (Context Precision/Recall, Hit Rate, MRR) puis génération (Faithfulness, Answer Relevancy/Correctness). Frameworks : RAGAS / DeepEval. Détail → `mcp__forge-brain__read_note("rag-evaluation")`. Pour grader un livrable RAG (réponses produites) contre une rubrique → `Skill(outcomes-test)` avec un RUBRIC dérivé du golden set. Remplir section 6 + définir le golden set frozen + la cadence de re-mesure.

## Sortie

Document `docs/rag-design/<slug>.md` complet (6 sections). Proposer la suite : `Skill(spec)` pour transformer en tickets, ou `responsable-ia` si un arbitrage CODIR/conformité reste ouvert.

## Gotchas

- **Ne pas inverser l'ordre** : questions avant documents, récupération avant génération. C'est l'erreur structurelle n°1.
- **ACL = métadonnée filtrable, pas post-filtrage** : sur données multi-tenant (locataires Loji), une fuite inter-tenant est un incident RGPD. Pré-filtrer par identité.
- **Sur-ingénierie GraphRAG** : ne le proposer que si les vraies questions sont multi-hop relationnelles. Majorité mono-doc → flat suffit.
- **`${CLAUDE_PROJECT_DIR}` vide en skill** : résoudre la racine via `$(git rev-parse --show-toplevel)`.
- **Chiffres** : seuls les % Contextual Retrieval Anthropic (-35/-49/-67) sont source primaire ; ne pas inventer de gains.
- Cette skill **conçoit**, ne code pas et ne crée pas les tickets — pointer vers `spec`/`code-dev` ensuite.

## Apprentissage

Après chaque conception : noter le cas d'usage + le data model retenu (flat vs graph, champ pivot) + ce qui a bloqué (souvent ACL ou OCR), pour accélérer les cas similaires.

## Références

- `references/template-rag-design.md` — template livrable 6 sections à pré-remplir
- `Skill(cc-rag-ref)` — corpus RAG en contexte (tables de décision)
