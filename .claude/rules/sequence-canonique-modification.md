# Séquence canonique pour TOUTE création/modification/OPTIMISATION de composant — OBLIGATOIRE

Quand tu :
- **Analyses** un repo (project-auditor, project-analyzer, cc-advisor)
- **Crées** un skill / agent / hook / CLAUDE.md / rule
- **Modifies** ou **OPTIMISES** un composant existant (skill-evolve, evolve, skill-creator quand il modifie, etc.)

tu DOIS suivre cette séquence dans l'ordre. **Pas d'exception** — y compris pour "juste" optimiser une skill existante.

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

## A. Analyser le RÉEL — selon le scope

**Avant toute prescription**, observer les faits bruts. Le scope d'observation dépend du type de tâche.

### Pour analyse REPO entier
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

### Pour optimisation d'un COMPOSANT EXISTANT (skill / agent / hook)
- Lire le composant EN ENTIER (SKILL.md / agent.md / hook script)
- Lire les `references/` et `scripts/` associés si présents
- Vérifier si la skill est référencée dans le body d'agents (`grep -r "skill-name" .claude/`)
- Vérifier l'usage récent (`git log --oneline -20 -- .claude/skills/<nom>/`)
- Mesurer : nombre de lignes, longueur description frontmatter, taille references/

### Pour modification de CLAUDE.md / rule
- Lire le fichier EN ENTIER
- Lister les composants qui le référencent (`grep -r "<rule-name>" .claude/`)
- Vérifier que la modif ne casse pas les dépendances

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

### Création
- `agent-creator` : créer un nouvel agent
- `skill-creator` : créer une nouvelle skill
- `hook-creator` : créer un nouveau hook
- `claudemd-optimizer` : créer / refaire un CLAUDE.md

### Modification / Optimisation (même séquence !)
- `skill-creator` quand on l'invoque pour MODIFIER une skill existante
- `agent-creator` quand on l'invoque pour MODIFIER un agent existant
- `hook-creator` quand on l'invoque pour MODIFIER un hook existant
- `claudemd-optimizer` pour optimiser un CLAUDE.md existant
- `skill-evolve` : analyser et proposer optims d'une skill existante
- `evolve` : analyser un projet et proposer des évolutions

### Analyse
- `project-analyzer` : "j'ai un projet X / URL GitHub"
- `project-auditor` : audit `.claude/` d'un repo
- `cc-advisor` : besoin flou / "comment automatiser X"
- `spec` : transformer un ticket en spec structurée
- `analyze-project` : analyse projet

### Session principale
- Quand l'utilisateur dit : "analyse mon repo", "propose config CC", "optimise cette skill", "améliore cet agent", "crée un hook pour X"

## Exemples concrets — séquence par cas d'usage

### Cas 1 — "Optimise la skill /xxx"
A. Lire `.claude/skills/xxx/SKILL.md` EN ENTIER + scripts/ + references/
B. `read_note("comment-creer-skill")` + `read_note("mcp-vs-skills-doctrine")` + `read_note("methode-analyser-repo")` SANS max_lines
C. Écarts : description > 250 chars ? body > 500L ? scripts orphelins ? skill orpheline (pas référencée dans agents) ? pas dans 9 catégories Thariq ?
D. Plan d'optim priorisé par impact
E. Modifier via `skill-creator` (qui re-applique la séquence)

### Cas 2 — "Améliore cet agent"
A. Lire `.claude/agents/xxx.md` EN ENTIER
B. `read_note("comment-creer-agent")` + `read_note("workflow-claude-code-optimal")` SANS max_lines
C. Écarts : `permissionMode` manquant ? `memory: project` manquant ? Skills dans frontmatter pas référencées dans body ? Description en 1ère personne ?
D. Plan d'optim
E. Modifier via `agent-creator`

### Cas 3 — "Crée un hook pour X"
A. Vérifier les hooks existants (`.claude/hooks/` + `.claude/settings.json`)
B. `read_note("comment-creer-hook")` + `read_note("raisonnement-22mai-doctrine-vs-enforcement")` SANS max_lines
C. La règle est-elle 100% (hook) ou advisory (skill/rule) ? Lint/security/scope (OK) ou workflow (anti-pattern) ?
D. Plan
E. Créer via `hook-creator`

## Référence

Source canonique : [[methode-analyser-repo]] section "ORDRE CANONIQUE — A → B → C → D → E".
Pivot doctrinal qui valide cette séquence : [[raisonnement-22mai-doctrine-vs-enforcement]].
