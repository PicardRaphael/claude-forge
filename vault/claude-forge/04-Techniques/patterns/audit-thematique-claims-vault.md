---
titre: "Audit thématique claims vault — méthode clusters + self-verify"
resume: "Méthode validée pour auditer les claims factuelles d'un corpus vault : lecture parallèle session principale, clusters thématiques de sub-agents, checkpoint avant phase B, self-verify des faux à fort impact, distinction Type 1/2/3."
aliases:
  - audit thématique claims vault
  - audit-thematique-clusters
  - methode-audit-claims-vault
  - feedback_audit_thematique_methode
  - audit claims sub-agents parallèles
type: technique
derniere-maj: 2026-07-07
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/vault"
  - "#pattern/audit"
  - "#pattern/sub-agents"
---

## Contexte

Méthode validée lors des audits thématiques vault du 23 mai 2026 : 95 claims / 12 notes (Claude Code) puis 130 claims / 26 notes (Agents IA). Distinct de [[audit-puis-vagues-paralleles]] qui cible l'audit de `.claude/` (fichiers de config) et non la vérification factuelle de claims dans des notes de connaissance.

## Pattern en 5 étapes

### 1. Lecture parallèle SANS sub-agents (session principale)

`read_note` de toutes les notes du thème en 1 message → inventaire global des claims. Déduplique les claims répétées entre notes (ex. le split Sonnet/Opus apparaissant dans 4 notes = 1 seule vérification, pas 4). Sub-agents par note = formats incohérents + claims vérifiées N fois.

### 2. Clusters thématiques pour phase B

5–8 sub-agents en parallèle, 1 par **cluster de claims** (pas 1 par note). Chaque sub-agent reçoit :
- (a) claims verbatim du cluster
- (b) URLs candidates pré-identifiées
- (c) format de sortie imposé (VRAI / FAUX / PARTIEL + justification)

Sans (b)+(c) : 10 rapports incohérents impossibles à croiser.

Exemples de clusters : verbatim speakers / docs Anthropic / papers arXiv / chiffres marché / frameworks / bugs GitHub / doctrines forge / attributions leaders.

### 3. Checkpoint write OBLIGATOIRE avant phase B

Sauvegarder `A-inventaire-claims.md` AVANT de lancer les sub-agents. Si la session crashe pendant les sub-agents (~5–10 min chacun), on repart de l'inventaire sans refaire la lecture parallèle.

### 4. Self-verify les FAUX à fort impact AVANT phase D

Les sub-agents parsent trop vite et se trompent. Sur l'audit Claude Code : 4 fondations re-vérifiées directement (Justin Young split, Brad Abrams advisor, 9 catégories Thariq, formule "Claude decides when to parallelize") → 1 confirmé faux, 1 vrai, 1 source à corriger, 1 paraphrase légitime. Sans self-verify, on réécrit des fondations correctes.

### 5. Distinguer 3 types d'erreur dans le plan de correction

| Type | Nature | Action |
|------|--------|--------|
| **Type 1** | Citation / date / attribution fausse, principe juste | Corriger la source, garder le concept |
| **Type 2** | Chiffre inventé ou non sourcé | Remplacer par qualitatif ou retirer |
| **Type 3** | Doctrine fausse au fond | Réécrire la section |

Les sub-agents mettent tout en "FAUX" sans distinguer — la session principale arbitre.

## How to apply (7 étapes)

1. Lecture parallèle des notes du thème (session principale, multi-`read_note` en 1 message)
2. Inventaire claims A → checkpoint write (`A-inventaire-claims.md`)
3. 5–8 sub-agents parallèles par cluster thématique avec brief structuré (claims + URLs + format)
4. Croisement C → identifier les FAUX à fort impact
5. Self-verify direct (WebFetch + WebSearch) sur les fondations avant phase D
6. Distinguer Type 1/2/3 dans le plan de correction
7. Validation Raphael par vagues : safe → vérifs → réécritures structurelles

## Scaling observé

| Audit | # notes | # claims | # clusters | Wall-time |
|-------|---------|----------|------------|-----------|
| Claude Code (22 mai) | 12 | 95 | 6 | ~30 min |
| Agents IA (23 mai) | 26 | 130 | 8 | ~25 min (parallèle + self-verify) |

8 clusters supporte 2× le volume de notes avec wall-time stable, à condition que les claims se dédupliquent bien. Au-delà de **~10 clusters**, le coût de coordination dépasse le gain de parallélisme.

## Liens

- [[agents-ia-22-claims-fausses-2026-05-23]] — audit Agents IA : méthode appliquée sur 130 claims / 8 clusters
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — audit Claude Code : 95 claims / 6 clusters, 22 erreurs corrigées
- [[audit-puis-vagues-paralleles]] — pattern soeur pour l'audit `.claude/` (config, pas claims)
- [[methode-analyser-repo]] — séquence A→B→C→D→E (macro-méthode analyse repo)
- [[feedback_auditor_false_positives]] — les sub-agents se trompent : toujours self-verify
- `.claude/rules/sequence-canonique-modification.md` — anti-pattern `search_brain` seul ≠ audit (read_note entier requis)
