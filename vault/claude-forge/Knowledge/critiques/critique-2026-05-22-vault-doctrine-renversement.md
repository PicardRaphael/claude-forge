---
titre: "Critique — Renversement doctrine vault dans agents createurs"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-22
auteur: claude
aliases:
  - critique-vault-doctrine-renversement
  - critique-etape-0-suppression
  - DA-vault-injection-prompt
  - critique-vault-before-dispatch
tags:
  - "#type/critique"
  - "#projet/claude-forge"
  - "#domaine/agents"
resume: "DA bloque la suppression Etape 0 des createurs - asymetrie hook + advisor inverse + responsabilite session principale fragile"
---

# Critique — Renversement doctrine vault dans agents createurs

## Proposition challengee

Deplacer la consultation vault des 8 agents createurs vers la session principale qui injecterait les best practices dans le prompt de dispatch via nouvelle rule.

## Verdict

**Bloquants : 3 | Avertissements : 4 | Nitpicks : 2**

**Decision : BLOQUER la version proposee.** Le diagnostic ("trop de OBLIGATOIRE, perte de temps") est valide. La solution proposee deplace le probleme vers la couche la moins fiable du systeme (session principale = moi).

## Bloquants

### 1. Asymetrie d enforcement fatale

Le hook `vault-query-guard.py` BLOQUE encore tout Write sur `.claude/skills/`, `.claude/agents/`, `vault/`, `output/` si marker absent ou > 60 min. Aucun bypass specialiste (ligne 18 du hook).

- Garder le hook → createurs sans Etape 0 vont se faire bloquer sans savoir pourquoi
- Desactiver le hook → advisory 80% (cf `feedback_enforce_not_advise`)
- Construire un nouveau hook `pre-dispatch-vault-check` → NON mentionne dans la proposition

La proposition oublie un composant critique du systeme actuel.

### 2. Le tracker matche deja l usage organique

`vault-query-tracker.py` lignes 26-41 declenche le marker sur Read/Grep/Glob de `vault/`, `memory/`, `Knowledge/`, `agent-memory/` et Skill `forge-brain`. En session normale, le marker est deja frais. **L Etape 0 dans createurs n est PAS la cause principale du "perdre du temps".** La vraie cause : agents qui ne respectent pas l escape hatch deja present (skill-creator.md ligne 25).

### 3. "BP injectees dans le prompt" exige une connaissance prealable

La session principale doit chercher dans le vault AVANT de savoir quoi injecter. La proposition ne supprime pas le travail vault — elle le DEPLACE dans le contexte principal qui se pollue, contredisant le pattern "deleguer la recherche aux subagents pour garder le contexte principal propre" (Workflow Boris).

## Avertissements

1. **Distinction analyseurs vs createurs fragile** — skill-creator sur sujet nouveau a meme besoin vault qu auditeur. Le besoin depend du sujet, pas du type d agent.
2. **Etape 0 deja conditionnelle** — l escape hatch existe textuellement. Si agents l ignorent, refondre la doctrine ne fixe pas leur respect du contrat.
3. **Vrai probleme = fatigue / bruit doctrinaire** — solution 10x meilleure : extraire Etape 0 dans rule unique `vault-consultation-protocol.md`, referencee depuis chaque createur en 2 lignes. Reduit verbosite, garde hook, zero regression.
4. **Une rule de plus dans un systeme deja sature** — `feedback_enforce_not_advise` rappelle qu une rule sans hook = advisory.

## Nitpicks

- Le pattern "session principale consulte avant dispatch" est ce qui a echoue hier ("me perdre")
- Cout de maintenance "BP injectees" : 4 etapes manuelles par dispatch vs 2 search_brain en sub-agent

## Plan si on veut faire marcher

1. **MESURER avant de reformer** : 2 semaines instrumentation. Combien de dispatches createurs/jour ? Combien bloques par vault-query-guard ? Combien triviaux ?
2. **Conditionner l Etape 0** : escape hatch explicite `[VAULT_INJECTED]` dans le prompt = skip
3. **Hook symetrique AVANT relachement** : `pre-dispatch-vault-check.py` qui bloque dispatch createur sans marker frais ni `[VAULT_INJECTED]`
4. **Garder Etape 0 integrale pour skill-creator et hook-creator** (les 2 plus a risque). Pour python-dev et self-updater, la proposition tient
5. **Test comportemental** : 5 dispatches reels en session fraiche avant propagation

## Historique vault pertinent

- `critique-2026-05-21-dispatch-guard-livraison.md`
- `critique-2026-05-21-refonte-hooks-16-vers-6.md` — precedent : Raphael a deja simplifie puis du corriger
- `feedback_enforce_not_advise.md` — "Advisory = 80%, hook = 100%". **Proposition fait l inverse explicitement**
- `feedback_hooks_enforcement_pattern.md` — "Rules advisory ignorees, hooks marker+guard obligatoires"
- Commit `de4c297` : vault-before-specialist construit EN REACTION a fiabilite insuffisante de la session principale

## Liens

[[critique-2026-05-21-dispatch-guard-livraison]]
[[critique-2026-05-21-refonte-hooks-16-vers-6]]
