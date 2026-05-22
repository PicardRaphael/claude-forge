---
titre: "Pattern audit complet .claude/ d'un repo — 4 auditeurs parallèles + vérif empirique"
type: technique
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - audit claude folder pattern
  - audit .claude/ méthode
  - 4 project-auditor parallèles
  - audit repo claude-code complet
  - pattern audit conformité .claude/
resume: "Méthode validée pour auditer le .claude/ d'un repo : 4 project-auditor en parallèle (agents/skills/hooks/rules+CLAUDE.md), checklist explicite par auditeur, vérification empirique des claims douteux, consolidation + DA, application des fix par vagues via agents spécialisés. Testé sur neo_ia (72 composants, 26 fix) et ia_back (74 composants, 30+ fix) le 22 mai 2026."
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#pattern/audit"
sources:
  - "[[Boris Cherny]]"
  - "[[best-practices-claude-code-leaders]]"
  - "[[feedback_audit_repo_method]]"
---

# Pattern Audit Complet .claude/

## Quand utiliser

- Le user demande "audite mon repo" / "vérifie .claude/" / "le PARFAIT"
- Repo avec 50+ composants `.claude/` (agents + skills + hooks + rules)
- Suspicion de drift après migration stack/refonte majeure
- Maintenance trimestrielle

## Volumétrie typique

| Repo | Agents | Skills | Hooks | Rules | CLAUDE.md | Total |
|------|--------|--------|-------|-------|-----------|-------|
| neo_ia | 12 | 25 | 14 | 17 | 4 | 72 |
| ia_back | 16 | 27 | 14 | 16 | 1 | 74 |
| forge | 11 | 34 | ~20 | ~25 | 1 | 91 |

## Méthode

### Phase 0 — Orientation (5 min)

```bash
ls .claude/agents/*.md | wc -l
ls -d .claude/skills/*/ | wc -l
ls .claude/hooks/ | wc -l
ls .claude/rules/ | wc -l
find . -name CLAUDE.md -not -path "*/node_modules/*"
```

Identifier signaux pré-audit :
- Compteurs CLAUDE.md vs filesystem
- Fichiers suspects (`.test.md` dans hooks/, paths Windows mal échappés)
- Sédiments (`.architect-marker`, `.tdd-bypass`)
- Stack du repo (TS/Python/Go)

### Phase 1 — 4 auditeurs en parallèle

**JAMAIS Explore** (read-only mais pas conçu pour conformité). **JAMAIS general-purpose** (dilue). **JAMAIS 1 seul** (tronque).

Lancer 4 `project-auditor` avec `run_in_background: true` :

1. **Agents** — Frontmatter (permissionMode, memory, effort, color) + body + cross-check code
2. **Skills** — Frontmatter + body + structure references/ + doublons
3. **Hooks + settings.json** — Stack same-stack, pipeline markers complet, matcher MultiEdit, orphelins
4. **Rules + CLAUDE.md** — Frontmatter description obligatoire, compteurs cohérents, sweet spot <150L

Checklist par auditeur : voir [[boris-thariq-bestpractices]] pour les standards.

### Phase 2 — Vérification empirique des claims (CRITIQUE)

Les project-auditor produisent des **faux positifs récurrents** :

| Claim auditeur | Vérif | Source |
|----------------|-------|--------|
| Skill "inexistante" | `grep <skill> ~/.claude/plugins/installed_plugins.json` | Plugin scope user actif partout |
| "`allowed-tools` obligatoire" | docs Anthropic | FAUX — optionnel |
| "`skills:` invalide SKILL.md" | docs Anthropic | Subagent-only mais ignoré silencieusement |
| "Agent X inexistant" | Vérifier scope repo (ia_back vs neo_ia) | Spec-specific |

Si doute → WebSearch `code.claude.com/docs/skills`.

### Phase 3 — Consolidation rapport

Format markdown structuré :
```
# AUDIT <repo> — Rapport consolidé
## 🔴 BLOQUANTS (corrections obligatoires)
## 🟠 DÉRIVES (à corriger)
## 🟡 OPTIMISATIONS
## ✅ CONFORME (à garder)
## SCORE GLOBAL : X/Y PARFAITS
```

Sauvegarder dans `claude-forge/output/audit-<repo>-YYYY-MM-DD.md`.

### Phase 4 — Devil's Advocate (optionnel mais recommandé)

Lancer `devils-advocate` sur le rapport. ATTENTION : DA peut planter sur PowerShell heredoc (bug récurrent Windows). Si DA planté, vérifier manuellement les angles morts.

