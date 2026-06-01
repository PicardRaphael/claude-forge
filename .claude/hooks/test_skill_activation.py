#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for skill-activation.py -- simulated stdin, shared tracker file.

Runs 6 tests against the actual hook code (imported, not subprocess).
Uses a temp tracker file to simulate a real session across turns.
"""
import io
import json
import os
import sys
import tempfile
import importlib.util

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ---------------------------------------------------------------------------
# Bootstrap: import skill-activation as a module (it lives in the same dir)
# ---------------------------------------------------------------------------
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_HOOK_PATH = os.path.join(_THIS_DIR, "skill-activation.py")

spec = importlib.util.spec_from_file_location("skill_activation", _HOOK_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------
PASS = "PASS"
FAIL = "FAIL"
results = []


def run_turn(prompt, tracker_path):
    """Run find_matches with the actual tracker file, return matches (or [] on error)."""
    original = mod.SESSION_TRACKER
    mod.SESSION_TRACKER = tracker_path
    try:
        triggers = mod.load_triggers()
        already = mod.load_session_tracker()
        matches = mod.find_matches(prompt.lstrip(), triggers, already)
        if matches:
            newly = already | {m["_tracker_key"] for m in matches}
            mod.save_session_tracker(newly)
        return matches if matches is not None else []
    except Exception as e:
        print("EXCEPTION in run_turn: " + str(e))
        return []
    finally:
        mod.SESSION_TRACKER = original


def check(test_id, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((test_id, status, detail))
    msg = "[" + status + "] " + test_id
    if detail:
        msg += " -- " + detail
    print(msg)


# ---------------------------------------------------------------------------
# Session A: Tests 1, 2, 3 (shared tracker)
# ---------------------------------------------------------------------------
tracker_a = tempfile.mktemp(suffix=".json", prefix="skill-activation-test-")

# T1: "propose une skill" -> forge-brain::skill
matches1 = run_turn("propose une skill dans mon projet", tracker_a)
forge_keys1 = [m["_tracker_key"] for m in matches1 if m["name"] == "forge-brain"]
check(
    "T1: propose une skill -> forge-brain::skill emis",
    "forge-brain::skill" in forge_keys1,
    "keys=" + str(forge_keys1)
)

# T2 (meme session): "cree un agent" -> forge-brain::agent (sujet different)
# Both accented and unaccented variants are in triggers, test sans accent
matches2 = run_turn("cree un agent maintenant", tracker_a)
forge_keys2 = [m["_tracker_key"] for m in matches2 if m["name"] == "forge-brain"]
check(
    "T2: cree un agent -> forge-brain::agent (sujet != skill, meme session)",
    "forge-brain::agent" in forge_keys2,
    "keys=" + str(forge_keys2)
)

# T3: "propose une skill" x2 -> 0 rappel supplementaire (meme sujet)
matches3a = run_turn("propose une skill encore", tracker_a)
forge_keys3a = [m["_tracker_key"] for m in matches3a if m["name"] == "forge-brain"]
matches3b = run_turn("propose une skill encore", tracker_a)
forge_keys3b = [m["_tracker_key"] for m in matches3b if m["name"] == "forge-brain"]
check(
    "T3: propose une skill x2 apres T1 -> 0 rappel forge-brain::skill",
    len(forge_keys3a) == 0 and len(forge_keys3b) == 0,
    "3a=" + str(forge_keys3a) + " 3b=" + str(forge_keys3b)
)

if os.path.exists(tracker_a):
    os.remove(tracker_a)

# ---------------------------------------------------------------------------
# Session B: Test 4 (fresh tracker)
# ---------------------------------------------------------------------------
tracker_b = tempfile.mktemp(suffix=".json", prefix="skill-activation-test-")

matches4 = run_turn("corrige ce typo", tracker_b)
forge_keys4 = [m["_tracker_key"] for m in matches4 if m["name"] == "forge-brain"]
check(
    "T4a: 'corrige ce typo' -> aucun rappel forge-brain",
    len(forge_keys4) == 0,
    "all=" + str([m["name"] for m in matches4])
)

matches4b = run_turn("merci", tracker_b)
forge_keys4b = [m["_tracker_key"] for m in matches4b if m["name"] == "forge-brain"]
check(
    "T4b: 'merci' -> aucun rappel forge-brain",
    len(forge_keys4b) == 0,
    "all=" + str([m["name"] for m in matches4b])
)

if os.path.exists(tracker_b):
    os.remove(tracker_b)

# ---------------------------------------------------------------------------
# Session C: Test 5 -- legacy entry cc-news (flat triggers list)
# ---------------------------------------------------------------------------
tracker_c = tempfile.mktemp(suffix=".json", prefix="skill-activation-test-")

matches5a = run_turn("quoi de neuf sur claude code", tracker_c)
ccnews_keys5a = [m["_tracker_key"] for m in matches5a if m["name"] == "cc-news"]
check(
    "T5a: 'quoi de neuf' -> cc-news recommande (legacy)",
    "cc-news" in ccnews_keys5a,
    "keys=" + str(ccnews_keys5a)
)

matches5b = run_turn("quoi de neuf sur les features", tracker_c)
ccnews_keys5b = [m["_tracker_key"] for m in matches5b if m["name"] == "cc-news"]
check(
    "T5b: 'quoi de neuf' x2 -> cc-news PAS recommande 2e fois",
    len(ccnews_keys5b) == 0,
    "keys=" + str(ccnews_keys5b)
)

if os.path.exists(tracker_c):
    os.remove(tracker_c)

# ---------------------------------------------------------------------------
# Session D: Test 6 -- tracker corrompu -> fail-open, pas de crash
# ---------------------------------------------------------------------------
tracker_d = tempfile.mktemp(suffix=".json", prefix="skill-activation-test-")

with open(tracker_d, "w") as f:
    f.write("NOT VALID JSON }{{{")

try:
    matches6 = run_turn("propose une skill", tracker_d)
    check(
        "T6: tracker corrompu -> pas de crash, fonctionne normalement",
        matches6 is not None,
        "matches=" + str([m["name"] for m in matches6] if matches6 else "None")
    )
except Exception as e:
    check("T6: tracker corrompu -> pas de crash", False, "EXCEPTION: " + str(e))
finally:
    if os.path.exists(tracker_d):
        os.remove(tracker_d)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
print("Resultat : " + str(passed) + "/" + str(passed + failed) + " PASS")
if failed:
    print("FAILURES :")
    for tid, s, d in results:
        if s == FAIL:
            print("  " + tid + " -- " + d)
    sys.exit(1)
else:
    print("Tous les tests passent.")
    sys.exit(0)
