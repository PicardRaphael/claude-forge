@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Installation MCP obsidian-brain
echo   pour Claude Desktop
echo ============================================
echo.

:: 1. Detecter Python
echo [1/4] Detection de Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR : Python non trouve. Installez Python d'abord.
    pause
    exit /b 1
)
for /f "delims=" %%i in ('where python') do set PYTHON_PATH=%%i
echo   Python trouve : %PYTHON_PATH%

:: 2. Detecter le chemin du MCP server
echo.
echo [2/4] Detection du MCP obsidian-brain...
set MCP_PATH=%USERPROFILE%\Documents\mcp-obsidian-brain\src\server.py
if not exist "%MCP_PATH%" (
    echo   Pas trouve dans %USERPROFILE%\Documents\mcp-obsidian-brain
    echo.
    set /p MCP_PATH="   Entrez le chemin complet vers server.py : "
)
if not exist "!MCP_PATH!" (
    echo ERREUR : server.py non trouve a !MCP_PATH!
    pause
    exit /b 1
)
echo   MCP trouve : !MCP_PATH!

:: 3. Convertir les backslash en forward slash pour JSON
set PYTHON_JSON=%PYTHON_PATH:\=/%
set MCP_JSON=!MCP_PATH:\=/!

:: 4. Ecrire le config
echo.
echo [3/4] Ecriture de la configuration...
set CONFIG_DIR=%APPDATA%\Claude
set CONFIG_FILE=%CONFIG_DIR%\claude_desktop_config.json

if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

:: Backup si existe deja
if exist "%CONFIG_FILE%" (
    echo   Backup de la config existante...
    copy "%CONFIG_FILE%" "%CONFIG_FILE%.bak" >nul
    echo   Backup sauvegarde : %CONFIG_FILE%.bak
)

:: Ecrire le nouveau config
(
echo {
echo   "mcpServers": {
echo     "obsidian-brain": {
echo       "command": "%PYTHON_JSON%",
echo       "args": ["%MCP_JSON%"]
echo     }
echo   }
echo }
) > "%CONFIG_FILE%"

echo   Config ecrite : %CONFIG_FILE%

:: 5. Verifier
echo.
echo [4/4] Verification...
type "%CONFIG_FILE%"
echo.
echo ============================================
echo   Installation terminee !
echo   Redemarrez Claude Desktop pour appliquer.
echo ============================================
pause
