# align-vault-skills-check.ps1 — Veille d'alignement vault <-> skills-ref + agents (hebdo)
# Planifier via Task Scheduler :
# powershell -ExecutionPolicy Bypass -File "<path-to-claude-forge>\.claude\scripts\align-vault-skills-check.ps1"
#
# Kill-switch : creer le fichier .claude\.alignment-loop.stop pour stopper (la skill s'arrete d'elle-meme).

# Resolve project root from script location (portable across machines)
$forgeDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Push-Location $forgeDir
claude -p "/align-vault-skills" --yes 2>&1
Pop-Location
