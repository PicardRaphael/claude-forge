---
titre: "Decoupe agents — anti-crash pattern (principes qualitatifs)"
resume: "Principes qualitatifs pour eviter les crashs d'agents : scoping precis, prompt format de sortie, parallelisation independante. Pas de seuil numerique canonique Anthropic."
aliases:
  - agent anti-crash
  - decoupage agents
  - agent crash prevention
  - agent splitting pattern
  - eviter crash agent
  - principes decoupe agents
domaine: claude-code
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "https://code.claude.com/docs/en/sub-agents"
  - "https://code.claude.com/docs/en/best-practices"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
---

## Description

Principes qualitatifs pour eviter les crashs d'agents Claude Code. **Pas de seuil numerique canonique** dans la doc Anthropic — les "max 6-8 ops" et "max 5 fichiers" qui ont longtemps circule dans forge sont du folklore (mythes confirmes par audit 23 mai 2026, voir [[feedback_seuils_canoniques_agents_mythes]] et [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]]).

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

## Signaux d'alerte AVANT de lancer (qualitatifs)

- Tache vague sans scope clair ("analyse tout") → cadrer dans le prompt
- Beaucoup d'operations independantes empilees → decouper ou paralleliser
- Gros fichiers a analyser → paginer ou cibler
- Melange lecture + ecriture + recherche dans un seul agent → separer les phases
- Pas de format de sortie explicite → l'agent improvise et drift

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

## Regles qualitatives

1. **Prompt precis** — dire EXACTEMENT quoi chercher, ou, et format de sortie attendu (verbatim Anthropic best-practices)
2. **Limiter la taille de reponse** — "sous 300 mots", "liste uniquement"
3. **Paralleliser ce qui est independant** — un seul message avec N blocs Agent()
4. **Sequencer ce qui depend** — Agent 1 finit → consolider → Agent 2 part avec le contexte
5. **Jamais de tache floue** — "fais tout" = crash. "Fais X dans Y, retourne Z" = OK

> [!note] Pas de seuil chiffre
> Les versions anterieures de cette note enoncaient "Max 6-8 operations lourdes par agent" et "Max 5 fichiers par agent" comme regles absolues. **Ces seuils n'existent pas dans la doc Anthropic.** WebFetch direct de [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) et `/docs/en/best-practices` (audit 23 mai 2026) ne montre aucun chiffre. La description Anthropic est qualitative : "side task would flood your main conversation". Garder donc des principes qualitatifs, pas des nombres magiques.

## Quand NE PAS utiliser d'agent

- 1-2 operations simples → faire directement (Read, Grep, Bash)
- Fichier connu, chemin connu → Read direct
- Grep cible → Grep direct
- Question simple → repondre directement

L'agent est pour les taches qui demandent plusieurs etapes de raisonnement ou qu'on veut paralleliser.

## Incident de reference

cc-news 8 mai 2026 : 1 agent general-purpose avec 24 recherches web → crash. Redecoupage en 4 agents paralleles avec scope precis → succes en ~60s chacun, parallelises. **L'apprentissage canonique** : scoping + parallelisation, pas un seuil numerique magique.

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

Le `6` ici est empirique pour CE cas (volume de recherches similaires sur des themes proches), pas une regle universelle. Mesure-le pour ton cas, ne le cite pas comme canonique.

## Liens

- [[MOC-Techniques]]
- [[limites-subagents-claude-code]] — Limites techniques (bugs GitHub)
- [[subagent-explore-then-edit]] — Pattern Anthropic explore/edit
- [[Knowledge/erreurs/agents-ia-22-claims-fausses-2026-05-23]] — audit source de cette reecriture
