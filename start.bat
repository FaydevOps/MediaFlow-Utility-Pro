@echo off
title MultiDownloader - Inicializador

:: OBLIGAR AL SCRIPT A TRABAJAR EN SU PROPIA CARPETA
cd /d "%~dp0"

cls

echo ===================================================
echo    Verificando entorno y actualizando dependencias  
echo ===================================================
echo.

:: 1. Verificar si Python está instalado
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no se agrego al PATH.
    echo Por favor, instala Python antes de continuar.
    pause
    exit
)

:: 2. Actualizar Pip de forma silenciosa
echo [+] Actualizando el gestor de paquetes (pip)...
python -m pip install --upgrade pip --quiet

:: 3. Actualizar yt-dlp
echo [+] Actualizando yt-dlp a la ultima version...
python -m pip install -U --pre "yt-dlp[default]" --quiet

:: 4. Verificar e instalar requirements.txt
if exist requirements.txt (
    echo [+] Instalando dependencias del archivo requirements.txt...
    pip install -r requirements.txt --quiet
) else (
    echo [AVISO] No se encontro requirements.txt. Saltando este paso.
)

:: 5. Lanzar la aplicación gráfica
echo.
echo ===================================================
echo    Iniciando interfaz grafica de MultiDownloader...
echo ===================================================
echo.

:: Ejecutar la GUI en segundo plano
start "" pythonw MultiDownloaderv.py

timeout /t 2 >nul
exit
