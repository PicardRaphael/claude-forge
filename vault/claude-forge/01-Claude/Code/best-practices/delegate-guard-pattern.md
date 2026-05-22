---
titre: "Pattern delegate-guard : hook de protection des composants"
resume: "Chaque repo doit avoir un hook PreToolUse qui bloque les edits directs sur SKILL.md, agents/*.md, CLAUDE.md et redirige vers les agents specialises"
aliases:
  - "delegate guard"
  - "hook protection composants"
  - "guard edit direct"
domaine: claude-code
type: best-practice
auteur-source: "Raphael Picard / claude-forge"
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "[[erreur-edit-direct-skills]]"
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
---

## Regle

Chaque projet Claude Code DOIT avoir un hook `delegate-guard` dans PreToolUse (Edit|Write) qui :
1. Bloque les edits directs sur les fichiers proteges (SKILL.md, agents/*.md, CLAUDE.md)
2. Indique quel agent specialise utiliser a la place
3. Autorise les typos < 20 chars (warning sans blocage)
4. Fail-open sur erreur de parsing (ne jamais bloquer par accident)

## Pourquoi

Les rules advisory ("OBLIGATOIRE" ecrit dans un .md) ne sont PAS respectees sous pression. Documente 3 fois (2026-04-26) : 6 skills + 14 agents edites directement en ignorant toutes les rules. Seul un hook deterministe (exit 2) empeche reellement l'erreur.

## Comment appliquer

### 1. Adapter au langage du projet

| Stack projet | Format hook | Runner |
|-------------|-------------|--------|
| TypeScript/Bun | `.ts` | `bun .claude/hooks/delegate-guard.ts` |
| Python | `.py` | `python3 .claude/hooks/delegate-guard.py` |
| Go | `.py` (Python par defaut) | `python3 .claude/hooks/delegate-guard.py` |
| SQL/PL-pgSQL | `.py` (Python par defaut) | `python3 .claude/hooks/delegate-guard.py` |

### 2. Adapter aux agents du projet

Le message de blocage doit referencer les agents DU PROJET, pas ceux de forge :

```
# Si le projet a ses propres agents specialises :
BLOCKED: Direct edit of 'SKILL.md' — use skill-creator agent

# Si le projet n'a PAS d'agents specialises (depend de forge) :
BLOCKED: Direct edit of 'SKILL.md' — use skill-creator agent (from forge)
```

### 3. Adapter le bypass

- `CLAUDE_AGENT` env var = nom de l'agent specialise autorise
- Ou `CLAUDE_DELEGATE_BYPASS=1` pour bypass total (mode urgence)

### 4. Ajouter dans settings.json

Le delegate-guard doit etre le PREMIER hook du matcher Edit|Write (avant les guards specifiques au projet) :

```json
{
  "matcher": "Edit|Write",
  "hooks": [
    { "type": "command", "command": "python3 .claude/hooks/delegate-guard.py", "timeout": 5 },
    { "type": "command", "command": "..." }
  ]
}
```

### 5. Checklist setup nouveau repo

- [ ] Creer `.claude/hooks/delegate-guard.{py|ts}` adapte au langage
- [ ] Ajouter dans `settings.json` PreToolUse, matcher `Edit|Write`, en premiere position
- [ ] Tester : un Edit sur un SKILL.md doit retourner exit 2
- [ ] Tester : un Edit < 20 chars doit passer avec warning
- [ ] Tester : un fichier normal doit passer sans rien

## Implementation de reference

- Python : `claude-forge/.claude/hooks/delegate-guard.py`
- TypeScript : `ia_back/.claude/hooks/delegate-guard.ts`

## Liens

- [[MOC-Claude-Code]]
- [[erreur-edit-direct-skills]] — erreur qui a motive ce pattern
- [[methode-analyser-repo]] — checklist setup projet
