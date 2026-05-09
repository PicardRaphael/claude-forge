---
description: "Mandatory 5-step checklist before any create/modify: memory, vault, references, forge skill, delegate to specialist"
---

# Verifier AVANT de creer ou modifier — OBLIGATOIRE

Avant toute creation ou modification de composant (skill, agent, hook, rule, prompt), executer ce checklist dans l'ordre. AUCUNE EXCEPTION, meme si "c'est juste un petit changement".

## 1. Memoire (MEMORY.md)

Relire les feedbacks pertinents au TYPE de tache. Les erreurs passees sont documentees — ne pas les refaire.
- skill → `feedback_skill_*`, `feedback_use_skill_creator`
- agent → `feedback_agent_*`, `feedback_no_cto_agent`
- hook → `feedback_hooks_*`
- general → `feedback_major_mistakes`

## 2. Forge Brain (vault) — via MCP forge-brain

Interroger le vault via MCP (JAMAIS CLI, Grep ou Read brut) — AVANT de toucher quoi que ce soit :

```
forge-brain:search_brain  query="<sujet>"  limit=10
forge-brain:search_brain  query="erreur"   limit=5
```

Sections a chercher :
- `04-Techniques/` — best practices, patterns
- `Knowledge/erreurs/` — erreurs passees a eviter (CRITIQUE)
- `Knowledge/questions/` — questions deja resolues
- `07-Prompts/` — prompts reutilisables

## 3. References existantes

Lire les `references/` du composant cible AVANT de modifier le SKILL.md ou l'agent.
Si le composant n'existe pas encore, lire les references des composants similaires.

## 4. Skill de reference forge

Charger la skill forge pertinente (cc-skills-ref, cc-agents-ref, cc-hooks-ref, cc-prompt-ref) pour avoir le format a jour.

## 5. Deleguer aux agents specialises

SKILL.md → skill-creator, agents/*.md → agent-creator, CLAUDE.md → claudemd-optimizer, hooks → hook-creator.
Le hook `delegate-guard.py` BLOQUERA l'edit direct de toute facon. Autant deleguer d'entree.

## Anti-patterns (TOUS observes en production)

- "Je sais deja" → FAUX. C'est arrive le 2026-04-26 : 6 skills + 14 agents edites a la main sans rien verifier
- "C'est juste un petit ajout" → petit ajout x 20 = gros probleme de conformite
- "Je vais aller plus vite sans agent" → plus vite OUI, mais non conforme = refaire tout apres
- "Je vais verifier apres" → non, tu oublieras. Verifier AVANT ou le hook te bloquera.
