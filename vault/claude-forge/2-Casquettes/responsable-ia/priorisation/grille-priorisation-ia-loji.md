---
titre: "Grille de priorisation des opportunités IA (moat ×2)"
resume: "Scorer chaque opportunité IA sur 3 axes — Impact € + Moat ×2 (exploite la donnée Loji ?) + Faisabilité. Le moat compte double : priorise l'inimitable sur le faisable. Montre ce qu'on choisit de NE PAS faire."
aliases:
  - "grille priorisation IA"
  - "scoring opportunités IA"
  - "priorisation moat"
  - "quelle feature IA d'abord"
  - "matrice impact moat faisabilité"
domaine: priorisation
type: methode
derniere-maj: 2026-06-01
auteur: claude
sources:
  - "[[comprendre-neoteem-vue-responsable-ia]]"
  - "[[wsjf-pour-equipe-petite]]"
tags:
  - "#type/methode"
  - "#casquette/responsable-ia"
  - "#domaine/priorisation"
---

# Grille de priorisation des opportunités IA

## Quand utiliser

Pour arbitrer entre plusieurs opportunités IA (features produit, agents, chantiers internes) et **expliquer la priorisation à une direction**. L'intérêt n'est pas seulement de choisir — c'est de **montrer ce qu'on choisit de NE PAS faire**, ce qui distingue un Lead IA senior d'un technicien qui empile les démos.

## Les 3 axes

| Axe | Question | 1 | 5 |
|---|---|---|---|
| **Impact €** | Gain mesurable ou argument de vente ? | Confort | €€€ / deal-maker |
| **Moat ×2** | Exploite la donnée propriétaire (Loji) ? | Générique (Gemini le fait) | Branché données client |
| **Faisabilité** | Socle prêt, risque qualité/RGPD maîtrisé ? | Build from scratch | Quick win sur l'existant |

**Score = Impact + (Moat × 2) + Faisabilité. Max = 20.**

## Pourquoi le moat compte double

L'IA est une commodité (mêmes modèles pour tous les concurrents). L'avantage inimitable de Neoteem = **la donnée Loji** (cf [[comprendre-neoteem-vue-responsable-ia]], le moat). Donc une opportunité qui exploite la donnée propriétaire vaut structurellement plus qu'une opportunité générique, même plus faisable. Le ×2 force ce tri.

## La règle à énoncer (devant la direction)

> « Je ne priorise pas ce qui est faisable. Je priorise ce qui exploite notre donnée et que personne ne peut copier. Le reste attend ou est écarté. »

## L'item parké volontaire

Toujours garder dans la grille **un item à score bas (générique)** pour illustrer la discipline. Exemple : un chatbot générique faisable mais à faible moat reste parké. C'est cet item qui prouve que tu priorises vraiment — à dégainer si on te dit « pourquoi pas plus de X ? ».

## Pièges

- ⚠️ Score haut ≠ go immédiat : une opportunité à fort moat peut déclencher un statut **Provider AI Act** (ex. scoring locataire) → instruire la conformité avant de lancer.
- ⚠️ Fenêtre concurrentielle : intégrer l'urgence quand un concurrent direct émerge (ne pas figer la grille sur le seul score).

## Anti-patterns

- ❌ Prioriser sur l'instinct / le plus excitant techniquement
- ❌ Distribuer les priorités pour « équilibrer » les axes (cf [[feedback_pas_de_symetrie_artificielle_priorisation]] côté forge)
- ❌ Cacher les items écartés → on perd l'argument de discipline

## Liens

- [[comprendre-neoteem-vue-responsable-ia]] — le moat (donnée Loji) qui justifie le ×2
- [[wsjf-pour-equipe-petite]] — autre méthode de scoring (RICE/WSJF), pour backlog produit classique
- [[reunion-kit-de-decision-autonome]] — la grille en annexe d'une réunion de décision
- [[roadmap-now-next-later]] — où atterrissent les opportunités priorisées
