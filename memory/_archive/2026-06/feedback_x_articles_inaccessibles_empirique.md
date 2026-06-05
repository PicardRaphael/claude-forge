---
name: x-articles-inaccessibles-confirmation-empirique
description: "Articles X (x.com/i/article/...) inaccessibles 3 méthodes — copy-paste manuel obligatoire"
metadata:
  type: reference
  originSessionId: a4e196c9-ffac-4668-a189-2e0902c13357
---

Cf skill [[x-read]] body — gotcha articles X gated documenté canoniquement.

**Confirmation empirique 26 mai 2026** : tweet @sairahul1 id 2058832033628241931 pointait vers `x.com/i/article/2058805590043009024`. 3 méthodes échouées :
- `scraper.tweets_by_ids([article_id])` → `{"tweetResult": [{}]}` vide
- `scraper.tweets_details([article_id])` → uniquement `TimelineClearCache`
- `WebFetch` → HTTP 402 (X Premium gated)

Action : récupérer metadata tweet parent uniquement, demander copy-paste manuel Raphael. JAMAIS paraphraser depuis stats seules (cf [[tweet-hype-paraphrase-non-verifiee-pattern]]).
