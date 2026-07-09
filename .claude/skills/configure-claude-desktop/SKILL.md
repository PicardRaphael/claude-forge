---
name: configure-claude-desktop
description: ALWAYS invoke when configuring Claude Desktop or Cowork for a Neoteem team member — 'bras droit' profile, onboarding, member preferences. NOT for generic Claude Desktop questions outside Neoteem.
model: sonnet
effort: high
user-invocable: true
allowed-tools: Read, Write, Edit
---

# Configure Claude Desktop — Générateur de profil Neoteem

Génère les instructions optimales pour Claude Desktop (profil + Cowork) adaptées au rôle d'un membre Neoteem.

## Étape 1 — Collecter les informations

Poser ces questions à l'utilisateur (sauter celles dont la réponse est déjà connue) :

| Question | Pourquoi |
|----------|----------|
| Qui est la personne ? (nom, poste) | Adapter le ton et le contexte |
| Quel est son rôle ? (dirigeant, PO, support, dev, commercial) | Déterminer le niveau technique |
| Quelles questions pose-t-il à Claude ? (exemples concrets) | Calibrer les instructions |
| Niveau technique ? (non-tech, semi-tech, dev) | Router vers la bonne skill brain |
| Il utilise quoi ? (Claude Chat, Cowork, les deux) | Savoir quels champs remplir |
| Des préférences de ton connues ? (direct, pédagogique, formel) | Adapter la posture |
| Des anti-patterns ? (choses qu'il déteste dans les réponses IA) | Section negative instructions |

## Étape 2 — Choisir le routing skill

| Niveau technique | Skill par défaut | Skill si question technique |
|-----------------|------------------|---------------------------|
| Non-tech (support, dirigeant, commercial) | neoteem-brain-support | neoteem-brain-dev |
| Semi-tech (PO, chef de projet) | neoteem-brain-support | neoteem-brain-dev |
| Tech (dev, devops) | neoteem-brain-dev | neoteem-brain-dev-ia |

## Étape 3 — Générer les instructions

Consulter `references/best-practices.md` pour les principes, puis générer :

### Structure profil (Claude Chat)

```
1. Identité + contexte (1-2 lignes)
2. Framing : "bras droit" pas "assistant"
3. Routing vault-first (quelle skill par défaut, quelle skill si technique)
4. Posture (franchise, alternatives, risques explicites)
5. Anti-slop (ce qu'on ne veut PAS)
6. Mémoire (retenir préférences, corrections, contexte projets)
7. Contexte équipe (si pertinent)
8. Timestamp
```

### Structure Cowork

```
1. Contexte (1 ligne)
2. Routing vault-first (même pattern, plus directif)
3. Posture (1-2 lignes)
4. Préférences de sortie (3-4 bullets)
5. Timestamp
```

### Règles de génération

- < 500 mots par champ (tokens à chaque conversation)
- Expliquer POURQUOI derrière chaque règle, pas juste MUST/NEVER
- BLUF : instruire "réponse directe d'abord, raisonnement ensuite"
- Adapter le registre au public (pas de jargon dev pour un non-dev, mais ne pas brider si question technique)
- Toujours inclure : franchise totale + Auto Memory + timestamp
- Référencer les skills par nom (pas les outils MCP directement)

## Étape 4 — Output

Écrire le fichier dans `output/claude-desktop-config-{role}.md` avec :
- Les 2 blocs de texte prêts à copier-coller
- La checklist d'installation (plugins, MCP, Obsidian, test)

## Gotchas

- Claude Chat et Cowork n'ont PAS accès à Bash — les skills utilisent le fallback MCP automatiquement
- Les couches se cumulent : ne pas répéter les prefs profil dans Cowork
- Auto Memory doit être activée dans Settings > Features
- Obsidian doit être ouvert sur le poste pour que les skills fonctionnent
- Un profil non-dev ne doit JAMAIS mentionner d'outils MCP par nom — les skills encapsulent ça

## Apprentissage

Quand tu configures un nouveau profil et que tu découvres :
- Une préférence qui marche particulièrement bien → noter ici
- Un anti-pattern spécifique à un rôle → noter ici
- Un problème de routing skill → noter ici
