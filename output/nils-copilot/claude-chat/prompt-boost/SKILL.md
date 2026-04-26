---
name: prompt-boost
description: Reformulate a vague or complex idea into a powerful structured prompt. Use when the user asks for help formulating a request, wants a prompt generated or optimized, or when a request is clearly too vague to produce a good result.
---

# Prompt Boost — Reformulateur de demandes

L'utilisateur a une idee complexe ou floue. Cette skill la transforme en demande structuree qui donne un excellent resultat.

## Quand s'activer

| L'utilisateur dit... | Action |
|----------------------|--------|
| "Aide-moi a formuler ca" | Reformuler sa demande |
| "Comment je demande ca a Claude ?" | Lui proposer le prompt ideal |
| "Donne-moi un prompt pour X" | Generer la demande optimale |
| "Optimise cette demande / ameliore ma demande" | Prendre sa demande et la rendre plus puissante |
| "J'ai une idee mais c'est flou" | Poser 2-3 questions puis reformuler |
| Demande tres vague qui va donner un mauvais resultat | Proposer proactivement : "Tu veux que je t'aide a mieux formuler ca ?" |

## Methode

### 1. Comprendre l'intention

Poser des questions simples si l'idee est floue :
- "C'est pour obtenir quoi au final ?" (un document, une analyse, une decision, un plan)
- "C'est pour qui ?" (toi, un client, ton equipe)
- "Tu veux un truc court ou detaille ?"

Maximum 3 questions. Si l'idee est deja claire, passer directement a la reformulation.

Technique socratique (best practice Cowork Anthropic) : demander a l'utilisateur ce qu'il sait deja et ce qui lui manque, plutot que de deviner.

### 2. Reformuler

Transformer l'idee brute en demande optimisee pour Claude Chat / Cowork (Opus 4.7) :

**Principes de reformulation :**
- Garder le fond et le ton de l'utilisateur (ne pas denaturer)
- Ajouter ce qui manque pour que Claude comprenne bien (contexte, format attendu, contraintes)
- Structurer : objectif clair, etapes si necessaire, format de sortie
- Rester en langage naturel — pas de jargon prompt engineering
- Ton respectueux et precis — eviter les formulations critiques ou agressives qui declenchent des "spirales d'excuse" chez Claude (best practice Amanda Askell)

**Optimisations Claude Chat :**
- Demander le format de fichier specifique si applicable (tableau, document Word, presentation)
- Si la demande necessite des infos a jour, inclure "cherche sur internet" explicitement
- Privilegier des prompts courts et iteratifs — le boss peut toujours affiner apres

**Optimisations Cowork :**
- Formuler comme un brief de delegation : le livrable attendu, ce que "termine" veut dire, les contraintes
- Ne PAS micro-detailler les etapes ("ouvre le fichier, puis copie la colonne B") — decrire le resultat attendu
- Si la tache est complexe, inclure "avant de commencer, dis-moi quelles questions tu as"

### 3. Presenter

Montrer la version amelioree :

```
Voici ta demande reformulee :

---
[demande reformulee]
---

Tu veux l'envoyer comme ca, ou tu veux ajuster quelque chose ?
```

### 4. Optionnel — Executer directement

Si l'utilisateur dit "oui vas-y" ou "envoie", executer la demande reformulee directement dans la conversation au lieu de juste la montrer.

## Exemples

### Exemple 1 — Idee vague

> Boss : "J'aimerais un truc qui compare nos modules avec ce que font les concurrents"
>
> Prompt Boost : "Pour bien formuler ca, 2 questions rapides : tu veux comparer quels modules (syndic, gerance, compta, tous) ? Et tu veux un tableau comparatif ou une analyse detaillee ?"
>
> Boss : "Syndic et gerance, un tableau"
>
> Prompt Boost :
> "Voici ta demande reformulee :
>
> ---
> Fais-moi un tableau comparatif des modules Syndic et Gerance de Neoteem par rapport aux concurrents du marche (logiciels de gestion immobiliere). Pour chaque fonctionnalite cle, indique : ce qu'on a, ce que les concurrents ont, et ce qui nous manque. Cherche sur internet les fonctionnalites des principaux concurrents. Consulte le vault pour ce qu'on a deja.
> ---
>
> Tu veux l'envoyer comme ca ?"

### Exemple 2 — Demande complexe mal formulee

> Boss : "Je voudrais savoir si on devrait faire un truc avec de l'IA pour les AG de copro genre automatiser les PV ou je sais pas"
>
> Prompt Boost :
> "Voici ta demande reformulee :
>
> ---
> Analyse le potentiel d'automatisation par IA pour les assemblees generales de copropriete chez Neoteem. Consulte le vault pour comprendre comment on gere les AG aujourd'hui. Cherche sur internet ce que font les meilleurs logiciels sur ce sujet. Propose 3 cas d'usage concrets (par exemple : generation automatique de PV, synthese des votes, preparation de l'ordre du jour) avec pour chacun : le gain, l'effort, et si c'est faisable avec notre stack.
> ---
>
> Tu veux l'envoyer comme ca ?"

### Exemple 3 — Demande deja claire

> Boss : "Fais-moi un recap de tous les tickets bloques cette semaine avec les raisons"
>
> → Pas besoin de reformuler, la demande est claire. Executer directement.

## Regles

- **Ne jamais denaturer l'intention** — reformuler, pas reinterpreter
- **Langage naturel** — pas de XML, pas de jargon, pas de "en tant que X agis comme Y"
- **Si la demande est deja bonne, ne pas reformuler** — dire "ta demande est claire, je l'execute"
- **Proposer proactivement** quand une demande vague va donner un mauvais resultat — mais ne pas insister si l'utilisateur veut juste une reponse rapide
- **Maximum 3 questions** pour clarifier, pas un interrogatoire

## Gotchas

- Ne pas transformer une question simple en prompt complexe — si le boss demande "c'est quoi X ?", c'est pas une demande a reformuler
- Ne pas ajouter de contexte invente — si une info manque, la signaler avec [A PRECISER]
- Le boss peut dire "non fais juste ce que j'ai dit" — respecter et executer tel quel


## Apprentissage

Noter ici :
- Formulations de prompt qui marchent bien vs celles que le boss rejette
- Types de demandes les plus frequentes
- Niveau de detail que le boss prefere dans les prompts