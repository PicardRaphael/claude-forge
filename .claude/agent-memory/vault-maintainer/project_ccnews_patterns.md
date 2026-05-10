---
name: Patterns capitalisation cc-news vault
description: Patterns récurrents observés lors des sessions cc-news → vault (create vs append, cross-links, orphelins)
type: project
---

## Règle create vs append pour les notes existantes

Pour les concurrents (Cursor, xAI Grok, etc.) et les techniques (Context Engineering) : toujours `append_note` / `Edit` plutôt que créer une nouvelle note versionnée. Les notes concurrent/technique sont des profils évolutifs, pas des changelogs.

**Why:** Créer "Cursor-3-3.md" séparément fragmente le savoir ; une note profil unique avec sections datées est plus navigable.

**How to apply:** Chercher l'existant AVANT de créer. Si note de type `concurrent` ou `technique` existe → append la section datée (ex: "## Cursor 3.3 — Mai 2026").

## Backlinks jina-style : rag-embeddings pointe vers les nouvelles notes embedding

Quand une note atomique d'embedding est créée dans `04-Techniques/rag/`, la note `rag-embeddings.md` contient généralement déjà une mention en texte plat. Ajouter le wikilink `[[nom-note|Texte affiché]]` pour matérialiser le backlink.

**Why:** Évite les orphelins sur les notes techniques RAG.

**How to apply:** Après création d'une note RAG, Grep `rag-embeddings.md` pour la mention, remplacer par wikilink.

## Changelogs CC : cross-linking Précédent/Suivant

Chaque changelog doit référencer `[[CC v2.1.XXX]]` précédent ET suivant quand connus. La série forme une chaîne.

**Why:** Navigation séquentielle dans l'historique sans passer par le MOC.

**How to apply:** Créer d'abord les notes les plus anciennes (132 avant 133 avant 136), puis ajouter les liens bidirectionnels.
