---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-24
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Maintenance config `.claude/` — audit ia-workbench (repo de management hors forge) + nettoyage refs mortes forge après suppression de 2 skills.

## Derniere session (2026-06-24)
### Decisions prises
- **ia-workbench** : audit post-refonte du workflow `/spec` (modèle epics-jira → Module/4 familles de Stories REPO·UX·DevOps·QA → Sous-tâches). 4 casses réparées (`.mcp.json` résidu forge-brain → vidé ; SKILL.md préfixe Atlassian doublon + table routage incomplète ; tracker `.skill-recommendations-session` jamais reset → /spec ne se recommandait plus ; doc feature périmée). Puis audit conformité (repo-inspector, 92→100 : `permissionMode: plan` ajouté à repo-explorer). Atlassian = `mcp__plugin_atlassian_atlassian__*`. Commité `e80ea48` (repo LOCAL, pas de remote → pas de push).
- **claude-forge** : suppression par Raphael des 2 skills forge `spec` + `neoteem-back-ts`. Nettoyage des refs mortes (rules/comportement-proactif `, spec` retiré ; mémoire projet + MEMORY.md alignés). Commité+poussé `aa5ca5c` (main).
- Distinction clé : `/spec` survit via plugin PO `neoteem-admin` (shadow) → refs gardées ; `neoteem-back-ts` = nom de repo VIVANT, seule la skill forge est morte.

### En cours
Rien — 2 chantiers clos. Forge poussé (main @ aa5ca5c). ia-workbench commité local (e80ea48, pas de remote).

### Prochaines etapes
- ia-workbench : TROU 1 (oracle/rubrique de « ticket parfait », BLOCKING du DA 18 juin) à traiter avant d'allumer un loop d'exécution ; script de sync modules-jira → mono-repo ; dry-run réel de `/spec`.
- `/clean-memory` : memory/ forge toujours au-dessus du WARNING 250.

## Fils ouverts
- Capitalisation cette session : `[[audit-claude-folder-pattern]]` enrichi (gotcha « refonte interne casse l'index de recâblage ») + feedback `verifier-shadow-plugin-avant-ref-morte` (tier-2).
- Forge : 2 explorations vault non trackées + `output/claude-switcher.js` + notes vault (agents-architecture, architecture-langgraph, rag-evaluation) modifiées AVANT cette session, laissées hors commit — à traiter par Raphael.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
