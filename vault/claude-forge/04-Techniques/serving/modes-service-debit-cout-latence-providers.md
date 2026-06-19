---
titre: "Modes de service débit/coût/latence par provider — Batch, Priority/Flex/Scale, Provisioned Throughput, caching"
resume: "Comment arbitrer coût vs latence vs débit garanti par provider (OpenAI/Azure, Anthropic, Vertex/Gemini, Bedrock, vLLM self-hosted). Discriminant : chaque provider a SA propre unité de réservation (Scale units / PTU / GSU+burndown / Model Units) — ne pas les conflater"
aliases:
  - "modes de service llm providers"
  - "provisioned throughput comparaison providers"
  - "batch api priority flex scale tier"
  - "GSU PTU model units burndown"
  - "débit coût latence ia par provider"
  - "service tiers openai anthropic vertex bedrock"
domaine: ia
type: technique
derniere-maj: 2026-06-19
auteur: claude
sources:
  - "https://developers.openai.com/api/docs/guides/flex-processing"
  - "https://openai.com/api-priority-processing/"
  - "https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput/measure-provisioned-throughput"
  - "https://aws.amazon.com/bedrock/pricing/"
  - "https://www.respan.ai/articles/anthropic-message-batches-api"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/infrastructure"
---

> [!warning] Le discriminant signal/folklore
> « Batch = -50 % » est vrai partout et trivial. Le vrai sujet est le **débit garanti** : le *provisioned throughput n'est ni la même unité ni le même modèle de facturation* d'un provider à l'autre. OpenAI **Scale Tier** (throughput units, engagement ≥30j) · Azure OpenAI **PTU** · Vertex **GSU + burndown rate** · Bedrock **Model Units (MU)** · self-hosted = **GPU-heure**. Les conflater (« PTU/GSU ») est l'erreur qui fait passer la note de canonique à folklore.
>
> ⚠️ **Pricing volatil** : les chiffres ci-dessous sont datés (juin 2026) et tagués VÉRIFIÉ/RAPPORTÉ. Les noms de tiers rebrandent souvent. **Toujours revérifier en source primaire avant d'engager** (les claims chiffrés des deep-research LLM sont souvent hallucinés — feedback mémoire `llm-deep-research-version-numbers`).

## Les 4 leviers (axes orthogonaux)

1. **Async / Batch** — latence sacrifiée (≤24 h) contre **-50 %**. Levier coût n°1 pour le hors-temps-réel.
2. **Tiers temps-réel** (Flex/Priority/Standard) — curseur coût↔latence sur l'on-demand, **sans engagement**.
3. **Débit réservé** (provisioned throughput) — capacité dédiée, débit garanti, **engagement + facturation à l'heure quelle que soit l'utilisation**.
4. **Caching** — orthogonal aux 3 autres et **cumulable** (cf [[prompt-caching-kv-cache]]).

## Matrice par provider

### OpenAI (API hébergée)

Quatre service tiers via le paramètre `service_tier`, par requête (RAPPORTÉ docs + agrégateurs, juin 2026) :

| Tier | Coût vs Standard | Latence / SLA | Pour |
|---|---|---|---|
| **Standard** | base | best-effort, pas de SLA | usage général |
| **Priority** | **~2×** | la plus rapide et constante, même en pic | apps user-facing latency-critique. ❌ pas pour data-processing/evals erratiques |
| **Flex** | **-50 %** (tarif Batch) | variable, 429 possibles en pic, mais **interactif** | evals, enrichissement, async non-prod |
| **Batch** | **-50 %** | jusqu'à 24 h, asynchrone (S3-like) | gros volumes offline |
| **Scale Tier** | engagement | **throughput units réservés ≥30j, SLA uptime 99,9 %**, latence prévisible | entreprise gros volume |

> ⚠️ **GPT-5.5 gotcha (RAPPORTÉ)** : au-delà de **272 000 tokens d'entrée**, facturation **×2 input / ×1,5 output sur toute la session**, y compris Batch et Flex. Designer le contexte sous 272K peut diviser la facture par 2.

### Azure OpenAI

- Unité de réservation = **PTU (Provisioned Throughput Units)** — distincte du « Scale Tier » d'OpenAI direct. Réservation de débit dédié, facturation horaire/mensuelle, réductions sur engagement. Modèle mental ≈ Bedrock MU, **PAS** identique aux GSU Vertex (unité non comparable token-pour-token).

### Anthropic

| Levier | Détail (VÉRIFIÉ/RAPPORTÉ juin 2026) |
|---|---|
| **Message Batches API** | **-50 % input ET output**, ≤24 h, jusqu'à **100 000 requêtes/batch**, tous modèles. Les cache read/write reçoivent **aussi** le -50 % dans un batch. ❌ pas pour UX interactive/boucles d'agent |
| **Prompt caching** | write 5 min = **1,25×** base · write 1 h = **2,0×** · **read = 0,1×** (-90 %). Sweet spot : system prompt long+statique, tours user courts |
| **Priority Tier** | caps de file d'attente dépendant du tier de compte (notamment sur Batches) |
| **Stacking** | caching (-90 %) + Batch (-50 %) cumulables → **jusqu'à -95 %** |
| **Fast Mode (Opus 4.8)** | $10/$50 par MTok, **3× moins cher** que sur 4.7 ($30/$150) — latence Opus enfin viable |

