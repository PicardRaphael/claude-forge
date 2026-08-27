---
name: cc-news
description: ALWAYS invoke when Raphaël asks for news, nouveautés, what changed, whether a feature exists, or when a technical claim may be stale. Refreshes the vault from primary sources, corrects active false claims, and proposes genuinely new notes. NOT for a market tooling sweep (veille-outils-ia).
---

# cc-news — adaptateur Codex

Lire intégralement, dans cet ordre :

1. `docs/second-brain/news-refresh.md` — contrat canonique partagé.
2. `.claude/skills/cc-news/references/freshness-state.json` — checkpoint.
3. La seule référence de domaine utile sous
   `.claude/skills/cc-news/references/`.
4. `.claude/skills/cc-news/references/format-reponse.md` — rendu.

Utiliser les outils web et forge-brain disponibles dans la session Codex. Les
chercheurs délégués sont read-only ; la session principale est l'unique writer.
Une tâche planifiée reste toujours `proposal-only`. Une demande manuelle de news
peut corriger une assertion active existante selon le contrat, mais ne crée ni
ne supprime une note silencieusement.

Pour Claude Code, vérifier aussi la version publiée avec
`npm view @anthropic-ai/claude-code version`. Pour Codex et ChatGPT, utiliser
uniquement les pages officielles OpenAI pour les faits volatils.

Near misses : audit de qualité → `vault-audit`; paysage/pricing outils →
`veille-outils-ia`; question stable déjà documentée → `forge-brain`.
