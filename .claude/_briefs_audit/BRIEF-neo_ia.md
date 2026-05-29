# BRIEF fixes audit — neo_ia

> À coller dans une session Claude Code ouverte **DANS** `C:\Users\raphael.picard_neote\Documents\neot-v2\neo_ia`.
> Issu de l'audit `.claude/` multi-repo du 29 mai 2026.

## Déjà corrigé depuis la session forge (à committer, NE PAS refaire)

Edits déjà appliqués et vérifiés — il reste à les committer depuis neo_ia (`git diff` pour relire, puis commit sur `develop`) :

1. **Drift de nommage d'agents** (finding #1, `/go` était cassé) :
   - `.claude/skills/refactor-scan/SKILL.md` : `architect`→`architect-deep`, `dev`→`dev-lead`
   - `.claude/skills/agent-workflows/SKILL.md` : `architect`→`architect-deep`, `build-error-resolver`→`skill build-fix`
   - `.claude/skills/go/SKILL.md` : `code-reviewer`→`reviewer` (subagent_type)
   - `.claude/rules/agent-routing.md` : `code-reviewer`/`security-reviewer`→`reviewer`, `build-error-resolver`→`build-fix`
   - `.claude/rules/orchestrator-mindset.md`, `check-before-create.md`, `testing-mandatory.md` : `code-reviewer`→`reviewer`
2. **`.claude/skills/ia-back-contract/SKILL.md`** — chemins morts `src/` → `apps/` + `packages/shared_utils/shared_utils/ia_back_client.py`
3. **`.claude/hooks/meta-commentary-detector.py`** — ajout `is_inside_neo_ia()` + garde dans `is_in_scope()` (anti pollution cross-repo). Syntaxe + comportement testés OK.

## Reste à faire (1 fix, à faire DANS neo_ia)

### FIX — `.claude/hooks/spec-brief-boundary-guard.py:194-206` : gate structure documentaire → advisory

**Problème** : `check_required_sections()` (Gate 1, `exit 2`) BLOQUE l'écriture d'un BRIEF si des sections obligatoires (Surface à consommer / Intention attendue / Anti-patterns checklist) manquent. Gate de **structure documentaire / workflow process**, pas lint/security/scope → viole doctrine 22 mai.

**NE PAS toucher** : Gate 2 (forbidden-patterns cross-repo) = scope légitime.

**Fix** : transformer Gate 1 de blocking (`exit 2`) en advisory (`print(..., file=sys.stderr)` + `exit 0`). Garder Gate 2 intact. Ajuster les tests adverses du hook. Valider : Gate 2 bloque toujours, Gate 1 ne bloque plus.

## P2 optionnels (si tu veux pousser)

- `.claude/skills/done/SKILL.md` — vérifier le nom du serveur MCP (`mcp__neoteem-brain__*` vs `obsidian-brain` réel) contre le `.mcp.json` de neo_ia.
- `rules/implementation-notes.md` vs `skills/spec` / `notes` — incohérence chemin `apps/<app>/docs/` vs `docs/` racine.
