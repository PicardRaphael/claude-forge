---
name: skills-complete-guide
description: Official Anthropic guide (33 pages) for building Claude skills - located at .claude/skills/cc-skills-ref/references/complete-guide.pdf
type: reference
---

Le guide officiel Anthropic "The Complete Guide to Building Skills for Claude" est disponible localement à `.claude/skills/cc-skills-ref/references/complete-guide.pdf` (33 pages, 548KB).

Contenu clé :
- **Ch1 Fundamentals** : progressive disclosure (3 niveaux), composabilité, portabilité
- **Ch2 Planning** : 3 catégories de skills (Document/Asset Creation, Workflow Automation, MCP Enhancement), success criteria, YAML frontmatter rules
- **Ch3 Testing** : triggering tests, functional tests, performance comparison, skill-creator tool
- **Ch4 Distribution** : GitHub hosting, API `/v1/skills`, organization deployment
- **Ch5 Patterns** : 5 patterns (sequential workflow, multi-MCP coordination, iterative refinement, context-aware tool selection, domain-specific intelligence)
- **Ch6 Resources** : anthropics/skills repo, community, bug reports
- **Ref A** : Quick checklist before/during/after upload
- **Ref B** : YAML frontmatter complet (name, description, license, allowed-tools, metadata)
- **Ref C** : Liens vers skills exemples (PDF, DOCX, PPTX, XLSX, partners)

Règles critiques rappelées :
- SKILL.md exact (case-sensitive), pas de README.md dans le dossier skill
- Description MUST include WHAT + WHEN (trigger phrases), < 1024 chars, pas de XML tags
- kebab-case pour name et dossier
- SKILL.md < 5000 mots, déporter le détail dans references/
