#!/usr/bin/env bash
# x-read — Script d'installation cross-platform (Git Bash / Linux / macOS)
#
# Usage:
#   bash install.sh
#
# Effectue 5 etapes (identique a install.ps1):
#   1. Verifier Python 3.10+
#   2. Installer twitter-api-client
#   3. Creer le dossier .claude/secrets/
#   4. Guider la recuperation des cookies (etape manuelle)
#   5. Tester avec reader.py check

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m'

echo ""
echo -e "${CYAN}==========================================${NC}"
echo -e "${CYAN}  x-read — Installation${NC}"
echo -e "${CYAN}==========================================${NC}"
echo ""

# Resolve paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/../../.." && pwd )"
SECRETS_DIR="${PROJECT_ROOT}/.claude/secrets"
COOKIES_PATH="${SECRETS_DIR}/x-cookies.json"

echo -e "${GRAY}Project root: ${PROJECT_ROOT}${NC}"
echo ""

# Step 1 — Python
echo -e "${YELLOW}[1/5] Verification Python...${NC}"
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}  ECHEC: python introuvable${NC}"
    echo -e "${YELLOW}  Installer Python 3.10+ depuis https://python.org${NC}"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
PY_VERSION=$($PYTHON_CMD --version 2>&1)
PY_MAJOR=$(echo "$PY_VERSION" | grep -oE '[0-9]+' | head -1)
PY_MINOR=$(echo "$PY_VERSION" | grep -oE '[0-9]+' | sed -n '2p')

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    echo -e "${RED}  ECHEC: Python 3.10+ requis (trouve: $PY_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}  OK: $PY_VERSION${NC}"
echo ""

# Step 2 — pip install
echo -e "${YELLOW}[2/5] Installation twitter-api-client...${NC}"
if $PYTHON_CMD -c "import twitter" 2>/dev/null; then
    echo -e "${GREEN}  OK: twitter-api-client deja installe${NC}"
else
    echo -e "${GRAY}  Installation en cours (peut prendre 1-2 min)...${NC}"
    $PYTHON_CMD -m pip install "twitter-api-client>=0.10.20,<0.12.0" --quiet
    echo -e "${GREEN}  OK: twitter-api-client installe${NC}"
fi
echo ""

# Step 3 — secrets dir
echo -e "${YELLOW}[3/5] Creation du dossier secrets...${NC}"
mkdir -p "$SECRETS_DIR"
echo -e "${GREEN}  OK: $SECRETS_DIR${NC}"
echo ""

# Step 4 — cookies
echo -e "${YELLOW}[4/5] Configuration des cookies X (etape manuelle)...${NC}"

SKIP_COOKIES=false
if [ -f "$COOKIES_PATH" ]; then
    echo -e "${GRAY}  Fichier cookies existe deja: $COOKIES_PATH${NC}"
    read -p "  Le remplacer ? (o/N) " OVERWRITE
    if [ "$OVERWRITE" != "o" ] && [ "$OVERWRITE" != "O" ]; then
        echo -e "${GRAY}  Skip — utilisation du fichier existant${NC}"
        SKIP_COOKIES=true
    fi
fi

if [ "$SKIP_COOKIES" = false ]; then
    echo ""
    echo -e "${CYAN}  Instructions:${NC}"
    echo "  1. Ouvre https://x.com dans Chrome/Edge (logged-in avec ton compte perso)"
    echo "  2. Appuie sur F12 (DevTools)"
    echo "  3. Onglet 'Application' -> sidebar 'Cookies' -> clic sur 'https://x.com'"
    echo "  4. Cherche les 2 cookies suivants:"
    echo "     - auth_token (~40 caracteres hex)"
    echo "     - ct0 (~160 caracteres hex)"
    echo ""
    echo -e "${YELLOW}  ATTENTION: pas 'auth_multi' (plus long), bien 'auth_token' exact${NC}"
    echo ""

    read -p "  Colle la valeur de auth_token: " AUTH_TOKEN
    read -p "  Colle la valeur de ct0: " CT0

    # Validation longueurs
    AT_LEN=${#AUTH_TOKEN}
    CT0_LEN=${#CT0}
    if [ "$AT_LEN" -lt 30 ] || [ "$AT_LEN" -gt 60 ]; then
        echo -e "${YELLOW}  ATTENTION: auth_token fait $AT_LEN chars, attendu ~40. Continuer ? (o/N)${NC}"
        read CONTINUE
        if [ "$CONTINUE" != "o" ] && [ "$CONTINUE" != "O" ]; then exit 1; fi
    fi
    if [ "$CT0_LEN" -lt 100 ]; then
        echo -e "${YELLOW}  ATTENTION: ct0 fait $CT0_LEN chars, attendu ~160. Continuer ? (o/N)${NC}"
        read CONTINUE
        if [ "$CONTINUE" != "o" ] && [ "$CONTINUE" != "O" ]; then exit 1; fi
    fi

    cat > "$COOKIES_PATH" <<EOF
{
  "ct0": "$CT0",
  "auth_token": "$AUTH_TOKEN"
}
EOF
    echo -e "${GREEN}  OK: cookies enregistres dans $COOKIES_PATH${NC}"
fi
echo ""

# Step 5 — Test
echo -e "${YELLOW}[5/5] Test final...${NC}"
$PYTHON_CMD "${SCRIPT_DIR}/reader.py" check
echo ""

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}  Installation terminee !${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${CYAN}Pour tester:${NC}"
echo "  $PYTHON_CMD ${SCRIPT_DIR}/reader.py pretty 'https://x.com/trq212/status/2056415973125796184'"
echo ""
echo -e "${CYAN}Ou via Claude Code:${NC}"
echo "  /x-read https://x.com/<n-importe-quel-tweet>"
echo ""
echo -e "${GRAY}Cookies expirent dans ~30 jours. Relancer ce script pour les renouveler.${NC}"
echo ""
