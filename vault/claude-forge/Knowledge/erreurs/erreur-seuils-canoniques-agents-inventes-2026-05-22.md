---
titre: "Erreur — Seuils canoniques agents inventés (6-8 ops, <200L) puis confirmés mythes"
resume: "J'ai cité 5 seuils 'canoniques' pour les agents Claude Code dans les notes vault et audits ia_back. 4/5 confirmés mythes par recherche web 2026-05-22 — extrapolations ou confusion. Seuls 2 seuils sont vraiment canoniques (CLAUDE.md<200L, SKILL.md<500L)."
aliases:
  - "erreur seuils agents mythes"
  - "mythes canoniques agents claude code"
  - "6-8 ops agent mythe"
  - "200L agent mythe"
  - "max 8 tools agent mythe"
derniere-maj: 2026-05-22
auteur: claude
type: erreur
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
  - "#sujet/canoniques"
  - "#methode/verification"
---

# Erreur — Seuils canoniques agents inventés

## Ce qui s'est passé

Pendant l'audit ia_back du 22 mai 2026, j'ai cité comme "canoniques" 5 seuils numériques pour les agents Claude Code :

1. "Max 6-8 opérations par agent" (attribué à Cat Wu)
2. "Agent < 200 lignes" (attribué à Anthropic)
3. "Agent < 1500 mots"
4. "Max 8 tools par agent"
5. "Max N skills frontmatter par agent"

Ces seuils ont servi de **grille d'évaluation** pour juger les agents ia_back ("⚠️ À surveiller : architect-deep 237L, codebase-analyst 270L...").

## Pourquoi c'était une erreur

Raphael a challengé : "tu es sûr que c'est canonique ?". Recherche web (sub-agent dédié) a confirmé :

| Seuil | Vérité |
|---|---|
| 6-8 ops/agent | ❌ Mythe — aucune source. Confusion avec "1/2-4/10+ subagents" Anthropic |
| Agent < 200L | ❌ Mythe — 200L = pour CLAUDE.md, pas agents |
| Agent < 1500 mots | ⚠️ Single source (dbreunig, en tokens pas mots) |
| Max 8 tools/agent | ❌ Mythe — Anthropic refuse explicitement un chiffre |
| Max N skills | ❌ Pas de règle documentée |

Sources vérifiées :
- [Anthropic Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [HumanLayer — Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [dbreunig — How Claude Code Builds a System Prompt](https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html)
- [Anthropic — Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

## Seuils VRAIMENT canoniques (confirmés)

| Seuil | Sources convergentes |
|---|---|
| **CLAUDE.md < 200 lignes** | ✅ Anthropic docs + HumanLayer + autres |
| **SKILL.md body < 500 lignes** | ✅ Anthropic docs |

## Conséquence

Tous les audits qui s'appuyaient sur les 4 mythes étaient **biaisés**. Verdict "agent X à surveiller car 237L" = sans fondement.

## Cause racine

J'ai accumulé ces seuils dans le vault via [[comment-creer-agent]] sans **valider par recherche web** au moment de la création. Effet de répétition : à force d'apparaître dans plusieurs notes vault, ces chiffres ont pris l'apparence de "canoniques".

C'est exactement le pattern que [[feedback_lire_canoniques_avant_audit]] essaie d'éviter : **lire les canoniques d'abord = biais de perception**. Si la canonique elle-même est un mythe, c'est encore pire.

## Comment l'éviter à l'avenir

1. **Pour TOUT chiffre canonique cité**, vérifier 4+ sources convergentes (cf prompt `output/audit-vault-thematique/`)
2. **Si moins de 4 sources** → marquer `⚠️ Single source` ou `❌ Mythe`
3. **Anthropic team > tous** en cas de désaccord
4. **Pas d'extrapolation** : si une source dit "scope au minimum nécessaire" sans chiffre, ne PAS inventer "max 6-8 ops"

## Action prise (2026-05-22)

- Mémoire : [[reference_seuils_canoniques_agents_mythes]] créé pour ne pas les réutiliser
- Mémoire : [[feedback_single_source_truth_vault_canonique]] créé pour patcher vault, pas dupliquer
- 9 prompts d'audit thématique vault créés dans `output/audit-vault-thematique/` pour valider toutes les claims des canoniques à 4+ sources

## Liens

- [[feedback_lire_canoniques_avant_audit]] — ordre A→B→C→D→E, pas canoniques avant analyse
- [[reference_seuils_canoniques_agents_mythes]] — référence rapide des mythes
- [[comment-creer-agent]] — à patcher dans prompt d'audit Claude Code (`01-claude-code.md`)
- [[methode-analyser-repo]] — section ORDRE CANONIQUE intègre A→B→C→D→E
