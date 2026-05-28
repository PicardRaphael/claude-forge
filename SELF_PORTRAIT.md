# claude-forge — Self-Portrait

- **Auteur** : Raphaël Picard (raphael.picard@neoteem.fr) — consultant IA indépendant, Lead IA Neoteem
- **Dernière mise à jour** : 2026-05-28
- **Version** : 3.4 (CLAUDE.md condensé Workflow Git + Vault + Gotchas, 28 mai 2026)
- **État repo** : branche `main`, 361 commits, dernier `be30b99` (2026-05-28)
- **Statut** : stabilisé post bilan global 27-28 mai (oracle vault-first 3/3 CONFORME, audit lifecycle, architecture MEMORY tier-1/tier-2)

Document interne. Photographie technique fidèle pour reprise de contexte rapide (Raphaël, dispatcher futur). Pas un OVERVIEW destiné à Anthropic.

---

## 1. Chiffres bruts (mesurés 2026-05-28)

| Composant | Réel | Évolution depuis 27/05 |
|-----------|------|------------------------|
| Skills forge | **48** | +1 |
| Agents forge | **10** | -1 (fusion / consolidation) |
| Agents user-scope | **3** (boris-auditor, ecc-auditor, will-auditor) | stable |
| Hooks Python actifs | **12** (+1 inline `py_compile` dans python-dev) | stable |
| Rules | **9** | -1 vs brief (KILL color fait) |
| Tests baseline | **181 verts** (143 mcp-forge-brain + 38 hooks) | stable depuis ~100 commits |
| Notes vault | **453** | +23 vs 27/05 |
| MEMORY.md | **24,6k chars** | tier-1 visible post hierarchisation |
| `_index_archive.md` | **16,6k chars** | tier-2 archive |
| Plugins user-scope actifs | **3** (neoteem-brain-dev-ia, dev-admin, support-admin) | stable |
| Outils MCP forge-brain | **22** | stable |

---

## 2. Architecture technique

- **Stack** : Markdown (déclaratif) + Python ≥3.11 (hooks + MCP) + MCP FastMCP + SQLite-FTS5
- **Plateforme cible** : Windows (`py` launcher, `install.bat`). Code Python OS-agnostique sauf `mcp-autostart.py`
- **Path resolution 4 contextes** : skill = `git rev-parse`, hook = `__file__`, settings command = `${CLAUDE_PROJECT_DIR}`, .mcp.json = relatif cwd. Voir [[resolution-path-3-contextes]]
- **MCP forge-brain** : 22 outils — lecture (14, dont `search_brain` FTS5, `search_sessions` transcripts, `read_note`, `get_backlinks`), écriture (6, dont `create_note`, `append_note`, `update_property`), move/delete (2 atomiques + wikilinks auto). Auto-start SessionStart port 8091
- **Architecture MEMORY** : tier-1 visible `MEMORY.md` (24,6k, feedbacks cités) + tier-2 `_index_archive.md` (16,6k, valides non cités). Réintégration tier-1 dès citation
- **Mémoire portable** : `<repo>/memory/` versionné, chargé via `@memory/MEMORY.md` dans CLAUDE.md (relative path Anthropic). Symétrique multi-machines, zéro setup global
- **Doctrine vivante** : 3 verdicts INFO / REINFORCE / PIVOT avec gate humain. Voir [[doctrine-vivante]] + [[methode-pivoter-doctrine]]

---

## 3. Composants vivants

### Skills (48) — par catégorie

- **Référence CC** (user-invokable: false, chargées par parent) : cc-agents-ref, cc-skills-ref, cc-hooks-ref, cc-features-ref, cc-cowork-ref, cc-prompt-ref, python-ref
- **Outil-pur** (slash command exécution mécanique) : `/recap`, `/done`, `/expand`, `/spec`, `/notes`, `/forge-status`, `/install-forge`, `/self-check`, `/clean-memory`, `/pivot-check`
- **Exécution / création** : `/cc-advisor`, `/cc-news`, `/evolve`, `/skill-evolve`, `/craft-prompt`, `/watch`, `/x-read`, `/forge-review`, `/vault-audit`, `/reasoning-cache`, `/python-script-refactor-masse`, `/analyze-project`
- **Audit / jugement** : `/agentshield-like-scanner`, `/audit-thematique-clusters`, `/auditor-empirical-verify`, `/outcomes-test`, `/config-guardian`, `/da-blocking-arbitrage`, `/doctrine-impact-check`, `/methode-pivoter-doctrine`, `/web-search-canonical-source`, `/arxiv-verification`, `/cross-repo-propagation`
- **Support** (auto-trigger) : forge-brain, mcp-brief-then-direct, defuddle, configure-claude-desktop, windows-hooks-cross-machine, json-canvas, obsidian-markdown, obsidian-bases, git-multi-repo

