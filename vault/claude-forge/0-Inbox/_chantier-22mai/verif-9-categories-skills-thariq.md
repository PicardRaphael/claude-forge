---
titre: "Vérification — 9 catégories skills Claude Code selon Thariq"
resume: "Liste verbatim des 9 catégories de skills selon Thariq Shihipar (équipe Anthropic) avec URL source primaire"
aliases:
  - "9 categories skills"
  - "thariq 9 categories"
  - "skills taxonomy thariq"
  - "taxonomie skills claude code"
  - "9 types de skills"
derniere-maj: 2026-05-22
auteur: claude
tags:
  - "#type/verification"
  - "#domaine/claude-code"
---

# 9 catégories de skills Claude Code — Thariq Shihipar

## Source primaire

- **URL** : https://www.linkedin.com/pulse/lessons-from-building-claude-code-how-we-use-skills-thariq-shihipar-iclmc
- **Auteur** : Thariq Shihipar (équipe Anthropic Skills)
- **Date capture** : 2026-05-22
- **Titre article** : "Lessons from building Claude Code: how we use Skills"

Tweet pivot `https://x.com/trq212/status/2033949937936085378` inaccessible (HTTP 402). PDF Anthropic `The-Complete-Guide-to-Building-Skill-for-Claude.pdf` non parsable (binaire).

## Liste verbatim (ordre Thariq)

1. **Library & API Reference** — Explains correct usage of libraries, CLIs, or SDKs, including internal tools and common gotchas.
2. **Product Verification** — Describes how to test or confirm code is working, often paired with tools like Playwright or tmux.
3. **Data Fetching & Analysis** — Connects to data and monitoring stacks, providing credentials, dashboard IDs, and common query workflows.
4. **Business Process & Team Automation** — Converts repetitive workflows into single commands, often depending on other skills or MCPs.
5. **Code Scaffolding & Templates** — Generates framework boilerplate for specific codebase functions, especially when natural language requirements are involved.
6. **Code Quality & Review** — Enforces organizational code standards and supports review, optionally running via hooks or CI actions.
7. **CI/CD & Deployment** — Helps fetch, push, and deploy code, sometimes referencing other skills for data collection.
8. **Runbooks** — Takes a symptom like an alert or error, conducts a multi-tool investigation, and produces "a structured report."
9. **Infrastructure Operations** — Handles routine maintenance and operational procedures, including those involving "destructive actions that benefit from guardrails."

## Notes

- Catégories 6, 7 peuvent se brancher sur hooks/CI (enforcement vs advisory).
- Catégorie 8 (Runbooks) = pattern multi-tool investigation → structured report, proche du devil's advocate / project-auditor forge.
- Catégorie 9 (Infra Ops) → guardrails obligatoires pour actions destructives, cohérent avec doctrine hooks lint/security/scope du 22 mai.

## Liens

- [[reference_boris_thariq_bestpractices]]
- [[reference_skills_guide]]
