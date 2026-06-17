---
titre: "Outils IA vocaux (TTS / STT / agents vocaux) — Paysage build-vs-buy juin 2026"
resume: "Paysage des outils voix IA pour entreprise : TTS (ElevenLabs/Cartesia/Google/Chatterbox), STT (Gladia/Deepgram/Whisper), agents vocaux temps réel (Retell/Vapi/LiveKit/Pipecat). Build-vs-buy tranché PAR brique : TTS=buy, STT=build viable, agents=buy-POC-puis-build."
aliases:
  - "outils voix IA"
  - "TTS STT agents vocaux"
  - "text-to-speech speech-to-text"
  - "robot vocal téléphonique IA"
  - "synthèse vocale entreprise"
  - "ElevenLabs Deepgram Vapi"
domaine: ia
type: technique
derniere-maj: 2026-06-17
auteur: claude
sources:
  - "https://elevenlabs.io/pricing"
  - "https://cartesia.ai/pricing"
  - "https://deepgram.com/pricing"
  - "https://gladia.io/pricing"
  - "https://retellai.com/pricing"
  - "https://github.com/livekit/agents"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/voix"
---

## Description

Paysage des briques voix IA pour une entreprise — usage interne (support, répondeur, transcription réunions) OU revente de la voix aux clients (produit SaaS). Légende : `[v]` = chiffre lu sur page officielle (vérifié juin 2026) · `[r]` = source tierce (page officielle JS-walled, défunte ou timeout).

> [!tip] Le build-vs-buy se tranche DIFFÉREMMENT par brique
> | Brique | Verdict | Pourquoi |
> |---|---|---|
> | **TTS** (synthèse) | ✅ **BUY** | Reconstruire une voix multilingue FR + clonage + 48 kHz = plusieurs FTE ML. L'OSS commercial-OK ne rivalise pas sur le FR conversationnel premium. |
> | **STT** (transcription) | ❌ **BUILD viable** | Whisper (Apache-2.0) = le **même modèle** que beaucoup d'API. Au-delà de ~centaines d'h/mois ou sous RGPD, self-host (faster-whisper) bat l'API. L'API gagne sur faible volume + diarisation clé en main + SLA. |
> | **Agents vocaux** (robot tél.) | 🔶 **BUY pour POC, BUILD à l'échelle** | Managé (Vapi/Retell) pour valider <~10K min/mois ; bascule LiveKit/Pipecat (OSS) dès que volume/marge/conformité comptent — surtout pour un produit revendu. |

## TTS (synthèse vocale)

| Outil | Pricing repère | Latence | FR | OSS / Licence | Verdict |
|---|---|---|---|---|---|
| **ElevenLabs** | 99$/mo (600k crédits) `[v]` | ~75 ms (Flash) `[v]` | Excellent | Non | **BUY** premium client-facing |
| **Cartesia** (Sonic) | Pro 5$, agents 0,06$/min `[v]` | sub-90 ms `[v]` | Oui (42 langues) | Non | **BUY** temps réel |
| **Hume** (Octave/EVI) | 70$/mo (1M), 0,05-0,15$/1k `[v]` | EVI3 <300 ms `[r]` | Oui (11 langues) | Non | **BUY** émotion — ⚠️ vendor-risk |
| **OpenAI** | tts-1 15$ / hd 30$ /1M chars `[v]` | ~300-600 ms `[r]` | Oui mais EN-optimisé | Non | **BUY** si déjà GPT |
| **Google Cloud** | Standard 4$ / Chirp HD 30$ /1M `[v]` | n/a | **Fort (~42 fr-FR)** `[v]` | Non | **BUY** moins cher + free tier |
| **Azure** | ~15$ / ~22$ HD /1M `[r]` | ~400-800 ms `[r]` | Fort (~31 fr) `[v]` | Non | **BUY** conformité/souverain |
| **Kokoro** (82M) | gratuit | RTF 2-10× CPU `[r]` | 1 voix maigre | **Apache-2.0** ✅ | **SELF-HOST** EN/batch |
| **Chatterbox** (Resemble) | gratuit (GPU) | sub-200 ms (claim) | Oui (v3, 23 langues) + clone | **MIT** ✅ | **SELF-HOST** meilleur fit OSS commercial |
| **Piper** | gratuit (CPU/RPi) | temps réel CPU | Oui (6 voix) | **GPL-3.0** ⚠️ | **SELF-HOST** edge/offline |
| **XTTS-v2 / Coqui** | gratuit | <200 ms GPU `[v]` | Oui + clone | **CPML non-commercial** ⚠️ | **ÉVITER** en commercial |
| **PlayHT** | défunt | — | (mort) | — | **MORT** |

## STT (transcription)

