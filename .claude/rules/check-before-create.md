---
description: "Short reminder pointing to canonical sequence — memory + vault + references + forge skill + delegate. Full spec in sequence-canonique-modification.md"
---

# Verifier AVANT de creer ou modifier — RAPPEL COURT

Avant toute création/modification/optimisation de composant (skill, agent, hook, rule, CLAUDE.md), AUCUNE EXCEPTION :

1. **Mémoire** — relire feedbacks pertinents (`feedback_skill_*`, `feedback_agent_*`, `feedback_hooks_*`, `feedback_major_mistakes`)
2. **Séquence canonique A→B→C→D→E** — voir source unique : `.claude/rules/sequence-canonique-modification.md` (et vault [[methode-analyser-repo]] section "ORDRE CANONIQUE")
3. **References existantes** — lire les `references/` du composant cible AVANT modification
4. **Référence forge** — pour les skills : `skill-creator` contient toute la doctrine + vault [[comment-creer-skill]]. Pour agents : `cc-agents-ref`. Pour hooks : `cc-hooks-ref`.
5. **Déléguer aux spécialistes** — SKILL.md → invoquer la skill `skill-creator` (Skill tool), agents/*.md → agent-creator (hook bloque), CLAUDE.md → claudemd-optimizer (hook bloque), hooks → hook-creator.

## Anti-patterns (observés en production)

- "Je sais déjà" → FAUX. 2026-04-26 : 6 skills + 14 agents édités à la main sans vérification, tous non conformes
- "C'est juste un petit ajout" → petit ajout × 20 = gros problème de conformité
- "Je vais aller plus vite sans agent" → plus vite OUI, mais non conforme = refaire tout après
- "Je vais vérifier après" → non, tu oublieras. Vérifier AVANT ou le hook te bloquera.

## Source canonique unique

La séquence A→B→C→D→E détaillée (avec cas d'usage par type de tâche, anti-patterns, exemples concrets) vit dans **`.claude/rules/sequence-canonique-modification.md`**. Cette rule (`check-before-create.md`) est un rappel court qui pointe vers la canonique — pas de duplication (cf [[feedback_single_source_truth_vault_canonique]]).
