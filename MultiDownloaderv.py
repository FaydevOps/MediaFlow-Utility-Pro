import os
import sys
import time
import json
import shutil
import random
import threading
import subprocess
import tempfile
import urllib.request
import tkinter as tk
from tkinter import messagebox as MessageBox
from tkinter import filedialog
from PIL import Image, ImageTk 
import customtkinter as ctk 
from yt_dlp import YoutubeDL

# Intento de importar win10toast para notificaciones nativas en Windows
try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
except ImportError:
    toaster = None

# Configuración Global de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ========== PALETA DE COLORES ==========
BG_COLOR = "#0F172A"       # Fondo principal (Slate oscuro)
CARD_BG = "#1E293B"        # Fondo de tarjetas
CARD_BORDER = "#334155"    # Borde sutil
ACCENT_BLUE = "#3B82F6"    # Botón primario
ACCENT_GREEN = "#10B981"   # Acciones positivas
ACCENT_ORANGE = "#F59E0B"  # Advertencias/APIs
TEXT_MAIN = "#F8FAFC"      # Texto principal
TEXT_MUTED = "#94A3B8"     # Texto secundario


# ========== FUNCIONES AUXILIARES ==========

def send_notification(title, message):
    if toaster:
        try:
            threading.Thread(target=toaster.show_toast, args=(title, message), kwargs={'duration': 5, 'threaded': True}).start()
        except Exception:
            pass

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    ]
    return random.choice(user_agents)

def detect_installed_browsers():
    browsers = []
    browser_paths = {
        'chrome': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
        ],
        'firefox': [
            os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Mozilla Firefox', 'firefox.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Mozilla Firefox', 'firefox.exe'),
        ],
        'edge': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
        ],
        'opera': [
            os.path.join(os.environ.get('APPDATA', ''), 'Opera Software', 'Opera Stable'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Opera'),
        ],
        'brave': [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'BraveSoftware', 'Brave-Browser', 'User Data'),
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe'),
        ],
    }
    
    if sys.platform != 'win32':
        if sys.platform == 'darwin':
            browser_paths['chrome'].append(os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Google', 'Chrome'))
            browser_paths['firefox'].append(os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'Firefox', 'Profiles'))
        else:
            browser_paths['chrome'].append(os.path.join(os.path.expanduser('~'), '.config', 'google-chrome'))
            browser_paths['firefox'].append(os.path.join(os.path.expanduser('~'), '.mozilla', 'firefox'))
    
    for browser, paths in browser_paths.items():
        for path in paths:
            if os.path.exists(path):
                if browser not in browsers:
                    browsers.append(browser)
                break
    return browsers

# ========== GESTIÓN DE PROXIES Y APIS CUSTOM ==========

def load_proxy_list():
    proxy_file = os.path.join(get_base_path(), "proxies.json")
    if os.path.exists(proxy_file):
        try:
            with open(proxy_file, 'r') as f:
                proxies = json.load(f)
                return proxies.get('http', []), proxies.get('socks5', [])
        except:
            pass
    return [], []

def save_proxy_list(http_proxies, socks5_proxies):
    proxy_file = os.path.join(get_base_path(), "proxies.json")
    proxy_data = {'http': http_proxies, 'socks5': socks5_proxies}
    try:
        with open(proxy_file, 'w') as f:
            json.dump(proxy_data, f, indent=2)
        return True
    except:
        return False

def load_custom_apis():
    api_file = os.path.join(get_base_path(), "custom_apis.json")
    if os.path.exists(api_file):
        try:
            with open(api_file, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'http': [], 'socks5': []}

def save_custom_apis(apis_dict):
    api_file = os.path.join(get_base_path(), "custom_apis.json")
    try:
        with open(api_file, 'w') as f:
            json.dump(apis_dict, f, indent=2)
        return True
    except:
        return False

def get_proxies_from_api(proxy_type='http'):
    custom_apis = load_custom_apis()
    if proxy_type == 'http':
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ] + custom_apis.get('http', [])
    else:
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt"
        ] + custom_apis.get('socks5', [])
        
    headers = {'User-Agent': get_random_user_agent()}
    collected_proxies = []

    for url in sources:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    proxies_text = response.read().decode('utf-8', errors='ignore').strip()
                    proxies = [p.strip() for p in proxies_text.split('\n') if ':' in p]
                    if proxies:
                        collected_proxies.extend(proxies)
        except Exception:
            pass

    return list(dict.fromkeys(collected_proxies))

def get_random_proxy(proxy_type='http'):
    http_proxies, socks5_proxies = load_proxy_list()
    if proxy_type == 'http' and http_proxies:
        return random.choice(http_proxies)
    elif proxy_type == 'socks5' and socks5_proxies:
        return random.choice(socks5_proxies)
    return None

def test_proxy(proxy, proxy_type='http'):
    try:
        handler = urllib.request.ProxyHandler({'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'})
        opener = urllib.request.build_opener(handler)
        opener.addheaders = [('User-Agent', get_random_user_agent())]
        response = opener.open('http://httpbin.org/ip', timeout=8)
        return response.getcode() == 200
    except:
        return False


# ========== CLASE PRINCIPAL DE INTERFAZ ==========

class MultiDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi Downloader Pro v4.0")
        master.geometry("850x900")
        master.minsize(780, 750)
        self.master.configure(fg_color=BG_COLOR)
        
        # Variables de estado
        self.video_resolution = ctk.StringVar(value="none")
        self.video_format = ctk.StringVar(value="none")
        self.audio_format = ctk.StringVar(value="none")
        self.output_path = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.ffmpeg_custom_path = ctk.StringVar(value="") 
        self.use_proxy = ctk.BooleanVar(value=False)
        self.proxy_type = ctk.StringVar(value="http")
        self.auto_retry_proxy = ctk.BooleanVar(value=True)
        self.auto_fetch_proxies = ctk.BooleanVar(value=True)
        self.use_browser_cookies = ctk.BooleanVar(value=False)
        self.embed_metadata = ctk.BooleanVar(value=True)
        
        self.installed_browsers = detect_installed_browsers()
        self.selected_browser = ctk.StringVar(value=self.installed_browsers[0] if self.installed_browsers else "ninguno")

        # --- CABECERA (HEADER CON LOGO) ---
        self.header_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.header_frame.pack(fill=ctk.X, padx=25, pady=(15, 5))

        # Intentar cargar la imagen del logo desde 'assets/youtubemp3.png'
        logo_path = os.path.join(get_base_path(), "assets", "youtubemp3.png")
        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                self.logo_image_ctk = ctk.CTkImage(
                    dark_image=logo_image,
                    light_image=logo_image,
                    size=(50, 50)
                )
                logo_label = ctk.CTkLabel(self.header_frame, image=self.logo_image_ctk, text="")
                logo_label.pack(side=ctk.LEFT, padx=(0, 12))
            except Exception as e:
                print(f"Error al cargar el logo: {e}")

        # Contenedor de títulos
        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.pack(side=ctk.LEFT)

        title_label = ctk.CTkLabel(
            title_box, 
            text="Multi Downloader Pro", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_MAIN
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            title_box, 
            text="v4.0 • Universal Downloader", 
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        )
        subtitle_label.pack(anchor="w")

        # Botones de la cabecera (Acerca de / Apoyar)
        btn_donate = ctk.CTkButton(
            self.header_frame, text="💖 Apoyar", command=self.popup_donate,
            fg_color="#EC4899", hover_color="#DB2777", text_color="white", width=85, height=28, corner_radius=6
        )
        btn_donate.pack(side=ctk.RIGHT, padx=5)

        btn_about = ctk.CTkButton(
            self.header_frame, text="Acerca de", command=self.popup_author,
            fg_color=CARD_BG, hover_color=CARD_BORDER, text_color=TEXT_MAIN, width=85, height=28, corner_radius=6
        )
        btn_about.pack(side=ctk.RIGHT)

        # --- ÁREA SCROLLABLE PRINCIPAL ---
        self.scroll_container = ctk.CTkScrollableFrame(
            master, fg_color="transparent", corner_radius=0
        )
        self.scroll_container.pack(fill=ctk.BOTH, expand=True, padx=15, pady=5)

        # 1. TARJETA: COLA DE URLS
        self.build_url_card()

        # 2. TARJETA: RUTA Y FFMPEG
        self.build_paths_card()

        # 3. TARJETA: OPCIONES DE DESCARGA (Formatos/Calidad)
        self.build_options_card()

        # 4. TARJETA: CONFIGURACIÓN AVANZADA (Cookies & Proxies)
        self.build_advanced_card()

        # --- BARRA INFERIOR (FOOTER / ACCIONES) ---
        self.build_footer_actions(master)

    # ---------- MÉTODOS DE CONSTRUCCIÓN DE INTERFAZ ----------

    def build_card(self, title):
        """Crea un contenedor con estilo de tarjeta unificado"""
        card = ctk.CTkFrame(self.scroll_container, fg_color=CARD_BG, border_color=CARD_BORDER, border_width=1, corner_radius=10)
        card.pack(fill=ctk.X, pady=8, padx=10, ipadx=10, ipady=10)
        
        if title:
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_MAIN).pack(anchor="w", pady=(0, 8))
        return card

    def build_url_card(self):
        card = self.build_card("📋 Cola de Descargas")
        
        sub_header = ctk.CTkFrame(card, fg_color="transparent")
        sub_header.pack(fill=ctk.X, pady=(0, 5))
        
        ctk.CTkLabel(sub_header, text="Ingresa URLs (una por línea):", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side=ctk.LEFT)
        ctk.CTkButton(
            sub_header, text="📂 Importar .txt", command=self.load_txt_file, 
            width=110, height=24, fg_color=CARD_BORDER, hover_color="#475569", font=ctk.CTkFont(size=11)
        ).pack(side=ctk.RIGHT)

        self.url_textbox = ctk.CTkTextbox(card, height=90, corner_radius=8, font=('Consolas', 11))
        self.url_textbox.pack(fill=ctk.X)

    def build_paths_card(self):
        card = self.build_card("📁 Ubicaciones y Herramientas")
        
        # Carpeta Destino
        row1 = ctk.CTkFrame(card, fg_color="transparent")
        row1.pack(fill=ctk.X, pady=4)
        ctk.CTkLabel(row1, text="Destino:", width=80, anchor="w", font=ctk.CTkFont(size=11)).pack(side=ctk.LEFT)
        ctk.CTkEntry(row1, textvariable=self.output_path, state='readonly').pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=5)
        ctk.CTkButton(row1, text="Buscar", command=self.browse_directory, width=80, fg_color=ACCENT_BLUE).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(row1, text="Abrir", command=self.open_output_dir, width=60, fg_color=CARD_BORDER).pack(side=ctk.LEFT, padx=2)

        # Ruta FFmpeg
        row2 = ctk.CTkFrame(card, fg_color="transparent")
        row2.pack(fill=ctk.X, pady=4)
        ctk.CTkLabel(row2, text="FFmpeg:", width=80, anchor="w", font=ctk.CTkFont(size=11)).pack(side=ctk.LEFT)
        ctk.CTkEntry(row2, textvariable=self.ffmpeg_custom_path, state='readonly', placeholder_text="Opcional (para conversiones avanzadas)").pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=5)
        ctk.CTkButton(row2, text="Seleccionar", command=self.browse_ffmpeg_path, width=80, fg_color=CARD_BORDER).pack(side=ctk.LEFT, padx=2)

    def build_options_card(self):
        card = self.build_card("⚙️ Formato y Calidad")
        
        opts_frame = ctk.CTkFrame(card, fg_color="transparent")
        opts_frame.pack(fill=ctk.X)
        opts_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Res
        f1 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f1.grid(row=0, column=0, sticky="ew", padx=5)
        ctk.CTkLabel(f1, text="Resolución Video", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f1, variable=self.video_resolution, values=["none", "mejor", "2160p", "1440p", "1080p", "720p", "480p"]).pack(fill=ctk.X, pady=2)

        # Formato Video
        f2 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f2.grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkLabel(f2, text="Formato Video", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f2, variable=self.video_format, values=["none", "mp4", "webm", "mkv"]).pack(fill=ctk.X, pady=2)

        # Formato Audio
        f3 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f3.grid(row=0, column=2, sticky="ew", padx=5)
        ctk.CTkLabel(f3, text="Formato Audio", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f3, variable=self.audio_format, values=["none", "mp3", "wav", "m4a"]).pack(fill=ctk.X, pady=2)

        ctk.CTkCheckBox(
            card, text="Incrustar carátula y metadatos ID3 en descargas de audio", 
            variable=self.embed_metadata, font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=(10, 0))

    def build_advanced_card(self):
        card = self.build_card("🛡️ Red y Autenticación")

        # Cookies
        cook_frame = ctk.CTkFrame(card, fg_color="transparent")
        cook_frame.pack(fill=ctk.X, pady=(0, 8))
        
        ctk.CTkCheckBox(cook_frame, text="Usar cookies del navegador:", variable=self.use_browser_cookies, command=self.on_cookie_toggle, font=ctk.CTkFont(size=11)).pack(side=ctk.LEFT)
        if self.installed_browsers:
            ctk.CTkOptionMenu(cook_frame, variable=self.selected_browser, values=self.installed_browsers, width=120, height=24).pack(side=ctk.LEFT, padx=10)
        
        ctk.CTkButton(cook_frame, text="🔄 Detectar Navegadores", command=self.refresh_browsers, width=130, height=24, fg_color=CARD_BORDER, font=ctk.CTkFont(size=11)).pack(side=ctk.RIGHT)

        # Separador interno
        ctk.CTkFrame(card, height=1, fg_color=CARD_BORDER).pack(fill=ctk.X, pady=8)

        # Proxies
        proxy_head = ctk.CTkFrame(card, fg_color="transparent")
        proxy_head.pack(fill=ctk.X)
        
        ctk.CTkCheckBox(proxy_head, text="Habilitar Proxy", variable=self.use_proxy, font=ctk.CTkFont(size=11)).pack(side=ctk.LEFT)
        ctk.CTkOptionMenu(proxy_head, variable=self.proxy_type, values=["http", "socks5"], width=90, height=24).pack(side=ctk.LEFT, padx=10)

        proxy_btns = ctk.CTkFrame(card, fg_color="transparent")
        proxy_btns.pack(fill=ctk.X, pady=(8, 0))
        
        ctk.CTkButton(proxy_btns, text="Obtener", command=self.fetch_proxies_now, width=80, height=26, fg_color=ACCENT_GREEN).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(proxy_btns, text="Gestionar", command=self.manage_proxies, width=80, height=26, fg_color=CARD_BORDER).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(proxy_btns, text="APIs", command=self.manage_custom_apis, width=80, height=26, fg_color=ACCENT_ORANGE).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(proxy_btns, text="Probar", command=self.test_proxies, width=80, height=26, fg_color=CARD_BORDER).pack(side=ctk.LEFT, padx=2)

    def build_footer_actions(self, master):
        footer = ctk.CTkFrame(master, fg_color=CARD_BG, corner_radius=0, border_color=CARD_BORDER, border_width=1)
        footer.pack(fill=ctk.X, side=ctk.BOTTOM)

        # Progresos y Estado
        status_container = ctk.CTkFrame(footer, fg_color="transparent")
        status_container.pack(fill=ctk.X, padx=20, pady=(10, 5))

        self.status_label = ctk.CTkLabel(status_container, text="Listo para iniciar descargas", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED)
        self.status_label.pack(anchor="w")

        self.progress_bar = ctk.CTkProgressBar(status_container, height=8, progress_color=ACCENT_BLUE)
        self.progress_bar.pack(fill=ctk.X, pady=(4, 0))
        self.progress_bar.set(0)

        # Botones Principales
        btn_container = ctk.CTkFrame(footer, fg_color="transparent")
        btn_container.pack(fill=ctk.X, padx=20, pady=(5, 12))

        self.download_button = ctk.CTkButton(
            btn_container, text="⬇️ DESCARGAR COLA", command=self.start_download,
            font=ctk.CTkFont(size=13, weight="bold"), fg_color=ACCENT_BLUE, hover_color="#2563EB", height=38
        )
        self.download_button.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 5))

        ctk.CTkButton(
            btn_container, text="🎵 Solo Audio", command=self.download_audio_only,
            width=110, height=38, fg_color=ACCENT_GREEN, hover_color="#059669", text_color="white"
        ).pack(side=ctk.LEFT, padx=2)

        ctk.CTkButton(
            btn_container, text="🎬 Solo Video", command=self.download_video_only,
            width=110, height=38, fg_color=ACCENT_GREEN, hover_color="#059669", text_color="white"
        ).pack(side=ctk.LEFT, padx=2)


    # ---------- LÓGICA DE NEGOCIO Y FUNCIONES DE EVENTOS ----------

    def load_txt_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.url_textbox.insert("end", f"\n{content}")

    def open_output_dir(self):
        path = self.output_path.get()
        if os.path.exists(path):
            if sys.platform == 'win32':
                os.startfile(path)
            else:
                subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', path])

    def get_urls_from_textbox(self):
        raw_urls = self.url_textbox.get("1.0", "end-1c").strip().split('\n')
        return [u.strip() for u in raw_urls if u.strip().startswith("http")]

    def popup_author(self):
        MessageBox.showinfo("Acerca de", "Multi Downloader Pro v4.0\nDesarrollado Por FayDev\n¡Soporte para descargas en lote y conversión avanzada! D  Arreglo de Bugs y Funciones Mejoradas")

    def popup_donate(self):
        donate_text = "¡Gracias por usar Multi Downloader Pro!\n\nPayPal: https://www.paypal.me/faycraxE\n\nTu apoyo ayuda a mantener el proyecto actualizado."
        MessageBox.showinfo("Donar", donate_text)

    def on_cookie_toggle(self):
        if self.use_browser_cookies.get() and not self.installed_browsers:
            MessageBox.showwarning("Sin navegadores", "No se detectaron navegadores instalados en el sistema.")
            self.use_browser_cookies.set(False)

    def refresh_browsers(self):
        self.status_label.configure(text="🔍 Buscando navegadores...")
        self.installed_browsers = detect_installed_browsers()
        if self.installed_browsers:
            self.selected_browser.set(self.installed_browsers[0])
            MessageBox.showinfo("Éxito", f"Navegadores encontrados: {', '.join([b.title() for b in self.installed_browsers])}")
            self.status_label.configure(text=f"✅ {len(self.installed_browsers)} navegadores detectados")
        else:
            MessageBox.showwarning("Sin resultados", "No se encontraron navegadores compatibles.")
            self.status_label.configure(text="❌ No se detectaron navegadores")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def browse_ffmpeg_path(self): 
        filepath = filedialog.askopenfilename(defaultextension=".exe", filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
        if filepath:
            self.ffmpeg_custom_path.set(filepath)

    def fetch_proxies_now(self):
        def fetch_thread():
            self.status_label.configure(text="Consultando APIs de proxies...")
            h_p = get_proxies_from_api('http')
            s_p = get_proxies_from_api('socks5')
            if h_p or s_p:
                save_proxy_list(h_p, s_p)
                total = len(h_p) + len(s_p)
                self.status_label.configure(text=f"✅ Obtenidos {total} proxies")
                MessageBox.showinfo("Éxito", f"Se guardaron {total} proxies actualizados.")
            else:
                self.status_label.configure(text="❌ Error consultando proxies")
        threading.Thread(target=fetch_thread, daemon=True).start()

    def test_proxies(self):
        def test_thread():
            self.status_label.configure(text="Probando conexión de proxies...")
            h_p, s_p = load_proxy_list()
            w_h = [p for p in h_p[:5] if test_proxy(p, 'http')]
            w_s = [p for p in s_p[:5] if test_proxy(p, 'socks5')]
            self.status_label.configure(text=f"✅ Test finalizado: {len(w_h) + len(w_s)} activos")
            MessageBox.showinfo("Resultado", f"Proxies funcionales detectados:\nHTTP: {len(w_h)}\nSOCKS5: {len(w_s)}")
        threading.Thread(target=test_thread, daemon=True).start()

    def manage_proxies(self):
        proxy_win = ctk.CTkToplevel(self.master)
        proxy_win.title("Gestor de Proxies")
        proxy_win.geometry("450x380")
        proxy_win.grab_set()

        h_p, s_p = load_proxy_list()
        ctk.CTkLabel(proxy_win, text="Proxies HTTP:").pack(anchor="w", padx=10, pady=(10, 0))
        http_txt = ctk.CTkTextbox(proxy_win, height=90)
        http_txt.pack(fill="x", padx=10, pady=5)
        http_txt.insert("1.0", "\n".join(h_p))

        ctk.CTkLabel(proxy_win, text="Proxies SOCKS5:").pack(anchor="w", padx=10, pady=(5, 0))
        socks_txt = ctk.CTkTextbox(proxy_win, height=90)
        socks_txt.pack(fill="x", padx=10, pady=5)
        socks_txt.insert("1.0", "\n".join(s_p))

        def save_and_close():
            save_proxy_list(
                [line.strip() for line in http_txt.get("1.0", "end-1c").split("\n") if line.strip()],
                [line.strip() for line in socks_txt.get("1.0", "end-1c").split("\n") if line.strip()]
            )
            proxy_win.destroy()

        ctk.CTkButton(proxy_win, text="Guardar Cambios", command=save_and_close, fg_color=ACCENT_GREEN).pack(pady=10)

    def manage_custom_apis(self):
        api_win = ctk.CTkToplevel(self.master)
        api_win.title("APIs de Proxies")
        api_win.geometry("450x380")
        api_win.grab_set()

        custom_apis = load_custom_apis()
        ctk.CTkLabel(api_win, text="URLs de APIs HTTP:").pack(anchor="w", padx=10, pady=(10, 0))
        http_api_txt = ctk.CTkTextbox(api_win, height=90)
        http_api_txt.pack(fill="x", padx=10, pady=5)
        http_api_txt.insert("1.0", "\n".join(custom_apis.get('http', [])))

        ctk.CTkLabel(api_win, text="URLs de APIs SOCKS5:").pack(anchor="w", padx=10, pady=(5, 0))
        socks_api_txt = ctk.CTkTextbox(api_win, height=90)
        socks_api_txt.pack(fill="x", padx=10, pady=5)
        socks_api_txt.insert("1.0", "\n".join(custom_apis.get('socks5', [])))

        def save_apis():
            save_custom_apis({
                'http': [l.strip() for l in http_api_txt.get("1.0", "end-1c").split("\n") if l.strip()],
                'socks5': [l.strip() for l in socks_api_txt.get("1.0", "end-1c").split("\n") if l.strip()]
            })
            api_win.destroy()

        ctk.CTkButton(api_win, text="Guardar APIs", command=save_apis, fg_color=ACCENT_ORANGE).pack(pady=10)

    def download_audio_only(self):
        self.audio_format.set("mp3")
        self.video_format.set("none")
        self.start_download()

    def download_video_only(self):
        self.audio_format.set("none")
        self.video_format.set("mp4")
        self.start_download()

    def start_download(self):
        urls = self.get_urls_from_textbox()
        if not urls:
            MessageBox.showwarning("Atención", "Por favor ingresa al menos una URL válida.")
            return

        out_dir = self.output_path.get()
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                MessageBox.showerror("Error", f"No se pudo crear el directorio de destino:\n{e}")
                return

        def download_thread():
            self.download_button.configure(state="disabled")
            total = len(urls)

            for idx, url in enumerate(urls, 1):
                self.status_label.configure(text=f"Procesando ({idx}/{total}): {url[:40]}...")
                self.progress_bar.set(0)

                ydl_opts = {
                    'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.ydl_progress_hook],
                    'nocheckcertificate': True,
                    'ignoreerrors': True,
                }

                if self.ffmpeg_custom_path.get() and os.path.exists(self.ffmpeg_custom_path.get()):
                    ydl_opts['ffmpeg_location'] = self.ffmpeg_custom_path.get()

                if self.use_browser_cookies.get() and self.selected_browser.get() != "ninguno":
                    ydl_opts['cookiesfrombrowser'] = (self.selected_browser.get(),)

                if self.use_proxy.get():
                    p_addr = get_random_proxy(self.proxy_type.get())
                    if p_addr:
                        ydl_opts['proxy'] = f"{self.proxy_type.get()}://{p_addr}"

                v_res, v_fmt, a_fmt = self.video_resolution.get(), self.video_format.get(), self.audio_format.get()
                postprocessors = []

                if a_fmt != "none" and v_fmt == "none":
                    ydl_opts['format'] = 'bestaudio/best'
                    postprocessors.append({'key': 'FFmpegExtractAudio', 'preferredcodec': a_fmt, 'preferredquality': '192'})
                    if self.embed_metadata.get():
                        postprocessors.extend([{'key': 'FFmpegMetadata'}, {'key': 'EmbedThumbnail'}])
                        ydl_opts['writethumbnail'] = True
                elif v_fmt != "none":
                    if v_res in ["mejor", "none"]:
                        ydl_opts['format'] = f'bestvideo[ext={v_fmt}]+bestaudio/best'
                    else:
                        ydl_opts['format'] = f'bestvideo[height<={v_res.replace("p", "")}]+bestaudio/best'

                if postprocessors:
                    ydl_opts['postprocessors'] = postprocessors

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                except Exception as e:
                    print(f"Error descargando {url}: {e}")

            self.status_label.configure(text="✅ Todas las descargas completadas con éxito.")
            self.progress_bar.set(1.0)
            self.download_button.configure(state="normal")
            send_notification("Multi Downloader Pro", "¡Cola de descargas finalizada!")
            MessageBox.showinfo("Finalizado", "Se procesaron todas las descargas de la cola.")

        threading.Thread(target=download_thread, daemon=True).start()

    def ydl_progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total_bytes > 0:
                pct = downloaded / total_bytes
                self.progress_bar.set(pct)
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                self.status_label.configure(text=f"Descargando: {int(pct*100)}% | Velocidad: {speed} | Restante: {eta}")
        elif d['status'] == 'finished':
            self.status_label.configure(text="Conversión/Procesamiento final...")


if __name__ == "__main__":
    root = ctk.CTk()
    app = MultiDownloaderGUI(root)
    root.mainloop()
