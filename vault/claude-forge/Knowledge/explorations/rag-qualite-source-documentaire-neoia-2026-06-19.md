---
titre: "Qualité RAG = qualité de la source documentaire (audit 250 pages NeoIA)"
resume: "Retour d'expérience : sur un RAG support 2-sources (Confluence + vault), la cause racine des mauvaises réponses était la GRANULARITÉ des docs (17% multi-thèmes) et des mots-clés non discriminants, pas le pipeline. + gotchas : skill générateur amont, collection vectorielle partagée DELETE destructif, re-sync ciblé, défense en profondeur PII, et faux négatif du grading par synonymie de marque (NEOTEEM=Lojii)"
aliases:
  - "qualité rag source documentaire"
  - "rag multi-thèmes mots-clés discriminants"
  - "audit docs confluence neoia rag"
  - "collection vectorielle partagée delete danger"
  - "qualité doc amont rag"
  - "grading faux négatif synonymie marque"
domaine: ia
type: exploration
derniere-maj: 2026-06-23
auteur: claude
tags:
  - "#type/exploration"
  - "#domaine/ia"
  - "#domaine/rag"
  - "#projet/neo_ia"
---

## Contexte

Agent Support NeoChat (neo_ia) = RAG 2-sources : Confluence NeoIA (~250 pages) + vault neoteem-brain (07-Support), MÊME collection pgvector `confluence_docs`. Problème signalé : « réponses pas parfaites ». Pipeline déjà bon (hybrid RRF + grading LLM + reranker bge + Contextual Retrieval). Audit read-only des 250 pages (5 agents parallèles via MCP Confluence).

## Constat — la cause racine est en AMONT, pas dans le pipeline

- **~42 pages / 250 (17%) multi-thèmes** (≥4 sujets indépendants : « 10 erreurs de paie » = 10 sujets, « paramétrage admin » = 6). Le Contextual Retrieval génère 1 résumé PAR PAGE → sur une page fourre-tout, chaque chunk reçoit un contexte vague + des mots-clés mutualisés. Retrieval flou, grading qui hésite, génération qui mélange.
- **Mots-clés non discriminants** : `NEOTEEM` dans ~100% des pages (bruit pur) ; `correspondance` (15 docs), `copropriété` (14)… Un bloc mots-clés IDENTIQUE copié verbatim sur 4 pages. Le grading par mots-clés ne discrimine alors plus rien.
- **Keyword-stuffing** induit par la règle d'écriture (« répéter 2-3 fois ») → « copropriétaires copropriétaires », dégrade l'embedding.

**Leçon clé** : un pipeline RAG state-of-the-art ne sauve pas une source mal structurée. La qualité de la réponse = qualité de la doc. Cohérent avec [[RAG]] « audit data en amont ». Avant de tuner le retrieval, AUDITER la granularité documentaire (1 page = 1 sujet ?) et la discrimination des mots-clés entre docs.

## Granularité : scinder selon les UNITÉS que l'utilisateur cherche

