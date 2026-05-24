---
titre: "Erreur — Audit RAG 23 mai 2026, 11 claims FAUX sur 78"
resume: "Synthèse des 11 erreurs Type 1/2/3 détectées dans le vault RAG (14 notes, 78 claims) : 5 critiques fort impact, patterns récurrents (arXiv ID format, URL swap, paraphrase Karpathy, inversion modèle, seuil cache inversé, chiffres fantômes)."
aliases:
  - "erreur audit RAG 23 mai"
  - "11 claims faux RAG"
  - "erreurs vault RAG"
  - "audit thematique 03-rag erreurs"
  - "patterns erreurs audit"
type: erreur
domaine: ia
derniere-maj: 2026-05-24
auteur: claude
sources:
  - "output/audit-rag/A-inventaire-claims (artefact audit, hors vault)"
  - "output/audit-rag/D-synthese-croisement (artefact audit, hors vault)"
  - "output/audit-rag/F-rapport-final (artefact audit, hors vault)"
tags:
  - "#type/erreur"
  - "#domaine/rag"
  - "#sujet/audit-thematique"
---

## Contexte

Audit thématique RAG vault forge-brain (14 notes `04-Techniques/rag/*` + `rag-vs-fine-tuning`) le 23 mai 2026, méthode validée audit Claude Code (95 claims, 22 erreurs). Sur ~78 claims auditées, **11 erreurs ❌ détectées + 34 ⚠️ à nuancer = 45 corrections**.

## Les 11 FAUX par type

### Type 1 — Source/attribution fausse (7)

1. **TOOLQP date 2025 → 2026** — paper arXiv 2601.07782 = janvier 2026 (format YYMM)
2. **URL MCP-Zero 2603.13426 → 2506.01056** — swap avec OATS
3. **Gemini 1.5 Pro NIAH multi-fact ~60%** — c'est GPT-4 Turbo ; Gemini >99.7%
4. **Karpathy "alternative au RAG"** — paraphrase déformante, verbatim = "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase"
5. **Cache sémantique cosine >0.95** — seuil inversé, optimal = 0.80 (arXiv 2411.05276)
6. **RAFT affiliations Berkeley/Microsoft/Meta** — paper = 100% UC Berkeley ; MS/Meta = contributeurs blog seuls
7. **H-RAG nDCG@5 0.4728 → 0.4271** — erreur chiffre

### Type 2 — Chiffres approximés (1 majeur)

8. **C2.5 Late Chunking 0.8516/0.8590 inversés** — Late Chunking = 0.8516, Contextual Embedding Anthropic = 0.8590

### Type 3 — Chiffres fantômes / doctrine fausse (3)

9. **"73% retrieval"** — circulant sans source primaire identifiable
10. **"Naive 65% / Advanced 85-90%"** — pourcentages absolus non sourcés
11. **"pgvector 70% workloads IA-agent"** + **"73% enterprises hot/warm/cold"** + **tableau benchmark reranking C4.2 (12 chiffres)** — fantômes

## Patterns récurrents identifiés

### Pattern 1 — arXiv ID format YYMM
ID `YYMM.NNNNN` : si mois cité dans note ≠ MM de l'ID → red flag. Vérification mécanique systématique.

### Pattern 2 — URL swap entre papers du même domaine
2 papers similaires (OATS + Semantic Tool Discovery, OATS + MCP-Zero) = URLs facilement confondues. WebFetch SYSTÉMATIQUE quand N URLs arXiv du même domaine côte-à-côte.

### Pattern 3 — Paraphrase de citation (Xe occurrence)
Karpathy "alternative au RAG" = paraphrase déformante d'une distinction philosophique (wiki cumulatif vs RAG stateless). Pattern documenté audit Claude Code 23 mai (Justin Young split, Willison lethal trifecta, etc.) [[feedback_tweet_hype_paraphrase_pattern]].

### Pattern 4 — Inversion modèle dans benchmarks comparatifs
Gemini 1.5 Pro / GPT-4 Turbo NIAH multi-fact : chiffre du concurrent attribué au modèle principal. Relire 2x les attributions modèle dans tables comparatives.

### Pattern 5 — Seuils inversés (cache cosine 0.95 vs 0.80)
Cosine élevé = strict = hit rate faible. Cosine bas = permissif = hit rate élevé. Confusion direction-effet courante. Vérifier sens des seuils.

### Pattern 6 — Chiffres trop précis = signal fabrication
"73%", "70%", "60%", "73%" — chiffres précis sans source = haute probabilité fabrication. Tableaux comparatifs avec latences/prix précis (C4.2 : 5 lignes toutes inventées) = à vérifier ligne par ligne.

## Conséquences

Si non corrigées, ces 11 erreurs auraient :
- Été propagées en contexte formel (présentations, partage externe)
- Crédibilisé des chiffres marketing non sourcés
- Inversé des recommandations opérationnelles (cache cosine, modèle long-context recommandé)
- Mal attribué la paternité de papers (RAFT, RAPTOR)
- Cassé des URLs de référence (MCP-Zero, OATS)

## Quoi faire à la place

1. **WebFetch verbatim** sur claims fort impact AVANT capitalisation
2. **arXiv ID YYMM check** automatique à chaque citation paper
3. **Source primaire** ou 4+ sources convergentes (cf [[feedback_anthropic_single_source]] [[feedback_regle_scope_pas_universelle]])
4. **Chiffres trop précis sans source** = retirer ou marquer [SOURCE MANQUANTE]
5. **Tableaux comparatifs** = vérifier ligne par ligne, pas accepter le bloc

## Liens

- A-inventaire-claims — inventaire 78 claims dédupliquées (artefact audit `output/`, hors vault)
- D-synthese-croisement — classification Type 1/2/3 complète (artefact audit `output/`, hors vault)
- F-rapport-final — rapport final audit (artefact audit `output/`, hors vault)
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — audit précédent (Claude Code)
- [[feedback_tweet_hype_paraphrase_pattern]] — pattern paraphrase Karpathy récurrent
- [[feedback_audit_thematique_methode]] — méthode 6 étapes validée
- [[feedback_arxiv_id_yymm_format]] — pattern arXiv ID
- [[feedback_arxiv_url_swap_papers_similaires]] — pattern URL swap
- [[pattern-vault-llm-karpathy]] — verbatim canonique Karpathy
