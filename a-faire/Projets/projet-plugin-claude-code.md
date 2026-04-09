# Projet : Plugin Claude Code — Agents et skills partages pour les devs

**Date :** 9 avril 2026
**Porteur :** Raphael Picard

---

## Le probleme

Aujourd'hui chaque repo a sa propre copie des agents et skills dans `.claude/`. Quand on ameliore un agent (ex: code-reviewer) :
1. Corriger dans ia_back
2. Copier dans neo_ia
3. Copier dans bdd
4. Copier dans ws
5. ... x128 repos

C'est ingerable. Les repos ont des versions differentes, certains n'ont rien.

## La solution

Un **plugin Bitbucket** qui contient les agents et skills communs. Chaque repo le reference — un seul push met tout le monde a jour.

```
Un dev ameliore le code-reviewer
  → Push sur Bitbucket (1 repo)
  → Claude Code detecte le changement (poll 1h)
  → Tous les devs sur tous les repos ont la nouvelle version
```

**Pas besoin de GitHub.** Bitbucket suffit pour Claude Code.

## Ce que contient le plugin

### Skills partagees (connaissances communes)

Des skills qui s'appliquent a tous les repos Neoteem, quel que soit le stack :
- Conventions API REST Neoteem
- Regles SQL PostgreSQL
- Patterns d'architecture
- Connexion au vault neoteem-brain (neo-brain)
- Etc.

Les skills specifiques a un stack (Drizzle pour ia_back, Go pour ws) restent dans le repo concerne.

### Agents partages (roles communs)

Des agents qui ont le meme comportement partout :
- code-reviewer (review qualite)
- test-writer (ecriture de tests)
- security-auditor (audit securite)
- Etc.

Les agents specifiques a un repo (refactor-pg-function pour ia_back) restent dans le repo.

### Ce qui n'est PAS dans le plugin

- **Rules** → specifiques a chaque repo (routing, workflows)
- **Hooks** → specifiques au stack (linting TS vs Python vs Go)
- **Agents metier** → specifiques au domaine du repo

## Ce que ca change

| Avant | Apres |
|-------|-------|
| Copier .claude/ dans chaque repo | 1 reference dans settings.json |
| Versions differentes par repo | 100% identique partout |
| Correction = copier dans N repos | 1 push = tout le monde a jour |
| Nouveau repo = tout recreer | Ajouter 3 lignes dans settings.json |

## Lien avec neoteem-brain

Le plugin et neoteem-brain sont complementaires :
- **neoteem-brain** = le vault de connaissances metier (tables, fonctions PG, domaines, decisions)
- **Plugin Claude Code** = les outils de travail (agents, skills)
- Le plugin inclut la skill `neo-brain` qui connecte au vault

```
Plugin (outils)  +  neoteem-brain (connaissances)  =  dev qui code avec contexte complet
```

## Ce qu'il faut pour lancer

| Action | Qui | Effort |
|--------|-----|--------|
| Creer repo Bitbucket `neot-v2/claude-dev-tools` | DevOps | 5 min |
| Extraire les agents/skills communs | Raphael | 1 jour |
| Ajouter `enabledPlugins` dans les repos actifs | DevOps | 5 min/repo |
| Former les devs | Raphael | 30 min |

**Cout supplementaire :** zero

## Planning

| Semaine | Livrable |
|---------|---------|
| S1 | Repo Bitbucket cree + plugin structure |
| S2 | Agents et skills communs extraits + testes |
| S3 | Deploye sur les repos prioritaires (ia_back, neo_ia, bdd, ws) |
| S4 | Formation + deploiement progressif sur les autres repos |
