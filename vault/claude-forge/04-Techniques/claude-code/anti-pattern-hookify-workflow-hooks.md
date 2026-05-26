---
titre: "Anti-pattern hookify — workflow hooks via transcript conditions"
resume: "Plugin officiel hookify (Anthropic) permet `event: stop` + conditions sur transcript pour bloquer Claude tant que tests pas lancés. Pattern viole doctrine 22 mai forge (hooks = lint/sécu/scope only, JAMAIS workflow). Documente pourquoi forge skip hookify."
aliases:
  - "anti-pattern hookify"
  - "hookify workflow hooks"
  - "hooks transcript conditions anti-pattern"
  - "workflow hooks pourquoi non"
  - "hookify vs doctrine 22 mai"
derniere-maj: 2026-05-26
auteur: claude
type: anti-pattern
sources:
  - "Plugin anthropics/claude-plugins-official/plugins/hookify (26 mai 2026)"
  - "[[raisonnement-22mai-doctrine-vs-enforcement]]"
tags:
  - "#type/anti-pattern"
  - "#domaine/claude-code"
  - "#doctrine"
---

# Anti-pattern hookify — workflow hooks via transcript conditions

> Pourquoi forge ne consomme pas le plugin officiel `hookify` malgré son ergonomie supérieure.

## Le plugin

`hookify` (Anthropic, plugins officiels) propose de créer des hooks via fichiers markdown YAML simples au lieu d'éditer `settings.json`. Exemple verbatim README :

```yaml
---
name: require-tests-run
event: stop
action: block
enabled: false
conditions:
  - field: transcript
    operator: not_contains
    pattern: npm test|pytest|cargo test
---
```

Traduction : **Claude ne peut PAS terminer sa session tant que `npm test` n'apparaît pas dans le transcript**. C'est un workflow hook.

## Pourquoi c'est un anti-pattern (selon doctrine forge 22 mai)

### Doctrine canonique vault

[[raisonnement-22mai-doctrine-vs-enforcement]] verbatim : *"Hooks = lint / sécurité / scope UNIQUEMENT. JAMAIS workflow agentique (architect-first, TDD strict, commit gates, markers TTL)."*

### Pourquoi cette doctrine existe

1. **Régression observée** sur forge début 2026 : hooks workflow `architect-first` + `tdd-strict` + `commit-gates` produisaient :
   - Sessions bloquées 10+ tours sur faux positifs
   - Claude rationalise pour contourner ("voici un test stub")
   - Workflow rigide imposé alors que la doctrine devait être *advisory*
2. **Hooks = enforcement 100%** : si la règle n'est pas 100% applicable (cas exceptionnels existent), on bloque à tort
3. **Workflow = advisory ~80%** : doctrine rules + CLAUDE.md + skills, Claude juge selon contexte

### Cas concrets violations hookify

| Hookify rule | Violation doctrine |
|--------------|-------------------|
| `event: stop` + `not_contains pytest` | Workflow gate (forcer test run) |
| `event: file` + transcript contains "TODO" | Workflow gate (forcer no-TODO policy) |
| `event: bash` + `not_contains git status` | Workflow gate (forcer status check avant push) |

À l'inverse, ces règles hookify seraient **conformes doctrine** :

| Hookify rule | Conforme car |
|--------------|--------------|
| `event: bash` + `pattern: rm -rf` + `action: block` | Sécurité (destructif) |
| `event: file` + `file_path: .env` + `action: block` | Sécurité (secrets) |
| `event: file` + `pattern: API_KEY = "` + `action: warn` | Sécurité (credentials hardcodés) |

## Décision forge

- **SKIP hookify plugin** complet
- Si Raphael veut hookify **uniquement pour règles sécu/lint/scope**, OK mais :
  - Risque dérive future ("rajouter juste cette règle workflow utile")
  - Préférable de conserver `.claude/hooks/*.py` Python custom (3 hooks sécu actuels : delegate-guard, security-guard, meta-commentary-detector)
- Capitaliser comme **anti-pattern documenté** pour ne pas y revenir

## Quand reconsidérer

- Anthropic publie une version qui marque les workflow patterns deprecated
- Doctrine forge évolue post-empirique (advisor + DA + 1 mois d'usage)
- Raphael décide d'abandonner doctrine 22 mai (très improbable, confirmée 24 mai 25 mai)

## Wikilinks

- [[raisonnement-22mai-doctrine-vs-enforcement]] — doctrine canonique
- [[comment-creer-hook]] — comment créer hook (29 events, doctrine appliquée)
- [[plugins-officiels-veille-2026-05-26]] — synthèse 11 plugins
- [[methode-pivoter-doctrine]] — si doctrine évolue un jour
