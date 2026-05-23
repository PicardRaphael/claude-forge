# Audit Vault — Thème : Prompt Engineering

> **Lire d'abord** : `output/audit-vault-thematique/00-TEMPLATE-COMMUN.md` pour méthode A→B→C→D→E + propagation F + règles absolues.
>
> **Méthode validée à appliquer impérativement** (cf audit Claude Code 23 mai 2026, 95 claims auditées, 22 erreurs corrigées) :
> 1. Lecture parallèle des N notes via `mcp__forge-brain__read_note` SANS max_lines (session principale, pas sub-agents)
> 2. Inventaire claims dédupliqué → **checkpoint write `A-inventaire-claims.md` AVANT lancer phase B**
> 3. **Sub-agents parallèles par CLUSTER thématique** (5-7 clusters, PAS par note) avec brief structuré : claim verbatim + URLs candidates + format imposé
> 4. **Self-verify FAUX fort impact AVANT phase D** : refetch direct WebFetch les fondations doctrinales avant réécriture
> 5. **Distinguer Type 1 (citation/source fausse, principe juste) / Type 2 (chiffre inventé) / Type 3 (doctrine fausse au fond)** dans plan correction
> 6. **Hiérarchie sources** (thème large, PAS bloqué sur Anthropic) :
>    - **Sources primaires** (les meilleurs du domaine, single source acceptable) : Amanda Askell pour prompt engineering Anthropic, **DAIR.AI (Elvis Saravia)**, **LearnPrompting.org (Sander Schulhoff)**, **promptingguide.ai**, **Riley Goodside**, **Simon Willison**, **Karpathy**, **Jason Wei (Few-shot Learners, CoT auteur)**, **Denny Zhou (Self-Consistency, Tree of Thoughts)**
>    - **Papers académiques arXiv** = single source acceptable (CoT Wei et al, Self-Consistency Wang et al, ToT Yao et al)
>    - **Docs officielles providers** (docs.claude.com, platform.openai.com, ai.google.dev) sur LEUR produit = single source
>    - **Anthropic sur Claude / sa propre doctrine** = single source MAIS pas extrapolable au prompt engineering général
>    - **Autres sources** (blogs, Medium, vidéos tierces) = 4+ sources convergentes obligatoire
> 7. Validation Raphael par vague (Type 2 safe → Type 1 source → Type 3 réécriture)
> 8. advisor() AVANT vague 3 ET AVANT rapport final
>
> **Mémoire forge à consulter avant lancer** : `feedback_audit_thematique_methode`, `feedback_anthropic_single_source`, `feedback_regle_scope_pas_universelle`, `Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23`

## Navigation vault — où lire selon le cas

| Si tu cherches... | Lire EN ENTIER via `mcp__forge-brain__read_note` SANS max_lines |
|-------------------|------------------------------------------------------------------|
| Méthode d'audit thématique générale | `[[methode-analyser-repo]]` (section ORDRE CANONIQUE A→B→C→D→E) |
| Comment éviter les pièges d'audit (paraphrase, attribution croisée) | `[[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]]` |
| Doctrine forge sur prompt engineering Claude | `[[comment-ecrire-claudemd]]` + `[[mcp-vs-skills-doctrine]]` |
| Pattern Karpathy applicable aux prompts | `[[pattern-vault-llm-karpathy]]` |
| Sources primaires prompt engineering (qui croire) | Voir hiérarchie sources ci-dessus + `[[07-Prompts/index-prompting]]` si présent |
| Convention 9 catégories Thariq (skills/prompts) | `[[comment-creer-skill]]` section "9 catégories" |
| Risques propagation de doctrine (verbatim Anthropic paraphrasé) | `[[methode-pivoter-doctrine]]` + `[[critique-2026-05-22-8-canoniques-chantier]]` |

**N'oublie pas de regarder aussi** :
- `Knowledge/erreurs/*` pour les erreurs d'audit passées (notamment paraphrases verbatim Anthropic, attributions croisées)
- `Knowledge/critiques/*` pour les DA précédents sur le sujet
- `07-Prompts/` pour les prompts existants à croiser

## Scope thème

**Dossier vault** : `04-Techniques/prompt-engineering/` + `07-Prompts/`

**Notes à auditer (~13)** :

`04-Techniques/prompt-engineering/` :
1. `Adaptive Thinking`
2. `Effort Levels Guide`
3. `System Prompt Design`
4. `amanda-askell-prompt-engineering`
5. `deprecated-techniques-2026`
6. `forge-prompt-machine`
7. `opus-47-design-defaults`
8. `outcome-first-prompting`
9. `over-specification-paradox`
10. `prompting-chat-cowork-code`
11. `prompting-opus47-cheatsheet`

