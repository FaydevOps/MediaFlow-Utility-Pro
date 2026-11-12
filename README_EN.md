# 🛡️ MediaFlow Utility Pro

<p align="center">
  <b>🌐 Select your language / Selecciona tu idioma:</b><br>
  <a href="./README.md">🇪🇸 Español</a> | <a href="./README_EN.md">🇬🇧 English</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="yt-dlp" src="https://img.shields.io/badge/engine-yt--dlp-red">
  <img alt="Platforms" src="https://img.shields.io/badge/platforms-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-informational">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

A **Python + CustomTkinter** desktop app for downloading and converting video and audio from [1800+ sites](SitiosSoportados.txt), powered by the open-source **yt-dlp** engine. It also includes a console version for **Termux (Android)**.

> **License note:** *Open Source* project under the [MIT](LICENSE) license. All source code is in this repository. Compiled binaries, when published, are offered only for end-user convenience.

---

## 📑 Contents

- [Preview](#-preview)
- [Legal disclaimer](#-legal-disclaimer)
- [Features](#-features)
- [Installation](#-installation)
- [Running the app](#️-running-the-app)
- [Usage guide](#-usage-guide)
- [Files created by the app](#-files-created-by-the-app)
- [Troubleshooting](#️-troubleshooting)
- [License and support](#-license-and-support)

---

## 📸 Preview

<p align="center">
  <img width="1897" height="1011" alt="MediaFlow Utility Pro interface" src="https://github.com/user-attachments/assets/fb40f455-3b6a-4a5e-990a-2f5dd9fa67c9" />
</p>

---

## 🛑 Legal disclaimer

> **⚠️ IMPORTANT:** **MediaFlow Utility Pro** exists solely to manage and download content that the user already has the legal right to access, or that is in the public domain or under Creative Commons licenses.

* **User responsibility:** the user alone is responsible for making sure their use complies with local laws, copyright, and each platform's terms of service.
* **Not endorsed:** the developers **DO NOT** support or promote using this tool to infringe intellectual property.
* **Any misuse is the sole responsibility of the end user.**

---

## ✨ Features

**Downloads**
* **📋 Download queue:** paste several URLs (one per line), use the **Paste** button, or import a `.txt` file. A counter shows how many are queued.
* **🎯 You get the format you pick:** if the site doesn't offer that format, the file is converted at the end. For mp4 and mkv the streams are just copied (*remux*), so it takes seconds and loses no quality.
* **🎞️ Video:** MP4, MKV, or WebM, with a maximum resolution from 480p up to 4K (2160p).
* **🎵 Audio:** MP3, M4A, or WAV at 192 kbps.
* **⏹️ Cancel anytime:** stops the queue and removes partial files (`.part`, unmerged streams, thumbnails). It never deletes a finished file.
* **📊 Detailed progress:** title, percentage, speed, time left, and queue position (`Cola 2/5`). When the queue ends, a summary shows how many downloads succeeded and which ones failed.

**Metadata**
* **🏷️ Clean music tags:** from a title like `Artist - Song (Official Video) [4K]` it gets the artist `Artist` and the title `Song`. It also writes date, genre, description, source URL, and chapters.
* **🖼️ Embedded cover art:** square in MP3 and M4A (like music players show it) and the original thumbnail in MP4 and MKV. WAV and WebM can't hold cover art; they only get the tags.

**Network and authentication**
* **🔑 Cookies:** from a `cookies.txt` file (Netscape format) or read straight from your browser (Firefox, Chrome, Edge, Brave, Opera). They let you download content that requires signing in to a valid account.
* **🔒 HTTP / SOCKS5 proxies:** fetched from public lists or your own APIs, editable by hand, and testable to see which ones work.

**Other**
* **🎨 Modern dark-themed interface** that fits small screens.
* **✅ FFmpeg detection:** the app warns you if it can't find it.
* **🔔 Windows notifications** when the queue finishes (optional, see [installation](#2-python-dependencies)).
* **🚀 Launchers** `start.bat` (Windows) and `start.sh` (Linux/macOS): they install dependencies, update yt-dlp, and open the app.
* **📱 Console version for Termux:** a separate script in `termux_version/` with an interactive menu.

---

## 🚀 Installation

> **Requirements:** **Python 3.10+** and **FFmpeg**. Without FFmpeg the app can't merge audio and video, convert formats, or embed metadata.

### 1. FFmpeg, Python, and the repository

```bash
git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro
cd MediaFlow-Utility-Pro
```

| System | Command |
| :--- | :--- |
| **Windows** | `winget install Gyan.FFmpeg` (or download the binaries from [ffmpeg.org](https://ffmpeg.org/download.html) and add their `bin` folder to the **PATH**) |
| **Debian / Ubuntu** | `sudo apt install ffmpeg python3 python3-pip python3-venv python3-tk` |
| **Arch** | `sudo pacman -S ffmpeg python python-pip tk` |
| **Fedora** | `sudo dnf install ffmpeg python3 python3-pip python3-tkinter` |
| **macOS** | `brew install ffmpeg python python-tk` (requires [Homebrew](https://brew.sh)) |
| **Termux (Android)** | `pkg update && pkg install ffmpeg python` |

> On Linux, the **tk** package (`python3-tk` / `tk` / `python3-tkinter`) is required for the graphical interface.

### 2. Python dependencies

> If you use the `start.bat` or `start.sh` launchers, you can skip this step: they do it for you.

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Optional:** to get Windows notifications when the queue finishes, also install `pip install win10toast`.

---

## ▶️ Running the app

### 🟢 Option A: launchers (recommended)

They install or update the dependencies and yt-dlp, then open the interface.

* **Windows 10 / 11:** double-click `start.bat`.
* **Linux / macOS:** also installs the system packages and creates an `env_downloader` virtual environment.
  ```bash
  chmod +x start.sh
  ./start.sh
  ```

### 🔵 Option B: manual

With the dependencies installed (and the virtual environment activated, if you use one):

```bash
python MultiDownloaderv.py
```

### 📱 Option C: Termux (Android)

```bash
termux-setup-storage            # lets the app save to ~/storage/downloads
pip install yt-dlp rich requests
cd termux_version
bash termuxupdate.sh            # updates yt-dlp and opens the menu
```

The console version downloads one URL at a time: video + audio, audio only, or video only, with your choice of quality, format, and proxy.

---

## 📖 Usage guide

1. **Add the URLs:** paste them into the box (one per line), or use **📋 Pegar** (Paste) or **📂 Importar .txt** (Import).
2. **Pick the destination:** **Buscar** (Browse) button. Your `Downloads` folder is the default.
3. **Pick format and quality:**

   | I want… | Formato Video | Formato Audio | Button |
   | :--- | :--- | :--- | :--- |
   | Video as the site provides it | `Original` | `Original` | **⬇️ DESCARGAR COLA** (Download queue) |
   | Video in a specific format | `mp4` / `mkv` / `webm` | — | **⬇️ DESCARGAR COLA** or **🎬 Solo Video** (Video only) |
   | Audio only | — | `mp3` / `m4a` / `wav` | **🎵 Solo Audio** (Audio only) |

   * **Resolución Video** (video resolution) is a maximum: with `1080p` you get the best quality available up to 1080p.
   * **🎵 Solo Audio** and **🎬 Solo Video** use the format picked in the menu; when it's set to `Original`, they use MP3 and MP4.
4. **Metadata:** keep *"Incrustar carátula y metadatos"* (embed cover and metadata) checked so the file gets title, artist, and cover art.
5. **Download:** follow the progress in the bottom bar. Press **⏹ Cancelar** (Cancel) to stop the queue.

> The interface is in Spanish; button names are translated in parentheses.

### 🔑 Content that requires signing in

Enable **"Usar autenticación (cookies)"** (use authentication) and pick a method:

* **archivo** (file) *(most reliable)*: export your cookies with an extension such as *Get cookies.txt LOCALLY* and load them with **Seleccionar cookies.txt**. The **Ayuda** (Help) button explains the format.
* **navegador** (browser): the app reads the cookies of the chosen browser. **Firefox** works well. Chrome, Edge, Brave, and Opera encrypt their cookies on Windows and may fail; if so, use the *archivo* method.

### 🔒 Proxies

Enable **Habilitar Proxy** (enable proxy) and pick `http` or `socks5`. Buttons:
* **Obtener** (Fetch): downloads public proxy lists.
* **Gestionar** (Manage): edit the list by hand.
* **APIs:** add your own proxy-list URLs.
* **Probar** (Test): checks which of the first 5 of each type work.

Each download uses a random proxy from the list.

---

## 📂 Files created by the app

They're saved next to `MultiDownloaderv.py`:

| File | Contents |
| :--- | :--- |
| `cookies.txt` | A copy of your cookies. **It contains your signed-in sessions: don't share it or push it to GitHub.** |
| `proxies.json` | HTTP and SOCKS5 proxy lists. |
| `custom_apis.json` | Your proxy-list URLs. |

---

## 🛠️ Troubleshooting

| Problem | Fix |
| :--- | :--- |
| ⚠️ *"FFmpeg no encontrado"* (FFmpeg not found) | Install it (see [installation](#1-ffmpeg-python-and-the-repository)) and restart the app, or point to the executable with **Seleccionar** in the FFmpeg row. |
| On Linux the app won't open: `No module named 'tkinter'` | Install `python3-tk` (Debian/Ubuntu), `tk` (Arch), or `python3-tkinter` (Fedora). |
| A YouTube download fails or qualities are missing | Update yt-dlp with `pip install -U yt-dlp` (the launchers do it automatically). If yt-dlp warns about a missing *JavaScript runtime*, install [Deno](https://deno.com). |
| Converting to **WebM** is slow | It only happens when the site doesn't offer WebM and the video must be re-encoded. MP4 and MKV never re-encode. |
| Chrome or Edge cookies don't work | Use the *archivo* method or Firefox (see [cookies](#-content-that-requires-signing-in)). |
| A video shows an error | The final summary lists the failed URLs. Common causes: private videos, age-restricted videos (use cookies), or region blocks (use a proxy). |

---

## 📜 License and support

Released under the **[MIT](LICENSE)** license. Developed by **FayDev**.

If you find it useful, you can support the project with the **💖 Apoyar** (Support) button in the app.
