---
titre: "Erreur — Audit thème 07 leaders/modèles/industrie/concurrents 23 mai 2026"
resume: "12 fabrications + 36 imprécisions détectées dans audit 98 notes (135 claims). Patterns récurrents : chiffres clients fabriqués paraphrasés comme verbatim, specs techniques inventées, drift stars/affiliations, premier-auteur confondu avec senior."
aliases:
  - "erreur audit 07 leaders"
  - "erreur audit thématique leaders modeles industrie"
  - "audit 07 2026-05-23"
type: erreur
derniere-maj: 2026-05-24
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/audit-vault"
  - "#meta/lessons-learned"
---

## Contexte

Audit thématique 07 du chantier audits vault — 6e thème consécutif après prompt-eng, RAG, agents-IA, fine-tuning, patterns/context/stacks. Scope : 98 notes (12 Claude Code + 14 agents + 9 prompt + 8 rag + 14 fine-tuning + 7 industrie leaders + 7 modèles + 5 concurrents + 7 industrie events). 135 claims auditées via 7 sub-agents parallèles par cluster + 3 self-verify WebFetch directs.

## Résultats

| Statut | Nombre | % |
|--------|--------|---|
| ✅ Canonique | 87 | 64% |
| ⚠️ Partiel / single source | 36 | 27% |
| ❌ Fabriqué / faux fort impact | 12 | 9% |

~40 notes patchées sur 98.

## Patterns d'erreur NOUVEAUX (à capitaliser)

### 1. Chiffres clients paraphrasés comme verbatim CwC London

**Cas** : fiche `cat-wu.md` contenait :
- "Mercado Libre — 23 000 ingénieurs sur Claude Code, 500k PRs reviewés, 9k apps modernisées"
- "Mercado Libre objectif 90% coding autonome Q3 2026 — Cité par Oscar Mowen"
- "Binti — 20 jours saved"

**Détection** : sub-agent cluster 4 + 2 WebFetch directs (Every podcast, anthropic.com) ont confirmé : **0 source externe accessible** mentionne ces chiffres. Aucune trace publique d'"Oscar Mowen" non plus.

**Verdict** : possiblement issus du livestream YouTube CwC London (transcription non publiée au 23 mai), mais NON sourçables actuellement. Décision : marqués ⚠️ "à confirmer livestream", pas supprimés.

**Pattern à éviter** : ne JAMAIS écrire une métrique chiffrée précise comme "verbatim source X" sans avoir le verbatim exact accessible. Si la source est un livestream non transcrit, marquer "à confirmer" dès l'écriture.

### 2. Specs techniques fabriquées (Dreaming)

**Cas** : fiche `jeremy-hadfield.md` contenait :
- Header API : `dreaming-2026-04-21`
- Limite : max 100 sessions par dream
- Modèles supportés : Opus 4.7 et Sonnet 4.6 uniquement

**Détection** : WebFetch direct `anthropic.com/news/dreaming` → **HTTP 404**. Aucune doc officielle Anthropic ne publie ces specs. Probable hallucination d'une session précédente extrapolant à partir du concept général.

**Pattern à éviter** : pour toute spec API/header/format chiffré, exiger une URL officielle accessible. Si la feature est "research preview annoncée", ne pas inventer ses specs internes.

### 3. Premier-auteur vs senior dans papers académiques

**Cas multiples détectés** :
- Self-Consistency : Wang premier, Zhou senior (vault attribuait à Zhou)
- SWE-agent : John Yang premier, Yao co-auteur (vault attribuait à Yao)
- BEIR : Thakur premier, Reimers co-auteur
- AWQ : Ji Lin premier, Song Han senior
- FlashAttention-4 : Zadouri/Shah/Hohnerbach co-leads, Tri Dao senior

**Pattern à éviter** : quand on crée une fiche "leader" autour d'un paper, ne pas systématiquement présenter le leader comme premier auteur. Vérifier arXiv → ordre exact des auteurs. Si senior/dernier, écrire "co-auteur senior" pas "auteur".

### 4. Awards conférences inventés (re-confirmation pattern)

**Cas** : `Sander Schulhoff.md` attribuait "EMNLP Best Theme Paper" au **Prompt Report** (arXiv 2406.06608). En réalité, c'est *"Ignore This Title and HackAPrompt"* (paper distinct du même Schulhoff) qui a eu **EMNLP 2023 Best Theme Paper**. Le Prompt Report (2024) n'a pas d'award listé EMNLP 2024 (vérifié sur emnlp.org/program/best_papers).

**Pattern récurrent** (confirmé sur audits précédents) : attribuer un award d'un paper à un autre paper du même auteur.

