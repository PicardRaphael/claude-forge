---
titre: "Pivot doctrinal — vault forge-brain agent-first (émancipation de Karpathy)"
resume: "Instruction du pivot agent-first via methode-pivoter-doctrine : forge-brain s'émancipe du pattern Karpathy (raw/ supprimé, index/log/MOC = couche humaine optionnelle). 11 foyers purgés, caveats forge-brain-exception, condition de falsification raw/ conservée. Karpathy reste référence générique pour autres vaults."
aliases:
  - "raisonnement pivot agent-first"
  - "pivot vault agent-first 27 juin"
  - "emancipation karpathy forge-brain"
  - "instruction pivot agent-first methode"
  - "drift purge agent-first 11 foyers"
type: raisonnement
derniere-maj: 2026-06-27
auteur: claude
sources:
  - "[[decision-vault-agent-first]]"
  - "[[methode-pivoter-doctrine]]"
  - "[[critique-2026-06-27-pivot-vault-agent-first]]"
  - "session 2026-06-27 (advisor + devils-advocate sur le plan)"
tags:
  - "#type/raisonnement"
  - "#domaine/vault"
  - "#domaine/claude-code"
  - "#doctrine/2026"
---

# Pivot doctrinal — vault forge-brain agent-first

> Instruction du pivot acté dans [[decision-vault-agent-first]] (2026-06-27) via la checklist `methode-pivoter-doctrine`. Source de vérité de l'orientation : la décision. Cette note trace l'exécution du pivot (foyers, raisonnement, conditions de falsification).

## Contexte

forge-brain est un **cerveau d'agent** piloté par Jarvis via MCP — Obsidian débranché de fait depuis ~30 mai 2026. Le pattern Karpathy (raw/ immuable, index navigable, MOCs, graphe) était l'échafaudage de départ, conçu pour un humain qui butine, pas pour un agent. Usage réel (`usage_stats`) dominé par `search_brain` + `read_note`, jamais par la navigation humaine.

## Décision instruite

**Critère unique : « est-ce que ça sert la boucle agent ? », jamais « est-ce conforme à Karpathy ? ».** forge-brain s'émancipe :
- `raw/` supprimé (8 notes git rm) — sources distillées directement en wiki/.
- `index.md` + `log.md` : couche humaine **optionnelle**, non auto-maintenue (plus « obligatoires »).
- MOCs : couche humaine optionnelle — **non supprimés** (~95 backlinks = dette nette), mais l'auto-maintenance `FOLDER_TO_MOC` de vault-audit doit être retirée (ÉTAPE B).

**Karpathy reste une référence générique** : la note [[pattern-vault-llm-karpathy]] documente le pattern tel que Karpathy l'a proposé, valide pour d'autres vaults (neo_ia, neoteem-brain). On documente l'émancipation de forge-brain, on n'efface pas la source d'inspiration ni l'historique.

## 11 foyers purgés (mesurés search_brain + grep .claude/)

| # | Foyer | Type |
|---|-------|------|
| 1 | SCHEMA.md | vault canonique (chirurgies : raw/ retiré des 3-layers, ontologie, ingest, anti-patterns) |
| 2 | pattern-vault-llm-karpathy | vault — bandeau STATUT unique en tête (chapeaute DRIFT/REQUALIF = trace) |
| 3 | architecture-cerveau-obsidian-mcp | vault — caveat forge-brain exception sur diagramme |
| 4 | mcp-vault-llm-design | vault — caveat sur "Layer Karpathy strict" |
| 5 | LLM Wiki | vault — section "Lien avec forge-brain" corrigée |
| 6 | index.md racine | vault — claims présent-actuel corrigés (nav raw/ + métadonnées) |
| 7 | Home.md | vault — resume + lien Karpathy + derniere-maj |
| 8 | forge-brain SKILL.md | skill (via skill-creator) |
| 9 | pivot-check SKILL.md | skill (via skill-creator) — ligne raw/ retirée |
| 10 | forge-brain-proactive.md | rule .claude/ |
| 11 | memory/feedback_drift_implementation_karpathy_organes_morts | mémoire — "dérive" → "décision délibérée" |

## Condition de falsification conservée (raw/)

Le trigger posé à la REQUALIFICATION du 8 juin reste valide, reformulé : **si un incident d'hallucination réel remontant à une source non archivée émerge → re-créer `raw/` pour ce besoin précis, SANS rouvrir le pivot agent-first global.** (conciliation advisor « falsification conservée » + DA « re-créer ≠ rouvrir tout l'arbitrage »).

## Méta-leçon

« Dévier du pattern canonique ≠ avoir un problème » — symétrique de « valoriser ≠ consommer ». La conformité au pattern n'est jamais le critère ; le besoin de l'agent l'est. Le DA a tenu la barre « zéro drift résiduel » : 5 foyers manqués au plan v1 (6 foyers) détectés empiriquement → plan v2 à 11 foyers. Un foyer manqué relance le cycle de drift doctrine↔réel déjà documenté (feedback_doctrine_drift_pattern).

## Liens

- [[decision-vault-agent-first]]
- [[methode-pivoter-doctrine]]
- [[pattern-vault-llm-karpathy]]
- [[architecture-cerveau-obsidian-mcp]]
- [[SCHEMA]]
