---
titre: "Fine-Tuning Privacy — On-Premise, RGPD, Données Personnelles"
resume: "Guide fine-tuning privé — solutions on-premise, differential privacy (DP-SGD, VaultGemma), federated learning, TEE, RGPD, machine unlearning, plateformes certifiées"
aliases:
  - "fine-tuning privacy"
  - "fine-tuning RGPD"
  - "fine-tuning GDPR"
  - "on-premise fine-tuning"
  - "VaultGemma"
  - "differential privacy LLM"
  - "federated learning LLM"
  - "données personnelles IA"
  - "machine unlearning"
type: technique
domaine: ia
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://research.google/blog/vaultgemma-the-worlds-most-capable-differentially-private-llm/"
  - "https://research.google/blog/fine-tuning-llms-with-user-level-differential-privacy/"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/fine-tuning"
  - "#domaine/privacy"
  - "#domaine/rgpd"
---

## Solution 100% Locale

**Stack complet :** modèle open-weight + Unsloth/LLaMA-Factory + Ollama pour servir.
**Hardware min :** RTX 4090 ($1,600 one-time) pour 7-13B QLoRA. Zéro frais récurrents.

## Techniques Privacy-Preserving

### Differential Privacy (DP-SGD)

Modifie SGD en (1) clippant chaque gradient per-example, (2) ajoutant du bruit gaussien calibré.

**VaultGemma** (Google, sept 2025) : LLM le plus capable avec DP formelle. Gemma 2 1B, epsilon ≤ 2.0. Zéro mémorisation détectée. Mais utilité ~5 ans de retard vs modèles non-privés.

**Conseil pratique :** Utiliser PEFT (LoRA/QLoRA) avec DP plutôt que full-parameter — moins de bruit nécessaire pour la même garantie.

### Federated Learning

Entraînement distribué — chaque participant entraîne localement, ne partage que les gradient updates. Combiné avec DP = garantie la plus forte.

### TEE (Trusted Execution Environments)

Entraînement/inférence dans des enclaves chiffrées matériellement. Même le cloud provider ne voit pas les données.

- **NVIDIA Hopper/Blackwell** : mode confidential computing
- **AMD EPYC Turin (SEV-SNP)** : chiffrement CPU
- **Intel TDX/SGX** : <10% overhead throughput

Pour Qwen-32B avec ~8K tokens : <1% latence overhead.

## Plateformes Certifiées

| Plateforme | Privacy | Forces |
|------------|---------|--------|
| **Prem Studio** | SOC2/GDPR/HIPAA, Suisse | PII redaction intégré, on-prem |
| **Lamini** | Enterprise | Memory Tuning (95% accuracy vs 50% GPT-4+RAG) |
| **Predibase** | SOC2, acquis par Rubrik | LoRAX — 1000+ adapters/1 GPU |
| **Katonic AI** | Sovereign, air-gapped | Gouvernements, Fortune 500 |
| **AWS SageMaker** | Your VPC | Données dans votre compte AWS |
| **TrueFoundry** | HIPAA, SOC2 | Medtronic, Siemens (17M inférences cliniques/mois) |

## RGPD / Compliance

- **DPA obligatoire** (Article 28) : couvre résidence données, rétention, sub-processors
- **Base légale** (Article 6) : documenter la base légale pour le fine-tuning
- **Transferts cross-border** : SCCs ou mécanisme approuvé
- **EU AI Act** : conformité complète août 2026

### Machine Unlearning (Droit à l'oubli)

Problème non résolu : que signifie "effacer" quand les données sont absorbées dans les poids ?

**Approches 2026 :**
1. Re-entraîner sur dataset nettoyé (le plus défendable juridiquement)
2. Approximate unlearning (gradient ascent, NPO)
3. FIT framework (2026) : filtrage + attribution de couches
4. LLMEraser (ICLR 2025) : influence functions
5. Output suppression (le plus rapide, le moins défendable)

**Recommandation :** Combiner (a) suppression output rapide + (b) suppression pipeline données + (c) unlearning ciblé. Tout documenter pour les auditeurs.

## RAG vs Fine-Tuning pour la Privacy

**RAG est naturellement plus privacy-friendly** pour les données dynamiques : documents supprimables du vector store sans re-entraîner. Le fine-tuning embarque dans les poids → problème d'unlearning.

**Approche hybride :** Fine-tune pour style/comportement (faible risque privacy) + RAG pour contenu factuel (facile à update/supprimer).

## Liens

- [[MOC-Techniques]]
- [[fine-tuning-infrastructure]] — GPUs et cloud
- [[rag-vs-fine-tuning]] — quand utiliser quoi
- [[fine-tuning-techniques-peft]] — LoRA/QLoRA pour réduire le bruit DP