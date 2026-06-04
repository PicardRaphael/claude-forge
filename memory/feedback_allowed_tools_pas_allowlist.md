---
name: allowed-tools-pas-allowlist
description: Le champ `allowed-tools` d'une skill est une PRÉ-APPROBATION (anti-prompt permission), PAS une allowlist restrictive. Tous les outils restent appelables, y compris Skill et MCP non listés. Source Anthropic.
metadata:
  type: reference
---

Le champ frontmatter `allowed-tools` d'une skill **pré-approuve** les outils listés (Claude les utilise sans prompt de permission quand la skill est active). Il **NE restreint PAS** les outils disponibles.

Verbatim doc Anthropic (`code.claude.com/docs/en/skills`, section "Pre-approve tools for a skill") :
> "The `allowed-tools` field grants permission for the listed tools while the skill is active... **It does not restrict which tools are available: every tool remains callable**, and your permission settings still govern tools that are not listed."

Conséquence : une skill avec `allowed-tools: Read, Grep` peut quand même invoquer le tool `Skill` (donc une autre skill) et des MCP non listés — ils restent callable, juste soumis aux permissions de base. Pour RETIRER un outil, c'est `disallowed-tools` (l'inverse).

**Why:** Le 3 juin 2026, un sub-agent auditeur (general-purpose) a flaggé un **faux P0** sur les skills po-lojii : il affirmait que `allowed-tools` sans `Skill`/`mcp__obsidian-brain__*` empêchait d'invoquer les skills brain. Faux — vérifié en source primaire. Preuve empirique concordante : `neo-brain-dev-admin` avait été invoquée avec succès la même session sans que `Skill` soit dans un allowed-tools. Si j'avais appliqué le P0, j'aurais "corrigé" un non-problème et alourdi les frontmatters.

**How to apply:**
1. Ne jamais traiter `allowed-tools` comme une allowlist qui bloque — c'est une pré-approbation. Pour bloquer un outil : `disallowed-tools`.
2. Un finding de sub-agent auditeur sur un comportement de la plateforme (pas sur le code) = hypothèse à vérifier en source primaire AVANT d'agir, surtout si le sub-agent lui-même écrit "à vérifier au 1er run". Cf [[feedback_subagent_audit_category_error]] + [[feedback_user_invocable_orthographe]] (vérité ≠ supposition).
3. La canonique vault `comment-creer-skill` décrit `allowed-tools` comme "optionnel — liste outils" sans préciser non-restrictif → candidat enrichissement vault (proposé à Raphael 3 juin, à valider).
