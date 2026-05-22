---
titre: "Auto-mode Classifier Claude Code"
resume: "Classifier Anthropic qui filtre les tool calls en mode auto : bloque scope escalation, self-modification, destructif. Bypass via permissions.allow"
aliases:
  - "auto mode classifier"
  - "classifier claude code"
  - "permission denied auto mode"
  - "claude code safety classifier"
  - "auto mode safety"
  - "classifier haiku claude"
domaine: claude-code
type: feature
derniere-maj: 2026-05-18
auteur: claude
sources:
  - "Découvert lors de session 2026-05-18 (commit/push cross-repo bloqué)"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
---

## Qu'est-ce que c'est

Petit modèle (probablement Claude Haiku) intégré au harness Claude Code par Anthropic. Filtre chaque tool call quand Claude tourne **en mode auto** (no-ask, acceptEdits, bypassPermissions).

C'est le remplaçant automatique de l'approbation utilisateur quand on lance Claude en non-interactif.

## Quand il tourne

| Mode | Classifier | Validation |
|------|------------|------------|
| Interactif (default) | OFF | Utilisateur valide chaque action |
| Auto / no-ask | ON | Classifier décide |
| acceptEdits | ON | Classifier décide |
| bypassPermissions | ON | Classifier décide |

## Les 3 axes bloquants

### 1. Scope escalation
Sortir du repo de départ de la session. Exemples bloqués :
- `cd C:/autre-repo && git push` quand la session a démarré dans claude-forge
- Édit d'un fichier dans un repo sibling sans permission explicite

### 2. Self-modification
L'agent modifie sa propre config pour bypasser les contrôles. Exemples bloqués :
- Édit de `.claude/settings.json` pour ajouter `Bash(*)`
- Modification des hooks pour les désactiver
- Édit des permissions allow/deny

### 3. Destructif
Actions non réversibles sans permission explicite :
- `rm -rf`
- `git push --force` sur main/master
- `drop table`, `truncate`
- `git reset --hard origin/...`

## Bypass propre

Ajouter une rule explicite dans `permissions.allow` de `.claude/settings.json` :

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(cd C:/Users/.../autre-repo && git *)",
      "Bash(git -C C:/Users/.../autre-repo *)"
    ]
  }
}
```

Le classifier respecte les `allow` rules et ne juge plus.

## Ce qu'il ne fait PAS

- Ne lit pas le code (pas d'analyse sémantique)
- Ne juge pas la qualité
- Ne bloque pas Read/Grep/Glob (lecture seule = toujours safe)
- Ne s'applique pas aux subagents avec leur propre `permissionMode` dans YAML

## Différence avec les hooks

| Mécanisme | Quand | Pourquoi |
|-----------|-------|----------|
| **Hooks PreToolUse** | Toujours (auto + interactif) | Logique custom Python, exit 2 = block |
| **Classifier** | Mode auto uniquement | Filet de sécurité Anthropic |
| **Permissions allow/deny** | Toujours | Configuration statique |

Les 3 se cumulent. Un tool call passe = autorisé par les 3.

## Gotcha

**Le classifier ne peut pas être désactivé**. Si tu lances en mode auto et qu'il bloque, les seules options sont :
1. Ajouter une permission allow dans settings.json (manuellement, l'agent ne peut pas)
2. Sortir du mode auto
3. Reformuler la commande pour qu'elle reste dans le scope

## Liens

- [[Claude Security]]
- [[delegate-guard-pattern]]
- [[comment-creer-hook]]
- [[MOC-Claude-Code]]
