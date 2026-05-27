---
titre: "Phase 4 — Comparaison Hermes Agent vs claude-forge"
resume: "Audit code source Hermes Agent (Nous Research, 169k stars) vs claude-forge, filtré par le critère use case synchrone (mémoire/apprentissage parfaits, pas agent autonome). Matrice + plan d'action 3 catégories."
aliases:
  - "phase 4 hermes"
  - "comparaison hermes claude-forge"
  - "hermes agent audit"
  - "hermes vs forge"
  - "roadmap phase 4"
derniere-maj: 2026-05-27
tags:
  - "#type/synthese"
  - "#projet/claude-forge"
  - "#concurrent/hermes"
---
# Phase 4 — Comparaison Hermes Agent vs claude-forge

Lien : [[methode-analyser-repo]], [[workflow-claude-code-optimal]], [[comment-creer-skill]]

## Statut d'implémentation

- **A3 — Capitalisation proactive à /done** : FAIT (2026-05-27). Skill `done` enrichie via skill-creator. 5 triggers de la spec mappés sur 3 types de blocs (feedback mémoire / note vault / ADR). Gate de validation `[v]/[m]/[i]` par item, aucune écriture sans validation. Pas de tests unitaires (skill de jugement LLM, validation = exécution réelle). Capitalisé : [[capitalisation-proposee-pas-auto]] (feedback mémoire), amendement [[comment-creer-skill]].
- **A1 — Recherche transcripts session** : à faire (P1).
- **A2 — Lifecycle / usage tracking skills** : à faire (P2).

## Contexte et critère de pertinence

Comparaison sur **code source réel** (repos clonés, chemins+lignes), pas articles SEO.
Source Hermes : `C:\temp\hermes-audit\HERMES_ARCHITECTURE.md`.

**Critère de pertinence appliqué** : le use case de claude-forge n'est PAS l'agent autonome. C'est la **mémoire et l'apprentissage parfaits en session synchrone** (compounding maximal, une erreur jamais deux fois, décisions tracées et réutilisées). Les axes async (cron, multi-canal, webhook) sont secondaires : Hermes peut y briller, ça ne change pas le verdict.

## Données vérifiées

| | Hermes Agent | claude-forge |
|---|---|---|
| Stars | 169 296 (gh api 2026-05-27) | projet perso, 1 auteur |
| Licence | MIT | privé |
| Stack | Python 3.11+, OpenAI SDK | Claude Code + MCP FastMCP/SQLite-FTS5 |
| Mémoire | MEMORY.md/USER.md plats (2200/1375 chars) + holographic SQLite optionnel | vault 417 notes, 2717 wikilinks, 2462 aliases + MEMORY.md auto + .claude/ |
| Skills | 25 bundled + 17 optional | 47 skills |
| Tests | `tests/` non audité | 207 verts (101 hooks + 106 MCP), 0 régression |
| Use case | Agent autonome multi-canal | Session synchrone, compounding |

## Matrice comparative — axes prioritaires en haut

Vainqueur honnête. Colonne "Pertinent" = pour le use case synchrone de claude-forge.

### Axes PRIORITAIRES (mémoire / apprentissage / compounding / conformité)

