---
name: methode-abcde-carte-pas-verdict
description: Niveau 1 mesure statique frontmatter = CARTE pas VERDICT. Niveau 2 transcripts JSONL = verdict echantillon. Niveau 3 instrumentation continue = verdict statistique. Refactor mass sur Niveau 1 seul = reproduction F1/F2.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632e98ec-976c-4408-8507-4988788a8d26
---

Avant tout refactor mass d'agents/skills/hooks base sur metriques frontmatter (lines, tools, sections, mots), exiger Niveau 2 transcripts JSONL ou Niveau 3 CSV avant verdict.

**Why:** Session 3 (22-23 mai 2026), Niveau 1 a flagge `architect-deep` 5/5 seuils depasses (211L, 1518 mots, 10 tools, 8 skills, 11 sections H2) comme "candidat split urgent". Niveau 2 transcripts JSONL a montre **6 ops typique** = SOUS le seuil canonique Cat Wu (6-8 ops/agent). Le frontmatter mesure CAPACITE, pas USAGE. Refactor sur Niveau 1 seul aurait casse un agent qui fonctionne bien. Verdict advisor verbatim : "Tu conflates capacite avec usage. C'est un fait Niveau 1 transforme en verdict."

Sur `dev-neochat` (n=31 invocations) : mean=42.8 ops MAIS median=27, p75=52, p90=116, max=198. La moyenne est tiree par outliers. Pattern = "invocations parfois mal scopees", PAS "agent surcharge en steady state". Solution = option (b) rule scope invocations callers, PAS split agent (option (a) couteuse).

**How to apply:**
1. Niveau 1 (`wc -l`, count tools, count sections) = CARTE — identifie candidats SUSPECTS
2. Niveau 2 (transcripts JSONL `~/.claude/projects/<repo>/<session>/subagents/agent-*.jsonl`) = VERDICT echantillon — analyse ops reelles
3. Niveau 3 (hook PostSubagentStop -> CSV append-only) = VERDICT statistique avec n>>30 sur duree
4. **JAMAIS refactor mass sans Niveau 2 minimum**. Pattern reproduction F1/F2 si non.
5. Si pression d'agir : option (b) preferer (a) - rule de scope plutot que split agent. 1 ligne, 0 risque structurel.
6. Cf canonique [[comment-creer-agent]] : seul seuil hard = "max 6-8 ops/agent" (Cat Wu), c'est ops dans TRANSCRIPT REEL pas tools listes.

Documente dans vault forge : `Knowledge/explorations/niveau-1-static-mesure-agents-neo-ia-2026-05-22.md` (UPDATE 2026-05-23 avec Niveau 2 findings).
