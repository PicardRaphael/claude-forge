# x-read — Script d'installation Windows (PowerShell)
#
# Usage:
#   .\install.ps1
#
# Effectue 5 etapes:
#   1. Verifier Python 3.10+
#   2. Installer twitter-api-client
#   3. Creer le dossier .claude/secrets/
#   4. Guider la recuperation des cookies (etape manuelle)
#   5. Tester avec reader.py check

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  x-read — Installation Windows" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Resolve project root (script is in .claude/skills/x-read/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $ScriptDir))
$SecretsDir = Join-Path $ProjectRoot ".claude\secrets"
$CookiesPath = Join-Path $SecretsDir "x-cookies.json"

Write-Host "Project root: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Step 1 — Python check
Write-Host "[1/5] Verification Python..." -ForegroundColor Yellow
try {
    $PyVersion = python --version 2>&1
    if ($PyVersion -match "Python (\d+)\.(\d+)") {
        $Major = [int]$Matches[1]
        $Minor = [int]$Matches[2]
        if ($Major -lt 3 -or ($Major -eq 3 -and $Minor -lt 10)) {
            Write-Host "  ECHEC: Python 3.10+ requis (trouve: $PyVersion)" -ForegroundColor Red
            Write-Host "  Installer depuis https://python.org" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "  OK: $PyVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "  ECHEC: 'python' introuvable dans le PATH" -ForegroundColor Red
    Write-Host "  Installer Python 3.10+ depuis https://python.org en cochant 'Add to PATH'" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Step 2 — pip install
Write-Host "[2/5] Installation twitter-api-client..." -ForegroundColor Yellow
try {
    python -c "import twitter" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: twitter-api-client deja installe" -ForegroundColor Green
    } else {
        throw "not installed"
    }
} catch {
    Write-Host "  Installation en cours (peut prendre 1-2 min)..." -ForegroundColor Gray
    python -m pip install "twitter-api-client>=0.10.20,<0.12.0" --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ECHEC: pip install a echoue" -ForegroundColor Red
        Write-Host "  Tenter manuellement: python -m pip install 'twitter-api-client>=0.10.20,<0.12.0'" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "  OK: twitter-api-client installe" -ForegroundColor Green
}
Write-Host ""

# Step 3 — Create secrets dir
Write-Host "[3/5] Creation du dossier secrets..." -ForegroundColor Yellow
if (-not (Test-Path $SecretsDir)) {
    New-Item -ItemType Directory -Path $SecretsDir -Force | Out-Null
    Write-Host "  OK: cree -> $SecretsDir" -ForegroundColor Green
} else {
    Write-Host "  OK: existe deja -> $SecretsDir" -ForegroundColor Green
}
Write-Host ""

# Step 4 — Cookies setup (manual)
Write-Host "[4/5] Configuration des cookies X (etape manuelle)..." -ForegroundColor Yellow

if (Test-Path $CookiesPath) {
    Write-Host "  Fichier cookies existe deja: $CookiesPath" -ForegroundColor Gray
    $Overwrite = Read-Host "  Le remplacer ? (o/N)"
    if ($Overwrite -ne 'o' -and $Overwrite -ne 'O') {
        Write-Host "  Skip — utilisation du fichier existant" -ForegroundColor Gray
        Write-Host ""
        $SkipCookies = $true
    }
}

if (-not $SkipCookies) {
    Write-Host ""
    Write-Host "  Instructions:" -ForegroundColor Cyan
    Write-Host "  1. Ouvre https://x.com dans Chrome/Edge (logged-in avec ton compte perso)"
    Write-Host "  2. Appuie sur F12 (DevTools)"
    Write-Host "  3. Onglet 'Application' -> sidebar 'Cookies' -> clic sur 'https://x.com'"
    Write-Host "  4. Cherche les 2 cookies suivants:"
    Write-Host "     - auth_token (~40 caracteres hex)" -ForegroundColor White
    Write-Host "     - ct0 (~160 caracteres hex)" -ForegroundColor White
    Write-Host ""
    Write-Host "  ATTENTION: pas 'auth_multi' (plus long), bien 'auth_token' exact" -ForegroundColor Yellow
    Write-Host ""

    $AuthToken = Read-Host "  Colle la valeur de auth_token"
    $Ct0 = Read-Host "  Colle la valeur de ct0"

    # Validation longueurs
    if ($AuthToken.Length -lt 30 -or $AuthToken.Length -gt 60) {
        Write-Host "  ATTENTION: auth_token fait $($AuthToken.Length) chars, attendu ~40. Continuer ? (o/N)" -ForegroundColor Yellow
        $Continue = Read-Host
        if ($Continue -ne 'o' -and $Continue -ne 'O') { exit 1 }
    }
    if ($Ct0.Length -lt 100) {
        Write-Host "  ATTENTION: ct0 fait $($Ct0.Length) chars, attendu ~160. Continuer ? (o/N)" -ForegroundColor Yellow
        $Continue = Read-Host
        if ($Continue -ne 'o' -and $Continue -ne 'O') { exit 1 }
    }

    $CookiesJson = @{
        ct0 = $Ct0
        auth_token = $AuthToken
    } | ConvertTo-Json

    Set-Content -Path $CookiesPath -Value $CookiesJson -Encoding UTF8
    Write-Host "  OK: cookies enregistres dans $CookiesPath" -ForegroundColor Green
}
Write-Host ""

# Step 5 — Test
Write-Host "[5/5] Test final..." -ForegroundColor Yellow
$ReaderPath = Join-Path $ScriptDir "reader.py"
python $ReaderPath check
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ECHEC: le check n'a pas reussi" -ForegroundColor Red
    Write-Host "  Verifier le contenu de $CookiesPath" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Done
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Installation terminee !" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Pour tester:" -ForegroundColor Cyan
Write-Host "  python $ReaderPath pretty 'https://x.com/trq212/status/2056415973125796184'"
Write-Host ""
Write-Host "Ou via Claude Code:" -ForegroundColor Cyan
Write-Host "  /x-read https://x.com/<n-importe-quel-tweet>"
Write-Host ""
Write-Host "Cookies expirent dans ~30 jours. Pour les renouveler: relancer ce script." -ForegroundColor Gray
Write-Host ""
