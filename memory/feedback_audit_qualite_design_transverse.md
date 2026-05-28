---
name: audit-qualite-design-transverse-mandatory
description: "Audit `.claude/` = check technique + qualité-design transverse (split/fusion/kill) référencé canoniques forge"
metadata:
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Cf [[audit-claude-folder-pattern]] section "Phase 1 — 4 auditeurs en parallèle" (checklist 4 catégories + canoniques forge obligatoires).

**Cas empirique 2026-05-22** : un agent neo_ia a fait l'erreur — audit "skill décrit-il bien le code" sans audit qualité-design transverse (skills monolithiques à diviser, redondantes à fusionner, > 30 candidates kill, orphelines, hooks workflow INTERDITS doctrine 22 mai, agents chevauchement). Raphael a dû recadrer. Patché dans project-auditor.md + comportement-proactif.md.

**Règle** : à toute demande "analyse skills/agents/hooks/rules", project-auditor doit faire les 2 niveaux. Référencer canoniques forge, pas connaissances génériques.
