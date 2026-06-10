# Epics Jira [IA] — les 5 thèmes permanents (référentiel embarqué)

> **Source = Jira, figé une fois pour toutes par le PO.** Ce fichier est embarqué dans la skill pour la portabilité (chaque repo a sa copie — neo_ia ne lit pas neoteem-back-ts). Ne jamais le modifier sans décision PO. On ne crée JAMAIS d'epic : tout travail = une **story** rattachée à l'un de ces 5 epics, avec ses **sous-tâches** (US). Chaque fiche ci-dessous = la description à coller telle quelle dans le champ description de l'epic Jira.

---

## 💬 Chatbots assistants [IA] — [N2-68082](https://neoteem.atlassian.net/browse/N2-68082)

🎯 **Objectif** — Offrir aux utilisateurs Loji des **assistants conversationnels** : NeoChat, chatbot support, et tout dialogue multi-tours où l'IA accompagne un utilisateur — répondre à ses questions métier, naviguer dans ses données, l'aider à agir — en orchestrant les outils du backend.

📦 **Ce qui vit dans cet epic** — Nouvelles capacités NeoChat (questions métier, indicateurs, actions guidées) · chatbot support client · orchestration des outils backend par les assistants (tool use, routage d'intentions) · le socle backend qui sert ces assistants (ex. story Migration ia_back → neoteem-back-ts).

🚫 **Hors-périmètre** — Tâche unique sans conversation → 🤖 Agents [IA] (N2-106433) · exclusivement du mail → 📧 Gestion mail [IA] (N2-111277) · serveur/tool MCP exposé aux clients IA → 🔌 MCP [IA] (N2-111230).

🔧 **Repos** — [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) (backend neoia-api, packages `@neoteem/*`) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/) (agents Python NeoChat/NeoDoc/NeoMail).

---

## 🤖 Agents [IA] — [N2-106433](https://neoteem.atlassian.net/browse/N2-106433)

🎯 **Objectif** — Construire des **agents IA à tâche unique**, déclenchés à la demande : une entrée bien définie, un livrable, pas de conversation longue. L'agent fait UNE chose et la fait bien.

📦 **Ce qui vit dans cet epic** — Comparaison de devis · rédaction d'annonces immobilières · génération d'indicateurs / synthèses à la demande · tout nouvel agent métier mono-tâche et le branchement d'un agent sur une nouvelle source de données.

🚫 **Hors-périmètre** — Dialogue multi-tours → 💬 Chatbots assistants [IA] (N2-68082) · exclusivement du mail → 📧 Gestion mail [IA] (N2-111277) · outil pour les équipes internes → 🛠️ Outils internes [IA] (N2-111276).

🔧 **Repos** — [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/).

---

## 🔌 MCP [IA] — [N2-111230](https://neoteem.atlassian.net/browse/N2-111230)

🎯 **Objectif** — Créer et faire évoluer les **serveurs MCP** qui exposent le métier Loji aux clients IA (Claude, ChatGPT, Gemini…) : **une codebase par domaine métier, déployée une fois par client**.

📦 **Ce qui vit dans cet epic** — Nouveau serveur MCP d'un domaine métier (`apps/mcp-<domaine>`) · nouveaux tools MCP et leurs évolutions · le socle commun `mcp-kit` (auth OAuth, metering, audit) · tout ce qui touche au déploiement/multi-tenant des MCP.

🚫 **Hors-périmètre** — Un endpoint REST consommé par NeoIA n'est pas un MCP → epic du produit concerné (💬/🤖/📧) · skill/plugin Claude interne → 🛠️ Outils internes [IA] (N2-111276).

🔧 **Repos** — [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) (`apps/mcp-*`, `packages/mcp-kit`, `packages/auth-mcp`).

---

## 🛠️ Outils internes [IA] — [N2-111276](https://neoteem.atlassian.net/browse/N2-111276)

🎯 **Objectif** — Équiper les **équipes Neoteem** (jamais les clients) avec l'IA : skills, plugins Claude, base de connaissances, automatisations internes. Tout ce qui rend les collaborateurs plus efficaces avec l'IA.

📦 **Ce qui vit dans cet epic** — Skills et plugins Claude d'équipe (support, PO, dev) · enrichissement et outillage de la base de connaissances neoteem-brain · automatisations internes (veille, reporting, workflows d'équipe).

🚫 **Hors-périmètre** — Feature exposée à un client ou un produit Loji → 💬/🤖/📧/🔌 selon la nature · serveur MCP produit → 🔌 MCP [IA] (N2-111230).

🔧 **Repos** — [neoteem-brain](https://bitbucket.org/neot-v2/neoteem-brain/src/master/) (base de connaissances) · [neoteem-plugin-claude](https://bitbucket.org/neot-v2/neoteem-plugin-claude/src/master/) (plugin équipes : support + brain) · [neoteem-plugin-claude-admin](https://bitbucket.org/neot-v2/neoteem-plugin-claude-admin/src/master/) (plugin admin : PO + brain-admin, accès restreint).

---

## 📧 Gestion mail [IA] — [N2-111277](https://neoteem.atlassian.net/browse/N2-111277)

🎯 **Objectif** — Tout le **traitement intelligent des e-mails** par l'IA (NeoMail) : comprendre, classer, répondre, extraire — pour que les gestionnaires passent moins de temps dans leur boîte mail.

📦 **Ce qui vit dans cet epic** — Classification automatique des mails entrants (urgence, sujet, service) · réponses automatiques ou assistées · extraction d'informations (demandes, coordonnées, pièces jointes) et rattachement au bon dossier/locataire · toute feature où l'IA lit ou écrit du mail.

🚫 **Hors-périmètre** — Conversation multi-tours → 💬 Chatbots assistants [IA] (N2-68082) · tâche unique sans mail → 🤖 Agents [IA] (N2-106433).

🔧 **Repos** — [neoteem-back-ts](https://bitbucket.org/neot-v2/neoteem-back-ts/src/master/) · [neo_ia](https://bitbucket.org/neot-v2/neo_ia/src/master/) (NeoMail).

---

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

- Story : `createJiraIssue` type **[IA] FEATURE** (type story des chantiers IA — jamais « Story fonctionnelle »), parent = epic (N2-…), description en ADF (rendu : headings colorés `#00b8d9`, voir templates).
- Sous-tâche : `createJiraIssue` type Sous-tâche, parent = la story.
- **Assigné : TOUJOURS demander à l'utilisateur** (AskUserQuestion) qui est assigné à la story et aux sous-tâches AVANT de créer — jamais de ticket sans assigné tranché (un seul appel pour tout le lot suffit ; réponses possibles : une personne, « moi », « personne pour l'instant »). Résoudre le nom via `lookupJiraAccountId` → `assignee_account_id`.
- Toujours présenter la liste de ce qui va être créé et obtenir le OK AVANT le premier appel. Jamais de création silencieuse.
