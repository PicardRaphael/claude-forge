---
titre: "Jonas Roman"
resume: "Expert RAG français, ex-Mistral AI, fondateur Lagentia.fr, chaîne YouTube AI Ops (ex-IA en Prod)"
aliases:
  - Jonas Roman
  - AI Ops
  - IA en Prod
  - Lagentia
  - Jonas Roman RAG
  - "expert RAG production FR"
  - "IA en production"
  - "RAG francophone"
role: "Fondateur Lagentia.fr, AI Engineer"
affiliation: "Lagentia (ex-Mistral AI)"
derniere-maj: 2026-06-05
auteur: claude
sources:
  - "https://www.youtube.com/@JonasRoman-t5t"
  - "https://lagentia.fr"
tags:
  - "#type/leader"
  - "#domaine/ia"
  - "#domaine/rag"
type: ""
---
## Profil

Expert IA générative français, fondateur de Lagentia.fr (agence IA pour ETI : audit stratégique → mise en production). Anciennement AI Engineer chez **Mistral AI** avec des clients comme BNPP, Ministère des Armées, CNAMTS, INRIA, SNCF, Orange.

Chaîne YouTube **"Jonas Roman | AI Ops"** (ex-"IA en Prod"). Communauté Skool "AI Ops | The 93% Club".

## Contributions clés

### Approche pragmatique du RAG
- **"Données Internes = RAG" est un réflexe coûteux** — challenge l'utilisation systématique du RAG quand des solutions plus simples existent
- **Human-in-the-loop** essentiel : "Si un humain valide les outputs, c'est OK si c'est faux 20% du temps, les 80% d'économies comptent"
- Focus sur **fiabilité et ROI** plutôt que bleeding-edge tech
- Production-oriented : pas de tutoriels académiques, des leçons de déploiement réel

### Vidéos RAG notables
- [Comment rendre vos RAG fiables et puissants facilement !](https://www.youtube.com/watch?v=keiw3AEfJAQ) (mai 2025)
- [RAG : La Méthode Que 99% des Tutos ne Montrent Pas](https://www.youtube.com/watch?v=P8UWNj7kFxQ) (nov 2025)
- [RAG : Les leçons que personne ne partage](https://www.youtube.com/watch?v=tGiCvd9I80U) (2026)
- ["Données Internes = RAG" — Pourquoi Ce Réflexe Coûte Très Cher !](https://www.youtube.com/watch?v=HYsIHWVngzE) (fév 2026)

## Positions récentes

- Le RAG en production est un problème d'**ingénierie**, pas de recherche
- Les ETI françaises sous-estiment le coût de maintenance d'un pipeline RAG
- Prône des solutions **simples et mesurables** avant d'ajouter de la complexité

## Liens

- [[MOC-Leaders]]
- YouTube : [youtube.com/@JonasRoman-t5t](https://www.youtube.com/@JonasRoman-t5t)
- Communauté : skool.com/ia-en-prod
- Agence : [lagentia.fr](https://lagentia.fr)
- [[RAG]] — Index RAG


## ZParse — son outil d'ingestion RAG (souveraineté EU)

**[ZParse](https://zparse.io)** est l'outil d'ingestion RAG créé/promu par Jonas Roman, désormais pièce maîtresse de son stack. Positionnement : *"Made in France, hosted in Europe"*, ISO 27001 en cours — réponse directe aux enjeux RGPD/souveraineté.

- **ETL pour données IA-ready** : parse PDF scannés, Excel, XML, JSON, Markdown, Parquet, CSV ; connecteurs SharePoint/GDrive/S3/SFTP ; livre vers Qdrant/Weaviate/Pinecone/pgvector/Elasticsearch.
- **LLM-agnostic** : Mistral (souveraineté), OpenAI (perf), Claude (reasoning), Llama local (air-gap) — no lock-in, no data retention (data en transit only).
- **Observabilité chunk-par-chunk** : chaque étape tracée, loggée, rejouable (data trails) + versioning/rollback. Argument anti-pipeline-Python-fragile.
- Tarifs (juin 2026) : Free €0 / Builder €29 / Builder+ €89 par mois.

Voir [[rag-architecture#RAG souverain EU]] pour le contexte souveraineté complet.

## Méthodologie RAG production (synthèse vidéos 2026)

Cf [[rag-obsidian-claude-video-analyse]] (analyse d'une autre vidéo) et ses 2 vidéos de mai 2026 :
- **["200k€ de projets RAG : mon pipeline d'ingestion exposé"](https://www.youtube.com/watch?v=phZ_iqu1gN0)** (20 mai 2026) — pipeline d'ingestion A→Z : Mistral OCR → chunking sémantique (fenêtre page, group=1 + overlap ±1 page) → enrichissement métadonnée + **scoring de pertinence par chunk** → filtre seuil → markdown structuré. Cf [[rag-chunking#Scoring de pertinence à l'ingestion (write-time)]].
- **["Comment faire un vrai système de connaissance pour l'IA"](https://www.youtube.com/watch?v=yEmVTVTjzag)** (31 mai 2026) — push des chunks dans **Supabase + pgvector** (embeddings OpenAI text-embedding-3-large 3072d), filtrage SQL par catégorie pour garder la précision au scale.

Doctrine constante : **le bottleneck d'un RAG est l'ingestion (write-time), pas le modèle ni le prompt.** Toute la complexité en write-time, simplicité en query-time. Démarche : Golden Dataset (15-50 Q/R, 3 niveaux, construit AVEC le client) → audit data avant retrieval → config de base (chunking + embedding hybride + reranker) → éval **Précision / Recall / Faithfulness**. Note : *"savoir quand NE PAS faire de RAG"*.

> Note stack : VectorShift + Voiceflow (vidéo mai 2025) ont été remplacés par ZParse + Supabase/pgvector dans son stack récent (mai 2026).
