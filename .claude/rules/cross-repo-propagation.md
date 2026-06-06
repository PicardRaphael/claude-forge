---
description: Toute décision de naming/structure prise sur un repo doit être propagée explicitement aux autres repos concernés. Les décisions ne s'auto-propagent jamais.
---

# Cross-repo propagation — Décisions naming/structure

## Principe

Quand une décision de naming, structure ou doctrine est prise sur un repo, elle ne se propage JAMAIS automatiquement aux autres. Réflexe immédiat après toute décision : **"est-ce que ça s'applique aux autres repos ?"**

## Checklist repos concernés

| Alias | Chemin |
|-------|--------|
| forge | `C:/Users/raphael.picard_neote/Documents/claude-forge/` |
| ia_back | `C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back/` |
| neo_ia | `C:/Users/raphael.picard_neote/Documents/neot-v2/` |
| lojii | `C:/Users/raphael.picard_neote/Documents/neofront/` |
| neoteem-brain | `C:/Users/raphael.picard_neote/Documents/neot-v2/neoteem-brain/` |

## Protocole

1. **Identifier le scope** : décision forge-only → pas de propagation. Décision multi-repo → continuer.
2. **Pour chaque repo concerné** :
   - Identifier le composant à modifier (agent, skill, rule, CLAUDE.md)
   - Session principale pour les writes cross-repo (sub-agents bloqués cross-repo)
   - Path absolu si délégation : `C:/Users/.../<repo>/.claude/agents/<nom>.md`
3. **Vérifier empiriquement** après propagation : grep le terme modifié sur chaque repo.
4. **Documenter** dans le vault si décision à valeur canonique :
   ```
   mcp__forge-brain__create_note(path="Knowledge/decisions/<sujet>.md", ...)
   ```

## Gotchas

- **Décisions naming silencieuses** : renommer sans propager = drift pendant des semaines (ex : `cto-mindset` → `orchestrator-mindset` sur neo_ia, non propagé ia_back, découvert audit 25 mai)
- **Sub-agents bloqués write cross-repo** : session principale doit faire les writes cross-repo, pas déléguer
- **Path absolu obligatoire** pour agent cross-repo : chemin relatif = fail silencieux
- **Scope forge ≠ règle universelle** : vérifier si la règle s'applique à tous les repos avant propagation

Source : `memory/feedback_propagate_decisions_cross_repo.md`
