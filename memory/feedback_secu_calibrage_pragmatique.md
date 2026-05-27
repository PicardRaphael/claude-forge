---
name: secu-calibrage-pragmatique
description: Raphael accepte le risque sécu sur base test si effort de fix > impact. JAMAIS de nouveau secret committé. Anciens secrets déjà compromis = pragmatique
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2e41f528-a0ac-468c-a271-ba63d887cbd2
---

Calibrage sécu Raphael : la rigueur "JAMAIS de secret en clair" reste absolue pour les NOUVEAUX commits (template + .gitignore + var d'env). Mais pour les secrets DÉJÀ compromis dans l'historique git d'une **base de test**, Raphael accepte le risque si la remédiation est coûteuse (force push, équipe à prévenir).

> NOTE : ce feedback a été rétroactivement nettoyé le 2026-05-27 lors de l'audit Mémoire Portable. Le secret réel (mot de passe PostgreSQL prod + IP serveur) a été retiré et remplacé par `[REDACTED]`. La leçon ci-dessous reste valide.

**Why** : observé session 22 mai 2026.
- `.mcp.json` ia_back versionné avec `DATABASE_URL=postgresql://postgres:[REDACTED]@[REDACTED]:5432/test` (mdp clair + TLS off).
- Mémoire `secret-in-mcp-json-never` dit "JAMAIS de credentials en clair". Conflit apparent avec décision Raphael "oublie le mdp pas grave fais le reste".
- Résolution : la mémoire reste valide pour PRÉVENIR (template + gitignore créés), mais pour le passé compromis sur base test, rotation + purge historique sont reportées (pas pro de force push sans prévenir Jérôme actif sur repo).

**How to apply** :

Quand tu trouves un secret en clair dans un fichier versionné :

1. **TOUJOURS créer/mettre à jour le template `.X.example`** sans le secret (versionné)
2. **TOUJOURS vérifier .gitignore** que le fichier sensible n'est plus tracké
3. **TOUJOURS documenter dans README** comment initialiser proprement
4. **Évaluer la criticité** :
   - Prod / PII / accès admin → ESCALADE : rotation immédiate + purge historique obligatoire
   - Base de test / sandbox → PROPOSER rotation, mais accepter "risque assumé" si Raphael le dit
5. **Demander avant de purger l'historique git** (`git filter-repo`) — force push casse les copies locales de l'équipe. Toujours prévenir d'abord.

**Anti-pattern** : faire une rotation creds + purge unilatéralement parce que "c'est la best practice". Casse l'équipe (Jérôme avait poussé < 7 jours sur le repo), spam Slack, perte de confiance.

## Liens
- [[secret-in-mcp-json-never]] — règle préventive (toujours valide pour nouveaux commits)
- [[never-commit-foreign-repos]] — pattern adjacent (autonomie sur les autres repos)
- [[org-blocks-github]] — contexte sécu Neoteem
