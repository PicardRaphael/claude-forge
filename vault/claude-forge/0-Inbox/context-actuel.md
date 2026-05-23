---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-23 : 4 audits thématiques vault complétés en parallèle (02 prompt-eng, 03 RAG, 04 agents-IA, 06 patterns/context/stacks). Reste 05 fine-tuning + 07 leaders + 08 dogfooding."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Audits thématiques vault forge en cours (méthode A→B→C→D→E + propagation F) — **4/7 thèmes complétés** : 02 prompt-eng ✅, 03 RAG ✅, 04 agents-IA ✅, 06 patterns/context/stacks ✅. Reste : 05 fine-tuning, 07 leaders-modèles-industrie, 08 forge dogfooding.

## Dernière session (2026-05-23 — audit thème 06 patterns/context/stacks)

### Décisions prises
- Méthode validée 23 mai (sub-agents par cluster + checkpoint A + self-verify FAUX fort impact + Type 1/2/3) appliquée intégralement sur thème 06
- 6 sub-agents parallèles par cluster thématique (Karpathy/Anthropic/Spec-driven/Forge-custom/Stacks/Figma) + 5+ self-verify WebFetch direct
- Carte blanche Raphael honorée — exécution direct du plan jusqu'au commit/push sans re-valider note par note
- Empty commit `70bd497` de traçabilité créé après détection HEREDOC Windows échoué

### Corrections appliquées (28 sur ~92 claims, 21 notes)
- **Type 3 (4 réécritures)** : LLM Wiki, Context Engineering, Context Management, pattern-sdd-triangle
- **Type 2 (16 chirurgicales)** : Spec Kit 105K stars / 7 fichiers / 40+ ext, BMAD 21 agents, S*=0.509 retiré, Modal cold start corrigé, Figma 8 skills (3 noms inventés corrigés), 70x RAG non attestable, 400K mots non attesté, sweet spot 150-300 mots retiré, /compact 40-60% (pas 70%)
- **Type 1 (8 attributions)** : 3 niveaux SDD = Böckeler (pas Breunig/Park), 4 piliers context-eng = communauté (pas Karpathy), Document & Clear = Manus AI (pas Boris), Anti-pattern #1 Karpathy = lecture forge, date Thariq RIN 19 mai (pas 18), GSD = Lex Christopherson/TACHES, ponctuation `;` verbatim Karpathy
- **Propagation F** : Andrej Karpathy.md, context-management.md, project-analyzer.md, cc-features-ref/SKILL.md

### Fondations canoniques confirmées (WebFetch direct)
- ✅ Verbatim Karpathy "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase" — gist 442a6bf, 4 avril 2026
- ✅ Verbatim Anthropic blog 15 mai 2026 codebase-maps
- ✅ Verbatim Thariq RIN 4 sections (19 mai)
- ✅ Leak Claude Code 31 mars 2026 / 512K lignes / 1900 TS files
- ✅ Drew Breunig Plumb (`github.com/dbreunig/plumb`)
- ✅ Sid Bidasaria feature-dev plugin + 7 phases
- ✅ Addy Osmani 2500+ configs + 6 zones

### Prochaines étapes (par priorité)
1. **Audit thème 05 fine-tuning** — ~15 notes (Dettmers, Hu, Han, Dao, etc.)
2. **Audit thème 07 leaders/modèles/industrie** — ~80 notes (le plus gros, dernière étape)
3. **Audit thème 08 forge dogfooding** — méta-audit canoniques forge

## Fils ouverts

- **Notes prompt-engineering encore avec S*=0.509** : over-specification-paradox, deprecated-techniques-2026, outcome-first-prompting, index-prompting — déjà couvert par audit thème 02 (commits eb8f058, daf5d28, 0d8a415)
- **`gh` CLI absent forge** : workarounds documentés dans `reference_workarounds_session_constraints`
- **HEREDOC long Git Bash Windows échoue silencieusement** : préférer `git commit -F` ou inline court
- **Commits parallèles d'autres sessions/agents** englobent les modifs working tree — pas de bug, juste un pattern à connaître
- **Propagation cross-vault** : 18 notes pointent vers Context Engineering, plusieurs vers pattern-spec-driven-development — toutes scope thèmes 02/04/07 (à valider quand ces audits tournent)

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[methode-analyser-repo]]
- [[feedback_audit_thematique_methode]]
- [[feedback_carte_blanche_commit_push]]
- [[reference_audit_06_findings]]
- [[reference_workarounds_session_constraints]]
- [[LLM Wiki]]
- [[Context Engineering]]
- [[Andrej Karpathy]]
- [[Birgitta Böckeler]]
- [[Drew Breunig]]
