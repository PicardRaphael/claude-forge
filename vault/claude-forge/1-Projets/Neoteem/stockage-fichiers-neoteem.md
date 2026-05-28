---
titre: "Stockage fichiers Neoteem — pas de S3, Drive client + BDD JSON"
resume: "Neoteem n'utilise pas S3. Stockage fichiers = Drive client (via webservices Jérôme) ou BDD JSON pour données structurées. Pas de bucket object storage interne hors GCS NeoDoc"
aliases:
  - "stockage fichiers neoteem"
  - "pas de s3 neoteem"
  - "drive client neoteem"
  - "object storage neoteem"
  - "persistance pdf neoteem"
  - "bucket neoteem"
type: technique
derniere-maj: 2026-05-28
auteur: claude
tags:
  - "#type/technique"
  - "#projet/neoteem"
  - "#domaine/architecture"
---

## Contrainte

Neoteem **n'utilise pas S3** (ni MinIO, GCS interne, OVH Object Storage côté infra applicative). Exception : GCS utilisé en interne par NeoDoc pour ingestion documents (cf [[neodoc-architecture]]) — pas exposé aux autres features métier.

## Options de persistance pour features

1. **BDD en JSON structuré** — pour données requêtables (résultats d'agents, comparatifs, métadonnées). Léger, ré-affichable, historique consultable côté Neoteem.
2. **PDF / fichiers sur le Drive client** — via webservices Jérôme (voir [[webservices-jerome]]). Pas de trace côté Neoteem, le client a son fichier dans son Drive.
3. **Combo BDD JSON + Drive client** — données structurées en BDD pour UX (ré-affichage, recherche, historique), fichier final dans Drive client pour archivage client.

## Implications de conception

- Pour features qui génèrent un PDF / document final : **pas de "lien S3" possible**, l'archivage passe par le Drive client.
- Si besoin d'historique consultable côté Neoteem : **sérialiser en JSON BDD**, pas stocker le fichier binaire.
- Anti-pattern : stocker des binaires (PDF, images) en blob BDD — BDD lourde, backups longs, requêtes ralenties.
- Pour pré-régénérer un PDF à la demande (option 1 seule) : prévoir un service de rendu côté appelant.

## Questions à poser au PO sur toute feature avec fichier généré

- Le résultat est-il sauvegardé en BDD (JSON requêtable) ?
- Le PDF est-il systématiquement classé Drive client ou à la demande ?
- Rétention : combien de temps on garde ?
- Suppression manuelle possible (RGPD / droit à l'oubli) ? Qui peut supprimer, quel scope (BDD seulement, Drive aussi, les deux) ?

## Origine

Confirmé par Raphael session 28 mai 2026 lors de la rédaction du commentaire ticket comparatif devis.

## Liens

- [[archi-backs-neoteem]] — Contrats d'exposition front
- [[webservices-jerome]] — Canal d'écriture vers Drive client
- [[neodoc-architecture]] — Exception GCS pour ingestion NeoDoc
