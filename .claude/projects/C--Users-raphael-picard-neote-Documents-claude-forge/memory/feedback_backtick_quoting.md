---
name: backtick-quoting-safety
description: Skills backtick commands must protect $ARGUMENTS from shell injection via single-quote assignment
type: feedback
---

Ne JAMAIS passer `$ARGUMENTS` dans des `!backtick` commands shell dans les skills. Aucune méthode de quoting ne fonctionne car :
- `$ARGUMENTS` est substitué littéralement avant exécution shell
- Les guillemets doubles ET simples cassent si la valeur contient `\` ou `"`
- Les heredocs cassent car le système `!backtick` aplatit le contenu sur une seule ligne

**Why:** Testé avec `@.claude\` — double quotes, single quotes, et heredocs ont tous échoué. Le système `!backtick` ne supporte pas le multi-ligne et la substitution littérale casse tout quoting.

**How to apply:** Ne jamais utiliser `!backtick` pour injecter `$ARGUMENTS` dans du shell. A la place, référencer `$ARGUMENTS` dans le texte markdown de la skill et instruire l'agent d'utiliser ses outils (Glob, Read, Bash) pour explorer le chemin. C'est plus robuste et plus flexible.
