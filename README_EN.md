# 🛡️ MediaFlow Utility Pro

> 🌐 **Language / Idioma:** English | [Versión en Español](README.md)

---

### Advanced Media Stream Manager

A desktop application (GUI) developed in **Python (CustomTkinter)** designed to manage, customize, and acquire media streams leveraging the power of the open-source engine **yt-dlp**.

> **License Note:** This project is *Open Source*. The complete source code is provided in this repository. The distribution of compiled binaries is offered for user convenience and intellectual property protection of the developer.

---

### 📸 Interface Preview (GUI)

<p align="center">
  <img src="https://github.com/user-attachments/assets/4702e7e2-583c-401f-93e5-e6273dab76a9" alt="MediaFlow Utility Pro GUI" width="700"/>
</p>

---

### 🛑 Legal Disclaimer

> **⚠️ IMPORTANT:** The purpose of **MediaFlow Utility Pro** is strictly to facilitate managing and downloading content that the user already has the legal right to access or that is available under Public Domain / Creative Commons licenses.

* **User Responsibility:** The user is entirely responsible for ensuring that the use of this software complies with all local laws, copyright regulations, and the terms of service of any source platform.
* **Not Endorsed:** The developers **DO NOT** support or promote the use of this tool to infringe upon intellectual property laws.
* **Any misuse is the sole responsibility of the end user.**

---

### ✨ Key Features

* **🎨 Modern and Intuitive GUI:** Built with **CustomTkinter** for a clean, responsive, and adaptable visual experience.
* **📋 Multiline Download Queue:** Add multiple links at once by pasting a list of URLs or importing a `.txt` file.
* **🎵 ID3 Metadata & Auto Cover Art:** Integrated option to automatically embed thumbnails as album covers and song metadata for audio downloads.
* **🔔 System Notifications:** Native desktop alerts upon completing download tasks.
* **⚡ Advanced Management with yt-dlp:** Support for custom resolutions (up to 4K/2160p), container conversion (MP4, MKV, WebM, MP3, WAV, M4A), and playlist management.
* **🔒 Proxy Management & Rotation:** Support for HTTP/SOCKS5 proxies, loading via public/custom APIs, and latency testing.
* **🔑 Authentication Support:** Automatic session cookies import from browsers to access private content from platforms where you hold a valid subscription.
* **🚀 Cross-Platform Auto Launchers:** Includes quick-start scripts (`start.sh` and `start.bat`) that automate environment check and application launch.
* **📱 Hybrid Mode (CLI/GUI):** Automatic environment detection; if run on **Termux (Android)** or headless environments, it automatically switches to console mode (CLI).

---

### 🚀 Requirements and Installation

> **Mandatory Requirement:** The tool requires **FFmpeg** to process, extract, and merge high-quality audio and video streams.

#### 1. Installing FFmpeg and Cloning

| System | Method |
| :--- | :--- |
| **Clone Repo** | `git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro` |
| **Windows** | Download binaries from [FFmpeg.org](https://ffmpeg.org/download.html), extract to `C:\ffmpeg` and add `C:\ffmpeg\bin` to the system **PATH**. |
| **Linux (Debian/Ubuntu)** | `sudo apt update && sudo apt install ffmpeg python3 python3-pip python3-venv -y` |
| **Linux (Arch)** | `sudo pacman -S ffmpeg python python-pip` |
| **Linux (Fedora)** | `sudo dnf install ffmpeg python3 python3-pip python3-virtualenv` |
| **macOS** | `brew install ffmpeg python` (requires Homebrew) |
| **Termux (Android)** | `pkg update && pkg install ffmpeg python -y` |

#### 2. Installing Python Dependencies and Virtual Environment

Inside the project folder:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: .\venv\Scripts\activate

# Install dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt
