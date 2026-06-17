---
titre: "Fine-Tuning Datasets — Préparation, qualité, données synthétiques"
resume: "Best practices préparation de données pour fine-tuning LLM — taille dataset, qualité, données synthétiques, outils (Argilla, Distilabel, Label Studio), formats"
aliases:
  - "fine-tuning datasets"
  - "training data"
  - "données fine-tuning"
  - "synthetic data"
  - "données synthétiques"
  - "data preparation fine-tuning"
  - "Argilla"
  - "Distilabel"
type: technique
domaine: ia
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://ai.meta.com/blog/how-to-fine-tune-llms-peft-dataset-curation/"
  - "https://github.com/argilla-io/distilabel"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/data"
---

## Taille de dataset recommandée

| Type de tâche | Minimum | Recommandé | Rendements décroissants |
|---------------|---------|------------|------------------------|
| Classification simple | 50-100/classe | 100-300/classe | >1,000/classe |
| Extraction de données | 100-200 | 200-500 | >2,000 |
| Génération de contenu | 200-500 | 500-2,000 | >5,000 |
| Adaptation domaine complexe | 500 | 1,000-5,000 | >10,000 |
| Instruction following | 100 | 500-1,000 | >5,000 |

**Principe critique** (heuristique praticienne inspirée de [LIMA — Zhou et al. 2023, arXiv 2305.11206](https://arxiv.org/abs/2305.11206)) : un petit dataset expert-curated (~1000 exemples chez LIMA) peut surpasser un large dataset bruyant. Le ratio "200 vs 2000" est une paraphrase communauté, pas un chiffre du paper. Répéter un dataset filtré pendant plusieurs epochs > entraîner un dataset N× plus grand pendant 1 epoch.

## Best Practices Qualité

1. **Format consistant** — instruction/input/output, conversation, ou ShareGPT. Standardiser tout le dataset
2. **Supprimer doublons et quasi-doublons** — causent mémorisation au lieu de généralisation
3. **Valider l'exactitude factuelle** — 1 exemple faux peut enseigner l'hallucination
4. **Équilibrer les catégories** — sous-échantillonner majorité ou sur-échantillonner minorité
5. **Inclure les edge cases** — cibler les faiblesses spécifiques
6. **Focus sur ce que le base model rate** — évaluer d'abord, créer les exemples ensuite

## Formats de données

| Format | Structure | Usage |
|--------|-----------|-------|
| **Alpaca** | `{"instruction", "input", "output"}` | Simple, instruction-following |
| **ShareGPT** | `{"conversations": [{"from", "value"}]}` | Multi-turn, conversationnel |
| **Chat Template** | Messages avec rôles system/user/assistant | Standard HuggingFace |

## Données Synthétiques

**Approche dominante 2026 :** Teacher-student distillation — un LLM fort (GPT-4, Claude) génère des données d'entraînement pour un modèle plus petit.

**Pipeline multi-étapes :**
1. Générer exemples synthétiques avec un modèle teacher
2. Filtrage automatisé : scoring cohérence, détection contradictions, déduplication
3. Review humain de 10-20% pour calibration qualité
4. Raffinement itératif : feedback des échecs dans le prompt de génération

## Outils

| Outil | Stars | Fonction | Meilleur pour |
|-------|-------|----------|---------------|
| **Distilabel** (Argilla) | ~3.2K | Génération données synthétiques + AI feedback | Pipelines scalables |
| **Argilla** | ~5K | Annotation et review | Human-in-the-loop |
| **Label Studio** | ~27K | Annotation multi-format | Multi-modal |

## Workflow Recommandé 2026

```
1. Évaluer base model sur la tâche (identifier gaps)
2. Générer exemples synthétiques avec Distilabel (cibler les gaps)
3. Review et filter avec Argilla (humain + AI hybrid)
4. Fine-tune avec Unsloth / LLaMA-Factory
5. Évaluer → identifier gaps restants → itérer
```

## Dataset de préférence (DPO / RLHF)

Les sections ci-dessus couvrent les datasets SFT (instruction/output). Le **preference tuning** (cf [[fine-tuning-alignment]]) exige un format différent : des **paires** $\{x, y_w, y_l\}$ — prompt, réponse gagnante, réponse perdante.

### Construction (recette on-policy)

1. Le modèle **SFT** (pas le base model) génère plusieurs complétions par prompt (typiquement ~16).
2. Toutes les candidates sont scorées (reward model ou juge).
3. On forme la paire en sélectionnant la **meilleure** et la **pire** complétion (contrastive selection) → signal net, on écarte les comparaisons ambiguës à faible signal.

**On-policy > off-policy** : échantillonner depuis la distribution générative du modèle lui-même évite le *distribution shift* et donne des gains d'alignement plus stables et fiables que les paires off-policy. Datasets de référence : UltraFeedback.

### Pitfalls DPO (empiriques)

| Pitfall | Conséquence | Remède |
|---------|-------------|--------|
| **Skipper le SFT** (DPO direct sur base model) | Instable, mauvais résultats | DPO = raffinement d'un modèle déjà instruction-tuned |
| **Learning rate trop haut** | Oubli catastrophique | LR faible (DPO ≪ SFT) |
| **Trop d'epochs** | Modèle rigide, répétitif | 1–2 epochs suffisent souvent |
| **Données de préférence bruitées** | Garbage in, garbage out | Signal de préférence clair, déduplication |
| **Ignorer le modèle de référence** | Perte de stabilité | La pénalité KL via $\pi_{\text{ref}}$ est cruciale (cf [[dpo-derivation]]) |

Outils : `DPOTrainer` de **TRL** (charge un dataset type UltraFeedback, `accelerate launch`), pipeline config-driven via **Axolotl** (cf [[fine-tuning-frameworks]]).

## Liens
- [[fine-tuning-alignment]] — DPO, GRPO, variantes (consomme le dataset de préférence)
- [[dpo-derivation]] — pourquoi la pénalité KL / le modèle de référence est cruciale

- [[MOC-Techniques]]
- [[fine-tuning-techniques-peft]] — techniques PEFT
- [[fine-tuning-evaluation]] — évaluer le modèle fine-tuné
- [[fine-tuning-frameworks]] — outils de fine-tuning