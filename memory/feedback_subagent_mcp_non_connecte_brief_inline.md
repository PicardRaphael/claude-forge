---
name: subagent-mcp-non-connecte-brief-inline
description: "MCP frontmatter d'un sub-agent = décoratif (non connecté en contexte). Un brief 'lis les canoniques via MCP' force le sub-agent à cat le vault. Fournir le contenu inline, jamais ordonner de lire le vault."
metadata:
  type: feedback
---

Le `tools: mcp__forge-brain__*` du frontmatter d'un sub-agent NE garantit PAS que le serveur MCP soit connecté dans son contexte d'exécution — il ne l'est pas (`No such tool available`). Si le brief ordonne « lire les canoniques via MCP » sans fournir le contenu, le sub-agent fallback sur `cat`/`find` du vault (viole la doctrine MCP-only). Tout brief sub-agent impliquant le vault doit contenir les extraits canoniques INLINE + interdiction stricte d'accès vault brut + ESCALADE si manque.

**Why:** Chantier A (27 mai 2026). skill-creator briefé « lis doctrine-vivante + comment-creer-skill via MCP » a `cat` le vault. Diagnostic empirique : frontmatter MCP correct, mais MCP non connecté en sous-agent — confirmé sur 2 agents (skill-creator observé, hook-creator → `No such tool available: mcp__forge-brain__read_note`). Le re-brief inline (mcp-brief-then-direct) a résolu : 0 accès vault. Variante de [[feedback_feedback_reviole_3x_regle_insuffisante]] : règle inapplicable STRUCTURELLEMENT (pas de moyen), pas négligente.

**How to apply:** Avant tout dispatch creator/analyste touchant le vault : la session principale lit via MCP (elle SEULE a le MCP effectif), extrait les sections, les met inline dans le brief, ajoute « JAMAIS cat/find/grep/Read sur le vault ; si manque, ESCALADE ». Complète [[cartographie-exhaustive-avant-delegation]] (grep cible) et [[session-consulte-vault-avant-brief]] (extraire avant briefer). Note canonique : amendement de [[pattern-mcp-brief-then-direct]].