### Google Vertex AI / Gemini

- Réservation = **Provisioned Throughput (PT)**, mesurée et facturée en **GSU (Generative AI Scale Unit) + burndown rate** (ratio qui convertit input/output en tokens/s — unité standard cross-modèle). Le **prix par GSU est fixe** mais le débit qu'une GSU fournit **varie selon le modèle**.
- Termes : **1 semaine / 1 mois / 3 mois / 1 an**. Capacité réservée → requêtes priorisées. **Pas de SLA de latence formel**, mais latence plus stable en pic.
- **Fenêtre dynamique** d'enforcement du quota (s'adapte aux pics) — ex. 1 GSU Gemini 2.5 Flash ≈ **2 690 tokens/s** soutenu (≤322 800 tokens / fenêtre 120 s).
- **Débordement automatique** : si une requête dépasse le quota PT estimé, elle bascule en **pay-as-you-go** au lieu d'échouer.
- Prix RAPPORTÉ : **$42 → $158 / GSU-heure** selon modèle/région.
- ⚠️ **Gotcha contre-intuitif** : sur Gemini 2.0 Flash, 1 GSU à $42/h vs ~$4,96/h en on-demand pour le même débit → **PT ≈ 8× plus cher** sauf si l'utilisation approche **100 % du plancher**. Le provisioned n'est rentable qu'à **saturation soutenue**, jamais pour du trafic en dents de scie.
- Context caching : **implicite** (discount auto sur cache hit) + **explicite** (contrôle + discount garanti). Cf [[architecture-gemini-api]].
- PT supporte désormais **Gemini 3 + Live API** (streaming multimodal). Estimateur GSU fourni par Google.

### AWS Bedrock

| Mode | Détail (VÉRIFIÉ/RAPPORTÉ juin 2026) |
|---|---|
| **On-demand** | pay-per-token, le plus flexible |
| **Batch Inference** | **-50 %** on-demand (Anthropic/Meta/Mistral/Amazon ; ❌ DeepSeek exclu), ≤24 h via S3 |
| **Flex** | **-50 %** (per AWS pricing page) |
| **Priority** | **+75 % premium** sur Standard |
| **Provisioned Throughput** | réservation en **Model Units (MU)**, **facturation horaire quelle que soit l'utilisation**, engagement 1 ou 6 mois (sans commit = 1 MU au tarif horaire). Réductions **15–40 %** sur engagement. Ex. officiel : 1 MU × $21,18 × 24h × 31j = **$15 757,92/mois** |
| **Prompt caching** | jusqu'à -90 % sur l'input caché |

### Self-hosted (vLLM / SGLang)

- Pas de « tier » : le débit garanti = **dimensionnement GPU + serving engine**. L'unité de coût est la **GPU-heure**, pas un token managé.
- Leviers de débit : continuous batching, PagedAttention/RadixAttention, quantification FP8/AWQ, désagrégation prefill/decode. Détail complet : [[serving-inference-optimisation]] + [[reference-technique-stack-ia]] §2.
- Build-vs-buy : rentable seulement à **volume soutenu très élevé** (l'équivalent du « 100 % du plancher » Vertex, mais que tu opères toi-même). Sinon l'API managée gagne. Cf [[fine-tuning-infrastructure]] (provisioned throughput GPU) + [[briques-produit-ia-build-vs-buy]].

## Arbre de décision

```
Temps réel requis ?
├── NON  → Batch API (-50 % partout). Cumuler avec caching → jusqu'à -95 % (Anthropic).
└── OUI
     ├── Volume faible/erratique → On-demand Standard + prompt caching (toujours).
     ├── Latence critique user-facing → Priority (OpenAI ~2× / Bedrock +75 %) ; Anthropic Fast Mode.
     └── Volume ÉLEVÉ et SOUTENU (≈ saturation continue)
          → Débit réservé : OpenAI Scale / Azure PTU / Vertex GSU / Bedrock MU.
          ⚠️ Ne réserver QUE si utilisation ≈ plancher 24/7. Sinon on-demand reste moins cher
             (cf gotcha Vertex 8×). Self-host seulement à volume extrême maîtrisé en interne.
```

## Liens

- [[reference-technique-stack-ia]] — référence longue (§1 caching, §2 serving)
- [[prompt-caching-kv-cache]] — levier caching détaillé (cumulable avec tous les modes)
- [[parametres-echantillonnage-llm]] — l'autre delta NEUF : réglages de sampling par cas d'usage
- [[serving-inference-optimisation]] — débit self-hosted (vLLM/SGLang, quantif, P/D)
- [[fine-tuning-infrastructure]] — provisioned throughput GPU + cloud providers
- [[architecture-openai-api]] · [[architecture-gemini-api]] — optimisations par provider
- [[briques-produit-ia-build-vs-buy]] — arbitrage build-vs-buy
- [[index-architectures]] — optimisations transversales coût
