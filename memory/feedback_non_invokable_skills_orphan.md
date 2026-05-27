---
name: non-invokable-skills-must-be-referenced
description: "Skills user-invokable:false doivent être dans skills: frontmatter + body d'une autre skill, sinon orphelines"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e6b6877c-05fe-485a-991f-1162ad5fc575
---

Skills avec `user-invokable: false` ne sont triggées QUE si une autre skill les référence dans son `skills:` frontmatter ET les mentionne dans son body avec instructions d'usage.

**Why:** Découvert sur neo_ia le 2026-05-18 — `gemini-prompting` était `user-invokable: false` mais aucune autre skill ne la référençait. Résultat : Claude ne savait pas qu'elle existait et modifiait les prompts Gemini sans appliquer les conventions.

**How to apply:**
- Skills de RÉFÉRENCE/CONVENTIONS (patterns, rules, architecture, best practices) → TOUJOURS `user-invokable: true` pour que Claude les consulte spontanément en codant
- Skills UTILITAIRES INTERNES (templates rapport, setup paths, format output) → `user-invokable: false` OK car chargées par un agent/workflow spécifique
- Si une skill est `false`, vérifier qu'au moins un agent/skill parente la référence dans `skills:` + body
- Lors d'un audit repo ([[config-guardian-audit-pattern]]), vérifier les skills orphelines ET les skills référence mal marquées `false`
