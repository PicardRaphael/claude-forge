---
titre: "Steps of AI Adoption — framework Boris Cherny (16 juillet 2026)"
resume: "Échelle de maturité 5 états (0-4) de l'adoption Claude Code par Boris Cherny : Gated → Assisted (pair) → Parallel (~10 agents) → Supervised autonomy (~100) → AI-native (~1000+, VP steering by intent). Thèse : les tokens ne suffisent pas, chaque transition = casser les bottlenecks + monter les guardrails. Anthropic = step 3→4, Boris perso = 4."
aliases:
  - "Steps of AI Adoption"
  - "steps adoption Boris"
  - "échelle maturité adoption Claude Code"
  - "gated assisted parallel supervised AI-native"
  - "framework adoption IA Cherny"
derniere-maj: 2026-07-27
auteur: claude
type: technique
sources:
  - "https://x.com/bcherny/status/2077929379661844559"
  - "https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf"
  - "https://docs.google.com/document/d/1R91ayvj7uvlxgNi--__2-Bf3w8x5r1nF-xIBN7ds8Ns"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/workflow"
  - "#doctrine/2026"
---

# Steps of AI Adoption — Boris Cherny

> Publié le **16 juillet 2026** (thread X @bcherny, 1,38M vues, 17k bookmarks + artifact claude.ai + LinkedIn). **Source primaire = thread X lu verbatim** (x-read authentifié, 27 juil.) ; la table détaillée vient d'un transcript Google Doc haute confiance corroboré par 6+ sources indépendantes — cellules non recoupées par le thread à citer avec cette réserve. ⚠️ Plusieurs blogs tiers affirment « publié sur anthropic.com » : **faux**.

## Thèse (verbatim thread)

> « one person is 10x'ing their output with Claude but the rest of the org hasn't caught up »

> « at each step, **tokens aren't enough** to move you forward: to get to the next step, you need to find and break down the next set of **bottlenecks**, and build up the next set of **guardrails**. »

Nuance sémantique : Boris parle de « the same 4 steps » = 4 **transitions** ; la table a **5 états (0-4)**.

## Les 5 états

| Step | Rôle humain | Agents | Unlock verbatim | Bottleneck |
|---|---|---|---|---|
| **0 Gated** | — | 0 | — | process sécu legacy, coût-par-token vs outcomes |
| **1 Assisted** | You + an agent (a pair) | ~1 | « A change that used to fill an afternoon becomes something you finish between meetings » | ton attention (tu lis tout, synchrone) |
| **2 Parallel** | Orchestrator | ~10 | « A backlog that used to take the team weeks becomes one engineer's afternoon of orchestration » | review de l'output, steering multi-sessions |
| **3 Supervised autonomy** | Manager of managers (org tree) | ~100 | maintenance/cleanup proactifs en background | confiance dans la boucle, throughput décisionnel |
| **4 AI-native** | VP steering by intent | ~1000+ | « The quarter-long migration becomes a workflow you kick off and check on » | identifier/automatiser le travail à l'échelle |

## Transitions clés (le contenu actionnable)

- **1→2** : plusieurs agents à la fois + **une boucle d'auto-vérification en laquelle tu as confiance** (tests + build + lint + e2e réel) + auto mode + code review automatisée.
- **2→3** : donner à Claude l'accès au contexte (code, wikis, discussions) ; **découper le travail en loops et routines** ; « **let Claude kick off Claude** ».
- **3→4** : automatisation par cas d'usage domaine (migrations, fuzzing, feature-building, remédiation feedback).
- Step 3 produits : **subagents + worktree isolation ; Routines, /loop, /batch, /goal ; dynamic workflows ; Claude Tag proactif**. Guardrails step 3 : CLAUDE.md + Skills pour encoder les standards, **casser CLAUDE.md en Skills lazy**, tuning classifier auto mode, advisors/LSPs pour l'efficience token.
- Step 4 : **Claude Agent SDK pour scheduler des agents programmatiquement ; la plupart des agents sont lancés par Claude**.
- Piège nommé (step 3) : **scaler le nombre d'agents AVANT que la boucle de vérification ait gagné une confiance large**.
- ROI (tweet 4) : l'usage mesure l'activité, pas le retour — la bonne question : « would you have spent engineering effort on this anyway? …what would it have cost in manual eng-hours? »

## Positionnement

- Verbatim : « **Anthropic is on step 3 and pushing toward 4. Personally, I just hit level 4.** »
- **Forge (27 juil. 2026)** : machinerie step 3 en place (routines, /loop, subagents+worktrees, review) ; l'écart vers 4 = proactivité (agents lancés par Claude, pas par Raphael) et boucles de vérification e2e systématiques.
- Précurseur direct : post Boris du 15 juil. (1,68M vues) — « If Claude instead writes a lint rule, CI step, or routine, that class of issue can be fully automated forever. **This is really what people are talking about when they talk about loops** ». Contexte : [[Mitchell-Hashimoto]] « My AI Adoption Journey » (5 fév. 2026) = framing précurseur.

## Wikilinks

- [[workflow-claude-code-optimal]] — les routines/multi-clauding = steps 2-3 en pratique
- [[concevoir-loops-travail]] — « découper le travail en loops et routines » (transition 2→3)
- [[pre-compute-vs-inference-loops-boris]] — le fondement théorique
- [[Boris Cherny]] — fiche leader
- [[CC juillet 2026 - Opus 5 + v2.1.212-220]] — fenêtre de publication
