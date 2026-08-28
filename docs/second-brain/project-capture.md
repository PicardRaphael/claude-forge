# Project capture — contrat de création et de décisions

Ce contrat s'applique quand Raphaël demande explicitement de créer/démarrer un
projet ou de conserver un choix de projet. Une idée évoquée ou une exploration
sans engagement ne crée aucun foyer.

## Foyers

| Information | Destination |
|---|---|
| vision, résultat attendu, périmètre, contraintes, acteurs, liens | `1-Projets/<Projet>/<Projet>.md` |
| choix actif réversible | section `Choix actifs` du foyer projet |
| décision structurante avec alternatives et conséquences | `Knowledge/decisions/decision-<projet>-<clé>.md` |
| état de travail temporaire | `memory/project_<slug>.md` avec `expires` |
| préférence personnelle généralisable explicitement formulée | `Raphael-Picard` ou casquette |
| connaissance réutilisable hors projet | note technique canonique |

## Création du foyer projet

Avant création, chercher le nom puis le concept seul et lire les candidats. Si
un foyer existe, l'enrichir. Sinon créer une note avec :

- frontmatter `titre`, `resume`, 4 à 6 `aliases`, `type: context`,
  `status: active`, `derniere-maj`, `auteur` et tags projet ;
- sections `Vision`, `Résultat attendu`, `Périmètre`, `Contraintes`,
  `Choix actifs`, `État`, `Liens` ;
- un lien vers `Raphael-Picard` et vers les connaissances déjà utiles.

La demande explicite de création autorise ce foyer. Ne pas demander une seconde
validation sauf ambiguïté matérielle sur le projet visé ou donnée sensible.

Pour une demande autonome « retiens ce choix pour X » sans foyer retrouvé :

- créer un foyer minimal si Raphaël affirme que X est un projet actif ;
- demander si X est seulement une idée lorsque le statut change matériellement
  l'écriture ;
- ne jamais inventer silencieusement un projet depuis une formulation
  hypothétique.

## Capturer un choix

Un choix rejoint le foyer projet lorsqu'il est explicite et utile à une future
session. Créer une note de décision séparée seulement si au moins deux de ces
signaux sont présents : alternatives comparées, coût de retour élevé,
conséquences cross-composants, contrainte durable, besoin de justification.

Une décision séparée contient : contexte, options, décision, raisons,
conséquences, statut et date. Le foyer projet porte un wikilink vers elle. Si la
décision change, marquer l'ancienne comme remplacée et relier la nouvelle ; ne
pas réécrire l'histoire comme si l'ancienne n'avait jamais existé.

La `<clé>` est stable et sémantique, choisie sur le domaine de décision plutôt
que sur la solution retenue : `database`, `hosting`, `auth`, `data-residency`.
Une nouvelle solution pour le même domaine met à jour/remplace la décision
existante ; elle ne crée pas un second slug dépendant du fournisseur.

## Vérification

Après chaque mutation : relire le foyer et les décisions touchées, vérifier les
wikilinks, l'absence de doublon et `derniere-maj`. Rapporter les créations,
enrichissements, choix temporaires et conflits.
