---
name: askuserquestion-sub-agent-impossible
description: AskUserQuestion ne fonctionne PAS en sub-agent (verbatim Anthropic issue
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f9514081-5b0f-4d0a-934a-9a3a4fee9a3e
---

Si un sub-agent rencontre une ambiguïté, il ne peut PAS appeler `AskUserQuestion` lui-même — le tool est silencieusement ignoré dans le contexte sub-agent (verbatim Anthropic GitHub issue #18721).

**Why:** session 24 mai 2026, j'allais ajouter `AskUserQuestion` aux tools de 15 sub-agents pour permettre l'escalade utilisateur. Recherche web post-implémentation a révélé la limitation Anthropic. Pattern correct = sub-agent retourne markdown structuré `## AMBIGUÏTÉ DÉTECTÉE` avec options + recommandation + question pour user, **session principale lit le bloc et appelle AskUserQuestion elle, puis re-dispatch avec la réponse**.

**How to apply:**
- ❌ Jamais ajouter `AskUserQuestion` au frontmatter `tools:` d'un sub-agent (inutile)
- ✅ Ajouter dans le **body** du sub-agent une section "Si AMBIGU détecté — STOP + format ESCALADE"
- ✅ Sub-agent retourne markdown structuré (5 champs : Contexte, Ambiguïté, Options, Recommandation, Question, État actuel)
- ✅ Session principale = orchestrateur user interaction
- Pattern jumeau de ESCALADE REQUISE (hors-scope) — différence : AMBIGUÏTÉ = manque info, ESCALADE = autre agent doit prendre

Vault canonique : [[anti-reentrance-sub-agents-pattern-escalade]] + section "AJOUT 24 mai 2026" dans [[comment-creer-agent]].

Déployé 24 mai sur 15 sub-agents (9 neo_ia + 5 ia_back + 1 forge devils-advocate). Hook SubagentStop `escalade-detector` détecte les markers et suggère en stderr.
