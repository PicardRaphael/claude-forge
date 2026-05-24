---
titre: "Erreur — delegate-guard.py bypass via env var au lieu de stdin JSON"
resume: "Le hook delegate-guard.py lisait CLAUDE_AGENT depuis os.environ (toujours vide en pratique) au lieu du champ agent_type passé dans stdin JSON par Claude Code. Conséquence : bypass impossible, catch-22 où agent-creator dispatché se bloquait lui-même."
aliases:
  - "delegate-guard env var dead code"
  - "bug delegate-guard bypass"
  - "claude_agent env var impossible"
  - "agent_type stdin hook"
  - "hook bypass agent_type"
derniere-maj: 2026-05-24
auteur: claude
type: erreur
domaine: claude-code
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#sujet/hooks"
  - "#projet/claude-forge"
---

# Erreur — delegate-guard.py bypass via env var au lieu de stdin JSON

## Ce qui s'est passé

Le hook `delegate-guard.py` de claude-forge contenait depuis sa création (avril 2026) la fonction de bypass suivante (ligne 78-81 avant fix) :

```python
def agent_bypass_active(expected_agent: str) -> bool:
    claude_agent = os.environ.get("CLAUDE_AGENT", "")
    allowed = {"skill-creator", "agent-creator", "hook-creator", "claudemd-optimizer"}
    return claude_agent in allowed
```

Le message d'erreur du hook disait pourtant : *"Bypass: set CLAUDE_AGENT=agent-creator in your environment."*

**Problème** : Claude Code ne définit jamais `CLAUDE_AGENT` dans l'environnement du processus du hook. Quand un sub-agent est dispatché, l'info est passée via le **stdin JSON** du hook, pas via env var.

Résultat : le bypass était dead code. Catch-22 — le hook disait "passe par agent-creator" mais agent-creator dispatché se bloquait lui-même.

## Preuve empirique (24 mai 2026)

Dump du stdin JSON reçu par le hook lors d'un dispatch `agent-creator` :

```json
{
  "session_id": "...",
  "permission_mode": "acceptEdits",
  "agent_id": "a15f201e35f8eeb94",
  "agent_type": "agent-creator",
  "effort": {"level": "high"},
  "hook_event_name": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {...}
}
```

ENV au même moment : **aucune variable CLAUDE_AGENT**. Confirmé : Claude Code v2.1.150 passe l'info via stdin field `agent_type`.

## Pourquoi c'était une erreur

1. **Doctrine forge** dit "déléguer aux agents spécialisés via delegate-guard" — mais la délégation est impossible si l'agent lui-même se bloque.
2. **Workaround documenté** dans `feedback_delegate_guard_env_var_blocked` mémoire : *"Edit manuel ou Shift+Tab"*. Ce workaround masquait le vrai bug du hook au lieu de le corriger.
3. **Conséquence opérationnelle** : tous les edits d'agents/skills depuis avril 2026 ont été faits soit manuellement par Raphael, soit en désactivant temporairement le hook. Friction quotidienne masquée par habitude.

## Fix appliqué (24 mai 2026)

Lire `agent_type` depuis stdin en premier, garder env var en fallback :

```python
def agent_bypass_active(expected_agent: str, data: dict) -> bool:
    allowed = {"skill-creator", "agent-creator", "hook-creator", "claudemd-optimizer"}
    agent_type = data.get("agent_type", "")
    if agent_type in allowed:
        return True
    claude_agent = os.environ.get("CLAUDE_AGENT", "")
    return claude_agent in allowed
```

Validé empiriquement : dispatch `agent-creator` → Edit sur `.claude/agents/devils-advocate.md` → OK.

## Quoi faire à la place (pour TOUT futur hook)

**Règle universelle** : pour détecter l'agent invocateur dans un hook, **TOUJOURS** lire `data["agent_type"]` depuis stdin JSON, **JAMAIS** via env var.

Référence canonique : [[comment-creer-hook]] section gotchas — "stdin JSON agent_type vs env var".

Pour vérifier le format stdin réel d'un événement Claude Code, déployer temporairement un dump debug dans le hook (avant la logique métier) :

```python
debug_log = Path(__file__).parent / ".hook-stdin-debug.log"
with debug_log.open("a", encoding="utf-8") as f:
    f.write(json.dumps(data, indent=2, default=str)[:3000])
```

Puis lancer une opération qui déclenche le hook. Inspecter `data` réel.

## Wikilinks

- [[comment-creer-hook]]
- [[reference_agent_type_hook_detection]]
- [[feedback_delegate_guard_env_var_blocked]]
- [[raisonnement-22mai-doctrine-vs-enforcement]]
- [[methode-pivoter-doctrine]]
