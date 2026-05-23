# Séquence canonique pour TOUTE création/modification de composant — OBLIGATOIRE

Quand tu analyses un repo, proposes ou crées/modifies un **skill / agent / hook / CLAUDE.md / rule**, tu DOIS suivre cette séquence dans l'ordre. Pas d'exception.

## Séquence A → B → C → D → E

```
A. ANALYSER le RÉEL (faits bruts du repo, sans biais canonique)
        ↓
B. LIRE canoniques EN ENTIER (read_note via MCP forge-brain, pas search_brain extraits)
        ↓
C. CROISER analyse ⨯ canoniques → écarts mesurables
        ↓
D. PLAN basé sur écarts (pas sur idéologie)
        ↓
E. EXÉCUTER après validation utilisateur
```

Source canonique vault : [[methode-analyser-repo]] section **ORDRE CANONIQUE**.

## A. Analyser le RÉEL du repo

**Avant toute prescription**, observer les faits bruts :
- Stack (langages, versions, framework, DB)
- Structure (mono-repo / microservices / workspaces)
- `.claude/` existant (skills, agents, hooks, rules, CLAUDE.md)
- Tests / CI / build
- Patterns récurrents dans le code

Outils :
- `Glob '**/*'` pour topologie
- `Read package.json / pyproject.toml / Cargo.toml`
- `Read README.md`
- `git log --oneline -50`

**Verbatim Anthropic** : *"Explore: Read the codebase and understand existing implementation patterns... This phase is critical because it prevents Claude from making assumptions about your architecture."*

## B. Lire canoniques EN ENTIER via MCP forge-brain

**Outils obligatoires** :
- `mcp__forge-brain__read_note(file="...")` SANS `max_lines` (ou `max_lines: 500+`)
- JAMAIS `search_brain` seul (extraits ~10 lignes = insuffisant pour audit/création)

| Tâche | Notes canoniques à lire EN ENTIER |
|-------|-----------------------------------|
| Créer/modifier agent | [[comment-creer-agent]] + [[workflow-claude-code-optimal]] |
| Créer/modifier skill | [[comment-creer-skill]] + [[mcp-vs-skills-doctrine]] |
| Créer/modifier hook | [[comment-creer-hook]] + [[raisonnement-22mai-doctrine-vs-enforcement]] |
| Optimiser CLAUDE.md | [[comment-ecrire-claudemd]] + [[pattern-vault-llm-karpathy]] |
| Auditer / analyser repo | TOUTES ci-dessus + [[methode-analyser-repo]] |

Plus : chercher dans `Knowledge/erreurs/`, `Knowledge/critiques/`, `Knowledge/raisonnements/` pour le contexte spécifique.

## C. Croiser analyse ⨯ canoniques → écarts mesurables

Mettre côte-à-côte FAITS observés (A) et RÈGLES canoniques (B). Lister les ÉCARTS :
- Agent X = Opus mais canonique dit Sonnet → écart Sonnet/Opus split
- Skill Y = 800L mais canonique dit < 500L → écart taille
- Hook Z = workflow gate mais doctrine 22 mai interdit → écart doctrinal
- Description skill > 250 chars → écart auto-trigger

Pas d'opinion, pas d'idéologie. Que des **écarts mesurables**.

## D. Plan basé sur les ÉCARTS

Plan = liste des écarts à fixer, priorisés. Si pas d'écart sur un point → pas de fix.

Présenter le plan à Raphael **AVANT exécution**. Pas d'application aveugle de canonique.

## E. Exécuter après validation

Exécution via agents spécialisés ou Edit/Write selon contexte. Capitaliser apprentissages :
- Erreur observée → `Knowledge/erreurs/<nom>.md`
- Raisonnement multi-étapes → `Knowledge/raisonnements/<nom>.md` via `/reasoning-cache`
- Décision majeure → `Knowledge/critiques/<nom>.md` via devils-advocate

## Anti-patterns documentés

- ❌ **Skipper A** = "code that solves the wrong problem" (Anthropic docs)
- ❌ **Lire canoniques avant analyser** = biais de perception (ATAM/SAAM existent pour ça)
- ❌ **`search_brain` seul** = audit basé sur mémoire session, pas source de vérité ([[feedback_lire_canoniques_avant_audit]])
- ❌ **Prescrire sans observer** = config ad-hoc, pas adaptée
- ❌ **Édit direct** au lieu de déléguer aux agents spécialisés (skill-creator, agent-creator, hook-creator, claudemd-optimizer)

## Composants concernés (doivent appliquer cette séquence)

- **Agents créateurs** : `agent-creator`, `skill-creator`, `hook-creator`, `claudemd-optimizer`
- **Agents analystes** : `project-analyzer`, `project-auditor`
- **Skills d'analyse/modification** : `analyze-project`, `cc-advisor`, `evolve`, `skill-evolve`, `spec`
- **Session principale** : quand l'utilisateur dit "analyse mon repo / propose-moi config CC"

## Référence

Source canonique : [[methode-analyser-repo]] section "ORDRE CANONIQUE — A → B → C → D → E".
Pivot doctrinal qui valide cette séquence : [[raisonnement-22mai-doctrine-vs-enforcement]].
