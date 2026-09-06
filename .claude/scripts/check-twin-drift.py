#!/usr/bin/env python3
"""Detecte les corrections appliquees a une surface et oubliees sur sa jumelle.

Usage : py .claude/scripts/check-twin-drift.py [chemin_repo]
        py .claude/scripts/check-twin-drift.py --update-baseline [chemin_repo]
Exit  : 0 = aucune divergence nouvelle  ·  1 = au moins une

Pattern mesure les 5 et 6 sept. 2026 : TROIS propagations Codex manquees en
24 h — deux tests rapatries cote .claude et laisses orphelins cote .codex, un
check-frontmatter dont le perimetre s'arretait a .claude, un libelle de
security-guard corrige d'un seul cote. A chaque fois la surface Claude etait
juste, la jumelle en retard, et rien ne le signalait. `cross-repo-propagation`
couvre les repos externes ; le jumeau interne n'avait aucun garde.

CE QUI EST COMPARE, ET POURQUOI PAS LE TEXTE
Ces surfaces sont des ADAPTATEURS : elles doivent differer. Un diff brut est
donc inutilisable — security-guard.py affiche 24 lignes d'ecart alors que ses
trois libelles sont alignes, l'ecart etant du formatage (regex sur une ligne
cote Codex, sur plusieurs cote Claude). On compare donc des FAITS :
  - fichiers Python  -> les messages (litteraux de 12 a 90 caracteres sans
    antislash). Les regex sont volontairement exclues : coupees en morceaux par
    le formatage, elles produisent des ecarts fantomes. Un vrai ecart de regex
    se voit dans les suites de tests, pas ici.
  - fichiers Markdown -> les champs de frontmatter a semantique partagee
    (model, effort…), et seulement quand les DEUX cotes les declarent. Un champ
    absent d'un cote est une adaptation, pas une derive.
  - presence -> un composant qui n'existe que d'un cote.

RATCHET. Les divergences legitimes sont figees dans twin-drift-baseline.json ;
seules les NOUVELLES sont signalees. Meme principe que les gates poses sur du
legacy : on mesure l'existant, on empeche l'aggravation. Accepter une nouvelle
divergence est un geste explicite (--update-baseline), jamais un silence.
"""
import glob
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

BASELINE = ".claude/scripts/twin-drift-baseline.json"

# Un adaptateur qui execute le fichier de l'autre surface n'a qu'UNE source :
# aucune derive n'y est possible, et le comparer produirait un ecart permanent.
_PARTAGE = re.compile(r"exec\(\s*compile\(")

# Messages : assez longs pour porter du sens, sans antislash (cf docstring).
_MESSAGE = re.compile(r'"([^"\\\n]{12,90})"')

# Champs dont la valeur signifie la meme chose des deux cotes. `description` et
# `allowed-tools` sont exclus : l'un est adapte a la plateforme, l'autre nomme
# des outils qui n'existent pas des deux cotes.
_CHAMPS = ("model", "effort", "user-invocable", "disable-model-invocation")

# (famille, glob cote Claude, gabarit du jumeau) — {name} = nom de fichier,
# {dir} = nom du dossier parent.
_FAMILLES = (
    ("hooks", ".claude/hooks/*.py", ".codex/hooks/{name}"),
    ("agents", ".claude/agents/*.md", ".codex/agents/{name}"),
    ("skills", ".claude/skills/*/SKILL.md", ".agents/skills/{dir}/SKILL.md"),
    # Sens inverse : un composant cree cote Codex et jamais porte cote Claude.
    ("hooks-codex", ".codex/hooks/*.py", ".claude/hooks/{name}"),
    ("agents-codex", ".codex/agents/*.md", ".claude/agents/{name}"),
    ("skills-codex", ".agents/skills/*/SKILL.md", ".claude/skills/{dir}/SKILL.md"),
)


def lire(path):
    try:
        return open(path, encoding="utf-8-sig").read()
    except OSError:
        return None


