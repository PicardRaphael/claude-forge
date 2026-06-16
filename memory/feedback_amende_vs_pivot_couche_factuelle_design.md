---
name: amende-vs-pivot-couche-factuelle-design
description: Avant de déclarer un "pivot doctrinal" suite à une update Anthropic, séparer la couche FACTUELLE (prémisse "impossible/interdit") de la couche DESIGN (reco "session principale orchestre"). Si seule la possibilité technique change, c'est une AMENDE ciblée, pas un pivot. Exécution : une AMENDE appendée en bas ne corrige PAS les vitrines (resume frontmatter, corps amont, gloses d'index, analogies cross-notes) — search_brain la formule périmée et corriger tous les foyers.
metadata:
  type: feedback
---

Run cc-news 16 juin 2026 : v2.1.172 (10 juin) introduit les sous-agents imbriqués (« a subagent can spawn its own subagents », jusqu'à 5 niveaux). Réflexe initial = « pivot doctrinal de [[anti-reentrance-sub-agents-pattern-escalade]] ». L'advisor a recadré : **c'est une amende, pas un pivot**.

**Le discriminant** (à appliquer avant tout verdict de pivot) : une note canonique mélange souvent deux couches.
- **Couche factuelle** = prémisse de réalité (« techniquement impossible / interdit par la plateforme »). Une update peut la rendre FAUSSE → à corriger.
- **Couche design** = recommandation (« session principale orchestre, escalade propre leaf-node »). Elle SURVIT généralement, et une feature d'enforcement peut même la renforcer.

Cas concret : la note listait 4 raisons (boucle infinie / tool_use conflits / explosion contexte / debugging impossible). La doc primaire subagents lève la possibilité technique et **neutralise 2 craintes** (boucle = foreground self-limiting + background plafonné 5 ; debugging = panel arborescent + transcripts isolés) mais **confirme** le coût contexte. Donc : requalifier « interdit » → « possible mais reco = leaf-node, désormais ENFORÇABLE » via `disallowedTools: Agent` ou `Agent(agent_type)` (v2.1.178). Le pattern ESCALADE REQUISE reste intact.

**Why** : « pivot » est un mot fort qui déclenche une réécriture lourde + drift multi-fichiers. Surdimensionner le diagnostic = travail inutile et risque d'effacer une reco encore valide.

**How to apply** :
1. Décomposer la note en couche factuelle vs couche design.
2. Demander : combien des raisons sont des raisons d'IMPOSSIBILITÉ vs de COÛT/QUALITÉ ? Seule l'impossibilité bascule avec une feature ; le coût/qualité survit.
3. Vérifier en source PRIMAIRE (changelog officiel + doc), pas agrégateur (cf [[llm-deep-research-version-numbers-hallucinated]]).
4. Si seule la possibilité change → **amende ciblée** (corriger la prémisse, garder le design, ajouter le levier d'enforcement). Sinon → vrai pivot via skill `methode-pivoter-doctrine`.
5. Toujours GATE humaine avant de toucher une note canonique (cc-news étapes 7-9).
6. **Une AMENDE appendée en bas NE corrige PAS les vitrines.** Append d'une section « AMENDE » = la fin de la note est juste, mais le `resume:` frontmatter, le corps amont (sections QUOI/POURQUOI), les gloses d'index (MOC, autres notes qui résument celle-ci en 1 ligne) et les analogies cross-notes (« même classe que X qui ne peut pas… ») continuent d'asserter le faux claim. Un lecteur du haut, ou un `search_brain` qui remonte le résumé, prend le périmé pour vrai. Après l'append : `search_brain` sur la FORMULE périmée (le claim ET ses raisons, ex. « boucle infinie + tool_use conflits ») pour traquer toutes les vitrines, puis corriger résumé + corps amont + gloses. Discriminant fin (16 juin) : une glose qui *asserte* l'impossibilité = drift à corriger ; une glose qui *décrit* une « limitation contextuelle » (coût, MCP décoratif) reste vraie → intacte (diff minimal).

Foyer méthode : [[methode-pivoter-doctrine]] (le pivot ≠ l'amende) + [[doctrine-vivante]]. Cf aussi [[regression-diagnostic-diff-avant-redesign]] (ne pas surdimensionner le diagnostic) + [[memory-discipline]] (chercher ACTIVEMENT tous les foyers, enrichir avant créer).
