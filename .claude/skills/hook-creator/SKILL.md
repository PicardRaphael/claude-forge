---
name: hook-creator
description: ALWAYS invoke when user wants to create, modify, or audit a Claude Code hook. Do not hand-write hook configurations directly — use this skill first.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
---

# hook-creator

Crée et optimise des hooks Claude Code selon la doctrine forge + référence Anthropic officielle.
Couvre : décision créer/PAS → OS+stack → interview → draft → test → livraison.

Si besoin du détail complet de la doctrine : `mcp__forge-brain__read_note("comment-creer-hook")`.

## GATE 0 — AUDIT PROFOND OBLIGATOIRE (avant toute action, AUCUNE exception)

**L'audit est TOUJOURS profond. Jamais de raccourci, jamais de mode léger.** Que ce soit une création, une optimisation ou un audit — création triviale incluse — ces 3 étapes sont un PASSAGE OBLIGÉ avant de produire ou modifier quoi que ce soit :

1. **Lire les canoniques vault EN ENTIER** via `mcp__forge-brain__read_note("comment-creer-hook")` — SANS `max_lines`. `search_brain` seul (extraits ~10 lignes) = INSUFFISANT. Bloquant : ne rien rédiger avant.
2. **Passer SYSTÉMATIQUEMENT les 4 dimensions de `references/checklist-hook-parfait.md`** — toutes, dans l'ordre, rien zappé. Chaque dimension cochée avec evidence (fichier:ligne + écart mesurable). C'est un GATE, pas une option de fin de fichier.
2bis. **VÉRIFIER L'ADÉQUATION DU TYPE DE COMPOSANT (création ET audit — toujours).** Un hook doit-il rester un hook ? Signaler — sans transformer d'office — si le mécanisme ne peut PAS tenir la promesse du composant :
   - Un hook est DÉTERMINISTE mais opaque (pas de raisonnement). S'il tente du WORKFLOW AGENTIQUE (architect-first, TDD, multi-étapes avec jugement) → mauvais type, candidate SKILL/AGENT où le modèle raisonne.
   - S'il ne fait qu'injecter un rappel probabiliste sans rien garantir → une RULE/CLAUDE.md suffit peut-être.
   Si décalage promesse/mécanisme détecté → le signaler comme observation ARCHITECTURE dans le rapport (« devrait peut-être être un <autre type> parce que <raison> »), distincte des écarts qualité. NE JAMAIS transformer le composant sans validation explicite de Raphaël — c'est une décision d'architecture, pas une correction qualité.

3. **PUIS calibrer l'effort de création/eval à l'enjeu** : profondeur d'audit = toujours 100% ; lourdeur du process de création (evals A/B, optimization loop) = proportionnée (skill réutilisée cross-repo = process complet ; composant trivial = audit complet + création directe). Profondeur ≠ lourdeur mécanique.

Sortie du gate : un rapport d'écarts (CRITIQUE / IMPORTANT / SUGGESTION) présenté AVANT exécution. Pas d'écart mesuré = pas de modification cosmétique inutile.


## Phase 0 — Test préliminaire : faut-il vraiment un hook ?

**Avant tout** — répondre à ces questions :

1. La règle doit-elle tenir **à 100% mécaniquement** ?
   - **OUI** → hook (seul mécanisme déterministe de CC)
   - **NON** → une **rule** `.claude/rules/` ou **CLAUDE.md** suffit (advisory, ~80% compliance)

2. De quel type est le besoin ?
   - **lint / sécurité / scope / format / logging / injection de rappel / vérification complétion** → hook OK, continuer
   - **workflow agentique** (architect-first, TDD strict, commit gates, markers TTL) → STOP. Expliquer : "Tu décris du workflow — un hook n'est pas le bon outil. Un hook est déterministe mais opaque. Ce que tu décris appartient à un agent ou une skill où le modèle raisonne. Je te recommande [skill/agent] parce que [raison]. Tu veux partir sur ça ?"
   - **comportement réutilisable invocable à la demande** → STOP. Proposer une **skill**.

3. L'environnement cible est-il le **CLI** ?
   - Les hooks ne fonctionnent **PAS** dans Desktop app / Cowork → le confirmer avant de continuer.

Vérifier qu'un hook similaire n'existe pas déjà :
```bash
cat .claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A5 '"hooks"'
cat ~/.claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A5 '"hooks"'
```
Si similaire → proposer modifier/étendre plutôt que créer.

---

## Phase 1 — Interview OS + Stack (OBLIGATOIRE en premier, avant tout code)

**Ces deux questions doivent être posées AVANT de générer le moindre code.** Ne jamais supposer.

**Round 1 — Environnement (toujours)**
1. **OS du repo** : Windows / macOS / Linux / cross-machine (partagé plusieurs OS) ?
2. **Stack du projet** : Python / TypeScript-JS / Go / Rust / autre ? (pour les hooks de lint/test)
3. Créer un nouveau hook ou modifier/auditer un existant ?

