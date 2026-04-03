---
name: cc-hooks-ref
description: Référence complète des hooks Claude Code — 21 événements, 4 types de handlers, format settings.json, scripts Python, blocage exit 2, hooks inline. Charger quand on crée ou modifie un hook.
user-invokable: false
---

# Référence — Hooks Claude Code

## 21 événements

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

## 4 types de handlers

```json
{"type": "command", "command": "python3 .claude/hooks/hook.py", "timeout": 60}
{"type": "http", "url": "https://webhook.example.com"}
{"type": "prompt", "prompt": "Sûr ?", "model": "haiku"}
{"type": "agent", "agent": "mon-agent", "prompt": "Vérifie..."}
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
