---
titre: "Erreur — chiffres précis hallucinés dans les outputs de deep research LLM tiers"
resume: "Les LLM tiers (Gemini deep research, ChatGPT) fabriquent fréquemment des numéros de version, dates et stats précises ; WebFetch source primaire obligatoire avant toute action structurelle."
aliases:
  - "llm deep research hallucination chiffres"
  - "gemini version numbers hallucinated"
  - "deep research LLM claims numériques"
  - "webfetch avant deep research"
  - "chiffres hallucinés LLM tiers"
type: erreur
domaine: verification
derniere-maj: 2026-07-07
auteur: claude
tags:
  - "#type/erreur"
  - "#domaine/verification"
  - "#domaine/llm"
---

## Contexte

28 mai 2026 — Gemini deep research affirmait : *"bug #60237 fixé dans Claude Code v1.21.1 et v1.22"*. WebFetch CHANGELOG officiel : ces versions n'existent pas (CC versionné `v2.1.x`). Fix réel = v2.1.147. Les numéros étaient hallucinés ; le fait sous-jacent (bug existe, fix existe) était correct.

**Mécanisme** : les LLM tiers mélangent knowledge cutoff + invention plausible pour combler les trous. Les chiffres précis (versions, dates, étoiles, comptes) sont le vecteur principal du biais — ils sonnent crédibles et passent sans friction dans les décisions.

## Règle

Avant toute action structurelle (restructuration vault, mise à jour doctrine, promotion d'un outil), scanner **tous les chiffres précis** d'un document deep research LLM tiers :
- Claim "version X.Y.Z fixe le bug" → WebFetch raw CHANGELOG avant de croire/citer
- Claim "repo X a N étoiles, créé en YYYY" → WebFetch GitHub direct
- Claim "Boris fait N sessions parallèles" → vérifier source primaire (site Boris, talk Anthropic)

Le **fait qualitatif** peut être vrai même quand les **chiffres sont faux** — distinguer les deux dans le verdict.

## Méthode standard (amendement 28 mai 2026)

À la réception d'un document LLM deep research, avant d'utiliser le document pour décision ou restructuration :

1. Parcourir le document en mode "chasse aux chiffres précis" (versions, dates, étoiles, citations verbatim, comptes de commits/stars).
2. WebFetch source primaire ciblée sur chaque chiffre structurant.
3. Marquer les chiffres non-vérifiables `[SOURCE MANQUANTE]` ; retirer les plus risqués.
4. Seulement ensuite utiliser le document pour prescription.

Application du principe [[methode-analyser-repo]] (analyser le RÉEL avant prescription) aux documents tiers.

## Distinction avec les hallucinations self-forge

Ce pattern concerne les **outputs entrants** de LLM tiers utilisés comme source de décision. Les fabrications dans le vault forge lui-même (paraphrases tweet, verbatim inventés) sont documentées dans [[erreur-4-fabrications-vault-prompt-engineering-2026-05-23]] et [[erreur-22-claims-fausses-vault-claude-code-2026-05-23]].

## Liens

- [[erreur-4-fabrications-vault-prompt-engineering-2026-05-23]] — fabrications self-forge lors de cc-news/capitalisation
- [[erreur-audit-rag-11-faux-2026-05-23]] — chiffres précis sans source dans notes vault
- [[methode-analyser-repo]] — analyser le RÉEL avant prescription (symétrique pour documents tiers)
