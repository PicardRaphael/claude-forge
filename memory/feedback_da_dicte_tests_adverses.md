---
name: da-dicte-tests-adverses-pas-moi
description: "Sur livrable code avec rewriting/destructif, mes tests passent souvent sans couvrir les cas adverses. DA verbalise les trous (silent data loss). Ses tests manquants deviennent ma checklist obligatoire avant push"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3751b01a-33d9-4962-b652-428c951e42d4
---

Cf [[erreur-tests-heureux-vs-adverses]] (doctrine : tests "happy path" PASS ≠ validation sécurité ; pour tout livrable réécriture/suppression/enforcement, lister les cas adverses et lancer le DA AVANT push, pas après).

## Cas empirique(s) :

- **2026-05-24 — MCP forge-brain `move_note`** : première implémentation à **22/22 tests pass**. Regex `r"\[\[" + re.escape(old_stem) + r"(?=[\]|#])"` correctement construit pour les 4 variantes annoncées : `[[stem]]`, `[[stem|alias]]`, `[[stem#section]]`, `[[stem|alias#section]]`. Le DA a identifié **4 trous SILENCIEUX** non couverts (tous silent data loss, tous fixés par tests adverses dictés) :
  1. **Embed `![[stem]]`** : matché par hasard mais aucun test.
  2. **Self-link** : la note déplacée contient `[[old-stem]]` → boucle skippait `bl_path == normalized_new` → self-link cassé.
  3. **Case-insensitive** : `[[Alpha]]` ne match pas target `alpha` (Obsidian résout case-insensitive, ma DB stockait verbatim).
  4. **Code blocks** : `` `[[stem]]` `` réécrit alors que contenu littéral.
- Claim sécurité incident-spécifique : mes propres claims ("we match ONLY exact old_stem") étaient vraies pour les 4 cas annoncés mais fausses pour 4 cas non couverts.

## Liens

- [[tests-adverses-hooks-secu]]
- [[feedback_claim_security_must_be_provable]]
- Knowledge/critiques/critique-2026-05-24-mcp-move-note-4-trous-silent (à créer si capitalisé)
