---
name: forced-parity-antipattern
description: Copier la config agents/skills/hooks d'un repo vers un repo de nature differente sans adapter le scope au contexte = antipattern recurrent
metadata:
  type: feedback
---

## Pattern de fragilite : parite forcee multi-repo

Copier la config d'un repo (ex: neo_ia = monorepo Python, 11 agents) vers un repo de nature differente (ex: lojii = frontend Vue 3 legacy) en visant le "meme nombre d'agents" produit systematiquement :

1. **Agents inutiles** : codebase-analyst, build-error-resolver = over-engineering pour un frontend
2. **Agents hors echelle** : windev-migrator seul pour 914 ecrans = pas viable sans pipeline
3. **Recouvrement de scope** : architect + dev-lead + codebase-analyst + ticket-resolver font tous de la planification
4. **Rules sans enforcement** : copier les rules sans les hooks correspondants = 80% compliance max

**Why:** Chaque repo a des besoins specifiques. Le bon objectif n'est pas "meme nombre d'agents" mais "memes principes (hooks, conventions, pipeline) adaptes au contexte".

**How to apply:** Quand une proposition vise la "parite" avec un autre repo, verifier :
- Les repos ont-ils la meme nature (backend vs frontend vs monorepo vs vault) ?
- Le .claude/ est-il partage (equipe) ou personnel (1 dev) ? Le scope doit suivre.
- Chaque agent propose a-t-il un use case distinct ET frequent ? Si invoque < 1x/semaine → supprimer.
- Les rules "OBLIGATOIRE" ont-elles des hooks correspondants ?

Premiere observation : critique lojii 2026-05-13 ([[critique-2026-05-13-setup-lojii]]).
