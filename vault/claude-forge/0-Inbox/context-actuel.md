---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-24 tour 3 marathon (40+ tours) : workflow sub-agents enforcement + delegate-guard fix + 36 frontmatters wildcard MCP + vault enrichi."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Chantier majeur 24 mai 2026 marathon (40+ tours) terminé et pushé sur 3 repos. Workflow sub-agents enforcement aligné doctrine Anthropic 2026 (Thariq, AskUserQuestion limitation, wildcard MCP). 8 chantiers cohérents shippés ensemble : delegate-guard fix + 14 frontmatters MCP forge + pattern ESCALADE/AMBIGUÏTÉ sur 15 sub-agents + hook escalade-detector + 10 skills directives + plugin feature-dev + /spec HTML + notes canoniques enrichies.

## Dernière session (2026-05-24 tour 3 — marathon)

### Décisions prises

- **Patch delegate-guard.py** : lecture stdin `agent_type` au lieu d'env var dead code → sub-agents éditeurs peuvent enfin bypasser
- **Pattern AMBIGUÏTÉ DÉTECTÉE** sur 15 sub-agents (vault canonique `anti-reentrance-sub-agents-pattern-escalade` étendu — AskUserQuestion ne marche pas en sub-agent, issue Anthropic #18721)
- **Wildcard `mcp__server__*`** sur 36 frontmatters (14 forge + 9 neo_ia + 13 ia_back) — syntaxe Anthropic officielle vérifiée verbatim
- **Formule directive skills** `ALWAYS invoke when X. DO NOT Y` sur 10 skills critiques (audit communautaire 214 skills = 73% silencieusement cassées sans formule)
- **Hook SubagentStop escalade-detector** créé : Python neo_ia + TS ia_back, non-bloquant, doctrine 22 mai préservée
- **Plugin feature-dev Anthropic** activé sur neo_ia + ia_back (Raphael l'a installé via /plugin install)
- **/spec étendue option HTML** : Thariq Shihipar pattern (HTML > Markdown 17/20 pour plans/specs)
- **CLAUDE.md ligne 13** : instruction forçant consultation vault AVANT toute proposition (anti-pattern 40 tours sans vault)
- **5 lignes Karpathy ouverture** CLAUDE.md préservées
- **Doctrine 22 mai préservée** : pas de retour workflow gates. Enforcement = advisory + skills directives + sub-agents qui escaladent

### En cours / shipped

- 3 commits push 3 repos (forge `28ad3ff` GitHub, neo_ia `749d381` Bitbucket, ia_back `8751171` Bitbucket)
- ~80 fichiers modifiés / créés, ~1500 lignes shipped
- 4 nouveaux feedbacks mémoire (askuserquestion, mcp-wildcard, self-modification, sub-agent-invente)
- 6 notes vault forge enrichies (4 canoniques + 2 erreurs + 1 nouvelle html-vs-markdown-thariq)

### Prochaines étapes

- **Test comportemental** : lancer une vraie feature dans neo_ia ou ia_back pour vérifier que le pipeline architect→dev→/go fonctionne avec ESCALADE en cas d'ambiguïté
- **Mesure efficacité formule directive skills** : observer si auto-invocation passe de ~50% à > 80% sur add-endpoint / create-tool / create-agent
- **Capitaliser apprentissages méta** : 4 nouveaux feedbacks créés ce soir, en consulter avant chaque session future

## Fils ouverts

- **Plugin feature-dev usage réel** : utiliser le pipeline 7 phases sur une vraie feature pour comparer avec /spec custom
- **Token cost MCP audit** : si Raphael s'inquiète des tokens, faire mesure réelle nombre MCP servers actifs vs Thariq seuil "50-100 tools = modèle se perd"
- **Format HTML pour autres docs** : Knowledge/decisions/ADR-NNN-X.html ? lojii/docs/design-system.html ? — à explorer si pertinent
- **Forge méta-framework** vs neo_ia/ia_back applicatif : la différence est claire (forge = framework Claude Code, neo_ia/ia_back = produits). Pas de propagation aveugle entre les 3.

## Apprentissages méta

- **Vault consultation est un RÉFLEXE** — Raphael l'a forcé à 40 tours en l'inscrivant dans CLAUDE.md ligne 13. Pattern récurrent à briser.
- **Sub-agents inventent des refus** : pattern `feedback_sub_agent_invente_classifier` capitalisé. Toujours demander verbatim error, jamais paraphrase.
- **Self-modification = cross-dispatch** : pour modifier agent-creator, dispatcher skill-creator. Pattern `feedback_self_modification_agent_cross_dispatch` capitalisé.
- **Wildcard MCP token cost = négligeable** : le vrai risque token = nombre MCP servers actifs (Thariq).

## Liens

- [[Raphael Picard]]
- [[claude-forge]]
- [[anti-reentrance-sub-agents-pattern-escalade]]
- [[html-vs-markdown-thariq]]
- [[comment-creer-agent]] (sections AJOUT 24 mai)
- [[comment-creer-hook]] (section AJOUT 24 mai)
- [[comment-creer-skill]] (section AJOUT 24 mai)
- [[workflow-claude-code-optimal]] (pipeline ADR enrichi)
- [[erreur-delegate-guard-env-var-vs-stdin]]
- [[raisonnement-22mai-doctrine-vs-enforcement]] (doctrine préservée)
