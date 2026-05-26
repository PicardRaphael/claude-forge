---
titre: "Méthode veille marketplace plugins Claude Code — reproductible"
resume: "Pattern 6 étapes pour analyser un batch de plugins du marketplace anthropics/claude-plugins-official et trancher ADAPT/REFERENCE/SKIP sans créer de skills forge inutiles. Validé 26 mai 2026 sur 11 plugins (203 total marketplace)."
aliases:
  - "méthode veille plugins"
  - "pattern analyse marketplace plugins"
  - "comment analyser plugins officiels"
  - "veille claude-plugins-official reproductible"
  - "11 plugins méthode 26 mai"
derniere-maj: 2026-05-26
auteur: claude
type: raisonnement
sources:
  - "Session forge 26 mai 2026 — analyse 11 plugins"
  - "Advisor + AskUserQuestion arbitrages"
tags:
  - "#type/raisonnement"
  - "#domaine/claude-code"
  - "#meta"
---

# Méthode veille marketplace plugins — reproductible

> Quand un user demande "analyse ces N plugins officiels", appliquer cette méthode 6 étapes. Pas d'improvisation.

## Contexte du raisonnement

26 mai 2026 — Raphael demande d'analyser 11 plugins officiels Anthropic. Marketplace compte 203 plugins. Tentation naturelle : créer 11 skills forge équivalentes ou WebFetch en série bête.

**Approche qui a marché** : 6 étapes structurées avec arbitrage user + advisor + capitalisation ciblée.

## Méthode 6 étapes

### Étape 1 — Inventaire vault EXISTANT (5 min)

AVANT toute recherche web :
- `search_brain("plugins officiels anthropic")` + variantes
- `list_notes("04-Techniques/claude-code")`
- Lire notes pertinentes : `comparaison-skill-anthropic-claude-code-setup`, `analyse-plugin-claude-code-setup`

**Pourquoi crucial** : Le vault contient déjà la **doctrine d'absorption** ("on absorbe pas dans skill forge") et le **pattern de capitalisation** (1 note synthèse, pas 11 atomiques). Sauter cette étape = 11 notes redondantes.

### Étape 2 — Clarifier scope via AskUserQuestion (1 min)

3 questions critiques :
1. **Méthode** : recherche complète vs priorisée vs sub-agents parallèles
2. **Scope d'application** : forge / neo_ia / ia_back (multiselect)
3. **Capitalisation** : note par plugin vs synthèse vs rien

Sans ça → 30 min de travail mal calibré.

### Étape 3 — WebFetch parallèle marketplace.json + 11 plugins (10 min)

```bash
# marketplace.json complet via raw + Python parse pour filtrer
curl -s https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json | python -c "
import json,sys
d=json.load(sys.stdin)
plugins=d.get('plugins',[])
targets=['name1','name2',...]
for p in plugins:
    if p['name'] in targets:
        print(p['name'], p['source'], p['description'][:80])
"
```

Puis WebFetch sur chaque plugin GitHub tree (en parallèle batch unique).

**Gotcha** : WebFetch 404 sur certains tree GitHub si plugin est REMOTE (`source.type: url`). Aller chercher sur le repo externe identifié dans marketplace.json.

### Étape 4 — Advisor AVANT verdict (3 min)

Advisor reçoit le transcript complet (11 plugins + inventaire vault + scope user). Il identifie :
- Discriminateurs (forge a-t-il déjà ? technique vs produit ? stack-match ? conflit doctrinal ?)
- Découvertes non-évidentes (gap mesurable skill-creator eval, confidence scoring code-review, caveat remember, naming confusion forge-skills Atlassian)
- Stratégie capitalisation (1 note synthèse, pas 11)

**Pourquoi avant verdict** : Sans advisor, tentation de tout absorber dans skills forge. Advisor force le filtre doctrinal.

### Étape 5 — AskUserQuestion arbitrage propositions (1 min)

Présenter en table 11 lignes (plugin | quoi | équivalent forge | verdict | action) + 3 propositions concrètes en questions multiselect :
1. Enrichir canonique X ?
2. Enrichir canonique Y ?
3. Capitalisation vault — quelles notes créer ?

Raphael tranche en 1 click multi-select.

### Étape 6 — Exécution + vérification empirique (15 min)

Parallèle MAX :
- 3 `create_note` simultanés (synthèse + anti-pattern + technique)
- 2 `append_note` notes existantes
- 2 `update_property` derniere-maj
- 1 `Edit` CHANGELOG vault
- Dispatch 2 sub-agents skill-creator EN PARALLÈLE pour modifs canoniques (note vault + skill forge)
- Mémoire `Write` reference_*.md + `Edit` MEMORY.md
- **Vérification empirique** post sub-agent via `grep -n` (feedback `auditor-empirical-verify`)

## Anti-patterns évités

| ❌ Anti-pattern | ✅ Approche correcte |
|---|---|
| Créer 11 skills forge équivalentes | Enrichir canoniques existants (single source of truth) |
| 1 note vault par plugin | 1 note synthèse + 2-3 notes techniques ciblées |
| Lancer WebFetch sans inventaire vault | search_brain AVANT WebFetch (doctrine absorption pré-établie) |
| Décider verdict sans advisor | Advisor AVANT verdict (filtre doctrinal) |
| Relayer claim sub-agent sans vérif | grep -n post-dispatch (feedback empirique) |
| Capitalisation aveugle | AskUserQuestion multiselect sur quelles notes créer |

## Discriminateurs réutilisables (pour future veille)

1. **Forge a-t-il déjà absorbé l'équivalent ?** → Doctrine canonique vault dit "on absorbe pas"
2. **Technique vs produit ?** → Technique = enrichir canonique. Produit = note référence ou skip
3. **Stack-match neo_ia/ia_back ?** → Empirique : grep pyproject.toml / package.json
4. **Conflit doctrinal ?** → Notamment doctrine 22 mai (hooks workflow = NON)
5. **Caveat bloquant ?** → Ex : remember exige désactiver auto-compact CC = SKIP

## Reproductibilité

Quand marketplace dépasse 300 plugins (estimé août 2026) ou quand Anthropic lance batch nouveau :
1. User désigne N plugins ou catégorie
2. Appliquer ces 6 étapes
3. Compter sur 25-40 min total pour N=10-15 plugins
4. Capitalisation = 1 note synthèse + 0-3 notes techniques selon découvertes

## Wikilinks

- [[plugins-officiels-veille-2026-05-26]] — synthèse exécutée 26 mai
- [[comparaison-skill-anthropic-claude-code-setup]] — doctrine "on absorbe pas"
- [[methode-analyser-repo]] — méthode sœur (analyse repo)
- [[methode-pivoter-doctrine]] — méthode sœur (pivot doctrinal)
- [[anti-pattern-hookify-workflow-hooks]] — exemple verdict SKIP doctrinal
- [[eval-pattern-anthropic-skill-creator]] — exemple verdict ADAPT (enrichi canonique)