- Catalogue d'erreurs / troubleshoot multi-causes → 1 page par erreur/cause (chacune = une procédure distincte que l'user cherche)
- Glossaire → FAQ par DOMAINE (~8-10 pages), PAS 1 page/terme (70 micro-pages = chunks faméliques qui noient l'espace) ni 1 page fourre-tout
- Doc « config » couvrant N réglages sans rapport → 1 page par réglage
- Critère : scinder dès ≥3 sujets INDÉPENDANTS, jamais sur un seuil de taille seul (un doc de 4295 chars peut contenir 10 sujets).

## Mots-clés : différencier, ne pas répéter

Anti-pattern : règle d'écriture qui dit « répéter les mots-clés » → optimise le recall lexical d'une page ISOLÉE mais détruit la discrimination ENTRE pages. Bon pattern : mots-clés qui DISTINGUENT la page (codes exacts, écrans, versions, termes rares) ; interdire le nom du produit/module seul et tout terme présent dans >5 pages du module.

## Gotcha 1 — corriger le générateur AMONT, pas seulement l'aval

Les docs étaient produites par un skill (Cowork `neodoc`). Ses règles d'écriture fabriquaient les défauts (règle « répéter », seuil de scission par taille). Réflexe : remonter au PRODUCTEUR de la donnée. Réparer 42 pages à la main sans corriger le skill = les régénérer au prochain doc. Le levier le plus haut est la source de la source.

## Gotcha 2 — collection vectorielle PARTAGÉE = DELETE de réconciliation destructif

Confluence + vault dans la MÊME collection. Une « purge des orphelins » naïve (« supprimer tout page_id absent de la liste Confluence ») verrait les chunks du vault (page_id = chemins de fichiers) comme orphelins → **DELETE massif des chunks de l'autre source**. Bug invisible en test unitaire (mock), visible seulement en intégration. Règles : (a) un DELETE de masse prod ne va jamais dans une PR fourre-tout ; (b) scoper par `space_key`/source ; (c) souvent **inutile** : si on réindexe la collection FROM SCRATCH après une refonte, les orphelins disparaissent sans code destructif. Le bon ordre des opérations élimine le besoin.

## Gotcha 3 — MCP Atlassian (Cowork) n'expose PAS de suppression de page

Le connecteur Atlassian de Cowork expose `createConfluencePage` et `updateConfluencePage`, mais **aucun outil de suppression**. Conséquence pour une scission (1 page fourre-tout → N pages atomiques) : impossible de supprimer l'ancienne page par programme. Pattern de contournement :
1. Créer les N nouvelles pages.
2. **`updateConfluencePage` sur l'ancienne** → la vider et la remplacer par un court renvoi vers les nouvelles, bloc Mots-clés vide (pour qu'elle ne matche PLUS au retrieval). Ça la **neutralise immédiatement** : tant qu'elle garde son contenu complet, elle concurrence les nouvelles au retrieval (doublon).
3. **Tracker les pageId** des anciennes pages dans le fichier de progression → suppression/archivage MANUEL groupé dans Confluence à la fin du run.
4. La réindexation full du RAG (plus tard) retire définitivement les pages neutralisées.

Règle : neutraliser (update vide) AVANT de réindexer ; ne jamais laisser une ancienne page scindée avec son contenu actif. Distinct du Gotcha 2 (DELETE vectoriel) : ici c'est la page Confluence SOURCE, pas les chunks.

## Gotcha 4 — Un skill multi-cibles, pas un skill qui duplique les règles

Cas : le RAG support a 2 sources (Confluence + fichiers .md du vault). Réflexe tentant = créer un 2e skill « neodoc-brain-doc » pour écrire les .md. MAUVAIS : les règles de qualité RAG (granularité, mots-clés discriminants, anti-stuffing) sont IDENTIQUES — seule la CIBLE DE SORTIE diffère (page Confluence via MCP vs fichier .md sur disque). Dupliquer les règles dans 2 skills = drift garanti (on change une règle, on l'oublie dans l'autre).

Bon pattern : UN skill orchestrateur (`neodoc-write-doc`) avec N **sources d'entrée** (URL/PDF/vidéo/image/texte) ET N **cibles de sortie** (Confluence / fichier .md vault). Les règles vivent une seule fois ; entrée et sortie sont des handlers. Cohérent avec « 1 concept = 1 foyer canonique » ([[feedback_single_source_truth_vault_canonique]]) appliqué aux skills.

Corollaire ingestion : quand un script de sync (ex. `neoteem_brain_sync.py`) avale un fichier monolithique (lexique 48 Ko), le problème n'est PAS le script (sain) mais la MATIÈRE (le .md non atomique). On nettoie le contenu source, on ne modifie pas le script.

## Suite empirique — bilan mesuré du chantier (21 juin 2026)

Après l'audit amont (19 juin), le chantier a MESURÉ le RAG au lieu de supposer. Verdict en 3 temps :

