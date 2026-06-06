# BRIEF — neo_ia : pipeline Confluence qualité + skill brain→Confluence

> Contrat pour `neo_ia`. À copier dans `neo_ia/TODO/feature-rag-support-multi-source/`. Voir `SPEC.md` pour le contexte complet.
> Architecture : « tout converge vers Confluence » — Confluence = seule source embeddée.

## Contexte
Agent support RAG existant et mature (NON refondu). Pipeline Confluence existant (`shared_utils/confluence/`, `scripts/confluence_sync.py`). Contrainte : **Gemini/Vertex exclusif**, **jamais de DDL en code**.

## À faire

### V0 — Barrière « À valider » (RISQUE ÉLEVÉ — prérequis dur)
1. **Exclure les pages non validées du sync** : ajouter au CQL `status:current` **ET** `label != "a-valider"` dans `get_modified_pages` (chemin incrémental, aujourd'hui SANS filtre statut) **ET** vérifier `get_all_pages`. Les DEUX chemins, sinon la barrière fuit.
2. **Bascule espace** : sync cible `NeoIA` (pas `NEO`). Ajuster `space_key` défaut + commande. ⚠️ cutover collection `confluence_docs` à confirmer (PO).

### V1 — content_hash anti-ré-embedding
3. Dans `ingestor.py` `_process_page` : `content_hash = sha256(content)` avant chunking ; comparer au hash stocké en `cmetadata` ; **inchangé → skip total** (pas de chunk, pas de LLM-context Gemini, pas d'embedding). Modèle : `mcp-obsidian-brain/src/watcher.py:57-69` + `database.py:93-95`. Stocker le hash en `cmetadata`.

### V2 — Description d'images via Gemini multimodal
4. Dans `processor.py`/`ingestor.py` : pour chaque image détectée (`_insert_image_markers`), télécharger (`client.download_attachment`), décrire via `get_genai_client()` (`gemini-2.5-flash`, **PAS Mistral OCR** — contrainte Gemini), injecter la description en texte dans le chunk. Décrire seulement si page changée (combiner V1) + cacher en `cmetadata`. GIF reste en lien.

### V3 — ConfluencePublisher (BLOCKER #2 : écriture inexistante)
5. **CREER** `shared_utils/confluence/publisher.py` (`ConfluencePublisher`, séparé de `client.py` read-only) : `POST /wiki/api/v2/pages` (création, parent=page « À valider »), `PUT /wiki/api/v2/pages/{id}` (MAJ idempotente), `POST .../label` (poser `a-valider`), recherche d'existence par titre create-vs-update. Auth = session `parametrage documentation_lojii`.

### V4 — Skill brain→Confluence
6. **CREER** `neo_ia/.claude/skills/brain-to-confluence/SKILL.md` : sélectionne les notes brain `#statut/valide` (07-Support, 06-Regles-Metier), les transforme en pages Confluence « parfaites RAG » (titre=question, sections H2/H3 auto-suffisantes, problème→cause→solution, labels=domaine+type, wikilinks traduits, descriptions d'images), publie sous le dossier « À valider » de NeoIA + label `a-valider` via `ConfluencePublisher`. Validation humaine avant mise en ligne.

## Fichiers
- MODIFIER : `shared_utils/confluence/{client.py,ingestor.py,processor.py}`, `scripts/confluence_sync.py`
- CREER : `shared_utils/confluence/publisher.py`, `.claude/skills/brain-to-confluence/SKILL.md`

## Référence BDD
- Vector DB `get_async_session_vector()`, collection `confluence_docs`. Credentials Atlassian table `parametrage` type=`documentation_lojii`. **JAMAIS de DDL en code** (content_hash va en `cmetadata` JSONB, pas en nouvelle colonne).

## Critères de done
- [ ] Une page avec label `a-valider` n'est JAMAIS embeddée (testé sur les 2 chemins CQL).
- [ ] Sync cible NeoIA.
- [ ] Page inchangée → 0 appel embedding + 0 appel LLM-context (vérifié par log/compteur).
- [ ] Image dans une page → sa description Gemini est présente dans le chunk embeddé.
- [ ] `ConfluencePublisher` crée/met à jour une page + pose le label.
- [ ] Skill brain→Confluence produit une page dont chaque section est une réponse auto-suffisante.

## Implementation Notes
Maintenir `docs/implementation-notes/rag-support-confluence-pipeline.md`.

## Acceptance Tests
- Test barrière : créer une page labellée `a-valider` → `confluence_sync.py` ne l'ingère pas ; retirer le label → elle est ingérée au sync suivant.
- Test hash : 2 syncs consécutifs sans modif → 0 ré-embedding au 2e (compteur).
- Test image : page avec capture → chunk contient la description Gemini.
- `pytest apps/neochat/tests/unit/` ciblé sur les modules touchés — vert.

## Bloquants PO (SPEC §7)
Cutover NEO→NeoIA · mécanisme barrière (label A) · validation manuelle V1 · coût Gemini images.
