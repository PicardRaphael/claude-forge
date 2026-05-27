---
name: audit-coherence-pattern
description: "Deep coherence audit checklist: skills orphelines, rules mortes, hooks orphelins, credentials trackés — 8 checks systematiques"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2c8f61e9-59a4-4658-863a-864e27242ec9
---

Checklist audit cohérence .claude/ d'un repo (8 checks) :

1. **Agents → Skills** : chaque skill dans `skills:` frontmatter référencée dans le body
2. **Agents → Tools** : tools cohérents avec le rôle (read-only = pas Write/Edit)
3. **Skills → References** : SKILL.md < 500L, references/ utilisées
4. **Rules → Frontmatter** : chaque rule a `description:` (sinon morte)
5. **Hooks → Settings** : chaque hook dans settings.json existe physiquement
6. **Delegation → Agents** : agents mentionnés dans les rules existent
7. **Memory** : `memory: project` sur tous les agents
8. **Fichiers sensibles** : credentials pas trackés par git

**Why:** Audit 2026-05-21 sur ia_back (43 problèmes) et neo_ia (24 problèmes). Skills orphelines = pattern #1 (11 agents ia_back), rules mortes = pattern silencieux le plus dangereux.

**How to apply:** Lancer cet audit après tout déploiement de setup CC sur un repo. Utiliser `project-auditor` avec ces 8 checks.
