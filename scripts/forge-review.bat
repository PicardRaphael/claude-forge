@echo off
setlocal
for %%I in ("%~dp0..") do set PROJECT=%%~fI
set LOGDIR=%PROJECT%\logs
set TIMESTAMP=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOGFILE=%LOGDIR%\forge-review_%TIMESTAMP%.log

cd /d %PROJECT%

echo [%date% %time%] === forge-review START === >> "%LOGFILE%"

REM Ensure MCP is running
python scripts\ensure-mcp.py >> "%LOGFILE%" 2>&1

REM Run forge-review via Claude CLI
echo [%date% %time%] Launching Claude CLI... >> "%LOGFILE%"
claude -p "Lance /forge-review — review strategique mensuelle. Analyse CLAUDE.md, rules, skills, agents. Produis un verdict KILL/EVOLVE/KEEP/MISSING avec evidence. Sauvegarde le rapport dans le vault Knowledge/reviews/. Sois exhaustif et franc." --yes --max-turns 50 --model claude-sonnet-4-6 >> "%LOGFILE%" 2>&1

echo [%date% %time%] === forge-review END (exit code: %ERRORLEVEL%) === >> "%LOGFILE%"
endlocal
