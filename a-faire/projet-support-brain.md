# Projet : Support Brain — Base de connaissances support partagee

**Public :** Equipe support (non-technique)
**Outil :** Claude Cowork (Claude Desktop)
**Statut :** A creer

---

## Objectif

Creer un **vault de connaissances support** (meme principe que neoteem-brain pour les devs) :
- Les supports utilisent Claude Cowork pour traiter les tickets
- Claude cherche dans la base avant de repondre
- Chaque resolution enrichit la base pour les prochains
- Memoire partagee via dossier reseau (pas de git pour les supports)

---

## Architecture

```
                    DevOps gerent
                         │
Dossier reseau ────── git sync auto ────── Bitbucket (backup)
\\serveur\support-brain\                    neot-v2/support-brain
  │
  ├── FAQ/
  ├── Process/
  ├── Solutions/
  ├── Escalade/
  ├── Templates/
  └── CLAUDE.md
  │
  └── Supports ouvrent Claude Desktop
      pointent vers ce dossier
      Claude lit/ecrit dedans
```

---

## Comment ca marche

### Pour le support (zero technique)

1. Ouvre Claude Desktop (Cowork)
2. Pointe vers le dossier `\\serveur\support-brain\`
3. Colle le ticket ou decrit le probleme
4. Claude cherche dans FAQ/, Process/, Solutions/
5. Propose une reponse
6. Le support valide → Claude capitalise dans Solutions/

### Pour les DevOps (une fois)

1. Creer le dossier reseau partage
2. Init git dans le dossier + remote Bitbucket
3. Script auto-sync (git pull/push periodique en background)
4. Installer Claude Desktop sur les postes support

---

## Lien avec neoteem-brain

```
neoteem-brain (devs)          support-brain (support)
  ├── 01-Domaines/              ├── FAQ/
  ├── 02-BDD/                   ├── Process/
  ├── 03-Apps/                  ├── Solutions/
  ├── Knowledge/                ├── Escalade/
  └── ...                       └── ...
       │                              │
       └──── Liens cross-vault ───────┘
```

Les deux vaults se completent :
- **neoteem-brain** = connaissances techniques (tables, fonctions PG, architecture)
- **support-brain** = connaissances operationnelles (FAQ clients, process, solutions tickets)

A terme, les supports peuvent aussi consulter neoteem-brain (via neo-brain skill dans le plugin Cowork) pour comprendre le contexte technique d'un ticket.

---

## Plugin Cowork "Support Neoteem"

Plugin auto-installe sur les postes support via marketplace Cowork.

**Necessite GitHub** pour l'auto-sync marketplace (voir `proposition-github-cowork.md`).

### Skills du plugin

Les skills seront definies avec l'equipe support selon leurs besoins reels. Exemples possibles :
- Triage automatique de tickets
- Recherche dans la base de connaissances
- Aide a la redaction de reponses
- Escalade intelligente

### Mise a jour

Push sur GitHub → marketplace Cowork detecte → tous les postes support recoivent en 30 min.

---

## Etapes de mise en place

| # | Action | Qui | Quand |
|---|--------|-----|-------|
| 1 | Admin connecte GitHub a l'orga Claude | Admin | Prealable |
| 2 | Creer dossier reseau `support-brain` | DevOps | Semaine 1 |
| 3 | Init git + remote Bitbucket | DevOps | Semaine 1 |
| 4 | Script auto-sync git en background | DevOps | Semaine 1 |
| 5 | Rediger CLAUDE.md + premiers FAQ/Process | Raphael + support lead | Semaine 1-2 |
| 6 | Installer Claude Desktop sur postes support | DevOps | Semaine 2 |
| 7 | Creer le plugin Cowork (skills a definir avec l'equipe) | Raphael | Semaine 2-3 |
| 8 | Publier plugin sur GitHub + marketplace | Raphael + DevOps | Semaine 3 |
| 9 | Formation support (1h) | Raphael | Semaine 3 |
| 10 | Recueil feedback + iteration | Raphael + support lead | Semaine 4+ |

---

## Questions ouvertes (a valider avec l'equipe support)

- Quel outil de ticketing utilisent-ils ? (Jira, Freshdesk, email ?)
- Quels types de tickets sont les plus frequents ?
- Existe-t-il deja une FAQ ou base de connaissances ?
- Combien de supports vont l'utiliser ?
- Qui sera le "support lead" referent pour alimenter la base ?
