#!/usr/bin/env python3
"""
config-guardian/scripts/scan.py
Scan repos Neoteem pour les ecarts de config Claude Code.
Usage: python3 scan.py [ia_back|neo_ia|neoteem-brain|all]
Output: JSON avec tous les faits collectes (Claude produit les jugements et le rapport)
"""

import json
import os
import sys
import glob
import re

REPOS = {
    "ia_back": r"C:\Users\raphael.picard_neote\Documents\neot-v2\ia_back",
    "neo_ia": r"C:\Users\raphael.picard_neote\Documents\neot-v2\neo_ia",
    "neoteem-brain": r"C:\Users\raphael.picard_neote\Documents\neot-v2\neoteem-brain",
}

GLOBAL_SETTINGS = os.path.expanduser(r"~\.claude\settings.json")

STACK_INTERPRETERS = {
    "ia_back": ["bun"],
    "neo_ia": ["python", "uv"],
    "neoteem-brain": ["python3"],
}

REQUIRED_RULES = ["check-before-create.md", "learn-from-mistakes.md", "quality-gates.md"]


def read_json_safe(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"_error": str(e)}


def read_file_safe(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def parse_frontmatter(content):
    if not content or not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    fm_block = content[3:end].strip()
    result = {}
    for line in fm_block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("\"'") for v in val[1:-1].split(",")]
            result[key] = val
    return result


def extract_wired_hooks(settings_data):
    """
    Parse CC hooks structure:
    { "hooks": { "EventName": [ { "matcher": "...", "hooks": [ {"command": "..."} ] } ] } }
    Returns list of dicts with event, command, file, starts_with.
    """
    wired = []
    if not isinstance(settings_data, dict):
        return wired
    for event_name, event_entries in settings_data.get("hooks", {}).items():
        if not isinstance(event_entries, list):
            continue
        for outer in event_entries:
            if not isinstance(outer, dict):
                continue
            inner_hooks = outer.get("hooks", [])
            if not isinstance(inner_hooks, list):
                continue
            for hook in inner_hooks:
                if not isinstance(hook, dict):
                    continue
                cmd = hook.get("command", "")
                if not cmd:
                    continue
                parts = cmd.split()
                file_guess = ""
                for part in parts:
                    basename = os.path.basename(part.replace("\\", "/"))
                    # Accepter uniquement des fichiers avec extension valide (pas "." seul)
                    if "." in basename and len(basename) > 2 and basename != ".":
                        file_guess = basename
                        break
                wired.append({
                    "event": event_name,
                    "command": cmd,
                    "file": file_guess,
                    "starts_with": parts[0] if parts else "",
                })
    return wired


def scan_repo(name, base_path):
    result = {"repo": name, "path": base_path, "exists": os.path.isdir(base_path)}
    if not result["exists"]:
        return result

    claude_dir = os.path.join(base_path, ".claude")

    settings = read_json_safe(os.path.join(claude_dir, "settings.json"))
    settings_local = read_json_safe(os.path.join(claude_dir, "settings.local.json"))
    settings_global = read_json_safe(GLOBAL_SETTINGS)
    result["settings"] = settings
    result["settings_local"] = settings_local
    result["settings_global"] = settings_global

    def get_allow(s):
        return s.get("permissions", {}).get("allow", []) if isinstance(s, dict) and "_error" not in s else []
    def get_deny(s):
        return s.get("permissions", {}).get("deny", []) if isinstance(s, dict) and "_error" not in s else []

    result["permissions_allow"] = get_allow(settings) + get_allow(settings_local)
    result["permissions_global_deny"] = get_deny(settings_global)

    hooks_dir = os.path.join(claude_dir, "hooks")
    hook_files = [os.path.basename(p) for p in glob.glob(os.path.join(hooks_dir, "*"))]
    result["hook_files_on_disk"] = hook_files

    wired_hooks = extract_wired_hooks(settings)
    result["wired_hooks"] = wired_hooks

    wired_files = set(h["file"] for h in wired_hooks if h["file"])
    disk_files = set(hook_files)
    result["hooks_orphan"] = list(disk_files - wired_files)
    result["hooks_phantom"] = list(wired_files - disk_files)

    expected_interpreters = STACK_INTERPRETERS.get(name, [])
    mismatches = []
    for h in wired_hooks:
        starts_with = h.get("starts_with", "")
        if starts_with and not any(starts_with.startswith(i) for i in expected_interpreters):
            mismatches.append({"hook": h["file"], "found": starts_with, "expected": expected_interpreters})
    result["hooks_stack_mismatch"] = mismatches

    rules_dir = os.path.join(claude_dir, "rules")
    present_rules = [os.path.basename(p) for p in glob.glob(os.path.join(rules_dir, "*.md"))]
    result["rules_present"] = present_rules
    result["rules_missing"] = [r for r in REQUIRED_RULES if r not in present_rules]

    agents = []
    for agent_path in glob.glob(os.path.join(claude_dir, "agents", "*.md")):
        content = read_file_safe(agent_path)
        fm = parse_frontmatter(content) if content else {}
        tools = fm.get("tools", [])
        if isinstance(tools, str):
            tools = [tools]
        agents.append({
            "file": os.path.basename(agent_path),
            "has_memory_project": fm.get("memory", "").strip() == "project",
            "has_tools_key": "tools" in fm,
            "tools": tools,
            "description": fm.get("description", ""),
        })
    result["agents"] = agents

    claudemd = read_file_safe(os.path.join(base_path, "CLAUDE.md"))
    result["claudemd_exists"] = claudemd is not None
    result["claudemd_has_gotchas"] = bool(
        re.search(r"^#{1,3}\s+gotchas", claudemd or "", re.IGNORECASE | re.MULTILINE)
    )
    memory_keywords = ["memory", "memoire", "apprentissage", "learn", "MEMORY.md", "update CLAUDE.md"]
    result["claudemd_has_memory_mention"] = any(
        kw.lower() in (claudemd or "").lower() for kw in memory_keywords
    )

    agent_memory_dir = os.path.join(claude_dir, "agent-memory")
    memory_files = glob.glob(os.path.join(agent_memory_dir, "**", "*"), recursive=True)
    result["agent_memory_count"] = len([f for f in memory_files if os.path.isfile(f)])

    return result


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "all":
        repos_to_scan = REPOS
    elif target in REPOS:
        repos_to_scan = {target: REPOS[target]}
    else:
        print("Usage: scan.py [ia_back|neo_ia|neoteem-brain|all]", file=sys.stderr)
        sys.exit(1)

    output = {}
    for name, path in repos_to_scan.items():
        output[name] = scan_repo(name, path)

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
