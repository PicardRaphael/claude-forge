#!/usr/bin/env python3
"""Detecte les references mortes de ROUTAGE : un texte dit d'invoquer un
agent/skill qui n'existe pas.

Usage : py .claude/scripts/check-refs.py [chemin_repo]
Exit  : 0 = aucune ref morte  ·  1 = au moins une (chainable avant un commit)

Pattern mesure le 29 juil. 2026 : 3 agents fantomes cites comme exemples
canoniques dans le CLAUDE.md de forge, 4 renvois a un agent `architect`
inexistant dans neo_ia. Aucun ne levait d'erreur — le routage echouait
silencieusement au moment de l'invocation.

PORTEE VOLONTAIREMENT ETROITE. On ne signale QUE les citations posees dans un
contexte de routage explicite : "agent `x`", "skill `y`", "invoquer `z`",
"Skill(z)", "subagent_type=z". Un nom en backticks hors de ce contexte peut
etre une note vault, un hook, un paquet npm, un repo, un champ de config — les
signaler tous produisait 108 faux positifs, donc un outil qu'on ignore.

Le silence de ce script ne prouve pas l'absence de toute ref morte : il prouve
qu'aucun ROUTAGE ne pointe vers le vide. C'est le sous-ensemble qui casse.
"""
import glob
import os
import re
import sys

# Contextes de routage : le nom capture est cense etre un agent ou une skill.
_ROUTING = (
    re.compile(r"(?:agents?|sous-agents?|subagents?)\s+`([a-z][a-z0-9-]{2,40})`", re.I),
    re.compile(r"(?:skills?|compétences?)\s+`([a-z][a-z0-9-]{2,40})`", re.I),
    re.compile(r"(?:invoquer|invoke|dispatcher|déléguer|appeler)\s+`([a-z][a-z0-9-]{2,40})`", re.I),
    re.compile(r"Skill\(\s*([a-z][a-z0-9-]{2,40})\s*[,)]"),
    re.compile(r"subagent_type\s*=\s*[\"']?([a-z][a-z0-9-]{2,40})"),
)

# Volontairement PAS de pattern sur `/xxx` : les slash commands built-in de
# Claude Code (/commit, /debug, /config, /theme, /context…) ne sont pas des
# composants du repo, et les routes d'API REST (/health, /documents) matchent
# aussi. Testé le 29 juil. 2026 : ce pattern seul produisait 22 faux positifs
# sur 25. Une skill user-invocable est de toute façon captée par les autres
# patterns quand un texte dit d'« invoquer » ou de router vers elle.

# Mots qui suivent "agent"/"skill" sans etre un nom de composant.
_STOPWORDS = {
    "creator", "creators", "createur", "createurs", "creatrice", "creatrices",
    "specialise", "specialises", "specialiste", "specialistes", "dedie",
    "read-only", "readonly", "general-purpose", "sub-agent", "sub-agents",
    "nom", "name", "type", "x", "y", "z", "xxx", "nnn",
    "clear", "compact", "doctor", "checkup", "model", "help", "init",
    "review", "code-review", "security-review", "verify", "btw", "loop",
    "schedule", "batch", "simplify", "voice", "agents", "skills", "run",
    # Outils Claude Code et CLI externes, cites avec un verbe d'appel
    "askuserquestion", "webfetch", "websearch", "toolsearch", "sendmessage",
    "notebookedit", "exitplanmode", "enterplanmode", "obsidian", "defuddle",
    "ffmpeg", "yt-dlp", "gh", "jq", "ruff", "mypy", "pytest", "biome", "knip",
    # Agents APPLICATIFS du produit (documentes, pas des composants CC a invoquer)
    "support", "neochat", "neodoc", "neomail", "neoagent", "neosupport",
}

# Une phrase qui NIE ou PROJETTE l'appel ne route pas vers un composant
# existant : « tu ne peux PAS appeler `X` », « créer une skill `Y` au premier
# conflit ». Testé le 29 juil. 2026 : sans ce filtre, 5 hits sur 6 etaient des
# faux positifs de ce type.
_NEGATED = re.compile(
    r"\b(?:pas|jamais|ne\s+peux|impossible|interdit|éviter|eviter|"
    r"créer|creer|create|futur|si\s+besoin|au\s+premier|n'existe)\b",
    re.I,
)


def inventory(root):
    """Noms de composants reellement presents (projet + user-scope + plugins)."""
    names = set()
    home = os.path.expanduser("~")
    scopes = [root, home]
    patterns = (
        ".claude/agents/*.md",
        ".claude/skills/*/SKILL.md",
        ".claude/commands/*.md",
        ".claude/plugins/*/*/skills/*/SKILL.md",
        ".claude/plugins/*/*/*/skills/*/SKILL.md",
        ".claude/plugins/cache/*/*/*/skills/*/SKILL.md",
        ".claude/plugins/marketplaces/*/*/skills/*/SKILL.md",
        ".agents/skills/*/SKILL.md",
    )
    for scope in scopes:
        for pattern in patterns:
            for path in glob.glob(os.path.join(scope, pattern)):
                if os.path.basename(path) == "SKILL.md":
                    names.add(os.path.basename(os.path.dirname(path)).lower())
                else:
                    names.add(os.path.splitext(os.path.basename(path))[0].lower())
    return names


_TEXT_GLOBS = (
    "CLAUDE.md",
    ".claude/rules/*.md",
    ".claude/agents/*.md",
    ".claude/skills/*/SKILL.md",
)


def scan(root, existing):
    hits = []
    for pattern in _TEXT_GLOBS:
        for path in glob.glob(os.path.join(root, pattern)):
            try:
                lines = open(path, encoding="utf-8-sig").read().splitlines()
            except OSError:
                continue
            for num, line in enumerate(lines, 1):
                if _NEGATED.search(line):
                    continue
                for rx in _ROUTING:
                    for token in rx.findall(line):
                        name = token.lower()
                        if name in _STOPWORDS or name in existing:
                            continue
                        hits.append((os.path.relpath(path, root), num, token))
    return hits


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    existing = inventory(root)
    if not existing:
        print("[SKIP] aucun agent/skill trouve — mauvais repo ? (fail-open)")
        return 0

    hits = scan(root, existing)
    if not hits:
        print(f"[OK] aucun routage mort ({len(existing)} composants connus)")
        return 0

    by_name = {}
    for path, num, token in hits:
        by_name.setdefault(token, []).append(f"{path}:{num}")

    print(f"[FAIL] {len(by_name)} nom(s) route(s) mais introuvable(s) :")
    for token, places in sorted(by_name.items()):
        print(f"  `{token}` -> {len(places)} citation(s)")
        for place in places[:6]:
            print(f"      {place}")
        if len(places) > 6:
            print(f"      … et {len(places) - 6} autre(s)")
    print(
        "\nSoit le composant a ete renomme/supprime (corriger le texte),\n"
        "soit ce n'est pas un routage (ajouter le mot a _STOPWORDS)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
