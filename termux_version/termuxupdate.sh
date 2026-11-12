#!/bin/bash

# Colores para la interfaz
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin Color

clear
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}   🚀 INICIANDO MEDIAFLOW UTILITY PRO 🚀   ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# 1. Actualizar yt-dlp y dependencias
echo -e "${YELLOW}[+] Comprobando y actualizando yt-dlp...${NC}"
pip install -U yt-dlp --no-cache-dir

echo ""
echo -e "${GREEN}[✔] yt-dlp actualizado correctamente.${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# 2. Ejecutar la aplicación principal de Python
cd "$(dirname "$0")"
if [ -f "MediaFlowTermuxver.py" ]; then
    echo -e "${YELLOW}[+] Iniciando script principal...${NC}"
    python MediaFlowTermuxver.py
else
    echo -e "${YELLOW}[!] 'MediaFlowTermuxver.py' no se encuentra en este directorio.${NC}"
fi
