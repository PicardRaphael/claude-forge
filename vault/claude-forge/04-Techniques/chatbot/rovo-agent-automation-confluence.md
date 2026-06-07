---
titre: "Rovo agent en automation — contraintes Confluence (écriture, dédup)"
resume: "Contraintes dures d'un agent Rovo invoqué par automation : texte-seul via {{agentResponse}}, pas d'écriture native de contenu (REST obligatoire), dédup par grounding non fiable (indexing delays). Fork archi auto-merge vs gate validation."
aliases:
  - rovo automation confluence
  - rovo agent ecriture page
  - agentResponse confluence
  - rovo dedup doc
  - rovo agent limitations automation
derniere-maj: 2026-06-05
tags:
  - "#type/technique"
  - "#domaine/chatbot"
  - "#domaine/atlassian"
---

# Rovo agent en automation — contraintes Confluence (écriture, dédup)

Contraintes vérifiées (doc Atlassian, juin 2026) pour le chantier **chatbot support NeoIA** : pipeline ticket Jira (SC / AML) → agent Rovo rédige → page Confluence dans l'espace NeoIA → embedding (chaîne lecture neo_ia : voir [[comprendre-neoteem-vue-responsable-ia]]).

## Contraintes dures (agent invoqué PAR automation)

| Contrainte | Conséquence archi |
|---|---|
| Agent en automation **ne peut PAS utiliser ses skills** — réponse texte seule via `{{agentResponse}}` | L'agent **rédige le markdown**, il ne publie rien lui-même |
| Création/écriture/suppression de contenu **non supportée côté agent** | La **publication = l'automation**, jamais l'agent |
| Action native "Create Confluence Page" **n'écrit aucun body** (titre seul) | Body obligatoirement via **Send Web Request → REST** (`/wiki/api/v2/pages`) |
| Agent a accès aux **knowledge sources** (espace NeoIA) en lecture/recherche | Dédup *théoriquement* possible dans ses instructions, mais peu fiable (cf ci-dessous) |
| **Indexing delays** sur le knowledge source | Page juste ajoutée à "À valider" peut être non indexée → l'agent ne la voit pas → **doublon** sur le cas qui compte (ajouts récents) |
| **Branch-with-Conditions** Confluence (2026, Premium/Enterprise) | Signalé **cassé** côté Confluence (communauté) — ne pas l'assumer fonctionnel |
| Deep research : timeout automation **15 min**, 30 req/jour/user | Ne pas activer deep research dans un flux automation |

## Fork de décision — dédup ("pas de doc trop grosses / une page par problème")

Les deux moitiés du besoin sont **distinctes**, ne pas les fusionner :

1. **"Pas de doc pour rien"** → filtre *documentable* dans les **instructions de l'agent** (~80% des tickets SC sont client-spécifiques = non documentables ; ne documenter que questions de fonctionnement ou bug-où-l'user-fait-mal).
2. **"Pas une page par problème"** → fork archi :
   - **Option A — auto-merge dans l'automation** : l'agent retourne un **JSON structuré** (`décision: create|update`, `page_id_cible`, `markdown`) parsé en smart values → branchement → REST. Fragile : dédup ratée sur pages non indexées + branching Confluence cassé + parsing `{{agentResponse}}` délicat (erreur "Could not parse page content" connue).
   - **Option B — merge au gate "À valider" (recommandé)** : l'agent publie toujours un brouillon Q/R dans "À valider" ; le regroupement thématique se fait **à la validation** (humain ou passe de curation), pas dans l'automation déclenchée par ticket. Le dossier "À valider" EST le point de dédup naturel. Contourne d'un coup agent texte-seul + branching cassé + indexing delays.

## Format doc cible — pensé POUR le chunking/embedding

Paramètres RÉELS de prod (vérifiés dans `scripts/confluence_ingest_v2.py`, racine neot-v2, juin 2026 — 3e script de sync trouvé, tous lecture→embed) :

- **Chunker** : `RecursiveCharacterTextSplitter`, `chunk_size=2500` chars (~600 tokens, **dans la zone optimale**, sous le context cliff ~2500 *tokens*), `chunk_overlap=300`, séparateurs `["\n\n", "\n", ". ", ...]`.
- **Titre de page injecté en tête de CHAQUE chunk** (`# {page_title}\n\n{chunk}`) → chunk auto-suffisant.
- **Dédup à la sync = suppression+réinsertion par `page_id`** (`DELETE FROM langchain_pg_embedding WHERE cmetadata->>'page_id' = :page_id` puis ré-embed). **PAS de content_hash** → re-embed toute la page à chaque modif (gotcha coût, cf [[rag-chunking]] anti-gaspillage). Modèle prod = `text-embedding-004` Vertex (la cible neo_ia migrée = `gemini-embedding-001` 768d).

**Règles de format qui en découlent** (= structure déjà observée sur la page NeoIA "Lecteur de chèques", à conserver) :
1. **1 page = 1 thème**, découpée en sections `##` **autonomes** (le splitter coupe sur `\n\n`).
2. `> Module:` + `> Mots-clés:` en tête de page (le titre est déjà réinjecté par chunk).
3. Sections Q/R groupées : symptôme → cause → solution → escalade, anonymisées.

**Insight contre-intuitif (à dire à Raphael)** : « pas trop de pages » n'est **PAS** un objectif d'embedding — le nombre de pages est **neutre** pour le retrieval (1 grosse page = N chunks, 10 petites = N chunks). Le vrai levier contre « plein de doc pour rien » = **qualité des chunks + write-time scoring** (LLM note chaque chunk 1-10, ne vectoriser que `≥5` — pattern [[Jonas Roman]], cf [[rag-chunking]] section write-time). Regrouper par thème sert la **cohérence sémantique des chunks**, pas la réduction du nombre de pages.

## À prouver empiriquement (non tranchable par doc)

Le **grounding sur le knowledge source NeoIA fonctionne-t-il quand l'agent est invoqué par automation** (vs en chat) ? Plausible (le grounding n'est pas une "skill") mais non confirmé. Seule preuve = **mini-rule de test dans Rovo Studio**. Ne pas bâtir l'archi dédup-par-agent dessus sans ce test.

## Sources

- [Automating Rovo agents](https://support.atlassian.com/rovo/docs/agents-in-automations/)
- [Rovo agent permissions & governance](https://support.atlassian.com/rovo/docs/rovo-agent-permissions-and-governance/)
- [Jira automation actions](https://support.atlassian.com/cloud-automation/docs/jira-automation-actions/)
- [Branch with Conditions](https://community.atlassian.com/forums/Automation-articles/Introducing-Branch-with-Conditions-for-Atlassian-Automation/ba-p/3180282)

Lié : [[architecture-claude-api]] · [[architecture-crewai]] · [[index-architectures]]
