---
name: arxiv-verification
description: 'ALWAYS verify arXiv papers before citing : YYMM format must match cited month, URL must not be swapped between similar papers, venues NeurIPS/ICLR must be verified (often falsely attributed to arXiv-only papers).'
allowed-tools: WebFetch
user-invocable: true
effort: high
---

## RÃ´le

VÃ©rifier la validitÃ© d'une citation arXiv avant de la capitaliser dans le vault ou de la prÃ©senter Ã  l'utilisateur. Trois vecteurs d'erreur distincts.

## Ã‰tapes

### Check 1 â€” Format YYMM vs mois citÃ©

Le format arXiv `YYMM.XXXXX` encode l'annÃ©e et le mois de soumission :
- `2601.07782` â†’ janvier 2026 (26 = 2026, 01 = janvier)
- `2410.21228` â†’ octobre 2024

**VÃ©rifier** : si la note cite "paper X, mars 2025" mais l'ID est `2502.XXXXX` â†’ incohÃ©rence, recalibrer le mois citÃ©.

### Check 2 â€” URL swap entre papers similaires

Quand N papers du mÃªme domaine sont citÃ©s ensemble (ex: tool retrieval, RAG, agents), les URLs peuvent Ãªtre swapÃ©es entre fiches.

**VÃ©rifier** : WebFetch de l'URL arXiv, confirmer que le titre affichÃ© correspond au paper citÃ© dans la note.

```
WebFetch("https://arxiv.org/abs/YYMM.XXXXX")
â†’ lire le titre H1 et vÃ©rifier correspondance
```

### Check 3 â€” Venues NeurIPS/ICLR/EMNLP/ACL

Un paper arXiv peut affirmer "soumis Ã  NeurIPS 2025" dans l'abstract sans y Ãªtre acceptÃ©. La venue confirmÃ©e est dans le PDF ou openreview.

**VÃ©rifier** : si la note affirme "Paper X â€” NeurIPS 2025", WebFetch du PDF ou openreview.net avant validation.

- Abstract arXiv insuffisant
- Si incertain : Ã©crire `arXiv YYMM.XXXXX, [mois annÃ©e], venue non confirmÃ©e`

## Gotchas

- **Abstract arXiv â‰  venue confirmÃ©e** â€” les venues n'y sont pas listÃ©es systÃ©matiquement.
- **Pattern N papers mÃªme domaine** â€” probabilitÃ© swap Ã©levÃ©e. WebFetch systÃ©matique si â‰¥ 2 papers similaires traitÃ©s en mÃªme temps.
- **Brief sub-agents auditeurs** â€” inclure explicitement : "vÃ©rifier venues par WebFetch PDF, pas seulement abstract".
- **YYMM â‰  date de publication** â€” c'est la date de soumission arXiv, pas la date de confÃ©rence.

## Apprentissage

Patterns observÃ©s :
- TOOLQP citÃ© "ICLR 2025" â†’ FAUX (arXiv jan 2026, aucune venue ICLR)
- "Intruder dimensions LoRA â€” NeurIPS 2025" â†’ FAUX (arXiv 2410.21228, aucune venue dans abstract)
- MCP-Zero â†” OATS swap trouvÃ© dans `tool-retrieval-query-expansion.md`
- JudgeBench "ICLR 2025" â†’ CONFIRMÃ‰ via WebFetch PDF

Capitaliser les nouveaux faux positifs/nÃ©gatifs dÃ©couverts ici en append.
