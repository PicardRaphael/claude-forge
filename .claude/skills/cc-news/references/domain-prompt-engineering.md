# Domaine — Prompt Engineering & Techniques

Couvre : techniques de prompting, context engineering, guides officiels, papers académiques, prompt injection defense.
Nombre de queries : 15 — **Découper sur 2 agents** (Agent A + Agent B)

## Sources officielles

- `platform.claude.com/docs/en/build-with-claude/prompt-engineering`
- `developers.openai.com/api/docs/guides/prompt-guidance`
- `ai.google.dev/gemini-api/docs/prompting-strategies`

<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->

## Leaders canonisés (11) — vault 05-Leaders/prompt/

| Personne | Rôle | Sources |
|----------|------|---------|
| **Amanda Askell** (@AmandaAskell) | Researcher — Alignment & Character | x.com, www.anthropic.com |
| **Anthony Mikinka** | Chercheur indépendant, auteur de 'Universal Conditional Logic: A Formal Language for Pr… | arxiv.org |
| **Denny Zhou** | Research Scientist Google DeepMind, fondateur Reasoning Team Google Brain (intégrée dan… | dennyzhou.github.io, scholar.google.com |
| **Elvis Saravia** | Co-Founder + Lead AI Researcher DAIR.AI, auteur du Prompt Engineering Guide (promptingg… | www.promptingguide.ai, www.getprog.ai |
| **Ethan Mollick** (@emollick) | Associate Professor Wharton School. Voix #1 sur Generative AI dans le workplace/work fu… | www.linkedin.com, papers.ssrn.com |
| **Imran Khan** | Chercheur indépendant, auteur de 'You Don't Need Prompt Engineering Anymore: The Prompt… | arxiv.org |
| **Jason Wei** | Inventeur de Chain-of-Thought prompting (NeurIPS 2022), instruction tuning (FLAN), emer… | www.jasonwei.net, arxiv.org |
| **Riley Goodside** | Premier Staff Prompt Engineer au monde (Scale AI 2022, désormais Google DeepMind). Pion… | thegradientpub.substack.com, twimlai.com |
| **Sander Schulhoff** | CEO Learn Prompting + HackAPrompt, auteur principal The Prompt Report (1500+ papers, 20… | learnprompting.org, sanderschulhoff.com |
| **Takeshi Kojima** | Auteur principal de 'Large Language Models are Zero-Shot Reasoners' (NeurIPS 2022) — pa… | arxiv.org, weblab.t.u-tokyo.ac.jp |
| **Yann LeCun** | Turing Award 2018, ex-Chief AI Scientist Meta, co-fondateur AMI Labs (déc 2025, $1B). P… | en.wikipedia.org, ai.meta.com |

> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer la fiche dans `05-Leaders/prompt/` puis relancer `py scripts/sync-leaders.py`.
> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.

<!-- SYNC:leaders:end -->

## Watchlist signaux non canonisés

> Cibles suivies par cc-news mais fichées dans un autre domaine vault. Section éditable à la main, **jamais touchée par le sync**.

| Personne | Rôle | Sources |
|----------|------|---------|
| **Alex Albert** (@alexalbert__) | Anthropic head of Claude relations (fiche vault en `claude-code/`) | x.com/alexalbert__ |

## Queries à exécuter

### Agent A — Guides officiels + techniques

```
Amanda Askell prompt engineering Claude
Alex Albert Claude prompt techniques
Anthropic prompt engineering guide update
OpenAI GPT-5 prompting best practices
Gemini prompt engineering new techniques
"context engineering" OR "harness engineering"
prompt injection defense techniques
"adaptive thinking" Claude
```

### Agent B — Chercheurs + papers

```
@emollick prompt engineering
Jason Wei chain-of-thought emergent abilities
Denny Zhou reasoning LLM DeepMind
Sander Schulhoff Learn Prompting HackAPrompt
Riley Goodside prompt engineering
new prompt techniques academic papers (Kojima, Khan, Mikinka, Saravia)
Yann LeCun world models LLM critique
```

## Capitalisation vault

Nouvelles techniques → `04-Techniques/prompt-engineering/`
Nouveaux prompts/system prompts → `07-Prompts/<sous-dossier>/`
Techniques dépréciées → `04-Techniques/prompt-engineering/deprecated-techniques-<année>.md`
