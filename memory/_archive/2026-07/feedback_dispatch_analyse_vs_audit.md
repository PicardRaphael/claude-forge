---
name: dispatch-analyse-audit-routing
description: "analyse les skills/agents" = project-auditor PAS Explore. Explore = recherche rapide, jamais audit
type: feedback
originSessionId: 00ed39aa-17db-4d58-bcdc-ef097926d20a
---
Quand l'utilisateur dit "analyse les skills/agents de X", router vers `project-auditor` (audit existant), PAS `Explore` (recherche rapide read-only) ni `project-analyzer` (recommandations from scratch).

**Why:** Session 8 mai 2026 — dans une autre session, "analyse ia_back et neo_ia" a été routé vers un agent Explore qui a juste fait des `ls` sans rien auditer. Le mot "analyse" matchait project-analyzer au lieu de project-auditor.

**How to apply:**
- "analyse skills/agents/config" → project-auditor
- "j'ai un nouveau projet" → project-analyzer
- "cherche un fichier" → Explore
- Multi-repo → 1 project-auditor par repo, en parallèle (jamais 1 seul agent pour tout)
