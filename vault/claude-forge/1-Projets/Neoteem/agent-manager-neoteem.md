---
titre: "Agent Manager Neoteem — Application concrète du rôle à Raphael et l'équipe"
resume: "Cas Neoteem du rôle Agent Manager : Raphael joue le rôle informellement sur ia_back/neo_ia/neoteem-brain/bdd/lojii, bus factor=1, knowledge tribal dans forge perso, marketplace privée non officialisée"
aliases:
  - "agent manager neoteem"
  - "claude code DRI neoteem"
  - "raphael agent manager"
  - "rôle claude code neoteem"
  - "gouvernance IA neoteem"
domaine: neoteem
type: context
derniere-maj: 2026-05-20
auteur: claude
tags:
  - "#type/context"
  - "#projet/neoteem"
  - "#domaine/claude-code"
---

## Contexte

Le rôle générique "Agent Manager" est documenté dans [[agent-manager-role]]. Cette note capture **l'application concrète à Neoteem** — qui le joue, comment, et ce qui doit évoluer.

## Qui joue le rôle aujourd'hui

**Raphael Picard** (Lead IA Neoteem) — joue actuellement le rôle d'**Agent Manager** sans titre officiel pour les repos :

- `ia_back` — backend IA FastAPI
- `neo_ia` — monorepo NeoChat/NeoDoc/NeoMail
- `neoteem-brain` — vault Obsidian
- `bdd` — repo PG/PL-pgSQL
- `lojii` — frontend Vue 3 gestion immo

Le setup Claude Code (CLAUDE.md, agents, skills, hooks, rules) est maintenu par Raphael sur tous ces repos.

## Risques actuels

| Risque | Impact | Mitigation possible |
|--------|--------|---------------------|
| **Bus factor = 1** | Si Raphael indispo, le setup ne tient pas | Désigner un binôme apprenant |
| **Knowledge tribal dans claude-forge (perso)** | Asset reste personnel au lieu d'être team | Migrer la partie réutilisable vers neoteem-brain |
| **Marketplace privée non officialisée** | Pas de canal de distribution standardisé | Setup marketplace privée Cowork (cf [[cowork-architecture]]) |
| **Rôle non documenté dans la fiche RH** | Ambiguïté responsabilités, sous-évaluation effort | Documenter dans [[Raphael-Picard]] explicitement |

## Évolutions à considérer

### Court terme (Q3 2026)
- Désigner un binôme apprenant (dev sénior intéressé par l'IA outillage)
- Documenter le rôle dans la fiche [[Raphael-Picard]]
- Migrer ~30% du knowledge forge perso vers neoteem-brain (notes Claude Code réutilisables team)

### Moyen terme (Q4 2026)
- Setup marketplace privée Cowork pour distribuer les plugins/skills approuvées
- Définir politique code review IA (gates, security review obligatoire sur PR > X lignes)
- Formaliser cross-functional working group (Eng + Infosec + Legal)

### Long terme (2027)
- Selon croissance team, transition Phase 2 (Agent Manager officialisé mi-temps) vers Phase 3 (équipe dédiée AI tooling)

## Knowledge perso vs asset team — frontière

| Asset | Où aujourd'hui | Où ça devrait être |
|-------|----------------|---------------------|
| Vault Obsidian forge-brain | claude-forge perso | Reste perso (vault Jarvis) |
| Skills Claude Code réutilisables | claude-forge/.claude/skills/ | Marketplace privée Neoteem |
| Agents spécialisés génériques | claude-forge/.claude/agents/ | Marketplace privée Neoteem |
| Hooks d'enforcement Neoteem | Dupliqués sur chaque repo | Plugin Neoteem distribué |
| Conventions CLAUDE.md communes | Dupliquées sur chaque repo | Plugin Neoteem ou repo template |

## Liens

- [[agent-manager-role]] — Rôle générique (parent conceptuel)
- [[Raphael-Picard]] — Personne qui joue le rôle
- [[neoteem-brain]] — Asset team à structurer
- [[neo_ia]] — Repo monorepo IA
- [[ia_back]] — Repo backend IA
- [[cowork-architecture]] — Marketplaces privées Cowork
- [[comment-ecrire-claudemd]] — Convention à standardiser cross-repo
