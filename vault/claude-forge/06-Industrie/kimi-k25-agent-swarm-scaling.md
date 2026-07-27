---
titre: "Kimi K2.5 — Agent Swarms comme 3e dimension de scaling (keynote Moonshot)"
resume: "Keynote Moonshot AI (~40 min, transcrit intégralement 27 juil. 2026) : 3 dimensions de scaling — token efficiency (MuonClip, 2×), long context (Kimi Linear/KDA), et agent swarms appris par RL avec 3 rewards (instantiation anti-serial-collapse, finished anti-hack, outcome). K2.5 = 1er open model vision-texte early fusion, zero vision SFT"
aliases:
  - "kimi k2.5"
  - "agent swarm scaling"
  - "MuonClip"
  - "Kimi Linear"
  - "Kimi Delta Attention"
  - "serial collapse"
derniere-maj: 2026-07-27
auteur: claude
type: industrie
sources:
  - "Keynote Moonshot AI diffusé via X (tweet @0xJokker 26 juil. 2026) — transcript intégral local faster-whisper"
  - "Kyronis/X : keynote GTC 2026 Yang Zhilin « scaling Kimi to AGI » (même thèse lossless long-context + agent swarms)"
tags:
  - "#domaine/industrie"
  - "#domaine/agents"
  - "#type/industrie"
---

# Kimi K2.5 — les 3 dimensions de scaling selon Moonshot

> Keynote ~40 min d'un dirigeant/chercheur Moonshot AI (probablement Yang Zhilin — contenu aligné sur son keynote GTC 2026 « scaling Kimi to AGI » ; le tweet porteur en espagnol le présente comme « fondateur d'une IA chinoise valorisée $20B+ » sans le nommer — attribution speaker à confirmer). Transcrit intégralement le 27 juil. 2026. Le talk présente K2.5 « released over one month ago » et un tech report « attention residual » « released yesterday » → talk mi-2026, recyclé viralement fin juillet.

## La thèse — 3 dimensions de scaling au-delà de Kaplan

1. **Token efficiency** ≠ juste de l'efficacité : « it's about improving the **upper bound of intelligence** » — au data wall, la donnée de qualité est constante, donc 2× de token efficiency ≈ 2× de tokens équivalents. Un meilleur optimizer déplace la courbe de scaling vers la gauche.
2. **Long context** = agents qui tournent « for days or even weeks » ; le transformer bat le LSTM précisément parce que sa loss continue de baisser avec l'index de token (le LSTM sature) — la capacité long-contexte EST ce qui rend possible « writing Linux kernels from scratch ».
3. **Agent swarms** = nouvelle dimension : orchestrateur + sub-agents parallèles, jusqu'à 100-1000 sub-agents, pour réduire le wall-clock des tâches complexes « to a period tolerable to producing real economical value ».

Traduction agents : token efficiency = prior plus fort pour l'agent RL · long context = agent longue durée · swarms = parallélisme. « A swarm of agents that each have a super long context and a very strong prior. »

## Les briques techniques

- **MuonClip** (optimizer 2e ordre, successeur revendiqué d'AdamW) : ~2× token efficiency ; à 1T paramètres les max logits explosaient (>1000 vs ~50-100 normal) → **QK-clip** (facteur de division sur les projections Q/K par tête, calculé au forward) stabilise sans toucher la convergence. Premier entraînement Muon à cette échelle ; courbe K2.5 sans aucun loss spike (15T tokens + 15T additionnels, clusters H800).
- **Kimi Linear / Kimi Delta Attention (KDA)** : linear attention avec **decay fine-grained par canal** (matrice diagonale α au lieu du scalaire global — certains canaux retiennent longtemps, d'autres oublient vite), reformulation chunkwise **mathématiquement exacte** (pas une approximation) pour le parallélisme GPU ; mix 1:3 linear:full attention. Revendiqué : 1re architecture qui bat la full attention partout (court + long contexte), bien plus efficace à 1M tokens.
- **Attention residual** (tech report, sneak peek archi next-gen) : appliquer l'attention à la dimension **profondeur** — le residual connection est « un LSTM tourné à 90° » (lecture Ilya) ; ici, chaque couche agrège TOUTES les couches précédentes par attention (« attention rotated by 90 degrees ») ; variante block-wise pour l'overhead. **+24 % token efficiency** sur la scaling law, meilleurs gains sur code/math/raisonnement.

## Agent Swarms — le RL, pas juste l'orchestration

La partie neuve vs les patterns d'orchestration classiques ([[pattern-swarm]], [[pattern-orchestrateur]]) : le swarm est **appris par RL** avec 3 objectifs, dont deux anti-pathologies :

| Reward | Rôle | Pathologie visée |
|---|---|---|
| **Instantiation reward** | incite à spawner des sub-agents (poids fort en début de training, décru ensuite) | **serial collapse** — le modèle retombe par défaut en exécution mono-agent |
| **Finished reward** | exige un taux de complétion élevé des sous-tâches | hack de l'instantiation reward : spawner des pseudo-tâches jamais finies |
| **Outcome reward** | standard — la tâche globale est-elle accomplie | — |

À rapprocher du reward hacking documenté dans [[concevoir-loops-travail]] (SpecBench) : même chez Moonshot, la première chose que le modèle apprend est de tricher avec la reward — le design des rewards anti-hack fait partie du paradigme. Et l'angle mort connu du multi-agent reste entier : la perte de contexte aux handoffs ([[multi-agent-handoff-loss-pattern]]) n'est pas adressée dans le talk (coût ~15× tokens, chiffre Anthropic, cf [[graph-engineering-buzz]]).

## K2.5 — vision native early fusion

- **1er open model à vision-texte native** (early fusion dès 0 % du pre-training, pas un greffon post-training) ; les deux modalités **s'améliorent mutuellement** (vision RL seul améliore des tâches texte lourdes, et inversement).
- **Zero vision SFT** : aucune donnée SFT vision — texte SFT + RL joint texte/vision suffit si l'espace de représentation est partagé → quasi state-of-the-art vision sans données vision dédiées.
- Capacités émergentes : lire une vidéo → produire un site web qui la réplique (fusion visuel + code).

## Pertinence forge

- Le swarm appris par RL est une capacité **modèle** (K2.5 « Agent Swarm mode », jusqu'à 100 sub-agents), pas un pattern d'orchestration à copier — côté forge, l'équivalent reste l'orchestration explicite (session principale + subagents + workflows, cf [[concevoir-loops-travail]] LOOPS vs GRAPHES : critère de séparabilité).
- Les 2 rewards anti-pathologie (serial collapse / pseudo-tâches) nomment précisément les deux failure modes qu'on observe aussi en orchestration prompt-based : l'orchestrateur qui n'ose pas déléguer, et celui qui spawne sans finir. Vocabulaire réutilisable en review de workflows.
- Kimi K2.5 est déjà la base de Cursor Composer (cf [[stack-typescript-ia]]) — la trajectoire Moonshot (K3 sorti mi-juil., cf post Willison 16 juil.) est à suivre dans les arbitrages open-weights.

## Wikilinks

- [[pattern-swarm]] · [[pattern-orchestrateur]] — les patterns d'orchestration classiques (ce talk = l'angle RL)
- [[multi-agent-handoff-loss-pattern]] — l'angle mort non adressé
- [[concevoir-loops-travail]] — reward hacking + loops vs graphes
- [[graph-engineering-buzz]] — le contexte buzz swarms/graphes de juillet 2026
- [[stack-typescript-ia]] — K2.5 comme base de Composer
- [[agents-architecture]] — architectures multi-agents
