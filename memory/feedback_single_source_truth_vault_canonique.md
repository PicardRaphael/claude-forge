---
name: single-source-truth-vault-canonique
description: "Pour les règles qui s'appliquent partout (ordre A→B→C→D→E, etc.), patcher la canonique vault UNIQUEMENT — pas dupliquer dans CLAUDE.md/rules/agents"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Quand une règle est universelle (méthode pour analyser/créer/modifier composant), elle doit vivre dans **UNE seule canonique vault**. Les autres composants pointent vers elle via wikilink.

## Exemple ordre canonique A→B→C→D→E

**Mon réflexe FAUX (2026-05-22)** : patcher la règle dans :
- CLAUDE.md forge (haut de section Critiques)
- check-before-create.md rule
- project-auditor.md agent
- skills cc-*-ref référence

→ 4 endroits = drift garanti, single source violée.

**Réflexe CORRECT (corrigé par Raphael)** :
- La règle vit dans `methode-analyser-repo` (canonique vault, section ORDRE CANONIQUE)
- `comment-creer-agent`, `-skill`, `-hook`, `-claudemd` ajoutent juste un **renvoi** : "Cf [[methode-analyser-repo]] section ORDRE CANONIQUE"
- CLAUDE.md / rules / agents **ne dupliquent PAS** — ils héritent par lecture vault

## Why

Single source of truth = principe fondamental documenté [[feedback_single_source_of_truth]].
Si la règle évolue, on modifie 1 fichier (la canonique vault). Toute duplication est un futur drift.

L'erreur "patcher CLAUDE.md avec règle universelle" est récurrente (je l'ai faite ce matin 2026-05-22 sur ordre A→B→C→D→E, Raphael m'a corrigé).

## How to apply

Avant de patcher CLAUDE.md / rule / agent pour ajouter une "règle universelle" :

1. **Question** : cette règle s'applique-t-elle dans plusieurs contextes (analyse repo, création agent, création skill, etc.) ?
2. **Si OUI** → la patcher dans la canonique vault correspondante (`methode-analyser-repo`, `comment-creer-X`)
3. **Si NON** (règle locale à un seul fichier) → OK de patcher CLAUDE.md ou la rule directement
4. **Pour propager** : les autres canoniques vault ajoutent un wikilink renvoi, PAS de duplication contenu

## Outils MCP pour update propre

Depuis 2026-05-22, MCP forge-brain a :
- `update_note(file, content)` — remplace contenu entier
- `insert_section(file, marker, content, position)` — insère avant/après header markdown précis

Utiliser ces outils plutôt que duplication.

Related : [[feedback_single_source_of_truth]], [[feedback_lire_canoniques_avant_audit]], [[reference_mcp_stdio_restart_impossible]].
