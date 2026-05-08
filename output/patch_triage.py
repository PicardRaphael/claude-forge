# -*- coding: utf-8 -*-
"""Patch triage-tickets SKILL.md - feedback devs: action-first format + Bug-Donnee vs Bug-Code."""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL = r'C:\Users\raphael.picard_neote\Documents\claude-forge\output\support-lojii-plugin\skills\triage-tickets\SKILL.md'
s = open(SKILL, encoding='utf-8').read()
print(f"Original lines: {s.count(chr(10))}")

# We use chr(39) for straight apostrophe (U+0027) to avoid curly-quote contamination from editors

apos = chr(39)  # U+0027 straight apostrophe

# ---- CHANGE 1: Classification section - add Bug sub-types after Bug paragraph ----
# Anchor on unique phrase that has no apostrophes
ANCHOR1 = 'Si non = Bug potentiel.\n\n**Support**'
assert s.count(ANCHOR1) == 1, f"ANCHOR1 count: {s.count(ANCHOR1)}"
INSERT1 = (
    'Si non = Bug potentiel.\n\n'
    '**Quand Bug identifié, toujours trancher entre les deux sous-types :**\n\n'
    '- **Bug-Donnée** : le programme fonctionne correctement mais les données en base sont incorrectes, '
    'manquantes ou incohérentes. Le message d' + apos + 'erreur ou le comportement anormal est causé par un '
    'état de donnée invalide, pas par un défaut de code. '
    '→ **Le support peut traiter** (Service Request / Intervention BDD). Pas de N2 dev.\n'
    '- **Bug-Code** : le programme lui-même a un défaut (logique incorrecte, cas non géré, '
    'régression). Le problème se reproduirait même avec des données correctes. '
    '→ **N2 dev** avec le programme exact, la ligne, et le fix proposé.\n\n'
    '**Règle de décision** : quand Claude identifie le programme source du problème, '
    'vérifier d' + apos + 'abord si les données en entrée sont correctes. '
    'Si données incorrectes → Bug-Donnée. '
    'Si données correctes et le programme produit un mauvais résultat → Bug-Code.\n\n'
    '**Support**'
)
s = s.replace(ANCHOR1, INSERT1, 1)
print("Change 1 OK")

# ---- CHANGE 2: New gotcha - Bug-Donnee vs Bug-Code ----
# Anchor: unique ending phrase of createIssueLink gotcha
ANCHOR2 = 'Mentionner le N2 dans la note interne avec l' + apos + 'URL nue.'
assert s.count(ANCHOR2) == 1, f"ANCHOR2 count: {s.count(ANCHOR2)}"
REPLACE2 = (
    'Mentionner le N2 dans la note interne avec l' + apos + 'URL nue.\n'
    '- **Bug-Donnée vs Bug-Code — TOUJOURS trancher** — quand le programme source est identifié, '
    'vérifier d' + apos + 'abord si les données en entrée sont correctes. '
    'Donnée incorrecte en base = Bug-Donnée (support traite, pas de N2). '
    'Code défectueux avec données correctes = Bug-Code (N2 dev). '
    'La majorité des “bugs” sont des problèmes de données, pas de code.'
)
s = s.replace(ANCHOR2, REPLACE2, 1)
print("Change 2 OK")

# ---- CHANGE 3: Replace note interne format template ----
# Use unique intro line as start anchor, unique end phrase as end anchor
START3 = 'Format de la note interne — titres en gras Unicode, séparateurs entre sections, URLs nues uniquement :\n```\n'
END3 = 'Aucune note vault sur ce sujet (après 2+ recherches avec termes alternatifs).]\n```'
idx_s = s.find(START3)
idx_e = s.find(END3)
assert idx_s != -1, "START3 not found"
assert idx_e != -1, "END3 not found"
idx_e += len(END3)
old3 = s[idx_s:idx_e]
assert s.count(old3) == 1, f"old3 count: {s.count(old3)}"

