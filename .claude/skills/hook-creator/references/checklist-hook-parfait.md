# Checklist hook parfait — 4 dimensions

Source : reference-hooks-claude-code.md (research LLM juin 2026) + doctrine forge 22 mai.

---

## 0. Décision — Faut-il vraiment un hook ? (OBLIGATOIRE)

- [ ] La règle doit tenir à **100% mécaniquement** ? (sinon → rule/CLAUDE.md advisory)
- [ ] C'est du lint / sécurité / scope / format / logging / injection / vérification ? → hook OK
- [ ] Ce n'est PAS du workflow agentique (architect-first, TDD, commit gates, markers TTL) ?
- [ ] L'environnement cible est bien le **CLI** ? (Desktop/Cowork → hooks absents)
- [ ] Aucun hook similaire existant ? (sinon → modifier/étendre)

## 1. Fonctionnement

- [ ] Bon événement : PreToolUse (bloquer), PostToolUse (réagir), Stop/SubagentStop (forcer)
- [ ] **exit 2 pour bloquer** (PreToolUse) — jamais exit 1 (ne bloque jamais — bug n°1)
- [ ] **exit 0 + JSON `{"decision":"block","reason":"..."}` pour Stop/SubagentStop** (reason riche)
- [ ] `stop_hook_active` vérifié sur Stop/SubagentStop (anti-boucle, cap 8 blocages)
- [ ] Choix UNIQUE : code retour OU JSON (si exit 2, JSON ignoré)
- [ ] Triplet `Write|Edit|MultiEdit` si PostToolUse écriture (sans MultiEdit = trou)
- [ ] MCP matcher : `mcp__server__.*` avec `.*` (sans = chaîne exacte → ne matche rien)
- [ ] Casse exacte : `MultiEdit` avec M majuscule

## 2. Adaptation OS & stack (demander d'abord, jamais supposer)

- [ ] OS demandé et confirmé (Windows / mac / Linux / cross-machine)
- [ ] Stack demandée (Python / TS / Go / Rust…)
- [ ] Interpréteur adapté : `py "..."` Windows, `python3 "..."` mac/linux
- [ ] Outils lint/test de la BONNE stack (`ruff`/`pytest` vs `eslint`/`tsc`)
- [ ] `${CLAUDE_PROJECT_DIR}` + slashs — jamais `C:\...` ni chemin absolu
- [ ] Chemins via `__file__` dans le script Python
- [ ] `shutil.which("outil")` avant appel — fail-open si absent
- [ ] Fail-open sur exception (`sys.exit(0)`) — sauf hook sécu (fail dur voulu)
- [ ] Cross-machine : wrapper Python détectant l'OS plutôt que commande shell dans settings.json

## 3. Performance & robustesse

- [ ] Rapide (< 500 ms — gate chaque appel d'outil concerné)
- [ ] `timeout` défini dans settings.json
- [ ] Scope correct : projet / user / local
- [ ] **Testé chemin PASS** (action autorisée passe bien)
- [ ] **Testé chemin BLOCK** (action bloquée — vérifier action empêchée, pas juste warnée)
- [ ] **Testé fail-open** (exception → exit 0, action continue)
- [ ] Enregistrement vérifié via `/hooks`
- [ ] Si distribué via plugin et Stop hook KO → installer depuis `.claude/hooks/` (bug #10412)

## 4. Evals (OBLIGATOIRES)

- [ ] 3 rounds d'interview complétés (OS+stack, événement, scope)
- [ ] Test manuel : `echo '{"tool_name":"Bash","tool_input":{"command":"..."}}' | py hook.py; echo $?`
- [ ] Test en session réelle : pattern bloqué déclenché, action confirmée empêchée
- [ ] `/hooks` consulté pour confirmer l'enregistrement
