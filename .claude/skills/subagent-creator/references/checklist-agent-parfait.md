# Checklist agent parfait — 5 dimensions

Source : reference-subagents-claude-code.md (research LLM juin 2026) + doctrine forge.

---

## 0. Décision — Faut-il vraiment un subagent ? (OBLIGATOIRE)

- [ ] La tâche a besoin d'isolation de contexte OU de parallélisme ?
- [ ] Elle n'a PAS besoin de poser des questions (AskUserQuestion filtré en subagent) ?
- [ ] Elle n'a PAS besoin du MCP vault fiable (MCP non garanti en subagent) ?
- [ ] Elle n'a PAS besoin du contexte de la conversation ?
- [ ] Ce n'est PAS un comportement déterministe obligatoire (→ hook à la place) ?
- [ ] Les workers n'ont PAS besoin de communiquer entre eux (→ Agent Teams sinon) ?

## 1. Frontmatter

- [ ] `name` kebab-case = nom exact du fichier sans `.md`
- [ ] `description` : directive 3e personne, UNE SEULE LIGNE anglais, jamais `>-` ni `|`
- [ ] `description` : "Use this agent when… Use PROACTIVELY when… Input must include…"
- [ ] `tools:` TOUJOURS explicite (sans → comportement variable, risque)
- [ ] `Skill` dans `tools:` si l'agent doit invoquer des skills (sinon impossible mécaniquement)
- [ ] `disallowedTools: Agent` — subagents ne peuvent PAS spawner (by design, issue #19077)
- [ ] `disallowedTools: Write, Edit` si agent read-only
- [ ] `disallowedTools: Bash` si délégation forcée (Bash = raccourci qui zappe les skills)
- [ ] `model` adapté : haiku (exploration), sonnet (implémentation), opus (jugement)
- [ ] `effort` calibré par TYPE : `xhigh` agentique/coding · `high` jugement structuré · `medium`/`low` extraction · `max` ponctuel jamais frontmatter
- [ ] `color` selon convention forge cross-repo (même rôle = même couleur)
- [ ] `memory: project` — TOUJOURS, sans exception
- [ ] `permissionMode` — TOUJOURS (`acceptEdits` pour writers, `plan` pour side-effects)
- [ ] `isolation: worktree` si agents parallèles sur fichiers

## Champs frontmatter VALIDES (liste FERMÉE — ne jamais en inventer)

Seuls ces champs existent dans le frontmatter d'un subagent. **Tout autre champ = ERREUR à signaler, JAMAIS à ajouter.**

| Champ | Obligatoire ? | Valeurs |
|-------|---------------|---------|
| `name` | OUI | kebab-case = nom du fichier sans `.md` |
| `description` | OUI | une ligne directive 3e personne |
| `tools` | OUI (explicite) | liste — inclure `Skill` si l'agent invoque des skills |
| `disallowedTools` | recommandé | `Write, Edit` (read-only) / `Agent` / `Bash` |
| `model` | OUI | `sonnet` / `opus` / `haiku` |
| `effort` | OUI | `high` / `xhigh` |
| `color` | recommandé | convention forge (red/orange/.../pink) |
| `memory` | OUI | `project` — toujours |
| `permissionMode` | OUI | `acceptEdits` / `plan` |
| `skills` | optionnel | liste de skills à précharger |
| `isolation` | optionnel | `worktree` (agents parallèles) |
| `maxTurns` | optionnel | entier |

**Champs INTERDITS (n'existent PAS pour un agent)** : `version`, `author`, `date`, `user-invocable` (skill uniquement), `allowed-tools` (agent = `tools`, pas `allowed-tools`), `disable-model-invocation`.

Si un audit signale l'absence d'un champ interdit comme un écart → c'est l'audit qui se trompe. Vérifier contre cette liste fermée AVANT de classer un champ « manquant ».

## 2. Body (system prompt)

- [ ] Ordre : Rôle → Input reçu → Étapes numérotées → Règles → Format sortie
- [ ] Responsabilité unique (1 agent = 1 expertise)
- [ ] Si skills nécessaires : invocation = ÉTAPE 1 bloquante avec raison explicite
- [ ] Règles non-négociables inlinées dans le body (pas seulement dans une skill zappable)
- [ ] Pattern ESCALADE inclus (AskUserQuestion indisponible en subagent) :
  ```
  ## AMBIGUÏTÉ DÉTECTÉE — escalade session principale
  Contexte / Ambiguïté / Options / Recommandation / Question / État
  ```
- [ ] Étapes à sortie visible (anti-skip de la validation)
- [ ] Body court — skills injectées EN ENTIER au démarrage, saturation si long
- [ ] Frontmatter non re-commenté dans le body (le frontmatter fait foi)
- [ ] JAMAIS "Pas de commit" dans le body seulement — mettre aussi dans le prompt d'invocation en TOP gras

## 3. Héritage & MCP

- [ ] Pas de dépendance MCP dans le subagent → brief inline depuis session principale
- [ ] Pas d'interview prévue dans le subagent → interview sur thread principal avant délégation
- [ ] Brief enrichi passé par session principale : contexte + canoniques + feedbacks inline
- [ ] `skills:` liste les skills à précharger (descriptions injectées — ne force pas l'invocation)

## 4. Enforcement (si skills à invoquer)

- [ ] `Skill` dans `tools:` (condition mécanique minimale)
- [ ] Ordre impératif dans le body (niveau 1)
- [ ] Règles critiques inlinées dans le body, pas seulement dans une skill (niveau 2)
- [ ] Script-output gating si déterministe requis (niveau 3)
- [ ] Hook SubagentStop si garantie CLI requise : exit 0 + JSON decision:block + stop_hook_active vérifié (niveau 4)

## 5. Evals (OBLIGATOIRES)

- [ ] 3 rounds d'interview complétés avant de rédiger
- [ ] Test cases (2–3) validés par l'utilisateur
- [ ] Runs with_agent + baseline lancés simultanément via Task tool
- [ ] Eval viewer généré AVANT jugement
- [ ] Seule exception : agent de jugement pur subjectif → éval qualitative uniquement
