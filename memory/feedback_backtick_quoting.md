---
name: backtick-quoting-safety
description: Ne jamais passer $ARGUMENTS dans des backtick shell — la substitution litterale casse tout quoting
type: feedback
---

Ne JAMAIS utiliser `$ARGUMENTS` dans des `!backtick` commands des skills.

**Why:** `$ARGUMENTS` est substitue litteralement avant execution shell. Si la valeur contient `\`, des guillemets, ou des caracteres speciaux, elle casse tout type de quoting (simple, double, heredoc sur une ligne). Le systeme `!backtick` aplatit le contenu sur une seule ligne, ce qui casse aussi les heredocs multi-lignes.

**How to apply:** Dans les skills, utiliser des instructions pour que l'agent explore avec ses outils natifs (Glob, Read, Bash) au lieu de `!backtick` commands. C'est plus robuste et c'est le bon pattern. Cette regle est aussi dans CLAUDE.md > Gotchas.
