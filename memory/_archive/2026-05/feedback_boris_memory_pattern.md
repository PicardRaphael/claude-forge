---
name: boris-memory-compounding
description: Pattern Boris Cherny pour mémoire compounding — CLAUDE.md ~100 lignes max, erreurs dans Auto Memory, relire avant d'agir. Appliquer sur tous les repos.
type: feedback
originSessionId: fdb162f8-52a4-438b-a60a-c8e2ce6e37cf
---
Boris Cherny (créateur Claude Code) — pattern mémoire compounding :

1. **CLAUDE.md = instructions de survie** — ~100 lignes max. "Pour chaque ligne : si je l'enlève, Claude fait des erreurs ? Non → couper."
2. **Erreurs dans Auto Memory** — après chaque correction, sauvegarder feedback rule (Why + How to apply) dans .claude/agent-memory/
3. **Relire avant d'agir** — en début de tâche, scanner les feedback rules existantes
4. **@claude en code review** — tagger pour ajouter les learnings au CLAUDE.md
5. **Compounding** — plus on travaille, plus le système s'améliore. 6 mois = centaines de rules, taux d'erreur chute

Karpathy (LLM Wiki) — même philosophie :
- "Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase"
- Plain markdown > vector DB. 70x plus efficace que RAG
- Le LLM compile le knowledge, pas juste le stocke

**Why:** Audit /insights montre que neo_ia a 0 feedback rules malgré la tuyauterie en place, ia_back en a 24 (ça compound). La différence c'est l'habitude de sauvegarder.

**How to apply:** Vérifier que chaque repo a (1) learn-from-mistakes rule, (2) memory: project sur tous agents, (3) section Mémoire dans CLAUDE.md. Le config-guardian vérifie ça automatiquement.
