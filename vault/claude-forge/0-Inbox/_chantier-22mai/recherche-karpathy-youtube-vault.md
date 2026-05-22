---
titre: "Karpathy YouTube — Méthode vault/LLM Wiki en vidéo et repos publics"
resume: "Vidéos YouTube Karpathy sur knowledge management/vault + repos publics avec CLAUDE.md/AGENTS.md — sources primaires verbatim pour optimiser forge-brain"
aliases:
  - "karpathy youtube vault"
  - "karpathy methode vault video"
  - "karpathy repo llm wiki"
  - "karpathy second brain"
  - "karpathy knowledge management"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/synthese"
  - "#domaine/agents"
  - "#type/leader"
---

# Karpathy YouTube — Méthode vault / LLM Wiki en vidéo et repos publics

> Recherche complémentaire au Gist + tweets + Sequoia Ascent déjà capitalisés.
> Objectif : identifier les sources YouTube **directement de Karpathy** sur le pattern vault et inventorier ses **repos publics** pour voir s'il y matérialise concrètement son LLM Wiki.

---

## TL;DR (à lire en premier)

1. **Karpathy n'a PAS publié de vidéo YouTube dédiée à sa méthode vault/LLM Wiki sur sa chaîne `@AndrejKarpathy`.** Le Gist (`llm-wiki.md`, 3-4 avril 2026) + ses tweets sont les seules sources primaires écrites. La seule mention orale verbatim retrouvée est dans le **Sequoia AI Ascent 2026** (~20 avril 2026, déjà couvert par recherche précédente — fireside chat avec Stephanie Zhan, intitulé YouTube *"From Vibe Coding to Agentic Engineering"*, watch?v=96jN2OCOfLs).
2. **Karpathy n'a PAS de repo public dédié au LLM Wiki / vault.** Ses 63 repos ont été énumérés (voir Section 3). Le pattern vit dans un Gist — pas dans un repo.
3. **Le seul artefact agent-skill dans ses repos publics est `nanochat/.claude/skills/read-arxiv-paper/SKILL.md`** (verbatim Section 3.A). C'est une skill d'ingest arxiv → markdown, alignée avec le pattern Ingest du Gist.
4. **`paper-notes`** (repo 2014-2015, 710 stars) est le seul repo avec un nom proche d'un vault, mais ce n'est qu'un dossier de markdown rough — pas une instanciation du pattern.
5. **L'écosystème communautaire est massif** (5000+ stars sur le Gist, ~16M vues sur le tweet, 7+ implémentations communautaires en une semaine, levée Edra 30M$ Seq A), mais aucune n'est de Karpathy lui-même.

---

## Section 1 — Vidéos YouTube transcrites

### Aucune vidéo de Karpathy spécifiquement sur le vault à transcrire

La skill `watch` n'a **pas été lancée**. Raison : aucune vidéo Karpathy directe sur le sujet vault/wiki à transcrire au-delà du Sequoia Ascent déjà capitalisé.

Vidéos parcourues (chaîne `@AndrejKarpathy`, via Google Search YouTube — la page chaîne directe est bloquée par mur de consentement YT) :

| Titre Karpathy 2025-2026 | Sujet | Pertinence vault |
|---|---|---|
| *Deep Dive into LLMs like ChatGPT* | Fondamentaux LLM | Aucune |
| *How I Use LLMs* | Usage pratique | À vérifier — pourrait toucher au workflow, mais pas mentionné dans les sources comme parlant de vault |
| *Zero to Hero* playlist | Cours technique | Aucune |
| *The Three Types of Programmers in 2026* (YT Short, 1 mars 2026) | Software 1.0/2.0/3.0 | Aucune (vault non mentionné) |

