---
name: cc-news
description: Use this skill when the user asks about recent Claude Code updates, new features, AI industry news, or when any information might be outdated. Use PROACTIVELY when the user asks "quoi de neuf", "est-ce que X existe maintenant", or when knowledge seems stale. Date de référence : 8 mai 2026 (v2.1.129).
user-invokable: true
allowed-tools: WebSearch, WebFetch, Read, Write
argument-hint: "fonctionnalité ou sujet à vérifier"
---

# Vérificateur de Nouveautés Claude Code

Date de référence du studio : **8 mai 2026** (v2.1.129)
Tout ce qui est postérieur à cette date doit être recherché.

## Sources à consulter

### Officielles
1. `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. `https://docs.anthropic.com/en/release-notes/claude-code`
3. `https://code.claude.com/docs/en/changelog`

### Équipe Claude Code (OBLIGATOIRE — vérifier chaque personne)
4. **Boris Cherny** (@bcherny) — créateur de Claude Code
   - `https://howborisusesclaudecode.com`
   - threads.com/@boris_cherny
   - x.com/bcherny
5. **Cat Wu** (@_catwu) — Head of Product Claude Code
   - x.com/_catwu
6. **Lydia Hallie** (@lydiahallie) — Claude Code team
   - x.com/lydiahallie
7. **Noah Zweben** (@noahzweben) — Claude Code team
   - x.com/noahzweben
8. **Thariq Shihipar** (@trq212) — Skills author, Claude Code team
   - x.com/trq212
   - linkedin.com/in/thariq
9. **Jarred Sumner** (@jaraboron) — Bun creator, acquis par Anthropic
   - x.com/jaraboron
10. **Felix Rieseberg** (@felixrieseberg) — Claude Code contributor
   - x.com/felixrieseberg

### Écosystème & frameworks (OBLIGATOIRE)
11. **LangChain** (@LangChainAI) — Framework agents/RAG
   - x.com/LangChainAI
12. **Claude officiel** (@AnthropicAI) — Compte officiel Anthropic
   - x.com/AnthropicAI
13. **Google AI Studio** (@GoogleAIStudio) — Gemini platform
   - x.com/GoogleAIStudio

## Recherches à effectuer

### Claude Code (obligatoire)
```
Chercher : Claude Code changelog site:github.com/anthropics/claude-code
Chercher : Claude Code $ARGUMENTS 2026
Chercher : @bcherny Claude Code 2026
Chercher : @_catwu Claude Code 2026
Chercher : @lydiahallie Claude Code 2026
Chercher : @noahzweben Claude Code 2026
Chercher : thariq shihipar claude code skills 2026
Chercher : jarred sumner anthropic claude code 2026
Chercher : @felixrieseberg Claude Code 2026
Chercher : Claude Code deprecated OR breaking 2026
Chercher : Claude Cowork update 2026
Chercher : Claude Dispatch new features 2026
Chercher : anthropic Agent Teams claude code 2026
```

### Plugins officiels Anthropic (obligatoire)
```
Vérifier version du plugin claude-code-setup :
  Read("~/.claude/plugins/cache/claude-plugins-official/claude-code-setup/*/. claude-plugin/plugin.json")
Si version > 1.0.0 → lire les changements et mettre à jour cc-advisor/references/mcp-catalog.md
Chercher : site:github.com/anthropics claude-code-setup plugin update 2026
```

### Écosystème & frameworks (obligatoire)
```
Chercher : @LangChainAI LangChain LangGraph new features 2026
Chercher : @AnthropicAI Claude announcements 2026
Chercher : @GoogleAIStudio Gemini updates 2026
Chercher : @felixrieseberg Claude Code 2026
```

### Prompt engineering & techniques
```
Chercher : @AmandaAskell prompt engineering Claude 2026
Chercher : @alexalbert__ Claude prompt techniques 2026
Chercher : @emollick prompt engineering 2026
Chercher : "context engineering" OR "adaptive thinking" Claude 2026
Chercher : Gemini prompt engineering new techniques 2026
```

