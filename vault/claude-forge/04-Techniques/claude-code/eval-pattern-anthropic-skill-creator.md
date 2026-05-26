---
titre: "Pattern eval Anthropic — mesurer skill quality via A/B benchmark"
resume: "Plugin skill-creator officiel Anthropic introduit infra eval A/B : workspace iteration-N + with_skill/baseline runs parallèles + run_loop.py optimization + benchmark.json + viewer HTML. Forge n'a pas l'équivalent. Pattern à intégrer comme reference pour mesurer skills critiques (pas systématique)."
aliases:
  - "eval pattern anthropic skill-creator"
  - "skill A/B benchmark"
  - "run_loop.py optimization skills"
  - "mesurer qualité skill"
  - "benchmark skill iteration"
derniere-maj: 2026-05-26
auteur: claude
type: technique
sources:
  - "Plugin anthropics/claude-plugins-official/plugins/skill-creator (26 mai 2026)"
  - "SKILL.md skill-creator Anthropic verbatim"
tags:
  - "#type/technique"
  - "#domaine/claude-code"
  - "#meta"
---

# Pattern eval Anthropic — mesurer qualité skill A/B

> Comment Anthropic mesure officiellement si une skill améliore les résultats. Forge n'a pas l'équivalent. À adopter pour skills critiques uniquement.

## Le gap forge

Forge a `outcomes-grader` (agent) + `outcomes-test` (skill) qui notent un livrable contre RUBRIC.md. Ce n'est PAS un benchmark itératif A/B. Skill-creator Anthropic introduit une vraie infra de mesure.

## Architecture A/B

```
<skill-name>-workspace/
└── iteration-1/
    ├── eval-name-1/
    │   ├── with_skill/outputs/      # Run AVEC la skill
    │   ├── without_skill/outputs/   # Run SANS (baseline)
    │   ├── eval_metadata.json
    │   ├── timing.json              # tokens + duration_ms
    │   └── grading.json             # expectations[] passed + evidence
    ├── eval-name-2/
    ├── benchmark.json               # agrégat
    └── benchmark.md                 # rapport human-readable
```

## Workflow itératif (verbatim Anthropic)

| Étape | Action |
|-------|--------|
| 1 | **Spawner simultanément** runs `with_skill` ET `baseline` |
| 2 | Pendant runs → rédiger assertions, expliquer pourquoi |
| 3 | Fin de chaque subagent → sauver `timing.json` |
| 4 | Grader → agréger → analyser → lancer viewer |
| 5 | Lire `feedback.json` → améliorer skill → recommencer |

## Format evals/evals.json

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Prompt utilisateur réaliste",
      "expected_output": "Description du résultat attendu",
      "files": [],
      "assertions": []
    }
  ]
}
```

## Format grading.json (champs exacts)

```json
{
  "expectations": [
    {
      "text": "description de l'assertion",
      "passed": true,
      "evidence": "preuve observée"
    }
  ]
}
```

## Commandes clés

```bash
# Agréger benchmark
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>

# Viewer HTML (Claude Code)
nohup python eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "mon-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &

# Cowork / headless : fichier statique
python eval-viewer/generate_review.py ... --static /tmp/review.html

# Optimisation du déclenchement (triggering)
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose

# Packaging skill
python -m scripts.package_skill <path/to/skill-folder>
```

## 3 agents Anthropic spécialisés (mentionnés)

- `agents/grader.md` — évaluer les assertions vs outputs
- `agents/comparator.md` — comparaison A/B en aveugle
- `agents/analyzer.md` — analyser pourquoi une version gagne

## Compatibilité environnement

| Fonctionnalité | Claude Code | Claude.ai | Cowork |
|----------------|-------------|-----------|--------|
| Subagents | ✅ | ❌ | ✅ (séries si timeout) |
| Browser viewer | ✅ | ❌ (inline) | ❌ (`--static`) |
| Baselines | ✅ | ❌ skip | ✅ |
| `run_loop.py` | ✅ | ❌ | ✅ |
| Packaging | ✅ | ✅ | ✅ |

## Principes de rédaction Anthropic (utile à intégrer)

- **Expliquer le _pourquoi_** plutôt que MUST/NEVER
- **Généraliser** depuis exemples test (éviter overfitting)
- **Garder lean** : < 500 lignes idéalement, supprimer ce qui ne sert pas (cohérent avec forge canonique)
- **Descriptions "pushy"** : mentionner explicitement contextes déclenchement (cohérent avec Thariq 9 catégories)

## Adoption forge

**ADOPTÉ** :
- Section "Pattern eval" ajoutée à [[comment-creer-skill]]
- Cette note technique comme référence détaillée

**NON-ADOPTÉ (par choix)** :
- **Pas de skill `/skill-eval` forge** : run_loop.py + viewer HTML = Python deps + maintenance lourde
- Justification : `outcomes-grader` + `outcomes-test` suffisent pour skills basiques. Pour skills critiques (5-6 max), faire l'éval **manuellement** en suivant ce pattern via skill-creator/skill-evolve enrichis

**REVERSE-POSSIBLE** : si forge passe à 100+ skills et besoin mesure systématique → reconsidérer skill `/skill-eval` lourde

## Wikilinks

- [[comment-creer-skill]] — canonique enrichie avec section eval
- [[plugins-officiels-veille-2026-05-26]] — synthèse veille parent
- [[outcomes-test]] — skill grader forge actuel (équivalent partiel)
- [[skill-evolve]] — skill forge optim (peut consommer ce pattern)
- [[Thariq-Shihipar]] — auteur skill-creator + 9 catégories skills

## Sources

- Plugin officiel `anthropics/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md`
- WebFetch 26 mai 2026
