---
titre: "How we contain Claude — architecture de containment Anthropic (28 mai 2026)"
resume: "Article engineering Anthropic (McGuinness et al., 28 mai 2026) : couches de containment cross-produits — sandbox OS (-84 % de prompts), auto mode (0,4 % bénins bloqués / 17 % risqués passants / 83 % comportements overeager attrapés), phishing exfiltration réussie 24/25 en test, vuln hooks settings.json exécutés avant le trust prompt. « The deterministic boundary is what gets hit when everything probabilistic misses »"
aliases:
  - "how we contain claude"
  - "containment Claude Anthropic"
  - "deterministic boundary"
  - "sandbox OS claude code"
  - "stats auto mode containment"
derniere-maj: 2026-07-27
auteur: claude
type: feature
sources:
  - "https://www.anthropic.com/engineering/how-we-contain-claude"
  - "https://simonwillison.net/2026/May/30/how-we-contain-claude/"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#domaine/securite"
---

# How we contain Claude (Anthropic engineering, 28 mai 2026)

> Article de Kevin McGuinness, Grace, De Jonghe, Eaton, Ribbink — architecture de containment de Claude à travers les produits (Code, Cowork, browser). Couvert par Simon Willison le 30 mai. **Capitalisé le 27 juil. 2026 depuis les synthèses d'un agent de veille + couverture Willison — relire l'article original avant citation externe des chiffres.** Découvert manquant au vault lors du run cc-news approfondi (l'article était sorti pendant la fenêtre Code with Claude, jamais capitalisé).

## Les chiffres clés

- Avant sandbox : **93 % des prompts de permission étaient approuvés** (fatigue de validation = les humains disent oui) → l'argument pour déplacer la sécurité vers des frontières structurelles.
- **Sandbox OS** (filesystem + réseau) : **−84 % de prompts de permission** — la majorité des actions deviennent sûres par construction au lieu d'être arbitrées par l'humain.
- **Auto mode** (classifier) : **0,4 %** d'actions bénignes bloquées à tort · **17 %** d'actions risquées qui passent (d'où les couches supplémentaires) · **83 %** des comportements « overeager » (zèle excessif de l'agent) attrapés.
- Test d'exfiltration par phishing : réussi **24/25** — la démonstration que le probabiliste seul ne suffit pas.
- Vulnérabilité documentée : **hooks de `.claude/settings.json` exécutés AVANT le trust prompt** du dossier (depuis corrigée/mitigée côté produit — vérifier l'état courant avant de citer).

## La phrase doctrine

> « **The deterministic boundary is what gets hit when everything probabilistic misses.** »

C'est exactement la doctrine forge 22 mai ([[raisonnement-22mai-doctrine-vs-enforcement]]) : advisory (CLAUDE.md/rules, ~80 % compliance) pour le workflow, **déterministe (hooks/sandbox) pour ce qui doit tenir à 100 %** — validée empiriquement par Anthropic à l'échelle.

## Pertinence forge

- Valide la rule forge `.claude/rules/contenu-externe-non-fiable.md` et [[agents-securite]] (le 24/25 phishing = lethal trifecta en pratique) ainsi que le choix hooks lint/security/scope.
- Le chiffre 93 % d'approbation = l'argument contre les gardes-fous « à prompt » : l'humain fatigué approuve tout. Préférer les frontières structurelles (deny-list, sandbox, hook exit 2).
- À croiser avec le fireside 21 juil. ([[fireside-cat-wu-thariq-aiewf-2026]]) : classifier Sonnet par tool call, credential injection.

## Wikilinks

- [[raisonnement-22mai-doctrine-vs-enforcement]] — la doctrine forge que l'article valide
- [[agents-securite]] — doctrine sécurité agents forge
- [[fireside-cat-wu-thariq-aiewf-2026]] — état sécurité juillet 2026
- [[comment-creer-hook]] — le mécanisme déterministe côté forge
