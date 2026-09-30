---
name: web-search-canonical-source
description: ALWAYS prefer canonical provider source (Anthropic docs for Claude, OpenAI docs for GPT). For broader topics, multi-source consensus. Never single tweet/article as authority without verification (paraphrase non-verified pattern).
allowed-tools: WebSearch, WebFetch, mcp__forge-brain__search_brain, mcp__forge-brain__read_note
model: opus
effort: medium
---

# Sources canoniques — hiérarchie et vérification

Pattern validé après 4 occurrences du même bug : tweet/article tiers → paraphrase verbatim non vérifiée → propagation comme fait Anthropic. **Avant de capitaliser une claim virale, WebFetch la source primaire.**

---

## Matrice provider → single source acceptable

| Sujet | Single source suffit | Multi-source obligatoire (4+) |
|-------|---------------------|-------------------------------|
| Claude / Claude Code / Anthropic produits | **Anthropic team, docs, blog** | Externes tiers sur Claude |
| GPT / OpenAI produits | **OpenAI docs / blog officiel** | Tiers sur OpenAI |
| Gemini / Google produits | **Google docs officiel** | Tiers sur Google |
| Llama / Meta produits | **Meta blog / docs** | Tiers sur Meta |
| Framework sur son propre produit | **Docs officielles** (LangChain, CrewAI) | Comparaisons tiers |
| Paper académique peer-reviewed | **arXiv ACL/EMNLP/NeurIPS/ICML** | Blogs commentant le paper |
| Prompt Engineering général | Amanda Askell, DAIR.AI, Wei/Zhou papers | Blogs Medium/DEV community |
| RAG | Kiela, Lewis, Khattab, Reimers, Kamradt, Chase | Blogs tiers |
| Agents IA | Ng, Weng, Chase, Yao, Moura, Nakajima | Blogs tiers |
| Fine-tuning | Dettmers, Hu, Han, Raschka + arXiv | Blogs tiers (Anthropic quasi non-pertinent) |
| Pattern auteur original | Auteur original sur SA création | Paraphrases tierces |

**Règle fondamentale** : provider/auteur officiel sur SON propre produit = single source acceptable. Hors de son scope = règle 4+ sources convergentes.

---

## Pattern vérification verbatim

Avant de capitaliser une claim comme verbatim Anthropic (ou tout provider) :

1. **WebFetch direct** la page docs supposée source (`docs.anthropic.com`, `platform.claude.com`, `code.claude.com/docs`)
2. **404 ou absent** → claim non canonique → reformuler "principe attesté mais formule X non vérifiée"
3. **Verbatim cité** → grep mot pour mot dans docs. Si absent → "paraphrase pédagogique", pas "verbatim"
4. **Attribution** (qui a dit quoi) → vérifier source primaire (LinkedIn officiel, X officiel, talk vidéo)

---

## Les 4 patterns d'erreur récurrents

| # | Source | Claim virale | Réalité |
|---|--------|-------------|---------|
| 1 | Justin Young article | "Init Opus + Coding Sonnet split" | Footnote 1 : "harness was otherwise identical" |
| 2 | Simon Willison live blog | "Angela Jiang advisor 5× cost reduction" | Brad Abrams (pas Angela), pas de chiffre "5×" |
| 3 | Agent SDK overview | "Claude decides when to parallelize" | Paraphrase — verbatim réel : "Claude decides when to call a tool" |
| 4 | Tweet @_vmlops | "/workflows in Claude Code" | Slug inexistant — feature canonique = Programmatic Tool Calling (PTC) |

**Cause racine** : sources tierces inventent des slugs plus catchy, des chiffres pour densité pédagogique, et paraphrasent pour l'élégance. Forge propage l'amélioration comme verbatim.

---

## Gotchas

- **"Anthropic single source" n'est PAS universel** : scoped à Claude/Anthropic produits. Pour RAG, Tim Dettmers > Anthropic. Pour prompt engineering, Amanda Askell > tweet tiers.
- **Presse tech reconnue** (Fortune, MIT Tech Review, TechCrunch) = 2+ sources convergentes (pas 4).
- **Blogs / Medium / DEV community** = 4+ sources convergentes obligatoires.
- **Articles X (x.com/i/article/...)** inaccessibles via WebFetch (402). User doit copy-paste si source critique.
- **Stars GitHub drift x3-x6 / 6 mois** pour repos AI/LLM — WebFetch obligatoire avant de citer un chiffre.
- **Papers NeurIPS/ICLR attribués à arXiv sans preuve** — WebFetch PDF avant attribuer une conférence.
- **Format arXiv YYMM doit matcher** le mois cité dans la note.

---

## Capitalisation après vérification

Une fois la claim vérifiée :
1. Créer note atomique vault via `mcp__forge-brain__create_note` si nouvelle découverte
2. Citer la source primaire dans `sources:` frontmatter
3. Si principe canonique mais slug non vérifié : note explicite "principe attesté multi-sources, formule `X` non trouvée verbatim"
4. Pour tout audit thématique : distinguer Type 1 (attribution fausse) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)

---

## Référence

Memory sources : `feedback_anthropic_single_source`, `feedback_tweet_hype_paraphrase_pattern`
Patterns liés : `feedback_arxiv_id_yymm_format`, `feedback_arxiv_url_swap_papers_similaires`, `feedback_stars_github_drift`, `feedback_venues_inventees_pattern`

---

## Apprentissage

Après chaque session impliquant WebFetch de vérification :
- Documenter les patterns d'erreur nouveaux (s'il en apparaît un 5e type)
- Mettre à jour le tableau des 4 patterns si nouvelle occurrence
- Si la règle de scope change (nouveau provider ou nouveau domaine) → mettre à jour la matrice ci-dessus
