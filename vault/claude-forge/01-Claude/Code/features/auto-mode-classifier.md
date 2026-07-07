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

## Hard block — tous les vecteurs settings.json

**Confirmé 2026-05-22** : le classifier bloque TOUS les vecteurs de modification de `.claude/settings.json` du repo courant, même indirects :
- `Write` direct · `Edit` · `cp settings.json.proposed settings.json` (Bash) · `cat .proposed > settings.json` (heredoc redirect)

**Pattern recommandé** : générer `.claude/settings.json.proposed` avec le fichier COMPLET (jamais un extrait — un `.proposed` partiel appliqué en remplacement total perd les sections `permissions`/`enabledPlugins` etc.) + instruction explicite à Raphael d'appliquer manuellement.

**Distinction project vs user-scope** : le hard block est project-scope du repo courant. `~/.claude/settings.json` (user-scope) passe sans blocage depuis n'importe quelle session. `.claude/settings.json` d'un *autre* repo passe aussi — sauf si le changement touche l'invocation de hooks de sécurité (le blocage dépend du CONTENU perçu, pas seulement du scope). Cf [[self-modification-user-scope-passe]].

## Hard block étendu aux hooks de sécurité `.py`

**Confirmé 2026-06-07** : le verdict self-modification ne se limite pas à `settings.json`. Le classifier bloque aussi l'`Edit` autonome d'un **hook de sécurité** (`.claude/hooks/*-guard.py`) — même pour une correction de texte pure (docstring, message stderr), zéro changement de logique.

**Le classifier juge l'INTENTION perçue, pas la lettre du brief.** Verdict observé : *"the user's task never authorized changing THIS SPECIFIC hook"* — alors que le brief nommait explicitement le hook concerné. Un hook sécu voisin = « non autorisé » indépendamment du brief textuel.

**Workarounds** : Raphael lève le mode (Shift+Tab) → les `Edit` passent immédiatement, puis l'agent rejoue. OU `.proposed` + renommage manuel. JAMAIS contourner (cf [[delegate-guard-pattern]]).

Distinct scope project/user : [[self-modification-user-scope-passe]] (settings.json user-scope passe) ne s'étend PAS aux hooks sécu — un hook du repo courant est bloqué quel que soit le scope.

## Windows — bug antislash dans settings.json (hooks)

**Confirmé 2026-05-22** : dans `settings.json`, ne JAMAIS utiliser de chemin Windows avec antislashes échappés (`"C:\\\\Users\\\\..."`) pour les `command` de hooks. Bash Git Bash mange les antislashes → chemin cassé (`C:Usersraphael...python.exe: command not found`).

**Solution cross-machine** : `py` (Python launcher Windows PEP 514). Pas de chemin en dur, pas de username.

```json
"command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/X.py\""
```

Sur macOS/Linux : `python3` ou shebang + chmod +x (py n'existe pas). Cf [[windows-hooks-doctrine]].

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
