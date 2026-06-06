---
type: reference
domaine: claude-code
sujet: subagents
mis_a_jour: 2026-06-06
tags: [claude-code, subagent, agent, skills, hooks, delegation, fiabilite]
---

# Référence — Subagents Claude Code CLI

> Guide de référence orienté fiabilité. Couvre : quand créer un subagent (et quand NE PAS), l'anatomie complète, ce qui est hérité ou non, pourquoi un subagent n'appelle pas ses skills, et comment forcer un workflow à 90-100 %. Pour le CLI (où les hooks fonctionnent).

## TL;DR

- **Un subagent sert à DEUX choses : l'isolation de contexte et le parallélisme.** Pas à « organiser le code » ni à « faire propre ». Si la tâche n'a pas besoin d'un contexte frais isolé ou de tourner en parallèle, **ne crée pas de subagent** — mets la logique dans une skill ou dans CLAUDE.md.
- **Le piège n°1 : sur-déléguer.** Un subagent ne voit pas la conversation, ne peut pas poser de questions (`AskUserQuestion` indisponible), n'a pas le MCP de façon fiable, et ne reçoit que le brief qu'on lui passe. Déléguer une tâche qui a besoin d'interaction ou de contexte = la casser.
- **Le champ `skills:` ne FORCE rien**, il précharge des descriptions. Sans l'outil `Skill` dans `tools:`, le subagent ne peut même pas invoquer de skill. Pour garantir un comportement → hook `SubagentStop` (exit 2 / `decision:block`), seul mécanisme déterministe.

---

## PARTIE 1 — QUAND créer un subagent (et quand PAS)

C'est la décision la plus importante, car la plupart des problèmes viennent d'une mauvaise délégation.

### Un subagent résout exactement deux problèmes

1. **Isolation de contexte** — sortir le travail bruyant (lire 40 fichiers, explorer, chercher) du transcript principal pour ne pas saturer la fenêtre de contexte. Le subagent fait le sale boulot dans SON contexte, et ne renvoie qu'un résumé.
2. **Parallélisme** — lancer plusieurs workers en même temps (background avec Ctrl+B, ou fork).

Si ton besoin n'est NI l'un NI l'autre, le subagent est le mauvais outil.

### Quand créer un subagent ✅

- Une sous-tâche lourde qui lirait/explorerait beaucoup et polluerait le contexte principal (recherche dans un gros repo, analyse exploratoire).
- Une revue « fresh-eyes » : un lecteur zéro-contexte détecte ce que l'auteur ne voit plus (pattern officiel Anthropic pour pptx/doc-coauthoring).
- Du travail parallélisable sans communication entre workers.
- Une expertise réutilisable et bien délimitée (un reviewer de sécurité, un explorateur de codebase).

### Quand NE PAS créer de subagent ❌

- **La tâche a besoin de poser des questions à l'utilisateur** → `AskUserQuestion` ne marche pas en subagent. C'est rédhibitoire. (Cas typique : un skill-creator qui doit interviewer.)
- **La tâche a besoin du contexte de la conversation** → le subagent démarre vierge, il ne sait que ce qu'on lui passe dans le brief.
- **La tâche a besoin du MCP** (vault forge-brain, etc.) → le MCP n'est pas garanti dans un subagent (« No such tool available »).
- **Juste pour « faire propre » ou « organiser »** → ce n'est pas un critère. Une skill ou une section de CLAUDE.md fait le travail sans les inconvénients.
- **Workers qui doivent communiquer entre eux** → ce sont les Agent Teams (expérimental), pas des subagents.
- **Comportement obligatoire/déterministe** → c'est un hook, pas un subagent.

### Le test en une phrase

> « Est-ce que cette tâche a besoin d'un contexte frais isolé OU de tourner en parallèle, ET n'a pas besoin de poser de questions ni du contexte de la conversation ? » Si non → ce n'est pas un subagent.

---

## PARTIE 2 — Ce qu'un subagent hérite (et n'hérite PAS) du parent

Table de référence. Détermine toute la stratégie.

