---
name: cc-news
description: Use this skill when the user asks about recent Claude Code updates, new features, AI industry news, or when any information might be outdated. Use PROACTIVELY when the user asks "quoi de neuf", "est-ce que X existe maintenant", or when knowledge seems stale. Date de référence : 9 avril 2026.
user-invokable: true
allowed-tools: WebSearch, WebFetch, Read, Write
argument-hint: "fonctionnalité ou sujet à vérifier"
---

# Vérificateur de Nouveautés Claude Code

Date de référence du studio : **9 avril 2026** (v2.1.97)
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
Chercher : Claude Code deprecated OR breaking 2026
Chercher : Claude Cowork update 2026
Chercher : Claude Dispatch new features 2026
Chercher : anthropic Agent Teams claude code 2026
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

1. Rechercher TOUTES les sources ci-dessus (officielles + équipe)
2. Identifier ce qui est postérieur à la date de référence
3. Comparer avec les features déjà connues (cc-features-ref + mémoire)
4. Vérifier les dépréciations et breaking changes
5. Résumer les nouveautés à l'utilisateur
6. Mettre à jour la mémoire si découvertes importantes

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
