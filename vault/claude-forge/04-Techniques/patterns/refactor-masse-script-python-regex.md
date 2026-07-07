---
titre: "Refactor en masse via script Python regex — alternative aux Edit séquentiels"
resume: "Quand un refactor identique touche 10+ fichiers avec un pattern textuel stable, un script Python ponctuel (regex + write atomique) remplace avantageusement les Edit séquentiels : 1 round-trip, atomique, idempotent, vérifiable par grep."
aliases:
  - "refactor masse script python"
  - "script python ponctuel refactor"
  - "edit séquentiels alternative"
  - "refactor regex batch fichiers"
  - "script tmp refactor"
  - "python regex multiline dotall"
derniere-maj: 2026-07-07
auteur: claude
type: pattern
tags:
  - "#domaine/claude-code"
  - "#type/pattern"
  - "#domaine/python"
  - "#pattern/refactor"
---

# Refactor en masse via script Python regex

## Seuil de déclenchement

Dès qu'un refactor concerne **> 10 fichiers** avec un pattern textuel **stable** (même bloc, mêmes marqueurs de début/fin) : remplacer les Edit séquentiels par un script Python ponctuel.

Si le pattern **varie** entre fichiers (cas particulier par fichier) → revenir aux Edit.

## Pourquoi

| Critère | Edit séquentiels | Script Python ponctuel |
|---------|-----------------|----------------------|
| Round-trips outil | N (1 Read + 1 Edit par fichier) | 1 (Write du script) + 1 (py script.py) |
| Risque d'erreur | Élevé (Read obligatoire avant chaque Edit) | Faible (regex compilée, write atomique) |
| Vérification | N greps | 1 grep post-exécution |
| Idempotence | Non (risque double-apply) | Oui (regex avec marqueurs clairs) |
| Nettoyage | Rien | Supprimer le script tmp |

## Pattern validé — ia_back 25 mai 2026

- 18 agents à refactor (13 blocs filet MCP + 5 blocs ESCALADE)
- Extraction de chaque bloc + remplacement par wikilink vers règle canonique
- 1 script Python (regex `re.MULTILINE|re.DOTALL` + `Path.write_text` atomique)
- 1 commande `py script.py` → **308 lignes économisées, 18 fichiers traités en < 5s**
- Vérif empirique post-exécution : 1 `grep -c` sur les fichiers cibles
- Commit `fdeee72` pushed, 0 régression

Contexte complet : [[audit-ia-back-25mai-quartet]] § "Refactor SSOT bonus".

## Comment appliquer

```python
# Pattern type — script tmp à placer dans .claude/tmp-refactor-<slug>.py
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent  # racine repo

# Regex à adapter selon le bloc à extraire
PATTERN = re.compile(
    r"<!-- BEGIN BLOC -->.+?<!-- END BLOC -->",
    re.MULTILINE | re.DOTALL
)
REPLACEMENT = "[[nom-de-la-rule-canonique]]"

files = list(ROOT.glob(".claude/agents/*.md"))
changed = 0
for f in files:
    content = f.read_text(encoding="utf-8")
    new_content, n = PATTERN.subn(REPLACEMENT, content)
    if n:
        f.write_text(new_content, encoding="utf-8", newline="\n")  # LF strict
        changed += 1

print(f"{changed}/{len(files)} fichiers modifiés")
```

**Points critiques :**
- `newline="\n"` obligatoire sur Windows (sinon `write_text` traduit LF→CRLF sur 100% des fichiers — [[gate-zero-diff-test-live-byte-exact]])
- `re.MULTILINE | re.DOTALL` : MULTILINE pour `^`/`$` ligne, DOTALL pour `.` qui traverse les sauts de ligne
- `Path.write_text` atomique (OS-level) — pas de fichier partiellement écrit

## Vérification post-exécution

```bash
# Vérif positive : le remplacement est présent
grep -c "[[nom-de-la-rule-canonique]]" .claude/agents/*.md

# Vérif négative : l'ancien bloc est absent
grep -c "BEGIN BLOC" .claude/agents/*.md  # doit retourner 0
```

## Nettoyage obligatoire

Supprimer le script tmp après exécution :
```bash
rm .claude/tmp-refactor-*.py
```

Convention de nommage : `.claude/tmp-refactor-<slug>.py` (visible, hors `.gitignore` standard, facile à retrouver si oublié).

## Cas d'usage validés

| Cas | Pattern stable ? | Script ou Edit ? |
|-----|-----------------|-----------------|
| Extraction bloc répété → wikilink | Oui | Script |
| Normalisation frontmatter (champ manquant) | Oui | Script |
| Port stack OLD → NEW (import, call) | Oui si syntaxe uniforme | Script |
| Fix slug → résumé (112 notes) | Oui | Script (log.md 2026-07) |
| Fix adapté fichier par fichier | Non | Edit |

## Gotchas

- **Windows CRLF** : `write_text` sans `newline=""` ou `newline="\n"` corrompt les fichiers LF du vault — cf [[gate-zero-diff-test-live-byte-exact]]
- **Script tmp oublié** : convenir `.claude/tmp-refactor-*.py` + supprimer après exécution
- **Regex trop large** : toujours tester `PATTERN.findall()` sur 1 fichier avant `.subn()` sur tous
- **Chemin Python Windows** : lancer avec `py script.py` (PEP 514 launcher), jamais `python` (peut pointer vers Microsoft Store alias)

## Wikilinks

- [[audit-ia-back-25mai-quartet]] — cas fondateur (18 agents, 308L, commit fdeee72)
- [[gate-zero-diff-test-live-byte-exact]] — write_text CRLF vs LF
- [[python-windows-tmp-msys-invisible]] — chemins /tmp invisibles depuis Python natif Windows
- [[quartet-analyse-multi-repo]] — contexte pattern audit qui déclenche ce type de refactor
