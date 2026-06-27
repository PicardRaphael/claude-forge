---
titre: "Méthode — choisir et construire la bonne capability pour résoudre un besoin"
resume: "Méthode transverse : arbre de décision besoin → Skill / Workflow / Agent / Framework / Hook / MCP, + 4 patterns de robustesse (validateur embarqué, template-par-étape, draft→approved, pureté contexte), 3 archétypes. Principes stack-agnostiques ; colonne 'créer via' = instanciation forge/Claude Code."
aliases:
  - "méthode monter système workflow"
  - "choisir capability"
  - "skill workflow agent framework"
  - "capabilities Eliott Meunier"
  - "validateur embarqué workflow"
  - "besoin vers capability dispatch"
type: technique
domaine: patterns
status: active
derniere-maj: 2026-06-27
auteur: claude
tags:
  - "#type/technique"
  - "#domaine/patterns"
  - "#domaine/claude-code"
  - "#domaine/agents"
sources:
  - "https://www.youtube.com/watch?v=5WiuP81OVJo (podcast agence/bootcamp IA — Eliott Meunier & associés)"
  - "memory/reference_eliott_meunier_prisme.md"
---

## Quand utiliser cette note

Déclencheur : **« je veux créer quelque chose pour résoudre un problème / automatiser X »**, mais sans savoir quelle brique construire. Cette note est la grille de dispatch : face à un besoin, elle dit **quelle capability** monter, **avec quels patterns de robustesse**, et **comment la créer**. Sœur de [[methode-analyser-repo]] (qui, elle, audite un repo existant).

