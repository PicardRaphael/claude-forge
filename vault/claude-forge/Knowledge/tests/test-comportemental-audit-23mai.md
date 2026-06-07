---
titre: "Test comportemental — audit doctrinal 23 mai 2026 (6/6 PASS)"
resume: "Test comportemental session fraîche post-audit thématique vault Claude Code 23 mai 2026. Valide propagation des 6 corrections doctrinales : Brad Abrams Advisor Strategy, 29 events hooks, max non déprécié, Justin Young sans split modèles, Simon Willison lethal trifecta, séquence A→B→C→D→E + pipeline conditionnel. 6/6 PASS."
aliases:
  - "test comportemental audit 23 mai"
  - "test audit doctrinal mai 2026"
  - "behavioral test audit 23mai"
  - "validation doctrine post-pivot"
  - "test 6 corrections doctrinales"
derniere-maj: 2026-05-24
auteur: claude
type: test
tags:
  - "#domaine/testing"
  - "#domaine/claude-code"
  - "#domaine/validation-doctrine"
  - "#doctrine/2026"
---

# Test comportemental — audit doctrinal 23 mai 2026

> Test comportemental PASS/FAIL en session fraîche pour valider que les corrections de l'audit thématique vault Claude Code (23 mai 2026) sont correctement propagées dans le vault forge-brain et accessibles via MCP.

## Contexte

Audit thématique du 23 mai 2026 = 22 corrections doctrinales dans le vault Claude Code, dont 6 majeures testées ici. Test conduit en session fraîche, prompt fourni par Raphael, méthode imposée : `mcp__forge-brain__read_note` SANS `max_lines` sur notes canoniques (pas `search_brain` extraits, pas mémoire approximative).

## Les 6 corrections testées

| # | Avant 23 mai (erreur) | Après 23 mai (correction) |
|---|----------------------|--------------------------|
| 1 | Angela Jiang 5× cost reduction | **Brad Abrams** Advisor Strategy (CwC SF 6 mai 2026, talk avec Mario Rodriguez GitHub CPO) |
| 2 | 25+ events hooks | **29 events officiels** (vérifié docs Anthropic 23 mai 2026) |
| 3 | effort max déprécié v2.1.91 | **max toujours disponible** mai 2026, déprécié = `budget_tokens` manuel |
| 4 | Justin Young Init=Opus / Coding=Sonnet | **Modèles non spécifiés** chez Justin Young, footnote 1 "harness was otherwise identical", seul différentiateur = initial user prompts |
| 5 | Lethal trifecta = Thariq | **Simon Willison** juin 2025 (URL simonwillison.net/2025/Jun/16/the-lethal-trifecta/) |
| Bonus | Pas de séquence canonique unifiée | **A→B→C→D→E** (analyser réel → lire canoniques EN ENTIER → croiser → plan écarts → exécuter) + pipeline conditionnel architect/dev/reviewer/test |

## Résultats — 6/6 PASS

| Test | Réponse vérifiée | Source [[note]] | Verdict |
|------|------------------|----------------|---------|
| 1 — Advisor Strategy | Brad Abrams, verbatim "close to Opus-level intelligence at much lower prices", pattern executor (Haiku) + advisor (Opus) | [[comment-creer-agent]], [[workflow-claude-code-optimal]] | **PASS** |
| 2 — Events hooks | 29 events. TaskCreated ✅ #14, StopFailure ✅ #17, PostToolBatch ✅ #10, PreEdit ❌, PostBash ❌ | [[comment-creer-hook]] | **PASS** |
| 3 — Effort max | Toujours disponible mai 2026 (verbatim docs), déprécié = budget_tokens, doctrine forge prudence (prone overthinking) | [[comment-creer-agent]], [[workflow-claude-code-optimal]] | **PASS** |
| 4 — Justin Young 2-agent | Initializer + Coding, modèles non spécifiés, "system prompt, set of tools, and overall agent harness was otherwise identical" | [[comment-creer-agent]] | **PASS** |
| 5 — Pipeline analyse | Séquence A→B→C→D→E + pipeline architect (Opus xhigh) → dev → code-reviewer → test (Sonnet high), CONDITIONNEL pas systématique | [[methode-analyser-repo]] | **PASS** |
| Bonus — Lethal trifecta | Simon Willison 16 juin 2025, 3 éléments : private data / untrusted content / exfiltration vector | [[mcp-vs-skills-doctrine]] | **PASS** |

## Méthode validée

- `mcp__forge-brain__read_note` SANS `max_lines` sur 6 notes canoniques en parallèle
- Aucune réponse de mémoire — citations verbatim depuis vault
- Chaque note canonique contient une **note de correction explicite** ("⚠️ Avant 23 mai 2026 : le vault forge attribuait à tort…") qui sert d'ancrage anti-régression

## Pourquoi 6/6 PASS importe

C'est la preuve que :
1. Les corrections sont **encodées dans les notes canoniques** (pas seulement dans un changelog)
2. Le **MCP forge-brain est accessible** et retourne le contenu complet sans troncature
3. Aucune **régression doctrinale silencieuse** depuis MEMORY/RECAP non purgés
4. La méthode **séquence A→B→C→D→E** appliquée au test lui-même fonctionne

## Anti-pattern évité par ce test

[[feedback_doctrine_drift_pattern]] — doctrine encodée dans rules mais annulée silencieusement par MEMORY/RECAP non purgés. Le test comportemental en session fraîche détecte ce drift mieux qu'un audit statique.

## Reproduction

Pour reproduire ce test dans 1 mois (vérification non-régression) :
1. Session fraîche (`/clear`)
2. Prompt identique à celui de Raphael 23 mai 2026
3. Exiger `mcp__forge-brain__read_note` sur les 6 notes canoniques
4. Grille PASS/FAIL identique

Si N tests FAIL → investiguer drift via :
```bash
grep -l "Angela Jiang\|25+ events\|max déprécié\|Init.*Opus.*Coding.*Sonnet\|Thariq.*lethal trifecta" \
  .claude/projects/**/memory/*.md MEMORY.md 2>/dev/null
```

## Wikilinks

### Notes canoniques validées
- [[comment-creer-agent]]
- [[comment-creer-hook]]
- [[workflow-claude-code-optimal]]
- [[methode-analyser-repo]]
- [[mcp-vs-skills-doctrine]]
- [[comment-creer-skill]]

### Knowledge liées
- [[feedback_doctrine_drift_pattern]]
- [[feedback_behavioral_test_pattern]]
- [[feedback_lire_canoniques_avant_audit]]
- [[methode-pivoter-doctrine]]

### Leaders cités correctement
- [[Brad Abrams]]
- [[Justin Young]]
- [[Simon Willison]]
- Mario Rodriguez (GitHub CPO) — fiche à créer
- [[Cat Wu]]
- [[Boris Cherny]]

---

**Fin note `test-comportemental-audit-23mai.md`** — créée 23 mai 2026 post-validation 6/6 PASS.
