---
titre: "Perte d'information au handoff multi-agent — un pattern mesuré"
resume: "Chaque transfert de contrôle entre agents perd du contexte : le paper Google/MIT 2025 le quantifie (séquentiel -39/-70%, error amplification 17x indépendant vs 4.4x centralisé). Thèse de synthèse : le coût du multi-agent n'est pas le nombre d'agents mais le nombre de handoffs sur le chemin critique ; le threshold 45% est le seuil de rentabilité du handoff."
aliases:
  - "multi-agent handoff loss pattern"
  - "perte information handoff agents"
  - "dégradation séquentielle multi-agent"
  - "error amplification handoff"
  - "pourquoi le multi-agent dégrade"
type: technique
derniere-maj: 2026-06-07
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/agents"
  - "#statut/canonique"
---

# Perte d'information au handoff multi-agent

Quand on fragmente une tâche entre plusieurs agents, chaque **transfert de contrôle** (handoff) coûte : l'agent receveur ne reçoit jamais l'intégralité de l'état mental du précédent. Cette note croise trois sources pour en tirer une grille de décision actionnable.

## Thèse — le coût, c'est le handoff, pas l'agent

Le réflexe naïf mesure le multi-agent au **nombre d'agents** (« plus d'agents = plus de puissance »). La bonne unité de coût est le **nombre de handoffs sur le chemin critique** — chaque passage de relais est un point de fuite de contexte et un point d'amplification d'erreur.

- **Tâche séquentielle** (chaque action dépend de l'état précédent) = handoffs empilés sur le chemin critique → dégradation garantie : le paper Google/MIT mesure **-39 % à -70 %** sur toute variante multi-agent (PlanCraft/Minecraft). Le raisonnement se fragmente, le « cognitive budget » part dans la coordination.
- **Tâche parallèle** (sous-tâches indépendantes) = **zéro handoff sur le chemin critique**, une seule agrégation finale → **+81 %** (analyse financière : trends/costs/market en parallèle). Le gain ne vient pas du nombre d'agents mais de l'absence de relais intermédiaire.

## Le mécanisme de la fuite (vu côté implémentation)

[[pattern-swarm]] documente exactement *par où* le contexte fuit, indépendamment des chiffres :

- **Failure mode « perte de contexte »** : l'agent B ne sait pas ce que A a déjà tenté. Mitigation = passer l'historique complet, ou un résumé explicite — mais un résumé est *par construction* une perte.
- **Failure mode « history bloat »** : passer TOUT l'historique fait exploser les tokens → on compacte → on reperd. Le handoff est pris entre deux pertes (troncature vs coût).

L'**error amplification** est la même cause vue côté qualité : sans point de validation au handoff, une erreur de A passe non vérifiée chez B. Mesure paper : **17x** en swarm indépendant vs **4.4x** en coordination centralisée (l'orchestrateur valide l'output avant de relayer).

## Implication design forge

La décision « single vs multi-agent » de [[comment-creer-agent]] se relit entièrement via le handoff :

1. **Mesurer le single-agent d'abord.** Le **threshold 45 %** (single-agent >45 % de succès → multi pas cost-effective) est le **seuil de rentabilité du handoff** : au-dessus, le gain d'un sub-agent ne couvre pas le coût du/des relais qu'il introduit.
2. **Ne paralléliser que le réellement indépendant.** Fragmenter du séquentiel = ajouter des handoffs sur le chemin critique = dégradation. Paralléliser des branches sans interdépendance = aucun handoff entre elles.
3. **Si on fragmente quand même : orchestrateur central > swarm.** 4.4x < 17x — le point de passage central est précisément l'endroit où valider et compacter *avant* de perdre le contexte. C'est la même conclusion que la topologie de coordination de [[workflow-claude-code-optimal]].

## En une phrase

Compte les handoffs sur le chemin critique, pas les agents. Chaque handoff est une perte de contexte et une amplification d'erreur ; le threshold 45 % dit quand cette perte n'en vaut plus la peine.

## Liens

- [[google-mit-scaling-agent-systems-2025]] — la source quantitative (180 expériences, les chiffres)
- [[pattern-swarm]] — le mécanisme de la fuite côté implémentation (failure modes #2/#4)
- [[comment-creer-agent]] — la règle de design (threshold 45 %, single avant sub-agent)
- [[workflow-claude-code-optimal]] — coordination topology (orchestrateur vs swarm)
