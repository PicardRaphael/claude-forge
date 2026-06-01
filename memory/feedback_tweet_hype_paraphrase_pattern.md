---
name: tweet-hype-paraphrase-non-verifiee-pattern
description: 4e occurrence pattern tweet/post hype → paraphrase verbatim non vérifiée → vérification croisée Anthropic docs montre slug/attribution faux. Toujours WebFetch direct docs Anthropic avant capitaliser claim viral.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 931783ff-d35c-4d9c-b53d-c30bcf6f294f
---

## Le pattern (4 occurrences en 2 jours)

| # | Source | Claim viral | Réalité docs Anthropic |
|---|--------|-------------|------------------------|
| 1 | Justin Young 2-agent article | "Init Opus + Coding Sonnet split" | Footnote 1 : "harness was otherwise identical" — pas de split modèles |
| 2 | Simon Willison live blog CwC London | "Angela Jiang advisor 5× cost reduction" | Brad Abrams (pas Angela), pas de chiffre "5×", verbatim "close to Opus-level intelligence at much lower prices" |
| 3 | Agent SDK overview citation | "Claude decides when to parallelize — you're defining the capability, not the scheduling" | Verbatim docs = "Claude decides when to call a tool" + "Skills are model-invoked" — formule paraphrasée |
| 4 | Tweet @_vmlops 23 mai 2026 | "Anthropic quietly shipped /workflows in Claude Code" | Slug "/workflows" inexistant docs (404). Feature canonique = **Programmatic Tool Calling (PTC)**. Principe juste, slug faux |

## La règle anti-pattern

**Avant de capitaliser une claim virale (tweet, live blog, article tiers) comme verbatim Anthropic** :

1. **WebFetch direct** la page docs Anthropic supposée source (`code.claude.com/docs/...`, `platform.claude.com/docs/...`, `anthropic.com/engineering/...`)
2. **404 ou 0 résultat WebSearch sur slug exact** → claim non canonique, à reformuler "principe attesté mais slug X non vérifié"
3. **Si verbatim cité** → grep mot pour mot dans docs Anthropic. Si pas trouvé → "paraphrase pédagogique" pas "verbatim"
4. **Attribution** (qui a dit quoi) → vérifier source primaire (LinkedIn officiel, X officiel, talk Anthropic vidéo) avant relayage

## Cause racine

Sources tierces (DevOps engineers, journalists, live bloggers) :
- **Inventent des slugs** plus catchy que les noms officiels Anthropic (`/workflows` vs `Programmatic Tool Calling`)
- **Inventent des chiffres** pour densité pédagogique ("5×", "80%")
- **Paraphrasent** verbatim pour formules élégantes (`Claude decides when to parallelize`)
- **Coquilles propagées** sans correction (Angela Kiang → Jiang → propagé comme vérité)

Tous ces patterns convergent : **la source tierce améliore l'original pour la lisibilité**, et forge propage l'amélioration comme verbatim.

## How to apply

Dans tout audit thématique vault, audit forge dogfooding, ou capitalisation de tweet/article tiers :

1. **Trianguler à 2-3 sources** AVANT de marquer ✅ canonique pour claim viral
2. **WebFetch direct docs Anthropic** sur slug exact cité
3. **Disclaimer explicite si principe canonique mais slug/chiffre/attribution non vérifié** : "principe attesté multi-sources mais formule `X` n'apparaît pas verbatim docs"
4. **Capitaliser le principe canonique** sous son vrai nom officiel (PTC, pas /workflows ; Advisor Strategy Brad Abrams, pas Angela Jiang 5×)
5. **Citer la source tierce comme illustration externe**, pas comme source primaire

## Liens

- [[feedback_regle_scope_pas_universelle]] — hiérarchie sources scopée (provider single-source sur SON produit)
- [[feedback_regle_scope_pas_universelle]] — règles validées un domaine pas universelles
- [[feedback_audit_thematique_methode]] — méthode validée audit
- [[Knowledge/erreurs/erreur-22-claims-fausses-vault-claude-code-2026-05-23]] — 22 claims fausses détectées (cas 1-3 ci-dessus)
- [[programmatic-tool-calling]] — note canonique créée 23 mai sur cas 4 (PTC vs slug /workflows)
