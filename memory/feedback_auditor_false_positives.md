---
name: auditor-false-positives-verify-claims
description: "Les project-auditor produisent régulièrement des faux positifs sur skills \"inexistantes\" (skills plugin scope user) et \"allowed-tools obligatoire\" (en fait optionnel). TOUJOURS vérifier empiriquement les claims douteux avant consolidation."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 364d9af7-1c65-4939-8a88-e0a5dae926ea
---

Erreurs récurrentes des project-auditor découvertes pendant audit neo_ia + ia_back 22 mai.

**Why:** Les sub-agents ne checkent pas systématiquement `~/.claude/plugins/installed_plugins.json` ni la doc Anthropic. Ils signalent comme "fantôme" des skills déployées par plugin scope user. Ils signalent comme "bloquant" `allowed-tools` manquant alors qu'Anthropic dit explicitement "all fields are optional".

**How to apply:**
- Avant consolidation rapport, vérifier les claims critiques :
  - Skill listée comme "inexistante" → `grep "<nom-skill>" ~/.claude/plugins/installed_plugins.json` (plugins scope user actifs partout)
  - "`allowed-tools` obligatoire" → FAUX selon code.claude.com/docs/skills (optionnel)
  - "`skills:` invalide dans SKILL.md" → vrai (subagent-only) mais champ inconnu = ignoré silencieusement, pas un crash
  - "Agent inexistant `db-inspector`/`api-designer`" → spec-specific (ia_back oui, neo_ia non — vérifier scope)
- Web search Anthropic docs en doute avant de classer un claim "bloquant"
- Le DA challenge utile sur ces cas mais peut planter (PowerShell heredoc bugs) — toujours vérifier manuellement quand DA absent

Patterns confirmés via vérif empirique 22 mai :
- neo-brain-dev-ia = vraie skill plugin `neoteem-brain-dev-ia@neoteem` v3.0.0 scope user
- superpowers:executing-plans = plugin officiel, à installer par repo
- `Agent` dans `allowed-tools` skill = INVALIDE, utiliser `Task`
