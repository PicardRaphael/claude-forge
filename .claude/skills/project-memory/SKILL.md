---
name: project-memory
description: ALWAYS invoke when Raphaël explicitly asks to create/start a project, persist its context, or record a project choice. Maintains the vault project hub and decisions. NOT for a casual idea, roadmap generation, or temporary task planning.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__forge-brain__*
argument-hint: "[project name or decision]"
---

# project-memory — mémoire vivante des projets

Lire entièrement `docs/second-brain/project-capture.md` et
`.claude/rules/memory-discipline.md` avant d'écrire.

## Déterminer l'intention

- « Crée/démarre le projet X » : création ou enrichissement autorisé.
- « Garde/retiens ce choix pour X » : mutation du foyer ou d'une décision
  autorisée.
- « J'ai une idée de X » : aucune écriture ; aider à explorer puis demander une
  décision seulement si la création matérielle du foyer est nécessaire.
- Une roadmap ou une spec est un livrable projet, pas la mémoire du projet :
  utiliser la skill métier adaptée puis ne capitaliser que les choix actés.

## Exécuter

1. Chercher le nom du projet, puis son concept seul, dans forge-brain.
2. Lire entièrement les foyers candidats et les décisions liées.
3. Enrichir le foyer existant ou, si la demande crée réellement un nouveau
   projet, créer le foyer défini par le contrat.
4. Classer chaque choix : actif réversible, structurant, temporaire, personnel
   généralisable ou connaissance cross-projet.
5. Écrire chaque delta dans son foyer, sans recopier le même contenu.
6. Relire les mutations, vérifier les liens et rapporter le résultat.

## Bornes

- Ne pas créer automatiquement un dossier de notes complet : commencer par un
  hub ; ajouter une décision seulement quand ses critères sont remplis.
- Ne pas créer un fichier temporaire si aucune phase active ne le justifie.
- Ne pas transformer un choix local en préférence personnelle globale sans
  formulation explicite de Raphaël.
- Pour une décision séparée, utiliser une clé de domaine stable (`database`,
  `hosting`, `auth`) et non le nom de la solution choisie.
- Si un choix autonome vise un projet introuvable, créer un hub minimal seulement
  quand le projet est explicitement actif ; sinon demander si c'est encore une
  idée avant toute écriture.
- Ne jamais supprimer automatiquement une note ou masquer une décision
  remplacée.

## Sortie

```markdown
## Mémoire projet — <nom>
- Foyer : créé | enrichi | inchangé
- Choix actifs : <deltas>
- Décisions : <créées/mises à jour>
- Temporaire : <fichier + expiration ou aucun>
- Personnel/cross-projet : <routage ou aucun>
- Vérification : PASS | conflit
```

## Gotchas

- Un nom différent peut désigner un foyer existant : les aliases tranchent après
  lecture, pas le nom de dossier seul.
- Une décision technique n'est pas forcément structurante ; éviter l'ADR spam.
- Le statut courant ne doit pas polluer le hub stable.

## Apprentissage

Si les mêmes choix restent difficiles à classer, enrichir
`docs/second-brain/project-capture.md` avec un critère discriminant, pas une
exception propre à un projet.
