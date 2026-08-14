
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

### ✨ Key Features and What's New

* **🎨 Modern and Intuitive GUI:** Built with **CustomTkinter** for a clean, responsive, and adaptable visual experience.
* **📋 Multiline Download Queue (New):** Add multiple links at once by pasting a list of URLs into the multiline input field or importing a plain text file (`.txt`).
* **🎵 ID3 Metadata & Auto Cover Art (New):** Integrated option to automatically embed thumbnails as album covers and song metadata for audio downloads.
* **🔔 System Notifications (New):** Native desktop alerts upon completing queue download tasks.
* **⚡ Advanced Management with yt-dlp:** Support for custom resolutions (up to 4K/2160p), container conversion (MP4, MKV, WebM, MP3, WAV, M4A), and playlist management.
* **🔒 Proxy Management & Rotation:** Support for HTTP/SOCKS5 proxies, loading via public/custom APIs, and latency testing.
* **🔑 Authentication Support:** Automatic session *cookies* import from browsers (Chrome, Firefox, Edge, Brave, Opera, Safari) to access private content from platforms where you hold a valid subscription.
* **🚀 Cross-Platform Auto Launchers (New):** Includes quick-start scripts (`start.sh` and `start.bat`) that automate environment check and application launch.
* **📱 Hybrid Mode (CLI/GUI):** Automatic environment detection; if run on **Termux (Android)** or headless environments, it automatically switches to console mode (CLI).

---

### 🚀 Requirements and Installation

> **Mandatory Requirement:** The tool requires **FFmpeg** to process, extract, and merge high-quality audio and video streams.

#### 1. Installing FFmpeg and Cloning

| System | Installation Method |
| :--- | :--- |
| **Clone Repo** | Run: `git clone https://github.com/FaydevOps/MediaFlow-Utility-Pro` |
| **Windows** | **1.** Download binaries from [FFmpeg Official Site](https://ffmpeg.org/download.html).<br>**2.** Extract to an accessible location (e.g., `C:\ffmpeg`).<br>**3. Crucial:** Add the `C:\ffmpeg\bin` folder to the Windows **PATH** environment variable. |
| **Linux (Ubuntu/Debian)** | Run: `sudo apt update && sudo apt install ffmpeg python3 -y` |
| **macOS** | Run (via Homebrew): `brew install ffmpeg python` |
| **Termux (Android)** | Run: `pkg update && pkg install ffmpeg python -y` |

---

#### 2. How to Run

##### 🟢 Option A: Quick Start Scripts (Recommended)

The repository includes launchers that simplify startup across any operating system:

* **Windows (10 / 11):**  
  Double-click the `start.bat` file.
* **Linux / macOS:**  
  Grant execution permissions and run it from the terminal:
  ```bash
  chmod +x start.sh
  ./start.sh