def frontmatter(texte):
    if yaml is None or not texte.startswith("---"):
        return {}
    parts = texte.split("---")
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def ecarts(chemin_a, texte_a, texte_b):
    """Faits presents d'un seul cote. Liste vide = les deux surfaces s'accordent."""
    if _PARTAGE.search(texte_b) or _PARTAGE.search(texte_a):
        return []  # source unique : rien a comparer

    if chemin_a.endswith(".py"):
        a, b = set(_MESSAGE.findall(texte_a)), set(_MESSAGE.findall(texte_b))
        return [f"message d'un seul cote : {m}" for m in sorted(a ^ b)]

    fa, fb = frontmatter(texte_a), frontmatter(texte_b)
    return [
        f"{champ} : {fa[champ]!r} d'un cote, {fb[champ]!r} de l'autre"
        for champ in _CHAMPS
        if champ in fa and champ in fb and fa[champ] != fb[champ]
    ]


def analyser(root):
    """{cle de paire: [ecarts]} — une paire sans ecart n'apparait pas."""
    trouve = {}
    for famille, motif, gabarit in _FAMILLES:
        for chemin_a in sorted(glob.glob(os.path.join(root, motif))):
            rel = os.path.relpath(chemin_a, root).replace("\\", "/")
            nom = os.path.basename(rel)
            dossier = os.path.basename(os.path.dirname(rel))
            jumeau = gabarit.format(name=nom, dir=dossier)
            cle = f"{famille}:{dossier if nom == 'SKILL.md' else nom}"

            chemin_b = os.path.join(root, jumeau)
            if not os.path.exists(chemin_b):
                trouve[cle] = [f"sans jumeau : {jumeau} n'existe pas"]
                continue
            # Le sens inverse ne sert qu'a reperer les absences : comparer le
            # contenu deux fois signalerait chaque ecart en double.
            if famille.endswith("-codex"):
                continue
            texte_a, texte_b = lire(chemin_a), lire(chemin_b)
            if texte_a is None or texte_b is None:
                continue
            liste = ecarts(rel, texte_a, texte_b)
            if liste:
                trouve[cle] = liste
    return trouve


def charger_baseline(root):
    texte = lire(os.path.join(root, BASELINE))
    if texte is None:
        return {}
    try:
        data = json.loads(texte)
    except json.JSONDecodeError:
        return {}
    return data.get("acceptees", {}) if isinstance(data, dict) else {}


def ecrire_baseline(root, trouve):
    chemin = os.path.join(root, BASELINE)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    contenu = {
        "_lisez_moi": (
            "Divergences jumelles acceptees. Ne PAS regenerer pour faire taire "
            "un ecart : verifier d'abord que la surface en retard n'attend pas "
            "une correction. Regenerer avec --update-baseline."
        ),
        "acceptees": {cle: sorted(v) for cle, v in sorted(trouve.items())},
    }
    with open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(contenu, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return chemin


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    maj = "--update-baseline" in sys.argv[1:]
    root = args[0] if args else "."

    if not os.path.isdir(os.path.join(root, ".claude")):
        print("[SKIP] pas de .claude/ — mauvais repo ? (fail-open)")
        return 0

    trouve = analyser(root)

    if maj:
        chemin = ecrire_baseline(root, trouve)
        total = sum(len(v) for v in trouve.values())
        print(f"[BASELINE] {total} divergence(s) sur {len(trouve)} paire(s) figee(s) dans {BASELINE}")
        print(f"           {chemin}")
        return 0

    acceptees = charger_baseline(root)
    nouvelles = {}
    for cle, liste in trouve.items():
        connues = set(acceptees.get(cle, []))
        reste = [e for e in liste if e not in connues]
        if reste:
            nouvelles[cle] = reste

    if not nouvelles:
        figees = sum(len(v) for v in acceptees.values())
        print(f"[OK] jumeaux alignes ({figees} divergence(s) acceptee(s) en baseline)")
        return 0

    total = sum(len(v) for v in nouvelles.values())
    print(f"[FAIL] {total} divergence(s) nouvelle(s) sur {len(nouvelles)} paire(s) :")
    for cle, liste in sorted(nouvelles.items()):
        print(f"  {cle}")
        for e in liste:
            print(f"      -> {e}")
    print(
        "\nUne correction appliquee d'un seul cote ? La porter sur la jumelle.\n"
        "Divergence voulue ? py .claude/scripts/check-twin-drift.py --update-baseline"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
