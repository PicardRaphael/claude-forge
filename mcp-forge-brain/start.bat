@echo off
chcp 65001 >nul 2>&1
title forge-brain MCP (port 8091)

cd /d "%~dp0.."
python "%~dp0start.py"
if %errorlevel% neq 0 (
    echo.
    echo  [ERREUR] Le serveur a crashe. Voir ci-dessus.
    pause
)