| Axe | Hermes | claude-forge | Vainqueur | Pertinent | Action |
|-----|--------|--------------|-----------|-----------|--------|
| **Mémoire session** | session_search indexe et cherche les transcripts passés (outil dédié) | Pas de recherche transcripts bruts en natif ; capitalisation manuelle vers vault | **Hermes** | OUI | A — combler (recherche transcripts) |
| **Mémoire projet** | subdirectory_hints lit CLAUDE.md/AGENTS.md statiques par sous-dir | CLAUDE.md + rules + vault 1-Projets/ + hooks scoped per-repo (mémoire projet apprenante + enforcée) | **claude-forge** | OUI | C — avantage acquis |
| **Mémoire cross-projet / doctrine** | MEMORY.md global plat 2200 chars, pas de structure | vault 417 notes, 3 layers, 2717 wikilinks, MCP FTS5 BM25, ontologie 07 dossiers | **claude-forge** (net) | OUI | C — avantage acquis majeur |
| **Recherche mémoire** | holographic FTS5+Jaccard+HRR (réel mais SNR dégrade >256 faits/cat, optionnel) ; builtin = aucune | MCP search_brain FTS5 BM25 (file_stem:10/aliases:8/content:1), navigation active, 4 stratégies | **claude-forge** | OUI | C — avantage acquis |
| **Écriture mémoire (qui décide)** | background review fork LLM auto toutes 10 itérations, écrit SANS validation, notif après coup | learning-reminder nudge advisory + Raphael décide et capitalise (humain valide before write) | **Égalité doctrinale** (couverture vs contrôle) | OUI | A — combler couverture, garder contrôle |
| **Capitalisation patterns décisionnels** | prompt cible "When X do Y rules" mais NL libre dans SKILL.md, pas de pourquoi, risque sur-généralisation | feedback_* files + Knowledge/raisonnements/ + reasoning-cache (règle + pourquoi + déclencheur) | **claude-forge** | OUI | C — avantage acquis |
| **Conformité par construction** | AUCUN delegate-guard. skills_guard = install externe only. file_safety = "NOT a security boundary" | delegate-guard.py BLOQUE exit 2 l'édition directe, meta-commentary-detector, security-guard, 207 tests | **claude-forge** (net) | OUI | C — avantage acquis majeur |
| **Doctrine versionnée datée** | AGENTS.md politiques datées narratives, pas de version/date structurée, pas de changelog doctrine | CLAUDE.md v3.3 datée + [[methode-pivoter-doctrine]] + CHANGELOG + pivot-check anti-drift | **claude-forge** | OUI | C — avantage acquis |
| **Self-improvement réel** | GEPA = mutation texte prompts/skills (pas fine-tuning), POC Phase 1/5, manuel, humain valide PR, hors runtime | Pas d'optim auto de prompts ; évolution skills via skill-evolve manuel + advisor/DA | **Hermes** (sur l'ambition tech) | PARTIEL | B — décliner (POC, hors runtime, ROI incertain) |
| **Lifecycle skills (usage/curation)** | .usage.json (use/view/patch counts) + curator stale→archive→prune + provenance created_by | Pas de tracking d'usage skills, pas de curation auto, orphelines détectées à la main | **Hermes** | OUI | A — combler (lifecycle skills) |
| **Détection contradictions mémoire** | holographic `contradict` (faits divergents, entités communes) | lint_vault (5 catégories qualité) mais pas de check contradiction sémantique | **Hermes** | OUI (léger) | A — combler (extension lint) |
| **Honnêteté méthodo (bugs/dette)** | pas de trace publique bugs caractérisés ; 14k open issues | 2 bugs caractérisés ET fixés Phase 2, dette tracée avec déclencheurs, ratio adverse ≥3:1 | **claude-forge** | OUI | C — avantage acquis |
| **Provenance / citation source** | builtin pas d'ID ; holographic fact_id entier ; pas de fichier:ligne | vault wikilinks + chemins + git history ; agents citent file:line | **claude-forge** | OUI | C — avantage acquis |
| **Audit trail capitalisation** | overwrite atomique, pas d'historique git de ~/.hermes/skills/ | tout versionné git + CHANGELOG vault + log.md append-only | **claude-forge** | OUI | C — avantage acquis |

### Axes INTERMÉDIAIRES

| Axe | Hermes | claude-forge | Vainqueur | Pertinent | Action |
|-----|--------|--------------|-----------|-----------|--------|
| Skills portables | agentskills.io standard, Skills Hub GitHub/URL, bundles | skills locales, pas de hub/registry public | **Hermes** | PARTIEL | B — décliner (mono-utilisateur) |
| Skills auto-créées | background review crée auto | skill-creator délégué, humain valide | Égalité (couverture vs contrôle) | OUI | déjà couvert axe écriture |
| Hooks lifecycle | shell_hooks basiques, pas de doctrine | 9 hooks, 29 events doc, doctrine 22 mai lint/secu/scope | **claude-forge** (net) | OUI | C — avantage acquis |
| Multi-agent / sous-agents | delegate_task + background fork | 11 agents spécialisés + Agent Teams + séquence canonique | **claude-forge** | OUI | C — avantage acquis |
| Trigger CLI synchrone | hermes TUI React/Ink | claude (Claude Code natif) | Égalité | OUI | acquis |
| MCP support | serveur+clients, ACP | MCP forge-brain custom 21 outils FastMCP/FTS5 | **claude-forge** (custom métier) | OUI | C — avantage acquis |
| Stratégie modèle par tâche | un modèle principal, no lock-in | Sonnet exécution / Opus jugement / Haiku scan, effort calibré | **claude-forge** | OUI | C — avantage acquis |
| Sécurité supply-chain | exact-pin + lazy-install (réel) | pas de gestion deps comparable (peu de deps) | **Hermes** | NON | B — décliner (surface différente) |
| Tests adverses composants critiques | présence non auditée | ratio ≥3:1 adverse/happy sur hooks sécu | **claude-forge** (prouvé) | OUI | C — avantage acquis |

