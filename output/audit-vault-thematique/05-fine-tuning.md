# Audit Vault — Thème : Fine-tuning

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md`
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème large, **pas du tout** lié à Anthropic — Anthropic ne fait pas de fine-tuning ouvert) :
>    - **Sources primaires fine-tuning** (les meilleurs du domaine, single source acceptable) : **Tim Dettmers (QLoRA, bitsandbytes)**, **Edward Hu (LoRA, μTransfer)**, **Daniel Han (Unsloth, 2-30x speedup)**, **Tri Dao (FlashAttention, Together AI)**, **Song Han (AWQ, SmoothQuant, TinyML MIT)**, **Georgi Gerganov (llama.cpp, GGUF)**, **Sebastian Raschka (Build LLM From Scratch, Lightning AI)**, **Hamel Husain (Parlance Labs, course Mastering LLMs)**, **Nathan Lambert (Post-Training Lead AI2, RLHF)**, **Maxime Labonne (Post-Training Liquid AI)**, **Philipp Schmid (Ex-HuggingFace → Google DeepMind)**, **Wing Lian (Axolotl)**, **Yaowei Zheng (LLaMA-Factory)**, **Teknium (Nous Research, Hermes)**
>    - **Papers académiques arXiv** = single source acceptable (LoRA Hu et al, QLoRA Dettmers et al, FlashAttention Dao et al, etc.)
>    - **Docs officielles** frameworks (Unsloth, Axolotl, HuggingFace PEFT, vLLM, LLaMA-Factory) sur LEUR produit = single source
>    - **Anthropic** = quasi non-pertinent ce thème (pas de fine-tuning public). Single source seulement si claim concerne Claude API capabilities limitées.
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **⚠️ Risque spécifique ce thème** : benchmarks et chiffres de performance fine-tuning (speedup, VRAM, etc.) souvent cités sans contexte précis (modèle / taille / hardware). Toujours préciser source primaire + setup exact.
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Scope

**Dossier** : `04-Techniques/fine-tuning/`

**Notes à auditer (~10)** :
1. `MOC-Fine-Tuning`
2. `fine-tuning-alignment`
3. `fine-tuning-datasets`
4. `fine-tuning-evaluation`
5. `fine-tuning-frameworks`
6. `fine-tuning-infrastructure`
7. `fine-tuning-models`
8. `fine-tuning-privacy`
9. `fine-tuning-techniques-peft`
10. `rag-vs-fine-tuning`

## Hiérarchie experts (priorité ce thème)

### Liste actuelle forge

**Researchers** (P1) :
- Tim Dettmers (QLoRA author, bitsandbytes)
- Edward Hu (LoRA paper auteur)
- Tri Dao (Flash Attention, Mamba)
- Sebastian Raschka (Lightning AI, fine-tuning content)
- Hamel Husain (parlance.ai, fine-tuning expert)
- Nathan Lambert (allenai, RLHF)
- Rafael Rafailov (DPO paper)
- Song Han (MIT, model compression)

**Frameworks** (P2) :
- Daniel Han (Unsloth)
- Wing Lian (Axolotl)
- Maxime Labonne (mlabonne)
- Philipp Schmid (Hugging Face)
- Yaowei Zheng (LLaMA-Factory)
- Teknium (Nous Research)
- Georgi Gerganov (llama.cpp, GGUF)

### Étape 0 — Valider/étendre

WebSearch : "fine-tuning expert 2026", "LoRA QLoRA author", "RLHF DPO researcher", "Hugging Face fine-tuning expert", "open source LLM fine-tuning leader".

## Sources spécifiques

### Papers (arXiv)
- "LoRA: Low-Rank Adaptation" (Hu 2021)
- "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers 2023)
- "Direct Preference Optimization (DPO)" (Rafailov 2023)
- "InstructGPT" (Ouyang 2022)
- "Constitutional AI" (Anthropic)
- "RLAIF" (Lee 2024)
- Papers PEFT récents

### Officiel
- huggingface.co/docs/peft
- github.com/huggingface/trl
- github.com/unslothai/unsloth
- github.com/OpenAccess-AI-Collective/axolotl
- github.com/hiyouga/LLaMA-Factory
- platform.openai.com/docs/guides/fine-tuning
- docs.anthropic.com (si fine-tuning Claude existe en 2026)

### Blogs reconnus
- sebastianraschka.com (Lightning AI courses, blog)
- huggingface.co/blog (Schmid, Labonne posts)
- mlabonne.github.io
- hamel.dev (Hamel Husain)
- timdettmers.com (rare posts mais référence)
- interconnects.ai (Nathan Lambert RLHF)

### Vidéos YouTube
- Sebastian Raschka talks
- Hamel Husain "Mastering LLMs" course
- Daniel Han Unsloth talks
- Hugging Face course (fine-tuning)
- Maxime Labonne tutorials

## Claims à vérifier (priorité)

### Techniques canoniques
- LoRA / QLoRA — convergence académique ✅
- DPO vs RLHF — quand utiliser quoi
- PEFT (Parameter-Efficient Fine-Tuning) — overview
- DoRA, AdaLoRA, autres variantes 2024-2026

### Frameworks comparaison
- Unsloth vs Axolotl vs LLaMA-Factory vs TRL
- Quand utiliser quel framework — convergence ?

### Stats
- Speedups Unsloth, claims marketing → vérifier benchmarks indépendants
- Memory savings QLoRA — citation paper exacte
- Coût fine-tuning vs RAG — convergence ?

### Verbatim
- "rag-vs-fine-tuning" — décision tree convergence ?
- Recommandations 2026 vs 2024 (techniques deprecated)

### Modèles fine-tunables
- Llama 3.x, Mistral, Qwen, autres — état 2026
- Claude fine-tuning : possible ou pas ?

## Étape F — Propagation Fine-tuning

Si modifs notes vault :

**Forge** :
- Pas d'usage direct fine-tuning dans forge (à vérifier)
- Skills pédagogiques si certaines

**Autres repos** :
- neo_ia si fine-tuning utilisé (probablement non, neo_ia utilise Claude API)
- ia_back idem

**Backlinks** :
- `get_backlinks` pour MOC-Fine-Tuning et notes principales

## Output

`output/audit-vault-thematique/05-fine-tuning/`

---

**Commence par étape 0. advisor() aux transitions.**
