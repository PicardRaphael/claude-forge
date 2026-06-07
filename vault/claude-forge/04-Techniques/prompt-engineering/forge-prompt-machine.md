---
titre: "FORGE Prompt Machine — Techniques croisees BellumAI x Askell"
resume: "12 principes de generation de prompts (FORGE v3 de Theo Haddad) croises avec les best practices Askell/Anthropic, orientes creation de skills/agents"
aliases:
  - "FORGE BellumAI"
  - "prompt machine"
  - "generation de prompts"
  - "12 principes prompts"
  - "bellumAI FORGE"
  - "checklist prompt skill"
domaine: technique
type: technique
derniere-maj: 2026-05-23
auteur: claude
sources:
  - "FORGE v3 — Theo Haddad, CEO BellumAI et SalesConnect"
  - "[[amanda-askell-prompt-engineering]] — TDD for system prompts"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/technique"
  - "#domaine/prompt-engineering"
---

## Contexte

FORGE est un system prompt de **Theo Haddad** (Founder BellumAI + SalesConnect — personne vérifiée publique, LinkedIn) concu pour generer des prompts optimises pour Claude. Version 3, orientee production (pas de bavardage, chaque reponse = un livrable).

> ⚠️ **Source FORGE v3 non publiable** : le system prompt original n'est pas publiquement diffusé. Les 12 principes ci-dessous sont une **synthèse forge** dérivée des recommandations Haddad croisées avec Askell + Anthropic docs. Chaque principe est individuellement canonique (sourçable), mais l'attribution "12 principes FORGE" est forge-curated, pas verbatim BellumAI.

Cette note extrait les principes utiles pour la creation de **skills, agents, rules et prompts** dans Claude Code, croises avec les pratiques [[amanda-askell-prompt-engineering]] et Anthropic.

## Les 12 principes FORGE — appliques aux skills/agents

### 1. Structure XML / sections semantiques

FORGE utilise du XML pour creer des zones semantiques distinctes. Claude les traite avec plus de precision que la prose libre.

