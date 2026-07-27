---
name: cc-news
description: ALWAYS invoke when user asks 'quoi de neuf', 'est-ce que X existe', or knowledge seems stale. Recent Claude Code updates, new features, AI industry news. Reference date : 25 juillet 2026 (v2.1.220).
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Agent, mcp__forge-brain__*
argument-hint: "domaine ou sujet (ex: rag, agents, fine-tuning, concurrents, claude-code, prompt, tout)"
skills:
  - x-read
  - doctrine-impact-check
---

# cc-news — Veille IA & Claude Code

Date de référence : **25 juillet 2026** (v2.1.220 — Opus 5 nouveau défaut Opus + /fork vers session background + tool EndConversation + patch sécu permissions PowerShell 5.1 + nesting subagents depth 3 avec caps 200/20 + skills context:fork en background par défaut)
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

## Orchestration complète (16 agents parallèles)

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

Agent 1c : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent C — Équipe élargie Anthropic (postent moins souvent)'.
             Return findings as bullet list with source URLs."

Agent 2a : "Read .claude/skills/cc-news/references/domain-rag.md
             Execute ONLY the queries under heading '### Agent A — Techniques + outils'.
             Return findings as bullet list with source URLs."

Agent 2b : "Read .claude/skills/cc-news/references/domain-rag.md
             Execute ONLY the queries under heading '### Agent B — Leaders'.
             Return findings as bullet list with source URLs."

Agent 3a : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent A — Leaders + Frameworks'.
             Return findings as bullet list with source URLs."

Agent 3b : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent B — Produits + MCP'.
             Return findings as bullet list with source URLs."

Agent 3c : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent C — Leaders agents complémentaires'.
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

Agent 5c : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent C — Leaders industrie (vault 05-Leaders/industrie/)'.
             Return findings as bullet list with source URLs."

Agent 6a : "Read .claude/skills/cc-news/references/domain-prompt-engineering.md
             Execute ONLY the queries under heading '### Agent A — Guides officiels + techniques'.
             Return findings as bullet list with source URLs."

Agent 6b : "Read .claude/skills/cc-news/references/domain-prompt-engineering.md
             Execute ONLY the queries under heading '### Agent B — Chercheurs + papers'.
             Return findings as bullet list with source URLs."

Agent 7  : "Read .claude/skills/cc-news/references/domain-discovery.md
             Execute all queries in the file. Return findings as bullet list with source URLs. Max 7 queries.
             Focus on things NOT already known — new tools, new people, breakthrough papers.
             AVANT d'exécuter les queries, le parent aura passé un résumé des notes vault récentes.
             Ignorer les résultats qui correspondent à des sujets déjà documentés."
```

Synthétiser avec le format de references/format-reponse.md.

Avant de capitaliser un paper arXiv dans le vault → `Skill(arxiv-verification)` (vérifie YYMM / URL / venue avant citation — les deep-research LLM hallucinent versions et venues).

## Étapes

1. **Vault forge-brain d'abord** — `search_brain` sur le sujet pour voir ce qui est déjà connu (`derniere-maj`)
2. Exécuter Tier 0 (5 queries fixes)
3. Router selon $ARGUMENTS (domaine unique ou orchestration complète)
4. Identifier ce qui est postérieur à la date de référence
5. Vérifier les dépréciations et breaking changes
6. Résumer les nouveautés à l'utilisateur (format references/format-reponse.md)
7. **Confronter chaque finding MAJEUR à l'existant** (findings vérifiés source primaire, crédit ÉLEVÉ/MAX uniquement — anti-cascade) — Sur DEUX plans :
   - **Notes vault** : `search_brain` sur le sujet du finding. Une note couvre déjà ce sujet → décider MODIFIER la note existante (amendement, pas doublon) vs CRÉER une note neuve. Gate humaine `[v]/[m]/[i]` avant toute modification d'une note existante.
   - **Composants `.claude/`** : ce finding rend-il obsolète une skill / agent / hook / rule / CLAUDE.md ? (ex : mot-déclencheur renommé, API dépréciée, feature qui change un workflow). Si OUI → SIGNALER à l'utilisateur avec recommandation de modification, mais NE PAS modifier le composant directement (gate humaine obligatoire ; délégation aux agents spécialisés : skill-creator / subagent-creator / hook-creator / claudemd-creator).
8. **Capitaliser dans le vault forge-brain** (obligatoire, pas optionnel) — Si une nouvelle version CC est découverte, mettre à jour la date de référence et la version dans ce SKILL.md (ligne 3 description + ligne 11 body).
9. **Doctrine impact check** (sur les findings MAJEURS uniquement) — Pour chaque finding majeur d'un leader reconnu (05-Leaders/) ou d'Anthropic officiel issu de ce run, invoquer la skill `doctrine-impact-check` avec le finding (claim + source + URL) pour le croiser avec la doctrine canonique forge. PAS pour tout finding (anti-cascade : un run cc-news peut produire 30 findings, seuls les findings à fort crédit qui touchent une doctrine méritent le croisement). La skill produit un verdict INFO / DOCTRINE_PIVOT_CANDIDATE / DOCTRINE_REINFORCE avec gate humaine `[v]/[m]/[i]`.

### Fallback X/Twitter

Si une source à analyser est une URL X.com/Twitter (`https://x.com/...` ou `https://twitter.com/...`) :
- Defuddle et WebFetch échouent systématiquement sur X (DOM JS / HTTP 402)
- Invoquer la skill `x-read` avec l'URL en argument : `Skill(x-read, args="<url>")`
- Si la skill x-read n'est pas disponible (cookies absents, pas encore installée) → fallback :
  1. Demander à l'utilisateur de coller le contenu du tweet
  2. Capitaliser quand même dans le vault avec la source citée

