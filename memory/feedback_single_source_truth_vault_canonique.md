---
name: single-source-truth-vault-canonique
description: "Pour les règles qui s'appliquent partout (ordre A→B→C→D→E, etc.), patcher la canonique vault UNIQUEMENT — pas dupliquer dans CLAUDE.md/rules/agents"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Cf [[pattern-maintenance-hybride-corpus-accumulatif]] (doctrine : une règle universelle vit dans UNE canonique vault, les autres composants la propagent par wikilink renvoi — jamais duplication ; workflow décision feedback vs vault ; outils MCP `update_note`/`insert_section` pour update propre). Voir aussi [[feedback_single_source_of_truth]].

**Cas empirique(s) :**

- **2026-05-22** — Réflexe FAUX : patcher la règle d'ordre canonique A→B→C→D→E dans 4 endroits à la fois — CLAUDE.md forge (haut de section Critiques), `check-before-create.md` rule, `project-auditor.md` agent, skills `cc-*-ref` référence. 4 endroits = drift garanti, single source violée. Raphael m'a corrigé : la règle vit dans `methode-analyser-repo` (canonique vault, section ORDRE CANONIQUE), et `comment-creer-agent`/`-skill`/`-hook`/`-claudemd` ajoutent juste un renvoi "Cf [[methode-analyser-repo]] section ORDRE CANONIQUE". CLAUDE.md / rules / agents ne dupliquent PAS, ils héritent par lecture vault. Erreur récurrente ("patcher CLAUDE.md avec règle universelle").

Related : [[feedback_lire_canoniques_avant_audit]], [[reference_mcp_stdio_restart_impossible]].