1. **Routing (boost route_query) = sain mais marginal** : sur un golden set pannes→note-brain hors-sample, 1 rescue / 0 régression. Peu de rescues NON parce que le boost échoue, mais parce que la baseline full-text trouvait déjà 6/7 (pannes à code d'erreur explicite). → cf [[rag-evaluation]] « Faible rescue ≠ boost inutile » (3 causes : gap sémantique / redondance / trou de contenu).
2. **Restitution (chunking + embeddings) = saine** : les « échecs » du golden set usage-normal étaient à 2/3 des **labels trop stricts** (une note voisine légitime domine la cible notée), pas des défauts de ranking. Le hit@3 « 80% » SOUS-ESTIMAIT la vraie qualité. Leçon : un golden set à cible unique surdéclare les échecs — accepter les cibles multi-valides.
3. **Seul vrai levier = la COUVERTURE** (cohérent avec le constat amont du 19 juin) : formulations clients sous le seuil sémantique + codes d'erreur absents des notes. C'est là qu'on a agi (3 trous comblés, dont lettrage TVA 96TZ/97T2 : miss → rang 2 après ajout d'une sous-section + entrée lexique).

**Décision prouvée non rentable** : étendre le lexique de routage pour cibler des pages Confluence (pas seulement des notes brain). Le boost matche par égalité de clé `page_id` ; les cibles Confluence sont des IDs numériques, les cibles brain des chemins POSIX → asymétrie structurelle. Construire le pont (map brain→Confluence) = coûteux + fragile, pour un gain là où le boost sert le moins (la baseline trouve déjà). On ne le fait pas.

## Gotcha 5 — Re-sync ciblé d'UNE note sans flag dédié (mini-vault temp + UPSERT idempotent)

`neoteem_brain_sync.py` n'a pas de flag `--file`/`--since`/diff : ses seuls modes sont `--vault-path` (tout le vault) + `--limit`/`--dry-run`. Réflexe naïf après avoir modifié UNE note = rebuild complet → ré-embed des 1671 chunks (coût Vertex, 1 appel LLM/page × ~222 pages pour le Contextual Retrieval) + refait les exclusions. **Inutile et risqué pour une seule note.**

Bon pattern (prouvé 21 juin) : l'écriture est un **UPSERT idempotent par chunk** (ID `uuid5(NAMESPACE, f"{page_id}:{chunk_index}")` déterministe, `INSERT … ON CONFLICT (id) DO UPDATE`), sans DELETE global. Donc pour re-syncer UNE note, l'**isoler dans un mini-vault temporaire** (la note dans son sous-dossier `07-Support/faq/` + dossiers `procedures/`+`problemes-connus/` VIDES pour que `collect_notes` n'en collecte qu'une) → `--vault-path <tmp>` → UPSERT sur les seuls chunks de cette note, reste de l'index jamais touché. Delta prouvé : 1671 → 1673 (+2 chunks pour une sous-section), exclusions lexique/glossaire intactes (l'exclusion vit dans `collect_notes`, respectée par construction).

Garde-fous : (a) **garder le contexte LLM activé** (pas `--no-context`) si l'index a été bâti avec Contextual Retrieval, sinon les chunks re-syncés divergent du reste ; (b) le `.md` à jour doit être **physiquement sur le disque** pointé par `--vault-path` (le script lit le fichier, pas une version git distante) ; (c) UPSERT ne supprime pas les chunks orphelins — sûr quand une note GRANDIT (chunk_index croissants), à surveiller si elle RÉTRÉCIT. Distinct du Gotcha 2 (DELETE vectoriel de réconciliation, lui destructif).

## Gotcha 6 — « C'est déjà neutralisé en amont » ne dispense PAS du filet aval (défense en profondeur, critère structurel)

Cas (21 juin) : audit du prompt de génération de l'agent support → axe anti-PII (masquer noms/email/IBAN/SC dans la réponse client). Objection naturelle de Raphael : « on a déjà fait en sorte que les docs indexés ne contiennent pas de PII (corps de note neutres, SC en frontmatter strippé à l'ingestion), donc le filet à la génération est-il vraiment obligatoire ? »

Réponse — le filet aval est P0 **non par principe de redondance**, mais parce que la couche amont est **structurellement incapable** de couvrir trois sources de fuite :

1. **Source non sous contrôle éditorial** : le RAG mélange brain (corps maîtrisés) ET Confluence (rédigé hors équipe). Une page Confluence avec un exemple « réaliste » (nom, email, IBAN de test) part dans l'index sans qu'on le voie passer. La neutralisation des corps brain ne l'atteint pas.
2. **L'entrée utilisateur**, jamais filtrée à l'ingestion : la question peut contenir un nom/SC que le LLM reprend dans sa reformulation (« comme indiqué pour le dossier de M. X… »). Le RAG ne contenait pourtant aucune PII. Seul un filtre sur la SORTIE voit la réponse réelle.
3. **Les écritures futures non disciplinées** : la garantie amont est « par discipline » (on a fait attention), pas « par construction ». Une note ajoutée sans la discipline, ou une page Confluence non revue, et la seule défense encore debout est le filtre de sortie.

