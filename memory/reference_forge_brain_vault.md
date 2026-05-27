---
name: forge-brain-vault
description: Vault Obsidian forge-brain — knowledge base persistante pour tout ce que j'apprends (CC, concurrents, modèles, techniques, leaders, industrie). Skill forge-brain + rule proactive.
type: reference
originSessionId: 65cf98c5-1e62-497b-a9f3-568b895cf577
---
## Forge Brain Vault

**Path** : `C:/Users/raphael.picard_neote/Documents/claude-forge/vault/claude-forge/`

## Structure

```
00-Hub/           — Home + 6 MOCs (index par thème)
01-Claude-Code/   — features/, changelog/, best-practices/, hooks/, skills/, agents/
02-Concurrents/   — gemini-cli/, codex/, copilot/, cursor/, xai/
03-Modeles/       — claude/, gpt/, gemini/, grok/
04-Techniques/    — prompt-engineering/, context-engineering/, patterns/
05-Leaders/       — Fiches personnes clés
06-Industrie/     — Market, funding, événements, tendances
07-Prompts/       — system-prompts/, agent-prompts/, skill-prompts/, templates-prompts/
Knowledge/        — explorations/, syntheses/, erreurs/
Templates/        — 11 templates (feature, changelog, best-practice, leader, technique, modele, concurrent, deprecation, knowledge, prompt, erreur)
```

## Accès

- **Skill** : `forge-brain` — search, read, write via obsidian-cli ou fallback Read/Write
- **Rule** : `.claude/rules/forge-brain-proactive.md` — query proactif à chaque session
- **Wrapper** : `.claude/skills/forge-brain/scripts/obsidian-cli.sh`

## Quand utiliser

1. **Début de session** : query les notes récentes pour rappeler le contexte
2. **Avant de CRÉER** skill/agent/hook/prompt : chercher best practices, erreurs passées, prompts réutilisables
3. **Analyse de repo/projet** : chercher patterns, concurrents, techniques pertinentes
4. **Avant de répondre** sur features/outils/modèles : chercher dans le vault d'abord
5. **Après cc-news** : capitaliser les découvertes en notes atomiques
6. **Après une erreur** : documenter dans `Knowledge/erreurs/`
7. **Nouvelle info apprise** : créer une note atomique

## Conventions

- 1 concept = 1 note atomique
- Frontmatter YAML obligatoire (titre, resume, aliases, domaine, type, derniere-maj, auteur, sources, tags)
- Wikilinks pour tout cross-référencement
- Tags `#type/` + `#domaine/`
- MAJ du MOC correspondant à chaque nouvelle note

## Why

La mémoire fichier (.claude/memory/) se compresse et se perd entre sessions. Le vault Obsidian est persistant, searchable, cross-linké, et consultable proactivement. Pattern validé par neoteem-brain (774 notes).

## How to apply

- Forge Brain = priority 1 dans la hiérarchie des sources (avant mémoire fichier)
- Les gros fichiers reference_* de la mémoire sont migrés en notes atomiques dans le vault
- La mémoire fichier reste pour : feedback, projets en cours, context conversationnel
