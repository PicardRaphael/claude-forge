# Domaine — Fine-tuning, Local AI & Quantization

Couvre : LoRA, QLoRA, GGUF, fine-tuning frameworks, quantization, post-training, local inference.
Nombre de queries : 20 — **Découper sur 2 agents** (Agent A + Agent B)

## Leaders Fine-tuning & Local AI

| Personne | Rôle | Sources |
|----------|------|---------|
| **Edward Hu** (@edwardjhu) | Inventeur de LoRA, PhD sous Yoshua Bengio (Mila) | x.com/edwardjhu, edwardjhu.com |
| **Tim Dettmers** (@Tim_Dettmers) | Créateur QLoRA & bitsandbytes, CMU/AI2 | x.com/Tim_Dettmers, timdettmers.com |
| **Sebastian Raschka** (@rasbt) | "Build a Large Language Model (From Scratch)", Lightning AI | x.com/rasbt, sebastianraschka.com, magazine.sebastianraschka.com |
| **Maxime Labonne** (@maximelabonne) | LLM Course (70K+ stars), Head of Post-Training Liquid AI | x.com/maximelabonne, mlabonne.github.io/blog |
| **Daniel Han** (@danielhanchen) | CEO Unsloth AI (YC S24), 2-30x faster fine-tuning | x.com/danielhanchen, unsloth.ai |
| **Georgi Gerganov** (@ggerganov) | Créateur llama.cpp & GGUF, acquis par HuggingFace (fév 2026) | x.com/ggerganov, github.com/ggml-org/llama.cpp |
| **Tri Dao** | FlashAttention (1→4), Chief Scientist Together AI | tridao.me |
| **Nathan Lambert** (@natolambert) | Post-Training Lead AI2, auteur du premier textbook RLHF | x.com/natolambert, interconnects.ai |
| **Wing Lian** (@winglian) | Créateur Axolotl, framework fine-tuning le plus complet | x.com/winglian, github.com/axolotl-ai-cloud/axolotl |
| **Philipp Schmid** (@_philschmid) | Ex-HuggingFace → Google DeepMind, guides fine-tuning référence | x.com/_philschmid, philschmid.de |
| **Song Han** (@songhan_mit) | AWQ (MLSys Best Paper), MIT Han Lab, TinyML | x.com/songhan_mit, hanlab.mit.edu |
| **Teknium** (@Teknium1) | Nous Research, Hermes models, communauté fine-tuning open-source | x.com/Teknium1 |
| **Hamel Husain** (@HamelHusain) | Mastering LLMs course, Parlance Labs | x.com/HamelHusain, maven.com/parlance-labs/fine-tuning |
| **Yaowei Zheng (hiyouga)** | LlamaFactory (65K+ stars), ByteDance | github.com/hiyouga/LLaMA-Factory |
| **Arthur Mensch** | CEO Mistral AI, champion open-source AI sovereignty | mistral.ai |
| **Liang Wenfeng** | Fondateur DeepSeek, GRPO, modèles open-source frontier à coût minimal | deepseek.com |

## Queries à exécuter

### Agent A — Leaders (queries 1-10)

```
Edward Hu LoRA new research
Tim Dettmers QLoRA bitsandbytes SERA
Sebastian Raschka LLM fine-tuning
Maxime Labonne LLM course fine-tuning
Daniel Han Unsloth AI update
Georgi Gerganov llama.cpp GGUF
Tri Dao FlashAttention update
Nathan Lambert RLHF post-training
Wing Lian Axolotl fine-tuning
Philipp Schmid fine-tuning tutorial
```

### Agent B — Techniques + Benchmarks (queries 11-20)

```
Song Han AWQ quantization MIT
Teknium Nous Research Hermes
Hamel Husain Mastering LLMs
LlamaFactory hiyouga update
Mistral AI Arthur Mensch open-source
DeepSeek Liang Wenfeng new model
Unsloth vs Axolotl vs LlamaFactory benchmark
best open source model fine-tuning
LoRA QLoRA DoRA ORPO DPO GRPO new technique
vLLM SGLang llama.cpp inference benchmark
```

## Capitalisation vault

Nouvelles techniques → `04-Techniques/`
Nouveaux modèles open-source → `03-Modeles/<provider>/`
