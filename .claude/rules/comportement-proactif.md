---
description: "Dispatch table: which agent or skill to invoke based on user situation"
---

# Comportement proactif — Dispatch

| Situation | Action |
|-----------|--------|
| Besoin flou / "comment automatiser X" | Invoquer `cc-advisor` |
| "J'ai un projet X" / URL GitHub | Invoquer `project-analyzer` |
| "Analyse les skills/agents/rules de X" / audit config | Agent `project-auditor` (PAS Explore) |
| "Analyse ia_back" / "analyse neo_ia" / multi-repo | Agent `project-auditor` par repo, en parallele |
| "Optimise / améliore mon CLAUDE.md" | Invoquer `claudemd-optimizer` |
| "Quoi de neuf / est-ce que X existe" | Invoquer `cc-news` |
| "Crée un agent / skill / hook" | Vérifier l'existant → créer |
| Skill à optimiser | Lire l'existant → améliorer |
| "Audite le vault / vérifie les notes" | Skill `/vault-audit` ou agent `vault-maintainer` |
| "Configure Cowork / Dispatch / tâche planifiée" | Skill `cc-cowork-ref` |
| Amélioration de prompt / description | Skill `cc-prompt-ref` |
| "Crée un prompt pour X" | Skill `craft-prompt` (Claude, Gemini, tout LLM) |
| Début de session / reprise | `/recap` pour snapshot contexte |

## Anti-patterns de dispatch

- **JAMAIS `Explore` pour auditer un projet** — Explore = recherche rapide read-only, PAS un audit
- **JAMAIS `general-purpose` pour > 8 operations** — decouper en agents paralleles
- **JAMAIS Grep/Read brut sur le vault** — utiliser CLI Obsidian (`obsidian search`, `obsidian read`)
- **JAMAIS un seul agent pour multi-repo** — 1 agent par repo, en parallele
