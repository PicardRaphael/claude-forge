---
description: "Canonical A→B→C→D→E sequence for ANY create/modify/optimize of skill/agent/hook/CLAUDE.md/rule. Mandatory brief for sub-agents creators/analyzers."
---

# Séquence canonique pour création/modification/optimisation — OBLIGATOIRE

S'applique à : analyse repo, création/modification skill/agent/hook/CLAUDE.md/rule, optimisations (skill-evolve, evolve). **Pas d'exception.**

## A → B → C → D → E

```
A. ANALYSER le RÉEL (faits bruts du repo/composant, sans biais)
        ↓
B. LIRE canoniques EN ENTIER (read_note via MCP forge-brain)
        ↓
C. CROISER analyse ⨯ canoniques → écarts mesurables
        ↓
D. PLAN basé sur écarts (présenté à l'utilisateur)
        ↓
E. EXÉCUTER après validation
```

Source canonique : [[methode-analyser-repo]] section ORDRE CANONIQUE.

## A. Analyser le RÉEL

Observer les faits bruts avant toute prescription.
- Repo entier : stack, structure, `.claude/`, tests, patterns récurrents (`Glob`, `Read package.json/pyproject.toml`, `git log -50`)
- Composant existant : SKILL.md/agent.md/hook EN ENTIER + `references/` + `scripts/` + grep dans body d'agents + `git log -20`
- CLAUDE.md / rule : EN ENTIER + grep composants qui le référencent

**Verbatim Anthropic** : *"This phase is critical because it prevents Claude from making assumptions about your architecture."*

## B. Lire canoniques EN ENTIER

`mcp__forge-brain__read_note(file="...")` SANS `max_lines`. JAMAIS `search_brain` seul (extraits insuffisants).

| Tâche | Notes canoniques |
|---|---|
| Skill | [[comment-creer-skill]] + [[mcp-vs-skills-doctrine]] |
| Agent | [[comment-creer-agent]] + [[workflow-claude-code-optimal]] |
| Hook | [[comment-creer-hook]] + [[raisonnement-22mai-doctrine-vs-enforcement]] |
| CLAUDE.md | [[comment-ecrire-claudemd]] + [[pattern-vault-llm-karpathy]] |
| Audit/analyse repo | TOUTES + [[methode-analyser-repo]] |

Plus : `Knowledge/erreurs|critiques|raisonnements/` pour contexte spécifique.

## C. Croiser → écarts mesurables

FAITS (A) côte-à-côte avec RÈGLES (B). Lister les écarts :
- Agent Opus mais canonique = Sonnet → écart split
- Skill 800L mais canonique < 500L → écart taille
- Description skill > 250 chars → écart auto-trigger
- Hook workflow gate mais doctrine 22 mai interdit → écart doctrinal

Pas d'opinion. Que des **écarts mesurables**.

## D. Plan basé sur écarts

Liste des écarts à fixer, priorisés. Pas d'écart = pas de fix. Présenter à Raphael AVANT exécution.

## E. Exécuter + capitaliser

Via agents spécialisés ou Edit/Write. Capitaliser :
- Erreur → `Knowledge/erreurs/<nom>.md`
- Raisonnement multi-étapes → `/reasoning-cache`
- Décision majeure → devils-advocate → `Knowledge/critiques/`

## Anti-patterns

- ❌ Skipper A = "code that solves the wrong problem" (Anthropic)
- ❌ Lire canoniques avant analyser = biais de perception
- ❌ `search_brain` seul = audit sur mémoire session, pas source vérité (cf [[feedback_lire_canoniques_avant_audit]])
- ❌ Édit direct au lieu de déléguer aux agents spécialisés (delegate-guard bloque)

## Exemple — "Optimise la skill /xxx"

A. Lire SKILL.md EN ENTIER + scripts/ + references/
B. `read_note("comment-creer-skill")` + `read_note("mcp-vs-skills-doctrine")` SANS max_lines
C. Écarts : description > 250 chars ? body > 500L ? skill orpheline ? hors 9 catégories Thariq ?
D. Plan priorisé par impact
E. Modifier via `skill-creator` (re-applique séquence)

## Référence

Source canonique : [[methode-analyser-repo]] section ORDRE CANONIQUE. Pivot doctrinal : [[raisonnement-22mai-doctrine-vs-enforcement]]. Méthode soeur post-pivot : [[methode-pivoter-doctrine]].
