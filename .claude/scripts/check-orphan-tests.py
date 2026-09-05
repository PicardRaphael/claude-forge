#!/usr/bin/env python3
"""Detecte les tests INERTES : un test_*.py present qu'aucune commande
documentee ne collecte.

Usage : py .claude/scripts/check-orphan-tests.py [chemin_repo]
Exit  : 0 = tout est collecte  ·  1 = au moins un test inerte

Pattern mesure le 5 sept. 2026 : test_security_guard_adverse.py et
test_dispatchers.py vivaient a la RACINE de .claude/hooks/, hors du chemin
`pytest .claude/hooks/tests` documente dans AGENTS.md. Ils n'ont jamais tourne.
L'un d'eux affirmait que `git branch -d` etait legitime — l'exact inverse du
comportement livre par security-guard.py. La contradiction a survecu des mois
sans produire un seul signal. C'est le mode de defaillance qui rend ce garde
necessaire : un test qui ne tourne pas ne fait pas de bruit, il fabrique de la
confiance. Les jumeaux .codex/ portaient encore la meme dette ce jour-la.

Deux familles :
  1. FICHIER HORS SUITE — test_*.py qui n'est dans aucun dossier `tests/`
  2. SUITE JAMAIS LANCEE — dossier tests/ peuple mais absent des commandes
     pytest documentees

Source de verite des chemins lances : les lignes `pytest <chemin>` d'AGENTS.md.
Aucune liste en dur — declarer une suite dans AGENTS.md suffit a la rendre
vivante aux yeux de ce script, et c'est le meme geste qui la rend vivante pour
de vrai.
"""
import os
import sys

# Arborescences qui ne sont pas du code de ce repo : checkouts paralleles,
# dependances, caches, et plugins tiers dont on ne maintient pas les tests.
_SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "worktrees",
    "plugins",
    ".pytest_cache",
    ".ruff_cache",
}


def collected_roots(root):
    """Chemins passes a pytest dans AGENTS.md, ou None s'il est illisible.

    Deux garde-fous, parce qu'un faux chemin ici declare une suite vivante a
    tort et fabrique un faux negatif — le defaut meme que ce script traque :
      - seules les lignes DANS un bloc de code comptent (la prose qui cite
        `pytest <chemin>` en exemple n'est pas une invocation) ;
      - le chemin doit exister sur le disque.
    """
    try:
        text = open(os.path.join(root, "AGENTS.md"), encoding="utf-8-sig").read()
    except OSError:
        return None
    roots = set()
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code or "pytest" not in line:
            continue
        for token in line.split("pytest", 1)[1].split():
            if token.startswith("-"):
                continue  # flag (-q, -m) : le chemin vient apres
            cleaned = token.strip("`\"'").replace("\\", "/").rstrip("/")
            if cleaned and os.path.exists(os.path.join(root, cleaned)):
                roots.add(cleaned)
            break  # un seul chemin par invocation
    return roots


def iter_tests(root):
    """Tests du repo de configuration, hors sous-projets Python autonomes.

    Un dossier qui porte son propre pyproject.toml declare sa propre collecte
    (`[tool.pytest.ini_options]`) : ses tests ne relevent pas d'AGENTS.md, qui
    ne couvre que la surface de config. Sans cette frontiere, mcp-forge-brain et
    mcp-forge-cognition produisaient 32 faux positifs sur 34 — soit un outil
    qu'on apprend a ignorer, ce qui est pire que pas d'outil.
    """
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        if dirpath != root and "pyproject.toml" in filenames:
            dirnames[:] = []
            continue
        for name in filenames:
            if name.startswith("test_") and name.endswith(".py"):
                yield os.path.join(dirpath, name)


def classify(rel, collected):
    """None si le test est collecte, sinon la raison pour laquelle il est inerte."""
    segments = os.path.dirname(rel).split("/")
    if "tests" not in segments:  # n'importe ou dans l'arborescence, pas seulement le parent
        return "hors de tout dossier tests/"
    if collected is None:
        return None  # sans AGENTS.md on ne peut pas juger cette famille
    if any(rel == c or rel.startswith(c + "/") for c in collected):
        return None
    suite = "/".join(segments[: segments.index("tests") + 1])
    return f"suite {suite}/ absente des commandes pytest d'AGENTS.md"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    collected = collected_roots(root)
    if collected is None:
        print("[WARN] AGENTS.md illisible — seuls les tests hors dossier tests/ sont verifies")

    inert, total = [], 0
    for path in sorted(iter_tests(root)):
        total += 1
        rel = os.path.relpath(path, root).replace("\\", "/")
        reason = classify(rel, collected)
        if reason:
            inert.append((rel, reason))

    if not total:
        print("[SKIP] aucun test_*.py trouve — mauvais repo ? (fail-open)")
        return 0

    if inert:
        print(f"[FAIL] {len(inert)}/{total} test(s) jamais collecte(s) :")
        for rel, reason in inert:
            print(f"  {rel}\n      -> {reason}")
        print(
            "\nSoit deplacer le fichier dans une suite collectee (et le convertir en\n"
            "pytest : un script a boucle module-level casse la collecte a l'import),\n"
            "soit declarer sa suite dans AGENTS.md § Verification locale."
        )
        return 1

    suites = len(collected) if collected else 0
    print(f"[OK] {total} tests, tous collectes ({suites} suite(s) declaree(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
