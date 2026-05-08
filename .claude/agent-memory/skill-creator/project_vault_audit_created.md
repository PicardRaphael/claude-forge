---
name: vault-audit-skill-created
description: Skill vault-audit créée 2026-05-08 — audit + fix vault forge-brain avec scripts Python déterministes
type: project
---

Skill `/vault-audit` créée le 2026-05-08.

**Why:** Le vault a 96 notes. Un audit manuel est fastidieux. La skill automatise la détection de problèmes qualité (frontmatter, aliases, wikilinks, orphelines).

**How to apply:** Invoquer `/vault-audit` pour un rapport rapide. `/vault-audit fix --dry-run` avant tout fix réel.

## Structure

- `.claude/skills/vault-audit/SKILL.md` — orchestrateur
- `.claude/skills/vault-audit/scripts/audit.py` — scan filesystem, score A/B/C/D
- `.claude/skills/vault-audit/scripts/fix.py` — corrections déterministes uniquement

## Résultat initial (2026-05-08)

- 96 notes analysées
- Score moyen : 94.4/100
- A=84, B=12, C=0, D=0
- 37+ wikilinks cassés (principalement dans les MOCs — notes pas encore créées)
- 13 notes orphelines

## Gotchas appliqués

- `SKIP_DIRS` inclut `.claude` et `agent-memory` pour ne pas scanner les fichiers de mémoire agent
- `sys.stdout.reconfigure(encoding='utf-8')` ajouté pour Windows CP1252
- Fix mode = déterministe seulement. Aliases/resume = suggestions interactives jamais auto-appliquées
- `property:set` CLI existe mais fix.py écrit le frontmatter directement (plus fiable, évite le bug `:` CLI)