**Round 2 — Fonctionnement**
4. **Quel événement** déclenche le hook ? (PreToolUse pour bloquer, PostToolUse pour réagir, Stop/SubagentStop pour forcer, UserPromptSubmit pour injecter du contexte, SessionStart pour charger contexte)
5. **Quelle action** déclenchera ce hook ? (Bash, Write, Edit, MultiEdit, agent_type spécifique, tout ?)
6. Doit-il **bloquer** (décision dure) ou **observer/réagir** (feedback) ?

**Round 3 — Détails**
7. **Scope** : projet (`.claude/settings.json`) / user (`~/.claude/settings.json`) / local (`.claude/settings.local.json`) ?
8. **Type de handler** : command (Python/shell), http, mcp_tool, prompt (LLM), agent ?
9. **Side-effects autorisés** ? (notifications, logs, network) — pour calibrer le fail-open

---

## Phase 2 — Adaptation OS + Stack (avant de coder)

Choisir l'interpréteur et les outils selon les réponses de l'interview :

| | Windows | macOS / Linux | Cross-machine |
|---|---|---|---|
| **Python** | `py "${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.py"` | `python3 ".claude/hooks/hook.py"` | wrapper détectant l'OS |
| **Shebang** | ignoré | `#!/usr/bin/env python3` + `chmod +x` | shebang + appel explicite |
| **Chemins** | `${CLAUDE_PROJECT_DIR}` + `/` | `/` natif | `${CLAUDE_PROJECT_DIR}` + `/` toujours |

**Stack → outils lint/test :**
- Python : `ruff`, `black`, `pytest` — vérifier avec `shutil.which("ruff")`
- TypeScript/JS : `eslint`, `prettier`, `tsc --noEmit`
- Go : `go vet`, `gofmt`, `go test`
- Rust : `clippy`, `rustfmt`, `cargo test`

**Règles cross-machine obligatoires :**
```python
_HOOK_DIR = os.path.dirname(os.path.abspath(__file__))  # jamais chemin en dur
_CLAUDE_DIR = os.path.dirname(_HOOK_DIR)
```
- Fail-open : toute exception → `sys.exit(0)` silencieux (sauf hook sécu où fail dur est voulu)
- `shutil.which("outil")` avant appel — skip proprement si absent

---

## Phase 3 — Rédiger le hook

### Sémantique des codes retour (CRITIQUE)

| Code | Effet | Quand utiliser |
|---|---|---|
| **exit 0** | Succès. stdout parsé si JSON sur events qui l'acceptent | Toujours par défaut |
| **exit 2** | Blocage RÉEL. stderr renvoyé à Claude. JSON ignoré | PreToolUse pour bloquer — JAMAIS exit 1 |
| **exit 1** | Erreur non-bloquante. L'action CONTINUE | LE bug n°1 — ne bloque jamais |

**Pour Stop/SubagentStop** : préférer `exit 0` + JSON `{"decision":"block","reason":"..."}` — le `reason` devient le prochain prompt (texte riche). Si exit 2, le reason est perdu.

**Toujours `stop_hook_active` vérifié** sur Stop/SubagentStop → anti-boucle infinie.

### Formats JSON par event

```python
# PreToolUse — bloquer
{"hookSpecificOutput": {"hookEventName":"PreToolUse", "permissionDecision":"deny", "permissionDecisionReason":"..."}}

# Stop / SubagentStop — forcer continuation
{"decision": "block", "reason": "..."}  # top-level, exit 0

# UserPromptSubmit / SessionStart — injecter contexte
{"hookSpecificOutput": {"hookEventName":"UserPromptSubmit", "additionalContext":"..."}}

# Universel — arrêt immédiat
{"continue": false, "stopReason": "...", "suppressOutput": true}
```

### Matchers (pièges critiques)

- `"*"` / omis = tout
- `Edit|Write|MultiEdit` = OR — TOUJOURS le triplet pour écriture (sans MultiEdit = trou architectural)
- MCP : `mcp__server__.*` — le `.*` est REQUIS (sans = chaîne exacte → ne matche rien)
- Casse exacte : `MultiEdit` avec M majuscule (pas `multiEdit`)

### Configuration settings.json

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "py \"${CLAUDE_PROJECT_DIR}/.claude/hooks/mon-hook.py\"",
        "timeout": 10
      }]
    }]
  }
}
```

### Structure script Python (template)

```python
#!/usr/bin/env python3
import json, sys, os

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # fail-open si JSON invalide
    
    try:
        # Logique du hook ici
        tool_input = data.get("tool_input", {})
        
        # Pour Stop/SubagentStop — anti-boucle obligatoire
        if data.get("stop_hook_active"):
            sys.exit(0)
        
        # Décision
        # sys.exit(2)  # bloquer (PreToolUse)
        # print(json.dumps({"decision":"block","reason":"..."})); sys.exit(0)  # Stop
        sys.exit(0)
    except Exception:
        sys.exit(0)  # fail-open sur toute exception

if __name__ == "__main__":
    main()
