# Pourquoi connecter GitHub a notre organisation Claude

**Date :** 9 avril 2026
**Porteur :** Raphael Picard
**Action requise :** Administrateur de l'organisation Claude IA

---

## En une phrase

Pour que les outils IA se mettent a jour **automatiquement** sur les postes de toute l'equipe, il faut connecter un compte GitHub a notre organisation Claude. C'est une operation de **5 minutes, une seule fois**.

## A qui ca sert

| Equipe | Outil | Besoin GitHub |
|--------|-------|---------------|
| **Support** (non-technique) | Claude Cowork (Desktop) | **Oui** — mise a jour automatique des plugins |
| **Developpeurs** | Claude Code (terminal) | **Non** — Bitbucket suffit |

GitHub est demande **uniquement pour le plugin support** (1 seul repo). Tout le reste continue sur Bitbucket.

## Pourquoi pas Bitbucket pour le support ?

Anthropic (editeur de Claude) a un partenariat technique avec Microsoft/GitHub. Le systeme de mise a jour automatique des plugins Cowork Desktop utilise l'API GitHub. Cette integration n'existe pas pour Bitbucket.

**Concretement :** sans GitHub, l'administrateur devrait re-uploader manuellement le plugin sur chaque poste a chaque mise a jour. Avec GitHub, c'est automatique en 30 minutes.

## Ce que ca ne change PAS

- Bitbucket reste notre outil principal pour le code source (128 repos)
- Aucune migration de code
- Les developpeurs ne sont pas concernes (Bitbucket suffit pour Claude Code)
- Aucun cout supplementaire (GitHub gratuit pour les repos prives, equipes < 5)

## Ce qu'il faut faire

L'administrateur de l'organisation "Claude IA" :
1. Se connecter a **claude.ai** avec le compte admin
2. Aller dans **Parametres** → **Organisation** → **Integrations**
3. Cliquer **Connecter GitHub**
4. Autoriser l'acces (un seul repo necessaire)

C'est tout. Apres ca, Raphael configure le reste.

## Securite

- GitHub est utilise par 100M+ de developpeurs dans le monde
- Le repo peut etre **prive** (visible uniquement par notre equipe)
- Anthropic est partenaire officiel de Microsoft/GitHub
- On peut deconnecter a tout moment sans perdre les outils deja installes
