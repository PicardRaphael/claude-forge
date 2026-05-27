---
name: arxiv-id-yymm-mois-cite-doit-correspondre
description: "Format arXiv YYMM.NNNNN doit correspondre au mois cité dans la note vault. Audit RAG 23 mai a trouvé TOOLQP cité \"MIT janvier 2025\" alors qu'arXiv 2601.07782 = janvier 2026."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7960dab2-e6be-4b55-ba9e-1985dac06f32
---

Format arXiv IDs = **YYMM.NNNNN** (les 2 premiers chiffres = année 20YY, les 2 suivants = mois MM).

**Règle** : à chaque citation d'un paper arXiv avec mois/année explicite dans une note vault, vérifier mécaniquement que YYMM de l'ID correspond.

**Why** : Audit thématique RAG 23 mai 2026 a trouvé note vault citant *"TOOLQP (MIT, Janvier 2025)"* alors que arXiv 2601.07782 = soumis **12 janvier 2026**. Erreur de date Type 1 critique (1 an de décalage).

**How to apply** :
- Pendant audit thématique, scanner systématiquement `arXiv:YYMM` vs date citée dans la phrase
- Pendant création de note, vérifier l'ID avant de typer la date
- Pendant relecture, si paper "ancien" avec ID > 25 (donc 2025+) ou "récent" avec ID < 24 → red flag automatique

Lié : [[feedback_audit_thematique_methode]] [[feedback_verify_exhaustive_claims]]
