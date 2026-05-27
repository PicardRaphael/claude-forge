---
name: audit-thematique-methode-sub-agents-clusters
description: "Méthode validée audit thématique vault — sub-agents parallèles par CLUSTER de claims (pas par note), 6 clusters, checkpoint write A-inventaire AVANT lancer B. Self-verify les FAUX à fort impact avant phase D."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 931783ff-d35c-4d9c-b53d-c30bcf6f294f
---

Audit thématique vault forge-brain 23 mai 2026 — 95 claims, 6 sub-agents parallèles, 4 commits poussés. Méthode qui a marché.

## Pattern qui marche

**1. Lecture parallèle SANS sub-agents** : read_note des 12 notes en parallèle depuis session principale = 1 message. Déduplique claims globalement. Sub-agents par note = 10 formats différents + claims dupliquées (Sonnet/Opus split apparaît dans 4 notes → vérifié 4×).

**2. Clusters thématiques pour phase B** : 6 sub-agents par CLUSTER de claims (verbatim Boris / CwC speakers / Anthropic docs / Karpathy / Fowler-Osmani / repos+Willison). Chaque sub-agent reçoit (a) claims verbatim, (b) URLs candidates pré-identifiées, (c) format de sortie imposé. Sans (b)+(c) tu reçois 10 rapports incohérents.

**3. Checkpoint write OBLIGATOIRE** : sauvegarder `A-inventaire-claims.md` AVANT lancer B. Si la session crashe pendant les sub-agents (~5-10 min chacun), tu repars de l'inventaire.

**4. Self-verify les FAUX à fort impact AVANT phase D** : les sub-agents se trompent (cf [[feedback_auditor_false_positives]]). Sur cet audit : 4 fondations à re-vérifier directement (Justin Young split, Brad Abrams advisor, 9 catégories Thariq, "Claude decides when to parallelize"). Sur les 4 : 1 confirmé faux, 1 confirmé vrai, 1 concept valide mais source à corriger, 1 principe canonique mais formule paraphrasée. Si tu ne self-verify pas, tu réécris des fondations correctes sur la foi de sub-agents qui ont parsé trop vite.

**5. Distinguer 3 types d'erreur** :
- Type 1 : citation/date/attribution fausse, principe juste → corriger source, garder concept
- Type 2 : chiffre inventé → remplacer par qualitatif ou retirer
- Type 3 : doctrine fausse au fond → réécrire section

Les sub-agents mettent tout en "FAUX" sans distinguer. Toi tu dois.

## Pourquoi

Validé sur audit Claude Code 23 mai (95 claims, 6 clusters, 4 vérifs directes, ~30 min wall-time). **Reconfirmé audit Agents IA 23 mai** : 130 claims, **8 clusters** (scale OK), 7 self-verify directs, 18 notes corrigées sans régression. Sans clusters, ça aurait été 26 sub-agents en série = >6h.

Le scaling 6 → 8 clusters fonctionne tant que chaque cluster reste thématiquement cohérent. Au-delà de ~10 clusters, le coût de coordination devient supérieur au gain de parallélisme.

## Scaling observé

| Audit | # notes | # claims | # clusters | Wall-time |
|-------|---------|----------|------------|-----------|
| Claude Code (22 mai) | 12 | 95 | 6 | ~30 min |
| Agents IA (23 mai) | 26 | 130 | 8 | ~25 min (parallèle + self-verify) |

Conclusion : **8 clusters supporte 2× le volume de notes avec un wall-time stable**, à condition que les claims se déduplient bien entre notes (le MOC + notes spécialisées tendent à répéter les mêmes claims fondamentales).

## How to apply

Pour tout audit thématique vault (les 6 autres prompts à venir : prompt-engineering, RAG, agents-ia, fine-tuning, patterns-context, leaders-modeles-industrie) :
1. Lecture parallèle des notes du thème (session principale, multi-read_note 1 message)
2. Inventaire claims A → checkpoint write
3. 5-7 sub-agents par cluster thématique avec brief structuré
4. Croisement C → identifier FAUX à fort impact
5. Self-verify direct (WebFetch + WebSearch) les fondations avant phase D
6. Distinguer Type 1/2/3 dans plan correction
7. Validation Raphael par vagues (safe → vérifs → réécritures structurelles)
