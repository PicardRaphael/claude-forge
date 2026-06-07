---
name: audit-completude-pointeur-vs-orphelin
description: Audit de complétude d'index/roadmap — un wikilink non résolu localement peut pointer vers une note existante ailleurs dans le vault. search_brain chaque cible AVANT de la compter comme orpheline, sinon surcompte du travail
metadata:
  type: feedback
---

Quand on audite la **complétude d'un index/hub/roadmap** (combien de cibles wikilink existent vs sont à créer), un lien `[[x]]` qui ne se résout PAS depuis le dossier courant n'est PAS forcément un orphelin : il peut pointer vers une note bien réelle ailleurs dans le vault (autre dossier, alias). Le compter comme « à créer » = **surcompter le backlog**.

**Cas observé 7 juin 2026** : backlog roadmap casquette `responsable-ia`. Le hub `technique-ia/index` cite ~60 wikilinks RAG/agents/prompt-engineering qui semblent orphelins depuis la casquette, mais pointent vers des notes existantes dans `04-Techniques/` (pointeurs valides, pas des trous). Compte brut ≈ 60-70 « orphelins » → compte réel après vérif = **41**. L'écart de 20-30 venait de ces pointeurs cross-dossier pris à tort pour des trous.

**Why** : confondre « pointeur cross-dossier valide » et « cible manquante » gonfle le périmètre de travail annoncé à Raphael (faux 52-70 au lieu de 41 réels). C'est le pendant inverse de [[verify-exhaustive-claims]] (grep avant « zéro/tous ») et de [[lire-fichier-entier-avant-verdict]] (lire avant « supprimer ») : ici c'est avant de déclarer « manquant/orphelin/à créer ».

**How to apply** :
1. Lister les wikilinks atomiques cités dans l'index audité.
2. Soustraire les notes du dossier courant (`list_notes`).
3. Pour CHAQUE cible restante ambiguë → `mcp__forge-brain__search_brain(cible)`. Si le seul résultat est le hub qui la cite → vrai orphelin. Si une note réelle apparaît (autre dossier) → **pointeur valide, hors backlog**.
4. Exclure d'emblée les hubs explicitement « carte d'orientation / pointe vers l'existant » (ex `technique-ia`) et les cheat-sheets « tout inline » (ex `frameworks`, `templates`, `tickets`).

Distinct de l'orphelin-graphe (note sans backlink) et du lien cassé au lint — ici la note CIBLE existe, c'est le contexte de lecture qui crée la fausse impression de trou.
