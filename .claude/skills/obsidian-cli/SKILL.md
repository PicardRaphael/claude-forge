---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the Obsidian CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## CLI — REGLE ABSOLUE (Windows)

**Ne JAMAIS appeler `obsidian` directement.** Sur Windows + Git Bash, `obsidian` resout vers l'app GUI (Obsidian.exe) au lieu de la CLI console (Obsidian.com). Ca casse tout.

**Toujours utiliser le wrapper** :
```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null
```

Les exemples ci-dessous utilisent `obsidian` par concision, mais **tu DOIS remplacer par `bash .claude/skills/forge-brain/scripts/obsidian-cli.sh`** dans chaque appel Bash.

## Pre-check (OBLIGATOIRE)

Before any CLI command, run:
```bash
bash .claude/skills/forge-brain/scripts/obsidian-cli.sh version 2>/dev/null
```
- If it succeeds: proceed with CLI commands (via le wrapper).
- If it fails (exit 127 or error): **Obsidian is not running or CLI unavailable.** Fall back to using `Write` / `Read` / `Glob` tools directly on vault files. The vault root is the current working directory.

## Templates (OBLIGATOIRE)

When creating notes, ALWAYS read the corresponding template first and follow its exact format:

| Target folder | Template |
|---|---|
| `01-Domaines/` | `Templates/domaine.md` |
| `02-BDD/tables/` | `Templates/table-bdd.md` |
| `02-BDD/fonctions-pg/` | `Templates/fonction-pg.md` |
| `03-Apps/` | `Templates/app.md` |
| `05-Decisions/` | `Templates/decision-adr.md` |
| `Knowledge/` | `Templates/knowledge.md` |

**Never modify Templates/.** Read them as format reference only.

Since `obsidian create` cannot handle frontmatter (colons break the CLI), use `Read` on the template then `Write` the new note following its structure.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

**IMPORTANT — Colons in content break the CLI parser.** Any `:` inside `content="..."` is interpreted as a parameter separator, causing exit code 127. This means YAML frontmatter (`key: value`) CANNOT be passed via `obsidian create content=`.

**To create notes with frontmatter:** use the `Write` tool directly instead:
```
Write(file_path="<vault_root>/<path>.md", content="---\ntitle: ...\n---\n\nBody")
```
Then use `obsidian` CLI only for read, search, append (without colons), property:set, tags, etc.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