| Outil | Pricing PAYG | WER (Earnings22) | FR | Diarisation | OSS | Verdict |
|---|---|---|---|---|---|---|
| **Gladia (Solaria-3)** 🇫🇷 | async $0,20-0,61/h `[v]` | **6,4 % (#1, auto-bench)** | **#1 FR** | Incluse gratuite `[v]` | Non | **BUY recommandé Loji FR** |
| **Deepgram Nova-3** | streaming $0,0048/min `[v]` | 5,26 % batch (vendor) | Multilingue | Incluse | Non | **BUY** streaming/voice agents |
| **AssemblyAI** | async $0,15-0,21/h `[v]` | 6,9 % | Multilingue | Add-on `[v]` | Non | **BUY** si Audio Intelligence |
| **Speechmatics** | Pro dès $0,24/h `[v]` | 7,8 % | FR (49 langues) | n/a | Non (on-prem) | **BUY** si on-prem/régulé |
| **OpenAI gpt-4o-transcribe** | $0,006/min `[v]` | ~5-6 % EN | Bon | Non native | Modèle=OSS | **BUY** faible volume, sinon BUILD |
| **Whisper OSS (large-v3)** | gratuit (GPU ~$0,05-0,15/h) | 2,8 % LibriSpeech | Bon | +pyannote | **Apache-2.0** | **BUILD** volume/privacy |
| **faster-whisper / whisper.cpp** | gratuit | = Whisper | Bon | +pyannote | **MIT** | runtime du BUILD |

## Agents vocaux temps réel (robot téléphonique)

| Outil | $/min réel | Latence v2v | Téléphonie | OSS | Verdict |
|---|---|---|---|---|---|
| **Retell AI** | ~$0,13 ($0,07-0,31) `[v]` | cascade | Twilio inclus | Non | **BUY** transparent (production) |
| **Vapi** | $0,13-0,31+ (plateforme $0,05) `[v]` | ~1-1,7s cascade `[r]` | Twilio + numéros | Non | **BUY** flexible (orchestration) |
| **Bland AI** | $0,11-0,14 `[v]` | low-latency | inclus + BYOT | Non | **BUY** mono-stack (outbound) |
| **LiveKit Agents** | ~$0,0735 Cloud / framework gratuit `[v]` | transport <100 ms | SIP natif | **Apache-2.0** | **BUILD de référence** |
| **Pipecat** (Daily) | gratuit + briques | dépend stack | Twilio + 5 serializers | **BSD-2** | **BUILD pur OSS** |
| **OpenAI Realtime** | ~$0,30/min équiv. (audio out $64/1M) `[v]` | **320-800 ms** `[v]` | aucune (brique) | Non | brique speech-to-speech |
| **ElevenLabs Agents** | $0,08/min `[v]` + LLM | TTS <100 ms | inclus | Non | **BUY** qualité voix FR |

> **Architecture clé** : pipeline cascade STT→LLM→TTS (latence ~1,4-1,7s, ~$6K/100K min) vs speech-to-speech natif OpenAI Realtime (latence 320-800 ms, ~$30K/100K min soit ~5×). Le levier #1 de latence = time-to-first-token du LLM, pas le transport.

## Recommandations Loji

**Cas A — usage interne** : STT **Gladia** (FR/RGPD/diarisation) ou Whisper self-host si volume · Agents **Retell** pour valider · TTS **Google Cloud** ou ElevenLabs si qualité prime.

**Cas B — proposer la voix aux clients (SaaS)** : **builder** la couche agent sur **LiveKit Agents** (Apache-2.0) ou **Pipecat** (BSD-2) dès qu'on dépasse le POC — pour la marge (revendre du managé empile les coûts), la maîtrise PII et la conformité. Brique TTS **ElevenLabs** (qualité FR), STT **Gladia** ou Deepgram.

> [!warning] Vendor-risk & EU AI Act
> - **PlayHT MORT** (acqui-hire Meta juil. 2025, éteint déc. 2025) — ne plus citer.
> - **XTTS/Coqui** : piège de licence (code MPL-2.0 mais **poids CPML non-commercial** + Coqui fermé = aucun licenceur). À éviter en commercial ; successeur actif `idiap/coqui-ai-TTS` (MPL-2.0).
> - **Hume** : deal licensing/talent avec Google DeepMind (janv. 2026) — drapeau de continuité.
> - **EU AI Act applicable 2 août 2026** `[r]` : disclosure IA en début d'appel + log d'interaction. Le **build** facilite la conformité — argument fort pour un SaaS B2B français.
> - **Gladia #1 FR** et **Deepgram WER** = auto-benchmarks → valider sur audio Loji réel avant engagement client.

## Liens

- [[outils-memoire-rag-gouvernance-juin-2026]] — hub outils mémoire/RAG/gouvernance
- [[briques-produit-ia-build-vs-buy]] — autres briques produit (OCR, embeddings, modération)
- [[economie-agentique-pricing-2026]] — économie build-vs-buy, moat data métier
- [[Arthur Mensch]] — Mistral, souveraineté IA FR
- [[MOC-Techniques]]
