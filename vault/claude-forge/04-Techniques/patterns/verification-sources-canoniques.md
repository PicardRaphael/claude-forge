---
titre: "Vérification des sources canoniques — matrice provider + 4 patterns d'erreur"
resume: "Méthode de vérification avant capitalisation : provider officiel sur SON produit = single source, hors scope = 4+ sources convergentes ; WebFetch la source primaire avant tout verbatim ; 4 patterns d'erreur récurrents documentés (slug inventé, chiffre inventé, paraphrase, attribution fausse)."
aliases:
  - "verification sources canoniques"
  - "matrice provider single source"
  - "source canonique verification"
  - "verbatim verification pattern"
  - "paraphrase non verifiee"
  - "web search canonical source"
type: pattern
derniere-maj: 2026-07-21
auteur: claude
sources:
  - "Ex-skill forge web-search-canonical-source (foldée en rule contenu-externe-non-fiable, 9 juil. 2026)"
  - "memory feedback_anthropic_single_source + feedback_tweet_hype_paraphrase_pattern"
tags:
  - "#type/pattern"
  - "#domaine/veille"
  - "#statut/canonique"
---
# Vérification des sources canoniques

Pattern validé après 4 occurrences du même bug : tweet/article tiers → paraphrase verbatim non vérifiée → propagation comme fait Anthropic. **Avant de capitaliser une claim virale, WebFetch la source primaire.**

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

**Règle fondamentale** : provider/auteur officiel sur SON propre produit = single source acceptable. Hors de son scope = règle 4+ sources convergentes. Presse tech reconnue (Fortune, MIT Tech Review, TechCrunch) = 2+ sources.

## Pattern vérification verbatim

1. **WebFetch direct** la page docs supposée source (`docs.anthropic.com`, `platform.claude.com`, `code.claude.com/docs`)
2. **404 ou absent** → claim non canonique → reformuler « principe attesté mais formule X non vérifiée »
3. **Verbatim cité** → grep mot pour mot dans docs. Si absent → « paraphrase pédagogique », pas « verbatim »
4. **Attribution** (qui a dit quoi) → vérifier source primaire (LinkedIn officiel, X officiel, talk vidéo)

## Les 4 patterns d'erreur récurrents

| # | Source | Claim virale | Réalité |
|---|--------|-------------|---------|
| 1 | Justin Young article | « Init Opus + Coding Sonnet split » | Footnote 1 : « harness was otherwise identical » |
| 2 | Simon Willison live blog | « Angela Jiang advisor 5× cost reduction » | Brad Abrams (pas Angela), pas de chiffre « 5× » |
| 3 | Agent SDK overview | « Claude decides when to parallelize » | Paraphrase — verbatim réel : « Claude decides when to call a tool » |
| 4 | Tweet @_vmlops | « /workflows in Claude Code » | Slug inexistant — feature canonique = Programmatic Tool Calling ([[programmatic-tool-calling]]) |

**Cause racine** : sources tierces inventent des slugs plus catchy, des chiffres pour densité pédagogique, et paraphrasent pour l'élégance.

## Gotchas

- **« Anthropic single source » n'est PAS universel** : scopé à Claude/Anthropic produits. Pour RAG, Tim Dettmers > Anthropic. Pour prompt engineering, Amanda Askell > tweet tiers.
- **Articles X (x.com/i/article/...)** inaccessibles via WebFetch (402) — copy-paste utilisateur si source critique.
- **Stars GitHub drift ×3-×6 / 6 mois** pour repos AI/LLM — WebFetch obligatoire avant de citer un chiffre.
- **Papers NeurIPS/ICLR attribués à arXiv sans preuve** — WebFetch le PDF avant d'attribuer une venue (cf skill `arxiv-verification`).
- **Format arXiv YYMM doit matcher** le mois cité dans la note.

## Capitalisation après vérification

1. Note atomique vault (`create_note`) si nouvelle découverte, source primaire dans `sources:`
2. Principe canonique mais slug non vérifié → note explicite « principe attesté multi-sources, formule X non trouvée verbatim »
3. Audit thématique : distinguer Type 1 (attribution fausse) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)

## Liens

- `.claude/rules/contenu-externe-non-fiable.md` (rule forge, hors vault — porte la doctrine toujours-active et pointe ici)
- [[programmatic-tool-calling]] — cas d'application du pattern
- Memory : `feedback_anthropic_single_source`, `feedback_tweet_hype_paraphrase_pattern`, `feedback_arxiv_id_yymm_format`, `feedback_stars_github_drift`


---

## AJOUT 21 juillet 2026 — Patterns 5 et 6 : quote inventée + contenu recyclé non daté

Deux nouveaux cas documentés le même jour (session forge, 2 vidéos X transcrites intégralement pour vérification) :

| # | Source | Claim virale | Réalité |
|---|--------|-------------|---------|
| 5 | Tweet @hrswatigupta (19 juil. 2026) | Verbatim « You're not supposed to prompt Claude. You're supposed to build a system that prompts itself » + « In 45 minutes » | **Citation absente** du transcript intégral (31 min, pas 45) du talk AI DevCon de Lamis (Anthropic Applied AI). Hook fabriqué pour l'engagement — le talk réel porte sur memory/dreaming, pas sur « prompter » |
| 6 | Tweet @cyrilXBT (20 juil. 2026) | « Boris Cherny sat down and showed how he actually uses it » (présent, implique du neuf) | Talk « pro tips » de **Code with Claude mai 2025** — 14 mois d'âge (GitHub app « announced today », prédiction fin des IDE « by the end of the year », `/vibe`, `.claude/commands/`). Doctrine Boris 2026 ([[workflow-claude-code-optimal]], [[pre-compute-vs-inference-loops-boris]]) très différente |

**Réflexe additionnel — DATER le contenu vidéo avant de capitaliser** : un talk recyclé n'est pas faux, mais le capitaliser comme état de l'art écrase une doctrine plus récente déjà en vault. Indices de datation dans la vidéo elle-même : annonces « today », features montrées à l'écran (slash commands disparues, UI datée), prédictions vérifiables, structure de config d'époque. La transcription intégrale (pipeline [[Memory Managed Agents|x-read → ffmpeg → faster-whisper]], cf memory `reference_transcrire_video_native_x`) reste le seul moyen fiable de vérifier un verbatim attribué à une vidéo.