# The new format - using the EXACT unicode bold characters from the user spec
new3 = (
    'Format de la note interne — entonnoir : action d' + apos + 'abord, analyse en dessous. '
    'Titres en gras Unicode, séparateurs entre sections, URLs nues uniquement :\n'
    '```\n'
    '⚡ \U0001d5c0̀ \U0001d5d9\U0001d5d4\U0001d5dc\U0001d5db\U0001d5d8 : '
    '[1 phrase — l' + apos + 'action concrète que le support doit faire]\n\n'
    '[Bug-Donnée] → Corriger la donnée : [table, champ, valeur attendue]\n'
    '[Bug-Code] → N2 dev : [programme], [ligne/fonction], [ce qui ne va pas]\n'
    '[Support] → Répondre au client : [résumé de la réponse]\n'
    '[SR] → Intervention : [action à réaliser]\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '⚫ \U0001d402\U0001d405\U0001d41a\U0001d42c\U0001d42c\U0001d422\U0001d41f\U0001d422\U0001d41c\U0001d41a\U0001d42d\U0001d422\U0001d428\U0001d427 : '
    '[Bug-Donnée / Bug-Code / Support / SR]\n\n'
    'Symptôme : [description courte du problème]\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '\U0001f50d \U0001d400\U0001d427\U0001d41a\U0001d425\U0001d432\U0001d42c\U0001d41e\n\n'
    'Programme identifié : [nom du programme/fonction PG si trouvé]\n'
    'Cause : [donnée incorrecte en base / défaut de code / méconnaissance client]\n'
    'Données vérifiées : [ce qui a été vérifié dans LOJII/BDD]\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '\U0001f7e0 \U0001d5d5\U0001d5f2\U0001d5ff\U0001d5f6\U0001d5f3\U0001d5f6\U0001d5f0\U0001d5ee\U0001d601\U0001d5f6\U0001d5fc\U0001d5fb\U0001d5f2\n\n'
    '1. [étape concrète]\n'
    '2. [étape concrète]\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '\U0001f517 \U0001d5e7\U0001d5f6\U0001d5f0\U0001d5f8\U0001d5f2\U0001d601\U0001d5f2\U0001d5f4 '
    '\U0001d5f4\U0001d5f6\U0001d5fa\U0001d5f6\U0001d5f3\U0001d5ee\U0001d5f6\U0001d5ff\U0001d5f2\U0001d5f4\n\n'
    '[SC/N2-XXXXX ou “Aucun”]\n'
    'https://neoteem.atlassian.net/browse/XX-XXXXX\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '\U0001f4ac \U0001d5e5\U0001d5f2\U0001d5ff\U0001d5f2\U0001d5fd\U0001d5fc\U0001d5fb\U0001d5f4\U0001d5f2 '
    '\U0001d5f0\U0001d5f3\U0001d5f6\U0001d5f2\U0001d5fb\U0001d601\n\n'
    'Bonjour,\n'
    '[texte concis, vouvoiement]\n'
    'Bien à vous,\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '⚙ \U0001d400\U0001d5f0\U0001d601\U0001d5f6\U0001d5fc\U0001d5fb\U0001d5f4\U0001d5f4 '
    '\U0001d5f2\U0001d5f3\U0001d5f3\U0001d5f2\U0001d5f0\U0001d601\U0001d602\U0001d5f2\U0001d5f4\n\n'
    'Type → [Bug-Donnée / Bug-Code / Support / SR] – Composant → [nom] – Priorité → [niveau]\n\n'
    '━━━━━━━━━━━━━━━'
    '━━━━━━━━━━━━━━━\n\n'
    '\U0001f9e0 \U0001d5e9\U0001d5ee\U0001d602\U0001d5f3\U0001d601\n\n'
    '[Notes utilisées ou “Aucune note vault”]\n'
    '```'
)
s = s.replace(old3, new3, 1)
print("Change 3 OK")

# ---- CHANGE 4: Update Regles de mise en page - add entonnoir rule, fix response client ref ----
# Anchor on unique phrase without apostrophes
ANCHOR4_START = '**Règles de mise en page des notes internes :**\n- Titres en **gras Unicode'
ANCHOR4_END = 'texte concis entre les deux.'
idx_s4 = s.find(ANCHOR4_START)
idx_e4 = s.find(ANCHOR4_END, idx_s4)
assert idx_s4 != -1, "ANCHOR4_START not found"
assert idx_e4 != -1, "ANCHOR4_END not found"
idx_e4 += len(ANCHOR4_END)
old4 = s[idx_s4:idx_e4]
assert s.count(old4) == 1, f"old4 count: {s.count(old4)}"

new4 = (
    '**Règles de mise en page des notes internes :**\n'
    '- **Entonnoir obligatoire** — la première section ⚡ À FAIRE contient l' + apos + 'action en 1 phrase. '
    'L' + apos + 'analyse (cause, vérifications, vault) vient après. Le support lit l' + apos + 'action d' + apos + 'abord, les détails si nécessaire.\n'
    '- Titres en **gras Unicode mathématique** (\U0001d5d4\U0001d5d5\U0001d5d6) — Jira affiche ces caractères en gras sans formatage wiki. '
    'Utiliser la table de conversion : A→\U0001d5d4, B→\U0001d5d5, C→\U0001d5d6, etc. '
    'Les accents fonctionnent dans le texte normal mais PAS dans les caractères gras Unicode.\n'
    '- **Séparateurs** ━━━ (U+2501 BOX DRAWINGS HEAVY HORIZONTAL) entre chaque section — 30 caractères par ligne.\n'
    '- **Emojis** en début de chaque titre de section.\n'
    '- **Sauts de ligne** : une ligne vide après chaque titre, une ligne vide avant chaque séparateur.\n'
    '- **Pas de formatage wiki/markdown** — pas de `*gras*`, `_italique_`, `+souligné+`. Jira Service Desk les ignore dans les notes internes.\n'
    '- La section \U0001f4ac Réponse client doit toujours commencer par “Bonjour,” et finir par “Bien à vous,” — '
    'texte concis entre les deux.'
)
s = s.replace(old4, new4, 1)
print("Change 4 OK")

# ---- CHANGE 5: Update batch summary repartition ----
OLD5 = '\U0001f4ca Répartition :\n- Bugs : [N]\n- Support : [N]\n- Service Requests : [N]'
NEW5 = '\U0001f4ca Répartition :\n- Bug-Donnée : [N] (support traite)\n- Bug-Code : [N] (N2 dev)\n- Support : [N]\n- Service Requests : [N]'
assert s.count(OLD5) == 1, f"Change 5 count: {s.count(OLD5)}"
s = s.replace(OLD5, NEW5, 1)
print("Change 5 OK")

open(SKILL, 'w', encoding='utf-8').write(s)
final_lines = len(open(SKILL, encoding='utf-8').readlines())
print(f"Final line count: {final_lines}")
assert final_lines < 500, f"OVER 500 LINES: {final_lines}"
print("ALL CHANGES APPLIED SUCCESSFULLY.")
