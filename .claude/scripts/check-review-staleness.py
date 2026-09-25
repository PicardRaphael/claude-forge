#!/usr/bin/env python3
"""Verdicts humains perimes : un composant relu, puis modifie sans nouvelle relecture.

Usage :
    py .claude/scripts/check-review-staleness.py [chemin_repo]
    py .claude/scripts/check-review-staleness.py --list [chemin_repo]
    py .claude/scripts/check-review-staleness.py --stamp <cle|chemin> --verdict "<phrase>" [chemin_repo]

Exit : 0 = aucune revue perimee - 1 = au moins un verdict perime (chainable avant commit)

Piege couvert : `forge-review` et `skill-evolve` rendent un verdict argumente sur
un composant, puis le rapport part dans output/ et le composant continue de
bouger. Trois mois plus tard, rien ne distingue une skill relue et inchangee
d'une skill relue puis reecrite deux fois. Le verdict n'a pas ete infirme : il a
ete perdu de vue -- ce qui est pire, parce qu'il continue d'inspirer confiance.

Ce garde ne juge RIEN et ne score RIEN (c'est le role de skill-evolve). Il
constate qu'un corps a change depuis la date du verdict, et rend la relecture
explicite. Poser une empreinte est un geste HUMAIN (--stamp, verdict obligatoire),
jamais un effet de bord d'une autre commande : une empreinte posee toute seule
serait une auto-promotion deguisee.

Deux niveaux, volontairement asymetriques :
  - composant estampille dont le corps a change  -> FAIL (c'est le livrable) ;
  - composant jamais estampille                  -> compte, jamais bloquant.
Sans cette asymetrie le garde serait rouge des le premier jour sur 127
composants, donc ignore des le deuxieme.

Portee : surfaces de JUGEMENT (skills, agents, rules, contrats). Les hooks en
sont absents -- leur regression se voit aux tests, pas a la relecture. Les
`references/*.md` d'une skill aussi : elles suivent une documentation amont et
bougeraient a chaque rafraichissement.

L'empreinte couvre le fichier ENTIER, frontmatter compris : `description` decide
du routage et `model`/`effort` sont des choix arbitres, donc leur derive perime
le verdict autant que le corps. Aucune circularite : la revue vit dans un
sidecar, jamais dans le frontmatter.

Mais ce depot fait des sweeps de PARC -- effort a chaque changement de modele
(SWEEP-effort-opus5), descriptions en juillet. Un sweep d'`effort` perimerait
d'un coup tous les verdicts du parc, et « le composant a change » serait vrai et
inutile. Chaque alerte nomme donc la ZONE qui a bouge (frontmatter seul / corps
seul / les deux) : une vague de « frontmatter seul » se lit en une seconde comme
un sweep, pas comme N relectures. Sans cette colonne le garde crierait sur du
sweep, et un garde qui crie sur du formatage se fait ignorer.
"""
import argparse
import glob
import hashlib
import json
import os
import sys
from datetime import date

BASELINE = ".claude/scripts/review-baseline.json"

# (famille, glob, gabarit de cle) -- {dir} = dossier parent, {name} = nom de fichier.
_FAMILLES = (
    ("skills", ".claude/skills/*/SKILL.md", "{dir}"),
    ("agents", ".claude/agents/*.md", "{name}"),
    ("rules", ".claude/rules/*.md", "{name}"),
    ("skills-codex", ".agents/skills/*/SKILL.md", "{dir}"),
    ("agents-codex", ".codex/agents/*.md", "{name}"),
    ("contrat", "AGENTS.md", "{name}"),
    ("contrat", "CLAUDE.md", "{name}"),
)


def lire(path):
    try:
        return open(path, encoding="utf-8-sig").read()
    except OSError:
        return None


def empreinte(texte):
    """SHA-256 d'un texte normalise.

    Fins de ligne et blancs de fin de ligne sont neutralises : ce depot porte un
    `.gitattributes`, un historique de passage en LF, et `git diff --check` dans
    sa chaine de verification. Une empreinte sensible au CRLF divergerait entre
    deux postes sans qu'une seule ligne ait change de sens.
    """
    normalise = "\n".join(ligne.rstrip() for ligne in texte.splitlines())
    return "sha256:" + hashlib.sha256(normalise.encode("utf-8")).hexdigest()


