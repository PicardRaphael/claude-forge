---
name: regle-scope-pas-universelle
description: "Une règle validée sur un thème n'est PAS automatiquement universelle. Toujours vérifier le scope avant de propager. Erreur évitée 23 mai 2026 : \"Anthropic single source\" propagé tel quel aux 6 audits thématiques non-Claude (RAG, fine-tuning, agents IA, prompt eng général, leaders industrie) — Raphael m'a corrigé."
trigger: propager, tous les repos, universel, scope, partout
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 931783ff-d35c-4d9c-b53d-c30bcf6f294f
---

**Verbatim Raphael** (23 mai 2026, après audit Claude Code, en lisant les 6 prompts thématiques que je venais de patcher) :
> "Tant trop pic, attention, c'est le gnostique c'était que ce qui est lié à l'entreprise [Anthropic], là c'est différent, donc ce n'est pas n'importe quoi non. Par contre, c'est toujours les meilleurs de la société, mais là, on est moins bloqué sur Anthropic"

## La règle

**Une règle validée sur un domaine spécifique n'est PAS automatiquement universelle.**

Avant de propager une règle d'un thème à un autre, **vérifier le scope d'origine** :
- Sur quel sujet la règle a été établie ?
- Le nouveau contexte est-il du même périmètre ?
- Les acteurs / experts du nouveau domaine sont-ils les mêmes ?

## L'erreur évitée

Audit Claude Code 23 mai → "Anthropic team = single source acceptable" (légitime car Anthropic = créateur Claude Code).

J'ai voulu propager cette règle aux 6 audits thématiques restants (02 à 07) en l'écrivant dans le template commun comme **règle universelle**.

**Raphael m'a corrigé** : le scope était Claude/Anthropic uniquement. Sur RAG, fine-tuning, agents IA en général, prompt engineering général, leaders industrie → Anthropic n'est qu'**un acteur parmi d'autres**, pas LA référence.

Les **vraies sources primaires** par domaine :
- **RAG** : Douwe Kiela, Patrick Lewis, Omar Khattab, Nils Reimers, Han Xiao
- **Fine-tuning** : Tim Dettmers, Edward Hu, Daniel Han, Tri Dao, Song Han
- **Agents IA** : Andrew Ng, Lilian Weng, Harrison Chase, Shunyu Yao, Joao Moura
- **Prompt engineering** : Amanda Askell, DAIR.AI, LearnPrompting, Jason Wei, Denny Zhou
- **Leaders industrie** : LinkedIn/X officiel + datasheets providers + presse tech reconnue

## How to apply

**Avant de propager une règle validée d'un audit/contexte à un autre** :

1. **Identifier le scope d'origine** : sur quel domaine la règle a été établie ?
2. **Demander : "cette règle s'applique-t-elle hors de son scope d'origine ?"** — si pas évident, demander à Raphael
3. **Si tu généralises** : tester sur 1-2 cas du nouveau domaine avant propagation large
4. **Si tu écris une règle dans un template commun** : préciser explicitement le scope d'application

## Pattern à mémoriser

> "Provider/auteur officiel sur SON propre produit ou SA propre recherche = single source acceptable."
> "Hors de son scope = règle 4+ sources."

Cette formulation **universalise correctement** sans tomber dans le piège "Anthropic universal" :
- Anthropic single source sur Claude/Anthropic ✓
- OpenAI single source sur GPT ✓
- Karpathy single source sur ses patterns ✓
- Dettmers single source sur QLoRA ✓
- Anthropic sur fine-tuning général = 4+ sources requis ✗

## Why

Audit Claude Code a validé Anthropic single source POUR LE THÈME ANTHROPIC. Extrapoler cette règle aux autres thèmes aurait écrasé les vraies sources primaires de chaque domaine. C'est exactement le pattern d'erreur que l'audit 23 mai a corrigé dans le vault forge (Justin Young 2-agent extrapolation, lethal trifecta attribué à Thariq au lieu de Willison) — réitérer cette erreur sur la méthode d'audit elle-même = méta-régression.

## Cas d'origine — Anthropic single source (consolidé ici)

La règle est née de ce cas : sur un audit Claude Code, **Anthropic team/docs/blog = single source acceptable** (créateur de Claude). Idem OpenAI sur GPT, Google sur Gemini, Karpathy sur ses patterns, Dettmers sur QLoRA — **provider/auteur officiel sur SON produit ou SA recherche = single source**. Hors scope = 4+ sources convergentes (blogs/Medium), 2+ pour presse tech reconnue. Papers peer-reviewed (ACL/EMNLP/NeurIPS/ICML) = single source. Sur les thèmes larges (RAG → Kiela/Lewis/Khattab ; fine-tuning → Dettmers/Hu/Han ; agents → Ng/Weng/Chase), Anthropic n'est **qu'un acteur parmi d'autres**, pas LA référence.

## Lien

- [[audit-thematique-claims-vault]] — méthode validée audit thématique

Consolide depuis : [[feedback_anthropic_single_source]] (fusionné le 1er juin 2026 — cas d'origine de la règle générale de scope).
