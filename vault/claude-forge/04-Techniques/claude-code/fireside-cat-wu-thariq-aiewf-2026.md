---
titre: "Fireside Simon Willison × Cat Wu + Thariq (AIEWF, 21 juillet 2026) — doctrine prompting frontière, tools, sécu, evals"
resume: "Transcript annoté par Willison : system prompt CC réduit de ~80 % pour Fable/Opus 4.8 (retirer les exemples aide, don't-lists dégradent, fewer hard constraints), fewer tools (grep/glob supprimés pour bash natif), workflows = Claude prompting Claude all the way down, auto mode quasi universel en interne, mémoire Tag = un markdown par canal, gate de ship = rétention interne"
aliases:
  - "fireside Cat Wu Thariq"
  - "fireside Willison juillet 2026"
  - "system prompt -80%"
  - "fewer hard constraints more context"
  - "Claude prompting Claude all the way down"
  - "ant fooding"
derniere-maj: 2026-07-27
auteur: claude
type: technique
sources:
  - "https://simonwillison.net/2026/Jul/21/cat-and-thariq/"
  - "https://www.youtube.com/watch?v=uU5Gv2h8-9g"
  - "https://x.com/_catwu/status/2069473118742331608"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#domaine/prompt-engineering"
  - "#doctrine/2026"
---

# Fireside Simon Willison × Cat Wu + Thariq Shihipar — AI Engineer World's Fair (publié 21 juillet 2026)

> Cat Wu = Head of Product Claude Code ; Thariq = engineering lead CC, créateur de l'Agent SDK. Transcript édité/annoté par Simon Willison = quasi-primaire (crédit ÉLEVÉ-MAX). ⚠️ Verbatims extraits via pipeline WebFetch — re-vérifier mot à mot contre la page/vidéo avant citation exacte externe.

## 1. Doctrine prompting frontière (le cœur — system prompt −80 %)

