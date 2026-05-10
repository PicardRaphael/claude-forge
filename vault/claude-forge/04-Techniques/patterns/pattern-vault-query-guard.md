---
titre: "Pattern Vault Query Guard — Agents DOIVENT consulter le vault avant d'ecrire"
resume: "Hook deterministe + Etape 0 dans chaque agent : forge-brain obligatoire avant tout Write sur vault/output/skills/agents. Pas de bypass specialiste."
aliases:
  - "vault query guard"
  - "vault query before create"
  - "etape 0 vault"
  - "hook vault obligatoire"
  - "forge-brain obligatoire agents"
  - "vault write guard pattern"
domaine: claude-code
type: technique
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "[[erreur-skip-checklist-skill-modification]]"
  - "[[Best practices Boris Thariq]]"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/neoteem"
---

# Pattern Vault Query Guard

## Description

Hook deterministe + Etape 0 dans chaque agent : forge-brain obligatoire avant tout Write sur vault/output/skills/agents. Pas de bypass specialiste.

## Quand utiliser

Sur tout projet utilisant le vault forge-brain avec des agents qui creent/modifient des fichiers. Empeche les agents de sauter la consultation du vault avant d'ecrire.

## Probleme

Les rules advisory ("toujours consulter le vault") sont ignorees sous pression conversationnelle. L'utilisateur a des idees, le flow est rapide, les verifications sautent. Documente 3+ fois comme erreur recurrente.

## Solution : hook deterministe + Etape 0 agent

### 1. Hook vault-query-tracker.py (PostToolUse)

Detecte quand Read/Grep/Glob/Skill cible le vault ou la memoire. Ecrit un marqueur timestamp.

Paths detectes : vault/, memory/, Knowledge/, forge-brain, 04-Techniques/, 07-Prompts/
Skills detectees : forge-brain, neo-brain

### 2. Hook vault-query-guard.py (PreToolUse — Write)

Bloque tout Write sur les chemins proteges si le marqueur est absent ou expire (60 min).

Chemins proteges : vault/, output/, .claude/skills/, .claude/agents/

**PAS DE BYPASS SPECIALISTE.** Tous les agents sont soumis au guard, y compris skill-creator, agent-creator, etc.

### 3. Etape 0 dans chaque agent

Chaque agent a une section standardisee :

```markdown
## Etape 0 — Verifier le vault (OBLIGATOIRE — hook bloquant)

Utiliser la skill forge-brain pour chercher :
1. Knowledge/erreurs/ — erreurs passees
2. 04-Techniques/ — best practices

Si le prompt contient deja des infos du vault → le tracker a deja pose le marqueur.
```

### 4. Skill forge-brain dans tous les agents

Tous les agents ont `forge-brain` dans leur liste `skills:`. L'invocation de la skill declenche le tracker.

## Flow complet

```
Agent demarre
  → Etape 0 : invoque forge-brain (skill)
  → Tracker detecte l'appel → pose le marqueur
  → Agent travaille, fait des Write
  → Guard verifie : marqueur frais ? → OK, Write passe
```

Si l'agent oublie l'Etape 0 :
```
Agent demarre
  → Saute Etape 0
  → Essaie un Write sur output/
  → Guard : marqueur absent → BLOQUE (exit 2)
  → Agent lit le message d'erreur → query le vault → retry
```

## Agents concernes (8)

skill-creator, agent-creator, hook-creator, claudemd-optimizer, project-analyzer, project-auditor, python-dev, self-updater

## Exemple

Etape 0 dans un agent :

```markdown
## Etape 0 — Verifier le vault (OBLIGATOIRE — hook bloquant)

Utiliser la skill forge-brain pour chercher :
1. Knowledge/erreurs/ — erreurs passees
2. 04-Techniques/ — best practices
```

## Liens

- [[MOC-Techniques]]
- [[erreur-edit-direct-skills]]
- [[best-practices-claude-code-leaders]]