### Axes SECONDAIRES (évalués, pas de pression de combler)

| Axe | Hermes | claude-forge | Vainqueur | Pertinent | Action |
|-----|--------|--------------|-----------|-----------|--------|
| Trigger cron / planifié | cron/scheduler.py intégré | /schedule cloud (pas d'accès local) | **Hermes** | NON | B — décliner |
| Trigger chat (Telegram/Slack) | gateway 6 canaux | aucun | **Hermes** | NON | B — décliner |
| Trigger webhook | via gateway | aucun | **Hermes** | NON | B — décliner |
| Coût d'inférence | background review = surcoût récurrent (16 iters/10) | capitalisation manuelle = coût nul hors session | **claude-forge** | NON | C — bénéfice latéral |
| Communauté / écosystème | 169k stars, 28k forks | 1 auteur perso | **Hermes** (massif) | NON | B — décliner |
| Portabilité OS | Linux/macOS/WSL2/Windows beta | Windows-first | **Hermes** | NON | B — décliner |
| Onboarding tiers | install.sh, docs site | privé, non packagé | **Hermes** | NON | B — décliner |

## Verdict sur les axes prioritaires

claude-forge gagne 8 axes prioritaires, Hermes 3 (mémoire session/session_search, lifecycle skills, détection contradictions), 1 égalité doctrinale (écriture mémoire), 1 Hermes ambition tech mais décliné (self-improvement GEPA).

**Sur la mémoire structurée, la conformité par construction, la doctrine versionnée, la traçabilité et la capitalisation décisionnelle — claude-forge est strictement supérieur.** Hermes mise sur l'automatisation (capitalisation auto sans validation, lifecycle skills auto) cohérente avec son use case autonome ; claude-forge mise sur le contrôle, la traçabilité et la structure cohérents avec le use case synchrone.

Le seul vrai gap pertinent et net : **recherche dans les transcripts de sessions passées** (session_search). claude-forge capitalise vers le vault, mais ne peut pas chercher "qu'est-ce qu'on a dit la semaine dernière sur X" dans l'historique brut.

## Plan d'action — 3 catégories

### A. Gaps à combler (Hermes meilleur ET pertinent)

Asymétrie non confirmée : les données mettent 3 gaps réels sur les axes prioritaires.
Section conçue pour être implémentable en session dédiée `/clear` sans recharger ce contexte.

**Ordre d'implémentation recommandé** : A3 (P1, autonome, haut ROI) → A1 (P1, plus lourd) → A2 (P2). Pas de dépendance bloquante entre les trois. Note de synergie : A3 (capitaliser à /done) et A1 (chercher les transcripts) se renforcent — A1 sert mieux A3 si l'historique brut est cherchable, mais A3 fonctionne sans A1. Faire A3 d'abord (valeur immédiate), A1 ensuite.

---

**A3 — Capitalisation proactive à /done (croisement Jarvis) (P1, ~2h)**

- Gap : le background review Hermes rattrape ce que l'agent oublie de capitaliser. `learning-reminder` rappelle mais ne PROPOSE pas de contenu concret. `done` fait de la métacognition mais ne génère pas de diff prêt-à-valider.
- Croisement X+Y=Z : importer la COUVERTURE de Hermes (proposer des capitalisations) en gardant le CONTRÔLE forge (Raphael valide, diff visible, ADR si décision).
- **Chemin du composant** : modifier `.claude/skills/done/SKILL.md` (303L, SKILL.md seul, pas de scripts/ ni references/ actuellement). Pas de nouveau dossier.
- **Créateur** : skill-creator (délégation obligatoire — delegate-guard bloque l'édit direct de SKILL.md). Séquence A→B→C→D→E : lire done/SKILL.md EN ENTIER + canoniques `comment-creer-skill` + `mcp-vs-skills-doctrine` via MCP read_note.
- **Skeleton attendu** :
  - Triggers de proposition (3) : (a) fin de session `/done`, (b) erreur comportementale détectée dans la session (workflow, oubli), (c) décision majeure prise (arbitrage, pivot).
  - Format de proposition : pour chaque apprentissage détecté, produire un BLOC CONCRET prêt-à-écrire :
    - feedback mémoire → bloc `name: / description: / metadata.type / corps **Why:** **How to apply:**` (format MEMORY.md)
    - note vault → bloc frontmatter + body Obsidian (via skill obsidian-markdown)
    - décision → bloc ADR (statut/contexte/décision/déclencheur de réactivation)
  - UX : présenter chaque bloc avec son chemin cible, puis demander à Raphael par item — `[v]alider / [m]odifier / [i]gnorer`. Validé → écrire (mémoire via Write, vault via MCP forge-brain). Pas d'écriture sans validation (principe humain dans la boucle, cf [[adr-gaps-hermes-declines-phase-4]] §2).
  - Différence clé vs Hermes : la proposition est un diff que Raphael relit, pas un overwrite silencieux.
- **Tests** : `done` n'a aucun test actuellement (skill procédurale). Pas de test unitaire pertinent (la skill orchestre du jugement LLM). Validation = exécuter `/done` en conditions réelles sur une session ayant produit ≥1 apprentissage, vérifier que les blocs proposés sont corrects et que rien n'est écrit sans validation.
- **Capitalisation post-implémentation** : amender [[comment-creer-skill]] (pattern "skill qui propose un diff à valider"). Feedback mémoire `feedback_capitalisation_proposee_pas_auto` (règle : proposer le diff, jamais auto-écrire). Mettre à jour [[workflow-claude-code-optimal]] (cycle de capitalisation).

---

**A1 — Recherche transcripts session (P1, ~3-5h)**

- Gap : `session_search` Hermes (`tools/session_search_tool.py:378`) cherche l'historique conversationnel brut. claude-forge n'a que le vault capitalisé — impossible de retrouver "qu'a-t-on dit la semaine dernière sur X" si non capitalisé.
- Nuance : l'auto-memory harness conserve déjà MEMORY.md ; le vault couvre ~80% du besoin de compounding. Le manque = recherche fulltext de l'historique brut non capitalisé.
- **Choix recommandé : extension MCP forge-brain** (pas une skill) — l'indexation FTS5 des transcripts est un travail de données, cohérent avec la doctrine mcp-vs-skills (MCP = data, skill = how-to).
- **Chemin du composant** : nouvel outil dans le serveur MCP forge-brain (`mcp-forge-brain/`, vérifier le fichier serveur exact — server.py ou équivalent). Nouvel outil `search_sessions(query, limit, project)`.
- **Source de données** : transcripts Claude Code dans `~/.claude/projects/<repo-encoded>/*.jsonl` (format JSONL, un message par ligne). Pour ce repo : `C:\Users\raphael.picard_neote\.claude\projects\C--Users-raphael-picard-neote-Documents-claude-forge\`.
- **Indexation** : table SQLite FTS5 séparée de l'index vault (les transcripts sont volumineux et éphémères vs notes durables). Indexer le texte utilisateur + assistant, garder session_id + timestamp + projet. Réindexation incrémentale (mtime des .jsonl).
- **Sortie attendue** : extraits avec session_id + date + projet, citables ("session du 2026-05-20, projet ia_back").
- **Créateur** : python-dev (code MCP) après séquence A→B→C→D→E. Pas un créateur de composant `.claude/`.
- **Tests** : OUI, indispensable (cœur MCP, ratio adverse attendu). Ajouter `mcp-forge-brain/tests/test_search_sessions.py` — couvrir : indexation JSONL malformé, requête vide, projet inexistant, FTS5 escaping, incrémental sur mtime. Aligner sur les suites MCP existantes (test_search.py, test_indexer.py).
- **Capitalisation post-implémentation** : note vault sur l'architecture (`mcp-vault-llm-design` ou nouvelle note `01-Claude/Code/`). Mettre à jour la doc des 21→22 outils MCP (CLAUDE.md + forge-brain-proactive.md + skill forge-brain).

---

**A2 — Lifecycle / usage tracking des skills (P2, ~2-3h)**

- Gap : Hermes track `use_count`/`last_used` (`.usage.json`) et archive les skills stale (curator). claude-forge a 47 skills, orphelines détectées à la main.
- Décision de doctrine : PAS de curation AUTO (garder le contrôle humain — cohérent use case synchrone). Outil d'AUDIT qui propose, Raphael décide.
- **Chemin du composant** : nouvelle skill `.claude/skills/skills-lifecycle/` (dossier à créer, SKILL.md + éventuellement scripts/audit.py).
- **Sources de données** (pas de tracking runtime — reconstruire depuis l'existant) :
  - Dernière modif d'une skill : `git log -1 --format=%ci -- .claude/skills/<nom>/`
  - Skill référencée dans un agent : `grep -rl "<nom-skill>" .claude/agents/` (frontmatter skills: + body)
  - Skill user-invokable vs référence : lire `user-invokable` dans le frontmatter
  - Orpheline = ni référencée dans un agent, ni user-invokable, ni modifiée depuis N mois
- **Format de sortie** : table Markdown (skill / dernière modif / référencée par / statut proposé : KEEP/REVIEW/ARCHIVE-candidate) + recommandations. Pas d'action automatique.
- **Créateur** : skill-creator (séquence A→B→C→D→E).
- **Tests** : si scripts/audit.py existe, test léger sur la détection d'orpheline (skill factice non référencée). Sinon validation manuelle.
- **Capitalisation post-implémentation** : feedback mémoire si un pattern de détection d'orpheline émerge. Note vault optionnelle.

### B. Gaps à décliner explicitement (Hermes meilleur, pas pertinent)

Voir ADR consolidée [[adr-gaps-hermes-declines-phase-4]] (`Knowledge/raisonnements/`) — chaque gap a son déclencheur de réactivation :
- **Triggers async** (cron, chat 6 canaux, webhook) — use case autonome, pas synchrone.
- **Background review autonome sans validation** — viole le principe "Raphael tranche", incompatible use case synchrone.
- **Self-evolution GEPA** — POC Phase 1/5, hors runtime, ROI incertain pour 1 utilisateur ; mutation auto de prompts sans humain = anti-doctrine forge.
- **Skills Hub / registry public** — mono-utilisateur, pas de besoin de distribution.
- **Sécurité supply-chain exact-pin** — surface de deps différente (peu de deps Python forge).
- **Communauté / portabilité OS / onboarding tiers** — projet perso Windows-first assumé.

### C. Avantages déjà acquis (claude-forge meilleur)

Sur les axes prioritaires, à capitaliser pour comm externe (LinkedIn, Anthropic Partner Network) :
- **Mémoire cross-projet structurée** : vault 417 notes / 2717 wikilinks / FTS5 BM25 vs MEMORY.md plat 2200 chars. Selling point fort.
- **Conformité par construction** : delegate-guard bloquant (exit 2) — Hermes a zéro équivalent. Selling point fort.
- **Doctrine versionnée + anti-drift** : v3.3 datée + methode-pivoter-doctrine + pivot-check. Unique.
- **Capitalisation décisionnelle tracée** : règle + pourquoi + déclencheur, versionné git. Hermes capitalise sans pourquoi ni historique.
- **Honnêteté méthodo** : bugs caractérisés+fixés, dette tracée, ratio adverse ≥3:1, 207 tests. Preuve de rigueur.
- **Humain dans la boucle by design** : Raphael valide avant écriture. Cohérent use case synchrone, supérieur en contrôle/correctibilité.

## Première action

A3 (capitalisation proactive à /done) — haut ROI compounding, cœur du use case, 2h, via skill-creator.

## Déclencheurs de réactivation des gaps déclinés

- Si claude-forge devient multi-utilisateur → réévaluer Skills Hub + onboarding.
- Si Raphael adopte un workflow asynchrone (laisser tourner la nuit) → réévaluer triggers async + background review.
- Si le nombre de skills dépasse ~80 → réévaluer lifecycle/curation auto.
- Si GEPA devient packagé stable et intégrable runtime → réévaluer self-evolution.

## Proposition Jarvis — compounding rétroactif

Croisement A1 × A3 : à `/done`, chercher dans les transcripts passés (A1) les apprentissages jamais capitalisés et les proposer à validation (A3). Rattraper le passé non capitalisé — capacité qu'aucun agent (Hermes ni forge) n'a. Détail : [[idee-compounding-retroactif]].
