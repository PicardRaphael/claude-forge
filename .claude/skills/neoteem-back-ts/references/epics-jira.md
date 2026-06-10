# Epics Jira [IA] — les 5 thèmes permanents (référentiel embarqué)

> **Source = Jira, figé une fois pour toutes par le PO.** Ce fichier est embarqué dans la skill pour la portabilité (chaque repo a sa copie — neo_ia ne lit pas neoteem-back-ts). Ne jamais le modifier sans décision PO. On ne crée JAMAIS d'epic : tout travail = une **story** rattachée à l'un de ces 5 epics, avec ses **sous-tâches** (US).

## 💬 Chatbots assistants [IA] — [N2-68082](https://neoteem.atlassian.net/browse/N2-68082)

Assistants conversationnels : NeoChat, chatbot support, tout dialogue multi-tours où l'IA accompagne un utilisateur en orchestrant les outils du backend. **Inclut le socle backend qui les sert** (ex. story Migration ia_back → neoia-api).
Repos : [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/).

## 🤖 Agents [IA] — [N2-106433](https://neoteem.atlassian.net/browse/N2-106433)

Agents IA à tâche unique, déclenchés à la demande : comparaison de devis, rédaction d'annonce immobilière, indicateurs… Une entrée, un livrable, pas de conversation longue.
Repos : [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/).

## 🔌 MCP [IA] — [N2-111230](https://neoteem.atlassian.net/browse/N2-111230)

Serveurs MCP exposant le métier Loji aux clients IA (Claude, ChatGPT…) : une codebase par domaine, déployée une fois par client. Socle mcp-kit, auth OAuth, tools.
Repo : [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/).

## 🛠️ Outils internes [IA] — [N2-111276](https://neoteem.atlassian.net/browse/N2-111276)

Outillage IA des équipes Neoteem (jamais les clients) : skills/plugins Claude, base de connaissances neoteem-brain, automatisations internes.
Repos : [neoteem-brain](https://bitbucket.org/neot-v2/neoteem-brain/src/master/) · [neoteem-plugin-claude](https://bitbucket.org/neot-v2/neoteem-plugin-claude/src/master/) · [neoteem-plugin-claude-admin](https://bitbucket.org/neot-v2/neoteem-plugin-claude-admin/src/master/).

## 📧 Gestion mail [IA] — [N2-111277](https://neoteem.atlassian.net/browse/N2-111277)

Traitement des e-mails par l'IA (NeoMail) : classification, réponse automatique/assistée, extraction d'informations, rattachement au bon dossier.
Repos : [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/).

## Routage des cas frontières

| Si la demande est… | Epic |
|---|---|
| Dialogue multi-tours avec un utilisateur | 💬 Chatbots assistants |
| Tâche unique sans conversation (comparer, rédiger, calculer) | 🤖 Agents |
| Exclusivement du traitement de mail | 📧 Gestion mail |
| Serveur/tool MCP exposé aux clients IA | 🔌 MCP |
| Outil pour les équipes internes Neoteem | 🛠️ Outils internes |
| Socle backend transverse | l'epic du produit principal qu'il sert (ex. migration ia_back → 💬) |
| Aucun thème ne colle | **AskUserQuestion** — jamais de choix silencieux, jamais d'epic neuf |

## Étiquettes (chaque story et sous-tâche)

`IA-DEV` (toujours) + étiquette projet = nom exact du repo (`neoteem-back-ts`, `neo_ia`…) + 1 label domaine (`setup`/`agent`/`db`/`migration`/`test`/`qualité`/`mcp`/`obs`) + `one-shot`|`récurrent`. Les labels Jira se créent à la volée — rien à pré-créer. Epics : `IA-DEV` seul.

## Création Jira via MCP Atlassian (après validation explicite uniquement)

- Story : `createJiraIssue` type Story, parent = epic (N2-…), description en ADF (rendu : headings colorés `#00b8d9`, voir templates).
- Sous-tâche : `createJiraIssue` type Sous-tâche, parent = la story.
- Toujours présenter la liste de ce qui va être créé et obtenir le OK AVANT le premier appel. Jamais de création silencieuse.
