---
name: webfetch-avant-subagents-audit
description: "AVANT dispatch sub-agents audit thématique, faire 3-4 WebFetch directs sur sources primaires suspectes (arXiv IDs incohérents, verbatim \"magique\", chiffres trop précis). Kill fabrications en 3 min, évite que 6 sub-agents chassent des fantômes."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 418b4be9-67c5-4bec-8f69-17086a63bb06
---

Pattern validé audit prompt-engineering 23 mai 2026, advisor a fait gagner 30 min wall-time.

## Règle

Entre checkpoint A (inventaire claims) et phase B (sub-agents par cluster), insérer une **mini-phase A.5** : 3-4 WebFetch parallèles sur les sources primaires les plus suspectes de l'inventaire.

## Signaux de fabrication à fetch en priorité

- **arXiv IDs incohérents** : format = YYMM.NNNNN. Si "déc 2025" annoncé mais ID en 2601 = janvier 2026 → mismatch fort
- **Verbatim "magique"** : phrases trop punchy avec chiffres précis ("X for GPT-5.2 may be actively making GPT-5.5 worse") = pattern hallu LLM
- **Chiffres très précis non-standards** : "S*=0.509", "305 prompts, 11 modèles", "157 versions", "512K lignes TS" — vrais OU fabriqués, à vérifier
- **Auteurs/companies obscurs** liés à doctrines entières (12 principes attribués à 1 personne = single point of failure)
- **Verbatim attribués à docs officiels** (Anthropic, OpenAI) → WebFetch direct la page citée

## Pourquoi

Sub-agents en cluster = ~10 min chacun. Si 4 claims fabriquées au cœur d'un cluster, le sub-agent invente une vérif autour d'un fantôme (cherche sources tierces qui paraphrasent le mythe). Coût : 30-45 min wall-time + faux positifs réinjectés dans phase C.

## How to apply

1. Checkpoint A écrit (inventaire claims dédupliqué)
2. Identifier 3-6 claims "fort impact + signal fabrication" (cf grille ci-dessus)
3. WebFetch parallèles en UN message
4. Injecter résultats (✅ confirmé / ❌ fabriqué / ⚠️ titre faux concepts vrais) dans les briefs sub-agents AVANT dispatch
5. Sub-agents partent avec terrain déminé

## Exemple chiffré audit 23 mai

- 4 WebFetch / WebSearch en ~3 min
- Résultats : 1 paper confirmé canonique (UCL Mikinka), 1 titre forge faux mais concepts vrais (Sculpting Khan), 1 personne réelle mais produit non-public (Theo Haddad FORGE), 1 verbatim totalement fabriqué (OpenAI GPT-5.5 "patterns months perfecting")
- Gain : 6 sub-agents partis avec briefs corrigés, pas de hallu cascade

## Lien

[[feedback_audit_thematique_methode]] — méthode mère sub-agents par cluster
[[feedback_advisor_da_mandatory]] — advisor AVANT travail substantiel (ici phase B = travail substantiel)
