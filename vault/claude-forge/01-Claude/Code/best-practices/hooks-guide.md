---
titre: "Guide complet des Hooks Claude Code"
resume: "Guide de reference des hooks Claude Code — 25+ events lifecycle, enforcement exit 2, pattern marker+guard pour prerequis deterministes"
aliases: ["hooks guide", "guide hooks CC", "hooks claude code", "hooks best practices", "hooks events", "hook exit 2", "hook marker guard", "hooks enforcement pattern", "hooks self-improving", "hooks settings.json format", "hookSpecificOutput", "PreToolUse PostToolUse hooks"]
  - "hooks guide"
  - "guide hooks CC"
  - "hooks claude code"
  - "hooks reference"
  - "exit 2 pattern"
  - "marker guard pattern"
domaine: claude-code
type: technique
derniere-maj: 2026-05-14
auteur: claude
sources:
  - "https://code.claude.com/docs/en/hooks"
  - "https://code.claude.com/docs/en/best-practices"
  - "https://howborisusesclaudecode.com"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/hooks"
---
## Principe fondamental

> **Hooks = deterministe (100%). CLAUDE.md = advisory.**

Boris Cherny : les instructions CLAUDE.md sont suivies la plupart du temps mais pas toujours. Si une regle DOIT etre appliquee 100% du temps, elle DOIT etre un hook.

## Events (25+)

| Categorie | Events |
|-----------|--------|
| Per-session | `SessionStart`, `SessionEnd`, `Setup` |
| Per-turn | `UserPromptSubmit`, `Stop`, `StopFailure` |
| Per-tool | `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`, `PostToolBatch` |
| Worktree | `WorktreeCreate`, `WorktreeRemove` |
| Agent | `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted` |
| Context | `PreCompact`, `PostCompact`, `InstructionsLoaded`, `CwdChanged`, `FileChanged` |
| Other | `Notification`, `ConfigChange`, `Elicitation`, `ElicitationResult`, `UserPromptExpansion` |

## 5 types de handlers

`command`, `http`, `mcp_tool`, `prompt`, `agent`

## Exit code 2 — enforcement

| Event | Effet exit 2 |
|-------|--------------|
| `PreToolUse` | **Bloque l'appel d'outil** — Claude recoit stderr comme feedback |
| `PermissionRequest` | Refuse la permission |
| `UserPromptSubmit` | Bloque et efface le prompt |
| `Stop`, `SubagentStop` | Empeche l'arret |
| `PostToolUse` | Ne peut PAS annuler (deja execute), mais ajoute du contexte |

Exit 1 = erreur non-bloquante (continue). Exit 2 = erreur bloquante.

## Pattern Marker + Guard (prouve en production)

Architecture de forge pour l'enforcement :

```
PostToolUse (tracker) : detecte l'action prerequise → ecrit un marker file
PreToolUse (guard) : detecte l'action protegee → verifie le marker → bloque (exit 2) si absent
```

Deploye 3 fois dans forge : `vault-query-guard`, `delegate-guard`, `architect-guard + commit-guard`.

## hookSpecificOutput (avance)

Les hooks PreToolUse peuvent aller au-dela de bloquer/autoriser :

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "Raison",
    "updatedInput": { "champ_modifie": "valeur" },
    "additionalContext": "Contexte pour Claude"
  }
}
```

Permet de modifier les inputs d'outils et d'injecter du contexte — plus riche que le simple exit 2.

## Patterns pratiques

### Auto-formatting (Boris)

PostToolUse hook qui formate le code apres chaque Write/Edit. Claude formate correctement ~90% du temps, le hook gere les 10% restants.

### Verification a l'arret (Agent Stop hook)

Boris : "Pour les taches longues, j'utilise un agent Stop hook pour verifier le travail de maniere deterministe." Exit 2 = la tache n'est pas marquee complete, stderr = feedback.

### Skill Activation Hook (pattern nouveau)

Un hook `UserPromptSubmit` ou `NotificationPostMessage` qui detecte les prompts et **ajoute des recommandations de skills** avant que Claude ne les voie. Claude ne peut pas oublier car il n'a jamais eu a se souvenir.

### asyncRewake

`"asyncRewake": true` — reveille Claude quand un hook background exit 2, montre stderr comme system reminder.

## Quand utiliser quoi

| Besoin | Solution |
|--------|----------|
| Guideline de style | CLAUDE.md (advisory) |
| Regle critique (jamais push main) | Hook PreToolUse exit 2 |
| Verification de sortie | Hook Stop exit 2 |
| Formatage automatique | Hook PostToolUse |
| Prerequis avant action | Pattern Marker + Guard |
| Workflow multi-etapes | Skill avec hooks inline |

## Gotchas

- Exit 2 sur SessionStart/Setup/Notification = impossible (ces events ne sont pas bloquables)
- Les hooks inline dans les skills ne s'activent que quand la skill est appelee
- `disableAllHooks` dans managed-settings override tout
- Timeout defaut = 60s. Au-dela, le hook est tue silencieusement
- Chemins Python dans settings.json doivent etre portables (`python` via PATH, pas de chemin absolu)

## Liens

- [[skills-guide]] — Hooks inline dans les skills
- [[harness-engineering]] — Hooks = couche enforcement du harness
- [[claudemd-guide]] — Quand les rules ne suffisent pas → hooks
- [[erreur-advisory-rules-insuffisantes]] — 3 incidents ou les rules ont ete ignorees
- [[erreur-settings-paths-hardcodes-multi-poste]] — Portabilite des hooks

## Self-improving hooks (pattern Anthropic, mai 2026)

> "Most teams think of hooks as scripts that prevent Claude from doing something wrong, but their more valuable use is continuous improvement." — Anthropic blog "Claude Code at scale" (14 mai 2026)

Le rôle le plus sous-exploité des hooks : **ne pas bloquer, mais améliorer le setup en continu**.

### Stop hook qui propose des updates CLAUDE.md

À la fin d'une session, un hook `Stop` analyse ce qui s'est passé et propose des additions au CLAUDE.md (gotchas découverts, patterns récurrents, erreurs évitables). Le contexte est encore frais → la qualité des suggestions est bien supérieure à une review post-hoc.

**Implémentation type :**

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python .claude/hooks/learning-reminder.py"
        }
      ]
    }
  ]
}
```