| Élément | Hérité par le subagent ? |
|---|---|
| **Contexte de conversation** | ❌ Contexte frais isolé. Ne reçoit que le brief passé par le parent |
| **Skills** | ❌ Pas automatiquement. Champ `skills:` = précharge les *descriptions*. Sinon, un subagent avec accès filesystem peut *découvrir* les skills en scannant `.claude/skills/` |
| **Outils (Read, Bash…)** | ❌ Définis par le champ `tools:`. Sans `tools:` explicite, comportement variable → risque (un agent a fait `git reset` et effacé 40 min de travail, incident mars 2026) |
| **Outil `Skill`** | ❌ Doit être dans `tools:` sinon le subagent ne PEUT PAS invoquer de skill |
| **MCP servers** | ⚠️ Instable — souvent « No such tool available ». Pas garanti |
| **CLAUDE.md / rules** | ⚠️ Variable. Explore/Plan sautent CLAUDE.md ; les autres le chargent. Ne pas s'y fier pour un subagent |
| **AskUserQuestion** | ❌ **Filtré hors des subagents** (issues #12890, #18721, #20275). Un subagent ne pose pas de questions |
| **Task tool (sous-subagent)** | ❌ Pas de subagents imbriqués |
| **Hooks** | ✅ Les hooks settings s'appliquent. `SubagentStart`/`SubagentStop` existent pour ça. (Les hooks `Stop` en frontmatter d'agent sont auto-convertis en `SubagentStop`) |
| **Mémoire (`memory:`)** | ✅ Persiste entre sessions si configurée |

**Deux conséquences majeures :**
1. **Pattern brief-then-direct** : puisque MCP et conversation ne sont pas garantis, le parent doit BRIEFER le subagent inline (lui passer le contenu canonique dans le prompt de délégation). Ne jamais compter sur le subagent pour aller chercher dans le vault.
2. **Pas de questions en subagent** : si une tâche doit interroger l'utilisateur, l'interview se fait sur le thread PRINCIPAL avant la délégation, puis les réponses sont passées dans le brief.

---

## PARTIE 3 — Anatomie complète d'un subagent

### Emplacements
- `.claude/agents/*.md` (projet, committable)
- `~/.claude/agents/*.md` (user, tous projets)
- Plugin-bundled

### Frontmatter complet

```yaml
---
name: mon-agent              # OBLIGATOIRE — kebab-case
description: ...             # OBLIGATOIRE — déclencheur de délégation (directif !)
tools: Read, Write, Edit, Bash, Skill   # outils autorisés — TOUJOURS explicite
model: sonnet               # sonnet|opus|haiku|inherit (défaut: inherit)
skills:                     # PRÉCHARGE les descriptions de ces skills (ne force pas)
  - cc-skills-ref
disallowedTools: Skill(forge-brain)   # pour EXCLURE une skill/un outil précis
color: pink
memory: project             # mémoire persistante entre sessions
permissionMode: acceptEdits
effort: high                # low|medium|high|xhigh (max supprimé v2.1.91)
---

(corps = system prompt de l'agent — son identité, son workflow, ses règles)
```

Seuls `name` et `description` sont requis.

### Résolution du modèle
Ordre : variable d'env `CLAUDE_CODE_SUBAGENT_MODEL` > `model` du frontmatter > paramètre passé à l'invocation > `inherit` (défaut). Pattern courant : Opus pour l'orchestration/jugement, Sonnet pour l'implémentation, Haiku pour explore/recherche.

### Invocation
- **Auto-délégation** via la `description` (Claude décide de déléguer)
- **Mention explicite** `@"mon-agent (agent)"` pour GARANTIR la délégation
- **Task tool** (programmatique)

### Le corps = system prompt
Il définit l'identité de l'agent, son workflow, ses règles, son format de sortie. C'est là que vit le critique (voir Partie 5).

---

## PARTIE 4 — POURQUOI un subagent n'appelle pas ses skills

Le problème le plus fréquent. Trois causes se cumulent.

### Cause 1 — `Skill` absent de `tools:` (mécanique)
Sans l'outil `Skill` dans le champ `tools:`, le subagent **ne peut pas** invoquer de skill, quoi que dise son corps. À vérifier en TOUT PREMIER.

### Cause 2 — `skills:` précharge, ne force pas
Doc officielle : ce champ « contrôle quelles skills sont préchargées, pas lesquelles le subagent peut utiliser ». Issue #32910 : il injecte les *descriptions* dans le system prompt au démarrage. « Description présente » ≠ « skill invoquée ». L'invocation reste une décision du modèle — même problème probabiliste qu'une skill sur le thread principal.

### Cause 3 — Le subagent préfère faire le travail directement
Finding empirique (Seleznov) : Claude saute l'invocation d'un skill quand il peut faire le travail avec un raccourci (Bash, sa propre connaissance). Si le subagent a tous les outils pour produire le résultat sans passer par la skill, il le fait. La skill devient un détour optionnel qu'il s'autorise à zapper.

### Le verdict
La présence dans `skills:` ne garantit jamais l'invocation. Pour la forcer, il faut d'autres leviers (Partie 6).

---

## PARTIE 5 — Design du corps de l'agent (system prompt)

Mêmes principes que pour une skill, appliqués au system prompt :