**Critère réutilisable** : pour décider si un garde aval reste obligatoire alors qu'une couche amont existe déjà, ne pas trancher « déjà couvert → on retire » ni « toujours redonder par sécurité ». Lister ce que la couche amont **ne peut PAS couvrir par construction** (sources hors contrôle, entrées non filtrées, évolutions futures). S'il reste un seul vecteur non couvert ET que l'invariant l'interdit (ici l'étoile polaire « ne fuite pas de données »), le filet aval est obligatoire. Coût à pondérer : ici très faible (brancher le Presidio EXISTANT `shared_utils/observability/pii.py` sur la sortie + regex `SC-\d+`), filet permanent → P0 confirmé. Spécialisation du swiss cheese ([[Thariq Shihipar]]) et des 7 couches ([[agents-securite]]) : la question n'est pas « combien de couches » mais « quel vecteur chaque couche laisse passer ».

Corollaire allowlist : le masquage support doit garder les **montants** (« solde de 150 € » > « solde de `<MONEY>` » qui casse l'étoile polaire « dit tout ce qu'il a »). D'où l'allowlist Support sans MONEY → factoriser dans le package (`mask_pii_entities(text, entities)` paramétrable, `mask_pii` reste le wrapper inchangé) plutôt que dupliquer le moteur PII dans l'agent (single-source, cf [[feedback_single_source_truth_vault_canonique]]).

**Suite (livré PR #33)** : l'allowlist Support a finalement EXCLU `PERSON` (pas seulement MONEY) — le NER spaCy FR masque les noms de sociétés/produits VOULUS (Yousign, Edilink, VoRio) comme des personnes, ce qui casserait des réponses légitimes. Allowlist finale = `EMAIL_ADDRESS, PHONE_NUMBER, IBAN_CODE` + post-pass regex `SC-\d+`. PERSON réintroductible un jour seulement derrière une allowlist produit déterministe, validée par une mesure (test corpus libellés produit, vrai Presidio). Trous résiduels ASSUMÉS et tracés P1 : nom-personne en clair non masqué + stream SSE temps réel non masqué (le masquage vit dans `respond_node` = persisté, pas le flux token-par-token).

## Gotcha 7 — Faux négatif du grading LLM : synonymie de marque NEOTEEM=Lojii ignorée (cause RÉELLE, prouvée 22-23 juin)

Cas : query « comment on fait vote extranet sur **lojii** ? » → le bot répond « pas trouvé » (interrupt `documentation_gap`) ALORS QUE la bonne page (« Comment voter par correspondance par Extranet », id 3555950601) est récupérée au **rang 4** du top-5. Root cause = **le grading LLM rejette 0/5 docs** — faux négatif.

> ⚠️ **Piste initiale INFIRMÉE** : on a d'abord soupçonné « le grader ne voit pas le mot vote » (métadonnée pauvre). **Faux, prouvé par le diagnostic** : le `summary` ET les `keywords` passés au grader contenaient parfaitement « vote/voter par correspondance ». Enrichir la métadonnée n'aurait rien changé. Leçon de méthode : ne pas figer une cause sans le **test discriminant** (cf ci-dessous) — la 1re hypothèse était plausible et fausse.

**VRAIE cause (test discriminant, déterministe, 2 runs/variante)** : on ne change QUE le nom de marque dans la query, mêmes 5 docs :

| Query | Cible 3555950601 | gardés |
|---|---|---|
| « …sur **lojii** » | rejetée — *reason : « parle de vote extranet mais sur NEOTEEM, pas sur Lojii »* | 0/5 |
| « …sur **NEOTEEM** » | acceptée | 1/5 |
| « voter sur l'extranet » (sans marque) | acceptée | 1/5 |

→ Le nom de marque est le **seul** facteur causal. Le grader traite « Lojii » et « NEOTEEM » comme **deux produits différents** et rejette pour « hors-périmètre marque ». Or **NEOTEEM = Lojii = Vorio = le même produit** (`parser.py` les listait déjà comme noms-produit équivalents — mais cette connaissance ne remontait PAS au grader).

**Correctif livré (PR `bug/support-grading-marque-synonymie`)** :
1. **Single-source** : constante `PRODUCT_NAME_SYNONYMS = frozenset({"lojii","neoteem","vorio"})` dans un module leaf `shared_utils/support_synonyms.py` (seul toit importable par `scripts/` ET `apps/` selon import-linter), consommée par parser + grader + prompt génération. Le `_STOPWORDS` du parser est scindé `_GENERIC | PRODUCT_NAME_SYNONYMS` (union = ensemble exact, zéro régression). Pas de 2ᵉ liste recopiée.
2. **2 FOYERS, pas un** (grep marque obligatoire) : le grader (`grading.py`) ET le prompt de génération (`prompts.py VERBATIM_RULES`) faisaient la confusion. Patcher seulement le grader aurait fait réapparaître le bug au node `generate`. Toujours grep le terme fautif dans TOUT le pipeline avant de conclure « foyer unique ».
3. **PAS de garde-fou « 0/N → garder des docs »** (Fix envisagé puis RETIRÉ) : il inversait la doctrine d'abstention anti-hallucination (`test_retrieval_node.py` : 0/N pertinent → `[]`, choix délibéré « mieux vaut "pas trouvé" qu'inventer »). Fix 1 réglant la cause à la source, le garde-fou devenait inutile ET dangereux (après le fix, un 0/N est plus probablement légitime). La session l'a stoppé en écrivant les tests, preuve à l'appui. Leçon : un « filet de sécurité » qui inverse une doctrine testée = décision séparée, pas un sous-produit d'un fix.
4. **DeepEval double test anti-faux-vert** : (a) « vote extranet sur lojii » → garde 3555950601 ; (b) « demander accès extranet **sur lojii** » → rejette la page de vote. Le (b) GARDE la marque « lojii » pour prouver que le rejet vient du SUJET (accès≠vote) et PAS de la marque — sinon le test passerait pour la mauvaise raison (faux-vert) en masquant une régression de synonymie.

### Sous-gotcha — la trace Langfuse ne tranche PAS un faux négatif de grading (I/O des nodes vide)

La trace de cette query confirme le **chemin** (`Agent Support` → retrieve → grade_documents → _should_generate → no_docs_found → interrupt `documentation_gap`) mais **tous les nodes LangGraph ET le `GENERATION` du grader ont `input`/`output`/`metadata` à `null`** (limite d'instrumentation Support). Donc la trace **prouve l'échec mais pas la cause** : impossible d'y lire ce que le grader a reçu ni pourquoi il a rejeté. Pour diagnostiquer un faux négatif de grading → **reproduire en local avec logging** (c'est le `reason` du grader, récupérable en local seulement, qui a tranché la cause).

**Observabilité livrée (même PR)** : `add_node_metadata` sur `retrieve_node` + `grade_documents_node` capture désormais query, docs (page_id+titre+score), **verdict grader par doc (relevant + reason)**, branche finale. Avec **masquage PII obligatoire** (`redact_for_observability` réutilise `mask_support_pii`) — sinon l'observabilité rouvrirait une fuite PII par la porte de derrière (query client + reason + titres en clair dans Langfuse), ce qui contredirait PR #33. Politique flag OFF = champ **omis** (pas masquage-en-clair fragile). 5 champs couverts dont le `error` (un message d'exception embedding peut inliner la query — 5ᵉ foyer trouvé par le reviewer). Relié au chantier online evals Langfuse (US6).

