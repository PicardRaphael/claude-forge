---
name: cc-news
description: 'ALWAYS invoke when user asks "quoi de neuf", "est-ce que X existe", or knowledge seems stale. Recent Claude Code updates, new features, AI industry news. Reference date : 2 juin 2026 (v2.1.160 â€” workflow trigger renamed ultracode + Opus 4.8).'
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Write, Agent, mcp__forge-brain__*
argument-hint: "domaine ou sujet (ex: rag, agents, fine-tuning, concurrents, claude-code, prompt, tout)"
skills:
  - x-read
  - doctrine-impact-check
---

# cc-news â€” Veille IA & Claude Code

Date de rÃ©fÃ©rence : **2 juin 2026** (v2.1.160 â€” workflow trigger renamed ultracode + Opus 4.8 + Dynamic Workflows)
Tout ce qui est postÃ©rieur Ã  cette date doit Ãªtre recherchÃ©.

## Tier 0 â€” VÃ©rifier EN PREMIER (toujours, avant tout routage)

Ces 5 queries s'exÃ©cutent quel que soit $ARGUMENTS :

```
Claude Code changelog site:github.com/anthropics/claude-code
@AnthropicAI Claude announcements
frontier model release OpenAI GPT OR Google Gemini OR Claude
Claude Code deprecated OR breaking
[si $ARGUMENTS fourni] Claude Code $ARGUMENTS
```

Puis consulter le vault forge-brain pour vÃ©rifier ce qui est dÃ©jÃ  documentÃ© :
`search_brain("Claude Code changelog")` + `search_brain("$ARGUMENTS")` si fourni.

## Routage $ARGUMENTS

| $ARGUMENTS | Action |
|------------|--------|
| vide ou "tout" | Lancer 11 agents parallÃ¨les (orchestration complÃ¨te) |
| "claude-code" ou "CC" | Read references/domain-claude-code.md â†’ exÃ©cuter ses queries |
| "rag" ou "embeddings" | Read references/domain-rag.md â†’ exÃ©cuter ses queries |
| "agents" ou "agentic" | Read references/domain-agents.md â†’ exÃ©cuter ses queries (2 agents) |
| "fine-tuning" ou "ft" ou "local" | Read references/domain-finetuning.md â†’ exÃ©cuter ses queries (2 agents) |
| "concurrents" ou "openai" ou "gemini" ou "cursor" | Read references/domain-concurrents.md â†’ exÃ©cuter ses queries (2 agents) |
| "prompt" ou "prompting" | Read references/domain-prompt-engineering.md â†’ exÃ©cuter ses queries |
| sujet spÃ©cifique (ex: "GPT-5.5") | search_brain(sujet) puis WebSearch sur les domaines pertinents |

## Orchestration complÃ¨te (16 agents parallÃ¨les)

Avant de lancer les agents, faire `search_brain("recent")` pour obtenir les notes rÃ©centes du vault.
Passer les titres des notes rÃ©centes dans le prompt de l'Agent Discovery pour qu'il filtre les doublons.

Lancer via Agent tool simultanÃ©ment â€” chaque agent lit son fichier de rÃ©fÃ©rence et exÃ©cute les queries indiquÃ©es :