`07-Prompts/` :
12. `System Prompt Amanda Askell`
13. `System Prompt Claude Code`
14. `Piebald-AI System Prompts`
15. `chain-of-thought`
16. `few-shot-prompting`
17. `index-prompting`

## Hiérarchie experts (priorité ce thème)

### Liste actuelle forge (à valider en étape 0)

**Anthropic / officiel** (P1) :
- Amanda Askell (Anthropic, prompt engineering thought leader)
- Anthropic prompt engineering docs (docs.claude.com)
- Boris Cherny (système prompt Claude Code)

**Académique / reconnu** (P2) :
- Lilian Weng (OpenAI, blog posts agents/prompts)
- Andrej Karpathy (prompt as program)
- Yao Fu (chain-of-thought research)
- Jason Wei (Few-shot Learners, CoT paper auteur)
- Denny Zhou (Self-Consistency, Tree of Thoughts)
- Eric Hartford (Cognitive Computations)

**Industrie** (P3) :
- DAIR.AI (Elvis Saravia — Prompt Engineering Guide reconnu)
- Riley Goodside (prompt engineering historique)
- Simon Willison (LLM tooling + prompts)
- Sander Schulhoff (LearnPrompting.org)

### Étape 0 — Valider/étendre

WebSearch : "prompt engineering expert 2026", "prompt engineering thought leader", "Anthropic Amanda Askell", "DAIR prompt engineering guide", "LearnPrompting authors", "academic prompt engineering researchers".

## Sources spécifiques à fouiller

### Officiel
- docs.claude.com/prompt-engineering
- platform.openai.com/docs (prompt engineering OpenAI)
- ai.google.dev/gemini-api/docs/prompting-strategies
- learnprompting.org (Schulhoff)
- promptingguide.ai (DAIR.AI)

### Papers (arXiv)
- "Chain-of-Thought Prompting Elicits Reasoning" (Wei et al, 2022) — arxiv.org/abs/2201.11903
- "Self-Consistency Improves Chain of Thought" (Wang et al, 2022)
- "Tree of Thoughts" (Yao et al, 2023)
- "Few-Shot Learners" (Brown et al, 2020 GPT-3 paper)
- "Constitutional AI" (Anthropic, 2022)
- Papers récents 2024-2026 sur Adaptive Thinking, Self-Refine, ReAct

### Talks publics
- Amanda Askell interviews (YouTube, podcasts)
- Karpathy "Software 3.0" YC AI Startup School
- DeepLearning.AI courses (Andrew Ng + experts)
- DAIR.AI YouTube channel

### Blogs reconnus
- lilianweng.github.io (Prompt Engineering, Agents posts)
- simonw.net / simonwillison.net
- karpathy blog/gist

### Vidéos YouTube à transcripter (skill watch)
- Amanda Askell interviews
- Karpathy "Intro to LLMs" 1h Andrej
- Lilian Weng talks
- DeepLearning.AI Prompt Engineering for Developers (course)

## Claims à vérifier (priorité)

### Techniques canoniques
- "Chain-of-Thought (CoT)" — paper Wei 2022, convergence académique
- "Few-shot prompting" — paper Brown 2020
- "Self-consistency" — Wang 2022
- "Tree of Thoughts" — Yao 2023
- "ReAct" — Yao 2023
- "Constitutional AI" — Anthropic 2022

### Verbatim à vérifier
- "Amanda Askell : <citations forge>" — vérifier sources originales
- "Outcome-first prompting" — qui a dit ça, source ?
- "Over-specification paradox" — source académique ou forge ?
- "Adaptive Thinking" — Anthropic feature ou concept général ?

### Seuils numériques
- Si des chiffres apparaissent (température, tokens, etc.) — vérifier sources

### Deprecated techniques 2026
- Vérifier que les techniques marquées "deprecated" le sont vraiment selon experts
- Chercher "prompt engineering deprecated 2026" pour convergence

## Étape F — Propagation Prompt Engineering

Si modifications notes vault, vérifier dans :

**Forge** :
- `.claude/skills/cc-prompt-ref/`
- `.claude/skills/craft-prompt/`
- `.claude/agents/*.md` (descriptions = prompts)
- CLAUDE.md (section "Comportement")
- Système prompts dans agents

**Autres repos** :
- ia_back, neo_ia : agents avec prompts customs
- Descriptions skills (3e personne canonique)

**Backlinks vault** :
- `get_backlinks` pour chaque note prompt-engineering

## Output attendu

`output/audit-vault-thematique/02-prompt-engineering/`
- A à F + rapport-final.md

---

**Commence par étape 0. advisor() avant transitions majeures.**