### Agents (10 forge + 3 user-scope)

| Agent | Rôle 1-ligne |
|-------|--------------|
| agent-creator | Créer/modifier subagents via 10 questions + checklist 9 points |
| claudemd-optimizer | Rédiger/optimiser CLAUDE.md vers ~200L, supprimer filler |
| devils-advocate | Critique adversariale livrables majeurs, verdicts BLOCKING/WARNING/NITPICK |
| hook-creator | Créer hooks doctrine 22 mai (lint/security/scope uniquement) |
| outcomes-grader | Notation RUBRIC.md, PASS/FAIL/PARTIAL (MUST gate + SHOULD 65% + NICE 35%) |
| python-dev | Implémenter Python en TDD strict, hook inline `py_compile` |
| repo-inspector | Auditer/analyser/scanner repo en 3 modes (effort xhigh) |
| responsable-ia | Assister actes Lead IA Neoteem (CODIR/6-pager, RICE, AI Act, Loji) |
| self-updater | Détecter nouvelles features CC via cc-news, MAJ skills `cc-*-ref` |
| skill-creator | Créer/optimiser skills (9 questions + checklist 10 points) |
| boris-auditor (user) | Audit lentille Boris Cherny — score 7/7 conformité workflow |
| ecc-auditor (user) | Audit lentille ECC (Affaan Mustafa) — comparaison références |
| will-auditor (user) | Audit lentille Will (Anthropic Applied AI) — FUSION/DELETE/REPLACE |

### Hooks Python actifs (12)

- `security-guard.py` — PreToolUse Bash/PowerShell, bloque rm -rf, push --force, reset --hard
- `delegate-guard.py` — PreToolUse Write/Edit, bloque édit direct SKILL/agent/CLAUDE.md (force spécialiste)
- `meta-commentary-detector.py` — PreToolUse Write/Edit, bloque 11 patterns méta-commentaire
- `vault-cat-guard.py` — PreToolUse Bash, force MCP forge-brain pour vault
- `mcp-alias-guard.py` — bloque alias court ambigu MCP append_note
- `memory-size-watcher.py` — surveille croissance MEMORY.md
- `session-reminder.py` — SessionStart, nettoie markers + affiche extrait MEMORY.md (résolution `__file__`)
- `mcp-autostart.py` — SessionStart async, démarre MCP forge-brain port 8091
- `session-health.py` — UserPromptSubmit, compteur tours + tips `/recap` `/compact`
- `skill-activation.py` — UserPromptSubmit, matche prompt vs `.skill-triggers.json`
- `learning-reminder.py` — Stop (`once:true`), 1×/session rappel capitalisation
- `proactivity-reminder.py` — Stop (`once:true`), 1×/session rappel proposition Jarvis

Plus 1 hook inline `py_compile` dans frontmatter `python-dev`.

### Rules (9)

`changelog-vault.md`, `check-before-create.md`, `comportement-proactif.md` (dispatch agents), `delegate-to-specialists.md`, `devils-advocate-pipeline.md` (conditionnel ciblé), `forge-brain-proactive.md` (MCP), `memory-discipline.md` (frontière mémoire/vault), `sequence-canonique-modification.md` (A→B→C→D→E), `vault-consultation-protocol.md`.

---

## 4. Doctrine en vigueur

Notes canoniques (lecture EXCLUSIVEMENT via MCP forge-brain, jamais Grep/Read brut) :

