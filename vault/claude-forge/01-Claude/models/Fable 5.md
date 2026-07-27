---
titre: "Claude Fable 5 — modèle classe Mythos, redéployé après levée de l'export-control"
resume: "Modèle Anthropic classe Mythos (au-dessus d'Opus), annoncé 9 juin 2026 (CC v2.1.170), 1M contexte par défaut, adaptive thinking only, fallback auto vers Opus 4.8 sur requêtes flaggées. Suspendu 12 juin (export-control US), REDÉPLOYÉ le 1er juillet 2026 (Commerce Dept lève l'ordre le 30 juin) avec un nouveau classifier renforcé. Dispo Claude.ai/Platform/Code/Cowork."
aliases:
  - "Claude Fable 5"
  - "Fable 5"
  - "claude-fable-5"
  - "Mythos 5"
  - "Mythos-class model"
  - "Project Glasswing"
derniere-maj: 2026-07-27
auteur: claude
type: modele
sources:
  - "https://www.anthropic.com/news/claude-fable-5-mythos-5"
  - "https://www.anthropic.com/news/redeploying-fable-5"
  - "https://code.claude.com/docs/en/changelog"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Fable 5

> Annoncé **9 juin 2026** (CC v2.1.170, verbatim changelog : *« a Mythos-class model that we've made safe for general use. Fable's capabilities exceed those of any model we've ever made generally available »*). Tier « Mythos-class » au-dessus d'Opus, rejoignant Opus/Sonnet/Haiku. **Suspendu 12 juin → redéployé 1er juillet 2026** (cf ci-dessous).

## Caractéristiques

- **1M tokens de contexte par défaut** (le suffixe `[1m]` des noms de modèle est normalisé/strippé depuis v2.1.173).
- **Adaptive thinking only** (comme Opus 4.8) : `budget_tokens` manuel → erreur 400. Le modèle décide quand/combien penser, calibré par effort × complexité.
- **Safety classifiers** : repli automatique vers **Opus 4.8** sur les requêtes flaggées. Si une org n'a pas Opus 4.8 activé, l'auto mode retombe sur le meilleur Opus disponible (fix v2.1.176).
- **Mythos 5** = même modèle sans les safety classifiers, disponibilité limitée via **Project Glasswing** (orgs approuvées uniquement, restauré pour les orgs US du programme).
- **État de l'art** sur presque tous les benchmarks (SWE, knowledge work, vision, recherche scientifique). Verbatim Anthropic : *« The longer and more complex the task, the larger Fable 5's lead over other models. »*

## Cycle suspension → redéploiement (juin-juillet 2026)

- **12 juin 2026 — suspension.** Directive export-control du gouvernement US (restriction d'accès aux ressortissants étrangers, impossible à vérifier en temps réel → suspension totale Fable 5 ET Mythos 5). Déclencheur : un rapport de chercheurs Amazon montrant une méthode de contournement des safeguards de Fable 5 (identification de vulnérabilités logicielles + code d'exploitation d'une vulnérabilité). Note : les tests Anthropic ont confirmé que des modèles moins capables (Opus 4.8, GPT-5.5, Kimi K2.7) identifiaient les mêmes vulnérabilités. Opus/Sonnet/Haiku non affectés.
- **30 juin — levée.** Le Commerce Dept US lève l'export-control après ~2 semaines de revue conjointe avec Anthropic. Engagements Anthropic : chasse proactive de failles, coordination sur les futurs lancements, signalement des usages malveillants. Négociation menée par le cofondateur Tom Brown.
- **1er juillet — redéploiement.** Fable 5 revient sur **Claude.ai, Claude Platform, Claude Code ET Claude Cowork**. Nouveau **classifier de sécurité renforcé** : bloque la technique du rapport Amazon dans > 99 % des cas ; requête bloquée → notification utilisateur + envoi vers **Opus 4.8**. CAISI (Commerce/CAISI) juge les safeguards « extraordinarily strong ». ⚠️ **Coût du nouveau classifier : flague plus souvent des requêtes bénignes de coding/debugging** (fallback Opus 4.8 plus fréquent). Réactivation AWS / Google Cloud / Microsoft Foundry en cours.
- Accès (au 1er juillet) : Pro/Max/Team + Enterprise sélectionnés → inclus jusqu'à 50 % des limites hebdo jusqu'au 7 juillet, puis via crédits d'usage.

## Pertinence forge

Fable 5 est de nouveau utilisable (dont en Cowork). Impact sur le défaut modèle : préférence Raphael = Opus 4.8 (cf feedback memory `preference-modele-opus-4-8`), à croiser avec l'arrivée de Sonnet 5 comme défaut CC. Gotcha à retenir pour tout usage coding : le classifier renforcé peut faire retomber des tâches légitimes sur Opus 4.8 (latence/comportement différents). Prompting : [[prompting-fable5-cheatsheet]].

## Wikilinks

- [[prompting-fable5-cheatsheet]] — 12 patterns officiels de prompting Fable 5
- [[CC juin 2026 - v2.1.160 ultracode]] — versions CC liées (v2.1.170 intro, fixes 173-176)
- [[Sonnet 5]] — nouveau défaut CC (croisement défaut modèle)
- [[MOC-Modeles]]
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — modèle de repli des classifiers


---

## AJOUT 27 juillet 2026 — recadrage accès du 20 juillet + arrivée d'Opus 5

- **20 juillet 2026 — fin du « limbo » d'accès** : Fable 5 devient **permanent dans Max et Team Premium à 50 % des limites hebdo** — limites elles-mêmes **réduites de 33 %** le même jour (fin du bonus post-redéploiement). Pro/Team Standard : usage credits à $10/$50 + crédit one-time de $100. Motif officiel : capacité, pas pénalité. (Presse tech convergente, the-decoder et autres.)
- **24 juillet 2026 — [[Opus 5]] lancé** : positionné « close to the frontier intelligence of Claude Fable 5 at half the price », à 0,5 % de Fable 5 sur CursorBench 3.2. Fable 5 garde l'avantage sur les tâches les plus longues/complexes et reste le seul tier Mythos-class ; Opus 5 devient l'option rationnelle pour la majorité des workloads Opus-tier (même mécanique de fallback classifier vers Opus 4.8).
