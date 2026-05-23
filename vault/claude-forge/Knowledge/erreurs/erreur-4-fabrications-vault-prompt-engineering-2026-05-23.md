---
titre: "Erreur — 4 fabrications dans le thème prompt engineering (audit 23 mai 2026)"
resume: "Audit thématique prompt engineering vault forge : 4 verbatim/chiffres fabriqués + 4 attributions fausses sur 17 notes. Pattern récurrent tweet-paraphrase-non-vérifiée (5e occurrence en 2 jours)."
aliases:
  - "erreur audit prompt-engineering 23 mai"
  - "4 fabrications prompt engineering"
  - "fabrications vault PE 2026"
  - "audit PE drifts"
type: erreur
domaine: vault
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "[[methode-analyser-repo]]"
  - "[[feedback_audit_thematique_methode]]"
  - "[[feedback_tweet_hype_paraphrase_pattern]]"
  - "[[feedback_webfetch_avant_subagents_audit]]"
tags:
  - "#type/erreur"
  - "#domaine/vault"
  - "#domaine/prompt-engineering"
---

## Contexte

Audit thématique vault forge — thème prompt engineering (17 notes, 57 claims). Méthode A→B→C→D→E + propagation F appliquée le 23 mai 2026. Suite à l'audit Claude Code de la veille (22 claims fausses sur 95 = 23%), ratio observé sur prompt engineering : **8 drifts factuels / 57 claims = 14%**.

## Les 4 fabrications

### 1. Verbatim OpenAI fabriqué (Type 1 fort impact, cité 2×)

Quote attribuée au GPT-5.5 Prompting Guide :
> ❌ "The prompt patterns you spent months perfecting for GPT-5.2 may be actively making GPT-5.5 worse."

**Réalité** : WebFetch direct du doc OpenAI — cette phrase N'EXISTE PAS. Verbatim canonique réel :
> ✅ "Legacy prompts often over-specify the process because earlier models needed more help staying on track. With GPT-5.5, that can add noise, narrow the model's search space, or lead to overly mechanical answers."

**Impact** : citée dans `outcome-first-prompting.md` ET `deprecated-techniques-2026.md` (duplication cross-note).

### 2. "15 échanges = Claude oublie décisions" inventé (Type 2)

Chiffre forgé dans `forge-prompt-machine.md` principe 7. **Lost in the Middle** (Liu et al 2024, arxiv 2307.03172) parle de **positions/tokens**, jamais de tours conversationnels. Le "15" est une projection forge non-supportée.

### 3. "Soul document ~30 000 mots" approximation presse (Type 2)

Chiffre officiel Anthropic = **80 pages / 35 000+ tokens (~26k mots)**. "30 000 mots" était une approximation presse répétée sans vérification.

### 4. "ALL-CAPS exception sécurité absolue" inverse de doctrine Anthropic (Type 3)

`deprecated-techniques-2026.md` section 8 disait : *"Contraintes de sécurité absolues — là les majuscules restent justifiées."*

**Verbatim Anthropic** (vérifié WebFetch) : *"The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."*

→ Doctrine forge **inverse** de la recommandation Anthropic officielle.

## Les 4 attributions fausses

### 5. Sculpting paper (Type 1)

Forge disait : "Papier connexe Sculpting (arXiv 2510.22251) — UCL, Mikinka". 
**Réel** : auteur = **Imran Khan** (indépendant), titre = "You Don't Need Prompt Engineering Anymore: The Prompting Inversion", oct 2025. Distinct du paper UCL Mikinka 2601.00880.

### 6. "Let's think step by step" attribué à Wei 2022 (Type 1)

`chain-of-thought.md` mentionnait CoT comme source canonique. **Réel** : "Let's think step by step" = **Kojima et al 2022** (arxiv 2205.11916, "Zero-Shot Reasoners"), distinct du paper CoT Wei et al 2022 (= few-shot CoT avec démonstrations).

### 7. Quote "give models reasons why" attribuée à claude-character (Type 1)

`amanda-askell-prompt-engineering.md` section 11. WebFetch direct anthropic.com/research/claude-character : verbatim **absent**. Vraie source = interview TIME janvier 2026.

### 8. Date update Askell system prompt "mi-avril 2026" (Type 1)

`System Prompt Amanda Askell.md` + `amanda-askell-prompt-engineering.md`. **Réel** : tweet août 2025 (X.com 1953147658031513860).

## Pattern récurrent identifié

5e occurrence en 2 jours du pattern documenté dans [[feedback_tweet_hype_paraphrase_pattern]] :
- Audit Claude Code 22 mai : Justin Young split inventé, Angela Jiang 5× advisor, "Claude decides parallelize" paraphrase
- Audit prompt engineering 23 mai : verbatim OpenAI fabriqué, Sculpting attribution, soul document chiffre, ALL-CAPS doctrine inversée

**Mécanisme** : lors de cc-news ou capitalisation web, les paraphrases pédagogiques d'articles tiers (Medium, blogs, podcasts) sont relayées comme verbatim provider officiel. Le drift s'installe quand la note vault est ensuite citée dans skills/agents/CLAUDE.md sans re-vérification.

## Méthode anti-régression validée

[[feedback_webfetch_avant_subagents_audit]] créé pendant cet audit : **mini-phase A.5** entre checkpoint A et phase B sub-agents.

3-6 WebFetch directs sur sources primaires suspectes (signaux : arXiv IDs incohérents, verbatim "magique" avec chiffres précis, auteurs obscurs porteurs d'une doctrine entière). Gain wall-time : ~30 min, évite que 6 sub-agents inventent une vérif autour d'un fantôme.

## How to apply (audits futurs RAG, agents-ia, fine-tuning)

1. Lors de la lecture des notes (phase A), flagger immédiatement tout claim avec :
   - arXiv ID + auteur + chiffres précis (305 prompts, 11 modèles, S*=0.509)
   - Verbatim attribué à un doc officiel (Anthropic, OpenAI, Google)
   - Date précise sur un événement vérifiable
2. Phase A.5 : WebFetch directs des sources primaires sur ces flags AVANT dispatch sub-agents
3. Injecter résultats (✅/⚠️/❌) dans les briefs sub-agents — terrain déminé
4. Self-verify FAUX fort impact phase C (cf [[feedback_audit_thematique_methode]])

## Liens

- [[methode-analyser-repo]] — méthode A→B→C→D→E
- [[feedback_audit_thematique_methode]] — sub-agents par cluster
- [[feedback_webfetch_avant_subagents_audit]] — phase A.5
- [[feedback_tweet_hype_paraphrase_pattern]] — pattern récidiviste
- [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — audit thématique précédent
