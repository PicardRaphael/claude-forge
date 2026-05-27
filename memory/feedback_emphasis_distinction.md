---
name: emphasis-prompt-vs-skill
description: Emphasis (JAMAIS, YOU MUST, CRITICAL) OK dans skills/rules/agents/CLAUDE.md, mais reduire dans tool descriptions (overtriggering). Distinction cle.
type: feedback
originSessionId: f3b37008-cac0-4a75-ae36-b058217ea80b
---
Emphasis ("IMPORTANT", "YOU MUST", "JAMAIS", "TOUJOURS") est RECOMMANDE par Anthropic dans CLAUDE.md, rules, skills et agents pour ameliorer l'adherence (~80%).

Reduire l'emphasis UNIQUEMENT dans les descriptions d'outils (tool triggering) — cause overtriggering sur Claude 4.5+/4.6.

**Why:** J'ai failli lancer un nettoyage massif des JAMAIS/TOUJOURS dans 3 projets en me basant sur une generalisation trop large. L'info source parlait specifiquement des tool descriptions, pas des instructions comportementales.

**How to apply:**
- Ne jamais recommander de retirer l'emphasis des skills/rules/agents/CLAUDE.md
- Si une regle est vraiment safety-critical (DDL, securite) → recommander un hook deterministe plutot que plus d'emphasis
- Verifier la source avant de generaliser une finding prompt engineering aux instructions agentic
