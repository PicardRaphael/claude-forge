---
name: refactor-masse-script-python-regex
description: "Pour refactor > 10 fichiers partageant le même bloc, script Python ponctuel + regex > Edit séquentiels"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 02a72a18-03e9-497d-9fbe-ea0961ddfa79
---

Quand un refactor identique doit être appliqué à 10+ fichiers (extraction bloc + remplacement par wikilink, normalisation frontmatter, port stack OLD → NEW, etc.), **préférer un script Python ponctuel** plutôt que 10+ Edit séquentiels.

Pattern validé ia_back 25 mai 2026 :
- 18 agents à refactor (13 filet MCP + 5 ESCALADE)
- 1 script Python (regex `re.MULTILINE|re.DOTALL` + `Path.write_text` atomique)
- 1 commande `py script.py` → 308 lignes économisées, 18 fichiers traités en < 5s
- Vérif empirique post-exécution en 1 grep
- Script supprimé après exécution (`.claude/tmp-refactor-*.py`)

**Why:** 18 Edit séquentiels = 18 round-trips tool + risque d'erreur (Read obligatoire avant chaque Edit). Script Python = 1 round-trip + atomicité + idempotent + vérification par grep.

**How to apply:** dès qu'un refactor concerne > 10 fichiers avec un pattern textuel stable (même bloc, même marqueurs de début/fin). Si le pattern varie entre fichiers (cas particulier par fichier), revenir aux Edit. Toujours nettoyer le script tmp après exécution.
