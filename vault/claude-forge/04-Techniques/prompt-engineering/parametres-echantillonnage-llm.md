---
titre: "Paramètres d'échantillonnage LLM par cas d'usage — temperature, top_p, top_k, penalties, seed"
resume: "Réglages de sampling à l'inférence calibrés par cas d'usage (extraction/RAG/chatbot/agent/créatif), qualifiés par provider. Les 5 gotchas qui distinguent le signal du folklore : non-portabilité, temp XOR top_p, reasoning verrouille la temp, penalties=0, seed≠déterminisme"
aliases:
  - "paramètres échantillonnage llm"
  - "temperature top_p top_k réglages"
  - "sampling parameters llm"
  - "réglages température ia par cas d'usage"
  - "decoding parameters cas d'usage"
  - "temperature rag chatbot agent extraction"
domaine: ia
type: technique
derniere-maj: 2026-09-05
auteur: claude
sources:
  - "https://platform.claude.com/docs/en/build-with-claude/extended-thinking"
  - "https://platform.openai.com/docs/guides/reasoning"
  - "https://developers.openai.com/api/docs/guides/advanced-usage"
tags:
  - "#type/technique"
  - "#domaine/ia"
  - "#domaine/prompt-engineering"
---

> [!warning] Le piège des « tableaux de température » de blog
> 90 % des tableaux « temperature 0.7 pour le chat » trouvés en ligne sont du **folklore** : ils omettent le provider (la plage n'est PAS la même), conseillent de tuner `temperature` ET `top_p` ensemble (erreur), et donnent des nombres pour des modèles de raisonnement qui **ignorent ou interdisent** la température. Cette note part des contraintes vérifiées en source primaire, puis donne les réglages.

## TL;DR — les 5 faits qui tuent le folklore

1. **La température n'est PAS portable entre providers.** Anthropic : **0 → 1**. OpenAI / Azure : **0 → 2**. « 0.7 » ne veut rien dire sans nommer le modèle. (VÉRIFIÉ-SOURCE docs Anthropic + OpenAI)
2. **`temperature` XOR `top_p`, jamais les deux.** Doctrine officielle OpenAI ET Anthropic (ils retravaillent la même distribution softmax). Sur **Claude 4.x, fournir les deux = erreur 400 dure** (`temperature and top_p cannot both be specified`). (VÉRIFIÉ-SOURCE)
3. **Les modèles/modes de raisonnement verrouillent la température** — inversion du folklore « agent → basse température » :
   - **OpenAI o-series / GPT-5 reasoning** : `temperature`, `top_p`, `n` **figés à 1**, penalties figées à 0. Tenter de les changer → erreur. (VÉRIFIÉ-SOURCE docs reasoning)
   - **Claude extended thinking** : `temperature`/`top_k` **incompatibles**, `top_p` accepté seulement entre **0.95 et 1**. Sur **Opus 4.7/4.8, toute valeur non-défaut → 400** ; il faut **omettre** ces champs et piloter par le prompt. (VÉRIFIÉ-SOURCE docs extended-thinking + migration guide)
4. **`frequency_penalty` / `presence_penalty` = 0 par défaut pour une raison.** À **éviter** sur RAG, code, extraction (répétition légitime de terminologie/syntaxe). À sortir uniquement pour un problème de répétition précis en génération longue. (VÉRIFIÉ-SOURCE docs OpenAI advanced-usage)
5. **`seed` ne garantit PAS le déterminisme.** Best-effort uniquement : floating-point, hardware, `system_fingerprint` qui change quand le provider met à jour le backend. Même `temperature=0` produit une variance résiduelle. **Toujours valider les sorties**, jamais supposer la reproductibilité. (VÉRIFIÉ-SOURCE docs OpenAI determinism)

## Les paramètres (mécanique courte)

| Paramètre | Effet | Plage | Centré |
|---|---|---|---|
| `temperature` | Aplatit/durcit la distribution avant le sampling | Anthropic 0–1 · OpenAI 0–2 | défaut 1 |
| `top_p` (nucleus) | Garde le plus petit ensemble de tokens dont la masse ≥ p | 0–1 | défaut 1 |
| `top_k` | Garde les k tokens les plus probables (dispo selon API) | entier | — |
| `frequency_penalty` | Pénalise un token ∝ son **nombre d'occurrences** déjà générées | -2 → 2 | 0 |
| `presence_penalty` | Pénalise un token dès qu'il est **apparu une fois** | -2 → 2 | 0 |
| `repetition_penalty` (vLLM/HF) | **Multiplicatif** : >1 pénalise les répétitions, <1 les encourage | ~0.5–2 | **1.0** |
| `seed` | Reproductibilité best-effort (cf gotcha #5) | entier | — |
| `max_tokens` / `stop` | Bornes de sortie | — | — |

> ⚠️ `repetition_penalty` (centré sur **1.0**, multiplicatif) ≠ `frequency`/`presence_penalty` (centrés sur **0**, additifs). Ne pas confondre les deux familles entre serving self-hosted (vLLM) et API OpenAI.

## Réglages par cas d'usage

> Convention : pour Anthropic, « bas » = proche de 0 ; pour OpenAI, mêmes valeurs absolues (0–1 suffit, pas besoin de monter au-delà de 1.2 — au-delà l'output devient incohérent). **On règle `temperature` SEULE, `top_p` reste à 1.**

| Cas d'usage | Temperature | Penalties | Notes |
|---|---|---|---|
| **Extraction / classification / function calling** | **0.0 – 0.2** | 0 / 0 | Déterminisme prioritaire. Penalties OFF (répétition de clés/labels légitime). Coupler à un structured output (cf [[reference-technique-stack-ia]] §8.1). |
| **RAG (génération ancrée)** | **0.2 – 0.5** | 0 / 0 | Assez bas pour rester ancré dans le contexte récupéré, assez haut pour une lecture naturelle. **Jamais de penalties** : le modèle doit reproduire fidèlement la terminologie source. |
| **Chatbot support** | **0.3 – 0.6** | 0 / 0 | Cohérence factuelle > variété. Bas de la plage pour les réponses procédurales/FAQ. |
| **Conversation / rédaction** | **0.5 – 0.7** | 0 (ou faible) | Équilibre. Une petite `frequency_penalty` (0.1–0.3) seulement si le ton devient répétitif sur du texte long. |
| **Créatif / brainstorming** | **0.7 – 1.0** | optionnel | Sur Claude moderne, **la température n'est pas le bon levier de variété** → préférer le prompt (cf [[opus-47-design-defaults]]). |
| **Agent / tool-use (modèle classique)** | **0.0 – 0.3** | 0 / 0 | Décisions d'outils stables et reproductibles. |
| **Agent / tool-use (reasoning model)** | **n/a — omettre** | n/a | o-series/GPT-5 reasoning = temp figée à 1 ; Claude extended thinking = omettre temp/top_k. **On ne règle rien, on pilote par le prompt.** (cf gotcha #3) |

> Règle terrain : **partir bas, monter jusqu'à l'équilibre précision/variété de TA tâche.** Une fois en prod (extraction, classif, code, tool-use, RAG, agents), le défaut cesse d'être bon — mais le bon réglage est rarement « plus haut ».

## Production / batch

- **Production > dev** côté stabilité : viser 0.2–0.5 en prod là où le dev explorait à 0.7–1.0.
- Au-delà de **~1.2** (OpenAI) : incohérence, pas de « créativité » gagnée — la créativité vient du prompt, pas de la température.

## Liens

- [[reference-technique-stack-ia]] — référence longue ingénierie LLM (cette note comble son trou « sampling »)
- [[opus-47-design-defaults]] — sur Claude moderne, la variété design passe par le prompt, pas la température
- [[serving-inference-optimisation]] — sampling côté serving self-hosted (vLLM/SGLang)
- [[architecture-openai-api]] · [[architecture-gemini-api]] — specs par provider
- [[prompting-opus47-cheatsheet]] — pilotage par le prompt

---

## AJOUT 5 septembre 2026 — les boutons de raisonnement, par fournisseur

Le gotcha n°3 ci-dessus (« les modèles de raisonnement verrouillent la température ») a une contrepartie : **quand on ne peut plus régler le sampling, on règle le raisonnement.** Chaque fournisseur expose désormais son propre bouton, et ils ne portent ni le même nom ni les mêmes valeurs.

| Fournisseur | Paramètre | Valeurs | Défaut | Portée |
|---|---|---|---|---|
| **Anthropic** | `effort` | `low` · `medium` · `high` · `xhigh` · `max` | `high` | Gouverne **toute** la dépense de tokens du tour : thinking, texte de réponse et tool calls — pas seulement un budget de réflexion séparé |
| **OpenAI** | `reasoning_effort` + **`verbosity`** | effort : `minimal`/`low`/… (⚠️ **pas de `none` sur GPT-6 Astra**) · verbosity : longueur de la **réponse finale**, distincte de la longueur du raisonnement | — | GPT-5.x et suivants. `verbosity` répond aussi à une surcharge en langage naturel dans le prompt |
| **Google** | **`thinking_level`** | `minimal` · `low` · `medium` · `high` (support variable selon modèle) | **thinking dynamique** si non fixé | Gemini 2.5 et 3.x. Remplace `thinkingBudget` |

### Ce qu'il faut retenir par fournisseur

**Anthropic** — l'effort est le contrôle principal. Sur **Opus 5**, `thinking: {type: "disabled"}` n'est autorisé qu'à effort `high` ou en dessous : le combiner avec `xhigh` ou `max` renvoie une **erreur 400**, changement cassant vs Opus 4.8. Et les niveaux ne sont **pas comparables d'un modèle à l'autre** : un sweep fait sur un modèle doit être refait sur le suivant (cf [[doctrine-par-modele-opus5-fable5]]).

**OpenAI** — deux boutons distincts, à ne pas confondre : `reasoning_effort` pilote combien le modèle réfléchit, `verbosity` combien il écrit. Recommandation officielle : **verbosity haute pour le code**, effort `minimal`/`low` pour le travail de routine, effort lourd réservé aux problèmes réellement complexes. **GPT-6 Astra** (3 sept. 2026) durcit les contraintes : pas de niveau d'effort `none`, **pas de `temperature`/`top_p` custom**, pas de logprobs, et le tool calling exige la **Responses API**.

**Google** — `thinking_level` remplace `thinkingBudget` sur Gemini 3.x. Par défaut, *« Gemini models engage in dynamic thinking… automatically adjusting the amount of reasoning effort based on the complexity of the request »* : ne rien fixer est un choix valide. Et surtout, **seule dépréciation explicite vérifiée des trois fournisseurs** : sur Gemini 3.x, garder `temperature`/`top_p`/`top_k` à leurs valeurs par défaut — verbatim *« Although you can modify these parameters, we strongly recommend keeping them at their default values for Gemini 3.x models. Changing these parameters (for example, setting the temperature below 1.0) can cause unexpected behavior »*. Cela étend le gotcha n°3 au-delà des seuls modes de raisonnement : sur Gemini 3.x, c'est **toute** la famille qui verrouille le sampling.

### Règle transversale

Le tableau « réglages par cas d'usage » plus haut ne s'applique qu'aux modèles **sans** raisonnement natif. Dès qu'un modèle raisonne, la séquence est : ne pas toucher au sampling → régler le bouton de raisonnement → piloter le reste par le prompt.

Sources vérifiées le 5 sept. 2026 : `ai.google.dev/gemini-api/docs/thinking`, `ai.google.dev/gemini-api/docs/prompting-strategies`, `developers.openai.com/api/docs/changelog`, `platform.claude.com/docs/en/models/fable-5-1/overview`.
