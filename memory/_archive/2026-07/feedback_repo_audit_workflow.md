---
name: repo-audit-workflow
description: "Workflow audit repo Neoteem depuis forge — scan parallèle, corrections par stack, commit par repo"
metadata:
  type: feedback
  originSessionId: fdb162f8-52a4-438b-a60a-c8e2ce6e37cf
---

Cf [[quartet-analyse-multi-repo]] (doctrine canonique vault — 4 agents spécialisés Sonnet/Opus parallèles + DA).

**Workflow Neoteem spécifique préservé** (4 mai 2026, 3 repos en une session) :
1. **Scanner en parallèle** — 1 agent par repo (ia_back / neo_ia / neoteem-brain)
2. **Rapport tableau** — par repo, checks, statut OK/WARN/CRITIQUE
3. **Corriger par stack** — ia_back=bun, neo_ia=python, neoteem-brain=python. Toujours respecter la stack du projet
4. **Commit par repo** — 1 commit séparé avec message descriptif
5. **Push** — forge depuis ici, autres repos via `git -C <path>` (cf `feedback_git_C_pas_cd`)

**Gotcha** : `~/.claude/settings.json` peut contenir des deny rules globales qui surprennent un repo spécifique.
