---
name: git-c-pas-cd-multi-repo
description: "Pour git multi-repos, TOUJOURS utiliser `git -C <path>` au lieu de `cd <path> && git`. Le cd persiste entre Bash calls et casse les commandes suivantes."
trigger: git -C, cd, multi-repo, cross-repo, cwd
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72a20014-5e49-4c73-a59e-6512f642233a
---

Quand on travaille sur plusieurs repos dans la même session, `cd <path> && git ...` change le CWD du shell de façon **persistante entre Bash calls successifs**. La commande suivante (qui croit être dans claude-forge) s'exécute en réalité dans le dernier repo où on a cd.

**Cas concret 24 mai 2026** (session propagation hook ia_back + neo_ia) :
- 3 fois CWD a glissé silencieusement après `cd /c/Users/.../neot-v2/neo_ia`
- Tentative de `ls vault/...` après → "No such file or directory" (cwd = neo_ia, pas claude-forge)
- Tentative de `py .tmp_patch3.py` → script non trouvé (cwd = neo_ia, script dans claude-forge)
- Diff intempestif appliqué dans le mauvais repo (risque réel)

**Why :** chaque tool `Bash` exécute un nouveau shell, MAIS le harness Claude Code maintient un CWD persistant entre les calls. Un `cd` dans un call précédent affecte tous les calls suivants jusqu'à explicit reset.

**How to apply :**

Pour git multi-repos, TOUJOURS :

```bash
# BON
git -C /c/Users/.../claude-forge status
git -C /c/Users/.../neot-v2/ia_back status
git -C /c/Users/.../neot-v2/neo_ia status

# MAUVAIS (cd persiste)
cd /c/Users/.../neot-v2/ia_back && git status
```

S'applique aussi à :
- `ls -C <dir>` ? non, ls n'a pas `-C`. Préférer `ls /chemin/absolu/`
- Pour les commandes non-git : utiliser chemins absolus directement (pas de cd intermédiaire)
- Pour les scripts Python avec paths relatifs : `py /chemin/absolu/script.py` ou cd EXPLICITE en début de chaque Bash call

**Cas où `cd` est OK :** une seule commande dans un seul Bash call, mais préférer quand même les paths absolus pour cohérence.

**Pattern méta :** "side effect persistant entre tool calls" = bug latent. Toujours préférer commandes idempotentes (path explicite à chaque call).

**Cas connexe — diagnostic de structure (consolidé ici)** : un `cd` dans un sous-dossier (ex: `cd mcp-forge-brain && pytest`) fait taper les commandes relatives suivantes (`ls .claude/`, `git ls-files .claude/`, `find .claude`) dans `<sous-dossier>/.claude/` → faux constat alarmant « le dossier est vide / les fichiers ont disparu ». Incident 27 mai 2026 : cru pendant 4 tours que skills/agents/hooks avaient disparu, alors qu'ils étaient intacts à la racine. **Règle** : pour un diagnostic de structure, partir de `cd "$(git rev-parse --show-toplevel)"` ou chemin absolu. Si un constat est surprenant (« vide », « disparu », « 0 tracké »), vérifier `pwd` AVANT de conclure — un constat contre-intuitif = suspecter l'environnement (CWD/scope), pas les données. Cf [[verify-exhaustive-claims]].

Consolide depuis : [[feedback_cd_sous_dossier_fausse_chemins_relatifs]] (fusionné le 1er juin 2026 — même cause racine CWD persistant).
