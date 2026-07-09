---
name: veille-outils-ia
description: ALWAYS invoke to refresh the market AI-tools landscape notes — re-verifies volatile facts (pricing, stars, valuations, M&A) at primary source, updates vault under human gate. NOT for Claude Code news (cc-news) or picking a tool (choix-outils-ia).
user-invocable: true
allowed-tools: WebSearch, WebFetch, Read, Skill, mcp__forge-brain__*
argument-hint: "catégorie (voix | briques | code | memoire-rag | infra | tout) ou note précise"
---

# veille-outils-ia — refresh des notes-paysage marché

Veille CIBLÉE sur les **outils IA du marché** : re-vérifie les **faits volatils** à la source primaire, détecte les écarts vs vault, met à jour les notes-paysage + CHANGELOG **sous gate humain par item**.

**Frontière (≠ cc-news)** : `cc-news` surveille Claude Code, modèles frontières, techniques, leaders (capitalise dans `01-Claude`/`<NN>-<Fournisseur>/models`/`04-Techniques`/`05-Leaders`). `veille-outils-ia` ne touche QUE les notes-paysage build-vs-buy ci-dessous. `choix-outils-ia` consomme ces notes pour recommander ; cette skill les maintient à jour.

## Périmètre — les notes maintenues

| Note (stem) | Faits volatils à re-vérifier |
|---|---|
| `outils-voix-ia-build-vs-buy` | pricing TTS/STT/agents, latences, WER, licences, morts (PlayHT) |
| `briques-produit-ia-build-vs-buy` | pricing OCR/embeddings/rerank/RAG-aaS, ⭐ GitHub OSS, free tiers |
| `intelligence-de-code-build-vs-buy` | ⭐ GitHub (CodeGraph, Serena, GitNexus…), pricing reviewers, licences, archivages |
| `outils-memoire-rag-gouvernance-juin-2026` + ses notes filles | versions (mem0 v3, Onyx v4), pricing Pinecone, statuts |
| `MOC-paysage-outils-ia-marche-2026` | M&A (Portkey→Palo Alto, Lakera→Cisco), morts (Humanloop, Predibase), nouveaux leaders |
| `economie-agentique-pricing-2026` | pricing à l'outcome (Fin, HubSpot), parts de marché Menlo |

Le `$ARGUMENTS` route vers une catégorie (voix / briques / code / memoire-rag / infra / tout) ou une note précise.

## Étapes

1. **Lire la note vault cible EN ENTIER** (`mcp__forge-brain__read_note` sans `max_lines`) — pour connaître l'état actuel ET la légende de provenance (`[v]` vérifié-source / `[r]` rapporté). Relever sa `derniere-maj`.
2. **Re-vérifier chaque fait volatil à la SOURCE PRIMAIRE** : page de pricing officielle (WebFetch ; `defuddle` pour le markdown propre, mais WebFetch direct sur `.md`/JSON), GitHub API pour les ⭐, communiqués pour M&A. **Ne jamais patcher un chiffre depuis un résultat de recherche secondaire** — les agents hallucinent les chiffres précis (cf `feedback_llm_deep_research_version_numbers`). Pour X/Twitter → `Skill(x-read)`.
3. **Détecter les écarts** : valeur vault vs valeur source. Classer : `CONFIRMÉ` (inchangé) / `DÉRIVÉ` (chiffre/version changé) / `MORT` (outil disparu/racheté) / `NOUVEAU` (acteur à ajouter).
4. **Présenter le diff par item** (gate humain) : pour chaque écart, montrer `champ + ancienne valeur → nouvelle valeur + source primaire (URL + date d'accès)` puis `[v]alider / [m]odifier / [i]gnorer`. Jamais d'écriture en bloc.
5. **Mettre à jour les notes** (après validation) via MCP `update_note` / `insert_section` / `update_property` — jamais Edit disque direct (désynchronise l'index SQLite). Conserver/mettre à jour la légende de provenance (`[v]` pour ce qu'on vient de vérifier à la source). Mettre à jour `derniere-maj` à la date du jour.
6. **CHANGELOG vault obligatoire** : mettre à jour `vault/claude-forge/CHANGELOG.md` AVANT le commit (rule `.claude/rules/changelog-vault.md`) — section « Modifiées » + « Source ».
7. **Signaler les impacts** : si un outil mort/renommé est cité dans une skill (`choix-outils-ia`, ses references) → le signaler à l'utilisateur (gate humain, ne pas modifier la skill directement — délégation `skill-creator`).

## Gotchas

- **Source primaire OBLIGATOIRE pour tout chiffre** : pricing, ⭐, valo, WER, latence. Un fait qualitatif (« X est le leader FR ») peut rester vrai même si son chiffre est faux — mais on ne patche un chiffre que vérifié à la source, avec URL + date d'accès.
- **Gate humain par item, jamais en bloc** : une veille touche des notes que `choix-outils-ia` lit pour conseiller des clients — une fausse MAJ se propage. Diff visible, validation item par item (cf pattern « skill qui propose un diff à valider »).
- **MCP pour écrire le vault, jamais Edit disque** : l'Edit direct désynchronise l'index SQLite (réindex au poll 30s). `update_note`/`insert_section`/`update_property`.
- **Légende de provenance** : ces notes distinguent `[v]` vérifié-source de `[r]` rapporté. Toujours préserver/mettre à jour ce marquage — ne pas dégrader un `[r]` en fait nu.
- **≠ cc-news** : ne pas re-scanner Claude Code / modèles / leaders ici. Si le besoin déborde (nouvelle technique, nouveau modèle) → renvoyer `cc-news`.
- **Morts à surveiller** : PlayHT, Humanloop, Predibase, Bloop, code-graph-rag-mcp (archivés). Vérifier qu'aucun n'est encore recommandé.
- **EU AI Act 2 août 2026** : échéance qui peut basculer des verdicts (disclosure voix) — la re-vérifier comme un fait daté.

## Apprentissage

Après chaque veille : noter quelles notes dérivent le plus vite (pricing voix, ⭐ code) pour calibrer la cadence de refresh, et tout nouvel acteur/mort détecté pour enrichir `choix-outils-ia`.