**Portée — transverse, pas seulement Claude Code.** Le cœur de la méthode (l'arbre de décision, les 4 patterns de robustesse, les archétypes, les frameworks conceptuels) est **stack-agnostique** : il vaut pour n'importe quel système agentique (Claude Code, SDK, OpenCode…) et même hors-code (process humain + IA). Seule la colonne **« créer via »** ci-dessous est l'**instanciation forge/Claude Code** — transposable à un autre harness.

Origine : extraction d'un podcast d'une agence IA (Eliott Meunier & associés). Leur système tourne intégralement sur Claude Code + Obsidian + MCP. Valeur de la note = formaliser leur taxonomie « capabilities » et leurs 2-3 idées non encore systématisées chez nous.

## Les briques (capability) — vocabulaire eux ↔ brique ↔ créer via (forge/CC)

| Capability (leur terme) | Définition | Brique (générique) | Créer via (forge/Claude Code) |
|---|---|---|---|
| **Skill** | 1 livrable, 1 transformation, 3-10 étapes, 1 template de sortie | unité de transformation | `.claude/skills/<nom>/SKILL.md` — [[comment-creer-skill]] |
| **Workflow** | Orchestre des skills dans un ordre + insère des validations | orchestrateur | rule · métaskill · outil `Workflow` — [[workflow-claude-code-optimal]] |
| **Agent** | Comportement récurrent, output **variable** (≠ skill figée) | acteur autonome | `.claude/agents/<nom>.md` — [[comment-creer-agent]] |
| **Framework** | Modèle mental réutilisé, appelé par skills/agents | modèle mental | rule `.claude/rules/` ou note vault — [[comment-ecrire-claudemd]] |
| **Hook** (ajout forge) | Garde déterministe lint / sécu / scope | garde déterministe | `.claude/hooks/*.py` — [[comment-creer-hook]] |
| **MCP** (donnée/outil) | Connexion à une source ou un outil externe | connecteur | `.mcp.json` → `mcp__<serveur>__<outil>` — [[mcp-vs-skills-doctrine]] |

## Arbre de décision — besoin → capability

```
Le besoin est-il UNE transformation, sortie précise et figée ?
   └─ OUI → SKILL (3-10 étapes, 1 template de sortie)
   └─ NON ↓
Faut-il ENCHAÎNER plusieurs skills, avec contrôle qualité entre étapes ?
   └─ OUI → WORKFLOW (+ 1 VALIDATEUR par étape risquée)
   └─ NON ↓
Veux-tu un COMPORTEMENT récurrent à output variable selon le cas ?
   └─ OUI → AGENT (instruction, output non figé)
   └─ NON ↓
Est-ce un MODÈLE MENTAL réutilisé par d'autres composants ?
   └─ OUI → FRAMEWORK (rule/note appelée par wikilink)
   └─ NON ↓
Faut-il GARANTIR mécaniquement une règle (lint/sécu/scope) ?
   └─ OUI → HOOK   |   Besoin de DONNÉE/OUTIL externe ? → MCP
```

Un système complet = **1 dossier** regroupant ses skills + son workflow + ses agents (dont les validateurs) + ses frameworks + ses MCP. C'est la structure d'un domaine `.claude/`.

## Les 4 patterns de robustesse (à voler de la vidéo)

1. **Validateur embarqué** (Sierra-style) — entre deux étapes risquées d'un workflow, un sous-agent juge **PASS/FAIL** l'output contre le template attendu, AVANT de passer à la suite. Évite la **dérive cumulative** (chaque étape construit sur l'erreur de la précédente). Forge a les briques (`outcomes-grader`, `devils-advocate`) mais les appelle surtout **en fin** de chaîne — le delta = les insérer **entre** les étapes.
   - ⚠️ Le validateur est un **sous-agent / étape de pipeline**, **JAMAIS un hook**. Un hook qui force un workflow agentique = anti-pattern (cf [[erreur-hooks-workflow-enforcement]], doctrine 22 mai). La validation vit dans le Workflow/la rule d'orchestration, pas dans `hooks/`.
2. **Template par étape** — la consistance du rendu vient du gabarit fourni à chaque sortie (section « Template de sortie » du SKILL.md), pas du modèle.
3. **Provenance draft → approved** — note générée par IA taggée `draft-IA` ; relue → `approved`. Méta-règle : l'IA **ne source jamais un draft**. + jauge **%draftia** comme métrique de santé (« à 50 %, le système dérive »). Forge a `status` en frontmatter mais pas la garde « interdit de sourcer un draft » ni la jauge.
4. **Pureté du contexte** — les bruts (transcripts d'appel) sont des **variables de transformation**, pas des notes stockées. On ne garde pas un résumé formulé par l'IA si rien n'en découle.

## Les 3 archétypes (choisir « suivant le besoin »)

Le style cognitif détermine la forme du système — ne pas copier, se situer.

- **Architecte / production templatisée** — structure d'abord. Dossiers `capabilities/`, validateurs, draft→approved, peu de thinking partner.
- **Penseur / thinking partner** — clarifie *avec* l'IA, veut être challengé. Skill de déconstruction maïeutique (livre/podcast → notes-concepts), frameworks anti-complaisance dans les prompts.
- **Codeur / many-terminals** — parallélisme, spec sheet, horizon agentique long, crons.

Contraste de discipline observé : **une seule boucle à la fois** (endurance, marathon) vs **6 terminaux** (boulimique). Aucun n'a raison — question de bande passante et de durabilité.

## Frameworks conceptuels (la couche qui fait tenir la mécanique)

- **Inversion 80/20** : passer de 80 % exécution → 80 % réflexion/décision/imagination.
- **Friction design** : dans un monde sans friction, choisir *où* en remettre (ex : enlever la friction sur la création de notes, la remettre sur la *manipulation* maïeutique).
- **Anti-dérive vault (Karpathy)** : ne PAS laisser l'IA construire la couche d'interconnexion entre idées → désalignement + auto-amplification → base éclatée. L'humain choisit les liens, l'IA suggère. Cf [[pattern-vault-llm-karpathy]].

## Stack technique — Claude Code suffit

**100 % du système quotidien décrit est faisable en Claude Code** (skills, agents, workflows, MCP, vault Obsidian). « Lia » dans la vidéo = simplement leur surnom pour « l'IA ».

Seul l'« infra de rêve » (aspirationnel, non quotidien) sort de Claude Code : **OpenCode** (CLI agentique open-source sur Vercel AI SDK) pour un horizon autonome plus long + **crons**, et **modèles open-source fine-tunés** (GLM-5.1, Kimi) pour souveraineté/vitesse. À considérer seulement si un jour un horizon agentique plus long que Claude Code devient nécessaire.

## Liens

- [[methode-analyser-repo]] — méthode sœur (auditer un repo existant)
- [[comment-creer-skill]] · [[comment-creer-agent]] · [[comment-creer-hook]] · [[comment-ecrire-claudemd]]
- [[mcp-vs-skills-doctrine]] — MCP (donnée) vs Skills (how-to)
- [[workflow-claude-code-optimal]] — orchestration sans scaffolding workflow
- [[erreur-hooks-workflow-enforcement]] — pourquoi le validateur n'est PAS un hook
- [[pattern-vault-llm-karpathy]] — anti-dérive de la couche d'interconnexion
