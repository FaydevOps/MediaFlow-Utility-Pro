# 🛡️ MediaFlow Utility Pro

<p align="center">
  <b>🌐 Selecciona tu idioma / Select your language:</b><br>
  <a href="./README.md">🇪🇸 Español</a> | <a href="./README_EN.md">🇬🇧 English</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="yt-dlp" src="https://img.shields.io/badge/motor-yt--dlp-red">
  <img alt="Plataformas" src="https://img.shields.io/badge/plataformas-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-informational">
  <img alt="Licencia" src="https://img.shields.io/badge/licencia-MIT-green">
</p>

Aplicación de escritorio en **Python + CustomTkinter** para descargar y convertir video y audio de [más de 1800 sitios](SitiosSoportados.txt), usando el motor de código abierto **yt-dlp**. Incluye una versión de consola para **Termux (Android)**.

> **Nota de licencia:** proyecto *Open Source* bajo licencia [MIT](LICENSE). Todo el código fuente está en este repositorio. Los binarios compilados, si se publican, se ofrecen solo por comodidad del usuario final.

---

## 📑 Contenido

- [Vista previa](#-vista-previa)
- [Descargo de responsabilidad](#-descargo-de-responsabilidad-legal)
- [Características](#-características)
- [Instalación](#-instalación)
- [Ejecución](#️-ejecución)
- [Guía de uso](#-guía-de-uso)
- [Archivos que crea la aplicación](#-archivos-que-crea-la-aplicación)
- [Solución de problemas](#️-solución-de-problemas)
- [Licencia y apoyo](#-licencia-y-apoyo)

---

## 📸 Vista previa

<p align="center">
  <img width="1897" height="1011" alt="Interfaz de MediaFlow Utility Pro" src="https://github.com/user-attachments/assets/b8caefe6-114d-45a1-8629-164ab19a7d1a" />
</p>

---

## 🛑 Descargo de responsabilidad legal

> **⚠️ IMPORTANTE:** **MediaFlow Utility Pro** existe exclusivamente para gestionar y descargar contenido al que el usuario ya tiene derecho de acceso legal, o que está en dominio público o bajo licencias Creative Commons.

* **Responsabilidad del usuario:** el usuario es el único responsable de que su uso cumpla las leyes locales, los derechos de autor y los términos de servicio de cada plataforma.
* **Uso no promovido:** los desarrolladores **NO** avalan ni promueven el uso de esta herramienta para infringir la propiedad intelectual.
* **Cualquier uso indebido es responsabilidad exclusiva del usuario final.**

---

## ✨ Características

**Descargas**
* **📋 Cola de descargas:** pega varias URLs (una por línea), usa el botón **Pegar** o importa un `.txt`. Un contador muestra cuántas hay en cola.
* **🎯 El formato que eliges es el que obtienes:** si el sitio no ofrece ese formato, el archivo se convierte al final. En mp4 y mkv solo se copian los streams (*remux*), así que tarda segundos y no pierde calidad.
* **🎞️ Video:** MP4, MKV o WebM, con resolución máxima de 480p a 4K (2160p).
* **🎵 Audio:** MP3, M4A o WAV a 192 kbps.
* **⏹️ Cancelar en cualquier momento:** detiene la cola y borra los archivos a medias (`.part`, streams sin unir, miniaturas). Nunca borra un archivo ya terminado.
* **📊 Progreso detallado:** título, porcentaje, velocidad, tiempo restante y posición en la cola (`Cola 2/5`). Al terminar, un resumen indica cuántas descargas funcionaron y cuáles fallaron.

**Metadatos**
* **🏷️ Etiquetas limpias para música:** de un título como `Artista - Canción (Official Video) [4K]` obtiene el artista `Artista` y el título `Canción`. También escribe fecha, género, descripción, URL de origen y capítulos.
* **🖼️ Carátula incrustada:** cuadrada en MP3 y M4A (como en los reproductores de música) y con la miniatura original en MP4 y MKV. WAV y WebM no admiten carátula; en ellos solo se escriben las etiquetas.

**Red y autenticación**
* **🔑 Cookies:** desde un archivo `cookies.txt` (formato Netscape) o leídas directamente de tu navegador (Firefox, Chrome, Edge, Brave, Opera). Permiten descargar contenido que requiere iniciar sesión en una cuenta válida.
* **🔒 Proxies HTTP / SOCKS5:** se obtienen de listas públicas o de tus propias APIs, se editan a mano y se prueba cuáles funcionan.

**Otros**
* **🎨 Interfaz moderna** en tema oscuro, que se adapta a pantallas pequeñas.
* **✅ Detección de FFmpeg:** la app avisa si no lo encuentra.
* **🔔 Notificaciones de Windows** al terminar la cola (opcional, ver [instalación](#2-dependencias-de-python)).
* **🚀 Lanzadores** `start.bat` (Windows) y `start.sh` (Linux/macOS): instalan dependencias, actualizan yt-dlp y abren la app.
* **📱 Versión de consola para Termux:** un script aparte en `termux_version/`, con menú interactivo.

---

## 🚀 Instalación

> **Requisitos:** **Python 3.10+** y **FFmpeg**. Sin FFmpeg no se pueden unir audio y video, convertir formatos ni incrustar metadatos.

### 1. FFmpeg, Python y el repositorio

```bash
git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro
cd MediaFlow-Utility-Pro
```

| Sistema | Comando |
| :--- | :--- |
| **Windows** | `winget install Gyan.FFmpeg` (o descarga los binarios de [ffmpeg.org](https://ffmpeg.org/download.html) y añade su carpeta `bin` al **PATH**) |
| **Debian / Ubuntu** | `sudo apt install ffmpeg python3 python3-pip python3-venv python3-tk` |
| **Arch** | `sudo pacman -S ffmpeg python python-pip tk` |
| **Fedora** | `sudo dnf install ffmpeg python3 python3-pip python3-tkinter` |
| **macOS** | `brew install ffmpeg python python-tk` (requiere [Homebrew](https://brew.sh)) |
| **Termux (Android)** | `pkg update && pkg install ffmpeg python` |

> En Linux, el paquete **tk** (`python3-tk` / `tk` / `python3-tkinter`) es necesario para la interfaz gráfica.

### 2. Dependencias de Python

> Si usas los lanzadores `start.bat` o `start.sh`, puedes saltarte este paso: lo hacen ellos.

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Opcional:** para recibir notificaciones de Windows al terminar la cola, instala también `pip install win10toast`.

---

## ▶️ Ejecución

### 🟢 Opción A: lanzadores (recomendado)

Instalan o actualizan las dependencias y yt-dlp, y luego abren la interfaz.

* **Windows 10 / 11:** doble clic en `start.bat`.
* **Linux / macOS:** también instala los paquetes del sistema y crea un entorno virtual `env_downloader`.
  ```bash
  chmod +x start.sh
  ./start.sh
  ```

### 🔵 Opción B: manual

Con las dependencias ya instaladas (y el entorno virtual activado, si lo usas):

```bash
python MultiDownloaderv.py
```

### 📱 Opción C: Termux (Android)

```bash
termux-setup-storage            # permite guardar en ~/storage/downloads
pip install yt-dlp rich requests
cd termux_version
bash termuxupdate.sh            # actualiza yt-dlp y abre el menú
```

La versión de consola descarga una URL a la vez: video + audio, solo audio o solo video, con elección de calidad, formato y proxy.

---

## 📖 Guía de uso

1. **Añade las URLs:** pégalas en la caja (una por línea), usa **📋 Pegar** o **📂 Importar .txt**.
2. **Elige el destino:** botón **Buscar**. Por defecto es tu carpeta `Descargas`.
3. **Elige formato y calidad:**

   | Quiero… | Formato Video | Formato Audio | Botón |
   | :--- | :--- | :--- | :--- |
   | Video tal como lo da el sitio | `Original` | `Original` | **⬇️ DESCARGAR COLA** |
   | Video en un formato concreto | `mp4` / `mkv` / `webm` | — | **⬇️ DESCARGAR COLA** o **🎬 Solo Video** |
   | Solo el audio | — | `mp3` / `m4a` / `wav` | **🎵 Solo Audio** |

   * **Resolución Video** es un máximo: con `1080p` se baja la mejor calidad disponible hasta 1080p.
   * **🎵 Solo Audio** y **🎬 Solo Video** usan el formato elegido en el menú; si está en `Original`, usan MP3 y MP4.
4. **Metadatos:** deja marcada *"Incrustar carátula y metadatos"* para que el archivo lleve título, artista y carátula.
5. **Descarga:** sigue el progreso en la barra inferior. Pulsa **⏹ Cancelar** para detener la cola.

### 🔑 Contenido que requiere iniciar sesión

Activa **"Usar autenticación (cookies)"** y elige el método:

* **archivo** *(el más fiable)*: exporta las cookies con una extensión como *Get cookies.txt LOCALLY* y cárgalas con **Seleccionar cookies.txt**. El botón **Ayuda** explica el formato.
* **navegador:** la app lee las cookies del navegador elegido. Con **Firefox** funciona bien. Chrome, Edge, Brave y Opera cifran sus cookies en Windows y pueden fallar; en ese caso usa el método *archivo*.

### 🔒 Proxies

Activa **Habilitar Proxy** y elige `http` o `socks5`. Botones:
* **Obtener:** descarga listas de proxies públicos.
* **Gestionar:** edita la lista a mano.
* **APIs:** añade tus propias URLs de listas de proxies.
* **Probar:** comprueba cuáles de los 5 primeros de cada tipo funcionan.

En cada descarga se usa un proxy al azar de la lista.

---

## 📂 Archivos que crea la aplicación

Se guardan junto a `MultiDownloaderv.py`:

| Archivo | Contenido |
| :--- | :--- |
| `cookies.txt` | Copia de tus cookies. **Contiene tus sesiones iniciadas: no lo compartas ni lo subas a GitHub.** |
| `proxies.json` | Lista de proxies HTTP y SOCKS5. |
| `custom_apis.json` | Tus URLs de listas de proxies. |

---

## 🛠️ Solución de problemas

| Problema | Solución |
| :--- | :--- |
| ⚠️ *"FFmpeg no encontrado"* | Instálalo (ver [instalación](#1-ffmpeg-python-y-el-repositorio)) y reinicia la app, o indica el ejecutable con **Seleccionar** en la fila FFmpeg. |
| En Linux la app no abre: `No module named 'tkinter'` | Instala `python3-tk` (Debian/Ubuntu), `tk` (Arch) o `python3-tkinter` (Fedora). |
| Falla una descarga de YouTube o faltan calidades | Actualiza yt-dlp con `pip install -U yt-dlp` (los lanzadores lo hacen solos). Si yt-dlp avisa de que falta un *JavaScript runtime*, instala [Deno](https://deno.com). |
| La conversión a **WebM** tarda | Solo ocurre si el sitio no ofrece WebM y hay que recodificar. MP4 y MKV no recodifican. |
| Las cookies de Chrome o Edge no funcionan | Usa el método *archivo* o Firefox (ver [cookies](#-contenido-que-requiere-iniciar-sesión)). |
| Un video muestra error | El resumen final lista las URLs que fallaron. Suelen ser videos privados, con restricción de edad (usa cookies) o bloqueados por región (usa un proxy). |

---

## 📜 Licencia y apoyo

Distribuido bajo licencia **[MIT](LICENSE)**. Desarrollado por **FayDev**.

Si te resulta útil, puedes apoyar el proyecto desde el botón **💖 Apoyar** de la aplicación.
