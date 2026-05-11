---
titre: "NeoDoc Ingestion Pipeline — Drive/Upload → GCS → Vertex AI Discovery Engine"
resume: "Pipeline d'ingestion documentaire 7 étapes : download Google Drive (export PDF natifs) → upload GCS → import Vertex AI Discovery Engine avec metadata multi-tenant, modes sync/async/batch/folder, retry intelligent, notes indexables"
aliases:
  - "neodoc ingestion pipeline"
  - "neodoc ingestion"
  - "pipeline ingestion neodoc"
  - "neodoc document pipeline"
  - "vertex ai import neodoc"
  - "neodoc drive ingestion"
type: context
status: active
derniere-maj: 2026-05-11
auteur: claude
tags:
  - "#type/context"
  - "#type/technique"
  - "#projet/neo-ia"
  - "#domaine/rag"
---

## Concept

NeoDoc permet aux utilisateurs d'importer des documents depuis Google Drive ou par upload direct. Chaque document passe par un pipeline d'ingestion qui le stocke dans GCS et l'indexe dans Vertex AI Discovery Engine pour la recherche RAG.

## Pipeline Google Drive (7 étapes)

```
1. Create DB record (status: pending)
       │
       ▼
2. Download from Google Drive (status: downloading)
   Google Docs/Sheets/Slides → export PDF automatique
   Autres formats → téléchargement direct
       │
       ▼
3. Upload to GCS (status: uploading)
   Path: {acteur_id}/{doc_id}/{filename}
   Bucket: NEODOC_TEMP_BUCKET
       │
       ▼
4. Import into Vertex AI Discovery Engine (status: importing)
   struct_data metadata: {
     customer_id, acteur_id, internal_id,
     type, ingestion_date, folder_path, shared
   }
       │
       ▼
5. Update DB (status: imported)
   Set doc_vertex_id (ID Discovery Engine)
       │
       ▼
6. Add to workspace
   Insert t_neodoc_workspace_document (N:N join)
       │
       ▼
7. Auto-select for uploader
   Insert t_neodoc_selection (sel_selected=True)
```

## Pipeline Upload direct (6 étapes)

Identique mais skip l'étape 2 (download Drive) — le fichier est déjà disponible.

## Modes d'exécution

| Mode | Usage | Implémentation |
|------|-------|---------------|
| **Sync** | Upload API (bloquant) | `await _run_pipeline()` |
| **Async** | Ingest Drive | `asyncio.create_task(_schedule_pipeline())` |
| **Batch** | Ingest multiple | `asyncio.gather()` avec `Semaphore(5)` |
| **Folder** | Ingest dossier Drive | Liste Drive → delegate batch |

## Retry intelligent

| Source | Comportement |
|--------|-------------|
| Drive | Re-download + pipeline complète |
| Upload | Réutilise le fichier GCS existant → re-import Discovery Engine |

Les fichiers GCS ne sont **jamais supprimés** — Discovery Engine crawle de façon asynchrone, le fichier doit rester disponible.

## Statuts d'ingestion

```
pending → downloading → uploading → importing → imported → indexed
                                                           ↓
                                                         error
```

Le statut `indexed` est vérifié via `GET /documents/{id}/index-status` qui interroge Discovery Engine en temps réel.

## Multi-tenant — Filtrage Vertex AI

Chaque document importé porte des metadata `struct_data` pour le filtrage :

```
(acteur_id: ANY("{acteur_id}") OR shared = "true") AND customer_id: ANY("{customer_id}")
```

Plus le filtre de sélection (documents actifs pour l'acteur dans le workspace) :
```
document_id: ANY("id1", "id2", ...)
```

## Export Google natifs → PDF

| Format Google | Export |
|--------------|--------|
| Google Docs | PDF |
| Google Sheets | PDF |
| Google Slides | PDF |
| Autres (PDF, DOCX, etc.) | Téléchargement direct |

Le `DriveService` gère la distinction via `mimeType` et `export_links`.

## Notes indexables

Les notes (manuelles ou sauvegardées depuis des réponses agent) peuvent être indexées dans Discovery Engine via `POST /notes/{id}/index` :
- Génère un titre automatique via Gemini Flash (≤80 chars)
- Importe le contenu dans le même data store que les documents
- La note devient retrouvable par le Research Agent

## Services impliqués

| Service | Fichier | Rôle |
|---------|---------|------|
| `IngestionService` | `services/ingestion_service.py` | Orchestration pipeline (7 modes) |
| `DriveService` | `services/drive_service.py` | Download + export Drive |
| `GCSService` | `services/gcs_service.py` | Upload/delete GCS |
| `SearchService` | `services/search_service.py` | Import/delete Discovery Engine |
| `NoteService` | `services/note_service.py` | Indexation notes + auto-titre |

## Liens

- [[neodoc-architecture]]
- [[neodoc-research-agent]]
