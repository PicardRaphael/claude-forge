# Projet : Support Brain — Assistant IA pour l'equipe support

**Date :** 9 avril 2026
**Porteur :** Raphael Picard

---

## Le probleme

Aujourd'hui quand un support recoit un ticket :
- Il cherche dans sa memoire ou demande a un collegue
- Les solutions passees ne sont pas capitalisees
- Chaque support refait le meme travail de recherche
- Les nouveaux mettent des semaines a etre autonomes

## La solution

Un assistant IA (Claude Cowork) connecte a une **base de connaissances partagee** :
- Le support decrit le probleme → Claude cherche dans la base → propose une reponse
- Chaque resolution enrichit la base automatiquement
- Le prochain support qui a le meme probleme → Claude trouve directement
- Formation acceleree : le nouveau a acces a toute l'experience de l'equipe

## Comment ca marche pour le support

```
1. Le support ouvre Claude Desktop (deja installe sur son poste)
2. Il colle le ticket ou decrit le probleme du client
3. Claude cherche dans la base :
   - FAQ : "Ah, question frequente sur les prelevements"
   - Solutions : "3 tickets similaires deja resolus comme ca"
   - Process : "Voici la procedure officielle"
4. Claude propose une reponse structuree
5. Le support valide, modifie si besoin, envoie au client
6. Claude memorise la resolution pour les prochains
```

## Ce que ca change

| Avant | Apres |
|-------|-------|
| Chaque support cherche seul | Claude a la memoire collective |
| Les solutions sont dans les tetes | Les solutions sont ecrites et retrouvables |
| Nouveau support = 3 semaines de formation | Nouveau support = 1h de formation + Claude |
| Escalade a tort vers les devs | Claude sait quand et a qui escalader |
| Memes questions posees 10x | Claude repond en 30 secondes |

## Resultats attendus

| Metrique | Estimation |
|----------|-----------|
| Temps moyen de resolution | -40% |
| Tickets escalades a tort | -60% |
| Temps de formation nouveau support | -50% |
| Base de connaissances | +10 solutions/semaine (auto) |

## Ce qu'il faut pour lancer

| Action | Qui | Effort |
|--------|-----|--------|
| Connecter GitHub a l'orga Claude (voir doc technique) | Admin | 5 min |
| Creer le dossier partage sur le serveur | DevOps | 30 min |
| Installer Claude Desktop sur les postes support | DevOps | 15 min/poste |
| Rediger la base initiale (FAQ, process) | Raphael + support lead | 2 jours |
| Creer le plugin support | Raphael | 2 jours |
| Former l'equipe (session collective) | Raphael | 1h |

**Cout supplementaire :** zero (Claude Desktop inclus dans l'abonnement Team actuel)

## Planning

| Semaine | Livrable |
|---------|---------|
| S1 | Infra prete (dossier partage, GitHub connecte) |
| S2 | Base initiale redigee + plugin cree |
| S3 | Formation + lancement pilote (2-3 supports) |
| S4 | Retour d'experience + ouverture a toute l'equipe |

## Questions a valider

- Combien de supports vont l'utiliser ?
- Quel outil de ticketing ? (Jira, Freshdesk, email ?)
- Qui sera le referent support pour alimenter la base ?
- Types de tickets les plus frequents ?
