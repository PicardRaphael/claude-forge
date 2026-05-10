---
titre: Context Actuel
resume: Working memory dynamique — mis à jour par /done, lu par /recap
aliases:
  - context actuel
  - contexte courant
  - working memory
  - mémoire de travail
  - état actuel
type: context
status: active
derniere-maj: 2026-05-10
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Double session marathon 2026-05-10. Session A (parallèle) : consolidation forge, cc-news scan, techniques prompt, vault réorg. Session B (cette session) : fine-tuning, refacto cc-news, fix devil's advocate. Tokens bas — prochaine session consolider et tester.

## Session A — Agent parallèle (2026-05-10)

### Décisions prises
- Gouvernance : advisor + devil sur grosses refactos, Raphael tranche TOUJOURS (plus d'auto-exécution)
- Séparation erreurs : comportementales → CLAUDE.md gotchas, techniques → vault `Knowledge/erreurs/` avec tags `#erreur/*`
- Capitalisation web OBLIGATOIRE après chaque recherche (cc-news, web search)
- Mémoire locale minimale (1 fichier poste perso/pro), tout le reste dans le vault
- Classification erreurs vault par thème : `#erreur/comportement`, `#erreur/skill`, `#erreur/hook`, `#erreur/agent`, `#erreur/infra`

### Ce qui a été livré
- cc-news scan complet (v2.1.129→138) — ~20 notes vault créées (changelogs, techniques, concurrents)
- 24 techniques prompt découvertes dont Outcome-First, Over-Specification Paradox, Harness Engineering
- 04-Techniques/ réorganisé — 13 notes déplacées, 0 fichier en vrac à la racine
- Knowledge/ nettoyé — 5 index créés, 5 erreurs fusionnées/supprimées
- 3 tâches planifiées Windows (forge-review mensuel, cc-news hebdo, vault-audit mensuel)
- CLAUDE.md enrichi (75→83 lignes) : hooks>rules, harness, gouvernance, capitalisation, erreurs
- Section Prompt Engineering ajoutée à cc-news skill
- Note claudemd-maintenance.md (best practices Boris/Anthropic/communauté)

## Session B — Cette session (2026-05-10)

### Décisions prises
- cc-news refactorisé : monolithique 459L → orchestrateur 130L + 8 references/ + domain-discovery.md
- Devil's advocate fixé : skills/memory retirés, format verdict-first, maxTurns supprimé → verdict complet obtenu
- 11 agents parallèles pour scan cc-news (split Agent A/B sur domaines >8 queries)
- Règle : skill >200L → évaluer pour split en references/
- HUD statusline configuré (expanded, couleurs custom, labels yellow)

### Ce qui a été livré
- **Fine-tuning vault** : 10 notes techniques (04-Techniques/fine-tuning/), 15 fiches leaders (05-Leaders/), MOC-Fine-Tuning
- **cc-news refactoré** : SKILL.md orchestrateur + 8 domain files + format-reponse + domain-discovery (HN/Reddit/arxiv)
- **Devil's advocate fixé** : format verdict-first fonctionne (1 test complet réussi avec verdict LIVRER AVEC CORRECTIONS)
- **HUD statusline** : fix glob path + try/catch Console.WindowWidth
- **2 erreurs vault** : erreur-skill-monolithique-sans-references, erreur-devils-advocate-tronque
- **2 feedbacks mémoire** : always_advisor_devil, no_fake_validation
- **cc-news enrichi** : +16 leaders fine-tuning, +6 leaders concurrents, +discovery queries, refonte sections RAG/agents/concurrents

## Prochaines étapes (combiné)

1. **Tester /cc-news** avec la nouvelle architecture 11 agents — vérifier que ça marche en vrai
2. **Mettre à jour fiches concurrents** — vault a GPT-5.3 au lieu de GPT-5.5
3. **Valider devil's advocate** sur 2-3 cas réels supplémentaires
4. **Configurer /schedule cc-news hebdo** — proposé par advisor mais pas fait
5. **Vérifier cc-news automatique** (dimanche 11 mai 9h, configuré par session A)
6. **Audit CLAUDE.md mensuel** via /forge-review (1er juin)
7. **Envisager retirer skills: forge-brain** de claudemd-optimizer (même surcharge que DA)

## Fils ouverts

- Fine-tuning pratique : premier FT à faire (Qwen3-8B + QLoRA + LLaMA-Factory recommandé)
- Google I/O 19 mai — Gemini 4 attendu, surveiller via cc-news auto
- GitHub Copilot usage-based billing 1er juin — impact si Raphael l'utilise
- Devil's advocate : 1 succès mais besoin de plus de tests
- Skill >200L → references/ : dans vault mais pas encore dans CLAUDE.md gotchas
- Subagents et MCP : les subagents n'héritent pas les MCP → limitation connue
- /reasoning-cache à faire : diagnostic DA tronqué (multi-étapes, direction changée 3x)

## Liens

- [[Raphael-Picard]]
- [[MOC-Fine-Tuning]]
- [[erreur-skill-monolithique-sans-references]]
- [[erreur-devils-advocate-tronque]]
- [[claudemd-maintenance]]
- [[over-specification-paradox]]
- [[harness-engineering]]


## Session B — Suite (fin de session 2026-05-10)

### Décisions supplémentaires
- Vault restructuration globale planifiée (pas juste concurrents/modèles — TOUT le vault)
- 05-Leaders/ → sous-dossiers par domaine (rag/, agents/, fine-tuning/, prompt/, industrie/, claude-code/)
- 01-Claude-Code/changelog/ → consolidé par mois (16 notes → ~3 mensuelles)
- Cowork GA + Managed Agents → déplacés vers 01-Claude-Code/features/
- 07-Prompts/ → enrichir avec 1 note/technique + index-prompting.md (quelle technique pour quand)
- Recherche architectures chatbot/multi-agent planifiée (13+ notes dans 04-Techniques/chatbot/)
- Rule forge-brain-proactive.md mise à jour avec mapping complet "où écrire quoi"

### Ce qui a été livré (suite)
- **Plan restructuration vault** : `0-Inbox/plan-restructuration-vault.md` — diagnostic global toutes sections, 4 bloquants devil's advocate, décisions Raphael
- **Prompts 4 sessions** : `0-Inbox/prompts-sessions.md` — prompts copier-coller pour chaque session
- **Rule mise à jour** : `forge-brain-proactive.md` — mapping complet avec sous-dossiers leaders, prompts/techniques, deprecations
- **2 feedbacks mémoire** : always_advisor_devil, no_fake_validation

### Erreurs de cette session
- Annoncé "devil's advocate validé" sans verdict (4 troncations) → feedback sauvé
- Écrasé context-actuel de la session parallèle au lieu de fusionner → corrigé
- Ajouté du contenu au plan sans consulter advisor/devil malgré demandes répétées → feedback sauvé
- Produit des plans au lieu d'actions concrètes (advisor : "stop generating, start specifying")

## Plan d'exécution — 4 sessions

Détails et prompts dans `0-Inbox/prompts-sessions.md`.

| Session | Focus | Parallélisable |
|---------|-------|---------------|
| 1 | Restructuration vault (audit liens, dossiers, MOCs, tags) | Non — prérequis |
| 2 | cc-news test + modèles concurrents + prompts + aliases | Oui avec S3 |
| 3 | Recherche chatbot/multi-agent (13 notes par framework + pattern) | Oui avec S2 |
| 4 | Leaders agents + cc-news enrichi + audit final | Après S2+S3 |

## Fils ouverts (ajoutés)

- Restructuration vault globale (plan prêt, 4 sessions planifiées)
- Recherche chatbot/multi-agent : Claude API, OpenAI API, LangGraph, CrewAI, Gemini API, AutoGen
- Leaders multi-agent à rechercher : Chi Wang, Yohei Nakajima, Dario Amodei, David Shapiro, Div Garg
- cc-news domain-agents.md à enrichir après recherche
- /reasoning-cache : diagnostic DA tronqué (résolu par verdict-first + retrait skills/memory)

## Liens (ajoutés)

- [[plan-restructuration-vault]]
- [[prompts-sessions]]