## Capitalisation vault (étape 8)

- Nouvelle version CC → `01-Claude/Code/changelog/CC vX.Y.Z.md`
- Nouveau modèle → `<NN>-<Fournisseur>/models/<nom>.md`
- Feature produit/outil fournisseur → mettre à jour `<NN>-<Fournisseur>/products/<produit>/`
- Nouvelle technique → `04-Techniques/<sous-dossier>/`
- Info leader → mettre à jour `05-Leaders/`
- Info industrie → `06-Industrie/`
- Utiliser les templates de `Templates/` pour chaque nouveau type

Règle : **1 concept = 1 note atomique**. Mettre à jour les MOCs. Mettre à jour `derniere-maj`.
Voir skill `forge-brain` pour le format complet et les outils MCP.

## Sync des leaders depuis le vault (maintenance)

Les listes de leaders dans chaque `references/domain-*.md` sont générées par `scripts/sync-leaders.py` à partir des fiches `vault/claude-forge/05-Leaders/<domaine>/`. Le vault est la SOURCE UNIQUE — ne pas éditer le bloc entre les marqueurs `<!-- SYNC:leaders:start -->` et `<!-- SYNC:leaders:end -->` à la main (écrasé au prochain sync).

Relancer après avoir ajouté ou supprimé une fiche dans `05-Leaders/<domaine>/` :

```bash
py .claude/skills/cc-news/scripts/sync-leaders.py          # tous les domaines
py .claude/skills/cc-news/scripts/sync-leaders.py --domain rag   # un domaine
py .claude/skills/cc-news/scripts/sync-leaders.py --check        # dry-run, sans écrire
```

Mapping domaine → dossier vault : `domain-claude-code` → `claude-code`, `domain-agents` → `agents`, `domain-rag` → `rag`, `domain-finetuning` → `fine-tuning`, `domain-prompt-engineering` → `prompt`, `domain-concurrents` → `industrie`. `domain-discovery` n'a pas de leaders (pas synced).

**Handles X manquants** : le script ne peut injecter un `@handle` que si un lien `x.com/` est présent dans la fiche vault. Les leaders sans handle apparaissent sans `@` — leurs queries sont à compléter à la main. Dette tracée, pas un bug.

## MCP — accès direct (filet de sécurité)

Tu reçois normalement un brief enrichi de la session principale avec les éléments MCP pertinents déjà extraits (vault, DB, docs). Si pendant l'exécution tu rencontres un doute non couvert par ton brief (terme inconnu, décision technique conflictuelle, pattern incertain, valeur précise non fournie), tu peux re-consulter directement le MCP via `mcp__forge-brain__*`.

**Pas systématique** — la session principale t'a déjà briefé. C'est un filet de sécurité, pas une exploration parallèle. Anti-pattern : scanner par réflexe (coût tokens × N agents).

**Quand l'utiliser** :
- ✅ Terme/acronyme non défini dans le brief
- ✅ Conflit entre 2 approches mentionnées
- ✅ Valeur précise nécessaire (note canonique exacte)
- ❌ Re-vérifier ce que le brief dit clairement
- ❌ "Au cas où" sans déclencheur précis

Source canonique : [[pattern-mcp-brief-then-direct]] vault forge.

## Gotchas

- **Max 6-8 queries par agent** — au-delà l'agent perd le fil. Les reference files sont conçus pour respecter ce budget.
- **fine-tuning = 2 agents ; rag + prompt = 2 agents chacun ; claude-code + agents + concurrents = 3 agents chacun** — ces domaines dépassent 8 queries ; l'orchestration complète utilise 16 agents (pas 6) pour cette raison.
- **Vault AVANT de chercher** — éviter de re-chercher ce qui est documenté avec un `derniere-maj` récent.
- **Capitaliser APRÈS le scan** — l'étape 8 est obligatoire, pas optionnelle.
- **Modèle vs produit vs industrie** — GPT-5.5 → `02-OpenAI/models/`. Codex CLI → `02-OpenAI/products/`. Acquisition/funding → `06-Industrie/`. Pas de dossier « Concurrents » : un fournisseur = un dossier acteur (`models/` + `products/`).
- **Ne pas hardcoder l'année dans les queries** — les reference files n'ont pas "2026" dans leurs queries ; la date de référence dans ce fichier suffit.
- **Si un agent ne retourne rien** — relancer le domaine individuellement plutôt que l'ignorer. Un scan incomplet doit être signalé.
- **X/Twitter inaccessible via Defuddle/WebFetch** — toujours déléguer à la skill `x-read` (utilise cookies du compte authentifié). Si x-read pas dispo → demander coller le contenu à l'utilisateur, ne pas abandonner la source.
- **Étape 9 sélective** — invoquer `doctrine-impact-check` seulement sur findings majeurs (leader/Anthropic), jamais sur tout finding (anti-cascade fatigue de validation).
- **Ne pas éditer manuellement le bloc SYNC** — le bloc `<!-- SYNC:leaders:start/end -->` dans les domain-*.md est géré par `scripts/sync-leaders.py`. Toute édition manuelle sera écrasée au prochain sync.
