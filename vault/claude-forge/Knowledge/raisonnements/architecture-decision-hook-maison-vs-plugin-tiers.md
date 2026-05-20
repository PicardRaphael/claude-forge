---
titre: "Hook maison vs plugin tiers pour enforcement TDD — raisonnement décision"
resume: "Premier instinct = plugin populaire (tdd-guard, 1.8k stars, marketplace Anthropic). Décision finale = hook maison 150L. L'argument décisif n'est pas le bus factor, c'est que le plugin utilise un LLM pour valider — non-déterminisme dans un guard = antipattern."
aliases:
  - hook maison vs plugin
  - enforcement deterministe vs LLM
  - tdd-guard plugin decision
  - guard determinism antipattern
  - choisir hook vs plugin tiers
  - claude code enforcement choice
type: raisonnement
domaine: claude-code
derniere-maj: 2026-05-19
auteur: claude
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#domaine/hooks"
---

## Problème

neo_ia passe en TDD strict. Il faut un enforcement bloquant (sinon rules advisory = 80% compliance, cf. `advisory-rules-insuffisantes`). Quelle techno : plugin Claude Code tiers populaire (tdd-guard de Nizar Selander), ou hook Python maison ?

## Contexte

- Repo neo_ia, équipe ~3 devs, Claude Code écrit tout le code
- Plugin tdd-guard : 1.8k stars GitHub, marketplace officielle Anthropic (101 plugins), star Boris Cherny, MIT
- Validation IA via Claude Sonnet à chaque Edit/Write
- Plugin pytest natif `tdd-guard-pytest` génère `test.json`
- Repo a déjà 9 hooks Python maison fonctionnels (architect-guard, commit-guard, marker-protect)
- Vault contient `marker-ttl-blocage-agents` : guards doivent être existence-binaire, jamais TTL ou logique complexe

## Chaîne de raisonnement

1. **Instinct initial : Option A (plugin tdd-guard)** — populaire, marketplace officielle, validation IA sophistiquée, "on ne réinvente pas la roue"
2. **Vérification "officiel" et adoption enterprise** — résultat : aucune référence Fortune 500, juste 1 mainteneur en Suède + star Boris (anecdotique). Bus factor faible, mais pas bloquant en soi
3. **Première reco modifiée : Option C (A + backup B)** — plugin + hook maison prêt en backup, "prudence"
4. **Appel advisor** — coupe court : "ne pas attendre le DA, sa réponse va converger. Vote B seul."
5. **Argument décisif advisor** : tdd-guard utilise un LLM pour valider TDD à chaque modif. C'est l'antipattern de `marker-ttl-blocage-agents` ("hooks de guard doivent être les plus simples possible — check binaire") appliqué au déterminisme : on utilise Claude pour valider Claude, boucle de coût + variance. Si la validation IA flake → soit bloque à tort (friction → désactivé en 6 semaines) soit laisse passer à tort.
6. **Pivot** : abandonner A et C, partir sur B pur. Le hook maison fait 100% du job nécessaire (check existence test + lecture `test.json` pour fail récent) en 150 lignes Python déterministes.
7. **Réutilisation gratuite** : format `test.json` compatible avec celui du plugin → si migration future souhaitée, 30 min suffisent. On garde la porte ouverte sans payer le coût aujourd'hui.

## Insight clé

**Le critère "officiel/populaire/Boris-starred" peut masquer l'antipattern architectural sous-jacent.** Le vrai critère de décision pour un guard n'est pas "est-ce répandu" mais "est-ce déterministe". Validation par LLM dans un PreToolUse hook = non-déterminisme là où le déterminisme est requis — c'est le pire des deux mondes vs un check binaire simple. L'argument bus factor / case studies enterprise est secondaire ; l'argument architectural est primaire.

Corollaire : quand l'équipe a déjà la skill (9 hooks Python sur neo_ia), réécrire en 50-150 lignes est moins risqué que d'absorber une dépendance externe complexe — même si la dépendance est mieux financée.

## Résultat

Hook `.claude/hooks/tdd-guard.py` (150 lignes) + `pytest_sessionfinish` dans `conftest.py` (20 lignes). Testé en live sur 4 cas (fichier source sans test = bloqué, bypass marker = autorisé, fichier tests = autorisé, doc = autorisé). Tous validés. Zéro dépendance externe, zéro coût IA, format `test.json` compatible plugin pour migration future éventuelle.

V1 livré 2026-05-19, métriques d'adoption via `scripts/tdd-metrics.py --days 7`. Seuils validation V1→V2 : red-green ≥ 70% sur 30j.

## Réutilisation

Utiliser ce raisonnement quand :
- Choix entre plugin tiers populaire et hook maison sur Claude Code
- Enforcement déterministe envisagé avec une couche de validation LLM "pour faire mieux"
- "Plugin officiel Anthropic / marketplace" est avancé comme argument de qualité
- Décision où l'argument d'autorité (Boris star, marketplace) risque de masquer l'antipattern architectural

Signal de déclenchement : "on prend le plugin existant ou on fait maison ?" sur un composant de type guard / hook / enforcement.

## Liens

- [[erreur-marker-ttl-blocage-agents]]
- [[erreur-advisory-rules-insuffisantes]]
- [[critique-tdd-neo-ia-proposal]]
- [[neo_ia]]
