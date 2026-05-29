---
name: audit-thematique-clusters
description: Use when auditing forge or any .claude/ setup across multiple themes (skills/agents/hooks/rules/CLAUDE.md). Dispatch repo-inspector (mode=audit) or specialized sub-agents PER CLUSTER (not all at once), checkpoint A before B, self-verify before declaring done.
allowed-tools: Read, Grep, Glob, Bash, mcp__forge-brain__read_note, mcp__forge-brain__search_brain
model: sonnet
effort: high
---

# Audit thématique — dispatch par clusters

Pattern validé sur audits vault Claude Code (95 claims, 6 clusters, ~30 min) et Agents IA (130 claims, 8 clusters, ~25 min). **Un seul auditeur sur 60+ composants tronque et perd des détails.**

---

## Pattern cluster vs composant-par-composant

| Approche | Problème |
|----------|----------|
| 1 auditeur tout-en-un | Tronque, dilue, perd cohérence sur 60+ composants |
| 1 sous-agent par note/composant | 10+ formats hétérogènes, claims dupliquées vérifiées N× |
| **Clusters thématiques** ✅ | Cohérence interne, déduplication globale, scaling 6→8 clusters stable |

---

## Workflow 7 phases

### Phase A — Lecture parallèle SANS sous-agents

**Depuis la session principale**, lire en parallèle TOUS les composants du périmètre (multi `Read`/`mcp__forge-brain__read_note` en 1 message). Déduplication globale des claims.

Objectif : inventaire des claims sans biais de sous-agent.

### Checkpoint write OBLIGATOIRE après Phase A

Sauvegarder `A-inventaire-claims.md` AVANT de lancer les sous-agents. Si la session crashe pendant les ~5-10 min/sous-agent, le redémarrage repart de l'inventaire.

```
output/audit-<theme>/A-inventaire-claims.md
```

### Phase B — Dispatch clusters thématiques

**5-8 sous-agents `repo-inspector` (mode=audit) en parallèle**, un par cluster. Chaque sous-agent reçoit :
1. La liste verbatim des claims de son cluster
2. Les URLs / sources candidates pré-identifiées
3. Format de sortie imposé (FAUX/VRAI/PARTIEL + justification)

Sans (b)+(c), on reçoit 10 rapports incohérents.

Exemples de clusters pour audit `.claude/` :
- Agents (frontmatter, body, skills: injection)
- Skills (taille, description, gotchas, apprentissage)
- Hooks (scope, règle lint/sécu/workflow, settings.json)
- Rules (frontmatter description:, routing, doublons)
- CLAUDE.md (taille, structure, 5 lignes Karpathy, séquence canonique)
- Transverse (cohérence cross-composants, références brisées)

### Phase C — Croisement résultats

Identifier les FAUX à fort impact. **Distinguer 3 types d'erreur** :
- Type 1 : citation/date/attribution fausse, principe juste → corriger source, garder concept
- Type 2 : chiffre inventé → remplacer par qualitatif ou retirer
- Type 3 : doctrine fausse au fond → réécrire section

Les sous-agents mettent tout en "FAUX" sans distinguer. La session principale tranche.

### Phase D — Self-verify les FAUX à fort impact

**AVANT de corriger**, vérifier directement les fondations les plus critiques (WebFetch, grep, lecture directe). Les sous-agents se trompent — sur un audit de 130 claims : 1/4 fondations re-vérifiées était un faux positif.

Ne jamais réécrire des fondations correctes sur foi d'un sous-agent qui a parsé trop vite.

### Phase E — Plan correction par type

Plan priorisé Type 1 → 2 → 3. Présenter à Raphael par vagues :
- Vague 1 : corrections sûres (Type 1)
- Vague 2 : vérifications (Type 2)
- Vague 3 : réécritures structurelles (Type 3)

### Phase F — Application

3 vagues parallèles max. Vérification empirique entre chaque vague.

### Phase G — Validation

Test comportemental (session fraîche ou prompt test PASS/FAIL) avant de déclarer "terminé".

---

## Mode tripartite — 3 lentilles doctrinales

**QUAND** : déclenché si l'utilisateur demande un audit "à fond / complet / sous tous les angles / 3 lentilles / tripartite", ou "mon setup .claude est-il bon / optimise ma config". Routé par `.claude/rules/comportement-proactif.md`. Distinct du mode clusters par défaut (7 phases ci-dessus).

**QUOI** : au lieu de clusters thématiques, dispatcher 3 agents auditeurs spécialisés EN PARALLÈLE depuis la session principale (1 message, 3 `Agent` calls) :

- `boris-auditor` — lentille conformité workflow Boris (score 7/7 : CLAUDE.md, compounding, /clear, verify, split, Karpathy, délégation)
- `ecc-auditor` — lentille sous-dimensionnement ECC (ADD list : agents/skills manquants ; rappel : seuils ECC = référence externe, PAS cible forge)
- `will-auditor` — lentille anti-empilement Will (FUSION/DELETE/REPLACE-BY-SKILL : ce qui est en trop)

**ORCHESTRATION** :

1. Session principale lance les 3 agents en 1 message (parallèle)
2. Attend leurs 3 rapports
3. SYNTHÉTISE les verdicts et ARBITRE les contradictions : si ECC dit "ajoute X" et Will dit "retire X", la session tranche selon la canonique forge anti-bloat
4. Les 3 auditeurs ne communiquent PAS entre eux (pas de SendMessage — anti-réentrance)

**ARBITRAGE des contradictions de seuils** : la canonique vault fait foi sur forge (CLAUDE.md <200L, skills <500L, anti-bloat). Les seuils ECC (119-181) sont une comparaison externe, jamais une cible forge.

**COÛT** : 3 agents Opus en parallèle. Réservé aux audits approfondis explicitement demandés — un "audite" nu va à `repo-inspector` mode=audit (mode clusters seul).

---

## Scaling

| Audit | # composants | # clusters | Wall-time |
|-------|-------------|------------|-----------|
| Claude Code vault | 12 notes / 95 claims | 6 | ~30 min |
| Agents IA vault | 26 notes / 130 claims | 8 | ~25 min |
| .claude/ repo standard | 60-80 composants | 4-5 | ~20 min |

Au-delà de ~10 clusters, le coût de coordination dépasse le gain de parallélisme.

---

## Gotchas

- **Ne PAS utiliser Explore** pour auditer — Explore = recherche rapide read-only, pas audit conformité
- **Ne PAS lancer B sans checkpoint A** — crash session = tout à refaire
- **Ne PAS accepter verdict sous-agent sans self-verify** sur fondations critiques (faux positifs documentés)
- **Ne PAS mettre > 10 clusters** — coordination overhead > parallélisme gain
- **Spécifier la stack du repo** dans le brief cluster pour éviter faux positifs cross-stack (TS vs Python)
- **Scope élargi** : auditer `.claude/` ET racine repo (`.mcp.json`, `conftest.py`) sinon angles morts

---

## Référence

Memory sources : `feedback_audit_thematique_methode`, `feedback_audit_repo_method`
Pattern 4 auditeurs parallèles : `.claude/agents/repo-inspector.md` (mode=audit)

---

## Apprentissage

Après chaque audit cluster complété :
- Nombre de clusters utilisés vs optimal estimé
- Taux faux positifs sous-agents (Phase D)
- Types d'erreur majoritaires (1/2/3)
- Sauvegarder dans `vault/Knowledge/syntheses/audit-<repo>-<date>.md`
