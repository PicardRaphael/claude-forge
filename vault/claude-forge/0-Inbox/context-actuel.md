---
titre: Context Actuel
resume: "Working memory dynamique — mis à jour par /done, lu par /recap. Session 2026-05-23 (tour 3) : audit thématique 03-RAG vault (45 corrections sur 12 notes RAG + 3 squelettes enrichis + 2 fiches leaders Jerry Liu/Harrison Chase + capitalisation 11 erreurs)."
aliases:
  - "context actuel"
  - "contexte courant"
  - "working memory"
  - "memoire de travail"
  - "etat actuel"
type: context
status: active
derniere-maj: 2026-05-23
auteur: claude
tags:
  - "#type/context"
  - "#meta/working-memory"
---

## Phase actuelle

Audits thématiques vault forge en cours (méthode A→B→C→D→E + propagation F) — 02 prompt engineering ✅, 03 RAG ✅, 06 patterns/context/stacks ✅. Reste : 04 agents-ia, 05 fine-tuning, 07 leaders-modeles-industrie.

## Dernière session (2026-05-23 — tour 3, audit RAG)

### Décisions prises
- **Méthode audit full 6 étapes appliquée** sur RAG (78 claims, 11 ❌ + 34 ⚠️ = 45 corrections en 1 session)
- **2 vagues de 3 sub-agents** (vs 6 simultanés) — recommandation advisor validée pattern réutilisable
- **Note erreurs synthétique unique** (vs 5 fragmentées) pour les 11 FAUX RAG
- **Pré-vérification arXiv IDs avant sub-agents** = pattern validé (économise tokens)
- **Ownership cross-cluster** (C2.6 Anthropic propriétaire Cluster 2, autres reprennent verdict) = pattern validé

### En cours
- Commits poussés : `c8382de` (audit RAG 14 fichiers) + `e4abf66` (post-audit : 2 fiches leaders + erreurs synthétique)
- Mémoire enrichie : 2 nouveaux feedbacks (`arxiv_id_yymm_format`, `arxiv_url_swap_papers_similaires`)
- Vault : 12 notes RAG corrigées, 3 squelettes enrichis (rag-evaluation, rag-production, ColPali), 2 leaders ajoutés

### Corrections critiques RAG (11 FAUX)
- TOOLQP date 2025→2026 (arXiv 2601.07782)
- URL MCP-Zero 2603.13426→2506.01056 (double swap avec OATS)
- Gemini 1.5 Pro NIAH multi-fact >99.7% (pas ~60% qui est GPT-4 Turbo)
- Karpathy "alternative au RAG" → verbatim canonique
- Cache cosine 0.95→0.80 (seuil inversé)
- Tableau benchmark reranking C4.2 (12 chiffres non traçables)
- 4 chiffres fantômes retirés (73% retrieval, 65%/85-90%, 70% pgvector, 73% enterprises)

### Prochaines étapes
- **Audit thème 04 (agents-ia)** — 10+ notes
- **Audit thème 05 (fine-tuning)** — 15+ notes
- **Audit thème 07 (leaders, modèles, industrie)** — ~80 notes (le plus gros, dernière étape)

## Fils ouverts

- **Pattern récidiviste paraphrase verbatim** : Karpathy "alternative au RAG" = Xe occurrence. Méthode self-verify phase E + WebFetch direct fonctionne pour mitigation.
- **6 patterns récurrents identifiés** dans `erreur-audit-rag-11-faux-2026-05-23` : arXiv YYMM, URL swap, paraphrase, inversion modèle, seuil inversé, chiffres fantômes. À surveiller en audits 04/05/07.
- **Notes ToolRerank top-50 dégrade** marqué "à sourcer dans tables paper" — à vérifier en lisant PDF complet si occasion.
- **Self-RAG et CRAG chiffres** également marqués "à vérifier tables PDF" pour cohérence verbatim.

## Liens

- [[Raphael-Picard]]
- [[Claude-Forge]]
- [[methode-analyser-repo]]
- [[feedback_audit_thematique_methode]]
- [[feedback_arxiv_id_yymm_format]]
- [[feedback_arxiv_url_swap_papers_similaires]]
- [[erreur-audit-rag-11-faux-2026-05-23]]
- [[RAG]]
- [[Jerry Liu]]
- [[Harrison Chase]]
