# Templates description Jira — Feedback Triage

Configuration standard pour tous les tickets :
- **Projet** : N2 (Neoteem)
- **Parent** : N2-109957 ([IA] Parent) — OBLIGATOIRE
- **Type** : `[IA] Bug` / `[IA] Feature` / `[IA] A CLASSER`
- **Etat initial** : `A specifier`

## Entete standard (tous les templates)

L'entete est identique pour les 3 types. Toujours inclure le lien direct vers la trace Langfuse.

```
**Feedback:** "<commentaire utilisateur ou resume>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Date:** <feedback_date_creation>
**Session ID:** <feedback_threadid>
**Trace ID:** <feedback_trace_id>
**Lien Langfuse:** https://cloud.langfuse.com/trace/<feedback_trace_id>
```

Notes :
- Si `feedback_trace_id` est null, ecrire "Trace non disponible" et ne pas mettre de lien
- Ne PAS inclure feedback_acteurid ni feedback_type (pas utile pour le triage)

## Template [IA] Bug

```
## Analyse automatique

**Feedback:** "<commentaire utilisateur ou resume du probleme>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Date:** <feedback_date_creation>
**Session ID:** <feedback_threadid>
**Trace ID:** <feedback_trace_id>
**Lien Langfuse:** https://cloud.langfuse.com/trace/<feedback_trace_id>

## Diagnostic

<Description precise du probleme observe dans la trace.
Qu'est-ce qui s'est passe ? Quelle observation a echoue ?
Quel tool a retourne un mauvais resultat ?
Quelle etape du raisonnement de l'agent est incorrecte ?>

## Fichiers probablement impactes

- `<chemin/fichier1>` — <raison : logique de recherche, prompt agent, config tool, etc.>
- `<chemin/fichier2>` — <raison>

## Suggestion de fix

<Description technique de ce qu'il faut corriger.
Etre precis : quel parametre changer, quelle logique modifier, quel prompt ajuster.>

## Contexte metier (si applicable)

<Info du brain qui aide a comprendre pourquoi le comportement est incorrect.>
```

## Template [IA] Feature

```
## Analyse automatique

**Feedback:** "<commentaire utilisateur ou resume de la demande>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Date:** <feedback_date_creation>
**Session ID:** <feedback_threadid>
**Trace ID:** <feedback_trace_id>
**Lien Langfuse:** https://cloud.langfuse.com/trace/<feedback_trace_id>

## Demande client

<Reformulation claire de ce que le client demande ou attend.
Quel use case n'est pas couvert ? Quelle fonctionnalite manque ?>

## Etat de l'existant (verifie via /neo-brain-dev-ia)

**BDD** : <fonctions PG existantes ou "n'existe pas">
**ia_back** : <endpoints existants ou "n'existe pas">
**neo_ia** : <tools/agents existants ou "n'existe pas">
**lojii-front** (si applicable) : <pages existantes ou "n'existe pas">

## Proposition technique

Selon ce qui manque, proposer la creation a chaque niveau :

1. **bdd** (si fonction PG manquante) : creer `f_<nom>` qui <description>
   Ou utiliser le mix de `<f_xxx>` + `<f_yyy>` existantes
2. **ia_back** (si endpoint manquant) : creer `<methode> /api/v1/<resource>`
   Fichier : `ia_back/src/<module>/<fichier>.ts`
3. **neo_ia** (si tool manquant) : creer tool `<nom_tool>`
   Fichier : `neo_ia/packages/<app>/tools/<fichier>.py`
4. **neo_ia** (config agent) : connecter le tool a l'agent `<nom_agent>`
   Fichier : `neo_ia/packages/<app>/agents/<agent>/config.py`

## Contexte metier

<Info du brain sur le domaine concerne.
Regles metier a respecter dans l'implementation.>
```

## Template [IA] A CLASSER

```
## Analyse automatique

**Feedback:** "<commentaire utilisateur ou resume>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Date:** <feedback_date_creation>
**Session ID:** <feedback_threadid>
**Trace ID:** <feedback_trace_id ou "non disponible">
**Lien Langfuse:** <lien ou "non disponible">

## Contexte

<Ce qu'on sait du feedback. La question posee, la reponse recue.>

## Pourquoi A CLASSER

<Explication precise de pourquoi l'IA n'a pas pu trancher entre Bug et Feature :
- Pas de trace disponible
- Commentaire trop vague
- Le comportement semble correct mais le client n'est pas satisfait
- Besoin d'info supplementaire du client
- Plusieurs interpretations possibles
- Concept metier non trouve dans le brain>

## Pistes d'investigation

- <Piste 1 : verifier tel aspect avec le client>
- <Piste 2 : regarder telle trace plus en detail>
- <Piste 3 : consulter tel domaine metier>
```

## Commentaire pour doublon (ticket existant)

```
## Feedback similaire recu

**Date:** <feedback_date_creation>
**Feedback:** "<commentaire utilisateur>"
**Agent:** <nom_agent> | **Client:** <client_id>
**Session ID:** <feedback_threadid>
**Trace ID:** <feedback_trace_id>
**Lien Langfuse:** https://cloud.langfuse.com/trace/<feedback_trace_id>

Ce feedback confirme le probleme deja identifie dans ce ticket.
Nombre de feedbacks similaires sur ce ticket : <N>
```

Si le ticket trouve est deja **ferme/resolu**, ajouter au commentaire :

```
ATTENTION : ce ticket a deja ete ferme. Ce feedback peut indiquer :
- Une regression (le probleme est revenu)
- Un probleme different qui ressemble superficiellement
- Un feedback legitime qui n'a pas ete pris en compte

A re-ouvrir ou a creer un nouveau ticket selon la decision de l'equipe.
```

## Regles communes

- **Projet** : N2
- **Parent** : N2-109957 ([IA] Parent) — jamais oublier
- **Etat initial** : A specifier
- **Titre du ticket** : max 80 caracteres, format `[Agent] Resume du probleme`
  - [IA] Bug : `[support] Mauvais retrieval sur les charges de copropriete`
  - [IA] Feature : `[neodoc] Ajouter export PDF des documents`
  - [IA] A CLASSER : `[neochat] Insatisfaction sur reponse votes AG`
- **Langue** : francais pour tout le contenu
- **Lien Langfuse** : toujours inclure le lien cliquable vers la trace
- **Fichiers** : utiliser les chemins relatifs depuis la racine du repo
- **Ne PAS inclure** : feedback_acteurid, feedback_type, score (inutile pour le triage)
