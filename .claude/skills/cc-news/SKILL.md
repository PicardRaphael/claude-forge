---
name: cc-news
description: ALWAYS invoke when Raphaël asks for news, nouveautés, what changed, whether a feature exists, or when a technical claim may be stale. Refreshes the vault from primary sources, corrects active false claims, and proposes genuinely new notes. NOT for a market tooling sweep (veille-outils-ia).
user-invocable: true
effort: high
allowed-tools: WebSearch, WebFetch, Read, Agent, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
argument-hint: "[proposal-only|apply] [claude-code|codex|chatgpt|rag|agents|fine-tuning|prompt|tout]"
---

# cc-news — veille vivante

Le workflow canonique est `docs/second-brain/news-refresh.md`. Le lire en entier
avant chaque run ; ne pas recopier sa doctrine ici.

Ne jamais faire tourner cette veille à effort `low` : le modèle répond alors de mémoire
au lieu de chercher, précisément sur le domaine où sa mémoire est périmée. Le frontmatter
fixe `high` et surcharge l'effort de session — ne pas l'abaisser.

## Démarrage

1. Lire `references/freshness-state.json`.
2. Déterminer le mode : une tâche planifiée ou `proposal-only` n'écrit rien ; une
   demande manuelle de news peut corriger une assertion active existante dans le
   vault ; une nouvelle note reste proposée.
3. Chercher le sujet dans forge-brain, puis lire en entier les notes pertinentes.
4. Charger seulement la référence de domaine nécessaire :

| Sujet | Référence |
|---|---|
| Claude Code / Anthropic | `references/domain-claude-code.md` |
| Codex / ChatGPT / OpenAI / Gemini / Cursor | `references/domain-concurrents.md` |
| RAG | `references/domain-rag.md` |
| agents / MCP | `references/domain-agents.md` |
| fine-tuning / local | `references/domain-finetuning.md` |
| prompting | `references/domain-prompt-engineering.md` |
| scan large | les domaines utiles + `references/domain-discovery.md` |

## Recherche

Toujours vérifier d'abord les sources primaires du domaine. Pour Claude Code,
comparer le changelog officiel et `npm view @anthropic-ai/claude-code version`.
Pour OpenAI, vérifier les docs Codex et les release notes ChatGPT officielles.

Les chercheurs sont read-only et rendent le schéma défini dans le contrat. Ne
leur transmettre aucun outil d'écriture ou MCP mutateur. Maximum quatre
chercheurs et 24 requêtes globales.

Une URL arXiv passe par `arxiv-verification`. Un finding majeur qui touche la
doctrine passe par `doctrine-impact-check`. Une norme invalidée suit
`methode-pivoter-doctrine`, puis `pivot-check`.

## Écriture et vérification

Appliquer exactement le writer borné du contrat : note entière lue, préimage,
assertion active distinguée de l'historique, seconde lecture, mutation MCP en
place, read-back, lint et CHANGELOG. Ne jamais supprimer automatiquement une
note entière.

Mettre à jour `freshness-state.json` uniquement quand tout le domaine est
complet. Un échec laisse l'ancien checkpoint et apparaît dans le rapport.

Rendre la réponse avec `references/format-reponse.md`, plus les statuts
`NOOP/UPDATE/SUPERSEDE/PROPOSE_NEW/DEFER/CONFLICT/IGNORE/FAILED`.

## Near misses

- Audit structurel ou qualité des notes sans recherche d'actualité → `vault-audit`.
- Prix, licences et paysage des outils IA → `veille-outils-ia`.
- Question stable déjà couverte par le vault → `forge-brain`, pas un scan news.
