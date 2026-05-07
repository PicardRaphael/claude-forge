---
description: "Dispatch table: which agent or skill to invoke based on user situation"
---

# Comportement proactif — Dispatch

| Situation | Action |
|-----------|--------|
| Besoin flou / "comment automatiser X" | Invoquer `cc-advisor` |
| "J'ai un projet X" / URL GitHub | Invoquer `project-analyzer` |
| "Optimise / améliore mon CLAUDE.md" | Invoquer `claudemd-optimizer` |
| "Quoi de neuf / est-ce que X existe" | Invoquer `cc-news` |
| "Crée un agent / skill / hook" | Vérifier l'existant → créer |
| Skill à optimiser | Lire l'existant → améliorer |
| "Audite ce projet / vérifie la config" | Agent `project-auditor` |
| "Configure Cowork / Dispatch / tâche planifiée" | Skill `cc-cowork-ref` |
| Amélioration de prompt / description | Skill `cc-prompt-ref` |
| "Crée un prompt pour X" | Skill `craft-prompt` (Claude, Gemini, tout LLM) |