Chaque agent doit ajouter l'annÃ©e en cours aux queries non-`site:` pour obtenir des rÃ©sultats rÃ©cents.
Exemple : "Jonas Roman RAG production" â†’ chercher "Jonas Roman RAG production 2026" (ou l'annÃ©e courante).
Les queries `site:` n'ont pas besoin d'annÃ©e â€” les rÃ©sultats sont dÃ©jÃ  triÃ©s par date.

```
Agent 1a : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent A â€” Officiel + Ã‰quipe'.
             Return findings as bullet list with source URLs."

Agent 1b : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent B â€” Plugins + Ã‰cosystÃ¨me'.
             Return findings as bullet list with source URLs."

Agent 1c : "Read .claude/skills/cc-news/references/domain-claude-code.md
             Execute ONLY the queries under heading '### Agent C â€” Ã‰quipe Ã©largie Anthropic (postent moins souvent)'.
             Return findings as bullet list with source URLs."

Agent 2a : "Read .claude/skills/cc-news/references/domain-rag.md
             Execute ONLY the queries under heading '### Agent A â€” Techniques + outils'.
             Return findings as bullet list with source URLs."

Agent 2b : "Read .claude/skills/cc-news/references/domain-rag.md
             Execute ONLY the queries under heading '### Agent B â€” Leaders'.
             Return findings as bullet list with source URLs."

Agent 3a : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent A â€” Leaders + Frameworks'.
             Return findings as bullet list with source URLs."

Agent 3b : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent B â€” Produits + MCP'.
             Return findings as bullet list with source URLs."

Agent 3c : "Read .claude/skills/cc-news/references/domain-agents.md
             Execute ONLY the queries under heading '### Agent C â€” Leaders agents complÃ©mentaires'.
             Return findings as bullet list with source URLs."

Agent 4a : "Read .claude/skills/cc-news/references/domain-finetuning.md
             Execute ONLY the queries under heading '### Agent A â€” Leaders (queries 1-10)'.
             Return findings as bullet list."

Agent 4b : "Read .claude/skills/cc-news/references/domain-finetuning.md
             Execute ONLY the queries under heading '### Agent B â€” Techniques + Benchmarks (queries 11-20)'.
             Return findings as bullet list."

Agent 5a : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent A â€” OpenAI + Google'.
             Return findings as bullet list with source URLs."

Agent 5b : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent B â€” Cursor + Copilot + xAI + Leaders'.
             Return findings as bullet list with source URLs."

Agent 5c : "Read .claude/skills/cc-news/references/domain-concurrents.md
             Execute ONLY the queries under heading '### Agent C â€” Leaders industrie (vault 05-Leaders/industrie/)'.
             Return findings as bullet list with source URLs."

Agent 6a : "Read .claude/skills/cc-news/references/domain-prompt-engineering.md
             Execute ONLY the queries under heading '### Agent A â€” Guides officiels + techniques'.
             Return findings as bullet list with source URLs."

Agent 6b : "Read .claude/skills/cc-news/references/domain-prompt-engineering.md
             Execute ONLY the queries under heading '### Agent B â€” Chercheurs + papers'.
             Return findings as bullet list with source URLs."

Agent 7  : "Read .claude/skills/cc-news/references/domain-discovery.md
             Execute all queries in the file. Return findings as bullet list with source URLs. Max 7 queries.
             Focus on things NOT already known â€” new tools, new people, breakthrough papers.
             AVANT d'exÃ©cuter les queries, le parent aura passÃ© un rÃ©sumÃ© des notes vault rÃ©centes.
             Ignorer les rÃ©sultats qui correspondent Ã  des sujets dÃ©jÃ  documentÃ©s."
```

SynthÃ©tiser avec le format de references/format-reponse.md.

## Ã‰tapes

1. **Vault forge-brain d'abord** â€” `search_brain` sur le sujet pour voir ce qui est dÃ©jÃ  connu (`derniere-maj`)
2. ExÃ©cuter Tier 0 (5 queries fixes)
3. Router selon $ARGUMENTS (domaine unique ou orchestration complÃ¨te)
4. Identifier ce qui est postÃ©rieur Ã  la date de rÃ©fÃ©rence
5. VÃ©rifier les dÃ©prÃ©ciations et breaking changes
6. RÃ©sumer les nouveautÃ©s Ã  l'utilisateur (format references/format-reponse.md)
7. **Confronter chaque finding MAJEUR Ã  l'existant** (findings vÃ©rifiÃ©s source primaire, crÃ©dit Ã‰LEVÃ‰/MAX uniquement â€” anti-cascade) â€” Sur DEUX plans :
   - **Notes vault** : `search_brain` sur le sujet du finding. Une note couvre dÃ©jÃ  ce sujet â†’ dÃ©cider MODIFIER la note existante (amendement, pas doublon) vs CRÃ‰ER une note neuve. Gate humaine `[v]/[m]/[i]` avant toute modification d'une note existante.
   - **Composants `.claude/`** : ce finding rend-il obsolÃ¨te une skill / agent / hook / rule / CLAUDE.md ? (ex : mot-dÃ©clencheur renommÃ©, API dÃ©prÃ©ciÃ©e, feature qui change un workflow). Si OUI â†’ SIGNALER Ã  l'utilisateur avec recommandation de modification, mais NE PAS modifier le composant directement (gate humaine obligatoire ; dÃ©lÃ©gation aux agents spÃ©cialisÃ©s : skill-creator / subagent-creator / hook-creator / claudemd-creator).
8. **Capitaliser dans le vault forge-brain** (obligatoire, pas optionnel) â€” Si une nouvelle version CC est dÃ©couverte, mettre Ã  jour la date de rÃ©fÃ©rence et la version dans ce SKILL.md (ligne 3 description + ligne 11 body).
9. **Doctrine impact check** (sur les findings MAJEURS uniquement) â€” Pour chaque finding majeur d'un leader reconnu (05-Leaders/) ou d'Anthropic officiel issu de ce run, invoquer la skill `doctrine-impact-check` avec le finding (claim + source + URL) pour le croiser avec la doctrine canonique forge. PAS pour tout finding (anti-cascade : un run cc-news peut produire 30 findings, seuls les findings Ã  fort crÃ©dit qui touchent une doctrine mÃ©ritent le croisement). La skill produit un verdict INFO / DOCTRINE_PIVOT_CANDIDATE / DOCTRINE_REINFORCE avec gate humaine `[v]/[m]/[i]`.

### Fallback X/Twitter

Si une source Ã  analyser est une URL X.com/Twitter (`https://x.com/...` ou `https://twitter.com/...`) :
- Defuddle et WebFetch Ã©chouent systÃ©matiquement sur X (DOM JS / HTTP 402)
- Invoquer la skill `x-read` avec l'URL en argument : `Skill(x-read, args="<url>")`
- Si la skill x-read n'est pas disponible (cookies absents, pas encore installÃ©e) â†’ fallback :
  1. Demander Ã  l'utilisateur de coller le contenu du tweet
  2. Capitaliser quand mÃªme dans le vault avec la source citÃ©e

## Capitalisation vault (Ã©tape 8)

- Nouvelle version CC â†’ `01-Claude/Code/changelog/CC vX.Y.Z.md`
- Nouveau modÃ¨le â†’ `03-Modeles/<provider>/<nom>.md`
- Feature concurrent â†’ mettre Ã  jour `02-Concurrents/<produit>/`
- Nouvelle technique â†’ `04-Techniques/<sous-dossier>/`
- Info leader â†’ mettre Ã  jour `05-Leaders/`
- Info industrie â†’ `06-Industrie/`
- Utiliser les templates de `Templates/` pour chaque nouveau type

RÃ¨gle : **1 concept = 1 note atomique**. Mettre Ã  jour les MOCs. Mettre Ã  jour `derniere-maj`.
Voir skill `forge-brain` pour le format complet et les outils MCP.

## Sync des leaders depuis le vault (maintenance)

Les listes de leaders dans chaque `references/domain-*.md` sont gÃ©nÃ©rÃ©es par `scripts/sync-leaders.py` Ã  partir des fiches `vault/claude-forge/05-Leaders/<domaine>/`. Le vault est la SOURCE UNIQUE â€” ne pas Ã©diter le bloc entre les marqueurs `<!-- SYNC:leaders:start -->` et `<!-- SYNC:leaders:end -->` Ã  la main (Ã©crasÃ© au prochain sync).

Relancer aprÃ¨s avoir ajoutÃ© ou supprimÃ© une fiche dans `05-Leaders/<domaine>/` :

```bash
py .claude/skills/cc-news/scripts/sync-leaders.py          # tous les domaines
py .claude/skills/cc-news/scripts/sync-leaders.py --domain rag   # un domaine
py .claude/skills/cc-news/scripts/sync-leaders.py --check        # dry-run, sans Ã©crire
```

Mapping domaine â†’ dossier vault : `domain-claude-code` â†’ `claude-code`, `domain-agents` â†’ `agents`, `domain-rag` â†’ `rag`, `domain-finetuning` â†’ `fine-tuning`, `domain-prompt-engineering` â†’ `prompt`, `domain-concurrents` â†’ `industrie`. `domain-discovery` n'a pas de leaders (pas synced).

**Handles X manquants** : le script ne peut injecter un `@handle` que si un lien `x.com/` est prÃ©sent dans la fiche vault. Les leaders sans handle apparaissent sans `@` â€” leurs queries sont Ã  complÃ©ter Ã  la main. Dette tracÃ©e, pas un bug.

## MCP â€” accÃ¨s direct (filet de sÃ©curitÃ©)

Tu reÃ§ois normalement un brief enrichi de la session principale avec les Ã©lÃ©ments MCP pertinents dÃ©jÃ  extraits (vault, DB, docs). Si pendant l'exÃ©cution tu rencontres un doute non couvert par ton brief (terme inconnu, dÃ©cision technique conflictuelle, pattern incertain, valeur prÃ©cise non fournie), tu peux re-consulter directement le MCP via `mcp__forge-brain__*`.

**Pas systÃ©matique** â€” la session principale t'a dÃ©jÃ  briefÃ©. C'est un filet de sÃ©curitÃ©, pas une exploration parallÃ¨le. Anti-pattern : scanner par rÃ©flexe (coÃ»t tokens Ã— N agents).

**Quand l'utiliser** :
- âœ… Terme/acronyme non dÃ©fini dans le brief
- âœ… Conflit entre 2 approches mentionnÃ©es
- âœ… Valeur prÃ©cise nÃ©cessaire (note canonique exacte)
- âŒ Re-vÃ©rifier ce que le brief dit clairement
- âŒ "Au cas oÃ¹" sans dÃ©clencheur prÃ©cis

Source canonique : [[pattern-mcp-brief-then-direct]] vault forge.

## Gotchas

- **Max 6-8 queries par agent** â€” au-delÃ  l'agent perd le fil. Les reference files sont conÃ§us pour respecter ce budget.
- **fine-tuning = 2 agents ; rag + prompt = 2 agents chacun ; claude-code + agents + concurrents = 3 agents chacun** â€” ces domaines dÃ©passent 8 queries ; l'orchestration complÃ¨te utilise 16 agents (pas 6) pour cette raison.
- **Vault AVANT de chercher** â€” Ã©viter de re-chercher ce qui est documentÃ© avec un `derniere-maj` rÃ©cent.
- **Capitaliser APRÃˆS le scan** â€” l'Ã©tape 8 est obligatoire, pas optionnelle.
- **ModÃ¨le vs produit vs industrie** â€” GPT-5.5 â†’ `03-Modeles/`. Feature Codex CLI â†’ `02-Concurrents/`. Acquisition/funding â†’ `06-Industrie/`. Ne pas tout mettre dans Concurrents.
- **Ne pas hardcoder l'annÃ©e dans les queries** â€” les reference files n'ont pas "2026" dans leurs queries ; la date de rÃ©fÃ©rence dans ce fichier suffit.
- **Si un agent ne retourne rien** â€” relancer le domaine individuellement plutÃ´t que l'ignorer. Un scan incomplet doit Ãªtre signalÃ©.
- **X/Twitter inaccessible via Defuddle/WebFetch** â€” toujours dÃ©lÃ©guer Ã  la skill `x-read` (utilise cookies du compte authentifiÃ©). Si x-read pas dispo â†’ demander coller le contenu Ã  l'utilisateur, ne pas abandonner la source.
- **Ã‰tape 9 sÃ©lective** â€” invoquer `doctrine-impact-check` seulement sur findings majeurs (leader/Anthropic), jamais sur tout finding (anti-cascade fatigue de validation).
- **Ne pas Ã©diter manuellement le bloc SYNC** â€” le bloc `<!-- SYNC:leaders:start/end -->` dans les domain-*.md est gÃ©rÃ© par `scripts/sync-leaders.py`. Toute Ã©dition manuelle sera Ã©crasÃ©e au prochain sync.
