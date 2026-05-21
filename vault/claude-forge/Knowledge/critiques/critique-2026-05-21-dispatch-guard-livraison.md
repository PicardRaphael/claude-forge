---
titre: "Critique — dispatch-guard + fix tdd-guard + migration agent_type"
resume: "1 bloquant (agent_type vs subagent_type non verifie empiriquement, risque deadlock), 2 avertissements (Bash heredoc bypass, marker set-and-forget). Fix 2 lignes propose."
aliases:
  - "critique dispatch-guard"
  - "DA dispatch guard neo_ia ia_back"
  - "critique agent_type vs subagent_type"
  - "devil advocate dispatch-guard 21 mai"
  - "critique delegation enforcement hook"
type: knowledge
domaine: claude-code
derniere-maj: 2026-05-21
auteur: devils-advocate
tags:
  - "#type/knowledge"
  - "#type/critique"
  - "#projet/neo-ia"
  - "#projet/ia-back"
  - "#domaine/claude-code"
sources:
  - "Session 2026-05-21 — dispatch-guard suite critique color-tdd-cto-mindset"
---

## Devils Advocate — dispatch-guard + fix tdd-guard + migration agent_type

**Intention declaree :** Bloquer de maniere deterministe la session principale quand elle tente d'ecrire du code source au lieu de deleguer aux agents dev, en complement de la rule advisory cto-mindset qui etait ignoree (~80% compliance).

---

### Verdict

**Bloquants :** 1 | **Avertissements :** 2 | **Nitpicks :** 1

**Decision recommandee :** LIVRER AVEC CORRECTIONS (la correction est 2 lignes, a exiger avant ship)

---

### Si je devais le faire marcher malgre mes objections

**Correction obligatoire (2 lignes par fichier)** — remplacer la detection simple par une multi-field :

Python (dispatch-guard.py et tdd-guard.py) :
```python
agent_type = data.get("agent_type", "") or data.get("subagent_type", "")
```

TypeScript (dispatch-guard.ts et tdd-guard.ts) :
```typescript
const agentType = String(data.agent_type ?? data.subagent_type ?? "");
```

Cela couvre les deux hypotheses de nommage et les variations inter-versions CC (documentees dans la memoire hook-creator : "field name varie selon les CC versions").

**Verification empirique recommandee** (5 min, pas bloquant si multi-field en place) : ajouter temporairement un dump JSON dans un fichier log a l'entree du hook, invoquer un vrai subagent dev qui fait un Write, lire le log, confirmer quel champ est injecte.

**Bash heredoc** : ajouter un hook PreToolUse Bash qui detecte les patterns `cat >`, `tee`, `echo >`, `printf >` ciblant des fichiers source. Pas urgent si le modele ne genere pas spontanement ces patterns (il prefere Write/Edit), mais a planifier.

---

### Angle Technique — Qu'est-ce qui se casse ?

Le dispatch-guard repose sur une hypothese non verifiee empiriquement : que le runtime Claude Code injecte un champ nomme `agent_type` au top-level du JSON stdin des hooks PreToolUse quand ils s'executent dans le contexte d'un subagent.

**Preuves contradictoires trouvees :**
1. `vault/01-Claude/Code/best-practices/agents-orchestration.md` dit : le `name` de l'agent est "recu par les hooks comme `agent_type`" — supporte l'hypothese
2. `vault/01-Claude/Code/changelog/CC mai 2026.md` (v2.1.140) dit : "`subagent_type` sur agent hook input" — **nom different**
3. `.claude/agent-memory/hook-creator/hook_devil_advocate_pair.md` dit : "`subagent_type` est le champ canonique, mais fallback JSON scan complet car field name varie selon les CC versions" — **confirme l'instabilite du nom**
4. Les `agent-marker-writer` existants (neo_ia et ia_back) utilisent `tool_input.subagent_type` (dans PostToolUse Agent), pas `data.agent_type`

