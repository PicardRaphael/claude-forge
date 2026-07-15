---
titre: "Loop d'apprentissage Codex — compounding via mémoire auto, skills et scheduled tasks"
resume: "Note canonique forge — le cycle d'amélioration continue de Codex : mémoire auto [memories] (background, redaction secrets), Skills capitalisées, et scheduled task documentée verbatim 'scan sessions → update skills'. Le 'summarize→memory' n'est PAS un event de hook. Vérifié doc officielle au 15 juil. 2026."
aliases:
  - "loop apprentissage codex"
  - "compounding codex"
  - "codex memories"
  - "[memories] config codex"
  - "scan sessions update skills"
  - "amelioration continue codex"
  - "codex auto memory"
derniere-maj: 2026-07-15
auteur: claude
type: technique
sources:
  - "https://learn.chatgpt.com/docs/customization/memories"
  - "https://learn.chatgpt.com/docs/config-file/config-reference ([memories])"
  - "https://learn.chatgpt.com/docs/automations · /docs/hooks"
tags:
  - "#type/technique"
  - "#domaine/codex"
  - "#domaine/workflow"
  - "#doctrine/2026"
---
# Loop d'apprentissage Codex — le compounding

> Note canonique forge — comment Codex capitalise ses erreurs/résultats pour s'améliorer (le « compounding » de Boris, version Codex). Trois briques natives se combinent ; le point clé est qu'**il n'y a PAS de hook « auto-memory » officiel** — la mémoire auto passe par un mécanisme dédié. Vérifié au **15 juil. 2026**.

---

## Les 3 briques du compounding Codex

### Brique 1 — Mémoire auto `[memories]` (CERTAIN)

Codex génère et injecte une mémoire persistante en arrière-plan (`~/.codex/memories/` : summaries, durable entries, recent inputs, supporting evidence). Verbatim : les mémoires « carry useful context from earlier work into future work » ; « helpful recall layer, not the only source for rules that must always apply » ; « Updates memories in the background instead of immediately at the end of every task » ; « Skips active or short-lived sessions » ; « Redacts secrets from generated memory fields ».

Config `[memories]` :
```toml
[memories]
generate_memories = true               # false → threads non stockés comme inputs
use_memories = true                    # false → pas d'injection des mémoires existantes
disable_on_external_context = false    # true → threads avec MCP/web/tool search exclus
min_rate_limit_remaining_percent = 25
max_raw_memories_for_consolidation = 256   # cap 4096
max_rollout_age_days = 30               # 0–90
min_rollout_idle_hours = 6              # 1–48
```
Contrôles : Settings > Personalization (global) ; commande `/memories` (par tâche).

### Brique 2 — Skills capitalisées

Les Skills sont le vecteur « best practice réutilisable » (l'équipe Codex en a **100+** internes, cf Pragmatic Engineer). Création : « Build me a skill… » ou **Record & Replay** (macOS) qui transforme une démo en skill. Détail : [[comment-creer-skill-codex]].

### Brique 3 — Scheduled task « scan sessions → update skills » (CERTAIN, verbatim)

L'exemple officiel documente **littéralement** le loop de compounding :

> Verbatim (doc automations) : « Scan all of the `~/.codex/sessions` files from the past day and if there have been any issues using particular skills, update the skills. »

C'est une automation planifiée (cf [[loops-codex]]) qui lit l'historique des sessions, détecte les frictions sur les skills, et **met à jour les skills** — le compounding error-driven de Boris, en routine native.

---

## Le cycle complet

```
Sessions Codex (~/.codex/sessions)
   │
   ├── [memories] consolide en arrière-plan → contexte réinjecté (recall layer)
   │
   └── scheduled task quotidienne : scan sessions → repère frictions skills → update skills
                                                                    │
                                                        Skills améliorées (Brique 2)
                                                                    │
                                            AGENTS.md mis à jour manuellement (ou par une autre scheduled task)
```

- **`[memories]`** = mémoire courte/contextuelle (recall), auto, jamais « la règle qui doit toujours s'appliquer ».
- **Skills + AGENTS.md** = les règles durables. AGENTS.md **ne se met PAS à jour tout seul** (cf [[agents-md-codex]]) — c'est une scheduled task ou une action manuelle.

---

## CORRECTION — « summarize→memory » n'est PAS un event de hook

Le cas d'usage « summarize conversations to create persistent memories » est listé dans la doc hooks, mais **aucun event dédié n'existe** (verbatim : « no dedicated hook event exists for this purpose »). Pour le câbler soi-même : hook `Stop` ou `PostCompact` (lire `transcript_path`, écrire un résumé) → réinjection via `SessionStart`. La mémoire auto « clé en main », elle, passe par `[memories]` — pas par un hook. Cf [[comment-creer-hook-codex]].

---

## Miroir forge / Claude Code

Ce loop est l'équivalent Codex de la doctrine forge « compounding CLAUDE.md » + des skills `skill-evolve` / `align-vault-skills` (qui font, côté forge, exactement ce que fait la scheduled task Codex : détecter les frictions et améliorer les skills). Différence : Codex a la mémoire auto `[memories]` **native** là où forge le fait manuellement (via `/done`, MEMORY.md, vault). C'est une des cross-pollinations du chantier (cf note maître, décisions applicables).

---

## ANTI-PATTERNS

- ❌ **Chercher un hook « auto-memory » officiel** — n'existe pas ; utiliser `[memories]` ou câbler Stop/PostCompact.
- ❌ **Traiter `[memories]` comme la source des règles dures** — c'est un recall layer, pas AGENTS.md/skills.
- ❌ **Attendre qu'AGENTS.md se mette à jour seul** — manuel ou scheduled task.
- ❌ **Laisser `[memories]` capturer des sessions à secrets sans vérifier la redaction** — activée par défaut, mais `disable_on_external_context` pour les threads sensibles (MCP/web).

---

## SOURCES

- `learn.chatgpt.com/docs/customization/memories` + `/docs/config-file/config-reference` (`[memories]`, CERTAIN).
- `learn.chatgpt.com/docs/automations` — exemple verbatim « scan sessions → update skills ».
- `learn.chatgpt.com/docs/hooks` — « no dedicated hook event » pour la mémoire.
- Pragmatic Engineer — 100+ skills internes équipe Codex.

---

## WIKILINKS

- [[workflow-codex-optimal]] — note maître (compounding niveau expert)
- [[loops-codex]] — la scheduled task comme loop
- [[comment-creer-skill-codex]] — Skills capitalisées
- [[agents-md-codex]] — pourquoi AGENTS.md ne se met pas à jour seul
- [[comment-creer-hook-codex]] — câbler summarize→memory à la main
- [[pre-compute-vs-inference-loops-boris]] — compounding error-driven (doctrine forge)
- [[concevoir-loops-travail]] — méthode loop universelle
