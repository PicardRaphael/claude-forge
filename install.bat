@echo off
chcp 65001 >nul 2>&1
title claude-forge — Installation des outils

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   claude-forge — Setup outils CLI        ║
echo  ╚══════════════════════════════════════════╝
echo.

:: --- Vérification des prérequis ---
echo [1/5] Vérification des prérequis...
echo.

set MISSING=0

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ Node.js — MANQUANT — installer depuis https://nodejs.org
    set MISSING=1
) else (
    for /f "tokens=*" %%v in ('node --version') do echo   ✓ Node.js %%v
)

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ Python — MANQUANT — installer depuis https://python.org
    set MISSING=1
) else (
    for /f "tokens=*" %%v in ('python --version') do echo   ✓ %%v
)

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✗ Git — MANQUANT — installer depuis https://git-scm.com
    set MISSING=1
) else (
    for /f "tokens=*" %%v in ('git --version') do echo   ✓ %%v
)

if %MISSING% equ 1 (
    echo.
    echo  ⚠ Installe les prérequis manquants puis relance ce script.
    pause
    exit /b 1
)

echo.

:: --- Outils npm ---
echo [2/5] Outils npm (defuddle-cli)...

call npx defuddle --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   → Installation de defuddle-cli...
    call npm install -g defuddle-cli
) else (
    echo   ✓ defuddle déjà installé
)

echo.

:: --- Outils pip ---
echo [3/5] Outils pip (yt-dlp, fastmcp, pyyaml)...

python -m yt_dlp --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   → Installation de yt-dlp...
    pip install yt-dlp
) else (
    for /f "tokens=*" %%v in ('python -m yt_dlp --version') do echo   ✓ yt-dlp %%v
)

python -c "import fastmcp" >nul 2>&1
if %errorlevel% neq 0 (
    echo   → Installation de fastmcp + pyyaml (MCP forge-brain)...
    pip install fastmcp pyyaml
) else (
    echo   ✓ fastmcp déjà installé
)

echo.

:: --- Optionnels ---
echo [4/5] Outils optionnels (video-to-text, yt-dlp amélioré)...

ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo   → Installation de ffmpeg via winget...
    winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
    echo   ✓ ffmpeg installé (redémarrer le terminal pour PATH)
) else (
    echo   ✓ ffmpeg installé
)

python -c "import faster_whisper" >nul 2>&1
if %errorlevel% neq 0 (
    echo   → Installation de faster-whisper (transcription audio)...
    pip install faster-whisper
) else (
    echo   ✓ faster-whisper installé
)

deno --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ○ deno — non installé (optionnel, améliore yt-dlp)
) else (
    echo   ✓ deno installé
)

echo.

:: --- Vérification finale ---
echo [5/5] Vérification finale...
echo.
echo   ┌─────────────────────────────────────┐

for /f "tokens=*" %%v in ('node --version') do echo   │ Node.js    : %%v
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo   │ %%v
for /f "tokens=*" %%v in ('git --version') do echo   │ %%v

call npx defuddle --version >nul 2>&1
if %errorlevel% equ 0 (
    echo   │ defuddle   : OK
) else (
    echo   │ defuddle   : ERREUR
)

python -m yt_dlp --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%v in ('python -m yt_dlp --version') do echo   │ yt-dlp     : %%v
) else (
    echo   │ yt-dlp     : ERREUR
)

ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo   │ ffmpeg     : OK
) else (
    echo   │ ffmpeg     : non installé
)

python -c "import faster_whisper" >nul 2>&1
if %errorlevel% equ 0 (
    echo   │ whisper    : OK
) else (
    echo   │ whisper    : non installé
)

echo   └─────────────────────────────────────┘
echo.
echo  ✓ Setup terminé !
echo.
pause