**Décision** : pas de transcription Whisper consommée. La vidéo *How I Use LLMs* est candidate à transcrire dans une session ultérieure si on veut vérifier qu'il parle bien de son workflow vault — mais d'après les sources secondaires recensées, aucun article ne cite cette vidéo comme source du pattern wiki (toujours le Gist et le tweet d'avril 2026).

---

## Section 2 — Vidéos identifiées mais non transcrites

### 2.A — Sequoia AI Ascent 2026 — "From Vibe Coding to Agentic Engineering"

- **URL** : https://www.youtube.com/watch?v=96jN2OCOfLs
- **Date pub** : ~20-30 avril 2026 (talk donné le 20 avril, upload "3 semaines avant" au 22 mai)
- **Speaker(s)** : Andrej Karpathy + Stephanie Zhan (Sequoia)
- **Pourquoi non transcrite ici** : déjà couverte par le rapport sœur `recherche-youtube-watch-vibe-coding.md` selon prompt. Mention vault dans cette vidéo confirmée par sources secondaires : *"an LLM-generated knowledge base"* est cité comme exemple de logiciel **Software 3.0** qui n'existait pas avant — *"there was no normal software program that could take a messy pile of documents, understand them, restructure them, rewrite them, and turn them into a useful wiki. Now that becomes possible."* (paraphrase article The AI Opportunities — pas de transcript verbatim public confirmé).

### 2.B — Dwarkesh Patel × Karpathy — "AGI is still a decade away"

- **URL** : https://www.dwarkesh.com/p/andrej-karpathy + YouTube Dwarkesh (~17 oct 2025)
- **Durée** : ~2h
- **Pourquoi non transcrite** : timestamps officiels publiés (AGI 10 ans / RL terrible / model collapse / éducation / self-driving / ASI / culture LLM) — **aucune section dédiée au vault ou aux notes** sur la liste de chapitres. Pas la peine de transcrire pour ce chantier.

### 2.C — Vidéos communautaires (NON-Karpathy mais référence)

| Vidéo | URL | Auteur | Pertinence |
|---|---|---|---|
| *Karpathy's LLM Wiki — Full Beginner Setup Guide* (12 avr 2026) | https://www.youtube.com/watch?v=iXd0t60YmMw | tiers | Implémentation Obsidian |
| *Building a Second Brain With AI* | https://www.youtube.com/watch?v=Mo0EFSFmYiU | tiers | Setup vault |
| *I Built AI Second Brain. Here's How.* | https://www.youtube.com/watch?v=mKwP4imvFo4 | tiers | Setup vault |

**Non transcrites** : ce ne sont pas des sources primaires Karpathy. Pour optimiser forge-brain, le Gist + Sequoia talk + tweets suffisent.

---

## Section 3 — Repos Karpathy publics

### 3.0 — Inventaire EXHAUSTIF des 60 repos publics (63 incluant 3 forks)

**Page 1** (30 repos) : nanochat, karpathy.github.io, autoresearch, jobs, rustbpe, cpython*, hn-time-capsule, llm-council, reader3, nanoGPT, rendergit, llm.c, nn-zero-to-hero, minGPT, build-nanogpt, micrograd, llama2.c, LLM101n, minbpe, makemore, calorie, lecun1989-repro, ng-video-lecture, char-rnn, notpygamejs, researchpooler, karpathy (root), arxiv-sanity-lite, randomfun, convnetjs

**Page 2** (30 repos) : transformers*, arxiv-sanity-preserver, deep-vector-quantization, optim*, cryptos, neuraltalk, ulogme, covid-sanity, gitstats, sqlitedict*, pytorch-normalizing-flows, tsnejs, reinforcejs, pytorch-made, examples*, svmjs, find-birds, neuraltalk2, tf-agent, nipspreview, **paper-notes**, recurrentjs, EigenLibSVM, nn*, simple-amt*, scholaroctopus, Random-Forest-Matlab, researchlei, twoolpy, forestjs

(* = fork)

### Recherche par mot-clé sur les 63 noms

| Pattern recherché | Match |
|---|---|
| `wiki` | **AUCUN** |
| `vault` | **AUCUN** |
| `notes` | `paper-notes` (1 match) |
| `knowledge` | **AUCUN** |
| `brain` / `second-brain` | **AUCUN** |
| `memex` | **AUCUN** |
| `obsidian` | **AUCUN** |
| `llm-wiki` | **AUCUN** |

**Conclusion empirique** : Karpathy n'a aucun repo public matérialisant son LLM Wiki. Le pattern est ABSTRAIT (Gist + tweets). Toutes les implémentations existantes (lucasastorian/llmwiki, Astro-Han/karpathy-llm-wiki, toolboxmd/karpathy-wiki, NicholasSpisak/second-brain, Programming-With-Maury/Karpathy-LLM-Wiki, forrestchang/andrej-karpathy-skills, etc.) sont communautaires.

---

### 3.A — `karpathy/nanochat` — SKILL agent-compatible

- URL : https://github.com/karpathy/nanochat
- Branche par défaut : `master`
- Description : *"The best ChatGPT that $100 can buy."*

**Structure racine vérifiée** :
```
.claude/skills/read-arxiv-paper/SKILL.md
dev/
nanochat/
runs/
scripts/
tasks/
tests/
.gitignore
.python-version
LICENSE
README.md
pyproject.toml
uv.lock
```

**Pas de `CLAUDE.md` racine. Pas de `AGENTS.md`.** Confirmé par 404 sur les deux URLs raw.

**FICHIER `.claude/skills/read-arxiv-paper/SKILL.md` — VERBATIM COMPLET** (source : raw GitHub) :

```markdown
---
name: read-arxiv-paper
description: Use this skill when asked to read an arxiv paper given an arxiv URL
---

You will be given a URL of an arxiv paper, for example:

https://www.arxiv.org/abs/2601.07372

### Part 1: Normalize the URL

The goal is to fetch the TeX Source of the paper (not the PDF!), the URL always looks like this:

https://www.arxiv.org/src/2601.07372

Notice the /src/ in the url. Once you have the URL:

### Part 2: Download the paper source

Fetch the url to a local .tar.gz file. A good location is `~/.cache/nanochat/knowledge/{arxiv_id}.tar.gz`.

(If the file already exists, there is no need to re-download it).

### Part 3: Unpack the file in that folder

Unpack the contents into `~/.cache/nanochat/knowledge/{arxiv_id}` directory.

### Part 4: Locate the entrypoint

Every latex source usually has an entrypoint, such as `main.tex` or something like that.

### Part 5: Read the paper

Once you've found the entrypoint, Read the contents and then recurse through all other relevant source files to read the paper.

### Part 6: Report

Once you've read the paper, produce a summary of the paper into a markdown file at `./knowledge/summary_{tag}.md`. Notice that 1) use the local knowledge directory here (it's easier for me to open and reference here), not in `~/.cache`, and 2) generate some reasonable `tag` like e.g. `conditional_memory` or whatever seems appropriate given the paper. Probably make sure that the tag doesn't exist yet so you're not overwriting files.

As for the summary itself, remember that you're processing this paper within the context of the nanochat repository, so most often we will be interested in how to apply the paper and its lessons to the nanochat project. Therefore, you should feel free to "remind yourself" of the related nanochat code by reading the relevant parts, and then explicitly make the connection of how this paper might relate to nanochat or what are things we might be inspired about or try.
```

**Observations clés** :
- Skill **ultra-minimaliste** (~40 lignes). Pas de scripts, pas de references/, pas de subdirs.
- Frontmatter **strict 2 champs** : `name` + `description` (pas de `model`, pas de `allowed-tools`, pas de `disallowed-tools`, pas de `color`).
- Description en **3ème personne** ("Use this skill when asked to read...") — aligné avec best practice Anthropic.
- Sections numérotées **Part 1..Part 6** — procédural.
- Output convention : `./knowledge/summary_{tag}.md` — dossier `knowledge/` LOCAL au repo, et `~/.cache/nanochat/knowledge/` pour cache global.
- **Lien direct au pattern Gist** : c'est exactement l'opération "Ingest" du LLM Wiki, appliquée à un arxiv. Le `summary_{tag}.md` est la wiki-page. Le `.tar.gz` source est la "raw source".
- Karpathy ne crée pas d'index.md ni de log.md ici — la skill s'arrête à l'ingest et produit un fichier markdown. Le linking inter-pages est laissé à l'agent en runtime.

### 3.B — `karpathy/paper-notes` — VERBATIM README

- URL : https://github.com/karpathy/paper-notes
- Stats : 710 stars, 87 forks, 11 commits total (repo dormant depuis ~2015-2016)
- Fichiers : `matching_networks.md`, `vin.md`, `wikireading.md`, dossier `img/`, `.gitignore`

**README contenu intégral** : *"Random notes? There should be a better place for this I think..."*

C'est tout. Une seule phrase. Le repo est antérieur d'une décennie au pattern LLM Wiki — c'est l'aveu de Karpathy que le problème vault n'était pas résolu en 2015-2016, ce qui contextualise pourquoi le Gist 2026 est important pour lui : 10 ans plus tard, le LLM résout enfin la maintenance qui rendait ce repo abandonnable.

### 3.C — `karpathy/autoresearch` — vérifié, NON pertinent

- Pas de `CLAUDE.md`, pas de `AGENTS.md`.
- Fichiers racine : `prepare.py`, `train.py`, `program.md`, `analysis.ipynb`, etc.
- Le `program.md` est décrit comme *"a super lightweight 'skill'"* mais c'est un prompt d'agent autonome pour expérimenter sur du training LLM overnight — sans rapport avec le pattern vault.

### 3.D — autres repos vérifiés indirectement

- `nanoGPT`, `llm.c`, `micrograd`, `makemore`, `microgpt` : repos d'apprentissage ML, aucun fichier agent.
- `karpathy.github.io` : site perso (`karpathy.ai`) — confirmé **aucune mention** de vault/Obsidian/wiki/knowledge base sur la page.
- `karpathy` (root profile repo) : profil README standard.

---

## Section 4 — Threads X Karpathy sur notes/wiki/vault

### 4.A — Tweet originel (3 avril 2026) — viral ~16-19M vues

Verbatim opening (cité par sources secondaires multiples) :

> *"Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest."*

### 4.B — Citation idée centrale (issue du Gist + thread)

> *"Instead of having the LLM re-read your raw documents every time you ask a question, build a persistent, structured wiki once and keep it updated forever."*

### 4.C — Analogie phare (Gist + thread suivi)

> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."*

### 4.D — Exemple chiffré personnel cité publiquement

Karpathy a indiqué que son vault personnel de recherche sur **un seul sujet ML** comptait au moment du tweet :
- **~100 articles**
- **~400 000 mots**
- **Aucun mot écrit directement par lui** — tout le contenu produit par l'agent LLM

> *"the entire wiki index fits comfortably within a modern LLM's context window"* (citation paraphrasée — implique que ~100 articles d'index reste sous ~200k tokens).

### 4.E — Analogie fan-wiki (Gist)

> *"Think of fan wikis like Tolkien Gateway — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance."*

### 4.F — Thread janvier 2026 (CLAUDE.md observations)

26 janvier 2026 — thread distinct sur les pitfalls de Claude Code pour le coding (PAS sur vault). Distillé par Forrest Chang en `andrej-karpathy-skills/CLAUDE.md` (109k+ stars GitHub). **À ne pas confondre avec le pattern wiki** : c'est un CLAUDE.md anti-pitfalls coding agent, pas un schéma wiki.

### 4.G — Tweet de suivi Sequoia (~27 avril 2026)

URL : https://x.com/karpathy/status/2049903821095354523

> *"Fireside chat at Sequoia Ascent 2026 from a ~week ago. Some highlights: The first theme I tried to push on is that LLMs are about a lot more than just speeding up what existed before (e.g. coding). Three examples of new horizons: 1. menugen: an app that can be fully engulfed by [...]"*

(Suite du thread non récupérée intégralement faute d'accès X authentifié — utiliser skill `x-read` pour le verbatim complet dans une session ultérieure si besoin).

---

## Section 5 — Synthèse : réponses aux 6 questions stratégiques

### 1. Karpathy a-t-il une vidéo YouTube spécifiquement sur sa méthode vault ?
**Non.** Aucune vidéo dédiée sur sa chaîne `@AndrejKarpathy`. La seule mention orale publique connue est le **Sequoia AI Ascent 2026** (https://www.youtube.com/watch?v=96jN2OCOfLs) où il cite l'"LLM-generated knowledge base" comme exemple emblématique de Software 3.0 — sans déroulement détaillé.

### 2. Quel repo public Karpathy implémente le pattern LLM Wiki ?
**Aucun.** Inventaire exhaustif des 63 repos : 0 match sur wiki/vault/knowledge/brain/memex/obsidian. Le repo le plus proche est `nanochat` qui contient une **skill `read-arxiv-paper`** matérialisant l'opération **Ingest** du pattern (verbatim Section 3.A). Le pattern complet (ingest + query + lint + index.md + log.md) n'existe dans aucun repo public Karpathy.

### 3. Quelle est la structure dossier EXACTE qu'il utilise dans ses repos publics ?
La seule structure agent observée (`nanochat`) :
```
.claude/skills/<skill-name>/SKILL.md       (skill ingest)
knowledge/summary_<tag>.md                 (wiki-page output, LOCAL au repo)
~/.cache/nanochat/knowledge/<id>/          (raw source cache, GLOBAL)
~/.cache/nanochat/knowledge/<id>.tar.gz    (raw archive)
```
Pas de `index.md`, pas de `log.md`, pas de `CLAUDE.md` racine dans le repo nanochat. Le Gist préconise ces fichiers, mais Karpathy ne les expose pas publiquement dans ses repos.

### 4. Quel outil il recommande pour query le vault ?
**`qmd`** (Quick Markdown) — outil CLI + MCP server de **Tobi Lütke (CEO Shopify)** : https://github.com/tobi/qmd. Combine BM25 + recherche vectorielle + LLM re-ranking, **100% local** (node-llama-cpp + GGUF). Cité explicitement dans le Gist. Karpathy mentionne aussi en complément : **Obsidian** (browse + graph view), **Obsidian Web Clipper** (ingest articles web), **Marp** (slides depuis markdown), **Dataview** (queries frontmatter), **Git** (versioning).

### 5. Combien de notes dans son vault personnel ?
**~100 articles / ~400 000 mots** sur **un seul sujet de recherche ML** (cité publiquement dans son tweet + Gist d'avril 2026). Pas de chiffre publié pour son vault total multi-sujets.

### 6. Workflow Ingest → Wiki → Query : exemple concret cité par lui ?
Le Gist décrit l'opération **Ingest** comme : "Drop a source → LLM reads, summarizes, updates ~10–15 wiki pages, appends to log." Le `read-arxiv-paper/SKILL.md` de nanochat est l'**implémentation atomique réelle** de cet ingest sur un input arxiv (Section 3.A : 6 étapes Normalize URL → Download src → Unpack → Locate entrypoint → Read → Report into `summary_{tag}.md`). C'est le seul exemple verbatim concret publié par Karpathy lui-même.

---

## Section 6 — Implications pour optimisation forge-brain et futurs vaults

### 6.A — Ce que forge-brain fait DÉJÀ aligné avec Karpathy

| Pattern Karpathy | forge-brain actuel | Status |
|---|---|---|
| 3 layers : Raw / Wiki / Schema | `0-Inbox/` (raw capture) + `1-Projets/` `04-Techniques/` etc. (wiki) + CLAUDE.md + rules (schema) | ✓ aligné |
| Ingest = nouvelle source → updates ~10-15 pages | Skill `forge-brain` MCP + `cc-news` capitalise + cross-link automatique | ✓ aligné |
| Query = LLM lit l'index d'abord | `search_brain` FTS5 sur tout le vault | ✓ aligné |
| LLM owns the wiki layer | Skills create/append/update via MCP | ✓ aligné |
| Schema co-évolué humain+LLM | CLAUDE.md + rules + protocoles | ✓ aligné |
| Obsidian comme IDE de browse | Vault Obsidian local | ✓ aligné |

### 6.B — Ce que forge-brain N'A PAS et que le pattern recommande

1. **`index.md`** — Karpathy : "LLM reads this first when answering queries". forge-brain a les MOCs `00-Hub/` mais **pas un index.md racine** consolidé. **Action proposée** : créer `vault/claude-forge/INDEX.md` content-oriented (pas folder-oriented) regroupant les ~50 notes les plus consultées par catégorie, lu en premier par `search_brain` en mode "navigation".
2. **`log.md`** append-only avec préfixe `## [YYYY-MM-DD] action | title` — forge-brain a `CHANGELOG.md` (similaire) mais format différent. **Action proposée** : harmoniser le format CHANGELOG vault avec le préfixe Karpathy `## [YYYY-MM-DD] action | title` pour grep-friendly.
3. **`qmd` MCP** — Karpathy recommande qmd pour query local hybride BM25+vector+LLM rerank. forge-brain utilise FTS5 SQLite uniquement (full-text, pas de vector). **Action à explorer** : tester qmd MCP en parallèle de l'actuel MCP forge-brain. Pourrait booster les recherches sémantiques sur les concepts abstraits.
4. **Opération `lint` périodique** — Karpathy : "scans entire wiki for inconsistencies, articles that contradict each other, and index entries that are stale or missing." forge-brain a `vault-audit` skill (manuel) mais **pas de lint scheduled**. **Action proposée** : `/schedule weekly /vault-lint` qui détecte orphelins, contradictions cross-notes, stale (`derniere-maj` > 90j), wikilinks cassés.
5. **Skill atomique Ingest par type de source** — Karpathy a `read-arxiv-paper`. forge-brain n'a pas l'équivalent. **Action proposée** : créer skills atomiques `ingest-youtube-video`, `ingest-arxiv-paper`, `ingest-x-thread`, `ingest-github-repo` qui suivent toutes le même contrat 6-step (Normalize → Fetch → Parse → Locate → Read → Report into `<note-name>.md`).

### 6.C — Ce que Karpathy ne mentionne PAS et que forge-brain a en plus

- **Aliases obligatoires (4-6 par note)** — pas dans le pattern Karpathy. Atout forge-brain pour la recherche multi-formulation.
- **Devil's advocate** sur livrables vault — pas dans le pattern Karpathy.
- **Hook architecture** (delegate-guard, vault-query-guard) — pas dans le pattern Karpathy (qui est advisory/Schema-only).
- **Compounding via skills meta** (`skill-evolve`, `reasoning-cache`) — pas dans le pattern Karpathy.

### 6.D — Conclusion stratégique

Le pattern Karpathy LLM Wiki **valide a posteriori** l'architecture forge-brain (3 layers + LLM owns wiki + schema co-évolué). Les 5 gaps identifiés (INDEX.md content-oriented, log format harmonisé, qmd à tester, lint scheduled, skills ingest atomiques) sont des **optimisations incrémentales** — pas de refonte nécessaire.

Le gap le plus haut-ROI à creuser : **skills `ingest-*` atomiques** sur le modèle `read-arxiv-paper`. Karpathy publie une seule skill — exactement celle qui mappe le mieux à son workflow de recherche ML. forge-brain devrait identifier ses 3-5 sources les plus fréquentes (YouTube, X threads, GitHub repos, blog Anthropic, arxiv) et créer une skill ingest atomique pour chacune.

---

## Sources

### Sources primaires Karpathy
- [Gist `llm-wiki.md` (4 avril 2026)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy GitHub profile (63 repos)](https://github.com/karpathy?tab=repositories)
- [karpathy.ai (site perso)](https://karpathy.ai/)
- [nanochat repo](https://github.com/karpathy/nanochat) + [SKILL.md raw](https://raw.githubusercontent.com/karpathy/nanochat/master/.claude/skills/read-arxiv-paper/SKILL.md)
- [paper-notes repo](https://github.com/karpathy/paper-notes)
- [autoresearch repo](https://github.com/karpathy/autoresearch)
- [Tweet Sequoia follow-up](https://x.com/karpathy/status/2049903821095354523)
- [Dwarkesh × Karpathy podcast (17 oct 2025)](https://www.dwarkesh.com/p/andrej-karpathy)
- [Sequoia AI Ascent 2026 — From Vibe Coding to Agentic Engineering (YT)](https://www.youtube.com/watch?v=96jN2OCOfLs)

### Sources tierces analyse / contexte
- [TrainingSites — 684 Videos / LLM Wiki](https://trainingsites.io/tutorial/684-videos-and-no-idea-whats-in-them-karpathys-llm-wiki-fixed-it/)
- [aimaker.substack — How I Took Karpathy's LLM Wiki](https://aimaker.substack.com/p/llm-wiki-obsidian-knowledge-base-andrej-karphaty)
- [MindStudio — LLM Wiki Obsidian Second Brain](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-obsidian-ai-second-brain)
- [agentpedia — CLAUDE.md Skills File](https://agentpedia.codes/blog/karpathy-claude-md-code-skills-guide)
- [aaronfulkerson — LLM Wiki in Production](https://aaronfulkerson.com/2026/04/12/karpathys-pattern-for-an-llm-wiki-in-production/)
- [Medium Nikhil — Karpathy Stopped Writing Code](https://medium.com/neuralnotions/andrej-karpathy-stopped-using-ai-to-write-code-hes-using-it-to-build-a-second-brain-instead-cddceadc5df5)
- [theaiopportunities — Sequoia AI Ascent 2026 Karpathy](https://www.theaiopportunities.com/p/sequoia-ai-ascent-2026-andrej-karpathy)
- [philippdubach — Software 3.0 Playbook 12 Lessons](https://philippdubach.com/posts/karpathys-software-3.0-playbook/)

### Implémentations communautaires (PAS de Karpathy)
- [tobi/qmd — outil query recommandé](https://github.com/tobi/qmd)
- [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki)
- [Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
- [toolboxmd/karpathy-wiki](https://github.com/toolboxmd/karpathy-wiki/tree/main/)
- [forrestchang/andrej-karpathy-skills (CLAUDE.md 109k stars)](https://github.com/forrestchang/andrej-karpathy-skills)
- [Programming-With-Maury/Karpathy-LLM-Wiki AGENTS.md](https://github.com/Programming-With-Maury/Karpathy-LLM-Wiki/blob/main/AGENTS.md)
- [NicholasSpisak/second-brain](https://github.com/NicholasSpisak/second-brain)

## Liens vault

- [[recherche-youtube-watch-vibe-coding]] — couverture Sequoia Ascent
- [[recherche-github-karpathy-leaders]] — recherche sœur sur repos Karpathy
- [[recherche-x-twitter-leaders]] — threads X Karpathy
- [[Andrej-Karpathy]] — fiche leader (à créer/MAJ)
