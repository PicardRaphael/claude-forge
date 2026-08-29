---
name: choix-outils-ia
description: ALWAYS invoke to choose an AI tool or decide build-vs-buy — voice/TTS/OCR, transcription, embeddings/reranking, AI in production. Returns verdict + tools + pricing + license traps. NOT for RAG design (rag-design) or CODIR strategy (responsable-ia).
user-invocable: true
allowed-tools: Read, Glob, Grep, mcp__forge-brain__search_brain, mcp__forge-brain__read_note, mcp__forge-brain__read_note_by_path, mcp__forge-brain__read_section, mcp__forge-brain__list_notes
---

# choix-outils-ia — build-vs-buy de tout outil IA

Sur un besoin en langage naturel, tu **dialogues** (cadrage) → **consultes le vault AVANT de proposer** → rends un verdict **build-vs-buy + outil(s) recommandé(s) + pricing repère + pièges de licence**. Échange avec Raphael, look le vault, ne balance pas une reco générique.

**Frontière** : ici = acte OPÉRATIONNEL outillé (« quel outil concret, build ou buy »). `responsable-ia` = build-vs-buy au niveau DÉCISION stratégique (CODIR, ADR, matrice). `rag-design` = conception technique d'un RAG. Si la demande est « faut-il investir dans l'IA » → renvoyer responsable-ia.

## Principe transversal (à dire d'emblée)

**Buy/intégrer gagne quasi partout** : ces briques sont des **commodités**, pas le différenciateur. Le moat reste les **données métier + evals propriétaires** (76% des solutions IA entreprise achetées en 2025, Menlo). Le « build » ne se justifie que sur : briques où le self-host bat l'API au volume/souveraineté (STT, embeddings, RAG), apps spécifiques, orgs à forte compétence infra (cf Ramp). Détail économie → `mcp__forge-brain__read_note("economie-agentique-pricing-2026")`.

## Étape 1 — Cadrer (dialogue, ne pas sauter)

Identifier la **catégorie** du besoin et poser les questions de cadrage manquantes (AskUserQuestion, batché ≤4). Questions pivots :
- **Usage interne ou revendu au client** (produit SaaS) ? — décale souvent le verdict vers build (marge, PII, conformité).
- **Volume** attendu (le seuil build-vs-buy se joue au volume sur STT/embeddings/agents vocaux).
- **Souveraineté / RGPD / hébergement FR** requis ? — pousse vers OSS self-host.
- **Stack existant** (déjà GCP/Azure/Postgres/LangChain ? un siège LLM en place ?).
- **POC ou production** ? — managé pour valider, build à l'échelle.

## Étape 2 — Consulter le vault (AVANT de proposer)

Lire la note-paysage pertinente EN ENTIER selon la catégorie (le détail — pricing chiffré, licences, morts — y vit, marqué vérifié-source vs rapporté) :

| Catégorie du besoin | Note vault à lire |
|---|---|
| Voix : TTS / STT / agents vocaux (robot tél., transcription) | `outils-voix-ia-build-vs-buy` |
| Briques produit : OCR, embeddings, reranking, modération, RAG-aaS, extraction structurée | `briques-produit-ia-build-vs-buy` |
| Intelligence de code : context engine, revue de code IA, gates qualité/sécu | `intelligence-de-code-build-vs-buy` |
| Mémoire d'agent / vector DB / RAG entreprise / gouvernance contexte | `outils-memoire-rag-gouvernance-juin-2026` |
| Productivité / infra-LLMOps / plateformes / pricing / morts du marché | `MOC-paysage-outils-ia-marche-2026` + `economie-agentique-pricing-2026` |

Si la catégorie est ambiguë → partir du `MOC-paysage-outils-ia-marche-2026` (cartographie 5+1 catégories). Tables de verdict denses embarquées dans `references/verdicts-par-categorie.md` pour orienter vite — mais **lire la note vault pour le pricing exact avant de recommander** (les chiffres datent vite, cf veille-outils-ia).

## Étape 3 — Rendre le verdict

Format de sortie (copy-paste-ready) :
1. **Besoin reformulé** + catégorie.
2. **Verdict build-vs-buy** (par brique si le besoin en couvre plusieurs — la voix se tranche brique par brique : TTS=buy, STT=build viable, agents=buy-POC-puis-build).
3. **Outil(s) recommandé(s)** : 1 reco principale + 1 alternative (managé vs OSS souverain), avec **pricing repère** et **distinctif**.
4. **Pièges de licence / vendor-risk** : OSS non-commercial (XTTS/Coqui CPML, GitNexus, SocratiCode AGPL-3.0), outils morts (PlayHT, Humanloop, Bloop), M&A récents (Portkey→Palo Alto, Lakera→Cisco).
5. **Conformité** si données personnelles ou revente : EU AI Act 2 août 2026, RGPD → renvoyer `responsable-ia`.
6. **Next step** : POC managé pour valider, condition de bascule vers build.

## Ancrage Loji (deux piles de référence)

- **⚡ Buy rapide (time-to-market)** : Mistral OCR 3 → Voyage-4/Gemini embeddings → zerank-2/Voyage rerank → Ragie (RAG-aaS) → OpenAI Moderation + Llama Prompt Guard 2 → BAML (extraction).
- **🇫🇷 Souveraineté FR self-host** : Docling/Mistral OCR self-hosted → Qwen3-Embedding-8B → BGE-reranker-v2 → briques RAG maison → Llama Guard 4 + Prompt Guard 2 → BAML. Tout OSS hébergeable en France.
- Voix Loji : STT **Gladia** (#1 FR, RGPD, diarisation) ou Whisper self-host au volume · agents vocaux **Retell** pour valider, **LiveKit/Pipecat** (OSS) à l'échelle si revendu · TTS **ElevenLabs**/Google Cloud.

## Gotchas

- **Consulter le vault AVANT de proposer** — jamais une reco de tête. Les pricing/morts y sont à jour et tracés (vérifié-source vs rapporté).
- **Pricing = zone d'obsolescence** : les chiffres bougent vite. Vérifier la `derniere-maj` de la note ; si > quelques semaines ou si la reco engage un client → re-vérifier à la source (ou lancer `veille-outils-ia`). Les agents hallucinent les chiffres précis (cf `feedback_llm_deep_research_version_numbers`).
- **Pièges de licence = bloquant produit** : un OSS « gratuit » en CPML/AGPL/non-commercial peut être interdit en revente. Toujours signaler la licence pour tout outil embarqué dans Loji.
- **Trancher par brique, pas en bloc** : « je veux de la voix » ≠ un seul verdict. Décomposer TTS / STT / agent.
- **Interne vs revendu change le verdict** : revendre du managé empile les coûts → build à l'échelle pour la marge.
- **Ne pas confondre avec rag-design** : « quel vector store / RAG-aaS » = ici (choix d'outil) ; « conçois mon pipeline RAG » = rag-design.

## Apprentissage

Après chaque choix : noter le besoin + la catégorie + le verdict rendu + le déclencheur de bascule build, pour accélérer les cas similaires et repérer les notes-paysage à rafraîchir (→ veille-outils-ia).

## Références

- `references/verdicts-par-categorie.md` — tables de verdict denses (orientation rapide ; pricing exact dans les notes vault)
