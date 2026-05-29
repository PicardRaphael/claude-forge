#!/usr/bin/env python3
"""Répare les wikilinks morts [[feedback_purgé]] dans les feedbacks survivants,
en les redirigeant vers la note vault qui a absorbé le feedback purgé (ou le survivant de fusion)."""
from pathlib import Path
import re

MEM = Path(r"C:\Users\raphael.picard_neote\Documents\claude-forge\memory")

# slug purgé -> cible de redirection (note vault canonique, ou feedback survivant pour fusions)
REDIR = {
    "feedback_advisor_da_mandatory": "workflow-claude-code-optimal",
    "feedback_arxiv_id_yymm_format": "erreur-audit-rag-11-faux-2026-05-23",
    "feedback_bras_droit": "feedback_jarvis_innovator",   # fusion: survivant
    "feedback_capitalisation_proposee_pas_auto": "comment-creer-skill",
    "feedback_gotchas_line_numbers_verifies": "erreur-gotchas-line-numbers-non-verifies-claudemd",
    "feedback_hook_scope_per_repo_mandatory": "critique-2026-05-24-regex-source-faux-positifs",
    "feedback_kill_pragmatique_vide_doctrinal": "pattern-mcp-brief-then-direct",
    "feedback_secret_in_mcp_json": "erreur-password-postgres-clair-mcp-json",
    "feedback_session_consulte_vault_avant_brief": "erreur-vault-jamais-consulte-session-principale",
    "feedback_tests_adverses_obligatoires": "tests-adverses-hooks-secu",   # fusion: survivant (par name)
    "feedback_tests_adverses_ratio_3_1": "tests-adverses-hooks-secu",       # fusion: survivant (par name)
}

total = 0
for f in sorted(MEM.glob("feedback_*.md")):
    text = f.read_text(encoding="utf-8")
    orig = text
    for purged, target in REDIR.items():
        # remplace [[feedback_purged]] et [[feedback_purged|alias]]
        text = re.sub(r"\[\[" + re.escape(purged) + r"(\|[^\]]*)?\]\]", f"[[{target}]]", text)
    if text != orig:
        f.write_text(text, encoding="utf-8")
        n = len(re.findall(r"\[\[", orig)) - len(re.findall(r"\[\[", text)) + sum(
            1 for p in REDIR if f"[[{p}" in orig
        )
        print(f"  {f.name}: wikilinks redirigés")
        total += 1
print(f"Fichiers modifiés: {total}")