**Application skills/agents :** Les sections markdown des SKILL.md (##) jouent le meme role que les balises XML. Chaque section = une zone semantique. Ne pas melanger les instructions dans un paragraphe monolithique.

**Croisement Askell :** Askell utilise aussi le XML dans les system prompts longs (30k+ mots). Pour nos skills (< 500 lignes), le markdown structure suffit. XML utile uniquement pour les prompts injectes dans des tools API.

### 2. Ordre des instructions (primacy/recency)

Claude donne plus de poids aux instructions au DEBUT et a la FIN du prompt.

**Application skills/agents :** Mettre les regles critiques (gotchas, interdits) en debut de SKILL.md ou en fin. Ne jamais enfouir une regle importante au milieu d'un workflow.

**Pattern forge :** Description YAML (debut) + Gotchas (fin) = les deux zones haute attention.

### 3. Negatifs absolus

"Ne fais JAMAIS X" est plus efficace que "Essaie d'eviter X".

**Application skills/agents :** Les gotchas doivent etre en negatif absolu. "Ne JAMAIS appeler obsidian directement" pas "Eviter d'appeler obsidian directement".

**Croisement Askell/Anthropic :** Anthropic nuance — les ALL-CAPS MUST/NEVER sans explication sont fragiles. Pattern recommande : negatif absolu + POURQUOI. "Ne JAMAIS appeler obsidian directement — sur Windows, ca resout vers le GUI au lieu de la CLI console."

### 4. Format de sortie obligatoire

Sans format explicite, Claude improvise.

**Application skills/agents :** Chaque skill qui genere un livrable doit inclure le schema exact de la sortie + un exemple concret. Voir backlog-triage (template de spec) et configure-claude-desktop (structure profil).

### 5. Exemples few-shot

1 exemple vaut 10 lignes d'instructions. 2 exemples fixent un pattern. 3 exemples ancrent un style.

**Application skills/agents :** Inclure 2-3 exemples entree/sortie dans les references/ des skills. Pour les profils Claude Desktop, inclure des exemples dans les prefs ("Si je demande X → tu fais Y").

**C'est la technique la plus impactante** selon Anthropic ET BellumAI. A utiliser systematiquement.

### 6. Controler la verbosite

Sans instruction de concision, Claude produit des reponses longues avec des formules de politesse inutiles.

**Application skills/agents :** Quantifier : "maximum 5 lignes", "budget 1 search + 2 reads". Ne pas dire "sois concis". Les anti-slop (pas de preambules, pas de disclaimers) vont dans les prefs/rules, pas dans chaque skill.

### 7. Gestion de la memoire conversationnelle

La performance de raisonnement des LLM se dégrade quand l'information critique est enfouie dans un long contexte — phénomène "Lost in the Middle" (Liu et al 2024, [arxiv 2307.03172](https://arxiv.org/abs/2307.03172)). Mesure faite en tokens/positions, **pas en tours conversationnels**. Voir [[Context Engineering]].

**Application skills/agents :** Pour les workflows longs, inclure un mecanisme de recap pour ramener les décisions critiques en début/fin de contexte (zones haute attention). Pattern : "Avant de continuer, recapitule les decisions prises jusqu'ici." Critique pour les agents longs (strategic-advisor, backlog-triage en mode lot).

> ⚠️ Correction 2026-05-23 : chiffre "15 échanges = oubli décisions" précédemment cité ici était **inventé** — Lost in the Middle parle de positions/tokens, pas de tours conversationnels.

### 8. Anti-hallucination explicite

Si le prompt ne dit pas "dis que tu ne sais pas", Claude remplit les trous avec des informations plausibles mais fausses.

**Application skills/agents :** Chaque skill qui consulte une source (vault, Jira) doit inclure : "Si le vault/Jira ne contient pas l'info, le dire clairement plutot qu'inventer."

### 9. Persona = role + anti-role

Un role clair canalise. Sans role, Claude reste generaliste. Definir ce que le persona EST et ce qu'il N'EST PAS.

**Application skills/agents :** La description YAML = le role. Les gotchas et restrictions = l'anti-role. Pour les prefs Claude Desktop : "Tu es mon bras droit, pas un assistant."

### 10. Hierarchie de priorites explicite

Deux regles contradictoires rendent le comportement imprevisible.

**Application skills/agents :** Quand une skill a plusieurs sources de verite (vault, Jira, code), definir l'ordre de priorite. Pattern : "Vault > Jira > memoire."

### 11. Chain of thought

Demander un raisonnement etape par etape ameliore la qualite sur les taches complexes.

**Application skills/agents :** Pour les skills de decision (strategic-advisor), inclure un workflow etape par etape. Pour les skills de recherche (neo-brain), le workflow token-smart joue ce role.

### 12. Contexte implicite inexistant

Claude n'a aucune connaissance de l'entreprise sauf si le prompt le precise.

**Application skills/agents :** Chaque skill metier doit soit inclure le contexte, soit indiquer ou le chercher (vault). C'est tout le pattern vault-first.

## Checklist de verification (avant livraison)

Adaptee de la checklist FORGE pour les livrables forge (skills, agents, prefs) :

- [ ] L'identite/role est claire (description YAML + premiere section)
- [ ] Les instructions sont numerotees et testables
- [ ] Le format de sortie a un schema ET un exemple (si applicable)
- [ ] Le bloc "si pas d'info, le dire" est present
- [ ] Les restrictions sont en negatif absolu + pourquoi
- [ ] La priorite entre sources est explicite
- [ ] Au moins 1-2 exemples sont inclus (dans le SKILL.md ou references/)
- [ ] Aucune instruction ne contredit une autre
- [ ] Les regles critiques sont en debut ou en fin
- [ ] Chaque ligne a une fonction (pas de remplissage)
- [ ] Le livrable fonctionnerait sans contexte de conversation

## Anti-patterns corriges (FORGE x forge)

| Anti-pattern | Correction FORGE | Correction forge |
|---|---|---|
| Role sans perimetre | Role + anti-role + limites | Description YAML = trigger + gotchas = limites |
| Pas de format de sortie | Schema strict + exemple | Template de sortie dans la skill |
| "Sois concis" | "Maximum N phrases" | Budget tokens quantifie |
| "Ne hallucine pas" | Bloc anti-hallucination | "Si le vault ne contient pas l'info, le dire" |
| Instructions en prose | Workflow numerote en imperatif | Etapes numerotees dans chaque skill |
| Aucun exemple | 2-3 few-shots realistes | Exemples dans references/ ou section dediee |
| Instructions enterrees | Reordonnancement par priorite | Gotchas en fin de SKILL.md (zone haute attention) |
| Prompt sans demarrage | Message d'initialisation | Description YAML = auto-trigger |

## Techniques avancees retenues

### Multi-perspective (pour strategic-advisor)

Analyser sous 2-3 roles differents puis synthetiser. Exemple : analyser une proposition technique du point de vue client, du point de vue dev, du point de vue business, puis arbitrer.

### Boucle de clarification (pour toutes les skills)

Si brief ambigu sur un point critique : proposer 2-3 interpretations, demander le choix. Pour les points secondaires : choisir l'interpretation la plus probable et preciser l'hypothese.

### Recherche contextuelle (pour strategic-advisor)

Inclure l'instruction de recherche web dans le prompt avec obligation de citer les sources. Ne pas se limiter au contexte interne.

## Quand utiliser

Reference lors de la creation ou review de prompts, skills, agents, ou instructions Claude Desktop. Les 12 principes servent de checklist qualite pour tout livrable textuel destine a un LLM.

## Ce qu'on ne retient PAS de FORGE

- **XML systematique** — nos skills markdown fonctionnent bien, XML serait du bruit
- **Zero emoji dans les prompts** — deja gere par nos rules/prefs, pas besoin de le repeter dans chaque skill
- **"Chaque reponse est un livrable"** — pertinent pour un generateur de prompts, pas pour un bras droit conversationnel
- **Variables {{NOM}}** — nos skills utilisent $ARGUMENTS, pas de variables balisees

## Liens

- [[MOC-Techniques]]
- [[amanda-askell-prompt-engineering]] — TDD for system prompts, reference Anthropic
- [[Context Engineering]] — Paradigme dominant 2026
- [[System Prompt Design]] — Structure optimale Amanda Askell