Le script lit le transcript, identifie les apprentissages, propose des updates en stderr (ou écrit directement un brouillon dans `.claude/CLAUDE-suggestions.md`).

→ Pattern déployé dans forge (`learning-reminder.py`).

### SessionStart qui charge le contexte dynamique

> "A start hook can load team-specific context dynamically so every developer gets the right setup for their module without manual configuration."

Au lieu d'un CLAUDE.md statique qui charge TOUT pour tout le monde, un hook `SessionStart` détecte le dossier courant (ou le ticket Jira lié, ou la branche git) et charge **uniquement** le contexte pertinent. Évite la pollution du contexte.

**Cas d'usage :**
- Dev qui ouvre `apps/payments/` → charge `payments-conventions.md` seul
- Dev qui ouvre `infra/` → charge `infra-runbook.md` seul
- Dev sur la branche `feature/XYZ` → charge le ticket Jira XYZ via MCP

### Enforcement de linting/formatting (rappel)

Plus consistent que de demander à Claude de se souvenir d'une instruction.

> "For automated checks like linting and formatting, hooks enforce the rules deterministically and produce more consistent results than relying on Claude to remember an instruction."

### Trois rôles des hooks (à connaître)

| Rôle | Event | Exemple |
|------|-------|---------|
| **Garde-fou** (bloquer le mauvais) | `PreToolUse` exit 2 | delegate-guard, commit-guard |
| **Enforcement** (faire à coup sûr) | `PostToolUse` | auto-format, lint, tests |
| **Self-improvement** (capitaliser) | `Stop`, `SessionEnd` | learning-reminder, CLAUDE.md proposer |

→ Les teams qui ne pensent qu'au premier rôle laissent la moitié de la valeur sur la table.


## Anti-pattern critique — Workflow enforcement (mise à jour 22 mai 2026)

**Ne JAMAIS utiliser un hook pour forcer un workflow agentique** (architect-first, code-reviewer-before-commit, dispatch-to-dev).

Hooks = lint, test, security, observabilité, scope (doctrine Anthropic 2026).
Doctrine = CLAUDE.md / rules — la session principale juge.

Pattern observé et corrigé le 22 mai 2026 sur ia_back + neo_ia :
- `architect-guard` (force architect avant Write/Edit) → SUPPRIMÉ
- `commit-guard` (force code-reviewer marker avant commit) → SUPPRIMÉ
- `dispatch-guard` (bloque session principale d'écrire dans src/) → SUPPRIMÉ
- `marker-protect`, `agent-marker-writer`, `pipeline-reset`, `session-reset-markers` → SUPPRIMÉS

Sources doctrine :
- Boris Cherny : "thinnest wrapper", "complex scaffolding rendered obsolete by next model"
- Anthropic Agent SDK : "Claude decides when to invoke subagents"
- Hooks reference : exemples = rm -rf, force-push, secret leak, lint blocant

Symptôme avant refonte : friction 6× sur le dev d'une feature. Voir [[raisonnement-22mai-doctrine-vs-enforcement]] et [[erreur-hooks-workflow-enforcement]] (à créer).
