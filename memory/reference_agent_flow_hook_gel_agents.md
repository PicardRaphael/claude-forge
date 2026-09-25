---
name: agent-flow-hook-gel-agents
description: Hook global agent-flow (~/.claude/agent-flow/hook.js via node fnm) = cause des gels d'agents (tool_use sans tool_result) — spawn node ~2s, parfois gelé en kernel avant d'exécuter le JS
metadata:
  type: reference
trigger: agent bloqué, agent gelé, sub-agent freeze, tool_use sans tool_result, agent-flow, hook node zombie
---

# Hook agent-flow global — gel des sub-agents (diagnostic 6 août 2026)

**Symptôme** : sur neo_ia (mais valable partout — hook GLOBAL `~/.claude/settings.json`), les sub-agents gèlent en plein run : transcript se termine sur un `tool_use` (Read/Grep/Write/Bash) complet, **jamais de tool_result derrière**. Relances = même gel.

**Cause vérifiée** : hook `agent-flow` (forwarder VS Code Agent Flow, installé 29 juil. 2026) branché sur **9 events dont PreToolUse de TOUT** : `node.exe (fnm) ~/.claude/agent-flow/hook.js`, timeout 2.
- Spawn node = **2,05 s mesurés** (1,78 s kernel — Defender) pour un no-op (aucune instance json = extension pas lancée) → chaque tool call de chaque session paie ~2 s et race le timeout:2.
- Parfois le processus node **gèle en kernel avant d'exécuter le JS** (0 CPU, immunisé contre son self-kill 1,5 s — un survivant observé 5 min+, 11 zombies accumulés du 3 au 6 août). Quand ça tombe sur le PreToolUse d'un agent → tool call jamais exécuté → agent gelé.
- Corrélation 4/4 : chaque heure de gel d'agent = heure de spawn d'un node agent-flow zombie.

**Fix** : retirer les 9 hooks agent-flow de `~/.claude/settings.json` (généré : `~/.claude/settings.json.proposed`, ne garde que SessionStart/mcp-autostart) + tuer les zombies :
`Get-CimInstance Win32_Process | ? { ($_.Name -eq 'node.exe' -and $_.CommandLine -match 'agent-flow') } | % { Stop-Process -Id $_.ProcessId -Force }`

**Méthode de diagnostic réutilisable** (agent « bloqué ») :
1. Transcript sub-agent (`~/.claude/projects/<proj>/<session>/subagents/agent-*.jsonl`) : dernier message. `stop_reason: tool_use` sans tool_result = blocage LOCAL (hook/permission) ; `stop_reason: null` = stream API coupé.
2. Scanner les 20 derniers transcripts pour quantifier (gelés vs end_turn).
3. `Get-Process` / `Win32_Process.CommandLine` : chercher des processus hooks (py/node) à 0 CPU vieux de minutes/heures, corréler leurs heures de spawn aux heures de gel.

Voir [[python-path-windows]] (les hooks py aussi gèlent occasionnellement au spawn — 2 zombies py observés : même cause machine, fréquence ×N par le volume d'events agent-flow).

**Suite 6 août après-midi** : même après retrait d'agent-flow (appliqué), le spawn `py` nu reste à **~2 s mesurés** (`py -c "pass"`, sys-dominated — hypothèse Defender scan par spawn, non prouvée). Conséquence : tout hook avec timeout ≤ 5 meurt en « hook timed out — output discarded ». Fix appliqué : timeouts forge 3/5 → 10 (settings.json). Règle : **sur cette machine, timeout hook py minimum = 10** tant que le spawn n'est pas revenu à la normale ; le vrai fix serait une exclusion Defender (décision Raphael).
