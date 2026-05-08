---
titre: "Decoupe agents — anti-crash pattern"
resume: "Regles universelles pour eviter les crashs d'agents : max 6-8 ops, decoupage par theme/repo/phase, prompt precis"
aliases:
  - agent anti-crash
  - decoupage agents
  - agent crash prevention
  - agent splitting pattern
  - eviter crash agent
  - max operations agent
domaine: claude-code
type: technique
derniere-maj: 2026-05-08
auteur: claude
sources: []
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Description

Regles universelles pour eviter les crashs d'agents Claude Code : max 6-8 operations lourdes, decoupage par theme/repo/phase, prompt precis avec format de sortie.

## Quand utiliser

Avant de lancer un agent avec une tache complexe, ou apres un crash d'agent pour comprendre pourquoi et decouper correctement.

## Probleme

Un agent qui recoit trop d'operations (lectures, recherches, analyses) dans une seule tache crash sans retourner de resultat partiel. Tout est perdu.

## Les 3 causes de crash

| Cause | Explication |
|-------|------------|
| Contexte sature | L'agent lit/recoit trop de donnees (gros fichiers, beaucoup de resultats) |
| Timeout | Trop d'operations sequentielles, depasse la limite (~2-5 min) |
| Boucle / erreur recurrente | L'agent retry en boucle, consomme tout son budget |

## Signaux d'alerte AVANT de lancer

- Plus de 6-8 operations independantes → decouper
- Fichiers > 500 lignes a analyser → paginer ou cibler
- Tache vague sans scope clair ("analyse tout") → cadrer dans le prompt
- Melange lecture + ecriture + recherche dans un seul agent → separer les phases

## Patterns de decoupage

### Par theme

```
Agent 1 : Claude Code officiel
Agent 2 : Concurrents
Agent 3 : Leaders
```

### Par fichier / repo

```
Agent 1 : ia_back
Agent 2 : neo_ia
Agent 3 : neoteem-brain
```

### Par phase

```
Agent 1 : recherche/exploration (read-only)
→ consolidation manuelle
Agent 2 : implementation (write)
```

### Par type d'operation

```
Agent 1 : lire 5 fichiers, extraire les patterns
Agent 2 : lire 5 autres fichiers
→ consolidation → Agent 3 : ecrire le resultat
```

## Regles absolues

1. **Max 6-8 operations lourdes par agent** (web search, lecture gros fichier, grep large)
2. **Prompt precis** — dire EXACTEMENT quoi chercher, ou, et format de sortie attendu
3. **Limiter la taille de reponse** — "sous 300 mots", "liste uniquement"
4. **Paralleliser ce qui est independant** — un seul message avec N blocs Agent()
5. **Sequencer ce qui depend** — Agent 1 finit → lire → Agent 2 part avec le contexte
6. **Jamais de tache floue** — "fais tout" = crash. "Fais X dans Y, retourne Z" = OK

## Quand NE PAS utiliser d'agent

- 1-2 operations simples → faire directement (Read, Grep, Bash)
- Fichier connu, chemin connu → Read direct
- Grep cible → Grep direct
- Question simple → repondre directement

L'agent c'est pour les taches qui demandent plusieurs etapes de raisonnement ou qu'on veut paralleliser.

## Incident de reference

cc-news 8 mai 2026 : 1 agent general-purpose avec 24 recherches web → crash. Redecoupe en 4 agents de 5-7 recherches → succes en ~60s chacun, parallelises.

## Exemple

Avant (crash) :
```
1 agent : 24 web searches + synthese → crash
```

Apres (succes) :
```
Agent 1 : 6 searches theme A → resultat
Agent 2 : 6 searches theme B → resultat
Agent 3 : 6 searches theme C → resultat
Agent 4 : 6 searches theme D → resultat
→ session consolide les 4 resultats
```

## Liens

- [[MOC-Techniques]]
- [[limites-subagents-claude-code]]
