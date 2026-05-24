---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-24 : 5 lignes Karpathy en tête CLAUDE.md forge + enforcement meta-commentaires via hook PreToolUse + auto-injection canonique dans 6 agents créateurs/analyseurs."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Doctrine forge durcie : enforcement réel via hook `meta-commentary-detector.py` ACTIF + auto-injection canonique dans body des 6 agents créateurs/analyseurs. Catalogue "HOOKS TRANSVERSAUX" établi pour proposition systématique en audit repo.

## Dernière session (2026-05-24)

### Décisions prises

- **5 lignes Karpathy verbatim en tête de tout CLAUDE.md forge** (claude-forge v3.2, ia_back, neo_ia). Décision Raphael + validation 2 tours advisor.
- **PAS de ligne italique tradeoff** sous les 5 lignes — bruit visuel, dilue le signal.
- **Règle universelle "JAMAIS de meta-commentaire"** dans hook/agent/skill/CLAUDE.md/rule. Validée par DA avec 6 amendements appliqués.
- **6 amendements DA appliqués** : frontière ≤3 mots stricte, purge claude-forge/CLAUDE.md (7 infractions), garde-fou anti-purge, Anthropic vérifié, methode-pivoter-doctrine, rule chargée systématiquement (via hook plutôt que rule passive).
- **Innovation #1 ACTIVE** : hook `meta-commentary-detector.py` PreToolUse Write|Edit|MultiEdit, 9 patterns, exclusions vault/Knowledge/references/RECAP/CHANGELOG/frontmatter, désambiguïsation ≤3 mots autorisée.
- **Innovation #2 ACTIVE** : section "Lecture obligatoire au démarrage" avec `read_note` SANS max_lines dans skill-creator, agent-creator, hook-creator, claudemd-optimizer, project-auditor, project-analyzer.
- **Catalogue HOOKS TRANSVERSAUX** dans `[[comment-creer-hook]]` : 6 hooks réutilisables avec cas d'usage. project-auditor + project-analyzer briefés pour les proposer en audit.
- **NE PAS propager 5 lignes à neoteem-brain** (vault Obsidian, principes "diff minimal/code minimum" pas pertinents).

### En cours

- **Hook meta-commentary-detector ACTIF en prod** : settings.json mis à jour, JSON valide, self-tests 15/15 passent. À surveiller : faux positifs réels sur composants nouveaux.
- **MEMORY.md à 24.5 KB** (sous cible 24.4 KB de justesse) : 7 doublons supprimés, 5 OBSOLÈTES retirés, 30+ lignes raccourcies.
- **claude-forge/CLAUDE.md à 103 lignes** : 7 infractions meta-commentaires purgées, version 3.2.

### Prochaines étapes

- **Tester hook en condition réelle** : edit avec `"Source: X"` dans un CLAUDE.md → doit bloquer (exit 2).
- **Décision à prendre** : trou architectural delegate-guard.py (sub-agents contournent via Bash). Options : (a) étendre couverture Bash, (b) accepter contournement comme voie documentée. Mini-DA dédié si tu veux durcir.
- **Proposition Jarvis ouverte** : propager hook detector à ia_back / neo_ia (mêmes risques meta-commentaires).
- **MEMORY.md** à ~24.5 KB, près de la limite. Surveiller croissance, purger trimestriellement.

## Fils ouverts

- **Karpathy avancé NON propagé dans corps CLAUDE.md** : décision = canonique vault suffit, auto-injection #2 force la lecture par construction. À ré-évaluer si trou observé.
- **Skill-creator + agent-creator contiennent encore 1 wikilink intro original** non patché (les wikilinks morts ont été corrigés, mais l'audit peut révéler d'autres référents décoratifs).
- **CLAUDE.md modifié hors session** mentionné dans précédent context-actuel (downgrade 3.2 → 3.x sans suffixe) — VÉRIFIÉ ce 24 mai : version 3.2 stable. Probablement résolu.
- **Mesurer impact innovations sur prochaine création** : skill-creator dispatché lira-t-il vraiment la canonique EN ENTIER ? Behavioral test à faire (cf `feedback_behavioral_test_pattern`).

## Métriques session 2026-05-24

- **5 commits push** sur main : `74916cd`, `1908a73`, `7614f51` (claude-forge) + `904497c` (ia_back) + `cc06033` (neo_ia)
- **18 fichiers modifiés** dans le dernier gros commit (+814 lignes)
- **Hook créé** : meta-commentary-detector.py (~200L) + tests (~100L)
- **6 agents patchés** avec auto-injection canonique
- **3 wikilinks morts fixés** (skills-guide, agents-orchestration, hooks-guide)
- **7 infractions CLAUDE.md purgées** (en 2 passes — 1ère passe sub-agent claim sans empirie)
- **MEMORY.md** : 30 KB → 24.5 KB (-18%)

## Patterns émergeant cette session

- **Posture Jarvis fragile sur sessions longues** → `feedback_glissement_jarvis_executant`
- **Sub-agents éditeurs claim sans empirie** → `feedback_sub_agent_claim_sans_empirie`
- **`.proposed` files = transitoire** → `feedback_proposed_files_antipattern`
- **Format proposition innovation calibré** : "ça serait top de faire X car Y, personne ne le fait, on pense que..."

## Liens

[[Raphael-Picard|Raphael Picard]]
[[Claude-Forge|Claude-Forge]]
[[comment-ecrire-claudemd]]
[[comment-creer-hook]]
[[erreur-meta-commentaires-composants]]
[[critique-2026-05-24-meta-commentaires-doctrine]]
[[methode-pivoter-doctrine]]
