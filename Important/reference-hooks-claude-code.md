---
type: reference
domaine: claude-code
sujet: hooks
mis_a_jour: 2026-06-06
tags: [claude-code, hooks, enforcement, pretooluse, posttooluse, stop, subagentstop, securite, windows]
---

# Référence — Créer un hook Claude Code parfait

> Méthode générique applicable à n'importe quel repo. Pour le CLI (les hooks ne se déclenchent PAS dans l'app desktop / Cowork). Orienté fiabilité, sécurité et cross-machine. Cohérent avec les docs skills, subagents et CLAUDE.md.

## TL;DR

- **Un hook est le SEUL mécanisme déterministe de Claude Code.** Tout le reste (CLAUDE.md, rules, corps de skill/agent) est du texte interprété = probabiliste. Un hook tourne hors de la boucle LLM : il ne peut pas halluciner.
- **`exit 2` bloque ; `exit 1` ne bloque JAMAIS.** C'est LE bug n°1, vu dans 3 équipes qui croyaient bloquer les force-push. exit 1 affiche un warning et l'action passe quand même. Teste TOUJOURS en déclenchant le pattern bloqué et en vérifiant que l'action a été empêchée, pas juste « warnée ».
- **Doctrine de scope (à respecter absolument) : hooks = lint / sécurité / scope UNIQUEMENT. JAMAIS de workflow agentique** (architect-first, TDD strict, commit gates, markers TTL). Le workflow vit dans les agents/skills, pas dans les hooks.
- **Rapides (< 500 ms idéalement) car ils gatent chaque appel d'outil concerné.** Dix hooks rapides battent deux lents.

---

## PARTIE 1 — Ce qu'est un hook (le modèle mental)

Un hook est une commande (shell / HTTP / MCP / prompt LLM / subagent) qui s'exécute automatiquement à un point précis du cycle de vie de Claude Code. Il reçoit du JSON sur stdin, et communique sa décision par **code retour** ou par **JSON sur stdout**.

Sa nature : **déterministe**. C'est ça qui le distingue de tout le reste. « Sans hooks, les règles du CLAUDE.md sont consultatives. Avec hooks, elles deviennent des barrières appliquées. »