### Industrie IA — Concurrents & leaders
```
Chercher : Google Gemini Code Assist OR Gemini CLI new features 2026
Chercher : OpenAI Codex CLI OR ChatGPT code new features 2026
Chercher : GitHub Copilot new features 2026
Chercher : Cursor AI new features 2026
Chercher : Andrej Karpathy AI coding tools 2026
Chercher : Yann LeCun AI agents 2026
Chercher : Sam Altman OpenAI announcements 2026
Chercher : Elon Musk xAI Grok coding 2026
```

## Étapes

1. **Chercher dans le vault forge-brain** d'abord — vérifier ce qui est déjà connu (`derniere-maj` des notes)
2. Rechercher TOUTES les sources ci-dessus (officielles + équipe)
3. Identifier ce qui est postérieur à la date de référence
4. Comparer avec les notes existantes du vault (pas juste cc-features-ref)
5. Vérifier les dépréciations et breaking changes
6. Résumer les nouveautés à l'utilisateur
7. **Capitaliser dans le vault forge-brain** :
   - Créer des notes atomiques pour chaque nouveauté significative (1 concept = 1 note)
   - Mettre à jour les notes existantes si l'info a évolué
   - Mettre à jour les MOCs correspondants (ajouter les wikilinks des nouvelles notes)
   - Mettre à jour `derniere-maj` sur chaque note touchée
8. Mettre à jour la mémoire si découvertes importantes (fichiers reference_*)

## Format de réponse

```markdown
## [Date] — Mise à jour cc-news

### Officiel (changelog)
- [version] : [features]

### Équipe Claude Code
- **Boris** : [tips/annonces]
- **Cat** : [insights produit]
- **Lydia** : [features/workshops]
- **Noah** : [features cloud/mobile]
- **Thariq** : [skills patterns]
- **Jarred** : [performance/runtime]

### Dépréciations
- [feature] → [remplacement]

### Industrie IA
- **Google/Gemini** : [updates Gemini Code, CLI]
- **OpenAI** : [updates Codex, ChatGPT code, Sam Altman]
- **GitHub Copilot** : [updates]
- **Cursor** : [updates]
- **xAI/Grok** : [updates Elon Musk]

### Leaders & visionnaires
- **Karpathy** : [AI coding, Obsidian, techniques]
- **Yann LeCun** : [vision AI, debats]
- **Sam Altman** : [annonces OpenAI]
- **Elon Musk** : [xAI, Grok]

### Prompt engineering & communauté
- **Amanda Askell** : [prompt techniques Claude]
- **Alex Albert** : [prompt techniques]
- **Ethan Mollick** : [observations]
- [autres observations notables]

Sources : [URLs]
```

- Indiquer la date de la recherche
- Distinguer "officiel" vs "equipe" vs "industrie" vs "communaute"
- Si rien de nouveau dans une section → l'omettre
- Si rien de nouveau du tout → dire que le studio est à jour

## Forge Brain — Capitalisation (OBLIGATOIRE)

Après chaque scan cc-news, capitaliser dans le vault `vault/claude-forge/` :

1. **Chercher d'abord** ce qui existe déjà dans le vault (éviter doublons)
2. **Créer des notes atomiques** pour chaque nouveauté significative :
   - Nouvelle version CC → `01-Claude-Code/changelog/CC vX.Y.Z.md`
   - Nouveau modèle/update → `03-Modeles/<provider>/<nom>.md`
   - Nouvelle feature concurrent → mettre à jour la fiche dans `02-Concurrents/`
   - Nouvelle technique/pattern → `04-Techniques/<sous-dossier>/`
   - Nouveau prompt/system prompt → `07-Prompts/<sous-dossier>/`
   - Info leader → mettre à jour la fiche dans `05-Leaders/`
   - Info industrie → `06-Industrie/`
3. **Mettre à jour les MOCs** — ajouter les wikilinks des nouvelles notes
4. **Mettre à jour `derniere-maj`** sur chaque note touchée
5. **Utiliser les templates** de `Templates/` pour chaque nouveau type de note
