---
titre: "Critique — Setup Claude Code complet lojii (Vue 3)"
resume: "4 bloquants : .claude/ gitignore invalide parite, windev-migrator hors echelle (914 ecrans), aucun hook enforcement, CLAUDE.md fantomes non traite"
aliases:
  - critique lojii setup
  - critique setup claude code lojii
  - critique parite lojii neo_ia
  - devil advocate lojii mai 2026
  - DA lojii
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-13
auteur: claude
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/lojii"
  - "#domaine/claude-code"
---

## Contexte

Proposition de deployer 12 agents, 15 skills, 12 rules, 8 hooks sur le projet lojii (frontend Vue 3, 634 composants, 914 ecrans WinDev a migrer) pour atteindre la parite avec [[neo_ia]] et [[ia_back]].

## Verdict

**LIVRER AVEC CORRECTIONS** — 4 bloquants, 6 avertissements, 3 nitpicks.

## 4 Bloquants

### 1. `.claude/` dans .gitignore + 12 agents = scope invalide
`.claude/` non partage = setup personnel Raphael. Deployer 47 composants (12+15+12+8) pour un seul utilisateur = dette de maintenance abandonnee en 3 mois. Soit retirer du `.gitignore`, soit reduire le scope (5-6 agents max).

### 2. `windev-migrator` agent unique pour 914 ecrans
Un agent migre UN ecran a la fois. Sans pipeline (inventaire, batching, etat persistant, review humaine), on perd la trace entre sessions. Le livrable doit etre un **pipeline de migration**, pas un agent.

### 3. Aucun hook d'enforcement de workflow
12 rules "OBLIGATOIRE" sans architect-guard ni commit-guard avec markers. 3 incidents documentes dans le vault prouvent que les rules advisory echouent a 80%. Le pipeline `architect → dev → reviewer → test` sera ignore des la 3e session.

### 4. CLAUDE.md 330L fantomes non traite comme prerequis
Ajouter 15 skills sur un CLAUDE.md qui reference des composants inexistants = doubler la confusion. Cleanup = prerequis bloquant.

## Chemin recommande

3 phases : Phase 0 (cleanup + decision .gitignore + adaptation Bitbucket) → Phase 1 (3 agents + 4 skills + 4 rules + 4 hooks enforcement) → Phase 2 (pipeline migration WinDev avec batching). Expansion Phase 3 seulement apres 2 semaines de Phase 1 fonctionnelle.

## Pattern identifie : parite forcee multi-repo

Copier la config d'un repo (neo_ia) vers un repo de nature differente (lojii) sans adapter = antipattern recurrent. Chaque repo a des besoins specifiques. Le bon objectif n'est pas "meme nombre d'agents" mais "memes principes (hooks, conventions, pipeline) adaptes au contexte".

## Liens

- [[erreur-advisory-rules-insuffisantes]] — rules ignorees sans hooks
- [[erreur-skill-monolithique-sans-references]] — lojii-conventions risque le meme sort
- [[erreur-edit-direct-skills]] — deploiement par edit direct = non conforme
- [[lojii]] — note projet
- [[neo_ia]] — repo source de la parite
- [[ia_back]] — repo source de la parite
