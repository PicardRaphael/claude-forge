---
titre: "Configuration des preferences Claude Desktop"
resume: "Guide pour configurer profil, projet et Cowork dans Claude Desktop, avec pattern vault-first MCP"
aliases:
  - "preferences Claude Desktop"
  - "custom instructions Claude"
  - "profil Claude Chat"
  - "instructions Cowork"
  - "claude desktop config"
  - "vault-first pattern desktop"
domaine: claude-code
type: feature
derniere-maj: 2026-05-10
auteur: claude
sources:
  - "https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features"
  - "https://www.jdhodges.com/blog/claude-ai-custom-instructions-a-real-example-that-actually-works/"
  - "https://promptoptimizer.tools/blog/how-to-set-up-claude-profile-preferences"
  - "[[amanda-askell-prompt-engineering]] — TDD for system prompts (X, dec 2024)"
  - "[[Alex Albert]] — Personal preferences announcement (X, dec 2024)"
  - "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
tags:
  - "#type/feature"
  - "#domaine/claude-code"
  - "#pattern/vault-first"
---

## Description

Claude Desktop a 3 couches de personnalisation qui se cumulent (stacking) :

| Couche | Portee | Ou configurer |
|--------|--------|--------------|
| **Profil** (preferences personnelles) | Toutes les conversations Claude Chat | Settings > Profil |
| **Projet** (project instructions) | Conversations dans un projet specifique | Settings du projet |
| **Style** (custom style) | Formatage/ton seulement | Settings > Styles |

En plus, **Cowork** a son propre champ d'instructions globales (Settings > Cowork) qui s'applique a toutes les sessions Cowork.

Les couches se cumulent : pas besoin de repeter les prefs profil dans le projet ou Cowork.

## Format recommande

- **< 500 mots** — charge en tokens a chaque conversation
- **Bullet points ou paragraphes courts** — pas de structure elaborate
- Penser "briefing jour 1 pour un assistant"
- Sections utiles : role/contexte, regles comportementales, anti-patterns (ce qu'on ne veut PAS)

## Interaction avec MCP

On ne peut pas "declarer" un MCP dans les preferences — les MCP sont configures via `claude_desktop_config.json` (ou Desktop Extensions) et decouverts automatiquement.

**Mais on peut ecrire des regles comportementales qui les utilisent.** C'est le pattern cle :

```
Si ma question porte sur le metier Neoteem : chercher d'abord dans le vault 
neoteem-brain via les outils MCP (search_brain, read_note) avant de repondre.
```

Claude verra les outils MCP disponibles ET l'instruction de les utiliser = il les appelera.

## Pattern vault-first (pour utilisateurs non-dev)

Le pattern "vault-first" force Claude a consulter le vault AVANT de repondre de memoire. Essentiel pour les utilisateurs non-dev qui n'ont pas le reflexe de dire "cherche dans le brain".

### Dans le profil (Claude Chat)

```
Si ma question porte sur [domaine], chercher d'abord dans le vault via les 
outils MCP (search_brain, read_note) avant de repondre de memoire. Le vault 
contient la documentation a jour. Si le vault ne contient pas l'info, le 
dire clairement plutot qu'inventer.
```

### Dans les instructions Cowork

```
Quand la tache touche a [domaine], TOUJOURS consulter le vault via les 
outils MCP avant de proposer quoi que ce soit :
1. search_brain(query="...", limit=5, context=true) pour chercher
2. read_note(file="...") pour lire une note trouvee
Le vault est la source de verite. Ne jamais repondre de memoire sur un 
sujet couvert par le vault.
```

### Cle : nommer les outils MCP explicitement

Dire "utilise le vault" ne suffit pas. Nommer les tools MCP (`search_brain`, `read_note`, `get_backlinks`) donne a Claude le signal concret de quel outil appeler.

## Best practices experts (Amanda Askell, Alex Albert, Anthropic)

### TDD pour prompts (Amanda Askell)

Ne pas ecrire les instructions puis chercher a les tester. Faire l'inverse :
1. Lister les situations ou Claude repond mal par defaut (tests)
2. Ecrire les instructions qui corrigent ces echecs
3. Iterer jusqu'a ce que tous les tests passent

Apres redaction, relire les instructions comme si on les voyait pour la premiere fois. Si une regle n'est pas claire sans contexte, la reformuler.

### BLUF — Bottom Line Up Front

Instruire Claude a donner la reponse directe d'abord, le raisonnement ensuite. Elimine le "laissez-moi reflechir..." qui fait perdre du temps. Pattern : "Reponse directe d'abord, raisonnement ensuite (pas l'inverse)".

### Expert Partner framing

Cadrer Claude comme un "bras droit" ou "partenaire expert", pas un assistant. Impact :
- Doit toujours proposer au moins une alternative non envisagee
- Rendre les risques/limites/compromis explicites
- Finir avec un plan d'action concret

### Anti-slop (Anthropic docs)

Eliminer les patterns IA generiques :
- Pas de preambules ("Bien sur !", "Excellente question !")
- Pas de disclaimers ("en tant qu'IA...")
- Pas de recap de la question avant de repondre
- Prose claire, pas de bullet points systematiques sauf si les items sont vraiment discrets

### Explain WHY, pas MUST/NEVER

Eviter les ALL-CAPS MUST/NEVER/ALWAYS sans explication. Pattern recommande :
- Enoncer la regle
- Expliquer POURQUOI (la raison derriere)
- Claude generalise mieux aux cas non prevus quand il comprend le pourquoi

### Timestamp

Ajouter "Derniere mise a jour : [date]" en fin d'instructions. Donne a Claude un contexte temporel et la permission de signaler si une info semble datee.

### Auto Memory

Claude Desktop a une memoire automatique (Settings > Features). L'activer ET le mentionner dans les preferences :
```
Retiens mes preferences, decisions, et le contexte de mes projets en cours.
Si je te corrige, retiens-le pour ne pas refaire la meme erreur.
```
La memoire se construit au fil des conversations = Claude devient plus pertinent avec le temps.

### Routing par skill (pattern Neoteem)

Plutot que de nommer les outils MCP, referencer les skills qui encapsulent la logique de detection CLI/MCP :
```
Question metier → skill neoteem-brain-support
Question technique → skill neoteem-brain-dev
```
Les skills gerent le mode d'acces (CLI ou MCP) automatiquement.

## Anti-patterns a eviter dans les preferences

- Trop long (> 500 mots) — gaspille du contexte a chaque conversation
- Trop vague ("sois utile") — pas d'impact
- Repeter ce qui est dans le projet — les couches se cumulent
- Adapter au public — pas de code/SQL pour un non-dev, mais ne pas brider si la question est technique
- ALL-CAPS MUST/NEVER sans expliquer pourquoi — Claude suit la lettre mais rate les cas limites
- Instructions contradictoires — "sois bref" en prefs + "sois exhaustif" en prompt = Claude perd du compute a reconcilier
- Ne jamais mettre a jour — revoir toutes les 4-6 semaines, corriger immediatement si un pattern se repete

## Quand utiliser

- Onboarding d'un nouveau utilisateur Claude Desktop chez Neoteem
- Configuration du profil d'un dirigeant/PO/support qui utilise Claude Chat + Cowork
- Deploiement du plugin neoteem-brain sur un nouveau poste

## Liens

- [[MOC-Claude-Code]]
- [[neoteem-brain-plugins]]
- [[Claude Desktop]]
- [[Cowork]]
- [[amanda-askell-prompt-engineering]]
