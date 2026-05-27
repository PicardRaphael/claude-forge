---
name: x-articles-inaccessibles-confirmation-empirique
description: "Articles X (x.com/i/article/...) inaccessibles via tweets_by_ids, tweets_details ET WebFetch (HTTP 402). Aucun workaround API — user doit copy-paste manuellement."
metadata: 
  node_type: memory
  type: reference
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Confirmation empirique 26 mai 2026 du gotcha déjà documenté dans skill [[x-read]].

**Why** : tweet @sairahul1 id 2058832033628241931 ne contenait qu'un lien `x.com/i/article/2058805590043009024`. Trois méthodes testées toutes échouées :
- `scraper.tweets_by_ids([article_id])` → `{"tweetResult": [{}]}` (vide)
- `scraper.tweets_details([article_id])` → uniquement `TimelineClearCache` sans contenu
- `WebFetch` sur URL article → HTTP 402 (X Premium gated)

**How to apply** : quand un tweet pointe vers `x.com/i/article/...` :
1. Récupérer les métadonnées du tweet parent (auteur, stats, date) — OK via skill x-read
2. **Ne pas tenter** de fetch l'article — c'est documenté inaccessible
3. Demander à Raphael de copy-paste le texte depuis son compte X authentifié
4. JAMAIS paraphraser depuis stats/contexte seul (cf [[tweet-hype-paraphrase-non-verifiee-pattern]])