- Le system prompt CC a été **réduit de ~80 %** pour les modèles frontière (Fable 5 ET Opus 4.8) ; les anciens modèles gardent le prompt complet. Confirmé par Thariq sur X le 24 juil. (@trq212, 3,9M vues) : « We removed ~80% of the Claude Code system prompt for our newest models ».
- **« removing examples was extremely helpful »** — Claude devient « more creative than the examples we gave it ». Willison note que ça contredit son propre conseil standard (les exemples ne sont « no longer best practice » sur Fable 5 / Opus 4.8).
- **Les « don't-lists » dégradent** : « don't do X and don't do Y » crée des conflits avec les instructions user en aval (« I've got this skill that says this and the system prompt says this »).
- Direction : « **fewer hard constraints, more context, and fewer instructions overall** » — donner une meilleure *shape* (tools, structure) plutôt que des interdits.
- **Méthode Cat Wu du « 100 % accurate »** : une instruction « 90% true » a un vrai 10 % de cas faux → chercher « the ways in which it could be misinterpreted by a well-intentioned human » puis « soften the prompt so that it's actually 100% accurate ». Exemple : « always verify » → « most of the time when you're doing front-end work you can't fully understand the experience by hitting the backend endpoints ».
- ⚠️ Périmètre : dit du SYSTEM PROMPT CC. La transposition aux CLAUDE.md/rules/skills user est une inférence — cohérente avec [[comment-ecrire-claudemd]] (règle testable + raison, pas d'ALL-CAPS) mais à calibrer : les don't-lists forge issues d'erreurs réelles portent leur « parce que ».

## 2. Tool design

- « **we've been trying to trend towards fewer tools** » ; principe Cat : « every tool we add has a distinct function from every other tool, so that Claude can very easily distinguish when to call each ».
- **grep/glob supprimés** du toolset CC « in favor of native bash ». Le file-edit tool survit pour le déterminisme UI (« so we could show people this nice UI ») — et Cat : en auto mode « I don't think it actually matters ».
- Thariq : les tools sont « **more of a biology than a physics** ».

## 3. Orchestration — position équipe

- Thariq : « **Workflows are actually a really good example… it's Claude not just prompting a single subagent, but prompting the orchestration of many subagents, and each one of them gets a very detailed prompt.** » — « almost a level above just spawning a subagent ». Et : « It's just Claude prompting Claude all the way down. »
- En creux : **zéro occurrence** de « harness », « multi-agent », « agent teams », « MCP » dans le transcript. La position = Claude compose l'orchestration dynamiquement, pas de graphes d'agents statiques (à croiser avec [[graph-engineering-buzz]] — silence d'Anthropic sur le buzz).

## 4. Sécurité

- Cat : « **Broadly within Anthropic, almost every single person uses auto mode.** » Durci « since January », rollout public fin mars ; « thousands of evals », red teamers adverses, « mitigated every single issue ».
- Mécanique : **un classifier Sonnet** juge chaque tool call avec le contexte conversationnel (permissions dynamiques) ; sandbox + évaluation des sorties de sandbox.
- Claim vendeur (à traiter comme tel) : « for the main categories of risks… prompt injection and data exfiltration, the risks are far lower than the average human reviewer ».
- Annonces : **trusted devices** (remote control) + **credential injection** — credentials « only usable by the agent but not accessible by the agent » (pattern proxy). Modèle pertinent pour les secrets/webhooks forge.

## 5. Usage interne (« ant fooding »)

- Gate de ship = **rétention interne** : « an internal bar for the number of active users and the amount of retention » — « If the feature isn't polished, people will churn — and then we shouldn't ship that feature. » (Analogue forge : verdicts KILL/EVOLVE/KEEP de /forge-review.)
- Code review : cap vers « **a world where humans don't need to be in the loop** » — code owners sur les zones critiques (system prompt a un code owner), review Claude complète sur les couches externes, confiance construite par mesure (« code review is catching 100% of the issues there ») ; incident → PRs fautives ajoutées à l'**eval set**.
- Claude Tag : « multiplayer by default », « the evolution of Claude Code » ; **65 % des PRs product engineering** de l'équipe CC (tweet Cat : « merges 65% of product PRs » — la variante « writes 65% of code » de la presse est imprécise). Mémoire Tag : « **a markdown file per channel** », mémoire partagée par canal, sessions qui recontribuent — validation directe de l'architecture markdown vault/memory forge. « We're always running memory experiments. »

## 6. Evals

- « **It takes a long time for customers to build really high-quality evals. So I think the tooling is less of the constraint, and more the skill set of how you build a great eval.** »
- Base d'evals pour que « new models can be a drop-in replacement » ; **behavioral evals** (en construction) distinctes des capability evals — comportements chassés : « it's time to go to sleep », « I finished two out of five parts — do you want me to continue? ».

## 7. Divers marquants

- Fable 5 « competent at editing video » (ffmpeg + Remotion, montage one-shot d'un talk avec tracking du speaker).
- Thariq pro-rewrite : « **a codebase is a spec, and maybe it's the only copy of the spec that you have** » / « rewrites are now good » (Bun réécrit en Rust).
- Cat : timeline idée→build « down from six to twelve months to maybe even a week » ; la valeur monte vers « product taste and business sense ».
- Anti-« Deep Blue » (Thariq) : « The way you offset that is by being more ambitious. »

## Wikilinks

- [[workflow-claude-code-optimal]] — foyer orchestration/routines
- [[mcp-vs-skills-doctrine]] — foyer tool design
- [[comment-ecrire-claudemd]] — foyer doctrine d'écriture des règles
- [[graph-engineering-buzz]] — le silence Anthropic sur les graphes
- [[cat-wu]] · [[Thariq Shihipar]] · [[Simon Willison]] — fiches leaders
- [[Fable 5]] · [[Opus 5]]