- **Responsabilité unique.** Un agent = une expertise. Surveille qu'il ne devienne pas un fourre-tout.
- **Workflow impératif numéroté**, étapes bloquantes, pas de prose descriptive.
- **L'invocation des skills doit être une ÉTAPE explicite**, pas une ligne noyée dans une liste :
  > « ÉTAPE 1 — OBLIGATOIRE AVANT TOUT. Invoque la skill `cc-skills-ref` (outil Skill). Ne génère rien avant. Raison : sans elle tu produis du format obsolète qui ne se déclenche jamais. »
- **Explique le POURQUOI** plutôt que des MAJUSCULES partout (le tout-caps est un drapeau jaune — réserve-le aux 1-2 étapes vraiment fragiles). La raison devient le critère que Claude utilise pour les cas non anticipés.
- **Inline le critique** dans le corps (voir Partie 6, niveau 2).
- **Étapes à sortie visible.** Le subagent saute les étapes sans output visible (comme la validation). Force une sortie : « Affiche le résultat de validate.py avant de continuer. »
- **Checklist à cocher** pour les workflows multi-étapes.
- **Court.** Les skills listées dans `skills:` sont injectées en ENTIER dans le contexte du subagent → agent + 3 skills longues = contexte saturé, étapes oubliées. Garde agent ET skills courts.

---

## PARTIE 6 — Forcer le workflow et l'invocation des skills (du mou au dur)

### Niveau 1 — Ordre impératif numéroté dans le corps (indispensable)
L'invocation du skill = ÉTAPE 1 bloquante avec raison (cf. Partie 5). Levier de base, mais probabiliste.

### Niveau 2 — Inline le critique dans le corps de l'agent (le plus fiable côté contenu)
**Principe : si une connaissance DOIT toujours être présente, ne la mets pas dans une skill séparée que le subagent peut zapper — mets-la dans le system prompt de l'agent.** Une skill est un détour optionnel ; le corps de l'agent est toujours chargé. Les 5-6 règles non-négociables vivent inline ; la skill devient la référence détaillée.

### Niveau 3 — Script-output gating
Un script de validation que l'agent doit lancer, et dont la sortie le bloque. La règle non-négociable vit dans le CODE, pas dans la prose. Déterministe.

### Niveau 4 — Hook SubagentStop (enforcement dur, CLI)
Se déclenche quand le subagent finit. Peut forcer la continuation s'il n'a pas fait son travail. C'est la SEULE vraie garantie.

**Détecter qu'un skill a été invoqué** : pas de signal propre fiable (PostToolUse `matcher:"Skill"` ne se déclenche pas, issue #43630). Méthode robuste = parser le transcript JSONL (`agent_transcript_path`), le Skill tool y figure comme `tool_use`.

Exemple SubagentStop (command) :
```python
#!/usr/bin/env python3
import json, sys, os
data = json.load(sys.stdin)
if data.get("stop_hook_active"):   # anti-boucle infinie : OBLIGATOIRE
    sys.exit(0)
tp = data.get("agent_transcript_path") or data.get("transcript_path")
used = False
try:
    with open(os.path.expanduser(tp)) as f:
        for line in f:
            if '"name": "Skill"' in line and "cc-skills-ref" in line:
                used = True
    if not used:
        print(json.dumps({"decision": "block",
          "reason": "Tu n'as pas invoqué cc-skills-ref. Invoque-le via l'outil Skill puis termine."}))
        sys.exit(0)   # exit 0 + JSON (PAS exit 2, sinon le JSON est ignoré)
except Exception:
    pass
sys.exit(0)
```

**Pièges hooks critiques :**
- **`exit 2` bloque ; `exit 1` ne bloque JAMAIS** (le bug le plus courant).
- Pour Stop/SubagentStop, utilise **`exit 0` + JSON `{"decision":"block","reason":...}`** (le `reason` devient le prochain prompt). Si tu fais exit 2, le JSON est ignoré.
- **Toujours vérifier `stop_hook_active`** pour éviter la boucle infinie (cap natif à 8 blocages).
- Bug #10412 : les Stop hooks exit 2 installés via plugin échouent → installe depuis `.claude/hooks/`.

### Niveau 5 — UserPromptSubmit (rappel injecté)
Un hook UserPromptSubmit imprime sur stdout (ajouté au contexte) un rappel d'activation du skill avant que le modèle agisse.

### Niveau 6 — `disallowedTools` (couper les raccourcis)
Si l'agent zappe le skill parce qu'il fait le travail directement, restreins ses outils (ex. un agent d'audit n'a que `Read, Skill`, pas `Write`).

---

## PARTIE 7 — Agent vs Skill vs Rule vs Hook : où mettre quoi

