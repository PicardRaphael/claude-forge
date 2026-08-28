---
titre: "Personnaliser ChatGPT — instructions, Projects, mémoire, GPTs et tâches"
resume: "Canon ChatGPT : instructions globales, mémoire personnelle contrôlable, Projects scopés, GPTs sans mémoire personnelle, tâches planifiées et vault canonique pour le profil durable."
aliases:
  - "personnalisation chatgpt"
  - "chatgpt custom instructions"
  - "chatgpt projects memoire"
  - "chatgpt memoire native"
  - "custom gpts 2026"
  - "chatgpt scheduled tasks"
  - "chatgpt work webhooks"
  - "chatgpt sources memoire"
derniere-maj: 2026-08-28
auteur: codex
type: technique
sources:
  - "https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt"
  - "https://help.openai.com/en/articles/10169521-projects-in-chatgpt"
  - "https://help.openai.com/en/articles/8554407-gpts-in-chatgpt"
  - "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
tags:
  - "#type/technique"
  - "#domaine/openai"
  - "#domaine/chatgpt"
  - "#doctrine/2026"
---
# Personnaliser ChatGPT — leviers réels

> Canon au **28 août 2026**. ChatGPT, Codex et le vault forge sont trois surfaces distinctes. Une continuité fiable ne doit pas dépendre d'une seule mémoire opaque.

## Carte des leviers

| Levier | Portée | Bon usage | Limite importante |
|---|---|---|---|
| **Instructions personnalisées** | compte ChatGPT | ton, format, préférences générales | peuvent être transmises aux apps tierces si pertinentes |
| **Mémoire personnelle** | conversations autorisées | préférences, intérêts, objectifs et continuité | générée par ChatGPT, contrôlable mais non versionnée |
| **Projects** | chantier | fichiers, chats, instructions et mémoire scopée | règles de scope propres au projet |
| **GPTs** | assistant packagé | instructions, knowledge, capacités, apps/actions | n'utilisent pas la mémoire sauvegardée ni les custom instructions |
| **Tâches planifiées / Work** | exécution différée ou événementielle | routines, webhooks et travail en arrière-plan | disponibilités et approbations dépendent du plan et de la surface |
| **Vault forge + adaptateurs repo** | système contrôlé de Raphaël | doctrine, décisions, profil explicite, projets et historique | doit être maintenu par workflows et preuves |

## Instructions personnalisées

OpenAI indique qu'elles s'appliquent immédiatement aux chats et qu'elles sont disponibles sur web, desktop, iOS et Android. Elles peuvent être modifiées ou désactivées dans les réglages de personnalisation.

Elles servent à la forme de collaboration, pas à stocker une base de connaissances importante. Éviter d'y placer des secrets : une app ou un plugin tiers peut recevoir l'information pertinente à son appel.

## Mémoire personnelle ChatGPT

La mémoire personnelle sert à rappeler des détails utiles entre conversations. Les leviers observables sont notamment :

- voir, corriger ou supprimer les souvenirs ;
- désactiver la mémoire ;
- utiliser un Temporary Chat qui ne l'utilise ni ne l'enrichit ;
- consulter les sources de personnalisation lorsqu'elles sont exposées ;
- indiquer qu'un élément n'est plus pertinent.

Depuis les évolutions 2026, ChatGPT peut actualiser automatiquement ce qu'il juge important et réduire les souvenirs contradictoires. Cette amélioration ne transforme pas la mémoire en registre canonique : les réglages, plans et déploiements peuvent varier, et l'utilisateur doit pouvoir corriger.

Pour Raphaël, les faits et préférences explicites importants vivent dans [[Raphael-Picard]] ou dans la casquette concernée, avec provenance et possibilité de révocation. `memory/user_raphael_profile.md` n'est qu'un adaptateur de compatibilité vers ce foyer.

## Projects

Un Project rassemble chats, fichiers, texte, instructions et sources issues d'apps. Il sert de second cerveau **scopé à un chantier**, pas de profil global.

- Les Projects sont disponibles sur les plans gratuits et payants.
- Le nombre de fichiers dépend du plan ; ne pas figer le chiffre dans une règle durable.
- La mémoire peut être `default` ou `project-only` selon le projet et les réglages.
- En project-only, les souvenirs personnels et conversations externes ne sont pas consultés.
- Un projet partagé passe en project-only et ne récupère pas le contexte personnel extérieur des membres.
- Les instructions du projet guident ses conversations.

Le bon pattern : un projet par contexte long dans ChatGPT, un foyer durable sous `1-Projets/` dans forge-brain, et le vault pour la doctrine cross-projet.

## GPTs

Un GPT combine instructions, knowledge et capacités. Il peut utiliser des apps ou des actions, mais pas les deux simultanément.

Point critique : les GPTs ne réutilisent pas les souvenirs sauvegardés, les instructions personnalisées ni les conversations précédentes. Chaque conversation commence donc sans cette mémoire personnelle. Tout comportement essentiel doit être présent dans les instructions ou la knowledge du GPT.

## Tâches planifiées et ChatGPT Work

Au 25 août 2026 :

- les tâches peuvent être partagées ; le destinataire révise les instructions, connecte ses propres apps et crée sa copie ;
- ChatGPT Work peut déclencher des tâches sur des événements Gmail, Slack et GitHub pour les plans éligibles ;
- une action nécessitant une approbation se met en pause ;
- le navigateur Work peut poursuivre certaines tâches sur des sites authentifiés, avec confirmation avant les actions conséquentes ;
- les limites et surfaces varient selon le plan, donc les vérifier avant recommandation.

Ce levier automatise l'exécution. Il ne remplace pas le workflow `cc-news` de forge pour corriger le vault avec préimage, sources et relecture.

## Architecture recommandée pour Raphaël

1. **Instructions ChatGPT** : préférences de forme courtes.
2. **Project ChatGPT** : contexte conversationnel d'un chantier et ses documents.
3. **Mémoire ChatGPT** : recall pratique, corrigible, non canonique.
4. **Vault forge** : doctrine, décisions, notes de connaissance et foyers projets.
5. **Raphael-Picard + casquettes** : profil durable canonique.
6. **Mémoire repo** : adaptateurs, incidents empiriques précis et états projet temporaires.
7. **Skills `cc-news`, `done` et `project-memory`** : maintenance, consolidation et capture projet.

Cette architecture tolère qu'un mécanisme de mémoire se mette à jour en retard, oublie un détail ou réécrive sa synthèse : aucune couche générée n'est seule propriétaire de l'information.

## Anti-patterns

- Confondre mémoire ChatGPT et mémoire locale Codex.
- Mettre un corpus entier dans les instructions personnalisées.
- Supposer qu'un GPT connaît les souvenirs personnels du compte.
- Utiliser un Project partagé en pensant qu'il accède au profil privé de chaque membre.
- Traiter une mémoire générée comme une preuve de fraîcheur.
- Maintenir une biographie concurrente dans la mémoire repo.
- Laisser des chiffres de plan ou de limites sans date ni re-vérification.

## Wikilinks

- [[memoire-optimale-codex-chatgpt]]
- [[codex-vs-chatgpt-seul]]
- [[MOC-Codex]]
- [[Raphael-Picard]]
- [[pattern-vault-llm-karpathy]]