## État réel du pipeline retrieval Support (analyse 3 traces Langfuse, 2026-06-22)

Faits établis sur le pipeline neo_ia réel (utile pour ne pas re-découvrir) :

- **Latence dominée à 95-96% par 2 appels Gemini séquentiels** (grade + generate, ~6s chacun, TTFT ~5s). Le retrieval/routing/cache cumulent ~0,5s. Optimiser le retrieval ne touche PAS le goulot — c'est les LLM.
- **Prompt caching Gemini INACTIF** (`input_cache_read:0` sur les 3 traces). Cause racine : le docstring de `factory.py` croit le caching « automatic, managed by Google » → vrai pour l'**API Gemini directe**, FAUX pour **Vertex via `ChatGoogleGenerativeAI`** (caching explicite `CachedContent` ou implicite-sous-conditions). Levier coût/latence n°1, zéro risque qualité. Toujours vérifier la doc primaire Vertex avant de prescrire le fix.
- **Le reranker bge n'est PAS en prod** : Dockerfile neochat = `--extra pii` seul, pas `--extra reranker` (torch ~2,5 Go). `rerank_node` → ImportError → `docs[:5]` = no-op total. Donc le pipeline prod = hybrid+RRF → **grading LLM (le vrai filtre)** → generate, SANS reranking cross-encoder. Décision implicite assumée : le grading LLM joue le rôle du reranker. Activer un reranker = managé (Cohere), pas bge CPU-bound sur Cloud Run sans GPU.
- **Le grading n'est PAS sensible au nombre de docs** : 1 batch call sur métadonnées courtes, dominé par le thinking (1024 tokens). « Moins de docs → grading plus rapide » est FAUX. Réordonner retrieve/rerank/grade pour alléger le grading ne gagne rien.
- **Thinking sur le grader = VOULU**, pas du gaspillage : ajouté pour corriger le grading (cas « erreur 224 » 0/5→4/5, synonymes « regul »↔« régularisation »). Ne pas couper. Calibrer (1024→512) seulement sous test de non-régression du cas 224.
- **Caches multiples à ne pas confondre** : global cache (Level 1, questions répétées, sain) · thread cache (Level 2, suivis intra-thread, buggé par un pattern `is_followup_question` trop laxiste qui sert les docs du mauvais sujet sur un changement de sujet) · cache sémantique (`check_cache`) · embedding cache · prompt caching Gemini (différent, côté API). Le bug « mauvais docs » = le pattern laxiste, pas « le cache » — fix chirurgical (whitelist référentielle : tout mot de contenu hors stopwords génériques → miss), pas couper tout le cache.

