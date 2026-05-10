@echo off
setlocal
set PROJECT=C:\Users\rapha\Documents\claude-forge
set LOGDIR=%PROJECT%\logs
set TIMESTAMP=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOGFILE=%LOGDIR%\vault-audit_%TIMESTAMP%.log

cd /d %PROJECT%

echo [%date% %time%] === vault-audit START === >> "%LOGFILE%"

REM Ensure MCP is running
python scripts\ensure-mcp.py >> "%LOGFILE%" 2>&1

REM Run vault-audit via Claude CLI
echo [%date% %time%] Launching Claude CLI... >> "%LOGFILE%"
claude -p "Lance /vault-audit — audit complet du vault forge-brain. Verifie : notes orphelines, frontmatter incomplet, tags manquants, aliases insuffisants, notes trop longues a decouper, doublons. Corrige automatiquement ce qui peut l'etre. Produis un rapport." --yes --max-turns 60 --model claude-sonnet-4-6 >> "%LOGFILE%" 2>&1

echo [%date% %time%] === vault-audit END (exit code: %ERRORLEVEL%) === >> "%LOGFILE%"
endlocal
