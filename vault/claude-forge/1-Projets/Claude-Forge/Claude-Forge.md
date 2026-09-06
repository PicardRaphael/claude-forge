---
titre: Claude-Forge
resume: Framework personnel Claude Code/Codex — contrats, skills, hooks, vault canonique et mémoire contrôlée
aliases:
  - claude-forge
  - forge
  - le forge
  - framework forge
type: context
status: active
derniere-maj: 2026-09-06
auteur: claude
tags:
  - "#type/context"
  - "#type/projet"
  - "#projet/claude-forge"
---

## Description

Framework personnel de productivité pour Claude Code et Codex, créé par
[[Raphael-Picard|Raphaël]]. Il fournit des contrats, skills, rules, hooks et
adaptateurs cross-platform, avec forge-brain comme second cerveau canonique.

## Pourquoi ce projet

Transformer les agents de code en partenaires de type Jarvis : anticiper,
protéger, apprendre, challenger et capitaliser sans accumuler de contexte
périmé. Le projet est aussi une vitrine de l'expertise IA de Raphaël.

## Architecture active

- `AGENTS.md` : contrat commun Claude Code/Codex.
- `CLAUDE.md` : adaptateur Claude court.
- `.claude/skills/` : noyaux de workflow.
- `.agents/skills/` : adaptateurs Codex minces quand le workflow est partagé.
- forge-brain : doctrine, connaissance, [[Raphael-Picard|profil/casquettes]],
  projets stables et décisions.
- `memory/` : adaptateurs, incidents empiriques et phases projet temporaires.
- mémoires natives Claude/Codex : shadow recall non autoritaire.
- hooks : lint, sécurité, scope et détection déterministe, jamais writer
  sémantique.

## Chaîne de vérification locale

`AGENTS.md` § Vérification locale déclare ce qui est vivant : trois suites de
tests (hooks Claude, hooks Codex, scripts) et quatre gardes — routages morts,
frontmatters cassés, tests jamais collectés, divergence entre surfaces jumelles.
Un outil ou une suite absent de ce bloc ne s'exécute jamais ; l'y ajouter est le
même geste que l'écrire. Méthode et pièges de calibrage :
[[dette-silencieuse-config]].

## Contraintes

- Projet personnel, pas Neoteem.
- Généraliste ; aucun focus repo professionnel sans demande.
- Les repos consommateurs restent autonomes sans claude-forge.
- Le vault est accessible uniquement via MCP forge-brain.
- La session principale est l'unique writer sémantique du vault.
- Aucune suppression automatique de note entière.

## Second cerveau — état 2026-08-28

Le pivot [[raisonnement-2026-08-28-profil-projets-vault-canoniques]] est appliqué :

- [[Raphael-Picard]] et ses casquettes remplacent la biographie locale comme
  source de vérité ; `memory/user_raphael_profile.md` devient un adaptateur.
- `project-memory` crée un hub unique lors d'une demande explicite de création
  de projet et conserve les choix durables.
- Les choix réversibles restent dans le hub ; les décisions structurantes sont
  reliées depuis `Knowledge/decisions/`.
- `done` consolide profil, casquettes, projets, décisions, connaissance et
  contexte temporaire dans leurs foyers.
- Le hook `learning-reminder` Claude reste un détecteur non bloquant ; Codex
  s'appuie sur les règles, skills et `memory-recall` sans faux portage au Stop.
- Les workflows news et session/projet sont séparés mais partagent la règle
  enrichir avant de créer et une relecture après mutation.

## Historique utile

### 2026-09-06

- Outillage de la dette silencieuse : détection des tests jamais collectés et
  du drift entre surfaces jumelles, périmètre du validateur de frontmatter
  étendu aux surfaces Codex.
- Trois propagations Codex manquées en 24 h ont motivé un garde structurel
  plutôt qu'une règle écrite de plus.
- Skill `auditor-empirical-verify` portée côté Claude avec un cinquième point
  absent de l'original — détection du commit parasite d'un sous-agent.

### 2026-07-09

- Sweep des descriptions de skills et réduction du budget résident.
- Fusion de skills de référence après forge-review.
- Correction de `delegate-guard` et validation de ses tests.

### 2026-06-29

- Orientation agent-first actée : forge-brain optimisé pour la boucle Jarvis via
  MCP, navigation humaine optionnelle.
- Doctrine hooks : lint/sécurité/scope uniquement, jamais workflow agentique.
- `/done` a commencé à maintenir les contextes projet existants.

## Liens

- [[Raphael-Picard]]
- [[memoire-optimale-codex-chatgpt]]
- [[raisonnement-2026-08-28-profil-projets-vault-canoniques]]
- [[decision-vault-agent-first]]
- [[methode-pivoter-doctrine]]
