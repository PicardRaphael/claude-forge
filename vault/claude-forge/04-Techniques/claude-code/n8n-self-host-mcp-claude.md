---
titre: "n8n self-host + MCP piloté par Claude — automatisation externe en langage naturel"
resume: "Recette opérationnelle : héberger n8n sur un VPS (Hostinger + Dokploy), brancher le MCP n8n non-officiel (czlonkowski/n8n-mcp) pour que Claude crée/modifie/débugge les workflows en langage naturel. Couvre triggers/actions/conditions, le point RGPD données pro, et la spec de la future skill /n8n-automate. Complète le panorama marché [[agents-automation]] côté how-to self-host."
aliases:
  - "n8n self-host MCP"
  - "n8n MCP Claude"
  - "automatisation n8n VPS Hostinger Dokploy"
  - "czlonkowski n8n-mcp"
  - "skill n8n-automate"
  - "piloter n8n langage naturel"
type: technique
domaine: claude-code
status: active
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/agents"
sources:
  - "https://www.youtube.com/watch?v=IubQUC9TL2w (Eliott Meunier — cours Second Cerveau IA, vidéo 5 automatisations)"
  - "github.com/czlonkowski/n8n-mcp (MCP n8n non-officiel)"
---

## Quand utiliser cette note

Quand un process mappé via [[cartographier-process-cma]] conclut à une **automatisation externe** (trigger auto, tourne sans Claude dans la boucle d'exécution). Angle = **recette self-host + pilotage par Claude**, complémentaire du panorama marché [[agents-automation]] (qui compare n8n/Zapier/Make mais ne décrit pas le montage).

## Anatomie d'une automatisation (3 composants)

1. **Trigger** — ce qui déclenche le flux. Tout workflow en a un, sinon il ne part jamais.
   - *Manuel* (bouton) · *App event* (intégration native : Telegram, Stripe, Typeform…) · *Schedule* (cron : « chaque matin 6h50 ») · *Webhook* (un service externe POST un payload — fallback universel quand l'app n'a pas d'intégration native).
2. **Actions** — les étapes (extraire data, résumer via LLM, écrire en base, envoyer un message). Bloc HTTP request ou bloc code (JS écrit par Claude) si l'outil n'est pas intégré.
3. **Conditions** — la logique (`if` : client insatisfait → alerte CSM ; sinon rien).

## La stack self-host (de la vidéo)

| Couche | Choix vidéo | Note |
|---|---|---|
| Serveur | **VPS Hostinger** (plan KVM2 conseillé, ~4-7 €/mois) | Sponsor de la vidéo (code promo « Eliott Meunier »). Alternative : tout autre VPS. |
| Orchestration | **Dokploy** (panel multi-services sur 1 VPS Ubuntu) | Permet n8n + cal.com + Ghost… sur le même serveur. Sinon : install n8n directe (1 VPS = 1 service). |
| Outil | **n8n** (open-source, 8000+ intégrations) | Alternative managée : n8n Cloud ~20 €/mois (mêmes blocs, support, moins d'intégrations OSS). |

Argument de fond : à l'ère des agents, **avoir un serveur perso = antifragile** — on peut demander à Claude d'y héberger un service à la volée (page client, calendrier cal.com en remplacement de Calendly à 200 €/mois, modèle local Ollama…).

## Le MCP n8n — le déclic

Sans MCP : Claude *imagine* un workflow, vous copiez-collez les blocs, vous débuggez en ping-pong manuel (Claude ne voit pas l'état réel). Avec MCP : **Claude dialogue directement avec n8n** — liste les workflows existants, en crée, les modifie, relie les nœuds, débugge les erreurs, et récupère la **doc de chaque nœud** (évite les hypothèses à l'aveugle).

- **MCP n8n natif** : limité (lister, parfois créer ; pas de modif/debug profond). Sûr mais bridé.
- **`czlonkowski/n8n-mcp`** (non-officiel, créé par Romuald Czlonkowski) : complet — list / create / modify / debug + doc par nœud. C'est celui de la vidéo.

**Workflow d'usage type** :
1. Donner la **fiche process** à Claude (cf [[cartographier-process-cma]]).
2. Claude conçoit l'architecture du workflow et **fait valider la structure** avant de créer.
3. Claude crée le workflow via le MCP, le valide, corrige les erreurs en boucle.
4. **Auth manuelle obligatoire** : les clés de connexion aux services (Telegram, OpenAI…) — on ne donne jamais ses identifiants à l'IA.
5. Debug conversationnel ensuite (« le nœud retourne cette erreur… »).

## ⚠️ Point RGPD / souveraineté — données pro Neoteem

Faire transiter des **résumés de réunion ou données clients Neoteem** par un n8n perso + OpenAI pose une question conformité (cf casquette [[responsable-ia]], AI Act). Pour du perso : OK. Pour du pro : à challenger. Levier dans la vidéo = héberger un **modèle local** (Ollama/Mistral/DeepSeek) sur le VPS pour les tâches de résumé sensibles → données ne quittent pas le serveur. Pertinent pour les professions réglementées.

## Spec — future skill `/n8n-automate` (à générer quand le VPS sera monté)

Coquille évitée tant que le MCP n8n n'est pas installé. Le jour venu, la skill ferait :
- **Input** : une fiche process « à automatiser » (de [[cartographier-process-cma]]).
- **Étapes** : (1) charger la doc du nœud cible via le MCP ; (2) proposer l'architecture du workflow + **gate de validation humaine** ; (3) créer via MCP ; (4) valider/débugger ; (5) rappeler les actions manuelles restantes (auth, activation, webhook côté source).
- **Garde-fou** : ne jamais activer le workflow sans validation explicite ; jamais d'identifiants gérés par la skill.
- **Création** : via `skill-creator` (delegate-guard), brief séquence A→B→C→D→E.

## Gotchas

- Le **webhook côté source** (ex : Phantom/outil de réunion) se configure à la main dans l'app source — Claude ne peut pas le faire à votre place.
- Une **clé API LLM expirée / quota** casse le nœud de résumé — symptôme classique (`exceeded your current quota`).
- Org Neoteem **bloque GitHub cloud / triggers cloud** — un VPS perso contourne côté perso, mais vérifier la cohérence côté pro avant d'y mettre des données métier.

## Liens

- [[cartographier-process-cma]] — l'amont : décide quels process partent en automatisation n8n
- [[agents-automation]] — panorama marché (n8n vs Zapier vs Make, computer use, coûts)
- [[MOC-paysage-outils-ia-marche-2026]] — n8n = candidat BUILD self-host pour process internes
- [[automatisation-triage-tickets-support-suivi]] — projet Neoteem connexe (triage via Cowork)
- [[methode-monter-systeme-workflow]] — MCP comme connecteur (donnée/outil externe)
