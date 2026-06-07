---
name: commit-message-no-herestring-bash-tool
description: "Message de commit multi-lignes via le Bash tool (PowerShell/Windows) : here-string @'...'@ injecte un @ littéral en tête. Utiliser des -m répétés."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 492c167d-73c8-42da-8e57-f7b41a17bfa8
---

Le Bash tool tourne en PowerShell sous Windows. Un here-string `@'...'@` passé à `git commit -m` injecte le `@` comme premier caractère du titre du commit. Les `-m` répétés (1 par paragraphe) passent proprement.

**Why:** observé 27 mai (session A3), commit 1 titré "@ feat(skill):..." au lieu de "feat(skill):...", corrigé par `git commit --amend`.

**How to apply:** commit multi-lignes via Bash tool = `git commit -m "titre" -m "corps" -m "Co-Authored-By..."`. Jamais de here-string `@'...'@`. Cas distinct de [[erreur-hooks-bash-quoting-windows]] (qui porte sur `bash -c '...$()...'` dans les hooks) et du heredoc Git Bash (écriture de fichiers). Ici c'est spécifiquement le message de commit.

**Re-violation 5 juin 2026 (≥2e occurrence)** : commit RAG via Bash tool avec `@'...'@` → `syntax error near unexpected token '('` (les parenthèses + l'apostrophe de « l'ingestion » cassent le parsing bash), corrigé en multi-`-m`. La règle est pourtant documentée 2× (ce feedback + vault [[erreur-da-heredoc-bash-silencieux]]). Documentée ≠ appliquée : le réflexe ne se déclenche pas au moment d'écrire le commit. **Déclencheur mental** : dès que je tape `git commit` dans le tool **Bash** avec plus d'une ligne → STOP, multi-`-m` direct, jamais `@'...'@` (syntaxe PowerShell). Cf [[feedback_feedback_reviole_3x_regle_insuffisante]] : une 3e violation justifierait un garde-fou structurel (hook PreToolUse qui bloque `@'` dans un `git commit` Bash).

**3e violation 7 juin 2026 — SEUIL ATTEINT** : commit chantier 1 hygiène doctrine avec `git commit -m @'...'@` → `@` parasite en tête du sujet (`@ chore(forge-brain):...`), corrigé `--amend`. Exactement le cas prédit ligne ci-dessus. Documentée 3× et re-violée 3× = la règle textuelle NE SUFFIT PAS ([[feedback_feedback_reviole_3x_regle_insuffisante]] : ≥3× → garde-fou structurel). **Action désormais justifiée** : hook PreToolUse Bash qui détecte `git commit` + `@'` dans la commande et bloque (exit 2) avec message « multi-`-m` sous Windows ». À créer via `hook-creator` quand Raphael valide. En attendant : ne JAMAIS composer un message de commit multi-lignes autrement qu'en `-m` répétés.
