---
titre: "Prompting par plateforme — Chat vs Cowork vs Code"
resume: "Differences de prompting entre Claude Chat, Cowork et Code. Best practices specifiques a chaque plateforme, Opus 4.7 par defaut"
aliases:
  - "prompting Claude Chat"
  - "prompting Cowork"
  - "Chat vs Code vs Cowork"
  - "differences prompting plateformes"
  - "prompting plateforme Anthropic"
  - "prompting Opus 4.7"
domaine: prompting
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
  - "https://az-arte.com/en/articles/claude-chat-cowork-code-differences"
  - "https://claudiaplusai.substack.com/p/claude-cowork-starter-guide-30-examples"
  - "[[amanda-askell-prompt-engineering]] — eviter les spirales de critique"
  - "https://medium.com/illumination/claude-cowork-vs-claude-chat-when-to-use-which-and-why-most-people-get-it-wrong-e09201a9de3f"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
  - "#pattern/prompting"
---

## Description

Differences de prompting entre Claude Chat, Cowork et Code. Chaque plateforme a ses patterns optimaux — le contexte engineering bat le wordsmithing dans les 3 cas.

## Quand utiliser

Quand on redige un prompt et qu'on a besoin de savoir quel style adopter selon la plateforme cible (Chat, Cowork, Code).

## Modele par defaut

Claude Chat et Cowork utilisent **Opus 4.7** par defaut (avril 2026). Les best practices Opus 4.7 s'appliquent : instructions plus litterales, moins d'interpretation spontanee, etre explicite sur le scope.

## Claude Chat — conversationnel, reactif

| Aspect | Best practice |
|--------|--------------|
| Style de prompt | Court, iteratif, exploratoire. On pense AVEC Claude, on ne delegue pas A Claude |
| Artifacts | Se declenchent automatiquement pour le contenu substantiel (15+ lignes). Demander le format specifique (.docx, .pptx, tableau) |
| Projets | Custom instructions = onboarding doc permanent. Specifique >> vague |
| Recherche web | Disponible mais Claude ne sait pas POURQUOI on a besoin de l'info — toujours donner le cadre |
| Limites | 20 fichiers/conversation, 30MB/fichier. Pas d'acces fichiers locaux |
| Memoire | Session-scoped sauf dans un Projet. Auto Memory si active |
| Ton | Respectueux et precis. Les tons critiques/agressifs declenchent des spirales d'excuse (Askell) |

### Pattern Chat optimal

```
[Contexte en 1 ligne]
[Ce que je veux — objectif clair]
[Format attendu si specifique]
[Contrainte si necessaire]
```

Court. Claude demandera des precisions si besoin.

## Claude Cowork — agentique, oriente resultat

| Aspect | Best practice |
|--------|--------------|
| Style de prompt | Brief de delegation : livrable, definition de "termine", contraintes, contexte |
| Micro-etapes | NE PAS micro-detailler ("ouvre le fichier, copie la colonne B"). Decrire le RESULTAT |
| Socratique | Technique la plus efficace : "Avant de commencer, quelles questions tu as ?" |
| Instructions globales | Identite + voix + regles anti-slop dans les instructions globales Cowork. Plus impactant que changer de modele |
| Memoire | Persiste dans les Projets, pas dans les sessions standalone |
| Sous-agents | Se lancent automatiquement pour les sous-taches independantes |
| Tokens | Consomme plus de tokens que Chat — etre concis dans les instructions |

### Pattern Cowork optimal

```
[Contexte]
[Livrable attendu — quoi exactement]
[Ce que "termine" veut dire]
[Contraintes / ce qu'il ne faut PAS faire]
[Avant de commencer, dis-moi quelles questions tu as]
```

Deleguer, pas micro-manager.

## Claude Code — terminal, codebase-aware

| Aspect | Best practice |
|--------|--------------|
| Style de prompt | Commandes orientees tache. Le contexte vient du CLAUDE.md + arbre projet automatiquement |
| Scope | Etre explicite sur le scope et le parallelisme (Opus 4.7 = plus litteral) |
| CLAUDE.md | ~100 lignes max. Trop long = regles ignorees. Convertir les evidences en hooks |
| Echec | Apres 2 corrections echouees : /clear et reecrire le prompt plutot que polluer le contexte |
| Skills/agents | Le prompt = la description YAML + le SKILL.md. Pas de conversation |

## Principe universel (les 3 plateformes)

**Le context engineering bat le wordsmithing.** Structurer ce que Claude recoit (fichiers, instructions, exemples, role) est plus efficace que peaufiner la formulation du prompt.

Concretement :
- Les custom instructions / CLAUDE.md > un prompt bien ecrit dans une conversation vide
- Les skills qui injectent du contexte (vault, Jira) > un prompt qui essaie de tout expliquer
- Les exemples few-shot > les regles abstraites

## Erreurs frequentes par plateforme

| Plateforme | Erreur | Correction |
|-----------|--------|-----------|
| Chat | Prompt trop long et detaille en une fois | Court et iteratif, affiner en conversation |
| Chat | Ton critique ("c'est nul, refais") | Ton precis et respectueux, eviter spirales d'excuse |
| Cowork | Micro-detailler chaque etape | Decrire le resultat, pas le process |
| Cowork | Pas de definition de "termine" | Inclure les criteres de completion |
| Code | CLAUDE.md de 300 lignes | Pruner a 100 lignes, deporter dans rules/ et skills/ |
| Code | Accumuler les corrections au lieu de /clear | /clear apres 2 echecs, reecrire le prompt |
| Toutes | Pas de format de sortie | Toujours specifier le format attendu |

## Exemple

**Chat** : "Je dois rediger un mail de relance client. Ton professionnel mais ferme. 3 paragraphes max."

**Cowork** : "Cree un rapport d'analyse concurrentielle. Livrable = tableau comparatif 5 criteres x 4 concurrents + recommandation. Avant de commencer, quelles questions tu as ?"

**Code** : `implemente l'endpoint POST /api/feedbacks avec validation zod et test unitaire`

## Liens

- [[MOC-Techniques]]
- [[forge-prompt-machine]] — 12 principes FORGE BellumAI x Askell
- [[Context Engineering]] — Paradigme dominant 2026
- [[Adaptive Thinking]] — Opus 4.7 comportement
