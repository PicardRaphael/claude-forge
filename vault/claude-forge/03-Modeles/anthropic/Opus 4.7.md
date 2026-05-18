---
titre: "Claude Opus 4.7"
resume: "Modèle le plus capable Anthropic — SWE-bench 87.6%, instruction-following littéral, adaptive thinking, xhigh effort, design defaults, nouveau tokenizer"
aliases:
  - "opus-4-7"
  - "claude-opus-4-7"
  - "opus 4.7"
  - "claude opus"
  - "modele opus"
  - "SWE-bench 87"
  - "opus prompting guide"
domaine: claude-code
type: modele
derniere-maj: 2026-05-18
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-opus-4-7"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/modele"
  - "#domaine/claude"
---

## Specifications

| Propriété | Valeur |
|-----------|--------|
| Context window | 200K (standard) / 1M (beta) |
| Prix input | $5/MTok |
| Prix output | $25/MTok |
| Thinking | Adaptive (off par défaut, `thinking: {type: "adaptive"}` requis) |
| Vision | 2,576px long edge (3.75 MP) vs 1,568px pour 4.6 |
| Tokenizer | Nouveau, ~1x-1.35x plus de tokens selon contenu |
| Computer use | Jusqu'à 2576px / 3.75MP, recommandé 1080p (balance perf/coût) |

## Benchmarks

| Benchmark | Score | vs Opus 4.6 |
|-----------|-------|-------------|
| SWE-bench Verified | 87.6% | +6.8% (80.8%) |
| Terminal-Bench 2.0 | 69.4% | +4% (65.4%) |
| GPQA Diamond | 94.2% | +2.9% (91.3%) |
| Bug-finding recall | +11pp | sur PRs réels Anthropic |

## Changements comportement vs 4.6 (guide officiel Anthropic)

### Instruction-following littéral (changement clé)
Interprète les prompts plus littéralement que 4.6, surtout à low effort. Ne généralise pas silencieusement une instruction d'un item à un autre. Ne fait pas de requêtes non demandées. Si un scope large est souhaité, le dire explicitement : "Apply this formatting to every section, not just the first one."

### Response length adaptative
Calibre la longueur sur la complexité perçue, pas une verbosité fixe. Réponses courtes sur lookups simples, longues sur analyses ouvertes. Exemples positifs de concision > instructions négatives ("don't be verbose").

### Tool use moins fréquent
Tendance à raisonner plus et appeler moins d'outils. Produit de meilleurs résultats dans la plupart des cas. Pour forcer plus de tool use : augmenter effort (`high`/`xhigh`) ou prompter explicitement.

### Subagents moins spontanés
Spawn moins de subagents par défaut (steerable via prompt). Donner des guidelines explicites : quand fan-out, quand travailler directement.

### Ton plus direct
Plus direct et opinioné, moins de validation-forward, quasi-zéro emoji. Pour récupérer un ton chaud : "Use a warm, collaborative tone. Acknowledge the user's framing before answering."

### Progress updates de meilleure qualité
Fournit des updates plus réguliers et de meilleure qualité pendant les traces agentiques longues. Supprimer le scaffolding forcé ("After every 3 tool calls, summarize progress").

### Design defaults persistants
Style "maison" par défaut : cream/off-white (#F4F1EA), serif (Georgia, Fraunces), accents terracotta/amber. Persiste même avec instructions génériques. Voir [[opus-47-design-defaults]].

### Code review : recall vs precision
+11pp recall sur bug-finding, mais les prompts "only report high-severity" sont suivis plus fidèlement → apparence de recall↓. Fix : "Report every issue you find, including uncertain/low-severity. Include confidence level and severity for downstream filtering."

### Prefilled responses supprimés
Prefills sur le dernier assistant turn retournent 400 error sur 4.6+. Alternatives : structured outputs, XML tags, instructions directes.

## Effort levels (critique pour 4.7)

Effort plus important que sur tout modèle précédent. Strict respect aux niveaux bas.

| Niveau | Usage recommandé |
|--------|-----------------|
| `xhigh` | Coding + agentic (défaut recommandé) |
| `high` | Intelligence-sensitive, sessions concurrentes |
| `medium` | Cost-sensitive, trading off intelligence |
| `low` | Tâches courtes, latency-sensitive |
| `max` | Gains marginaux possibles, risque overthinking |

À `xhigh`/`max` : toujours 64k+ max_tokens pour laisser de la place au thinking.

## Quand utiliser

- Modèle par défaut pour tous les agents projet Neoteem (`effort: xhigh` par défaut)
- Sessions agentiques complexes, analyses approfondies, sécurité
- `effort: high` minimum pour les subagents
- `effort: medium`/`low` pour réduire coût/latence
- Coding interactif : spécifier tâche/intent/contraintes upfront dans le 1er turn, ajouter auto mode, réduire interactions humaines

## Dates clés

- 16 avril 2026 : Lancement
- 23 avril 2026 : Devient modèle par défaut Enterprise + API

## Liens

- [[Effort Levels Guide]]
- [[Adaptive Thinking]]
- [[opus-47-design-defaults]]
- [[deprecated-techniques-2026]]
- [[MOC-Modeles]]
