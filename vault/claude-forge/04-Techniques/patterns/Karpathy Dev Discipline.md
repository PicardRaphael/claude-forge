---
titre: "Karpathy Dev Discipline"
resume: "4 principes coding (Simplicity, Surgical, Assumptions, Verifiable Steps) inspires de Karpathy, implementes en rules"
aliases:
  - "karpathy guidelines"
  - "karpathy skills"
  - "dev discipline"
domaine: technique
type: technique
derniere-maj: 2026-04-26
auteur: claude
sources:
  - "https://github.com/forrestchang/andrej-karpathy-skills"
  - "[[Andrej Karpathy]]"
tags:
  - "#type/technique"
  - "#type/technique"
---

## Description

Adaptation des anti-patterns LLM coding identifies par [[Andrej Karpathy]] (Silent Assumptions, Over-Engineering, Drive-By Refactoring) en rules Claude Code actionnables.

Le repo `forrestchang/andrej-karpathy-skills` propose 4 principes :
1. **Think Before Coding** — surfacer les hypotheses, poser des questions
2. **Simplicity First** — minimum de code, pas d'abstraction speculative
3. **Surgical Changes** — ne toucher que ce qui est demande
4. **Goal-Driven Execution** — steps verifiables avec criteres de succes

## Implementation Neoteem

Apres audit complet de neo_ia et ia_back, ~70-80% etait deja couvert (architect-first, cto-mindset, debugger). Les gaps combles :

### Rule `dev-discipline.md` (neo_ia + ia_back)
- **Simplicity First** nomme comme principe (absent avant — 1 seule mention "sur-ingenierie" dans tout neo_ia)
- **Surgical Changes** etendu aux dev-agents (avant, uniquement debugger ia_back)
- **Explicit Assumptions** — lister les hypotheses avant de coder (absent partout)

### Rule `verifiable-steps.md` (neo_ia + ia_back)
- Format `[Step N] → verify: [check concret]` dans les plans architect
- Pas de passage au step N+1 sans verification PASS

## Quand utiliser

Setup d'un nouveau projet Claude Code, ou audit d'un projet existant pour verifier que les principes Karpathy sont implementes en rules.

## Exemple

Rule `dev-discipline.md` :
```markdown
# Dev Discipline
1. **Simplicity First** — minimum de code, pas d'abstraction speculative
2. **Surgical Changes** — ne toucher que ce qui est demande
3. **Explicit Assumptions** — lister les hypotheses avant de coder
```

## Decision : pas de plugin

Le plugin brut est redondant a 80% avec l'existant. Les 2 rules ciblees comblent les gaps sans bruit contextuel.

## Liens

- [[MOC-Techniques]]
- [[Andrej Karpathy]]
- [[Amanda Askell|Amanda Askell — Prompt Engineering & Custom Instructions]]
- [[LLM Wiki]]
