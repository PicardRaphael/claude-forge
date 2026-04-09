# Projet : Dev Tools — Claude Code pour les developpeurs

**Date :** 9 avril 2026
**Porteur :** Raphael Picard

---

## Le probleme

Aujourd'hui quand un dev travaille sur un repo :
- Il ne connait pas le contexte metier (pourquoi cette table, cette regle de calcul)
- Chaque repo a une configuration Claude Code differente (ou pas du tout)
- Les bonnes pratiques ne sont pas partagees entre les devs
- Un nouveau dev met du temps a comprendre l'existant (200+ tables, 1000+ fonctions PG)

## La solution

**neoteem-brain** : un vault de connaissances metier partage que Claude consulte avant de coder.

Quand un dev demande "modifie le calcul des charges" :
1. Claude cherche dans le vault → trouve les regles metier, tables, fonctions PG
2. Code avec le contexte complet des le premier jet
3. Capitalise ce qu'il decouvre pour les prochains

## Ce qui est deja en place

| Repo | Statut |
|------|--------|
| ia_back (backend Bun/Hono) | Complet — 11 agents, 16 skills, connexion vault |
| neoteem-brain (vault) | Complet — 4 agents, 480+ notes, Agent Teams |
| neo_ia (backend IA Python) | Basique — a configurer |
| bdd, ws, et ~125 autres | A connecter |

## Ce que ca change

| Avant | Apres |
|-------|-------|
| Dev code sans contexte metier | Dev code avec le contexte (vault) |
| Chaque dev a sa propre config Claude | Config partagee et coherente |
| Nouveau dev = 2 semaines pour comprendre | Nouveau dev = Claude explique tout |
| Erreurs par meconnaissance du metier | Claude connait les regles metier |

## Ce qu'il faut pour continuer

| Action | Qui | Effort |
|--------|-----|--------|
| Connecter neo-brain aux repos actifs (copier le kit) | Raphael | 15 min/repo |
| Configurer .claude/ par repo (agents adaptes au stack) | Raphael | 1-2h/repo |
| Former les devs | Raphael | 30 min/equipe |

**Pas besoin de GitHub.** Tout fonctionne avec Bitbucket.

**Cout supplementaire :** zero (Claude Code inclus dans l'abonnement Team)
