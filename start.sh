#!/bin/bash
# Script de instalación y lanzamiento para MultiDownloaderv2.0
# Compatible con: Debian/Ubuntu, Arch, Fedora, RHEL/CentOS, openSUSE, Alpine, macOS (con Homebrew)

set -e  # Detener ejecución si hay error

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# ---- Detección de sistema operativo y gestor de paquetes ----
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo -e "${GREEN}🔍 Sistema detectado: $OS${NC}"
}

detect_package_manager() {
    if command -v apt &>/dev/null; then
        PKG_MANAGER="apt"
    elif command -v pacman &>/dev/null; then
        PKG_MANAGER="pacman"
    elif command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &>/dev/null; then
        PKG_MANAGER="yum"
    elif command -v zypper &>/dev/null; then
        PKG_MANAGER="zypper"
    elif command -v apk &>/dev/null; then
        PKG_MANAGER="apk"
    elif command -v brew &>/dev/null; then
        PKG_MANAGER="brew"
    else
        PKG_MANAGER="unknown"
    fi
    echo -e "${GREEN}📦 Gestor de paquetes detectado: $PKG_MANAGER${NC}"
}

# ---- Instalación de paquetes según gestor ----
install_packages() {
    local packages=("$@")
    case $PKG_MANAGER in
        apt)
            sudo apt update && sudo apt install -y "${packages[@]}"
            ;;
        pacman)
            sudo pacman -Syu --noconfirm "${packages[@]}"
            ;;
        dnf)
            sudo dnf install -y "${packages[@]}"
            ;;
        yum)
            sudo yum install -y "${packages[@]}"
            ;;
        zypper)
            sudo zypper install -y "${packages[@]}"
            ;;
        apk)
            sudo apk add "${packages[@]}"
            ;;
        brew)
            brew install "${packages[@]}"
            ;;
        *)
            echo -e "${RED}❌ No se pudo determinar el gestor de paquetes. Instala manualmente: ${packages[*]}${NC}"
            exit 1
            ;;
    esac
}

# ---- Función principal ----
main() {
    echo -e "${YELLOW}🚀 Iniciando instalación de MultiDownloaderv2.0...${NC}"

    # 1. Detectar sistema y gestor
    detect_os
    detect_package_manager

    # 2. Definir dependencias del sistema según el OS
    local deps=()
    if [[ "$OS" == "macos" ]]; then
        deps=("ffmpeg" "python3")
        # En macOS, python3-venv viene incluido con python3, y pip3 se instala con python3
        # Añadimos brew para asegurar
    else
        # Linux: dependencias comunes
        deps=("ffmpeg" "python3" "python3-pip" "python3-venv")
        # Para Arch, python3-pip y python3-venv no existen como paquetes separados,
        # pero pacman los incluye en python3. Aun así los dejamos, pacman ignorará si no existen.
        # Ajustamos para algunas distros
        if [[ "$PKG_MANAGER" == "pacman" ]]; then
            deps=("ffmpeg" "python" "python-pip")  # Arch usa "python" y "python-pip"
        fi
        if [[ "$PKG_MANAGER" == "apk" ]]; then
            deps=("ffmpeg" "python3" "py3-pip" "py3-virtualenv")  # Alpine
        fi
        # Para RHEL/CentOS 7, python3-venv puede llamarse python3-virtualenv
        if [[ "$PKG_MANAGER" == "yum" ]]; then
            deps=("ffmpeg" "python3" "python3-pip" "python3-virtualenv")
        fi
    fi

    echo -e "${YELLOW}📥 Instalando dependencias del sistema: ${deps[*]}${NC}"
    install_packages "${deps[@]}"

    # 3. Crear entorno virtual (si no existe)
    if [ ! -d "env_downloader" ]; then
        echo -e "${YELLOW}🔧 Creando entorno virtual...${NC}"
        python3 -m venv env_downloader
    else
        echo -e "${GREEN}✅ Entorno virtual ya existe.${NC}"
    fi

    # 4. Activar entorno virtual
    source env_downloader/bin/activate

    # 5. Actualizar pip e instalar yt-dlp (si no está en requirements)
    echo -e "${YELLOW}📦 Actualizando pip...${NC}"
    python3 -m pip install --upgrade pip

    echo -e "${YELLOW}📦 Instalando yt-dlp (pre-release)...${NC}"
    python3 -m pip install -U --pre "yt-dlp[default]"

    # 6. Instalar dependencias desde requirements.txt si existe
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}📦 Instalando dependencias desde requirements.txt...${NC}"
        pip3 install -r requirements.txt
    else
        echo -e "${YELLOW}⚠️  requirements.txt no encontrado. Omitiendo.${NC}"
    fi

    # 7. Ejecutar la interfaz gráfica en segundo plano
    if [ -f "MultiDownloaderv2.0.py" ]; then
        echo -e "${GREEN}🚀 Abriendo MultiDownloaderv2.0...${NC}"
        python3 MultiDownloaderv2.0.py > /dev/null 2>&1 &
        sleep 2
        echo -e "${GREEN}✅ Aplicación lanzada correctamente. Puedes cerrar esta terminal.${NC}"
    else
        echo -e "${RED}❌ No se encontró el archivo MultiDownloaderv2.0.py. Verifica que estés en el directorio correcto.${NC}"
        exit 1
    fi

    # Desactivar entorno virtual (opcional, ya que la terminal se puede cerrar)
    deactivate
}

# ---- Ejecución ----
main
