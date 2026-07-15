---
titre: "Dette — détection des signaux de friction skills (skill-evolve --mode=friction)"
resume: "Dette acceptée 15 juil. 2026 : sur les 4 signaux de friction skills, 2 sont fiables en détection auto (erreur récurrente, collision), 2 sont fragiles (skill manquée, résultat corrigé) et traités en 'candidats à valider' plutôt qu'en labels auto. Décidé après DA (2 bloquants) + recherche état de l'art."
aliases:
  - "dette detection friction skills"
  - "signaux friction skill-evolve"
  - "dette skill-friction-scan"
  - "skill manquee resultat corrige detection"
derniere-maj: 2026-07-15
auteur: claude
type: dette
sources:
  - "https://arxiv.org/abs/2505.00212 (Who&When, LLM-judge 14,2% step-level)"
  - "https://arxiv.org/abs/2507.23158 (implicit user feedback, EMNLP 2025, précision 61%/rappel 36%)"
  - "Knowledge/critiques/critique-2026-07-15-loop-skill-friction-scan.md (DA)"
tags:
  - "#type/dette"
  - "#domaine/claude-code"
  - "#domaine/skills"
---
# Dette — détection des signaux de friction skills

## Le BLOCKING du DA (15 juil. 2026)

DA sur la SPEC `skill-friction-scan` : **2 bloquants (≥80)**.
- **B1 (85)** : sur les 4 signaux de « skill qui a frotté », 2 sont indétectables de façon fiable depuis les transcripts — signal 1 (skill qui aurait dû se déclencher mais ne l'a pas) et signal 2 (résultat corrigé par l'utilisateur). Pas de vérité-terrain dans le `.jsonl` → risque d'hallucination.
- **B2 (82)** : composant candidat fusion (`skill-evolve --mode=friction`) plutôt que skill neuve.

## Décision (Raphael, 15 juil. 2026)

- **B2** : résolu → `skill-evolve --mode=friction`, source MCP indexée (indexer étendu pour exposer les `tool_use`). Pas de skill neuve. Pas de dette.
- **B1** : résolu par requalification des signaux selon leur confiance de détection (recherche état de l'art à l'appui) :

| Signal | Détection | Traitement |
|--------|-----------|------------|
| 3 — erreur/blocage récurrent (≥2 sessions) | **fiable auto** | rapport direct |
| 4 — collision de déclenchement | **fiable auto** (events tool_use concurrents) | rapport direct |
| 2 — résultat corrigé | **miner haute-précision** (taxonomie NEG_3, ~61% précision / 36% rappel — arXiv:2507.23158) | rapport, corrections nettes seulement |
| 1 — skill manquée | **proxy comportemental** (skill dispo + non appelée + invoquée à la main au tour suivant) | **candidat à valider par Raphael**, jamais affirmé |

## La dette assumée

Les signaux 1 et 2 **ne sont pas de la vérité-terrain** : le signal 1 en labeling auto plafonne à ~14% (Who&When), le signal 2 rate ~2/3 des corrections. **On les traite en surfaceurs de candidats à validation humaine, pas en détecteurs automatiques.** Le compounding reste jugement-piloté (cohérent avec [[loop-apprentissage-codex]] : ni Willison ni OpenAI ne décrivent un loop auto-édition). Remédiation possible si besoin : replay du routeur sur le prompt (plus fiable mais n'est plus du log-mining, coûteux) — non retenu pour l'instant.

## Angles morts à adresser à la construction

- **Chevauchement `/done`** : `/done` fait déjà la métacognition fin-de-session (extraction d'erreurs). Le mode friction ne doit pas re-surfacer ce que `/done` a déjà capturé.
- **`search_sessions` strippe les tool_use** (cf [[ajouter-source-donnees-mcp-forge-brain]]) → l'indexer doit être étendu pour exposer les tool_use, sinon signaux 1/4 aveugles.

## Liens

- [[loop-apprentissage-codex]] — le pattern auto-améliorant (compounding jugement-piloté)
- [[skill-evolve]] — la skill hôte du mode friction
- [[ajouter-source-donnees-mcp-forge-brain]] — pattern source MCP indexée
