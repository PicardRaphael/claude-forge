# Cross-pollination patterns — skill-evolve

Patterns identifies dans les skills forge qui ont de la valeur et peuvent etre transferes.
Ce fichier grandit a chaque analyse skill-evolve.

---

## Pattern : Fallback vault (CLI -> Glob)

**Skill de reference :** `forge-brain`, `vault-audit`

**Description :**
Avant d'utiliser Obsidian CLI, faire un pre-check. Si CLI indisponible, basculer vers Glob/Read directement sur les fichiers vault.

**Implementation type :**
```
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null
# si echec -> Glob sur vault/claude-forge/04-Techniques/ et Knowledge/erreurs/
```

**Applicable a :** Toute skill qui interroge le vault.

---

## Pattern : Validation $ARGUMENTS avec bail immediat

**Skill de reference :** `evolve`, `skill-evolve`

**Description :**
Verifier que $ARGUMENTS est fourni ET valide avant de commencer. Afficher le message d'usage et stopper proprement. Ne pas analyser un default silencieux.

**Implementation type :**
```
Si $ARGUMENTS absent ou invalide :
  afficher "Usage : /skill-name <arg>"
  Ne pas continuer.
```

**Applicable a :** Toute skill avec argument obligatoire.

---

## Pattern : Sections "Ce qui est bien" et "Ce qui a ete ecarte"

**Skill de reference :** `evolve`, `skill-evolve`

**Description :**
Un rapport de recommandations n'est credible que si il inclut :
1. Ce qui merite d'etre preserve (ne pas tout changer)
2. Ce qui a ete conscieusement ecarte (la selection est intentionnelle)

**Applicable a :** Toute skill qui produit des recommandations ou propositions.

---

## Pattern : Scripts Python pour validations deterministes

**Skill de reference :** `vault-audit`

**Description :**
Les validations critiques (format, structure, coherence) s'expriment mieux en code qu'en instructions naturelles. Le code est deterministe, le langage naturel ne l'est pas.

**Implementation type :**
```python
# scripts/check-skill-structure.py
import os, sys
skill_dir = sys.argv[1]
issues = []
if not os.path.exists(f"{skill_dir}/SKILL.md"):
    issues.append("SKILL.md manquant")
# etc.
```

**Applicable a :** Skills qui font des audits ou des validations structurelles.

---

## Pattern : Git log pour indicateur de stabilite

**Skill de reference :** `skill-evolve`

**Description :**
Le nombre de commits sur un fichier est un proxy de stabilite. Utiliser `git log --oneline -- <fichier> | wc -l` comme signal supplementaire.

**Applicable a :** Skills qui analysent des composants forge.

---

## Pattern : Format tableau pour sweep multi-items

**Skill de reference :** `skill-evolve`

**Description :**
Quand on analyse N items de la meme nature, un tableau est plus lisible qu'une liste de sections. Colonnes typiques : nom, score, signal principal.

**Applicable a :** Skills qui produisent une synthese sur plusieurs elements homogenes.

---

## Pattern : Pre-check outil externe + comportement degrade

**Skill de reference :** `forge-brain`, `obsidian-cli`, `skill-evolve`

**Description :**
Avant d'utiliser un outil externe (CLI, MCP, API), verifier qu'il est disponible. Definir un comportement de repli explicite si indisponible.

**Implementation type :**
```
# Verifier disponibilite
bash <outil> version 2>/dev/null
# si exit 127 ou erreur : [comportement degrade explicite]
```

**Applicable a :** Toute skill dependant d'un outil externe.

---

## Pattern : Section Apprentissage non vide

**Skill de reference :** `evolve`, toutes les skills metier

**Description :**
La section Apprentissage ne devrait pas rester vide indefiniment. Apres 2-3 usages significatifs, capitaliser les patterns observes.

**Signal d'evolution :** La section Apprentissage est vide depuis > 5 sessions d'une skill active.

**Applicable a :** Toutes les skills metier.

---

## Ajouter un nouveau pattern

Format :
```
## Pattern : [Nom court]

**Skill de reference :** `nom-skill`

**Description :** ...

**Implementation type :** (optionnel, si non evident)

**Applicable a :** ...
```
