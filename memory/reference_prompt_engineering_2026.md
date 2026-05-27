---
name: prompt-engineering-2026
description: State of prompt engineering avril 2026 — context engineering, adaptive thinking, outcome delegation, Graph of Thoughts. Claude vs Gemini differences.
type: reference
originSessionId: f3b37008-cac0-4a75-ae36-b058217ea80b
---
## 3 shifts majeurs de 2026

| Avant | Apres |
|---|---|
| Prompt unique | Context window entiere a chaque step (Context Engineering, Karpathy) |
| budget_tokens manuel | effort parameter + adaptive thinking |
| Instructions step-by-step | Criteres de succes + delegation (Outcome Delegation) |

## Techniques nouvelles 2026

- **Context Engineering** (Karpathy) — gerer tout ce qui entre dans la context window, pas juste le prompt
- **Outcome Delegation** — definir criteres de succes, pas les etapes
- **Graph of Thoughts** (ETH Zurich) — raisonnement en graphe +62% vs Tree of Thoughts
- **Reflexion** — agent examine sa trace, stocke lecons en memoire
- **Dynamic Tool Loading** — embed descriptions, retrieve top-k pertinents
- **Context Compaction** — resume traces pour agents long-horizon
- **Tool Description Engineering** — descriptions outils = prompt engineering (gains SWE-bench)
- **Adaptive Prompting** — modele co-auteur de ses prompts (Console Anthropic, Alex Albert)

## Breaking changes Claude

- Prefill deprecated sur 4.6+ → Structured Outputs
- budget_tokens deprecated → adaptive thinking
- Skills = standard ouvert (agentskills.io)
- Opus 4.6 explore plus → reduire "sois exhaustif"
- **Langage agressif dans les TOOL DESCRIPTIONS** cause de l'overtriggering sur Claude 4.5+/4.6 — reduire l'emphasis dans les descriptions d'outils. MAIS : Anthropic recommande explicitement l'emphasis ("IMPORTANT", "YOU MUST") dans CLAUDE.md/rules/skills pour ameliorer l'adherence (~80%). Distinction cle : tool triggering (reduire) vs regles comportementales (emphasis OK) vs safety-critical (hooks, pas prompts).

## Differences cles Claude vs Gemini

- Claude : XML tags, adaptive thinking (effort), prefill deprecated, 200K-1M context
- Gemini : system_instruction (remplace defaut), thinking_level, response_schema natif, grounding Google Search, code execution Python, multimodal video/audio, 1M natif, temperature=1.0 obligatoire Gemini 3
- Gemini : GEMINI.md remplace le system prompt (≠ CLAUDE.md qui s'ajoute)

## Skill /craft-prompt

Cree dans claude-forge avec 3 references :
- techniques-claude.md (30+ techniques)
- techniques-gemini.md (Gemini 3, grounding, code exec, JSON mode)
- techniques-universelles.md (patterns pour tout LLM, anti-patterns, checklist)

## Confirmations avril 2026

- **Context Engineering = discipline dominante** — engineering de systemes d'information (write/select/compress/isolate) plutot que craft de prompts
- **Amanda Askell** : document 35K+ tokens pour la personnalite de Claude, 100+ pages (moral reasoning + sujets sensibles). Mi-avril : mise a jour system prompt claude.ai "en collaboration avec Claude" (thread detaille)
- **Alex Albert** : prompt engineering = "systematic thinking" (latence, sources, version control). Avril : "CC experience pour tous les knowledge workers" — non-ingenieurs soumettent des PRs
- **Ethan Mollick** : "prompt engineering is disappearing" — interagir en conversation, iterer
- **Karpathy** : shift vers "LLM wikis" (knowledge management, 400K mots). AutoResearch 21K stars. Ere de l'"agentic engineering"
- **Adaptive Thinking pitfall** : peut allouer ZERO tokens reflexion → hallucinations precises (faux SHA, packages inexistants). Garde-fou : `CLAUDE_CODE_EFFORT_LEVEL=max` + `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Sweet spot prompts = 150-300 mots (~3000 tokens max)
- **Stanford AI Index** (13 avril) : Anthropic #1 Arena, IA agentique = "gains les plus extremes", +26% productivite dev

## Sources cles

- Anthropic Engineering Blog : context engineering, tool descriptions
- Karpathy (X) : definition context engineering, LLM wikis
- Amanda Askell (@AmandaAskell) : prompt engineering lead Anthropic, soul architect Claude
- Alex Albert (@alexalbert__) : adaptive prompting, prompt generator
- Ethan Mollick (@emollick) : observations sur la disparition du prompt engineering
- ETH Zurich (arXiv) : Graph of Thoughts
- Google ai.google.dev : Gemini prompting strategies
- Kaggle whitepaper (Lee Boonstra) : 68 pages prompt engineering Gemini
