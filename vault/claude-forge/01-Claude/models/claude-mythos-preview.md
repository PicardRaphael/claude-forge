---
titre: "Claude Mythos Preview"
resume: "Modele frontier Anthropic d'avril 2026 (SWE-bench 93.9%, zero-day autonome, acces Project Glasswing) ; deprecie depuis le 9 juin 2026, retrait « To be announced » au 30 sept. 2026, lignee continuee par Mythos 5 / 5.1"
aliases:
  - "mythos"
  - "claude-mythos"
  - "glasswing"
  - "claude-mythos-preview"
  - "mythos preview"
type: modele
derniere-maj: 2026-09-30
auteur: claude
sources:
  - "https://www.anthropic.com/news/claude-mythos-preview"
  - "https://platform.claude.com/docs/en/about-claude/model-deprecations"
tags:
  - "#type/modele"
  - "#domaine/claude"
  - "#domaine/securite"
---

> [!warning] DÉPRÉCIÉ depuis le 9 juin 2026 — retrait non daté
> Page officielle *Model deprecations* au 30 sept. 2026 : `claude-mythos-preview` | **Deprecated** | June 9, 2026 | **To be announced**. Le modèle n'est donc pas retiré côté API Anthropic ; aucune date de retrait n'est publiée. La lignée Mythos continue via Mythos 5 et Mythos 5.1 (accès limité, Project Glasswing), jumeaux de [[Fable 5]] et [[Fable 5.1]]. Le contenu ci-dessous décrit le modèle tel qu'annoncé en avril 2026 — historique.
>
> Historique de la note : une version antérieure affirmait un retrait effectif au 21 juillet 2026. Aucune source primaire n'a été retrouvée pour cette date (ni dans le CHANGELOG Claude Code, ni dans la page deprecations) ; assertion remplacée le 30 sept. 2026.

## Specifications

- **Provider** : Anthropic
- **Date annonce** : 7 avril 2026
- **SWE-bench Verified** : 93.9% (vs [[Opus 4.7]] = 87.6%, Opus 4.6 = 80.8%)
- **Pricing** : 5x le prix d'Opus 4.6
- **Acces** : Gated Research Preview uniquement (Project Glasswing)

## Capacites

- Modele general-purpose, mais capacites cybersecurite exceptionnelles
- Decouvre des zero-day **autonomement** sans instruction specifique
- RCE 17 ans FreeBSD (CVE-2026-4747) — exploite sans intervention humaine
- Bug 27 ans OpenBSD decouvert et exploite
- Firefox 147 JS engine : 181 exploits, register control 29 fois
- Anthropic precise : pas d'entrainement specifique exploitation, c'est emergent

## Project Glasswing

- Acces restreint a ~40 partenaires : Amazon, Apple, Google, Microsoft, Nvidia, CrowdStrike, Palo Alto, JPMorgan, Linux Foundation, etc.
- Anthropic engage $100M en credits usage
- White House s'oppose a l'extension a 70 orgs supplementaires
- Termes : usage restreint a la cybersecurite defensive
- Validateurs humains d'accord avec severity assessment dans 89% des cas (198 rapports)

## Quand utiliser

- Acces restreint — uniquement via Project Glasswing
- Cybersecurite defensive : audit, detection de vulnerabilites
- UK AISI : complete des "difficult multistep infiltration challenges" qu'aucun autre modele n'avait reussi
- <1% des vulns trouvees par Mythos sont patchees a ce jour

## Liens

- [[Opus 4.7]]
- [[Fable 5.1]]
- [[MOC-Modeles]]