def decouper(texte):
    """(frontmatter, corps). Sans frontmatter : ("", texte).

    Decoupage textuel, pas YAML : on compare des empreintes, pas des valeurs.
    Un fichier sans frontmatter (AGENTS.md, une rule nue) a donc tout son
    contenu dans le corps, ce qui est le comportement voulu.
    """
    if not texte.startswith("---"):
        return "", texte
    parts = texte.split("---", 2)
    if len(parts) < 3:
        return "", texte
    return parts[1], parts[2]


def empreintes(texte):
    """Les trois empreintes d'un composant : entiere, frontmatter, corps."""
    frontmatter, corps = decouper(texte)
    return {
        "empreinte": empreinte(texte),
        "empreinte_frontmatter": empreinte(frontmatter),
        "empreinte_corps": empreinte(corps),
    }


def zone_modifiee(ancien, courant):
    """Ou le composant a bouge depuis la relecture, en clair.

    Une baseline anterieure aux empreintes par zone ne peut pas repondre : elle
    le dit, plutot que de deviner.
    """
    if "empreinte_corps" not in ancien or "empreinte_frontmatter" not in ancien:
        return "zone inconnue (revue posee avant le decoupage par zone)"
    fm = ancien["empreinte_frontmatter"] != courant["empreinte_frontmatter"]
    corps = ancien["empreinte_corps"] != courant["empreinte_corps"]
    if fm and corps:
        return "frontmatter et corps"
    if fm:
        return "frontmatter seul"
    if corps:
        return "corps seul"
    return "blancs ou separateurs"


def inventaire(root):
    """{cle: chemin_relatif} des composants dont un verdict humain a du sens."""
    trouve = {}
    for famille, motif, gabarit in _FAMILLES:
        for path in sorted(glob.glob(os.path.join(root, motif))):
            nom = gabarit.format(
                dir=os.path.basename(os.path.dirname(path)),
                name=os.path.basename(path),
            )
            rel = os.path.relpath(path, root).replace("\\", "/")
            trouve[famille + ":" + nom] = rel
    return trouve


def charger_baseline(root):
    texte = lire(os.path.join(root, BASELINE))
    if texte is None:
        return {}
    try:
        data = json.loads(texte)
    except json.JSONDecodeError:
        return {}
    return data.get("revues", {}) if isinstance(data, dict) else {}


