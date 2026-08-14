# 🛡️ MediaFlow Utility Pro

<p align="center">
  <b>🌐 Selecciona tu idioma / Select your language:</b><br>
  <a href="./README.md">🇪🇸 Español</a> | <a href="./README_EN.md">🇬🇧 English</a>
</p>

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

### ✨ Características Principales y Nuevas Funciones

* **🎨 GUI Moderna e Intuitiva:** Desarrollada con **CustomTkinter** para una experiencia visual limpia, responsiva y adaptable.
* **📋 Cola de Descargas Multilínea (Nuevo):** Agrega múltiples enlaces a la vez pegando una lista de URLs en el campo multilínea o importando un archivo de texto plano (`.txt`).
* **🎵 Metadatos ID3 y Carátulas Automáticas (Nuevo):** Opción integrada para incrustar automáticamente la miniatura como carátula del archivo y los metadatos de la canción en descargas de audio.
* **🔔 Notificaciones del Sistema (Nuevo):** Alerta nativa en el escritorio al completar las tareas de descarga de la cola.
* **⚡ Gestión Avanzada con yt-dlp:** Soporte para resoluciones personalizadas (hasta 4K/2160p), conversión de contenedores (MP4, MKV, WebM, MP3, WAV, M4A) y gestión de listas de reproducción (*playlists*).
* **🔒 Rotación y Gestión de Proxies:** Soporte para proxies HTTP/SOCKS5, carga mediante APIs públicas/personalizadas y prueba de latencia.
* **🔑 Soporte de Autenticación:** Importación automática de *cookies* de sesión desde navegadores (Chrome, Firefox, Edge, Brave, Opera, Safari) para acceder a contenido privado de plataformas donde poseas una suscripción legítima.
* **🚀 Lanzadores Automáticos Multiplataforma (Nuevo):** Incluye scripts de inicio rápido (`start.sh` y `start.bat`) que automatizan la verificación y ejecución del programa.
* **📱 Modo Híbrido (CLI/GUI):** Detección automática del entorno; si se ejecuta en **Termux (Android)** o sin entorno gráfico, conmuta automáticamente al modo consola (CLI).

---

### 🚀 Requisitos e Instalación

> **Requisito Obligatorio:** La herramienta requiere **FFmpeg** para procesar, extraer y fusionar flujos de audio y video de alta calidad.

#### 1. Instalación de FFmpeg y Clonación

| Sistema | Método de Instalación |
| :--- | :--- |
| **Clonar Repositorio** | Ejecute: `git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro` |
| **Windows** | **1.** Descargue los binarios desde [FFmpeg Official Site](https://ffmpeg.org/download.html).<br>**2.** Descomprima en una ubicación accesible (ej: `C:\ffmpeg`).<br>**3. Crucial:** Añada la carpeta `C:\ffmpeg\bin` a la variable de entorno **PATH** de Windows. |
| **Linux (Ubuntu/Debian)** | Ejecute: `sudo apt update && sudo apt install ffmpeg python3 -y` |
| **macOS** | Ejecute (vía Homebrew): `brew install ffmpeg python` |
| **Termux (Android)** | Ejecute: `pkg update && pkg install ffmpeg python -y` |

---

#### 2. Formas de Ejecución

##### 🟢 Opción A: Scripts de Inicio Rápido (Recomendado)

El repositorio incluye ejecutable/lanzadores que simplifican el inicio en cualquier sistema operativo:

* **Windows (10 / 11):**  
  Haz doble clic sobre el archivo `start.bat`.
* **Linux / macOS:**  
  Otorga permisos de ejecución e inícialo desde la terminal:
  ```bash
  chmod +x start.sh
  ./start.sh