### 5. Stars GitHub drift x1.8 à x4 sur 6 mois (re-confirmation)

Confirmé empiriquement :
- Karpathy AutoResearch : 21K → 82.9K (x3.95)
- Ghostty (Hashimoto) : 30K → 55K (x1.84)
- Unsloth (Han) : 40K → 65K (x1.63)
- llama.cpp : sur-estimé 150K → réel 112K (correction à la baisse pour la première fois)

**Pattern à éviter** : toujours dater explicitement un chiffre stars GitHub. Re-fetcher en audit si > 3 mois.

### 6. Affiliations courantes obsolètes en 4-7 jours

**Cas critique** : Karpathy a rejoint Anthropic le **19 mai 2026** (verbatim X post). La fiche `Andrej Karpathy.md` datait du 8 mai 2026 et listait "Independent (ex-Tesla, ex-OpenAI)". Pas updatée en 4 jours malgré audit en cours.

Autres cas : Sutskever CEO SSI depuis juillet 2025 (pas 2024), Edward Hu statut "PhD Mila" obsolète (now Compute Exchange).

**Pattern à éviter** : pour leaders ultra-visibles (Karpathy, Sutskever, Sam Altman, Dario Amodei), vérifier affiliation chaque audit. Particulièrement sensible en période de mouvements lab (mai 2026 = vague de transitions).

### 7. Doublons cross-dossiers leaders

Détectés : Harrison Chase (agents+rag), Jerry Liu (agents+rag), Ethan Mollick (industrie+prompt), Hashimoto (claude-code+agents).

**Décision** : marquer canonique vs doublon plutôt que supprimer (préserve backlinks wikilink resolution Obsidian, format `[[Nom-leader]]`).

**Pattern à éviter** : avant de créer une fiche leader dans un dossier domaine, vérifier qu'elle n'existe pas dans un autre dossier domaine. Si oui, mettre canonique dans le dossier du scope **primaire** du leader (LangChain Harrison Chase = agents, pas RAG).

### 8. Verbatim vs paraphrase (re-confirmation pattern)

**Cas Thariq** : "99% of your AI-generated tokens should go to planning..." présenté comme verbatim Thariq dans la fiche. Cluster 4 a vérifié : c'est en fait une **paraphrase Lenny show notes** (HTML is the new markdown podcast). Concept attribuable, formulation exacte = show notes.

**Pattern à éviter** : un verbatim attribué à un speaker doit avoir un transcript audio/vidéo ou un blog signé par lui. Show notes d'un podcast = paraphrase éditoriale.

## Décisions méthode

### Self-verify FAUX impact = obligatoire AVANT phase D

Sur 3 self-verify WebFetch directs effectués (Mercado Libre via Every podcast, Karpathy Anthropic via TechCrunch, Dreaming via anthropic.com/news/dreaming) :
- 1 confirme fabrication (Mercado Libre)
- 1 confirme vrai (Karpathy)
- 1 confirme absence source (Dreaming 404)

**100% des self-verify ont apporté de l'info nouvelle ou critique**. Ne JAMAIS skip cette étape.

### Carte blanche + advisor sur bloqueur seulement

Raphael "carte blanche jusqu'au commit/push, advisor SI bloqueur réel". 1 advisor() appelé (avant phase A) + 1 advisor() appelé (avant V3). Le 2e advisor a confirmé "exécute direct, pas de nouveau advisor avant commit". Pattern validé.

## Décisions vault

### Sur fabrications "possibles mais non vérifiées"

Pour Mercado Libre + Dreaming specs : marqués ⚠️ avec note explicite "à confirmer livestream" + date audit, PAS supprimés. Justification : Raphael peut avoir vu le livestream et la source primaire existe peut-être hors de notre accès WebFetch.

**Anti-pattern à éviter** : supprimer aveuglément des claims qui pourraient être vrais juste parce que WebFetch ne les trouve pas. Marquer l'incertitude est plus honnête que supprimer une info potentiellement valable.

## Liens

- [[methode-analyser-repo]] — méthode A→B→C→D→E→F (confirmée à 6 audits consécutifs)
- [[feedback_audit_thematique_methode]] — méthode sub-agents clusters
- [[feedback_carte_blanche_commit_push]] — autonomie quand carte blanche
- [[feedback_anthropic_single_source]] — hiérarchie sources par thème
- [[Andrej Karpathy]] — affiliation Anthropic mise à jour
- [[cat-wu]] — fabrications Mercado Libre marquées
- [[jeremy-hadfield]] — specs Dreaming marquées non vérifiées
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — audit Claude Code (1er du chantier)
- [[erreur-audit-fine-tuning-2026-05-23]] — audit fine-tuning (5e)
