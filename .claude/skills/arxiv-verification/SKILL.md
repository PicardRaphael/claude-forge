---
name: arxiv-verification
description: ALWAYS verify arXiv papers before citing : YYMM format must match cited month, URL must not be swapped between similar papers, venues NeurIPS/ICLR must be verified (often falsely attributed to arXiv-only papers).
allowed-tools: WebFetch
user-invocable: true
effort: high
---

## Rôle

Vérifier la validité d'une citation arXiv avant de la capitaliser dans le vault ou de la présenter à l'utilisateur. Trois vecteurs d'erreur distincts.

## Étapes

### Check 1 — Format YYMM vs mois cité

Le format arXiv `YYMM.XXXXX` encode l'année et le mois de soumission :
- `2601.07782` → janvier 2026 (26 = 2026, 01 = janvier)
- `2410.21228` → octobre 2024

**Vérifier** : si la note cite "paper X, mars 2025" mais l'ID est `2502.XXXXX` → incohérence, recalibrer le mois cité.

### Check 2 — URL swap entre papers similaires

Quand N papers du même domaine sont cités ensemble (ex: tool retrieval, RAG, agents), les URLs peuvent être swapées entre fiches.

**Vérifier** : WebFetch de l'URL arXiv, confirmer que le titre affiché correspond au paper cité dans la note.

```
WebFetch("https://arxiv.org/abs/YYMM.XXXXX")
→ lire le titre H1 et vérifier correspondance
```

### Check 3 — Venues NeurIPS/ICLR/EMNLP/ACL

Un paper arXiv peut affirmer "soumis à NeurIPS 2025" dans l'abstract sans y être accepté. La venue confirmée est dans le PDF ou openreview.

**Vérifier** : si la note affirme "Paper X — NeurIPS 2025", WebFetch du PDF ou openreview.net avant validation.

- Abstract arXiv insuffisant
- Si incertain : écrire `arXiv YYMM.XXXXX, [mois année], venue non confirmée`

## Gotchas

- **Abstract arXiv ≠ venue confirmée** — les venues n'y sont pas listées systématiquement.
- **Pattern N papers même domaine** — probabilité swap élevée. WebFetch systématique si ≥ 2 papers similaires traités en même temps.
- **Brief sub-agents auditeurs** — inclure explicitement : "vérifier venues par WebFetch PDF, pas seulement abstract".
- **YYMM ≠ date de publication** — c'est la date de soumission arXiv, pas la date de conférence.

## Apprentissage

Patterns observés :
- TOOLQP cité "ICLR 2025" → FAUX (arXiv jan 2026, aucune venue ICLR)
- "Intruder dimensions LoRA — NeurIPS 2025" → FAUX (arXiv 2410.21228, aucune venue dans abstract)
- MCP-Zero ↔ OATS swap trouvé dans `tool-retrieval-query-expansion.md`
- JudgeBench "ICLR 2025" → CONFIRMÉ via WebFetch PDF

Capitaliser les nouveaux faux positifs/négatifs découverts ici en append.