```

### Scope et emplacement

| Emplacement | Portée |
|---|---|
| `.claude/settings.json` | Projet, committable |
| `~/.claude/settings.json` | Tous projets, machine-locale |
| `.claude/settings.local.json` | Projet, gitignored |
| Plugin `hooks/hooks.json` | Via plugin (Stop hook exit 2 → bug #10412 → installer depuis `.claude/hooks/`) |

---

## Phase 4 — Test obligatoire

**Le test qui compte** : déclencher réellement le pattern bloqué et vérifier que l'action a été **empêchée**, pas juste warnée.

```bash
# Test manuel d'un hook PreToolUse
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | py .claude/hooks/mon-hook.py
echo $?   # doit afficher 2 pour un hook bloquant

# Vérifier l'enregistrement
# Taper /hooks dans Claude Code
```

**Test en session réelle :** provoquer le cas bloqué et confirmer que l'action n'a pas eu lieu.

---

## Phase 5 — Evals (OBLIGATOIRES)

Les evals sont **obligatoires** pour tout hook créé. Sans test du chemin bloquant, le hook peut sembler fonctionner (affiche un message) sans bloquer réellement (exit 1).

- Tester le chemin PASS (action autorisée passe)
- Tester le chemin BLOCK (action bloquée avec exit 2 / decision:block)
- Tester le fail-open (exception → exit 0, l'action continue)
- Vérifier via `/hooks` que le hook est bien enregistré

---

## Checklist avant livraison (OBLIGATOIRE — cocher à voix haute, point par point)

**Process**
- [ ] Phase 0 passée : règle déterministe, lint/sécu/scope (pas workflow agentique)
- [ ] CLI confirmé comme environnement cible (hooks absents Desktop/Cowork)
- [ ] 3 rounds d'interview complétés (OS+stack, événement, scope)
- [ ] Aucun hook similaire existant (sinon modifier)

**Fonctionnement**
- [ ] Bon événement (PreToolUse bloquer, PostToolUse réagir, Stop/SubagentStop forcer)
- [ ] **exit 2 pour bloquer** — jamais exit 1 (ne bloque JAMAIS — bug n°1)
- [ ] **exit 0 + JSON `decision:block`** pour Stop/SubagentStop (reason riche)
- [ ] `stop_hook_active` vérifié sur Stop/SubagentStop (anti-boucle)
- [ ] Triplet `Write|Edit|MultiEdit` si matcher écriture
- [ ] Choix unique : code retour OU JSON, pas les deux

**Adaptation OS & stack**
- [ ] OS confirmé — interpréteur adapté (`py` Windows, `python3` mac/linux)
- [ ] Stack confirmée — outils lint/test corrects
- [ ] `${CLAUDE_PROJECT_DIR}` + slashs — jamais `C:\...`
- [ ] Chemins via `__file__` dans le script
- [ ] `shutil.which()` avant appel outil, fail-open si absent
- [ ] Fail-open sur exception (sauf hook sécu)

**Performance & robustesse**
- [ ] Rapide (< 500 ms — gate chaque appel d'outil)
- [ ] `timeout` défini dans settings.json
- [ ] Testé : chemin PASS + chemin BLOCK + fail-open
- [ ] Enregistrement vérifié via `/hooks`
- [ ] Si plugin et Stop hook → installer depuis `.claude/hooks/` (bug #10412)

---

## Gotchas

- **exit 1 ne bloque JAMAIS** — affiche un message, l'action continue. LE bug n°1, vu dans 3 équipes. Toujours exit 2 pour bloquer
- **Stop/SubagentStop** : exit 0 + JSON (pas exit 2 — le JSON serait ignoré et le reason perdu)
- **`stop_hook_active` obligatoire** sur Stop/SubagentStop — sans ça, boucle infinie possible (cap natif 8 blocages)
- **MultiEdit absent du matcher** → trou architectural. Toujours le triplet `Write|Edit|MultiEdit`
- **MCP matcher sans `.*`** → chaîne exacte qui ne matche rien. `mcp__server__.*` obligatoire
- **Casse du matcher** : `MultiEdit` avec M majuscule, pas `multiEdit`
- **Hooks ne tournent PAS** dans Desktop app / Cowork — CLI uniquement
- **Hot-reload partiel** : CC snapshote les hooks au début de session — redémarrer ou utiliser `/hooks` pour vérifier
- **Bug #10412** : Stop hook exit 2 via plugin échoue → installer depuis `.claude/hooks/` à la place
- **Workflow agentique dans un hook** → fragile, opaque, combat le jugement de l'agent. Toujours externaliser vers skill/agent
- **Chemin absolu OS-spécifique** → casse cross-machine silencieusement. Toujours `${CLAUDE_PROJECT_DIR}` + `__file__`

---

## Apprentissage

Après chaque création ou optimisation : noter ici les patterns efficaces et gotchas rencontrés.

---

## Références

- `references/checklist-hook-parfait.md` — 4 dimensions complètes
- `mcp__forge-brain__read_note("comment-creer-hook")` — doctrine forge canonique complète (30 events, formats JSON, matrice OS+stack)
- `mcp__forge-brain__read_note("raisonnement-22mai-doctrine-vs-enforcement")` — pourquoi workflow hors hooks
