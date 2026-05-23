# Audit Vault — Thème : Leaders + Modèles + Industrie + Concurrents

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md`
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture — particulièrement critique pour ce thème (attributions, dates, rôles)
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème industrie globale, **pas du tout** bloqué sur Anthropic — c'est tout l'écosystème) :
>    - **Sources primaires d'un leader** (single source acceptable) : LinkedIn officiel du leader concerné, Twitter/X vérifié officiel, talk YouTube officiel
>    - **Docs/blogs officiels providers** (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, etc.) sur LEUR propre annonce = single source
>    - **Benchmarks modèles** = exiger source primaire (datasheet provider OU lmsys arena OU paper officiel) + setup exact (température, harness, dataset, date)
>    - **Anthropic** = single source UNIQUEMENT sur Claude/Anthropic, pas extrapolable aux autres providers
>    - **Couvertures presse tech reconnue** (Fortune, MIT Tech Review, TechCrunch, CNBC, Bloomberg) = 2+ sources convergentes
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **⚠️ Risques spécifiques ce thème** :
> - Coquilles de noms propagées (cf erreur "Angela Kiang → Angela Jiang" propagée audit 23 mai). Toujours trianguler 2+ sources pour confirmer attribution d'un événement/quote à une personne.
> - Benchmarks modèles (GPT-5.2-Codex, Sonnet 4.6, Opus 4.7, Gemini, etc.) — vérifier le setup exact (température, harness, dataset) et la date du benchmark.
> - Rôles changent (Karpathy a rejoint Anthropic 19 mai 2026) — vérifier la date de la note vs l'état actuel du leader.
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `feedback_regle_scope_pas_universelle`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Navigation vault — où lire selon le cas

| Si tu cherches... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines |
|-------------------|------------------------------------------------------------------|
| Méthode d'audit thématique générale | `[[methode-analyser-repo]]` (section ORDRE CANONIQUE A→B→C→D→E) |
| Fiches leaders Claude Code | `05-Leaders/claude-code/*` (Boris, Cat Wu, Thariq, Erik, Brad-Abrams, Mitchell-Hashimoto, etc.) |
| Fiches leaders agents IA | `05-Leaders/agents/*` (Karpathy, Ng, Weng, Chase, Liu, Yao, etc.) |
| Fiches leaders fine-tuning | `05-Leaders/fine-tuning/*` (Dettmers, Hu, Han, Dao, etc.) |
| Fiches leaders RAG | `05-Leaders/rag/*` (Kiela, Lewis, Khattab, Reimers, etc.) |
| Fiches leaders industrie | `05-Leaders/industrie/*` (Amodei, Altman, Mensch, Liang Wenfeng, etc.) |
| Concurrents Anthropic | `02-Concurrents/*` (ChatGPT, Codex, Gemini CLI, Cursor, Forge AI) |
| Modèles IA (specs, benchmarks) | `03-Modeles/*` (GPT-5.5, Opus 4.7, Sonnet 4.6, Haiku 4.5, Gemini 3, etc.) |
| Industrie / événements (CwC, releases) | `06-Industrie/*` + `01-Claude/Code/features/Code with Claude 2026.md` |
| Erreurs d'attribution déjà documentées (Angela Kiang→Jiang→Abrams) | `[[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]]` |

**N'oublie pas de regarder aussi** :
- MOCs : `[[MOC-Leaders]]`, `[[MOC-Concurrents]]`, `[[MOC-Modeles]]`, `[[MOC-Industrie]]`
- LinkedIn officiel + X officiel du leader concerné (source primaire)
- `Knowledge/erreurs/*` pour attributions déjà rectifiées
- Pattern check `[[methode-pivoter-doctrine]]` si une attribution change rôle/affiliation

## Scope

**Dossiers** : `05-Leaders/` + `03-Modeles/` + `02-Concurrents/` + `06-Industrie/`

**Notes à auditer (~78)** :

`05-Leaders/` (59 notes — 6 sous-dossiers) :
- `claude-code/` : 12 (Boris, Cat Wu, Justin Young, Thariq, Angela, Erik, Lisa, Daisy, Jeremy, Noah, Lydia, Alex)
- `agents/` : 14 (Karpathy, Andrew Ng, Chi Wang, Hashimoto, Lilian Weng, Harrison Chase, Jerry Liu, etc.)
- `rag/` : 8 (Kiela, Lewis, Khattab, Reimers, Xiao, Briggs, Kamradt, Roman)
- `fine-tuning/` : 14 (Dettmers, Hu, Dao, Raschka, Husain, Lambert, Han, Lian, Labonne, Schmid, etc.)
- `industrie/` : 7 (Dario Amodei, Sam Altman, Arthur Mensch, Tobi Lütke, Ethan Mollick, Chip Huyen, Liang Wenfeng)
- `prompt/` : 1 (Amanda Askell)

`03-Modeles/` : 7 notes (modèles IA — providers + benchmarks)

`02-Concurrents/` : 5 notes (ChatGPT, Codex, Gemini CLI, Cursor, etc.)

`06-Industrie/` : 7 notes (news, funding, mouvement marché)

## Hiérarchie experts

### Liste actuelle forge

Ce thème **EST** la liste d'experts elle-même → vérification de chaque fiche leader.

### Étape 0 — Valider chaque leader

Pour CHAQUE fiche leader, vérifier :
1. **Existence et autorité** : la personne existe, a une crédibilité publique vérifiable
2. **Rôle exact** : titre, affiliation, contributions documentées
3. **Reconnaissance** : 3+ mentions par d'autres experts ou contributions officielles vérifiables
4. **Pas dépassé** : actif en 2026 (pas inactif depuis 2 ans), pas tombé en disgrâce

WebSearch + LinkedIn + Twitter par leader.

## Sources spécifiques

### Pour chaque leader
- Profile LinkedIn officiel
- Twitter / X verified
- Wikipedia (si applicable)
- Site personnel / blog
- Liste de publications (papers, talks, posts)
- GitHub (si applicable)
- Mentions par autres experts (verbatim)

### Modèles
- Providers officiels : anthropic.com, openai.com, ai.google.dev, mistral.ai, deepseek.com, x.ai
- Benchmarks indépendants : LMSYS Chatbot Arena, livecodebench.github.io, Aider leaderboard, SWE-Bench
- Papers techniques (model cards)

### Concurrents Claude Code
- cursor.sh, github.com/features/copilot, cline.bot, sweep.dev
- aider.chat (Paul Gauthier)
- continue.dev
- zed.dev/edit
- Anthropic vs concurrents : benchmarks Terminal Bench, SWE-Bench

### Industrie
- VC reports (Sequoia, a16z, Battery)
- Anthropic funding rounds
- OpenAI / Meta / Google AI news
- The Information, The Verge, Stratechery (analyses industrie)

### Vidéos YouTube
- Interviews chaque leader (Latent Space, How I AI, Lex Fridman, Lenny)
- Keynotes conferences (NeurIPS, ICML, ACL, Hugging Face)
- Sequoia AI Ascent talks

## Claims à vérifier (priorité)

### Pour CHAQUE fiche leader
- **Titre / rôle exact** : à jour ?
- **Contributions verbatim** : sources originales vérifiables ?
- **Aliases** : 4-6 minimum (FR + EN + variantes)
- **resume** : 1 phrase spécifique pas générique
- **derniere-maj** : ≤ 3 mois sinon revérifier
- **tags** : ≥ 2 (type + domaine)
- **Wikilinks** : ≥ 2 notes liées

### Pour modèles
- Specs (params, context window, knowledge cutoff)
- Benchmarks récents (Arena ELO, SWE-Bench, MMLU)
- Pricing à jour
- Capacités multimodales

### Pour concurrents
- État 2026 (toujours actif, racheté, mort)
- Features clés à jour
- Forces / faiblesses vs Claude Code

### Pour industrie
- Funding rounds 2026 vérifiés
- Mouvements stratégiques (acquisitions, partenariats)
- Pas de "rumeur" présentée comme fait

## Étape F — Propagation

Si modifs notes leaders :

**Forge** :
- Notes canoniques `04-Techniques/claude-code/*` citent les leaders → update si fiche change
- Skill `cc-news` (veille IA) — pertinence des sources
- Vault `index.md` (orientation LLM)

**Autres notes vault** :
- Wikilinks vers leaders dans toutes les autres notes
- Backlinks pour vérifier impact

**Backlinks** :
- `get_backlinks` pour chaque leader majeur

## Output

`output/audit-vault-thematique/07-leaders-modeles-industrie/`

---

## Note importante

Ce thème est **le plus volumineux** (78 notes) mais aussi **le plus "data"** :
- Beaucoup de fiches courtes (1 leader = 1 fiche)
- Vérification factuelle (rôle, contribution, lien) plutôt que claims complexes
- Possible de paralléliser massivement avec sub-agents (1 sub-agent = 5-10 fiches)

Recommandation : **scripts Python custom essentiels** ici pour batch-vérifier 78 profiles LinkedIn / Twitter / Wikipedia en parallèle.

---

**Commence par étape 0 (validation experts) sur les leaders Anthropic Claude Code en premier (priorité usage), puis agents/rag/fine-tuning par ordre. advisor() aux transitions.**