- [[doctrine-vivante]] — verdicts INFO/REINFORCE/PIVOT avec gate humain
- [[pattern-maintenance-hybride-corpus-accumulatif]] — maintenance tier-1/tier-2
- [[pattern-mcp-brief-then-direct]] — workaround MCP décoratif sub-agent
- [[mcp-vs-skills-doctrine]] — MCP data / Skills how-to / Bash exploration
- [[3-axes-strategiques-forge]] — innovation revendiquée
- [[methode-pivoter-doctrine]] — checklist 5 étapes anti-drift résiduel
- [[sequence-canonique-modification]] — A→B→C→D→E (analyser réel → canoniques entiers → croiser → plan → exécuter)
- [[raisonnement-22mai-doctrine-vs-enforcement]] — pivot hooks lint/security uniquement (PAS workflow)
- [[methode-analyser-repo]] — META 6 étapes audit repo + propose config CC
- [[comment-creer-skill]] · [[comment-creer-agent]] · [[comment-creer-hook]] · [[comment-ecrire-claudemd]]

---

## 5. Edge mondial revendiqué (3 axes)

1. **Diagnostic MCP décoratif sub-agent** — frontmatter MCP/skills ignoré en Agent Teams teammates. Workaround `pattern-mcp-brief-then-direct` (brief inline + ESCALADE) + enforcement `vault-cat-guard.py` (force MCP forge-brain pour accès vault)
2. **Critère architectural Agent vs Skill basé densité écriture MCP vault** — pas le verbe ni le scope mais le ratio écritures MCP vault / total ops. Voir [[densite-mcp-write-vs-filesystem]]
3. **Living doctrine pattern avec gate humain typé INFO/REINFORCE/PIVOT** — découverte web → confrontation canonique vault → verdict typé → gate humain avant pivot. Évite drift silencieux (cf [[doctrine-drift-silent-regression]])

---

## 6. Validations empiriques récentes

- **27-28 mai** : oracle vault-first 3/3 CONFORME (audit lifecycle auto-applique séquence canonique A→B→C→D→E sur lui-même)
- **Audit lifecycle complet** : 3 KILL + 2 AMEND + capitalisations (commit `e81e4aa`)
- **Architecture MEMORY.md tier-1/tier-2** : livrée + canonisée [[pattern-maintenance-hybride-corpus-accumulatif]] (commit `7d82034`)
- **Tests baseline 181 verts** : maintenue depuis ~100+ commits
- **MCP forge-brain port 8091** : auto-start fiable, eager boot session_messages 2,68s
- **~14k tokens contexte libérés** : purge hierarchisation MEMORY + nettoyage settings.local.json (48 → 11 entrées allow)

---

## 7. Dettes structurelles tracées

- **`comment-creer-rule` absente du vault** (P2) — canonique manquante pour le 4e type de composant CC
- **Push GitHub bloqué orga Team** — sauvegarde externalisée à arranger ([[org-blocks-github]])
- **Hook UserPromptSubmit "audit→lecture canoniques"** candidat — déclencheur 2e occurrence audit-à-l'œil (cf [[feedback_lire_canoniques_avant_audit]])
- **Évaluations LLM-as-judge absentes** — gap stratégique #1 vs setups concurrents (Boris/ECC/Will)
- **Tests pytest skill `/clean-memory`** à ajouter — pas de couverture sur ce nouvel outil

---

## 8. Engagement Anthropic

- **Cible #1 DM** : Boris Cherny (créateur Claude Code) — référencer bug GitHub #60237
- **Pré-requis** : 1-2 semaines usage mesuré avec architecture finalisée 27-28 mai
- **Rappel calendrier** : retour empirique advisor prévu 2026-06-10
- **Repo public/privé** : à décider avant DM — argumentaire à constituer (inclut ou non `vault/` ? `memory/` ?)

---

## Méthodologie

Métriques mesurées empiriquement ce soir : `git rev-list --count` (361 commits), `ls .claude/skills | wc -l` (48), `python -m pytest --collect-only` (181 tests), `find vault -name "*.md" | wc -l` (453), `wc -c memory/*.md` (24,6k + 16,6k), lecture directe `settings.json` (12 hooks Python + 1 inline). Wikilinks vault résolvables via MCP forge-brain `read_note`.
