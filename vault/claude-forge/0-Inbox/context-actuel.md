---
titre: Context Actuel
resume: Working memory dynamique -- mis a jour par /done, lu par /recap
aliases: [context actuel, contexte courant, working memory, memoire de travail, etat actuel]
type: context
status: active
derniere-maj: 2026-06-06
auteur: claude
tags: ["#type/context", "#meta/working-memory"]
---

## Phase actuelle
Audit + optimisation des skills forge — vague 1 (11 skills) terminée, vague 2 à planifier si nécessaire.

## Dernière session (2026-06-06)
### Décisions prises
- Skills externes (kepano) = intouchables absolument, même pour la description. Déclenchement via .skill-triggers.json uniquement.
- cc-hooks-ref supprimé — absorbé par hook-creator (nettoyage complet : dossier + skill-triggers + note vault).
- argument-hint = champ officiel Anthropic, ajouté à la liste fermée checklist-skill-parfaite.md.
- forge-brain : wildcard mcp__forge-brain__* remplace liste de 22 outils.

### En cours
- Rien de bloqué — toutes les 11 skills auditées, fixes appliqués, commit pushé (f498481).

### Prochaines étapes
- Auditer les skills de la liste "déjà à jour" pour confirmer qu'elles le sont vraiment (skill-creator, subagent-creator, hook-creator, claudemd-creator, responsable-ia, cc-news, forge-review, skill-evolve, align-vault-skills, pivot-check, auditor-empirical-verify, configure-claude-desktop).
- Ou considérer le chantier terminé et passer à autre chose.

## Fils ouverts
- skill-evolve description a changé dans le system-reminder (nouveau wording vu en session) — vérifier si c'est la version à jour ou un drift.
- Checklist `checklist-skill-parfaite.md` mise à jour pour argument-hint — propager la correction à ia_back/neo_ia si ces repos ont leur propre copie.

## Liens
[[2-Casquettes/Raphael-Picard|Raphael Picard]]
[[1-Projets/Claude-Forge/Claude-Forge|Claude-Forge]]