| Tu veux… | Mécanisme | Pourquoi |
|---|---|---|
| Isolation de contexte / parallélisme | **Subagent** | Contexte frais, renvoie un résumé |
| Connaissance/workflow réutilisable invocable à la demande | **Skill** | Chargée on-demand, progressive disclosure |
| Comportement TOUJOURS actif (routing, conventions) | **`.claude/rules/`** | Chargé chaque session, priorité CLAUDE.md |
| Ce qui s'applique partout, court et stable | **CLAUDE.md** | Routing global, standards |
| Comportement OBLIGATOIRE déterministe | **Hook (exit 2)** | Seul enforcement garanti |

**Règle d'or de l'enforcement :** rules, CLAUDE.md et corps de skill/agent sont des SUGGESTIONS (probabiliste). Seuls les hooks (exit 2 / decision:block) et le gating par sortie de script sont GARANTIS.

---

## PARTIE 8 — Le vault et le MCP dans un repo Jarvis

Point clé pour ton architecture (repo avec vault d'apprentissage) :

- **Le vault Obsidian (via MCP forge-brain) nourrit le THREAD PRINCIPAL**, où le MCP est fiable.
- **Le subagent n'a PAS le MCP de façon garantie.** Donc : tout ce qui doit survivre dans un subagent doit être **inliné** dans son corps ou ses skills — jamais seulement dans le vault.
- **Règle d'or : vault = thread principal ; inline = subagent.**
- Pour l'apprentissage : `memory: project` sur l'agent persiste les patterns entre sessions. Le vault reste la source de vérité canonique, mis à jour depuis le thread principal.

---

## PARTIE 9 — Checklist d'un subagent quasi-parfait

**Décision (avant tout)**
- [ ] La tâche a besoin d'isolation de contexte OU de parallélisme ?
- [ ] Elle n'a PAS besoin de poser des questions (sinon → skill/thread principal) ?
- [ ] Elle n'a PAS besoin du MCP ni du contexte de conversation (sinon → brief inline) ?

**Définition / frontmatter**
- [ ] `name` kebab-case = nom du fichier
- [ ] `description` directive (déclencheur de délégation), 3e personne
- [ ] `tools:` explicite — **inclut `Skill`** si l'agent doit invoquer des skills
- [ ] `model` adapté (haiku explore, sonnet implémentation, opus orchestration)
- [ ] `skills:` liste les skills à précharger
- [ ] `disallowedTools` pour couper les raccourcis qui font zapper les skills

**System prompt / exécution**
- [ ] Responsabilité unique
- [ ] Workflow impératif numéroté, étapes bloquantes
- [ ] Invocation des skills = ÉTAPE 1 explicite avec outil Skill + raison
- [ ] Critique inliné dans le corps (pas seulement dans une skill zappable)
- [ ] Étapes à sortie visible (anti-skip de la validation)
- [ ] Corps court + skills courtes (injectées en entier → anti-saturation)
- [ ] Explique le pourquoi ; majuscules réservées aux 1-2 étapes fragiles

**Fiabilité d'invocation des skills**
- [ ] `Skill` dans `tools:` (sinon impossible mécaniquement)
- [ ] Ordre impératif dans le corps
- [ ] Hook SubagentStop qui vérifie (parse transcript, exit 0 + JSON decision:block)
- [ ] `stop_hook_active` vérifié (anti-boucle)

**Accès / MCP / questions**
- [ ] Pas de dépendance MCP dans le subagent → brief inline
- [ ] Pas de questions prévues dans un subagent (impossible) → interview sur thread principal avant délégation
- [ ] Vault = thread principal ; inline = subagent

**Hooks (CLI)**
- [ ] exit 2 (jamais exit 1) pour PreToolUse ; exit 0 + JSON pour Stop/SubagentStop
- [ ] Vérifié via `/hooks` que le hook est enregistré
- [ ] Si distribué en plugin et Stop hook KO → installer depuis `.claude/hooks/` (#10412)

**Évaluation**
- [ ] Testé sur haiku/sonnet/opus
- [ ] Mesuré le taux réel d'invocation des skills
- [ ] Lu les transcripts, pas juste l'output final

---

## La vérité dure

1. **La plupart des problèmes viennent de la sur-délégation.** Un subagent n'est ni « plus propre » ni « mieux organisé » par défaut — il isole le contexte et parallélise. Sinon, skill ou CLAUDE.md.
2. **Un subagent ne pose pas de questions, n'a pas le MCP fiable, ne voit pas la conversation.** Déléguer une tâche qui en a besoin = la casser. Interview et accès vault sur le thread principal, puis brief inline.
3. **`skills:` ne garantit pas l'invocation ; `Skill` doit être dans `tools:`.** Vérifie ça en premier quand un agent « ne fait pas tout ».
4. **Le critique vit dans le corps de l'agent**, pas dans une skill optionnelle qu'il s'autorise à zapper.
5. **Seuls les hooks (exit 2 / decision:block) garantissent un comportement.** Tout le reste est probabiliste.
