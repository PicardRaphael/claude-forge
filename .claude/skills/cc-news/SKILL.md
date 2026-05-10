---
name: cc-news
description: Use this skill when the user asks about recent Claude Code updates, new features, AI industry news, or when any information might be outdated. Use PROACTIVELY when the user asks "quoi de neuf", "est-ce que X existe maintenant", or when knowledge seems stale. Date de reference : 10 mai 2026 (v2.1.138).
user-invokable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Agent
argument-hint: "domaine ou sujet (ex: rag, agents, fine-tuning, concurrents, claude-code, prompt, tout)"
---

# cc-news — Veille IA & Claude Code

Date de référence : **10 mai 2026** (v2.1.138)
Tout ce qui est postérieur à cette date doit être recherché.

## Tier 0 — Vérifier EN PREMIER (toujours, avant tout routage)

Ces 5 queries s'exécutent quel que soit $ARGUMENTS :

```
Claude Code changelog site:github.com/anthropics/claude-code
@AnthropicAI Claude announcements
frontier model release OpenAI GPT OR Google Gemini OR Claude
Claude Code deprecated OR breaking
[si $ARGUMENTS fourni] Claude Code $ARGUMENTS
```

Puis consulter le vault forge-brain pour vérifier ce qui est déjà documenté :
`search_brain("Claude Code changelog")` + `search_brain("$ARGUMENTS")` si fourni.

## Routage $ARGUMENTS

| $ARGUMENTS | Action |
|------------|--------|
| vide ou "tout" | Lancer 11 agents parallèles (orchestration complète) |
| "claude-code" ou "CC" | Read references/domain-claude-code.md → exécuter ses queries |
| "rag" ou "embeddings" | Read references/domain-rag.md → exécuter ses queries |
| "agents" ou "agentic" | Read references/domain-agents.md → exécuter ses queries (2 agents) |
| "fine-tuning" ou "ft" ou "local" | Read references/domain-finetuning.md → exécuter ses queries (2 agents) |
| "concurrents" ou "openai" ou "gemini" ou "cursor" | Read references/domain-concurrents.md → exécuter ses queries (2 agents) |
| "prompt" ou "prompting" | Read references/domain-prompt-engineering.md → exécuter ses queries |
| sujet spécifique (ex: "GPT-5.5") | search_brain(sujet) puis WebSearch sur les domaines pertinents |

## Orchestration complète (11 agents parallèles)

Avant de lancer les agents, faire `search_brain("recent")` pour obtenir les notes récentes du vault.
Passer les titres des notes récentes dans le prompt de l'Agent Discovery pour qu'il filtre les doublons.

Lancer via Agent tool simultanément — chaque agent lit son fichier de référence et exécute les queries indiquées :

Chaque agent doit ajouter l'année en cours aux queries non-`site:` pour obtenir des résultats récents.
Exemple : "Jonas Roman RAG production" → chercher "Jonas Roman RAG production 2026" (ou l'année courante).
Les queries `site:` n'ont pas besoin d'année — les résultats sont déjà triés par date.

```
Agent 1a : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent A — Officiel + Équipe'.
             Return findings as bullet list with source URLs."

Agent 1b : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent B — Plugins + Écosystème'.
             Return findings as bullet list with source URLs."

Agent 2  : "Read .claude/skills/cc-news/references/domain-rag.md
             Execute all queries in the file. Return findings as bullet list with source URLs. Max 11 queries."

Agent 3a : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent A — Leaders + Frameworks'.
             Return findings as bullet list with source URLs."

Agent 3b : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent B — Produits + MCP'.
             Return findings as bullet list with source URLs."

Agent 4a : "Read .claude/skills/cc-news/references/domain-finetuning.md
             Execute ONLY the queries under heading '### Agent A — Leaders (queries 1-10)'.
             Return findings as bullet list."

Agent 4b : "Read .claude/skills/cc-news/references/domain-finetuning.md
             Execute ONLY the queries under heading '### Agent B — Techniques + Benchmarks (queries 11-20)'.
             Return findings as bullet list."

Agent 5a : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent A — OpenAI + Google'.
             Return findings as bullet list with source URLs."

Agent 5b : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent B — Cursor + Copilot + xAI + Leaders'.
             Return findings as bullet list with source URLs."

Agent 6  : "Read .claude/skills/cc-news/references/domain-prompt-engineering.md
             Execute all queries in the file. Return findings as bullet list with source URLs. Max 10 queries."

Agent 7  : "Read .claude/skills/cc-news/references/domain-discovery.md
             Execute all queries in the file. Return findings as bullet list with source URLs. Max 7 queries.
             Focus on things NOT already known — new tools, new people, breakthrough papers.
             AVANT d'exécuter les queries, le parent aura passé un résumé des notes vault récentes.
             Ignorer les résultats qui correspondent à des sujets déjà documentés."
```

Synthétiser avec le format de references/format-reponse.md.

## Étapes

1. **Vault forge-brain d'abord** — `search_brain` sur le sujet pour voir ce qui est déjà connu (`derniere-maj`)
2. Exécuter Tier 0 (5 queries fixes)
3. Router selon $ARGUMENTS (domaine unique ou orchestration complète)
4. Identifier ce qui est postérieur à la date de référence
5. Vérifier les dépréciations et breaking changes
6. Résumer les nouveautés à l'utilisateur (format references/format-reponse.md)
7. **Capitaliser dans le vault forge-brain** (obligatoire, pas optionnel) — Si une nouvelle version CC est découverte, mettre à jour la date de référence et la version dans ce SKILL.md (ligne 3 description + ligne 11 body).

## Capitalisation vault (étape 7)

- Nouvelle version CC → `01-Claude-Code/changelog/CC vX.Y.Z.md`
- Nouveau modèle → `03-Modeles/<provider>/<nom>.md`
- Feature concurrent → mettre à jour `02-Concurrents/<produit>/`
- Nouvelle technique → `04-Techniques/<sous-dossier>/`
- Info leader → mettre à jour `05-Leaders/`
- Info industrie → `06-Industrie/`
- Utiliser les templates de `Templates/` pour chaque nouveau type

Règle : **1 concept = 1 note atomique**. Mettre à jour les MOCs. Mettre à jour `derniere-maj`.
Voir skill `forge-brain` pour le format complet et les outils MCP.

## Gotchas

- **Max 6-8 queries par agent** — au-delà l'agent perd le fil. Les reference files sont conçus pour respecter ce budget.
- **fine-tuning + concurrents + agents + claude-code = 2 agents chacun** — ces domaines dépassent 8 queries ; l'orchestration complète utilise 11 agents (pas 6) pour cette raison.
- **Vault AVANT de chercher** — éviter de re-chercher ce qui est documenté avec un `derniere-maj` récent.
- **Capitaliser APRÈS le scan** — l'étape 7 est obligatoire, pas optionnelle.
- **Modèle vs produit vs industrie** — GPT-5.5 → `03-Modeles/`. Feature Codex CLI → `02-Concurrents/`. Acquisition/funding → `06-Industrie/`. Ne pas tout mettre dans Concurrents.
- **Ne pas hardcoder l'année dans les queries** — les reference files n'ont pas "2026" dans leurs queries ; la date de référence dans ce fichier suffit.
- **Si un agent ne retourne rien** — relancer le domaine individuellement plutôt que l'ignorer. Un scan incomplet doit être signalé.
