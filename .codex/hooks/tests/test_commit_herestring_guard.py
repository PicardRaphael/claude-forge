"""Tests commit-herestring-guard.py

Perimetre declare du hook :
- Bloque UNIQUEMENT `git commit` avec un here-string PowerShell (@' ou @") place
  IMMEDIATEMENT apres un flag message (-m / --message / -am / -cm), via le tool Bash.
- Le here-string PowerShell est l'idiome LEGITIME du tool PowerShell -> ce hook ne
  doit JAMAIS tourner sur PowerShell (matcher Bash-only dans settings.json).

Ce que les tests NE verifient PAS (gaps hors-scope, volontaires) :
- Heredoc bash `<<EOF` : surface de faux positif trop large (`-m "a << b"`) et ce
  n'est PAS le bug recurrent documente. Scope out explicite (1 test de non-blocage).
- Le matcher settings.json (Bash-only) : verifie a l'enregistrement, pas ici.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from importlib import import_module

guard = import_module("commit-herestring-guard")
is_blocked = guard.is_blocked


# --- ADVERSE in-scope : le bug a attraper (faux negatifs tentes) ---

def test_herestring_single_quote_blocked():
    assert is_blocked("git commit -m @'\nTitre\ncorps\n'@") is True


def test_herestring_double_quote_blocked():
    assert is_blocked('git commit -m @"\nTitre\n"@') is True


def test_herestring_message_long_flag_blocked():
    assert is_blocked("git commit --message @'\nx\n'@") is True


def test_herestring_am_flag_blocked():
    assert is_blocked("git commit -am @'\nx\n'@") is True


def test_herestring_no_space_after_flag_blocked():
    assert is_blocked("git commit -m@'\nx\n'@") is True


def test_herestring_with_git_C_prefix_blocked():
    assert is_blocked("git -C /repo commit -m @'\nx\n'@") is True


# --- ADVERSE in-scope : over-block (faux positifs que l'ancrage doit eviter) ---

def test_herestring_chars_inside_quoted_message_passes():
    # @' apparait dans le message mais PAS apres le flag -> ne doit pas bloquer
    assert is_blocked("git commit -m \"fix @' parsing in lexer\"") is False


def test_at_mention_in_message_passes():
    assert is_blocked('git commit -m "thanks @mention for the fix"') is False


def test_heredoc_lookalike_in_message_passes():
    # heredoc hors-scope : ne doit pas bloquer un message contenant <<
    assert is_blocked('git commit -m "handle a << b bit shift"') is False


# --- HAPPY path (<= 25%) ---

def test_normal_single_m_passes():
    assert is_blocked('git commit -m "fix: normal commit"') is False


def test_multi_m_passes():
    assert is_blocked('git commit -m "titre" -m "corps"') is False


def test_commit_no_inline_message_passes():
    assert is_blocked("git commit") is False


def test_amend_multi_m_passes():
    assert is_blocked('git commit --amend -m "titre" -m "corps"') is False


def test_empty_command_passes():
    assert is_blocked("") is False


def test_non_git_command_passes():
    assert is_blocked("ls -la") is False


if __name__ == "__main__":
    import subprocess

    # Exit-code level tests (PASS=0, BLOCK=2, fail-open=0)
    hook = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "commit-herestring-guard.py")

    def run(payload):
        p = subprocess.run(["py", "-3", hook], input=payload, capture_output=True, text=True)
        return p.returncode

    import json

    pass_normal = run(json.dumps({"tool_name": "Bash", "tool_input": {"command": 'git commit -m "normal"'}}))
    block_here = run(json.dumps({"tool_name": "Bash", "tool_input": {"command": "git commit -m @'\nx\n'@"}}))
    pass_multi = run(json.dumps({"tool_name": "Bash", "tool_input": {"command": 'git commit -m "a" -m "b"'}}))
    failopen = run("not json at all")

    print(f"(a) git commit -m \"normal\"        -> exit {pass_normal}  (attendu 0)")
    print(f"(b) git commit -m @'...'@          -> exit {block_here}  (attendu 2)")
    print(f"(c) git commit -m \"a\" -m \"b\"       -> exit {pass_multi}  (attendu 0)")
    print(f"(d) JSON invalide (fail-open)      -> exit {failopen}  (attendu 0)")
    assert (pass_normal, block_here, pass_multi, failopen) == (0, 2, 0, 0), "EXIT CODES KO"
    print("\nTOUS LES TESTS EXIT-CODE PASSENT")
