---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, mémoire de travail, état actuel]
type: context
status: active
derniere-maj: 2026-05-21
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---
## Phase actuelle
Capitalisation Code with Claude 2026 terminée. Outcomes-test déployé sur 3 repos. Politique Opus/Sonnet alignée CwC 2026.

## Dernière session (2026-05-21)
### Décisions prises
- Politique modèles : Sonnet exécution (dev), Opus jugement (architect, reviewer, security). Exception dev-neochat = Opus (LangGraph complexe)
- Outcomes-test post-dev (pas post-architect) — évalue du code concret
- permissionMode: acceptEdits obligatoire sur tous agents créateurs
- Mémoire feedback_all_opus remplacée par model-allocation-strategy
- Autocompact 50% ajouté ia_back, Document & Clear ajouté neo_ia

### En cours
- Outcomes-test rule advisory sur ia_back/neo_ia — DA a signalé qu'elle devrait être enforced par hook (pas fait)
- 3 copies outcomes-test byte-identical → risque divergence (DA signalé)

### Prochaines étapes
- Tester /outcomes-test sur un vrai livrable (dev agent code) pour valider le pipeline
- Considérer hook outcomes-guard pour enforcer la rule (advisory = 80% compliance)
- Mesurer taux FAIL code-reviewer Sonnet vs Opus pendant 2-4 semaines
- cc-news Tokyo (10 juin) à surveiller

## Fils ouverts
- MCP Tunnels → évaluer pour brain Neoteem quand GA
- Outcomes rubric hook enforcement (rule advisory insuffisante selon vault)
- Template rubric "spec" à créer si on utilise /spec sur les repos projet

## Liens
[[Raphael-Picard]]
[[Claude-Forge]]
[[Code with Claude 2026]]