Méta-leçon : analyser des traces 1 Mo → fan-out sous-agents (1 par trace, extraction jq, pas de JSON brut en contexte). MAIS la session principale voit la CONVERSATION ENTIÈRE et le contexte historique (pourquoi le thinking a été ajouté) que les agents isolés ratent — croiser les deux. Vérifier l'état RÉEL (Dockerfile, `input_cache_read`, install) avant de prescrire : plusieurs « optimisations évidentes » étaient invalidées par le réel (reranker absent, grading insensible au doc-count, caching faux-automatique).

## Méthode réutilisable

1. Audit read-only multi-agents (1 lot/agent) sur 3 axes : atomicité, discrimination mots-clés, découpage structurel — avec note /5 par doc.
2. Corriger le générateur amont (skill/template) AVANT de réécrire en masse.
3. Pipeline : Contextual Retrieval par SECTION plutôt que par page (rattrape l'existant sans réécrire) — additif, mesurable.
4. Réindex full from scratch après refonte (pas de purge incrémentale destructive).
5. Mesurer (golden set : faithfulness, context recall, ET source-balance sur collection partagée).
6. **Diagnostic d'un faux négatif de grading** : test discriminant qui isole UN facteur (ici la marque) AVANT de figer la cause ; grep le terme fautif dans TOUT le pipeline (souvent ≥2 foyers) ; ne jamais inverser une doctrine testée (abstention) au nom d'un filet.

## Liens

- [[rag-chunking]] — chunking + Contextual Retrieval (foyer technique)
- [[RAG]] — audit data en amont (chaîne audit→data→retrieval)
- [[rag-embeddings]] · [[rag-reranking]] — couches aval (n'étaient PAS le problème ici)
- [[rag-evaluation]] — golden set, faible rescue ≠ boost inutile
- [[neodoc-architecture]] — autre RAG neo_ia (NeoDoc, distinct du Support)
- [[reference-technique-stack-ia]] §3.6 Contextual Retrieval, §3.7 Ragas
- [[feedback_single_source_truth_vault_canonique]] — un concept = un foyer (appliqué à PRODUCT_NAME_SYNONYMS)
