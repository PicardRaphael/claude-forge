---
titre: "Creation de composants sans interroger le vault"
resume: "Creer des notes vault, skills, agents sans consulter Knowledge/erreurs/ ni 04-Techniques/ produit des composants qui repetent des erreurs connues. Rules advisory ne suffisent pas — hook deterministe requis."
aliases:
  - "skip vault query"
  - "creation sans verification"
  - "advisory rules insuffisantes"
  - "vault pas consulte avant creation"
  - "composant sans brain check"
type: erreur
cree: 2026-05-06
derniere-maj: 2026-05-06
auteur: claude
repo: claude-forge
tags:
  - "#type/erreur"
  - "#domaine/claude-code"
---

# Creation de composants sans interroger le vault

## Ce qui s'est passe

Session du 6 mai 2026. Apres un scan cc-news, creation de 3 notes vault (agentic-engineering-karpathy, neoteem-agentic-engineering-mapping, pattern-agentic-engineering) sans aucune consultation prealable de :
- `Knowledge/erreurs/` — erreurs passees a eviter
- `04-Techniques/` — patterns existants
- `07-Prompts/` — prompts reutilisables
- Feedbacks memoire (`feedback_skill_*`, `feedback_major_mistakes`)

C'est la meme erreur que le 26 avril (erreur #7 et #8 dans feedback_major_mistakes) mais sur des notes vault au lieu de skills/agents.

## Pourquoi c'est une erreur

Les rules `check-before-create`, `forge-brain-proactive`, `memory-discipline` existent toutes. Elles sont lues en debut de session. Mais elles sont **advisory** (~80% compliance Boris). Sous pression conversationnelle ("la conversation coule, je sais quoi faire"), les rules sont skippees systematiquement.

Pattern de l'erreur : **fluency bias** — quand la tache semble evidente, le reflexe de verifier disparait. C'est exactement l'anti-pattern "Je sais deja" documente dans check-before-create.md.

## Pourquoi feedback_major_mistakes #8 n'a pas empeche la recurrence

L'erreur #8 disait : "Les rules advisory ne suffisent JAMAIS seules — doubler chaque regle critique d'un hook deterministe." Le hook `delegate-guard` a ete cree pour bloquer les edits directs sur skills/agents/CLAUDE.md.

Mais le scope etait trop etroit :
- delegate-guard bloque les **edits** sur skills/agents
- Rien ne bloque les **creations** (Write) dans vault/, output/
- Rien ne verifie que le vault a ete consulte AVANT de creer

## Fix applique

Deux hooks couples :

### vault-query-tracker.py (PostToolUse)
- Se declenche sur Read/Grep/Glob/Skill
- Detecte si la cible est dans vault/, memory/, Knowledge/, forge-brain
- Ecrit un fichier marqueur `.claude/.session-vault-queried` avec timestamp

### vault-query-guard.py (PreToolUse)
- Se declenche sur Write
- Si la cible est dans vault/, output/, .claude/skills/, .claude/agents/
- Verifie que le marqueur existe et a moins de 60 minutes
- Pas de marqueur → exit 2 BLOQUE
- Bypass : CLAUDE_AGENT = specialist (skill-creator, agent-creator, hook-creator, claudemd-optimizer, project-analyzer, project-auditor)

### Pourquoi 60 minutes et pas par-fichier
- Dans une meme conversation, le contexte lu reste en memoire
- Le probleme c'est "jamais consulte" pas "pas re-consulte pour chaque fichier"
- 60 min couvre une session typique. Au-dela, auto-compact a probablement perdu le contexte lu

## Lecon

1. Chaque rule critique DOIT etre doublee d'un hook. Pas "devrait" — DOIT.
2. Le scope du hook doit couvrir TOUS les chemins proteges, pas juste ceux qui ont cause le dernier incident.
3. Le fluency bias est le pire ennemi des rules advisory. Plus on "sait", plus on skip.
4. Un hook qui ecrit un marqueur + un guard qui le verifie = pattern reutilisable pour toute verification prealable.

## Pattern reutilisable

```
PostToolUse (tracker) : detecte action prerequis → ecrit marqueur
PreToolUse (guard) : detecte action protegee → verifie marqueur → bloque si absent
```

Applicable a tout workflow "verifie X avant de faire Y".

## Liens

- [[erreur-edit-direct-skills]] — meme famille, scope plus etroit
- [[pattern-agentic-engineering]] — le pattern qui a ete cree sans verification
- [[agentic-engineering-karpathy]] — la note qui a ete creee sans verification
