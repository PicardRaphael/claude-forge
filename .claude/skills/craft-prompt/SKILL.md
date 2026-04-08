---
name: craft-prompt
description: Use when the user asks to create, write, improve, or optimize a prompt for Claude, Gemini, or any LLM. Applies best techniques automatically based on target model and use case.
user-invokable: true
allowed-tools: Read, WebSearch
argument-hint: "description du prompt a creer (+ modele cible si pas Claude)"
model: opus
effort: high
---

# Craft Prompt — Generateur de prompts optimises

Cree des prompts optimises pour Claude, Gemini, ou tout LLM en appliquant les meilleures techniques automatiquement.

## Workflow

### 1. Comprendre le besoin

Poser ces questions si pas deja clair :
- **Objectif** : que doit faire le prompt ? (generer, analyser, transformer, decider)
- **Modele cible** : Claude (defaut), Gemini, GPT, ou generique ?
- **Contexte** : agent, skill, Cowork, API, chat ?
- **Input/Output** : quel format en entree ? quel format en sortie ?
- **Contraintes** : langue, longueur, ton, domaine ?

### 2. Selectionner les techniques

Consulter `references/techniques-claude.md` et `references/techniques-gemini.md` pour choisir les techniques adaptees au cas d'usage.

### 3. Construire le prompt

Appliquer la structure adaptee au modele cible (voir section structures ci-dessous).

### 4. Livrer

Presenter le prompt avec :
- Le prompt complet pret a copier
- Les techniques appliquees (et pourquoi)
- Des variantes si pertinent (court/long, strict/flexible)

## Structures par modele

### Claude — Structure recommandee

```xml
<system>
[Role + contexte + contraintes]
</system>

<instructions>
[Etapes numerotees, claires, specifiques]
</instructions>

<examples>
<example>
<input>[Exemple d'entree]</input>
<output>[Exemple de sortie attendue]</output>
</example>
</examples>

<constraints>
[Regles a respecter imperativement]
</constraints>
```

**Points cles Claude :**
- XML tags pour structurer (Claude les comprend nativement)
- Role clair en debut de system prompt
- Exemples concrets (few-shot) pour le format attendu
- Contraintes explicites en fin de prompt
- Prefill de la reponse pour forcer le format

### Gemini — Structure recommandee

```
System instruction:
[Role + contexte + regles globales]

Prompt:
[Tache + contexte specifique]

Format attendu :
[Schema JSON ou description du format]
```

**Points cles Gemini :**
- System instructions separees du prompt (champ dedie dans l'API)
- Grounding avec Google Search pour les faits recents
- JSON mode natif (responseSchema dans l'API)
- Pas de XML tags — utiliser markdown ou JSON
- Code execution integre (Gemini peut executer du code)

### Generique (tout LLM)

```markdown
# Role
[Qui es-tu]

# Contexte
[Ce que tu dois savoir]

# Tache
[Ce que tu dois faire, etape par etape]

# Format
[Comment structurer la reponse]

# Exemples
[1-3 exemples input/output]

# Contraintes
[Ce qu'il ne faut PAS faire]
```

## Techniques disponibles

Voir les fichiers de reference pour la liste complete :
- `references/techniques-claude.md` — techniques Claude-specifiques
- `references/techniques-gemini.md` — techniques Gemini-specifiques
- `references/techniques-universelles.md` — techniques pour tout LLM

## Cas d'usage courants

| Cas | Techniques a appliquer |
|-----|----------------------|
| Agent Claude Code | Role + XML tags + contraintes + progressive disclosure |
| Skill Claude Code | Description trigger + Gotchas + exemples |
| Prompt Cowork | Tache specifique + format attendu + verification |
| Prompt API (batch) | System prompt + few-shot + structured output + prefill |
| Prompt Gemini API | System instruction + JSON schema + grounding |
| Prompt creatif | Role immersif + temperature elevee + exemples de ton |
| Prompt analytique | Chain-of-thought + verification + structured output |
| Prompt extraction | Few-shot + schema strict + contraintes negatives |

## Regles

- **Modele par defaut = Claude** — sauf si l'utilisateur precise un autre modele
- **Toujours inclure des exemples** — meme 1 seul exemple ameliore drastiquement la qualite
- **Contraintes negatives** — dire ce qu'il ne faut PAS faire est aussi important que ce qu'il faut faire
- **Tester mentalement** — avant de livrer, simuler le prompt dans ta tete : est-ce qu'un humain comprendrait ?
- **Pas de jargon prompt** — le prompt final doit etre lisible par quelqu'un qui ne connait pas le prompt engineering

## Apprentissage

Quand tu crees un prompt et que tu decouvres :
- Une technique qui marche particulierement bien → noter ici
- Une structure qui echoue systematiquement → noter ici
- Une difference de comportement entre modeles → noter ici
