---
name: skills-metadata-tokens-load
description: Claude Code charge name+description de TOUTES les skills installees au demarrage. 49 forge + 35 plugins = 6.8k tokens. Cap desc 250-300 chars = levier optim contexte.
metadata:
  type: reference
---

Mesure empirique 28 mai 2026, session audit context tokens.

**Source non documentee** : le harness Claude Code charge a chaque session le frontmatter `name:` + `description:` de toutes les skills disponibles (forge `.claude/skills/` + plugins user-scope). Visible dans le system-reminder SessionStart "available skills".

**Mesure** :
- 49 skills forge : 15 300 chars descriptions = 3 825 tokens (/4)
- 35 skills plugins : 11 982 chars = 2 996 tokens (/4)
- Total : ~6 800 tokens (~8 200 avec /3.3 tokenizer reel)

**Top 3 forge descriptions a capper** : cc-news (530 chars), x-read (517), spec (511). Cap recommande : 250 chars max pour rester sous le radar tokens.

**Levier optim** :
1. Cap chaque desc skill forge a 250 chars → economie ~1 500 tokens cumules
2. Desinstaller plugins skills non utilises → economie ~3 000 tokens
3. Pour skill complexe : description courte + body riche (le body se charge a l'invocation, pas au demarrage)

Lien doctrine [[feedback_proactive_references_extraction]] : meme principe que references/ → garder l'init leger.

Methode mesure :
```powershell
Get-ChildItem .claude\skills -Directory | ForEach-Object {
  $sk = Join-Path $_.FullName 'SKILL.md'
  if (Test-Path $sk) {
    $c = Get-Content $sk -Raw
    $m = [regex]::Match($c, '(?ms)^description:\s*(.+?)(?=^\w+:|^---)')
    if ($m.Success) { [PSCustomObject]@{Name=$_.Name; Chars=$m.Groups[1].Value.Trim().Length} }
  }
} | Sort-Object Chars -Descending
```
