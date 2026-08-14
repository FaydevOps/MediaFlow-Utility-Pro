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
if [ -f "main.py" ]; then
    echo -e "${YELLOW}[+] Iniciando script principal...${NC}"
    python main.py
else
    echo -e "${YELLOW}[!] 'main.py' no se encuentra en este directorio.${NC}"
fi
