---
titre: "Dreaming — Self-Learning Agents via Review de Sessions"
resume: "Process scheduled qui review les sessions passées des managed agents, extrait patterns/erreurs récurrentes, déduplique, vérifie et enrichit la mémoire. Research preview mai 2026. Inspiré du sommeil humain — consolidation mémoire entre sessions"
aliases:
  - "dreaming"
  - "dreaming agents"
  - "dreaming managed agents"
  - "self-learning agents"
  - "agent dreaming"
  - "dream process"
  - "rêve agents"
type: feature
derniere-maj: 2026-05-11
auteur: claude
sources:
  - "https://www.youtube.com/watch?v=RtywqDFBYnQ"
  - "https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/agents"
---

## Contexte

Lancé en **research preview** dans le Managed Agents API, 6 mai 2026 (Code with Claude SF). Présenté par Mahesh Murag. Complète [[Memory Managed Agents]] avec un process de review automatique.

## Comment ça marche

Dreaming = process schedulé qui :
1. **Review** les transcripts des sessions récentes (configuré : ex. 7 derniers jours)
2. **Identifie** les patterns, erreurs récurrentes, workflows convergents, préférences partagées
3. **Déduplique** les entrées redondantes (5 entrées identiques → 1)
4. **Vérifie** que les mémoires existantes sont encore valides (ajoute des "verification notes")
5. **Enrichit/backfill** avec les patterns cross-sessions qu'un seul agent ne peut pas voir
6. **Supprime** les entrées stales/obsolètes
7. Produit un **diff** appliqué à la memory store

### Analogie humaine
"Quand on dort, le cerveau review les souvenirs et renforce ceux qui valent la peine d'être gardés." Dreaming fait pareil pour les agents.

## Contrôle développeur

- **Auto** : dreaming met à jour la mémoire automatiquement
- **Review** : les changements sont proposés comme diff, le développeur approuve avant application
- Visible dans le Claude Console : sessions d'entrée, sub-agents de review, diff de sortie

## Ce que Dreaming voit qu'un agent seul ne voit pas

> "It surfaces patterns that a single agent can't see on its own: recurring mistakes, workflows that agents converge on, and preferences shared across a team."

Exemple SRE démontré :
- Plusieurs agents SRE déclenchés à exactement 60s après un spike CPU
- Aucun agent individuel ne remarque le pattern
- Dreaming identifie : "retry logic inefficace déclenche des alertes cascade avec délai fixe de 60s"
- Note ajoutée → les futurs agents bénéficient de cette découverte

## Amortissement du coût

> "Creating this index up front and curating it so that all downstream agents can use it effectively lets us amortize this effort across all of those agents."

Le coût du dreaming est payé une fois, réparti sur tous les agents qui lisent la mémoire.

## Pertinence pour forge

| Dreaming feature | Équivalent forge actuel | Gap |
|---|---|---|
| Review sessions passées | `/done` (1 session) | Pas de cross-session |
| Déduplication | `vault-audit` (score) | Pas de dedup contenu |
| Vérification mémoire | Aucun | Notes > 30j jamais revérifiées |
| Enrichissement cross-session | Aucun | Le compounding qu'on construit manuellement |
| Pattern detection | Aucun | Pas d'automatisme |

**Implémentation possible** : skill `/dream` comme `/schedule` hebdo qui review git log + vault + mémoire, déduplique, vérifie, enrichit. Pas une feature native Claude Code — à construire comme routine.

## Liens

- [[Memory Managed Agents]] — Primitive memory (storage + structure)
- [[Managed Agents]] — Feature Managed Agents
- [[MOC-Claude-Code]]


## Limites techniques (mai 2026)

| Paramètre | Valeur |
|-----------|--------|
| Sessions par dream | Max 100 |
| Input store | Jamais modifié (review-before-attach) |
| Modèles supportés | Opus 4.7, Sonnet 4.6 uniquement |
| Header API | `dreaming-2026-04-21` |
| Billing | Standard API rates |

## Démo live keynote SF (6 mai)

Startup fictive "Lumara" — landing drones sur la Lune :
- Simulation initiale : 4/6 sites réussis (Site 3 crash à 398 m/s, Site 4 en descente à 20.8 m/s)
- Dreaming lancé overnight via bouton "Dream" dans Developer Console
- Agent produit un "descent-playbook.md" avec heuristiques des missions précédentes
- Simulation post-dreaming : **6/6 sites réussis**, pas de régression

Le hill-climbing s'est fait sans intervention humaine — juste un clic sur "Dream".
