# Bank de questions — Blocs 3-4-5 (branche HORS-CODE)

Questions à poser en 1-2 appels `AskUserQuestion` (batches de 4 max).

Un loop hors-code = processus humain, checklist récurrente, routine de réflexion, veille, validation qualité, rituels équipe, review périodique.

---

## Bloc 3 — Acteurs et canaux

Questions à sélectionner selon le contexte :

- **Acteurs** : qui réalise le loop ? (toi seul, toi + LLM, équipe, mix humain/IA)
- **Rôles** : y a-t-il plusieurs rôles distincts ? (initiateur, exécutant, validateur, destinataire)
- **Déclencheur humain** : qui déclenche chaque itération ? Sur quelle base ? (rappel calendrier, notification, événement externe)
- **Canal de travail** : où se passe le travail ? (Obsidian, Google Doc, Slack, email, Notion, outil interne)
- **Canal de communication** : comment les participants sont-ils notifiés / coordonnés ?
- **Async ou sync** : le loop est-il réalisé en temps réel (tous ensemble) ou en async (chacun à son rythme) ?
- **Fuseau horaire** : si équipe distribuée, contrainte de fuseau ?

---

## Bloc 4 — Artefacts et livrables

Questions à sélectionner selon le contexte :

- **Input du loop** : quel document / état / information déclenche l'itération ? (liste de tâches, rapport de la veille, ticket entrant, donnée à analyser)
- **Livrable de chaque itération** : qu'est-ce qui doit exister à la fin d'un cycle ? (note Obsidian, message Slack, rapport, ticket Jira, décision documentée)
- **Stockage** : où vivent ces artefacts ? (vault Obsidian, dossier partagé, wiki, email archivé)
- **Template** : y a-t-il un template à suivre pour le livrable ? (si non, faut-il en créer un ?)
- **Versioning** : faut-il garder l'historique de chaque itération ? Comment ?
- **Durée de vie** : combien de temps conserve-t-on les artefacts passés ? (7j, 30j, indéfini)

---

## Bloc 5 — Validation humaine et qualité

Questions à sélectionner selon le contexte :

- **Critère de qualité** : comment savoir qu'une itération est "bien faite" ? (checklist, score, validation par pair, gut feeling)
- **Reviewer** : qui valide le résultat de chaque itération ? (toi-même, manager, LLM, pair)
- **Feedback loop** : que se passe-t-il si la qualité est insuffisante ? (recommencer, corriger, escalader)
- **Seuil d'acceptation** : y a-t-il un seuil minimal en dessous duquel le livrable est rejeté ?
- **Biais à éviter** : y a-t-il un risque de dérive ou de biais au fil des itérations ? Comment le détecter ?
- **Apprentissage** : comment capitalise-t-on sur chaque cycle ? (note de rétro, section "leçons", MAJ du process)
- **Saturation** : comment détecter que le loop n'apporte plus de valeur et doit être arrêté / repensé ?

---

## Notes pour la spec

Dans la SPEC-loop générée, la section "Process / Opérations" doit inclure :
- La liste des acteurs + leur rôle exact
- Le livrable attendu par itération + son template (ou référence au template)
- Le critère de qualité / validation
- La durée estimée d'une itération
- La cadence (ex : "chaque lundi matin", "à chaque onboarding", "après chaque sprint")
- La mention explicite : "Ce loop ne génère PAS de code. Les outils techniques éventuels sont des supports, pas le livrable."