Ce qu'un hook PEUT faire selon l'événement :
- **Bloquer** une action (PreToolUse → deny)
- **Modifier** une entrée (PreToolUse → updatedInput)
- **Injecter du contexte** (UserPromptSubmit, SessionStart → additionalContext)
- **Forcer la continuation** (Stop, SubagentStop → decision:block + reason)
- **Observer** (PostToolUse → logging, format, lint — ne peut pas annuler, l'action a déjà eu lieu)

---

## PARTIE 2 — Liste des événements (27, v2.1.141+)

Liste complète : SessionStart, Setup, SessionEnd, UserPromptSubmit, UserPromptExpansion, Stop, StopFailure, PreToolUse, PostToolUse, PostToolUseFailure, PostToolBatch, PermissionRequest, PermissionDenied, SubagentStart, SubagentStop, TeammateIdle, TaskCreated, TaskCompleted, InstructionsLoaded, ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove, PreCompact, PostCompact, Notification, Elicitation, ElicitationResult.

### Les événements qui comptent vraiment (tableau)

| Événement | Quand | Peut bloquer ? | Usage type |
|---|---|---|---|
| **PreToolUse** | Avant un outil. Matcher = tool_name | **Oui** (deny / exit 2 / updatedInput) | Bloquer destructeur, gater commandes, valider scope |
| **PostToolUse** | Après succès d'un outil | Feedback uniquement (déjà exécuté) | Format, lint, validation, logging |
| **PostToolUseFailure** | Après échec d'un outil | Feedback | Contexte d'erreur pour Claude |
| **UserPromptSubmit** | À la soumission, avant que Claude voie | **Oui** + **additionalContext injecté** | Rappel d'activation de skill, injection de contexte |
| **Stop** | Quand Claude finit de répondre | **Oui** (decision:block force la continuation) | Checklist de complétion |
| **SubagentStop** | Quand un subagent finit. Matcher = agent_type | **Oui** (decision:block) | Vérifier qu'un subagent a fait son travail / invoqué un skill |
| **SubagentStart** | Au spawn d'un subagent | Non (command-only) | Injecter du contexte au subagent |
| **SessionStart** | Début/reprise. Matchers: startup/resume/clear/compact | Non ; **stdout → contexte** | Charger contexte projet dynamique |
| **PreCompact / PostCompact** | Avant/après compaction | — | Sauver/réinjecter le contexte critique |
| **PermissionRequest** | Dialogue de permission | Oui (auto-approve/deny) | Approbation auto d'opérations sûres |
| **InstructionsLoaded** | Chargement CLAUDE.md/rules | Non | Logger/réagir au chargement |
| **SessionEnd** | Fin de session | Non | Cleanup, métriques |

**Champs stdin communs (tous events)** : `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`. PreToolUse/PostToolUse ajoutent `tool_name`, `tool_input`, `tool_response`. SubagentStop ajoute `agent_id`, `agent_type`, `agent_transcript_path`, `last_assistant_message`, `stop_hook_active`.

---

## PARTIE 3 — Les 5 types de handler

| Type | Quoi | Quand l'utiliser |
|---|---|---|
| **command** | Script shell, JSON sur stdin, décision par exit code | Le workhorse. 90 % des cas. Déterministe, rapide |
| **http** | POST le JSON à un serveur, réponse 2xx avec décision | Politique d'équipe centralisée. ⚠️ non-2xx = NON-bloquant → pas pour du hard policy |
| **mcp_tool** | Appelle un tool MCP | ⚠️ serveur déconnecté = NON-bloquant → pas pour du hard policy |
| **prompt** | Évaluation LLM single-turn (`$ARGUMENTS` = le JSON), modèle rapide | Décision nuancée bornée. Renvoie `{ok, reason}` ou `{decision, reason}` |
| **agent** | Spawn un subagent (Read/Grep/Glob) | Vérification approfondie multi-étapes. Le plus lourd/lent |

> Règle : pour l'enforcement DUR (qui doit tenir même sous panne réseau), utilise **command** (ou http/mcp en sachant qu'ils échouent ouvert). prompt/agent = jugement, pas garantie.

---

## PARTIE 4 — Sémantique des codes retour (LE point critique)

- **exit 0** = succès. stdout parsé comme JSON UNIQUEMENT sur exit 0. Pour la plupart des events, stdout va au debug log. **Exceptions** : UserPromptSubmit, UserPromptExpansion, SessionStart → stdout AJOUTÉ au contexte que Claude voit.
- **exit 2** = blocage. stdout/JSON IGNORÉS ; **stderr renvoyé à Claude**. Effet selon l'event (PreToolUse bloque l'outil, Stop force la continuation).
- **tout autre code (dont exit 1)** = erreur NON-bloquante. L'action continue.

> ⚠️ **Le bug n°1, vu dans 3 équipes** : un hook de sécurité en `exit 1` « a l'air de marcher » (le message s'affiche) mais ne bloque RIEN. Le force-push passe quand même. **Sécurité = exit 2, jamais exit 1.**

### Format JSON de décision (varie par event — piège fréquent)
- **Universel** : `{"continue": false, "stopReason": "...", "suppressOutput": true}`. `continue:false` prime sur tout.
- **PreToolUse / PermissionRequest** : `{"hookSpecificOutput": {"hookEventName":"PreToolUse", "permissionDecision":"allow|deny|ask", "permissionDecisionReason":"...", "updatedInput":{...}}}`
- **PostToolUse / Stop / SubagentStop** : `{"decision":"block", "reason":"..."}` (top-level)
- **UserPromptSubmit / SessionStart** : `{"hookSpecificOutput": {"hookEventName":"UserPromptSubmit", "additionalContext":"..."}}`

