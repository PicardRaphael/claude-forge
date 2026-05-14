---
titre: "Kit rules standard pour tout nouveau projet"
resume: "3 rules obligatoires a deployer sur chaque repo : check-before-create, quality-gates, learn-from-mistakes"
aliases:
  - "kit rules"
  - "rules standard"
  - "socle rules"
domaine: claude-code
type: best-practice
auteur-source: "Raphael Picard / claude-forge"
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "[[delegate-guard-pattern]]"
  - "[[erreur-edit-direct-skills]]"
tags:
  - "#type/best-practice"
  - "#domaine/claude-code"
---

## Regle

Tout projet Claude Code avec des agents et skills DOIT avoir ces 3 rules minimum, adaptees a ses propres agents :

### 1. `check-before-create.md`

Checklist AVANT toute creation/modification de composant :
1. Memoire projet (feedbacks pertinents)
2. References existantes du composant
3. Patterns existants dans le projet (lire 2-3 composants similaires)
4. Deleguer aux agents DU PROJET (architect fast pass → implementer → code-reviewer)
5. Standards a respecter (taille, format, frontmatter)

### 2. `quality-gates.md`

Workflows concrets avec les agents DU PROJET par type de tache :
- Feature → architect → dev-* → test-writer → code-reviewer
- Bug fix → architect (fast pass) → dev-* → test-writer → code-reviewer
- Taille L → architect → TaskCreate → multi-dev → test-writer → code-reviewer
- Parallelisme quand taches independantes

Regle absolue : JAMAIS de commit sans test-writer + code-reviewer.

### 3. `learn-from-mistakes.md`

Sauvegarder chaque erreur corrigee en memoire. SANS `globs:` restrictifs (bug decouvert : `globs: ["**/*.py"]` limitait la rule au Python).

## Pourquoi

- Les rules advisory ne sont pas toujours respectees, mais elles guident le workflow
- Sans check-before-create : 6 skills + 14 agents edites a la main sans verification (2026-04-26)
- Sans quality-gates : les gates (test-writer, code-reviewer) sont oubliees sous pression
- Sans learn-from-mistakes : les erreurs se repetent entre sessions

## Comment appliquer

Quand project-analyzer analyse un projet :
1. Verifier si ces 3 rules existent
2. Si absentes → les recommander en P1
3. Les adapter aux agents DU PROJET (pas ceux de forge)
4. Le delegate-guard hook = forge ONLY, les autres repos utilisent architect + code-reviewer

## Implementation de reference

- neo_ia : `check-before-create.md` + `quality-gates.md` + `learn-from-mistakes.md`
- ia_back : idem, adapte aux agents ia_back (TypeScript/Bun)

## Liens

- [[MOC-Claude-Code]]
- [[delegate-guard-pattern]] — hook forge only
- [[erreur-edit-direct-skills]] — erreur qui a motive ce kit