**Risque asymetrique :**
- Si `agent_type` n'existe pas dans PreToolUse → le hook ne reconnait AUCUN subagent → bloque dev-neochat, dev-neodoc, tous les agents dev → dispatch loop deadlocked → **pire que le probleme original**
- Si `agent_type` existe → tout fonctionne comme prevu

Les 14/14 tests passes utilisent du JSON pre-forme injecte par pipe, pas le runtime CC reel. Ils testent la logique du hook, pas l'hypothese du champ.

**Objections :**
- BLOQUANT : Le nom du champ (`agent_type` vs `subagent_type`) n'a pas ete verifie empiriquement en conditions reelles. 3 sources internes se contredisent. Risque de deadlock si le champ n'existe pas (tous les agents dev bloques).
- AVERTISSEMENT : La fuite Bash heredoc (`cat > file.py <<EOF`) contourne le dispatch-guard. Confirme empiriquement : un `Bash` tool call avec heredoc passe le hook avec exit 0 car le matcher est `Write|Edit|MultiEdit`, pas `Bash`. Le modele preferera Write/Edit dans 95% des cas, mais apres un blocage repete, il peut pivoter vers Bash heredoc comme contournement (comportement documente dans le vault [[erreur-auto-mode-classifier-self-modification]]).
- AVERTISSEMENT : Le `.dispatch-bypass` marker est set-and-forget, meme pattern que `.tdd-bypass` deja critique dans [[critique-tdd-neo-ia-proposal]]. Pas de reset automatique, pas de TTL. Un bypass oublie = protection desactivee indefiniment.
- NITPICK : `EXEMPT_PREFIXES` ia_back contient `test/` mais les tests reels sont dans `src/**/__tests__/`. Le prefix `test/` est un no-op (le dossier n'existe pas). Pas un probleme — juste du dead code dans la config.

---

### Angle Strategique — Est-ce le bon probleme ?

Oui. La critique precedente ([[critique-2026-05-21-color-tdd-cto-mindset]]) identifiait exactement ce manque : "Le discriminant technique existe. Un dispatch-guard resolverait le vrai probleme." Ce livrable repond directement a cette recommandation.

Le passage de `CLAUDE_AGENT` (env var jamais settee) a `agent_type` (stdin JSON) est le bon move architectural — detection par le runtime plutot que par convention manuelle.

**Objections :**
- Aucun bloquant strategique
- AVERTISSEMENT : Le tdd-guard ia_back (`tdd-guard.ts`) n'a pas beneficie du meme fix de faux positifs que neo_ia. La fonction `findTestFile()` ia_back reste basique (sibling + `__tests__/` exact match) vs neo_ia (multi-search, prefixed match, parent remontee). Ce n'est pas le scope de ce livrable, mais c'est une dette a suivre.

---

### Angle Pratique — Combien de temps avant l'abandon ?

Le hook est simple (115L Python, 80L TypeScript), sans dependances externes, sans etat complexe. Maintenance faible — un hook PreToolUse est fire-and-forget.

Le seul cout de maintenance previsible : quand CC changera le nom/format du champ agent dans le stdin JSON (ce qui est deja arrive au moins une fois d'apres les sources internes). La detection multi-field proposee mitigue ce risque.

**Objections :**
- Aucun bloquant pratique
- AVERTISSEMENT : Les exemptions hardcodees (EXEMPT_PREFIXES, EXEMPT_SUFFIXES) divergeront entre les 2 repos au fil du temps sans synchronisation. Pas critique maintenant — les repos ont des stacks differentes — mais a surveiller.

---

### Vault — Historique pertinent

- [[erreur-advisory-rules-insuffisantes]] — 3 incidents prouvent que les rules `OBLIGATOIRE` sont ignorees sous pression (~80% compliance). Ce hook est la reponse directe.
- [[critique-2026-05-21-color-tdd-cto-mindset]] — critique precedente qui recommandait exactement ce dispatch-guard. Recommandation suivie.
- [[critique-tdd-neo-ia-proposal]] — bypass marker set-and-forget deja identifie comme risque.
- Memoire hook-creator (`hook_devil_advocate_pair.md`) — confirme que le field name varie selon les versions CC, recommande fallback multi-field.
