---
name: check-before-create-uses-local-agents
description: check-before-create rule must delegate to the PROJECT's own agents (architect + code-reviewer), never to forge agents that don't exist locally
type: feedback
originSessionId: d8d939df-a3a5-40ee-a82f-8efda6c1e9a6
---
## Regle

La rule `check-before-create` dans chaque projet doit utiliser les agents DU PROJET pour le workflow de validation, pas les agents forge (skill-creator, agent-creator, claudemd-optimizer) qui n'existent pas dans les autres repos.

**Why:** Le delegate-guard hook n'a de sens que dans forge (seul repo avec les agents specialises). Deployer le hook dans les autres repos bloquait les edits sans alternative disponible. L'utilisateur a corrige : les repos utilisent leur propre workflow architect → code-reviewer.

**How to apply:**
- Chaque repo a `architect` (fast pass pour valider la coherence) + `code-reviewer` (conformite aux standards)
- Le workflow check-before-create est : memoire → references → patterns existants → architect fast pass → implementer → code-reviewer
- delegate-guard = forge ONLY
- check-before-create = TOUS les repos, adapte aux agents locaux
- quality-gates.md = TOUS les repos, avec workflows concrets adaptes aux agents du projet
- Hooks stack = meme langage que le projet (Python pour neo_ia, TypeScript/Bun pour ia_back)

**Kit standard pour tout nouveau repo :**
Quand project-analyzer analyse un projet, TOUJOURS proposer :
1. `check-before-create.md` — adapte aux agents du projet
2. `quality-gates.md` — workflows concrets avec les agents du projet
3. `learn-from-mistakes.md` — sans globs restrictifs
Ces 3 rules sont le socle minimum au meme titre que agent-delegation et testing.
