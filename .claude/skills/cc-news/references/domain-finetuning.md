# Domaine — Fine-tuning, Local AI & Quantization

Couvre : LoRA, QLoRA, GGUF, fine-tuning frameworks, quantization, post-training, local inference.
Nombre de queries : 20 — **Découper sur 2 agents** (Agent A + Agent B)

<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->

## Leaders canonisés (15) — vault 05-Leaders/fine-tuning/

| Personne | Rôle | Sources |
|----------|------|---------|
| **Daniel Han** (@danielhanchen) | CEO Unsloth AI | unsloth.ai, github.com |
| **Edward Hu** (@edwardjhu) | Founder Compute Exchange (stealth) — ex-PhD Mila | edwardjhu.com, arxiv.org |
| **Georgi Gerganov** (@ggerganov) | Software Engineer / Creator llama.cpp | en.wikipedia.org, github.com |
| **Hamel Husain** (@HamelHusain) | Founder Parlance Labs | maven.com |
| **Maxime Labonne** (@maximelabonne) | Staff ML Scientist / Head of Post-Training, Liquid AI | github.com, mlabonne.github.io |
| **Nathan Lambert** (@natolambert) | Senior Research Scientist / Post-Training Lead, AI2 | www.interconnects.ai |
| **Philipp Schmid** (@_philschmid) | Google DeepMind (ex-HuggingFace Technical Lead) | www.philschmid.de |
| **Rafael Rafailov** | PhD Researcher | arxiv.org, cs.stanford.edu |
| **Sebastian Raschka** (@rasbt) | LLM Research Engineer Lightning AI / Prof UW-Madison | sebastianraschka.com, magazine.sebastianraschka.com |
| **Song Han** (@songhan_mit) | Associate Professor MIT EECS | hanlab.mit.edu |
| **Teknium** (@Teknium1) | Co-founder & Head of Post-Training, Nous Research | x.com, nousresearch.com |
| **Tim Dettmers** (@Tim_Dettmers) | Assistant Professor CMU / Research Scientist AI2 | timdettmers.com, github.com |
| **Tri Dao** | Chief Scientist, Together AI | tridao.me, tridao.me |
| **Wing Lian** (@winglian) | Creator Axolotl | github.com |
| **Yaowei Zheng (hiyouga)** | Creator LLaMA-Factory / ByteDance | github.com |

> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer la fiche dans `05-Leaders/fine-tuning/` puis relancer `py scripts/sync-leaders.py`.
> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.

<!-- SYNC:leaders:end -->

## Watchlist signaux non canonisés

> Cibles suivies par cc-news mais fichées dans un autre domaine vault. Section éditable à la main, **jamais touchée par le sync**.

| Personne | Rôle | Sources |
|----------|------|---------|
| **Arthur Mensch** | CEO Mistral AI, champion open-source AI sovereignty (fiche vault en `industrie/`) | mistral.ai |
| **Liang Wenfeng** | Fondateur DeepSeek, GRPO, modèles open-source frontier à coût minimal (fiche vault en `industrie/`) | deepseek.com |

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
