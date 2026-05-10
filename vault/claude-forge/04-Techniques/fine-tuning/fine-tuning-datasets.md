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
derniere-maj: 2026-05-10
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

**Principe critique :** 200 exemples expert-curated surpassent 2,000 exemples bruyants. Répéter un dataset filtré pendant 10 epochs > entraîner un dataset 10x plus grand pendant 1 epoch.

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
| **Argilla** | ~4.5K | Annotation et review | Human-in-the-loop |
| **Label Studio** | ~20K | Annotation multi-format | Multi-modal |

## Workflow Recommandé 2026

```
1. Évaluer base model sur la tâche (identifier gaps)
2. Générer exemples synthétiques avec Distilabel (cibler les gaps)
3. Review et filter avec Argilla (humain + AI hybrid)
4. Fine-tune avec Unsloth / LLaMA-Factory
5. Évaluer → identifier gaps restants → itérer
```

## Liens

- [[fine-tuning-techniques-peft]] — techniques PEFT
- [[fine-tuning-evaluation]] — évaluer le modèle fine-tuné
- [[fine-tuning-frameworks]] — outils de fine-tuning