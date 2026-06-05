---
name: "analyse-repo-includes-code-scan"
metadata: 
  node_type: memory
  originSessionId: d16cea52-3288-48fe-b266-693dd7948ca2
---

Quand Raphael dit "analyse mon repo et propose-moi la meilleure config CC" (ou variantes : "regarde mon code", "propose-moi un setup parfait", "vraiment en profondeur") :

**Réflexe FAUX** : lancer 4 project-auditor sur `.claude/` et s'arrêter là. Output = propositions théoriques basées seulement sur les composants CC existants, déconnectées du code.

**Réflexe CORRECT** : méthode 6 étapes canonique [[methode-analyser-repo]] complète, EN PARALLÈLE :
- **Audit `.claude/`** (4 project-auditor : agents / skills / hooks / rules+CLAUDE.md)
- **Scan archi code** (étape 1) : stack réelle vs déclarée, structure apps/packages, conventions internes, DB, tests, CI
- **Patterns récurrents code** (étape 5) : patterns qui apparaissent > 2 fois → candidats skills légitimes (9 catégories Thariq)

Puis synthèse Jarvis : `.claude/` actuel ⨯ code réel → propositions justifiées (ex : "ton repo a 17 fichiers avec stack X → skill Y manque" / "agent Z déclaré mais aucun code l'utilise → kill").

**Why:** L'utilisateur Raphael a dû le rappeler 2026-05-22 — par défaut je m'arrêtais aux composants CC. Une analyse "en profondeur" exige le code RÉEL, pas juste la config.

**How to apply:** À toute demande qui contient "analyse repo", "propose config", "meilleur setup", "vraiment en profondeur", "regarde le code" → lancer méthode 6 étapes COMPLÈTE en parallèle. Audit `.claude/` seul = strict "audite ma config", pas "analyse mon repo".

Related : [[methode-analyser-repo]], [[feedback_audit_repo_method]], [[feedback_analyse_first_not_questionnaire]].