**Manques fréquents auditeurs** (à challenger manuellement) :
- Fichiers racine repo (`.mcp.json*`, `conftest.py`, `coverage_final.json`)
- Worktrees + agent-memory
- Plugins scope project vs user

### Phase 5 — Application des fix par vagues

**3 vagues recommandées :**

- **Vague 1 — Bloquants doctrine** (rapide, zéro risque) : compteurs CLAUDE.md, description test-writer alignée, effort xhigh→high, matcher MultiEdit ajouté
- **Vague 2 — Bloquants structurels** : renaming rules, fix skills bloquantes, nettoyage sédiments
- **Vague 3 — Dérives + optimisations** : renaming naming anti-patterns, dédup, CLAUDE.md <120L, gotchas vides

Lancer en parallèle dans chaque vague (agents indépendants). Utiliser les agents spécialisés :
- `claudemd-optimizer` pour CLAUDE.md + rules
- `agent-creator` pour agents/*.md
- `skill-creator` pour skills/*/SKILL.md
- `hook-creator` pour hooks/* + settings.json

### Phase 6 — Vérification empirique post-fix

**TOUJOURS** vérifier ce que les sub-agents ont **vraiment** fait (feedback `audit-claims-after-brief`) :

```bash
grep -n "18 rules" CLAUDE.md  # compteur
ls .claude/rules/ | wc -l     # vs filesystem
grep "MultiEdit" .claude/settings.json | wc -l  # tous les guards
grep -rl "Drizzle" .claude/  # zéro si purge faite
```

### Phase 7 — Commit isolé

⚠️ **IMPORTANT** : Stage UNIQUEMENT les fichiers de l'audit. Ne pas mixer avec chantiers en cours (ex code applicatif).

```bash
git add CLAUDE.md .claude/agents/* .claude/skills/*/SKILL.md \
        .claude/hooks/* .claude/rules/* .claude/settings.json
git commit -m "chore(claude): audit complet .claude/ + N fix en 3 vagues..."
git push
```

## Gotchas (highest-signal)

- **Matcher `Write|Edit` sans MultiEdit** = trou architectural (voir [[multiedit-matcher-blind-spot-hooks]])
- **Stack drift** : code migré ≠ prompts migrés. Grep stack OLD vs NEW (Drizzle→postgres.js sur ia_back : 17 fichiers contaminés découverts)
- **Decisions cross-repo** : pas de propagation automatique. Renaming neo_ia 22 mai (cto-mindset, outcomes-after-architect) à refaire sur ia_back
- **`allowed-tools: Agent` dans skill** = INVALIDE. Utiliser `Task` pour invoquer subagent
- **Plugin scope user** (ex `neoteem-brain-dev-ia@neoteem`) actif partout — pas un faux phantôme
- **Sédiments .tdd-bypass / .architect-marker** à la racine repo = `pipeline-reset` pas tourné
- **DA bug Windows PowerShell heredoc** : si DA planté, sa critique vault peut être tronquée (que le frontmatter). Le titre du frontmatter contient parfois le verdict utile
- **Description = routing CC** : si elle ment, dispatch cassé même si le body est correct (cas test-writer phase=refactor)

## Apprentissage (méta sur le pattern lui-même)

- **Règle** : Toujours présenter le rapport AVANT d'appliquer les fix (feedback `present-before-build`)
  - **Why** : Raphael tranche les zones grises (agents à créer ou retirer, plugins à installer)
  - **How to apply** : Phase 4 → AskUserQuestion avec options claires, ensuite Phase 5

- **Règle** : Test comportemental PASS/FAIL en session fraîche après audit massif (feedback `behavioral-test-after-setup`)
  - **Why** : Audit statique = 95% confiance, comportemental = 100%
  - **How to apply** : Après commit, générer un prompt qui teste 3-5 patterns critiques (dispatch test-writer, hook MultiEdit, etc.)

## Liens

- [[boris-thariq-bestpractices]] — Standards Anthropic
- [[feedback_audit_repo_method]] — Mémoire forge méthode
- [[feedback_auditor_false_positives]] — Vérif empirique claims
- [[feedback_multiedit_matcher_blind_spot]] — Gotcha matcher
- [[feedback_drizzle_postgresjs_drift]] — Pattern stack drift
- [[feedback_propagate_decisions_cross_repo]] — Propagation cross-repo
- [[pattern-vault-query-guard]] — Hook deterministe pattern (variante enforcement)
