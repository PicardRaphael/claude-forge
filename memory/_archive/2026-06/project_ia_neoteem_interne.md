---
name: ia-projet-neoteem-interne
description: Google Drive "IA Projet Neoteem Interne" — dossier Projets (patron) + Technique (devops). Support brain + dev tools + GitHub pour Cowork.
type: project
originSessionId: b8821289-a77e-4c03-9a03-e61d32124156
---
## Google Drive : IA Projet Neoteem Interne

Structure du Drive partage pour les projets IA Neoteem :
- `Projets/` — docs business pour le patron (pourquoi, KPIs, planning)
- `Technique/` — docs techniques pour DevOps (setup, architecture, scripts)

## Projets en cours (avril 2026)

### 1. Support Brain
- Vault partage via dossier reseau pour l'equipe support (non-technique)
- Claude Cowork (Desktop) pointe vers le dossier
- Plugin Cowork auto-update via GitHub (seul cas necessitant GitHub)
- DevOps gere le git sync en background (Bitbucket)
- Skills a definir avec l'equipe support

### 2. Dev Tools
- Chaque repo a sa propre config .claude/ adaptee au stack
- neoteem-brain = point commun (tous les repos se connectent via neo-brain)
- Plugin Bitbucket optionnel pour composants partages
- Pas besoin de GitHub pour les devs

## Contrainte orga

- Orga "Claude IA" Team plan
- Admin doit connecter GitHub pour les plugins Cowork (support)
- Raphael est "Utilisateur" pas admin — ne peut pas connecter GitHub lui-meme
- Bitbucket suffit pour les devs (Claude Code poll git URL toutes les heures)

**Why:** Raphael prepare les projets IA pour Neoteem. Le Drive est le support de communication vers la direction et les DevOps.

**How to apply:** Quand on genere des docs projet, respecter la separation Projets/ (business, simple) et Technique/ (setup, code, architecture). Les docs Projets ne doivent pas contenir de code ou de commandes techniques.
