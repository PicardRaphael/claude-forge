---
name: da-dicte-tests-adverses-pas-moi
description: "Sur livrable code avec rewriting/destructif, mes tests passent souvent sans couvrir les cas adverses. DA verbalise les trous (silent data loss). Ses tests manquants deviennent ma checklist obligatoire avant push"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3751b01a-33d9-4962-b652-428c951e42d4
---

## Pattern

Quand j'implémente une fonction qui réécrit ou supprime des données (move_note, delete_note, refactor mass-fix), je tends à :
1. Écrire les tests sur les cas que j'ai prévus
2. Voir 100% pass
3. Conclure "safe to ship"

**Le piège** : mes cas prévus = mes assumptions. Les cas adverses (silent data loss) sont par définition ceux que je n'ai pas pensé à tester.

## Cas concret 24 mai 2026 — MCP forge-brain move_note

Première implémentation : 22/22 tests pass. Regex `r"\[\[" + re.escape(old_stem) + r"(?=[\]|#])"` correctement construit pour les 4 variantes annoncées : `[[stem]]`, `[[stem|alias]]`, `[[stem#section]]`, `[[stem|alias#section]]`.

DA review a identifié 4 trous SILENCIEUX :
1. **Embed `![[stem]]`** : matché par hasard mais aucun test
2. **Self-link** : la note déplacée contient `[[old-stem]]` → boucle skippait `bl_path == normalized_new` → self-link cassé
3. **Case-insensitive** : `[[Alpha]]` ne match pas target `alpha` (Obsidian résout case-insensitive, ma DB stockait verbatim)
4. **Code blocks** : `` `[[stem]]` `` réécrit alors que contenu littéral

Tous **silent data loss**. Aucun test ne les couvrait. Tous fixés par DA + tests adverses dictés.

## Why

Sub-agent DA voit le code avec un mindset "qu'est-ce qui casse ?". Moi je vois avec mindset "ça marche ?". Asymétrie cognitive utile.

Pattern qui revient :
- `feedback_tests_adverses_obligatoires` — hooks sécu : tester les bypass
- `feedback_claim_security_must_be_provable` — "by construction" ≠ "by discipline"
- `feedback_audit_claims_after_brief` — vérifier empiriquement les claims de sub-agents

Ici c'est l'inverse : mes propres claims sécurité ("we match ONLY exact old_stem") étaient vraies pour les 4 cas annoncés mais fausses pour 4 cas non couverts.

## How to apply

**Sur tout livrable qui réécrit/supprime/modifie en masse** :

1. Écrire impl + tests "happy path"
2. Lancer pytest, vérifier pass
3. **AVANT push** : appeler DA avec le code + les claims sécurité
4. Le DA renvoie liste de tests adverses manquants
5. Ajouter ces tests (le code adverse échouera typiquement)
6. Fixer le code jusqu'à ce que les tests adverses passent aussi
7. Commit + push

**Ne PAS** :
- Sauter l'étape DA si "ça marche localement"
- Écrire mes propres tests adverses sans DA — je rate les angles morts par construction
- Considérer 22/22 pass comme preuve de safety. Les tests prouvent ce qu'ils testent.

## Liens

- [[feedback_tests_adverses_obligatoires]]
- [[feedback_claim_security_must_be_provable]]
- Knowledge/critiques/critique-2026-05-24-mcp-move-note-4-trous-silent (à créer si capitalisé)
