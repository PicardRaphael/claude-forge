---
name: delegate-guard-scope-tout-skillmd
description: delegate-guard.py bloque l'écriture de TOUT fichier nommé SKILL.md, y compris hors .claude/skills/ (ex output/). Match par nom de fichier, pas par chemin. Déléguer à skill-creator même pour des skills hors forge.
metadata:
  type: feedback
---

`delegate-guard.py` (hook PreToolUse Write|Edit) bloque l'écriture directe de **tout** fichier nommé `SKILL.md`, peu importe son emplacement — y compris hors `.claude/skills/` (ex `output/`). Le matcher est sur le **nom de fichier**, pas sur le chemin `.claude/`. Vérifié 3 juin 2026 sur `output/po-lojii/skills/spec/SKILL.md`.

**Why:** Une supposition raisonnable sur le scope d'un hook (grep du chemin) ≠ vérification empirique. J'avais conclu que le hook ne mordrait pas hors `.claude/` ; faux.

**How to apply:** Pour créer/modifier n'importe quel `SKILL.md` (même hors forge, ex plugins dans `output/`), déléguer à `skill-creator` — pas d'Edit/Write direct. Si le contenu est déjà conçu et validé, briefer explicitement skill-creator « écris ce contenu VERBATIM, ne régénère pas » (sinon il réécrit et fait perdre la profondeur). Cf [[erreur-subagent-bypass-delegate-guard]] (ne jamais contourner le hook).
