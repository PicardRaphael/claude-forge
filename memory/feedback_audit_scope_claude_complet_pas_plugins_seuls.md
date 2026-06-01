---
name: audit-scope-claude-complet-pas-plugins-seuls
description: "Auditer un repo = .claude/ COMPLET (agents+scripts+rules), pas juste les plugins distribués"
metadata:
  type: feedback
---

Auditer la config Claude Code d'un repo qui distribue des plugins : auditer le `.claude/` COMPLET du repo source (agents, scripts, rules, hooks), PAS seulement les plugins distribués. Sur neoteem-brain, l'audit des 5 plugins seuls a conclu "Lint manquant / 3 agents redondants / 4 mappings dupliqués" — TOUS faux : le Lint existait (scripts `enrich-references.py` + agents `vault-linker`/`vault-validator`), les agents étaient délimités, 1 seul vrai doublon.

**Why:** Les plugins distribués sont la partie émergée ; la maintenance (scripts, agents, pipeline) vit dans le `.claude/` + `scripts/` du repo, invisible si on regarde que les bundles. Conclusions structurelles fausses garanties sinon.
**How to apply:** Avant tout verdict "X manque / Y est redondant" sur un repo à plugins, cartographier `.claude/agents`, `.claude/skills`, `scripts/`, `.claude/rules` du repo source. Croiser avant de conclure. Cf [[audit-claude-folder-pattern]] (claims faux à vérifier).
