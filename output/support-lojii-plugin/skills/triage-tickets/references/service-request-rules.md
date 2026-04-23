# Règles Service Request — Support direct vs N2 Intervention BDD

Consulter ce fichier pour tout ticket classifié Service Request.
Mettre à jour ce fichier à chaque fois qu'un nouveau type d'intervention est identifié.

---

## ✅ Le support peut intervenir directement dans LOJII

Ces actions sont réalisables via l'interface LOJII sans intervention technique :

| Action | Chemin dans LOJII |
|--------|-------------------|
| Corriger un IBAN copropriété | Fiche copropriété > Exercice > Informations bancaires |
| Corriger un IBAN propriétaire | Fiche propriétaire > Financier |
| Mettre à jour les dates de mandat syndic | Fiche copropriété > Général |
| Transférer un portefeuille entre agents | Fiche copropriété > Plus d'actions > Transfert de portefeuille |
| Fusionner des acteurs en double | Administration client > Fusion d'acteur |
| Ajouter / corriger les rôles tiers copropriétaire | Fiche copropriétaire > onglet correspondant |
| Corriger l'adresse email d'un salarié (connexion) | Administration > Fiche salarié |
| Mettre à jour les honoraires syndic | Fiche copropriété > Tarifs, puis recalculer |
| Vérifier / créer un mandat SEPA | Fiche copropriétaire > Financier |
| Paramétrer un nouveau utilisateur | Administration > Gestion des utilisateurs |
| Corriger la date premier mandat / mandat en cours | Fiche copropriété > Général |
| Vérifier/corriger les rôles tiers post-transfert | Fiche copropriétaire > Rôles |

---

## ❌ Un N2 Intervention BDD est nécessaire

Ces actions nécessitent un accès à la base de données ou sont trop risquées pour être faites via l'interface :

- Extraction de données (requête SQL, export non disponible dans l'interface)
- Correction d'écritures comptables sur des exercices clôturés
- Correction de données sur un grand nombre de copropriétés simultanément
- Modification de paramètres système inaccessibles aux agents
- Annulation ou correction d'opérations bancaires déjà comptabilisées et irréversibles via l'interface
- Toute correction qui nécessite d'agir directement en base de données

Pour ces cas → N2 de type "Intervention BDD", affecté au PO Responsable (customfield_10085 du Module parent), sprint en cours.

---

## ⚠️ En cas de doute

Classer SR avec la mention dans la note interne : "Faisabilité intervention directe à confirmer."
Proposer à l'utilisateur de trancher dans `/analyse` avant d'agir.

---

## Évolution de ces règles

Ajouter une ligne dans la section appropriée à chaque nouveau type d'intervention identifié.
Indiquer la date et le ticket d'origine pour traçabilité.

<!-- Exemple :
[2025-04-10] | Identifié via SD-4521 : Correction d'un plan de charges erroné = BDD (ne pas faire via interface)
-->
