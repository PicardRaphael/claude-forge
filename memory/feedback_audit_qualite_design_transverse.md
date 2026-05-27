---
name: audit-qualite-design-transverse-mandatory
description: "Audit `.claude/` = check technique + qualité-design transverse (split/fusion/kill/redondance) référencé aux canoniques forge 22 mai, pas connaissances génériques"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Quand Raphael demande "analyse les skills/agents/hooks/rules de X" :

**Réflexe FAUX** : audit technique uniquement (frontmatter valide, taille, chemins, modèle). Juger en référence aux connaissances génériques sur "comment créer un skill workflow".

**Réflexe CORRECT** : audit technique + qualité-design transverse OBLIGATOIRE :
- **Skills** : monolithiques à diviser, redondantes/chevauchement à fusionner, trop nombreuses (> 30) candidates kill, orphelines réelles
- **Hooks** : redondants à fusionner, workflow hooks INTERDITS doctrine 22 mai (architect-first, TDD strict, markers TTL)
- **Agents** : chevauchement rôles, trop nombreux (> 10), modèle/effort cohérent, JAMAIS agent CTO orchestrateur

**Référentiel canonique OBLIGATOIRE** (via MCP forge-brain) :
- [[methode-analyser-repo]], [[comment-creer-skill]], [[comment-creer-agent]], [[comment-creer-hook]], [[raisonnement-22mai-doctrine-vs-enforcement]]

**Why** : Un agent neo_ia a fait l'erreur 2026-05-22 — audit "skill décrit-il bien le code" sans audit qualité-design transverse. Raphael a dû recadrer. Patché dans project-auditor.md + comportement-proactif.md.

**How to apply** : À toute demande "analyse skills/agents/hooks/rules", project-auditor doit faire les 2 niveaux (technique + qualité-design). Référencer canoniques forge, pas connaissances génériques.

Related : [[feedback_analyse_repo_includes_code]], [[feedback_dispatch_analyse_vs_audit]], [[feedback_audit_repo_method]].
