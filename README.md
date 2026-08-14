# 🛡️ MediaFlow Utility Pro

<p align="center">
  <b>🌐 Selecciona tu idioma / Select your language:</b><br>
  <a href="./README.md">🇪🇸 Español</a> | <a href="./README_EN.md">🇬🇧 English</a>
</p>

---

### Advanced Media Stream Manager

Una aplicación de escritorio (GUI) desarrollada en **Python (CustomTkinter)** diseñada para gestionar, personalizar y adquirir flujos de medios utilizando la potencia del motor de código abierto **yt-dlp**.

> **Nota de Licencia:** Este proyecto es *Open Source*. El código fuente completo se proporciona en este repositorio. La distribución de binarios compilados se ofrece para conveniencia del usuario final y protección de la propiedad intelectual del desarrollador.

---

### 📸 Vista Previa de la Interfaz (GUI)

<p align="center">
  <img width="845" height="929" alt="image" src="https://github.com/user-attachments/assets/31e7bddb-ad60-4777-b747-f4c13355ff8f" />
</p>

---

### 🛑 Descargo de Responsabilidad Legal

> **⚠️ IMPORTANTE:** El propósito de **MediaFlow Utility Pro** es exclusivamente facilitar la gestión y descarga de contenido al que el usuario ya tiene derecho de acceso legal o que se encuentra bajo licencias de dominio público / Creative Commons.

* **Responsabilidad del Usuario:** El usuario es enteramente responsable de asegurar que el uso de este software cumpla con todas las leyes locales, las leyes de derechos de autor y los términos de servicio de cualquier plataforma fuente.
* **Uso No Promovido:** Los desarrolladores **NO** avalan ni promueven el uso de esta herramienta para infringir las leyes de propiedad intelectual.
* **Cualquier uso indebido es responsabilidad exclusiva del usuario final.**

---

### ✨ Características Principales

* **🎨 GUI Moderna e Intuitiva:** Desarrollada con **CustomTkinter** para una experiencia visual limpia, responsiva y adaptable.
* **📋 Cola de Descargas Multilínea:** Agrega múltiples enlaces a la vez pegando una lista de URLs o importando un archivo `.txt`.
* **🎵 Metadatos ID3 y Carátulas Automáticas:** Opción integrada para incrustar automáticamente la miniatura como carátula y los metadatos en descargas de audio.
* **🔔 Notificaciones del Sistema:** Alertas nativas al completar las descargas.
* **⚡ Gestión Avanzada con yt-dlp:** Resoluciones hasta 4K, conversión de contenedores (MP4, MKV, WebM, MP3, WAV, M4A) y soporte para listas de reproducción.
* **🔒 Rotación y Gestión de Proxies:** Soporte para HTTP/SOCKS5, carga mediante APIs y prueba de latencia.
* **🔑 Autenticación con Cookies:** Importación automática desde navegadores para acceder a contenido privado con suscripción válida.
* **🚀 Lanzadores Automáticos Multiplataforma:** Scripts `start.sh` y `start.bat` que verifican el entorno y lanzan la app.
* **📱 Modo Híbrido (CLI/GUI):** Detecta automáticamente si se ejecuta en Termux (Android) o sin entorno gráfico y cambia a modo consola.

---

### 🚀 Requisitos e Instalación

> **Requisito Obligatorio:** La herramienta requiere **FFmpeg** para procesar, extraer y fusionar flujos de audio y video.

#### 1. Instalación de FFmpeg y clonación del repositorio

| Sistema | Comando / Método |
| :--- | :--- |
| **Clonar Repositorio** | `git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro` |
| **Windows** | Descarga binarios desde [FFmpeg.org](https://ffmpeg.org/download.html), extrae en `C:\ffmpeg` y añade `C:\ffmpeg\bin` al **PATH** del sistema. |
| **Linux (Debian/Ubuntu)** | `sudo apt update && sudo apt install ffmpeg python3 python3-pip python3-venv -y` |
| **Linux (Arch)** | `sudo pacman -S ffmpeg python python-pip` |
| **Linux (Fedora)** | `sudo dnf install ffmpeg python3 python3-pip python3-virtualenv` |
| **macOS** | `brew install ffmpeg python` (requiere Homebrew) |
| **Termux (Android)** | `pkg update && pkg install ffmpeg python -y` |

#### 2. Instalación de dependencias Python y entorno virtual

Una vez dentro de la carpeta del proyecto:

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate   # En Windows: .\venv\Scripts\activate

# Instalar dependencias desde requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
