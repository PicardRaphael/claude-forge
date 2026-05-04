---
titre: "Claude Mythos Preview"
resume: "Modele frontier Anthropic, SWE-bench 93.9%, zero-day autonome, acces restreint Project Glasswing"
type: modele
provider: anthropic
date: 2026-04-07
derniere-maj: 2026-05-04
auteur: claude
tags:
  - "#type/modele"
  - "#domaine/modeles"
  - "#domaine/securite"
---

# Claude Mythos Preview

## Specs

- **Provider** : Anthropic
- **Date annonce** : 7 avril 2026
- **SWE-bench Verified** : 93.9% (vs Opus 4.6 = 80.8%)
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

## Contexte

- UK AISI : pas significativement meilleur sur taches individuelles, mais complete des "difficult multistep infiltration challenges" qu'aucun autre modele n'avait reussi
- <1% des vulns trouvees par Mythos sont patchees a ce jour
- Risque : modeles open-weight rattraperont sans les memes restrictions d'acces

## Liens

- [[Project Glasswing]]
- [[Claude Security]]
- [[Opus 4.7]]
