---
name: venues-conference-inventees-llm-pattern
description: "Pattern récurrent vault — venues conférence (NeurIPS, ICLR) attribuées à des papers arXiv sans preuve. Toujours vérifier dans PDF, pas seulement abstract."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9d187182-be69-4f77-822a-84b8ce7a1e5c
---

**Règle** : Une note vault qui affirme "Paper X — NeurIPS 2025" ou "ICLR 2025" SANS lien direct vers la venue (openreview / proceedings) doit être traitée comme suspecte. La venue se vérifie dans le PDF complet du paper, pas dans l'abstract arXiv.

**Why** : Pattern récurrent confirmé en 2 audits successifs (23 mai 2026) :
- Audit RAG : TOOLQP cité "ICLR 2025" → FAUX (paper arXiv jan 2026, pas de venue ICLR)
- Audit fine-tuning : "Intruder dimensions LoRA — NeurIPS 2025" → FAUX (Shuttleworth et al MIT, arXiv 2410.21228, aucune venue dans abstract)
- À l'inverse : JudgeBench cité "ICLR 2025" → CONFIRMÉ via WebFetch du PDF
→ Le pattern n'est pas systématique, mais le risque suffit à exiger WebFetch direct

**How to apply** :
- Audit thématique vault : tout claim "X — NeurIPS/ICLR/EMNLP/ACL 20XX" nécessite WebFetch PDF ou openreview avant validation
- Abstract arXiv ne suffit pas : les venues n'y sont pas toujours listées
- À l'écriture d'une note tech : si je ne suis pas certain de la venue, écrire "arXiv YYMM.XXXXX, [mois année], venue non confirmée"
- Brief sub-agents auditeurs : "vérifier venues par WebFetch PDF, pas seulement abstract"

**Sister rules** : [[arxiv-id-yymm-format]], [[arxiv-url-swap-papers-similaires]], [[tweet-hype-paraphrase-non-verifiee-pattern]]
