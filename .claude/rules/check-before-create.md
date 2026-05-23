---
description: "Mandatory 5-step checklist before any create/modify: memory, vault, references, forge skill, delegate to specialist"
---

# Verifier AVANT de creer ou modifier — OBLIGATOIRE

Avant toute creation ou modification de composant (skill, agent, hook, rule, prompt), executer ce checklist dans l'ordre. AUCUNE EXCEPTION, meme si "c'est juste un petit changement".

## 1. Memoire (MEMORY.md)

Relire les feedbacks pertinents au TYPE de tache. Les erreurs passees sont documentees — ne pas les refaire.
- skill → `feedback_skill_*`, `feedback_use_skill_creator`
- agent → `feedback_agent_*`, `feedback_no_cto_agent`
- hook → `feedback_hooks_*`
- general → `feedback_major_mistakes`

## 2. Ordre canonique : ANALYSER → LIRE CANONIQUES → CROISER → PLAN → EXÉCUTER

L'ordre est CRITIQUE. Sauter une étape ou inverser = audit biaisé.

### Étape A — ANALYSER LE RÉEL D'ABORD (sans biais canonique)

Pour un audit / création :
- Auditer skills/agents/hooks/rules existants (compter, lister, mesurer)
- Scanner le code RÉEL (étape 1 + 5 méthode canonique)
- Extraire les FAITS bruts : ce que le repo fait, pas ce qu'il devrait faire

**Pourquoi en premier** : si tu lis les canoniques avant, tu viens à l'analyse biaisé — tu vois ce que tu t'attends à voir. L'analyse brute donne le RÉEL sans filtre.

### Étape B — LIRE CANONIQUES EN ENTIER (après analyse)

Interroger le vault via MCP (JAMAIS CLI/Grep/Read brut). `search_brain` retourne des EXTRAITS ~10 lignes — INSUFFISANT pour audit/création.

**Règle absolue** : lire EN ENTIER les notes canoniques pertinentes via `read_note` (SANS `max_lines` ou `max_lines: 500+`).

| Tâche | Notes canoniques à lire EN ENTIER |
|-------|----------------------------------|
| Créer/modifier agent | [[comment-creer-agent]] + [[workflow-claude-code-optimal]] |
| Créer/modifier skill | [[comment-creer-skill]] + [[mcp-vs-skills-doctrine]] |
| Créer/modifier hook | [[comment-creer-hook]] + [[raisonnement-22mai-doctrine-vs-enforcement]] |
| Optimiser CLAUDE.md | [[comment-ecrire-claudemd]] + [[pattern-vault-llm-karpathy]] |
| Auditer / analyser repo | **TOUTES** : [[methode-analyser-repo]] + [[comment-creer-agent]] + [[comment-creer-skill]] + [[comment-creer-hook]] + [[comment-ecrire-claudemd]] + [[workflow-claude-code-optimal]] + [[raisonnement-22mai-doctrine-vs-enforcement]] |

Puis chercher dans `Knowledge/erreurs/`, `Knowledge/questions/`, `07-Prompts/` pour le contexte spécifique.

### Étape C — CROISER analyse ⨯ canoniques

Mettre côte-à-côte les FAITS observés (étape A) et les RÈGLES canoniques (étape B). Lister les ÉCARTS mesurables :
- Agent X = Opus mais doctrine dit Sonnet → écart sonnet/opus split
- Skill Y = 800L mais canonique dit < 500L → écart taille
- Hook Z = workflow gate mais doctrine 22 mai interdit → écart doctrinal
- Etc.

Pas d'opinion, pas d'idéologie. Que des écarts mesurables.

### Étape D — PLAN basé sur les ÉCARTS (pas sur l'idéologie)

Le plan = liste des écarts à fixer, priorisés. Si pas d'écart sur un point → pas de fix.

### Étape E — EXÉCUTER

Anti-pattern documenté ([[feedback_lire_canoniques_avant_audit]]) : "lire canoniques d'abord = biais de perception" + "search_brain seul = audit basé mémoire session, pas source de vérité". Erreur audit ia_back 22 mai 2026.

## 3. References existantes

Lire les `references/` du composant cible AVANT de modifier le SKILL.md ou l'agent.
Si le composant n'existe pas encore, lire les references des composants similaires.

## 4. Skill de reference forge

Charger la skill forge pertinente (cc-skills-ref, cc-agents-ref, cc-hooks-ref, cc-prompt-ref) pour avoir le format a jour.

## 5. Deleguer aux agents specialises

SKILL.md → skill-creator, agents/*.md → agent-creator, CLAUDE.md → claudemd-optimizer, hooks → hook-creator.
Le hook `delegate-guard.py` BLOQUERA l'edit direct de toute facon. Autant deleguer d'entree.

## Anti-patterns (TOUS observes en production)

- "Je sais deja" → FAUX. C'est arrive le 2026-04-26 : 6 skills + 14 agents edites a la main sans rien verifier
- "C'est juste un petit ajout" → petit ajout x 20 = gros probleme de conformite
- "Je vais aller plus vite sans agent" → plus vite OUI, mais non conforme = refaire tout apres
- "Je vais verifier apres" → non, tu oublieras. Verifier AVANT ou le hook te bloquera.
