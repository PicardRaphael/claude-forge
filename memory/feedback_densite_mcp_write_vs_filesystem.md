---
name: densite-mcp-write-vs-filesystem
description: Critère "densité MCP write" pour KILL/PIVOT agent→skill = écritures MCP VAULT en boucle UNIQUEMENT. Write/Edit filesystem (.claude/, code, skills) marchent en sous-agent → hors critère. Confondre les deux = faux candidats KILL (4 créateurs faussement flaggés). Audit 27 mai : 0 candidat sur 10 agents.
metadata:
  type: feedback
---

Quand on applique le critère "densité d'écriture MCP" (cf [[pattern-mcp-brief-then-direct]], KILL vault-maintainer) pour décider si un agent doit devenir une skill, le critère cible **uniquement l'écriture MCP vault** (`create_note`/`append_note`/`update_property`/`insert_section` × N en boucle), car le MCP est décoratif en sous-agent (`No such tool available`).

**Write/Edit sur le filesystem** (`.claude/`, code Python, fichiers skills) **fonctionnent normalement en sous-agent** → hors critère. Les créateurs (agent-creator, skill-creator, claudemd-optimizer, hook-creator) écrivent BEAUCOUP mais sur le filesystem, et leur `mcp__forge-brain__*` sert à la LECTURE (`read_note` canoniques), pas à l'écriture vault.

**Why:** Confondre write filesystem et write MCP vault produit des faux candidats KILL. L'audit transverse du 27 mai aurait flaggé 4 créateurs comme "denses" à tort si la distinction n'avait pas été faite.

**How to apply:** Avant de classer un agent "dense", grep le préfixe exact `mcp__forge-brain__(create_note|append_note|update_note|update_property|insert_section|bulk_update_property)` dans son corps — pas juste `Write|Edit`. Seul l'écriture MCP vault dense en boucle déclenche le verdict KILL/PIVOT. Résultat audit 27 mai : 0 candidat sur 10 agents (vault-maintainer était le cas isolé). Lié à [[visibilite-vs-consommation-demi-fix]] (tracer le vrai consommateur) et [[verify-exhaustive-claims]].
