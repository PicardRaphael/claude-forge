---
aliases:
  - veille-concurrents-ia-syndic
  - concurrents-neomail
  - mcp-gemini-grand-public
  - carte-concurrentielle-ia-immo
  - copropilot-genius-bellman-reemia
resume: Veille concurrentielle IA syndic/gérance (29 mai 2026) + verdict MCP chat Gemini grand public. Source pour benchmark dossier CODIR Neoteem.
derniere-maj: 2026-05-29
tags:
  - "#type/knowledge"
  - "#projet/neoteem"
  - "#casquette/responsable-ia"
  - "#domaine/strategie"
---

# Veille concurrents IA syndic + MCP Gemini (29 mai 2026)

> Recherche web multi-agents (6 axes, vérifiée). Complète [[comprendre-neoteem-vue-responsable-ia]]. Acteurs émergents 2025-2026 = infos volatiles, revérifier sous 1-2 mois.

## VERDICT MCP — chat Gemini grand public

**NON, un syndic ne peut PAS brancher lui-même le MCP de Loji dans l'app chat grand public Gemini (comme dans Claude Desktop/Claude.ai). Fait vérifié, 29 mai 2026.**

3 niveaux Google à distinguer :
| Niveau | MCP custom ? | Pour qui |
|---|---|---|
| Gemini API/SDK/CLI | OUI (code, config JSON) | développeurs (depuis mars 2026) |
| Gemini Enterprise/Agentspace | OUI (OAuth, console Cloud) | équipe IT entreprise, admin lourde |
| **App chat grand public** (Spark, I/O 19 mai 2026) | **NON** — 3 connecteurs partenaires curatés (Canva, OpenTable, Instacart), pas de portail self-service | grand public no-code |

**Conséquence stratégique** : Claude.ai/Desktop = SEULE plateforme grand public où l'utilisateur ajoute lui-même un connecteur MCP sans code → différenciateur réel. NE PAS baser une roadmap sur « Loji dans Gemini grand public » à court terme. Voie réaliste sur Gemini : partenariat Spark (BizDev Google, non daté) ou Gemini Enterprise (clients à équipe IT). Alternative propre : coder nous-mêmes l'intégration via Gemini API (= notre produit, pas « l'utilisateur branche son Gemini »).

## Carte concurrentielle

| Concurrent | IA | Menace Neoteem |
|---|---|---|
| **Genius Immo** | Suite EN PRODUCTION : Agent Mail, Genius GPT (RAG docs), mémoire immeuble, comparaison devis, AG. ChatGPT. ~49-59€/user | **Directe** sur NeoMail + comparateur devis (déjà live, prix bas). Mais RAG sur PDF, pas la logique métier ERP → ne reproduit pas le moat Loji. |
| **CoproPilot (Polsia)** | Triage mail + classif + rédaction human-in-the-loop + Document Intelligence + AG Autopilot | **Concurrent FRONTAL de NeoMail** (proposition quasi identique). Mais pré-lancement/waitlist, pas live, pas de prix. |
| **Syndic-AI (syndic-ai.com)** | Analyse mails copropriétaires + génération réponses + chatbot 24/7. Présent RENT Paris, SIREN 944 435 734 | Secondaire. Empreinte quasi nulle (pas fondateur/date/prix). |
| **Bellman/Septeo** | Réponse mail IA 1 clic (ChatGPT). Chiffres « -50% », « 70% 1 clic » datent de 2023 | Faible aujourd'hui (IA = roadmap future Septeo), **forte demain** : distribution Septeo (1,3M lots, 250k pros). Le danger = la distribution, pas l'IA. |
| **REEMIA (ex-Foncia/Emeria)** | Orion (IDP doc) + Sirius (agent conversationnel) | **Le + sérieux après Bellman** (crédibilité métier ex-Foncia). Mais couche IA SANS base métier propriétaire → doit s'intégrer. Chiffres auto-déclarés. |
| **KEYZIA** | Plateforme IA immo généraliste (8 modules, multi-LLM, couche data +80 sources/jour). PAS un outil mail | **Indirecte** : si ajoute module mail + canal SEO/formation = distribution redoutable. Early stage (6 hits annuaire). |
| **Mister IA** (10M€ levés 20/05/26) | Cabinet/intégrateur agents IA, 1000+ clients B2B | Pas éditeur syndic. Risque = descente via intégration. |
| **ICS Spirit / Matera / Immopen** | Cloud-migration, **aucune IA native documentée** | Nulle à court terme sur l'IA. |

⚠️ **« SyndicInboxAI » n'existe PAS sous ce nom** (2 recherches négatives). Concurrent réel = **Syndic-AI**. Corriger toute mention dans docs Neoteem.

## Insight stratégique #1 (Coprolab, 10/05/2026, source qui teste réellement)

**Aucun éditeur de logiciel syndic n'a d'IA native pleinement déployée en production — tout est encore du « branchage » externe (Make/n8n) sur API.** Personne n'a gagné. La fenêtre est ouverte. Neoteem possède la donnée structurée (PostgreSQL, graphe acteur/rôle) que les concurrents doivent scraper = prérequis n°1 du marché.

## Validation roadmap par le marché

- **NeoMail (tri/réponse mail) = cas d'usage n°1 validé** jusqu'au président de l'ANGC (post LinkedIn juin 2025) + presse métier (IRC n°715, 02/02/2026). Roadmap alignée, pas de décalage.
- 3 ajustements : (1) séquencer par RISQUE pas visibilité — impayés/sinistres/OCR d'abord (fort ROI, faible risque), agent AG en ASSISTANT validé humainement uniquement ; (2) neutraliser angle ARC (note 09/12/2025 : IA « au service du syndic pas de la copro ») → discours valeur copropriétaire ; (3) chiffrer en propre (les « -60% relances / 55% admin / 80% chatbot / 70% 1 clic » = chiffres de blog non sourçables, ne PAS réutiliser en CODIR).

## Risque juridique agent AG (vérifié)

PV d'AG = acte **non modifiable après signature** du président de séance. Délai contestation 2 mois (5 ans si non notifié). Erreurs de forme = 1re cause d'annulation. Syndic responsable même via outil auto. Hallucination juridique documentée (IRC n°7315). → agent AG = assistant validé humainement, JAMAIS générateur autonome.

## Incertitudes / à revérifier

- Calendrier ouverture self-service Spark (Gemini grand public) non daté par Google.
- Chiffres REEMIA, Bellman, FNAIM = auto-déclarés/blogs, pas de source tierce auditée.
- Maturité réelle Syndic-AI et CoproPilot (pré-lancement) à confirmer.
- Comparatif Coprolab 10 logiciels IA syndic 2026 annoncé, non encore consulté.
