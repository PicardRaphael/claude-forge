# Domaine — Concurrents (Modèles & Produits Coding)

Couvre : OpenAI, Google/Gemini, Cursor, GitHub Copilot, xAI/Grok, leaders industrie visionnaires.
Nombre de queries : 29 — **Découper sur 3 agents** (Agent A + Agent B + Agent C)

## Changelogs concurrents

- OpenAI : `https://openai.com/index` (blog/announcements)
- Gemini CLI / Antigravity : `https://github.com/google-gemini/gemini-cli/blob/main/CHANGELOG.md` (⚠️ Gemini CLI + Code Assist ont cessé de servir les requêtes le 18 juin 2026 → migration forcée vers **Antigravity + Antigravity CLI** ; surveiller aussi les release notes Antigravity)
- Cursor : `https://cursor.com/changelog`
- GitHub Copilot : `https://github.blog` (filtered for Copilot)

<!-- SYNC:leaders:start — généré par scripts/sync-leaders.py, NE PAS éditer à la main -->

## Leaders canonisés (13) — vault 05-Leaders/industrie/

| Personne | Rôle | Sources |
|----------|------|---------|
| **Allie K. Miller** | CEO Open Machine, ex-Global Head of ML for Startups AWS. Voice business-centric sur AI… | www.alliekmiller.com, www.linkedin.com |
| **Arthur Mensch** | CEO & Co-founder Mistral AI | mistral.ai |
| **Chip Huyen** (@chiphuyen) | Auteure & entrepreneure IA | huyenchip.com, github.com |
| **Dario Amodei** | CEO & Co-founder Anthropic | en.wikipedia.org, darioamodei.com |
| **Demis Hassabis** | CEO et co-fondateur DeepMind (acquis par Google 2014). Architecte AlphaGo, AlphaFold (N… | deepmind.google, en.wikipedia.org |
| **Ethan Mollick** (@emollick) | Associate Professor | www.oneusefulthing.org |
| **Geoffrey Hinton** | Père du deep learning, Turing Award 2018, Nobel Prize Physics 2024. University Professo… | en.wikipedia.org, www.fpa.es |
| **Ilya Sutskever** | Co-fondateur OpenAI, ex-Chief Scientist. Désormais CEO Safe Superintelligence Inc (SSI)… | en.wikipedia.org, ssi.inc |
| **Liang Wenfeng** | Founder & CEO DeepSeek | deepseek.com |
| **Reid Hoffman** | Co-fondateur LinkedIn, investisseur AI majeur, board Inflection AI. Framework 'person-p… | www.linkedin.com, www.greylock.com |
| **Sam Altman** (@sama) | CEO OpenAI | x.com, openai.com |
| **Tobi Lütke** (@tobi) | CEO Shopify. Créateur de qmd (github.com/tobi/qmd) : moteur de recherche local pour mar… | github.com, gist.github.com |
| **Yoshua Bengio** | Co-Turing Award 2018, fondateur MILA (Université de Montréal). Mathematical foundations… | en.wikipedia.org, mila.quebec |

> Bloc généré depuis le vault. Pour ajouter/retirer un leader : créer/supprimer la fiche dans `05-Leaders/industrie/` puis relancer `py scripts/sync-leaders.py`.
> Les leaders sans handle (`@`) sont en mode dégradé — compléter les queries à la main.

<!-- SYNC:leaders:end -->

## Watchlist signaux non canonisés

> Cibles suivies par cc-news mais sans fiche vault dédiée (ou fichées dans un autre domaine). Section éditable à la main, **jamais touchée par le sync**. Le bloc synced ci-dessus liste `05-Leaders/industrie/`.

| Personne | Rôle | Sources |
|----------|------|---------|
| **Kevin Weil** (@kevinweil) | CPO OpenAI | x.com/kevinweil |
| **Logan Kilpatrick** (@OfficialLoganK) | Ex-OpenAI → Google AI Studio lead | x.com/OfficialLoganK |
| **Aman Sanger** (@amanrsanger) | Co-founder & CEO Cursor/Anysphere | x.com/amanrsanger |
| **Thomas Dohmke** (@ashtom) | CEO GitHub | x.com/ashtom |
| **Andrej Karpathy** | Ex-Tesla/OpenAI, AI coding visionnaire (fiche vault en `agents/`) | — |
| **Yann LeCun** | Meta Chief AI Scientist, AMI Labs (fiche vault en `prompt/`) | — |

## Queries à exécuter

### Agent A — OpenAI + Google

#### OpenAI (modèles + Codex CLI)
```
OpenAI new model release GPT
OpenAI Codex CLI new features update changelog
ChatGPT new features coding agents
Sam Altman OpenAI announcements
Kevin Weil OpenAI CPO product
site:openai.com/index
```

#### Google (Gemini modèles + CLI + AI Studio)
```
Google Gemini new model release
Gemini CLI new features update changelog
Google AI Studio new features
Demis Hassabis Google DeepMind
site:blog.google/technology/ai gemini
```

### Agent B — Cursor + Copilot + xAI + Leaders

#### Cursor
```
Cursor AI new features changelog update
site:cursor.com/changelog
```

#### GitHub Copilot
```
GitHub Copilot new features update
GitHub Copilot coding agent changelog
site:github.blog copilot
```

#### xAI / Grok
```
xAI Grok new model coding features
Elon Musk xAI announcements
```

#### Leaders industrie & visionnaires
```
Andrej Karpathy AI coding software
Yann LeCun AI agents world models AMI Labs
Logan Kilpatrick Google AI Studio
```

### Agent C — Leaders industrie (vault 05-Leaders/industrie/)

```
@sama OR Dario Amodei frontier lab announcements
Arthur Mensch Mistral AI open-source sovereignty
Liang Wenfeng DeepSeek new model GRPO
Demis Hassabis DeepMind research
@chiphuyen AI engineering OR @emollick AI work
Ilya Sutskever SSI safe superintelligence
Geoffrey Hinton OR Yoshua Bengio AI safety risk
Reid Hoffman OR Allie K Miller OR Tobi Lütke AI business
```

## Capitalisation vault

Nouveaux modèles → `<NN>-<Fournisseur>/models/` (ex `02-OpenAI/models/`)
Nouvelles features produit coding → `<NN>-<Fournisseur>/products/` (ex `09-Anysphere/products/` pour Cursor, `02-OpenAI/products/` pour Codex)
Info industrie (funding, acquisitions) → `06-Industrie/`
