# news-check.ps1 — Verifie les nouveautes Claude Code tous les 2 jours
# Planifier via Task Scheduler :
# powershell -ExecutionPolicy Bypass -File "C:\Users\raphael.picard_neote\Documents\claude-forge\.claude\hooks\news-check.ps1"

$forgeDir = "C:\Users\raphael.picard_neote\Documents\claude-forge"

Push-Location $forgeDir
claude -p "Lance cc-news. Cherche les nouveautes Claude Code, Cowork, Dispatch, prompt engineering depuis la derniere date de reference. Si tu trouves des breaking changes ou des nouvelles features importantes, mets a jour les skills de reference (cc-features-ref, cc-hooks-ref, cc-cowork-ref, cc-news) et commit. Si rien de nouveau, ne fais rien." --yes 2>&1
Pop-Location