> **Choisis UNE approche par hook** : soit code retour seul, soit exit 0 + JSON. Si exit 2, le JSON est ignoré.
> **Pour Stop/SubagentStop** : préfère `exit 0` + JSON `{"decision":"block","reason":...}` car le `reason` devient le prochain prompt (texte riche). Si tu fais exit 2, tu perds le reason structuré.

---

## PARTIE 5 — Matchers (et les pièges)

- `"*"` / `""` / omis = tout
- Lettres+chiffres+`_`+`|` = chaîne exacte ou liste OR : `Edit|Write|MultiEdit`
- Tout autre caractère = **regex JavaScript**
- MCP : `mcp__server__.*` (le `.*` est REQUIS ; `mcp__server` seul = chaîne exacte → ne matche rien)

> **Piège de casse** : `Edit|Write|multiEdit` (m minuscule) ne matche PAS `MultiEdit`. Toujours `MultiEdit` avec M majuscule.

Matchers PreToolUse supportés : Bash, Edit, Write, Read, Glob, Grep, WebFetch, WebSearch, et tout `mcp__server__tool`.

---

## PARTIE 6 — Où configurer un hook (scope & précédence)

| Emplacement | Portée |
|---|---|
| `~/.claude/settings.json` | Tous projets, machine-locale |
| `.claude/settings.json` | Projet, committable |
| `.claude/settings.local.json` | Projet, gitignored |
| Managed policy (org) | Non-overridable |
| Plugin `hooks/hooks.json` | Via plugin |
| **Frontmatter skill/agent `hooks:`** (CC 2.1) | Scopé au cycle de vie du composant |

