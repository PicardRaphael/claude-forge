---
titre: "Agent Manager / DRI — Rôle org émergent pour Claude Code"
resume: "Rôle hybride PM/eng dédié à la gouvernance et l'évolution du setup Claude Code dans une organisation — alternative légère le DRI individuel"
aliases:
  - "agent manager"
  - "claude code DRI"
  - "agent manager role"
  - "claude code governance role"
  - "developer productivity claude code"
  - "rôle agent manager"
domaine: claude-code
type: best-practice
derniere-maj: 2026-05-20
auteur: claude
sources:
  - "https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start"
  - "Anthropic Applied AI — Claude Code at scale (14 mai 2026)"
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#projet/neoteem"
---

## Le constat Anthropic

> "The rollouts that spread fastest had a dedicated infrastructure investment before broad access. A small team, sometimes even just one person, wired up the tooling so Claude already fit developer workflows when they first touched it."

Les déploiements Claude Code qui marchent ont **systématiquement** une personne (ou une petite équipe) qui possède le sujet AVANT le rollout général. Sinon : adoption fragmentée, knowledge tribal, plateau d'adoption.

## Les 3 niveaux d'investissement

| Niveau | Rôle | Quand |
|--------|------|-------|
| **Équipe dédiée** | "AI coding tools team" | > 500 devs, gros monorepo |
| **Agent Manager** (rôle émergent) | Hybride PM/eng, mi-temps ou plein-temps | 50-500 devs |
| **DRI** (Directly Responsible Individual) | Un seul humain, 10-20% de son temps | < 50 devs ou bootstrap |

## Responsabilités du rôle (peu importe le niveau)

- **Settings** : politique permissions, hooks org-wide, settings managées
- **Marketplace plugins** : quels plugins sont approuvés, comment les distribuer
- **CLAUDE.md conventions** : standardiser la hiérarchie root + subdir
- **Skills curées** : liste des skills officielles validées par l'org
- **Code review IA** : process pour code généré par Claude (security review, gates)
- **Gouvernance** : règlement IA (legal, infosec), accès, audit

## Où loger ce rôle ?

> "The teams doing this work today tend to sit under developer experience or developer productivity, which is typically the function responsible for onboarding new engineers and building developer tooling."

→ Pas dans une équipe produit. Pas dans l'infra pure. **DevEx / Developer Productivity** est le bon home.

## Pattern d'évolution typique

```
Phase 0 : Personne                          → adoption sauvage, knowledge tribal
   ↓
Phase 1 : Un DRI émerge (volontaire)        → premiers patterns documentés, premiers plugins
   ↓
Phase 2 : Agent Manager officialisé         → marketplace privée, governance, formation
   ↓
Phase 3 : Équipe dédiée                     → multi-tools (Cursor, Codex), policy globale
```

## Application à Neoteem

Cas concret : Raphael = Lead IA Neoteem, joue actuellement le rôle **Agent Manager** sans titre officiel pour les repos ia_back, neo_ia, neoteem-brain, bdd, lojii.

**Risques actuels :**
- Bus factor = 1 (si Raphael indispo, le setup ne tient pas)
- Knowledge tribal dans claude-forge (perso) au lieu d'un asset Neoteem partagé
- Pas de marketplace privée Neoteem encore officialisée

**Évolutions à considérer :**
- Designer un binôme apprenant (futur Agent Manager)
- Migrer une partie du knowledge forge perso vers neoteem-brain (asset team)
- Documenter le rôle explicitement dans la fiche de Raphael (cf [[Raphael-Picard]])

## Gouvernance — questions à trancher tôt

Selon Anthropic, ces 4 questions reviennent systématiquement en enterprise :

1. **Qui contrôle quelles skills/plugins sont disponibles ?**
2. **Comment éviter que N devs rebuilent la même chose ?**
3. **Comment garantir que le code IA passe la même review que le code humain ?**
4. **Quelle est la politique d'accès et d'audit ?**

Réponses minimales pour démarrer (recommandation Anthropic) : ensemble défini de skills approuvées, process de code review obligatoire, accès initial limité, expansion par confiance acquise.

## Anti-patterns

- ❌ "Adoption bottoms-up suffit" → marche au début, plateau garanti après 6 mois
- ❌ DRI à temps zéro (juste un nom sur une page) → personne ne fait le boulot, fragmente quand même
- ❌ Loger le rôle dans Infra/Security uniquement → angle DevEx manquant, adoption faible
- ❌ Attendre une décision top-down avant de bouger → l'adoption se fait en attendant, mais mal

## Liens

- [[claudemd-guide]] — Convention CLAUDE.md à standardiser
- [[skills-guide]] — Catalogue skills à curate
- [[Raphael-Picard]] — Joue ce rôle pour Neoteem
- [[neoteem-brain]] — Asset team à structurer
- [[cowork-architecture]] — Marketplaces privées
