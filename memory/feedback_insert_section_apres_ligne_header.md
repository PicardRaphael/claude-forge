---
name: insert-section-apres-ligne-header-pas-section
description: MCP forge-brain insert_section(position=after) insère après la LIGNE du header, pas après le CONTENU de la section. Insérer une section après un header colle le nouveau header juste sous l'ancien et pousse le corps de l'ancienne section sous la nouvelle — structure cassée. Vérifier via read_section après, ou viser la dernière ligne de la section qui doit précéder.
metadata:
  type: feedback
---

`mcp__forge-brain__insert_section(file, marker, content, position="after")` insère le contenu immédiatement **après la ligne du marker** (le header), PAS après le contenu complet de la section que ce header introduit.

**Why:** 27 mai (Chantier A 2b), amendement de 3 canoniques creator. `insert_section after "## Header X"` a placé ma nouvelle section `## Header Y` juste sous `## Header X`, repoussant TOUT le corps de X sous Y. Résultat : header X orphelin (vide), corps de X attribué à Y. Empilement aggravé sur comment-creer-agent (2 insertions after le même type de marker → 3 headers consécutifs, 2 corps déplacés). Détecté via `read_section` (qui lit jusqu'au prochain header de même niveau → montrait du contenu étranger sous ma section).

**How to apply:**
- Après chaque `insert_section`, VÉRIFIER via `read_section(file, "## mon nouveau header")` que le corps affiché est bien le mien et rien d'autre.
- Pour insérer une section APRÈS une section complète : viser comme marker la **dernière ligne** (ou un sous-header `###`) de la section qui doit précéder, pas son header `##`. OU insérer `before` le header de la section qui doit suivre.
- `insert_section before` n'a pas ce piège (insère avant le header cible, propre).
- Fix d'une structure déjà cassée : Read main session (autorisé par vault-cat-guard) + reconstruction par bornes de lignes (PowerShell `Set-Content` ou Edit), réordonner header+corps. Vérifier via read_section après.

Cf [[mcp-alias-ambigu-chemin-exact]] (autre piège de résolution implicite des outils MCP d'écriture vault).