- **Tous les hooks de toutes les couches sont MERGÉS et tournent** (pas d'override).
- `disableAllHooks:true` désactive tout SAUF les hooks managés.
- **Hot-reload partiel** : Claude snapshote les hooks au début de session ; édite puis review via `/hooks`.
- **Bug #10412** : un Stop hook exit 2 installé via PLUGIN échoue → installe-le depuis `.claude/hooks/` à la place.

---

## PARTIE 7 — Adaptation OS + Stack (RÈGLE D'OR avant de générer)

Un hook exécute du **code réel**, donc il est OS-spécifique ET stack-spécifique. C'est LE point où une config copiée-collée casse un autre repo. Ne JAMAIS supposer l'environnement.

### Règle absolue : DEMANDER au début, jamais supposer

Avant de générer le moindre hook pour un repo, poser les deux questions :

1. **OS** : Windows / macOS / Linux / cross-machine (repo partagé sur plusieurs OS) ?
2. **Stack** : Python / TypeScript-JS / Go / Rust / autre ?

Ne pas deviner depuis ses propres habitudes. Une config Windows + `py` launcher appliquée à un repo Mac/Linux casse tout silencieusement.

### Matrice OS — l'interpréteur et les chemins

| | Windows | macOS / Linux | Cross-machine (le plus dur) |
|---|---|---|---|
| **Interpréteur Python** | `py "..."` (launcher) | `python3 "..."` | détecter, ou wrapper qui essaie les deux |
| **Shebang** | ignoré | `#!/usr/bin/env python3` + `chmod +x` | shebang + appel explicite |
| **Chemins** | jamais `C:\...` (Bash mange `\`) → `${CLAUDE_PROJECT_DIR}` + `/` | `/` natif | toujours `${CLAUDE_PROJECT_DIR}` + slashs |
| **Beep / notif** | `rundll32 user32.dll,MessageBeep` | `afplay` (mac) / `paplay` (linux) | conditionner sur l'OS, ou supprimer |
| **`shell:` du hook** | `powershell` possible | `bash` | `bash` (défaut), éviter le PS-spécifique |

### Matrice STACK — lint / test / format dans un hook

| Stack | Lint | Format | Test | Typecheck | Extensions |
|---|---|---|---|---|---|
| **Python** | `ruff` / `pyflakes` | `ruff format` / `black` | `pytest` | `mypy` | `.py` |
| **TypeScript / JS** | `eslint` | `prettier` | `npm test` / `vitest` / `jest` | `tsc --noEmit` | `.ts .tsx .js` |
| **Go** | `go vet` | `gofmt` | `go test` | (intégré) | `.go` |
| **Rust** | `clippy` | `rustfmt` | `cargo test` | `cargo check` | `.rs` |

→ Un PostToolUse de lint doit utiliser l'outil de la BONNE stack. Vérifier que l'outil existe (`shutil.which("ruff")`) et fail-open s'il est absent, plutôt que de planter.

### Règles cross-machine universelles (à appliquer toujours)

- **Résolution de chemin via `__file__`**, jamais en dur :
  ```python
  _HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
  _CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
  ```
- **Toujours `${CLAUDE_PROJECT_DIR}` + slashs**, jamais de chemin absolu OS-spécifique.
- **Fail-open** : toute exception → `sys.exit(0)` silencieux. Un hook qui plante ne doit jamais bloquer le travail (sauf hook de sécurité, où le fail dur est volontaire).
- **Vérifier la présence de l'outil avant de l'appeler** (`shutil.which("ruff")`), sinon skip proprement.
- **Si repo cross-machine** : préférer un wrapper Python qui détecte l'OS plutôt qu'une commande shell OS-spécifique dans le settings.json.

---

## PARTIE 8 — Patterns de hook parfait (par usage)

### Pattern A — Sécurité (PreToolUse, exit 2)
Bloquer le destructeur. Rapide (< 500 ms), exit 2 obligatoire.
```python
#!/usr/bin/env python3
import json, sys, re
data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")
DANGER = [r"\brm\s+-rf\b", r"git\s+push.*--force", r"git\s+branch\s+-D\b"]
for pat in DANGER:
    if re.search(pat, cmd):
        print(f"BLOQUÉ : pattern destructeur '{pat}'. Demande à Raphael explicitement.", file=sys.stderr)
        sys.exit(2)   # exit 2 = blocage RÉEL
sys.exit(0)           # permissif par défaut
```

### Pattern B — Qualité (PostToolUse, feedback)
Valider/formatter après Write/Edit. Ne peut pas annuler, mais renvoie un feedback que Claude corrige.
```json
{ "hooks": { "PostToolUse": [ { "matcher": "Write|Edit|MultiEdit",
  "hooks": [ { "type": "command",
    "command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/validate.py\"", "timeout": 5 } ] } ] } }
```

### Pattern C — Injection de contexte (UserPromptSubmit, stdout → contexte)
Rappeler d'invoquer un skill pertinent.
```python
#!/usr/bin/env python3
import sys
print("RAPPEL : si une skill cc-* couvre ce sujet, invoque-la (outil Skill) avant d'agir.")
sys.exit(0)   # stdout ajouté au contexte sur UserPromptSubmit
```

### Pattern D — Vérification subagent (SubagentStop, exit 0 + JSON)
Forcer un subagent à finir son travail. Parse le transcript (pas de signal propre d'invocation de skill).
```python
#!/usr/bin/env python3
import json, sys, os
d = json.load(sys.stdin)
if d.get("stop_hook_active"):   # anti-boucle infinie : OBLIGATOIRE
    sys.exit(0)
tp = d.get("agent_transcript_path", "")
ok = False
try:
    with open(os.path.expanduser(tp)) as f:
        for line in f:
            if '"name": "Skill"' in line and "cc-skills-ref" in line:
                ok = True
    if not ok:
        print(json.dumps({"decision":"block",
          "reason":"Tu n'as pas invoqué cc-skills-ref. Invoque-le puis termine."}))
        sys.exit(0)   # exit 0 + JSON (pas exit 2, sinon JSON ignoré)
except Exception:
    pass
sys.exit(0)
```

### Pattern E — Survie à la compaction (SessionStart compact)
Réinjecter le contexte critique après compaction via `additionalContext`.

---

## PARTIE 9 — La DOCTRINE de scope (ce qu'un hook NE doit PAS faire)

C'est la règle la plus importante après exit 2, et celle qu'on oublie le plus.

**Un hook fait : lint, sécurité, scope, format, logging, injection de rappel, vérification de complétion.**

**Un hook NE fait PAS de workflow agentique :**
- ❌ Forcer architect-first
- ❌ Imposer TDD strict
- ❌ Commit gates orchestrés
- ❌ Markers TTL / machines à états de workflow

Pourquoi : un hook est un point déterministe, pas un orchestrateur. Mettre du workflow dans un hook le rend fragile, opaque, et combat le jugement de l'agent. Le workflow vit dans les agents/skills (où le modèle raisonne), le hook ne fait que poser des barrières mécaniques.

> Si tu te surprends à écrire une machine à états dans un hook → c'est un agent ou une skill qu'il te faut, pas un hook.

---

## PARTIE 10 — Debug

- **`/hooks`** : menu read-only montrant event, matcher, type, source. Vérifie l'enregistrement.
- **`claude --debug`** : trace l'exécution.
- **Ligne de log au début du script** : `echo "[$(date)] $0 appelé" >> /tmp/hooks.log`. Si le fichier reste vide → le hook ne se déclenche pas (matcher ? enregistrement ?).
- **Test manuel** : `echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | py hook.py; echo $?` → doit afficher 2.
- **Le test qui compte** : déclenche le pattern bloqué et vérifie que l'action a été EMPÊCHÉE, pas juste warnée.

---

## PARTIE 11 — Checklist d'un hook parfait

**Fonctionnement**
- [ ] Bon événement choisi (PreToolUse pour bloquer, PostToolUse pour réagir, Stop/SubagentStop pour forcer)
- [ ] **exit 2 pour bloquer** (PreToolUse), jamais exit 1
- [ ] **exit 0 + JSON `decision:block`** pour Stop/SubagentStop (garde le reason riche)
- [ ] `stop_hook_active` vérifié sur Stop/SubagentStop (anti-boucle)
- [ ] Choix unique : code retour OU JSON, pas les deux

**Matcher & scope**
- [ ] Matcher correct (casse exacte, `MultiEdit` avec M, `mcp__x__.*` avec `.*`)
- [ ] Doctrine respectée : lint/sécu/scope, PAS de workflow agentique
- [ ] Bon emplacement (projet committable vs user vs local)

**Adaptation OS & stack (demander d'abord !)**
- [ ] OS du repo demandé (Windows / mac / Linux / cross-machine) — jamais supposé
- [ ] Stack du repo demandée (Python / TS / Go / Rust…)
- [ ] Interpréteur adapté (`py` Windows, `python3` mac/linux)
- [ ] Outils lint/test de la BONNE stack (`ruff`/`pytest` vs `eslint`/`tsc`)
- [ ] `${CLAUDE_PROJECT_DIR}` + slashs, jamais `C:\...`
- [ ] Chemins via `__file__` dans le script
- [ ] `shutil.which()` avant d'appeler un outil, fail-open s'il manque
- [ ] Fail-open (`exit 0` sur exception) — sauf hook sécurité

**Performance & robustesse**
- [ ] Rapide (< 500 ms pour un hook qui gate chaque appel)
- [ ] timeout défini
- [ ] Testé en déclenchant réellement le pattern (bloqué, pas juste warné)
- [ ] Enregistrement vérifié via `/hooks`
- [ ] Si distribué en plugin et Stop hook KO → installer depuis `.claude/hooks/` (#10412)

---

## La vérité dure

1. **Le hook est le seul mécanisme déterministe.** Tout ce qui doit être garanti passe par un hook ; le reste est probabiliste.
2. **exit 2 bloque, exit 1 ne bloque jamais.** Le bug le plus répandu et le plus dangereux. Teste en déclenchant le pattern.
3. **Hooks = lint / sécu / scope. Jamais de workflow agentique.** Le workflow vit dans les agents/skills.
4. **http / mcp_tool / prompt échouent OUVERT** (non-bloquant sur panne). Pour du hard policy → command + exit 2.
5. **Un hook lent gate chaque appel d'outil** → garde-le sous 500 ms, fail-open, snapshoté au début de session.
