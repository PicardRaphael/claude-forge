---
name: cc-hooks-ref
description: ALWAYS load this reference when creating or modifying a Claude Code hook. Covers 29 events, 5 handler types, hookSpecificOutput, asyncRewake, settings.json format, Python scripts, exit 2 blocking, inline hooks. Do NOT create hooks without loading this first.
user-invokable: false
---

# Référence — Hooks Claude Code

## 29 événements

| Événement               | Bloque               |
| ----------------------- | -------------------- |
| `PreToolUse`            | ✅ exit 2            |
| `PostToolUse`           | ❌                   |
| `PostToolUseFailure`    | ❌                   |
| `Stop`                  | ✅ JSON block        |
| `SubagentStart/Stop`    | ✅ Stop = JSON block |
| `SessionStart/End`      | ❌                   |
| `UserPromptSubmit`      | ❌                   |
| `PermissionRequest`     | ✅                   |
| `PermissionDenied`      | ❌                   |
| `Notification`          | ❌                   |
| `PreCompact`            | ❌                   |
| `Setup`                 | ❌                   |
| `TeammateIdle`          | ❌                   |
| `TaskCompleted`         | ❌                   |
| `ConfigChange`          | ❌                   |
| `WorktreeCreate/Remove` | ❌                   |
| `PostCompact`           | ❌                   |
| `InstructionsLoaded`    | ❌                   |
| `CwdChanged`            | ❌                   |
| `FileChanged`           | ❌                   |
| `PostToolBatch`         | ❌                   |
| `Elicitation`           | ❌                   |
| `ElicitationResult`     | ❌                   |
| `UserPromptExpansion`   | ✅ exit 2            |

### Notes par événement (avril-mai 2026)
- `PermissionDenied` → après refus auto mode. Return `{retry: true}` pour relancer
- `PostCompact` → après compression du contexte
- `InstructionsLoaded` → quand un CLAUDE.md ou rule se charge
- Deferred hooks → `PreToolUse` peut return `permissionDecision: "defer"` (sessions headless pausent et reprennent)
- `hookSpecificOutput.sessionTitle` sur `UserPromptSubmit` (v2.1.94) → nommer dynamiquement la session depuis un hook
- `CwdChanged` → répertoire de travail modifié
- `FileChanged` → changement de fichier détecté
- `PostToolBatch` → après un lot d'appels d'outils
- `Elicitation` / `ElicitationResult` → prompts de saisie utilisateur
- `UserPromptExpansion` → expansion du prompt (bloquable exit 2)

## 5 types de handlers

```json
{"type": "command", "command": "python3 .claude/hooks/hook.py", "timeout": 60}
{"type": "http", "url": "https://webhook.example.com"}
{"type": "prompt", "prompt": "Sûr ?", "model": "haiku"}
{"type": "agent", "agent": "mon-agent", "prompt": "Vérifie..."}
{"type": "mcp_tool", "server": "mon-server", "tool": "mon-outil", "input": {"key": "value"}}
```

## settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python3 .claude/hooks/format.py" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 .claude/hooks/security.py" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/notify.py",
            "once": true
          }
        ]
      }
    ]
  }
}
```

## Exit codes

| Code | Effet                   |
| ---- | ----------------------- |
| `0`  | Succès                  |
| `1`  | Erreur loggée, continue |
| `2`  | BLOQUÉ (PreToolUse)     |

## hookSpecificOutput — Pattern avancé

Permet de modifier les inputs d'outils et d'injecter du contexte (pas seulement bloquer/autoriser).

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "updatedInput": { "modified_field": "value" },
    "additionalContext": "Contexte injecté pour Claude"
  }
}
```

## asyncRewake

`asyncRewake: true` — réveille Claude quand un hook background exit 2, affiche stderr comme system reminder.

## Template Python

```python
#!/usr/bin/env python3
import json, sys, subprocess

def main():
    data = json.loads(sys.stdin.read())
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    # Logique ici
    # Bloquer : print("Raison", file=sys.stderr); sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Cas d'usage courants

**Formater Python (PostToolUse Write|Edit)**

```python
path = data.get("tool_input", {}).get("path", "")
if path.endswith(".py"): subprocess.run(["ruff", "format", path])
```

**Bloquer rm -rf (PreToolUse Bash)**

```python
cmd = data.get("tool_input", {}).get("command", "")
if "rm -rf" in cmd: print("Bloqué", file=sys.stderr); sys.exit(2)
```

**Notification sonore (Stop) — par OS**

macOS :  `afplay /System/Library/Sounds/Glass.aiff`
Windows : `powershell -c "[console]::beep(800,300)"`
Linux :  `paplay /usr/share/sounds/freedesktop/stereo/complete.oga`

```python
import platform
if platform.system() == "Darwin":
    subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
elif platform.system() == "Windows":
    subprocess.run(["powershell", "-c", '[console]::beep(800,300)'])
else:
    subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])
```

## Hooks Agent Teams (experimental)

| Hook | Declenchement | Blocage |
|------|--------------|---------|
| `TeammateIdle` | Un teammate n'a plus de tache | Non |
| `TaskCreated` | Nouvelle tache sur le board | Non |
| `TaskCompleted` | Tache terminee | Oui (exit 2 = renvoyer feedback) |

Activer : `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` dans `env` de settings.json.

## Hooks inline dans agents/skills

```yaml
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "ruff format $FILE"
          once: true
```

## Post-génération toujours

```bash
chmod +x .claude/hooks/<nom>.py
python3 -m json.tool .claude/settings.json
```

## Gotchas

- **JSON sur stdin, pas de variables d'environnement** — tous les hooks reçoivent leurs données via `json.loads(sys.stdin.read())`. Ne pas lire `os.environ` pour les inputs du hook.
- **Exit code 2 = blocage uniquement sur PreToolUse** — sur PostToolUse, Stop et autres événements, exit 2 est ignoré ou traité comme exit 1. Seul PreToolUse bloque l'exécution de l'outil.
- **Pas de TTL sur markers** — les markers doivent être vérifiés par leur existence seule (`os.path.exists(marker)`), jamais par logique temporelle. Un marker expirable = complexité inutile + bugs de timing.

## Vault

[[comment-creer-hook]], [[erreur-settings-paths-hardcodes-multi-poste]], [[erreur-advisory-rules-insuffisantes]]

## Apprentissage

Après chaque usage significatif, sauvegarder en mémoire projet les patterns efficaces et erreurs rencontrées.

_Aucune entrée pour le moment._
