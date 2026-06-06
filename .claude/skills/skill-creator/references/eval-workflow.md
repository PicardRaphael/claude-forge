# Eval workflow — Phases 5–9 (détail complet)

Source : workflow officiel Anthropic skill-creator + doctrine forge.

---

## Phase 5 — Lancer les evals

Pour chaque test case, spawner **simultanément** deux sub-agents via Task tool :
- `with_skill` : run avec la skill active
- `baseline` : run sans la skill (ou snapshot ancienne version si optimisation)

Structure résultats :
```
<skill>-workspace/iteration-N/eval-<id>/
├── with_skill/outputs/
├── without_skill/outputs/   # ou old_skill/
├── eval_metadata.json       # nom descriptif de l'eval
└── timing.json              # total_tokens + duration_ms — capturer dès notification
```

**Générer le eval viewer AVANT de juger soi-même** (`--static` sur Cowork/headless).

---

## Phase 6 — Rédiger les assertions pendant les runs

- Descriptives, vérifiables par script si possible
- Ne pas forcer des assertions sur des outputs subjectifs
- Format `grading.json` : champs exacts `text`, `passed`, `evidence` (le viewer dépend de ces noms)

---

## Phase 7 — Capturer timing

Dès chaque notification de fin de sub-agent → sauvegarder `timing.json` immédiatement.
C'est la seule occasion de capturer `total_tokens` et `duration_ms`.

---

## Phase 8 — Grader, agréger, lancer le viewer

1. Sub-agent grader (lit assertions) → `grading.json`
2. Agréger → `benchmark.json` + `benchmark.md` (pass_rate, time, tokens, mean±stddev, delta)
3. Sub-agent analyste → surface assertions non-discriminantes, evals flaky, tradeoffs
4. Lancer le eval viewer — `--previous-workspace` si itération 2+

Commandes clés :
```bash
# Agréger
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>

# Viewer (Claude Code)
python eval-viewer/generate_review.py <workspace>/iteration-N --skill-name "nom" --benchmark <workspace>/iteration-N/benchmark.json

# Viewer statique (Cowork/headless)
python eval-viewer/generate_review.py ... --static /tmp/review.html
```

---

## Phase 9 — Lire le feedback & améliorer

Depuis `feedback.json` — principes Anthropic :
- **Généraliser** — éviter l'overfitting sur les cas test
- **Garder lean** — lire les transcripts, pas juste les outputs ; supprimer ce qui ne sert pas
- **Expliquer le pourquoi** — ALL-CAPS MUST = yellow flag → reformuler avec raison
- **Bundler le répété** — si tous les sub-agents ont réécrit le même helper → `scripts/`

Recommencer depuis Phase 5 jusqu'à convergence.

---

## Compatibilité environnements

| Fonctionnalité | Claude Code | Claude.ai | Cowork |
|---|---|---|---|
| Sub-agents (Task tool) | ✅ | ❌ | ✅ (sériel si timeout) |
| Browser viewer | ✅ | ❌ (inline) | ❌ (`--static`) |
| Baselines | ✅ | ❌ skip | ✅ |
| `run_loop.py` | ✅ | ❌ | ✅ |

---

## Evals — OBLIGATOIRES

Les evals sont **obligatoires** pour toute skill créée ou optimisée.
Objectif : garantir que la skill améliore vraiment les résultats vs baseline.
Sans mesure → pas de validation que la skill fonctionne (SkillsBench : auto-généré sans eval = –1.3pp en moyenne).

Seule exception : skill de connaissance pure subjective (style d'écriture, art) → pas d'assertions objectives possibles, éval qualitative uniquement.
