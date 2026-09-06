---
name: auditor-empirical-verify
description: ALWAYS invoke after dispatching a sub-agent that claims to have created, modified, or deleted files. DO NOT relay sub-agent summaries to the user without empirical verification -- sub-agents lie by omission.
allowed-tools: Read, Glob, Grep, Bash
effort: high
user-invocable: true
---

## Role

Checklist de verification empirique post-dispatch. Les sub-agents retournent "done" meme quand ils ont echoue silencieusement -- la session principale doit toujours verifier avant de relayer.

## Checklist post-dispatch (4 points)

### 1. Fichiers existent ?
  ls -la "C:/path/to/expected/file.md"
  # ou Glob pattern: .claude/skills/nom-skill/**

### 2. Contenu conforme ?
  head -20 "C:/path/to/file.md"
  # Verifier frontmatter complet

### 3. Git diff confirme ?
  REPO="$(git rev-parse --show-toplevel)"
  git -C "$REPO" diff --stat
  git -C "$REPO" status --short
  # Repo tiers : resoudre son chemin sur la machine courante, jamais l ecrire en dur

### 4. Taille realiste ?
  wc -l "C:/path/to/file.md"
  # SKILL.md < 5 lignes = echec silencieux

## Par type d agent

| Agent            | Verifier |
|-----------------|---------|
| skill-creator    | ls .claude/skills/<nom>/SKILL.md + wc -l > 20 |
| subagent-creator    | ls .claude/agents/<nom>.md + frontmatter complet |
| hook-creator     | ls .claude/hooks/<nom>.py + grep exit 2 |
| claudemd-creator | wc -l CLAUDE.md + diff avant/apres |
| tout agent       | git diff --stat pour confirmer fichiers touches |

## Anti-patterns

- "Le sub-agent a dit done" -> non. exit 0 != succes. Verifier empiriquement.
- Relayer le resume sub-agent sans grep/ls -> regression silencieuse
- "Je vois le resultat dans la conversation" -> sub-agent peut avoir affiche PREVU sans avoir ecrit
- Skipper la verif sur agents "fiables" -> tous echouent silencieusement sur Write denied

## Gotchas

- Exit 0 != succes : Write denied retourne exit 0 cote Bash mais le fichier n existe pas
- Contenu affiche != contenu ecrit : sub-agent peut generer SKILL.md dans output sans avoir pu le Write
- Glob ne trouve pas = fichier absent : ne pas interpreter "aucun resultat" comme bug Glob
- git diff vide apres agent : soit rien fait, soit changements non stages -- verifier les deux

## Apprentissage

Feedback source : memory/feedback_subagent_autocommit.md et
memory/feedback_subagent_audit_category_error.md
Pattern : sub-agents editeurs clament succes sans empirie -- toujours grep/diff post-dispatch.
Verifier aussi git log --oneline -3 : un sub-agent commit malgre la consigne contraire.
Si nouvel anti-pattern de sub-agent decouvert -> ajouter dans Anti-patterns.
