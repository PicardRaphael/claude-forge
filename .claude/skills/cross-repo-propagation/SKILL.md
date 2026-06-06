---
name: cross-repo-propagation
description: "Use when a naming/structure decision is taken on one repo. ALWAYS propagate explicitly to other repos (forge, ia_back, neo_ia, neoteem-brain, lojii). Decisions don't auto-propagate."
effort: high
---

## Rôle

S'assurer qu'une décision de naming, structure ou doctrine prise sur un repo est propagée explicitement aux autres repos concernés. Les décisions ne se propagent jamais automatiquement.

## Étapes

1. **Identifier le scope de la décision** :
   - Décision forge uniquement → pas de propagation
   - Décision applicable à plusieurs repos → continuer

2. **Checklist repos concernés** :
   - `C:/Users/raphael.picard_neote/Documents/claude-forge/` — forge (origin)
   - `C:/Users/raphael.picard_neote/Documents/neot-v2/ia_back/` — backend IA
   - `C:/Users/raphael.picard_neote/Documents/neot-v2/` — neo_ia / monorepo Python
   - `C:/Users/raphael.picard_neote/Documents/neofront/` — frontend lojii
   - `neoteem-brain` dans `neot-v2/neoteem-brain/`

3. **Pour chaque repo concerné** :
   - Identifier le composant à modifier (agent, skill, rule, CLAUDE.md)
   - Dispatcher subagent-creator avec path absolu si agent/skill
   - Session principale pour modifications cross-repo (sub-agents bloqués write cross-repo)

4. **Documenter la décision** dans le vault si elle a valeur canonique :
   ```
   mcp__forge-brain__create_note(
     path="Knowledge/decisions/<sujet>.md",
     content="## Décision\n[contenu]\n## Propagation\n- [repo] : [composant] [status]"
   )
   ```

5. **Vérifier empiriquement** après propagation : grep le terme modifié sur chaque repo.

## Gotchas

- **Décisions naming silencieuses** : renommer `cto-mindset` → `orchestrator-mindset` sur neo_ia sans propager vers ia_back = drift pendant des semaines.
- **Sub-agents bloqués write cross-repo** : session principale doit faire les writes cross-repo, pas déléguer.
- **Agent-creator cross-repo = path absolu** : `C:/Users/.../<autre-repo>/.claude/agents/<nom>.md` fonctionne. Chemin relatif = fail silencieux.
- **Scope forge ≠ règle universelle** : vérifier si la règle s'applique à tous les repos ou seulement à forge avant propagation.

## Apprentissage

- `cto-mindset` → `orchestrator-mindset` : appliqué neo_ia, non propagé ia_back → découvert lors audit 25 mai
- Pattern : les décisions prises en fin de session fatiguée sont celles qui ne sont jamais propagées
- Après toute décision naming/structure, réflexe immédiat : "est-ce que ça s'applique aux 5 autres repos ?"
