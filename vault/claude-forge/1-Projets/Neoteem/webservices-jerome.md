---
titre: "Webservices Jérôme — Correspondance / AG / Drive (actions métier réutilisables)"
resume: "Jérôme expose 3 webservices métier réutilisables : envoi mail Correspondance, ajout résolution AG, classement Drive. À solliciter pour toute feature touchant ces actions, ne pas réimplémenter"
aliases:
  - "webservices jerome"
  - "ws jerome"
  - "correspondance jerome"
  - "ag jerome"
  - "drive jerome"
  - "webservices metier neoteem"
type: technique
derniere-maj: 2026-05-28
auteur: claude
tags:
  - "#type/technique"
  - "#projet/neoteem"
  - "#domaine/architecture"
---

## Périmètre

Jérôme gère 3 webservices métier existants, réutilisables par n'importe quelle feature Neoteem :

| Webservice | Périmètre | Contexte syndic | Contexte gérance |
|------------|-----------|-----------------|------------------|
| **Correspondance** | Envoi mail tracé, trames pré-remplies, PJ modifiables, historique de correspondance | Destinataires par défaut = Conseil Syndical (CS) | Destinataires par défaut = propriétaire(s) du mandat |
| **Résolution AG** | Rattachement de documents à une résolution AG existante ou création d'une nouvelle | Syndic uniquement | N/A (gérance n'a pas d'AG) |
| **Drive** | Classement de documents dans le Drive client avec labellisation contextuelle + déduplication par contenu | Labels = copropriété / immeuble | Labels = mandat / propriétaire / lot |

## Règle d'archi

Pour toute feature qui doit envoyer un mail, ajouter à une AG, ou classer dans le Drive : **ne pas réimplémenter, solliciter Jérôme pour les endpoints**. Surtout pas dans neo_ia ni ia_back (cf [[archi-backs-neoteem]]).

## À récupérer avant intégration (checklist)

- [ ] URLs / endpoints exacts (env dev / preprod / prod)
- [ ] Contrat d'entrée/sortie (payload attendu, format de réponse, codes d'erreur)
- [ ] Auth (token, header, scope)
- [ ] Couverture cas limites (CS non constitué, pas d'AG en préparation, doublon de contenu, etc.)
- [ ] Règles de gestion appliquées dans le webservice vs à implémenter côté appelant (détection contexte syndic/gérance, déduplication, labels contexte)

## Sous-ticket recommandé

Sur toute feature qui sollicite ces webservices, créer un sous-ticket de cadrage côté Jérôme en dépendance, pour qu'il documente les contrats avant l'implé côté appelant.

## Origine

Confirmé par Raphael session 28 mai 2026 lors de la rédaction du commentaire ticket comparatif devis (étapes 4-5 actions post-comparaison).

## Liens

- [[archi-backs-neoteem]] — Pourquoi ces webservices et pas neo_ia / ia_back
- [[stockage-fichiers-neoteem]] — Drive client = canal de stockage fichiers
- [[ia_back]] — Backend IA Jérôme (projet principal)
