---
titre: "IDOR détecté — /api/v1/coproprietes/:id/conseil-syndical"
resume: "Security-auditor ia_back a détecté un IDOR : auth présente mais aucun contrôle de scope par copropriété. Un utilisateur authentifié peut accéder aux données d'une autre copro."
aliases:
  - "IDOR conseil syndical"
  - "IDOR coproprietes"
  - "faille securite ia_back"
type: knowledge
domaine: securite
derniere-maj: 2026-05-21
auteur: claude
sources:
  - "Test comportemental ia_back scénario 3c — security-auditor"
tags:
  - "#type/knowledge"
  - "#domaine/securite"
  - "#projet/ia_back"
---

# IDOR — /api/v1/coproprietes/:id/conseil-syndical

## Problème

L'endpoint a un middleware d'auth (utilisateur authentifié requis), mais **aucun contrôle de scope** : un utilisateur authentifié peut passer n'importe quel `id` de copropriété et accéder aux données du conseil syndical d'une copro qui ne lui appartient pas.

## Impact

- **Sévérité** : HIGH (accès non autorisé à des données tierces)
- **Vecteur** : modifier le paramètre `:id` dans l'URL
- **Données exposées** : composition du conseil syndical (noms, rôles)

## Fix recommandé

Ajouter un contrôle de scope dans le middleware ou le use case : vérifier que l'utilisateur authentifié a un lien avec la copropriété demandée (syndic, copropriétaire, gestionnaire).

## Statut

À corriger avant toute mise en production de cet endpoint.

## Liens

- [[synthese-audit-coherence-neo-ia-ia-back]]
