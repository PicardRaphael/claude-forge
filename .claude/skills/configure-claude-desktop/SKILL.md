---
name: configure-claude-desktop
description: Generate Claude Desktop profile preferences and Cowork instructions for a Neoteem team member. Use when asked to configure Claude Desktop for someone, create a bras droit, or set up preferences for a new user.
---

# Configure Claude Desktop — Generateur de profil Neoteem

Genere les instructions optimales pour Claude Desktop (profil + Cowork) adaptees au role d'un membre Neoteem.

## Etape 1 — Collecter les informations

Poser ces questions a l'utilisateur (sauter celles dont la reponse est deja connue) :

| Question | Pourquoi |
|----------|----------|
| Qui est la personne ? (nom, poste) | Adapter le ton et le contexte |
| Quel est son role ? (dirigeant, PO, support, dev, commercial) | Determiner le niveau technique |
| Quelles questions pose-t-il a Claude ? (exemples concrets) | Calibrer les instructions |
| Niveau technique ? (non-tech, semi-tech, dev) | Router vers la bonne skill brain |
| Il utilise quoi ? (Claude Chat, Cowork, les deux) | Savoir quels champs remplir |
| Des preferences de ton connues ? (direct, pedagogique, formel) | Adapter la posture |
| Des anti-patterns ? (choses qu'il deteste dans les reponses IA) | Section negative instructions |

## Etape 2 — Choisir le routing skill

| Niveau technique | Skill par defaut | Skill si question technique |
|-----------------|------------------|---------------------------|
| Non-tech (support, dirigeant, commercial) | neoteem-brain-support | neoteem-brain-dev |
| Semi-tech (PO, chef de projet) | neoteem-brain-support | neoteem-brain-dev |
| Tech (dev, devops) | neoteem-brain-dev | neoteem-brain-dev-ia |

## Etape 3 — Generer les instructions

Consulter `references/best-practices.md` pour les principes, puis generer :

### Structure profil (Claude Chat)

```
1. Identite + contexte (1-2 lignes)
2. Framing : "bras droit" pas "assistant"
3. Routing vault-first (quelle skill par defaut, quelle skill si technique)
4. Posture (franchise, alternatives, risques explicites)
5. Anti-slop (ce qu'on ne veut PAS)
6. Memoire (retenir preferences, corrections, contexte projets)
7. Contexte equipe (si pertinent)
8. Timestamp
```

### Structure Cowork

```
1. Contexte (1 ligne)
2. Routing vault-first (meme pattern, plus directif)
3. Posture (1-2 lignes)
4. Preferences de sortie (3-4 bullets)
5. Timestamp
```

### Regles de generation

- < 500 mots par champ (tokens a chaque conversation)
- Expliquer POURQUOI derriere chaque regle, pas juste MUST/NEVER
- BLUF : instruire "reponse directe d'abord, raisonnement ensuite"
- Adapter le registre au public (pas de jargon dev pour un non-dev, mais ne pas brider si question technique)
- Toujours inclure : franchise totale + Auto Memory + timestamp
- Referencer les skills par nom (pas les outils MCP directement)

## Etape 4 — Output

Ecrire le fichier dans `output/claude-desktop-config-{role}.md` avec :
- Les 2 blocs de texte prets a copier-coller
- La checklist d'installation (plugins, MCP, Obsidian, test)

## Gotchas

- Claude Chat et Cowork n'ont PAS acces a Bash — les skills utilisent le fallback MCP automatiquement
- Les couches se cumulent : ne pas repeter les prefs profil dans Cowork
- Auto Memory doit etre active dans Settings > Features
- Obsidian doit etre ouvert sur le poste pour que les skills fonctionnent
- Un profil non-dev ne doit JAMAIS mentionner d'outils MCP par nom — les skills encapsulent ca

## Apprentissage

Quand tu configures un nouveau profil et que tu decouvres :
- Une preference qui marche particulierement bien → noter ici
- Un anti-pattern specifique a un role → noter ici
- Un probleme de routing skill → noter ici