def ecrire_baseline(root, revues):
    chemin = os.path.join(root, BASELINE)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    contenu = {
        "_lisez_moi": (
            "Verdicts humains poses sur un composant, avec l'empreinte du fichier "
            "AU MOMENT de la relecture. Ne PAS re-estampiller pour faire taire une "
            "alerte : l'alerte dit que le composant a change depuis, donc que le "
            "verdict n'a pas ete rendu sur ce texte-la. Relire d'abord, estampiller "
            "ensuite, avec un verdict qui dit ce qui a ete verifie."
        ),
        "revues": {cle: revues[cle] for cle in sorted(revues)},
    }
    with open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(contenu, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return chemin


def resoudre(cible, composants):
    """Accepte une cle (skills:done) ou un chemin (.claude/skills/done/SKILL.md)."""
    if cible in composants:
        return cible
    # `lstrip("./")` mangerait le point de `.claude/` — c'est un jeu de
    # caracteres, pas un prefixe.
    normalise = cible.replace("\\", "/")
    while normalise.startswith("./"):
        normalise = normalise[2:]
    for cle, rel in composants.items():
        if rel == normalise:
            return cle
    return None


def poser(root, cible, verdict):
    composants = inventaire(root)
    cle = resoudre(cible, composants)
    if cle is None:
        print("[FAIL] composant inconnu : " + cible)
        print("       `--list` donne les cles disponibles.")
        return 1

    texte = lire(os.path.join(root, composants[cle]))
    if texte is None:
        print("[FAIL] illisible : " + composants[cle])
        return 1

    revues = charger_baseline(root)
    ancienne = revues.get(cle)
    entree = {"revue": date.today().isoformat(), "verdict": verdict}
    entree.update(empreintes(texte))
    revues[cle] = entree
    chemin = ecrire_baseline(root, revues)
    geste = "mise a jour" if ancienne else "posee"
    print("[OK] revue " + geste + " pour " + cle + " (" + os.path.relpath(chemin, root) + ")")
    if ancienne:
        print("     verdict precedent (" + ancienne.get("revue", "?") + ") : " + ancienne.get("verdict", ""))
    return 0


def lister(root):
    composants = inventaire(root)
    revues = charger_baseline(root)
    jamais = [cle for cle in composants if cle not in revues]
    for cle in sorted(revues):
        info = revues[cle]
        etat = "revue posee" if cle in composants else "absent du depot"
        print("  " + info.get("revue", "?") + "  " + cle + "  (" + etat + ")")
        print("      " + info.get("verdict", ""))
    if jamais:
        print("")
        print("  Jamais revus (" + str(len(jamais)) + ") :")
        for cle in sorted(jamais):
            print("      " + cle)
    return 0


def auditer(root):
    composants = inventaire(root)
    revues = charger_baseline(root)

    perimees, orphelines = [], []
    for cle in sorted(revues):
        info = revues[cle]
        rel = composants.get(cle)
        texte = lire(os.path.join(root, rel)) if rel else None
        if texte is None:
            orphelines.append(cle)
            continue
        courantes = empreintes(texte)
        if courantes["empreinte"] != info.get("empreinte"):
            perimees.append((cle, rel, info, courantes, zone_modifiee(info, courantes)))

    posees = len([cle for cle in revues if cle in composants])
    jamais = len(composants) - posees

    if orphelines:
        print("[MENAGE] " + str(len(orphelines)) + " revue(s) sans composant correspondant :")
        for cle in orphelines:
            print("  " + cle)
        print("  Le composant a ete renomme ou supprime - retirer l'entree de la baseline.")
        print("")

    if perimees:
        print("[FAIL] " + str(len(perimees)) + " verdict(s) perime(s) - le composant a change depuis la relecture :")
        zones = {}
        for cle, rel, info, courantes, zone in perimees:
            zones[zone] = zones.get(zone, 0) + 1
            print("  " + cle + "  (" + rel + ")  [" + zone + "]")
            print("      revu le " + info.get("revue", "?") + " : " + info.get("verdict", ""))
        print("")
        if zones.get("frontmatter seul", 0) > 2:
            print(
                "  " + str(zones["frontmatter seul"]) + " entrees ne bougent QUE du frontmatter : "
                "signature d'un sweep de parc\n  (effort, description, model). A relire en lot, "
                "pas une par une."
            )
            print("")
        print("Relire, PUIS estampiller :")
        print('  py .claude/scripts/check-review-staleness.py --stamp <cle> --verdict "<ce qui a ete verifie>"')
        return 1

    print(
        "[OK] " + str(len(composants)) + " composants, " + str(posees) + " revue(s) a jour, "
        + str(jamais) + " jamais revu(s) (non bloquant - `--list` pour les voir)"
    )
    return 0


def main():
    parser = argparse.ArgumentParser(description="Verdicts humains perimes.")
    parser.add_argument(
        "--list", action="store_true",
        help="lister les revues posees et les composants jamais revus",
    )
    parser.add_argument("--stamp", metavar="CLE", help="poser/mettre a jour la revue d'un composant")
    parser.add_argument("--verdict", metavar="PHRASE", help="ce qui a ete verifie (obligatoire avec --stamp)")
    parser.add_argument("root", nargs="?", default=".", help="racine du depot (defaut : .)")
    args = parser.parse_args()

    if args.stamp and not args.verdict:
        print("[FAIL] --stamp exige --verdict : une empreinte sans phrase de relecture")
        print("       serait une auto-promotion deguisee, pas une revue.")
        return 1
    if args.stamp:
        return poser(args.root, args.stamp, args.verdict)
    if args.list:
        return lister(args.root)
    return auditer(args.root)


if __name__ == "__main__":
    sys.exit(main())
