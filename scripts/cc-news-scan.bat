@echo off
setlocal
for %%I in ("%~dp0..") do set PROJECT=%%~fI
set LOGDIR=%PROJECT%\logs
set TIMESTAMP=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOGFILE=%LOGDIR%\cc-news_%TIMESTAMP%.log

cd /d %PROJECT%

echo [%date% %time%] === cc-news START === >> "%LOGFILE%"

REM Ensure MCP is running
python scripts\ensure-mcp.py >> "%LOGFILE%" 2>&1

REM Run cc-news via Claude CLI
echo [%date% %time%] Launching Claude CLI... >> "%LOGFILE%"
claude -p "Lance /cc-news — scan complet des nouveautes. Capitalise toutes les decouvertes dans le vault forge-brain. Met a jour la date de reference dans la skill. Resume les 5 decouvertes les plus importantes en fin de session." --yes --max-turns 80 --model claude-sonnet-4-6 >> "%LOGFILE%" 2>&1

echo [%date% %time%] === cc-news END (exit code: %ERRORLEVEL%) === >> "%LOGFILE%"
endlocal
