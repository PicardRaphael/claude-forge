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
derniere-maj: 2026-05-23
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

**VaultGemma** ([Google Research, 12 sept 2025](https://research.google/blog/vaultgemma-the-worlds-most-capable-differentially-private-llm/)) : LLM le plus capable avec DP formelle. Architecture Gemma 2 1B, **ε ≤ 2.0 avec δ ≤ 1.1e-10 (sequence-level, 1024 tokens)**. No detectable memorization. Verbatim Google : *"today's private training methods produce models with utility comparable to that of non-private models from roughly 5 years ago"* (baseline proxy GPT-2 1.5B).

**Conseil pratique :** Utiliser PEFT (LoRA/QLoRA) avec DP plutôt que full-parameter — moins de bruit nécessaire pour la même garantie.

### Federated Learning

Entraînement distribué — chaque participant entraîne localement, ne partage que les gradient updates. Combiné avec DP = garantie la plus forte.

### TEE (Trusted Execution Environments)

Entraînement/inférence dans des enclaves chiffrées matériellement. Même le cloud provider ne voit pas les données.

- **NVIDIA Hopper/Blackwell** : mode confidential computing — H100 CC GPU ~4-8% throughput overhead
- **AMD EPYC Turin (SEV-SNP)** : chiffrement CPU
- **Intel TDX/SGX** : <10% overhead throughput, 20% latence ([benchmark ETH Zurich arXiv 2509.18886](https://arxiv.org/abs/2509.18886), sept 2025, sur Llama2 7B/13B/70B — SGX 4.80-6.15%, TDX 5.51-10.68%)

Pour H100 CC mode : ~4-8% overhead, diminue avec longueur de contexte (claim spécifique "Qwen-32B 8K <1%" non sourçable, retiré).

## Plateformes Certifiées

| Plateforme | Privacy | Forces |
|------------|---------|--------|
| **Prem Studio** | SOC2/GDPR/HIPAA, Suisse | PII redaction intégré, on-prem |
| **Lamini** | Enterprise | Memory Tuning — case study Fortune 500 spécifique : 95% accuracy vs 50% GPT-4+RAG (pas benchmark généralisé) |
| **Predibase** | SOC2, acquis par Rubrik (juin 2025) | LoRAX — "1000s of fine-tuned LLMs" (claim marketing ; benchmarks publics : 1-128 adapters sur A10G) |
| **Katonic AI** | Sovereign, air-gapped | Gouvernements, Fortune 500 |
| **AWS SageMaker** | Your VPC | Données dans votre compte AWS |
| **TrueFoundry** | HIPAA, SOC2 | Clients : ResMed, Siemens Healthineers, Automation Anywhere, Zscaler, NVIDIA. Volume "10B+ requests/month" (AI Gateway global, pas spécifique clinique) |

## RGPD / Compliance

- **DPA obligatoire** (Article 28) : couvre résidence données, rétention, sub-processors
- **Base légale** (Article 6) : documenter la base légale pour le fine-tuning
- **Transferts cross-border** : SCCs ou mécanisme approuvé
- **EU AI Act** : 2 août 2026 = main deadline ; **accord politique mai 2026** reporte high-risk Annex III à déc 2027, watermarking transparence à 2 déc 2026 ([Travers Smith mai 2026](https://www.traverssmith.com/knowledge/knowledge-container/eu-agrees-to-delay-key-ai-act-compliance-deadlines/))

### Machine Unlearning (Droit à l'oubli)

Problème non résolu : que signifie "effacer" quand les données sont absorbées dans les poids ?

**Approches 2026 :**
1. Re-entraîner sur dataset nettoyé (le plus défendable juridiquement)
2. Approximate unlearning (gradient ascent, NPO)
3. FIT framework ([arXiv 2601.21682](https://arxiv.org/abs/2601.21682), 29 janv 2026) : filtrage + importance-aware + targeted layer
4. LLMEraser ([arXiv 2412.00383](https://arxiv.org/abs/2412.00383), ICLR 2025) : influence functions + PEFT adapters
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