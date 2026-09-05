---
titre: "Claude Fable 5 — modèle classe Mythos, redéployé après levée de l'export-control"
resume: "Modèle Anthropic classe Mythos (au-dessus d'Opus), annoncé 9 juin 2026 (CC v2.1.170), 1M contexte par défaut, adaptive thinking only, fallback auto vers Opus 4.8 sur requêtes flaggées. Suspendu 12 juin (export-control US), REDÉPLOYÉ le 1er juillet 2026 (Commerce Dept lève l'ordre le 30 juin) avec un nouveau classifier renforcé. Remplacé comme défaut Fable par Fable 5.1 le 1er septembre 2026."
aliases:
  - "Claude Fable 5"
  - "Fable 5"
  - "claude-fable-5"
  - "Mythos 5"
  - "Mythos-class model"
  - "Project Glasswing"
derniere-maj: 2026-09-05
auteur: claude
type: modele
sources:
  - "https://www.anthropic.com/news/claude-fable-5-mythos-5"
  - "https://www.anthropic.com/news/redeploying-fable-5"
  - "https://code.claude.com/docs/en/changelog"
  - "https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1"
tags:
  - "#type/modele"
  - "#domaine/anthropic"
  - "#domaine/claude"
---

# Claude Fable 5

> Annoncé **9 juin 2026** (CC v2.1.170, verbatim changelog : *« a Mythos-class model that we've made safe for general use. Fable's capabilities exceed those of any model we've ever made generally available »*). Tier « Mythos-class » au-dessus d'Opus, rejoignant Opus/Sonnet/Haiku. **Suspendu 12 juin → redéployé 1er juillet 2026** (cf ci-dessous). **Remplacé comme défaut Fable par [[Fable 5.1]] le 1er septembre 2026.**

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

Fable 5 est de nouveau utilisable (dont en Cowork), mais ce n'est plus la fiche à consulter pour un usage courant : voir [[Fable 5.1]]. Sur le défaut modèle, le défaut forge est **Opus 5** depuis le 24 juillet 2026, avec Opus 4.8 en repli — préférence de Raphaël inchangée par l'arrivée des modèles Fable (feedback memory `preference-modele-opus`). Gotcha à retenir pour tout usage coding sur cette génération : le classifier renforcé peut faire retomber des tâches légitimes sur Opus 4.8 (latence/comportement différents) — c'est précisément ce que Fable 5.1 corrige. Prompting : [[prompting-fable5-cheatsheet]].

## Wikilinks

- [[Fable 5.1]] — successeur, défaut Fable depuis le 1er septembre 2026
- [[prompting-fable5-cheatsheet]] — 12 patterns officiels de prompting Fable 5
- [[CC juin 2026 - v2.1.160 ultracode]] — versions CC liées (v2.1.170 intro, fixes 173-176)
- [[Sonnet 5]] — défaut CC à l'époque de cette fiche (croisement défaut modèle)
- [[MOC-Modeles]]
- [[CC 28 mai 2026 - Opus 4.8 + Dynamic Workflows]] — modèle de repli des classifiers


---

## AJOUT 27 juillet 2026 — recadrage accès du 20 juillet + arrivée d'Opus 5

- **20 juillet 2026 — fin du « limbo » d'accès** : Fable 5 devient **permanent dans Max et Team Premium à 50 % des limites hebdo** — limites elles-mêmes **réduites de 33 %** le même jour (fin du bonus post-redéploiement). Pro/Team Standard : usage credits à $10/$50 + crédit one-time de $100. Motif officiel : capacité, pas pénalité. (Presse tech convergente, the-decoder et autres.)
- **24 juillet 2026 — [[Opus 5]] lancé** : positionné « close to the frontier intelligence of Claude Fable 5 at half the price », à 0,5 % de Fable 5 sur CursorBench 3.2. Fable 5 garde l'avantage sur les tâches les plus longues/complexes et reste le seul tier Mythos-class ; Opus 5 devient l'option rationnelle pour la majorité des workloads Opus-tier (même mécanique de fallback classifier vers Opus 4.8).

---

## AJOUT 5 septembre 2026 — successeur : Fable 5.1

**Fable 5 n'est plus le modèle Fable par défaut.** [[Fable 5.1]] est sorti le **1er septembre 2026** (`claude-fable-5-1`) et le remplace comme défaut, y compris dans Claude Code (v2.1.257 : *« Added Claude Fable 5.1 (claude-fable-5-1), now the default Fable model »*).

Ce qui change par rapport à cette fiche :

| | Fable 5 | [[Fable 5.1]] |
|---|---|---|
| Prix input / output | $10 / $50 par MTok | **identique** — *« priced the same as Claude Fable 5, except for cache reads »* |
| Cache read | **$1 / MTok** (0,1 × input, ratio standard des modèles Claude) | **$0,25 / MTok** (0,025 × input) — *« pay a quarter of the Claude Fable 5 rate »* |
| Contexte | 1M par défaut | 1M par défaut / 128k output max |
| Effort défaut | `high` | `high` |
| Safeguards | classifier renforcé post-redéploiement, faux positifs fréquents sur coding/debugging | **moins de faux positifs** ; *« finding vulnerabilities in source code is permitted »* |

Les deux lignes de prix sont issues de la section *Pricing* de la page officielle « What's new in Claude Fable 5.1 » (vérifiée en source primaire le 5 septembre 2026) : le tarif cache de Fable 5 n'y est pas écrit en dollars, il se déduit du ratio explicite `0.1 × base input` que la page attribue aux modèles Claude autres que 5.1, appliqué au prix input $10 de Fable 5.

⚠️ **Gotchas de transition observés dans Claude Code** :
- Derrière un Claude apps gateway, les alias `fable` et `best` **continuent de résoudre vers Fable 5** tant que le gateway n'est pas configuré pour 5.1 — il faut choisir Fable 5.1 explicitement dans `/model`.
- Un agent `model: fable` pouvait tourner **silencieusement en 200K** au lieu de 1M si le tag `[1m]` d'un pin `ANTHROPIC_DEFAULT_FABLE_MODEL` était ignoré (corrigé en v2.1.260).

**Mythos 5.1** sort en parallèle : *« Claude Fable 5.1 and Claude Mythos 5.1 are the same model, but with different levels of safeguards »* — accès restreint aux organisations vetted (Project Glasswing, cybersécurité et sciences de la vie).

Prompting : les patterns de [[prompting-fable5-cheatsheet]] restent valides sans modification (*« your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes »*) ; les écarts comportementaux de 5.1 sont documentés en fin de cette même note.
