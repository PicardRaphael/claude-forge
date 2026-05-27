---
aliases:
  - vault jamais consulté session principale
  - session skip vault avant brief
  - délégation lecture vault sub-agent
  - brief sub-agent sans contexte vault
  - vault pas call en premier
  - erreur consultation vault session
auteur: claude
cree: 2026-05-27
derniere-maj: 2026-05-27
repo: claude-forge
resume: La session principale a modifié des templates BRIEF /spec sans consulter le vault d'abord, et a délégué la lecture canonique au sub-agent sans vérifier — travail non sourcé.
tags:
  - "#type/erreur"
  - "#erreur/comportement"
  - "#erreur/vault"
  - "#domaine/claude-code"
titre: Vault jamais consulté par la session principale avant brief sub-agent
type: erreur
---

# Vault jamais consulté par la session principale avant brief sub-agent

## Ce qui s'est passé

Le 2026-05-27, lors du travail sur le workflow Spec-Driven Development de Neoteem (skill `/spec` sur ia_back + neo_ia), la session principale (Jarvis) a :

1. Conçu 4 nouvelles sections de template BRIEF (Gherkin, Recherche préalable, Implémentations de référence, Comment vérifier) en les **inventant**, aidée seulement de l'advisor, **sans lire aucune note canonique du vault**.
2. Briefé l'agent `skill-creator` en lui demandant de lire `comment-creer-skill` — **mauvaise canonique** (on touchait un template de spec/output, pas la structure d'une skill) — **sans vérifier empiriquement** qu'il l'a lue.
3. Découvert APRÈS le reproche de Raphael qu'il existait des notes canoniques directement pertinentes, jamais lues : [[pattern-spec-driven-development]], [[pattern-sdd-triangle]], [[pattern-spec-skill-deployment]] (template BRIEF déjà documenté), [[critique-2026-05-21-brief-distant-template-spec]] (un DA avait DÉJÀ critiqué ce template), [[running-implementation-notes]], [[methode-analyser-repo]].

## Pourquoi c'est une erreur

- CLAUDE.md forge ligne critique : "AVANT toute proposition / recherche web / refonte : consulter le vault via MCP forge-brain. Le vault contient probablement déjà la réponse."
- Les rules `forge-brain-proactive.md`, `sequence-canonique-modification.md`, `vault-consultation-protocol.md` l'exigent.
- Le travail produit est **non sourcé** : peut diverger des patterns canoniques, ignorer une critique DA existante, réinventer du déjà-documenté.
- Combinaison de 3 anti-patterns : biais d'action en session longue + délégation de la lecture vault au sub-agent + absence de vérification empirique.

## Quoi faire à la place

1. La SESSION PRINCIPALE consulte le vault EN PREMIER (`search_brain` sur le sujet réel, puis `read_note` EN ENTIER des canoniques).
2. Choisir la canonique par le SUJET de la tâche (SDD, BRIEF, handoff), pas par le type de fichier.
3. EXTRAIRE le contexte vault et le METTRE dans le brief du sub-agent (pattern [[pattern-mcp-brief-then-direct]]).
4. Le sub-agent re-consulte seulement en filet de sécurité.
5. VÉRIFIER empiriquement que le sub-agent a consulté le vault (cf erreur sub-agent claim sans empirie).

## Pattern général

La règle "consulter le vault d'abord" est advisory et a été zappée sous pression (session longue, fatigue, biais d'action). Question ouverte : faut-il un enforcement plus fort sans tomber dans le workflow-hook (anti-pattern doctrine 22 mai) ? Audit de réparation dédié : `claude-forge/PROMPT-audit-vault-jamais-consulte.md`.

## Liens

- [[methode-analyser-repo]]
- [[pattern-mcp-brief-then-direct]]
- [[pattern-spec-skill-deployment]]
- [[critique-2026-05-21-brief-distant-template-spec]]
