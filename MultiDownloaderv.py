import os
import re
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
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import DownloadCancelled, remove_terminal_sequences

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
        return os.path.dirname(os.path.abspath(__file__))

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

# ========== FUNCIONES PARA GESTIÓN DE COOKIES ==========

def get_cookie_file_path():
    """Obtiene la ruta del archivo de cookies"""
    return os.path.join(get_base_path(), "cookies.txt")

def browser_has_dpapi_issue(browser_name):
    """Chrome y Edge tienen problemas con DPAPI en Windows"""
    return browser_name.lower() in ["chrome", "edge", "brave", "opera"]

def validate_cookie_file(cookie_path):
    """Valida que el archivo de cookies tenga el formato correcto"""
    if not os.path.exists(cookie_path):
        return False
    try:
        with open(cookie_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Verificar que tenga el formato de cookies Netscape
            if not content.startswith('# Netscape HTTP Cookie File'):
                return False
            # Verificar que tenga al menos una línea con formato de cookie
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 7:  # Formato Netscape: domain, flag, path, secure, expires, name, value
                    return True
        return False
    except:
        return False

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
    # Se usa la capa de red de yt-dlp porque urllib no soporta SOCKS
    try:
        opts = {'proxy': f'{proxy_type}://{proxy}', 'socket_timeout': 8, 'quiet': True,
                'http_headers': {'User-Agent': get_random_user_agent()}}
        with YoutubeDL(opts) as ydl:
            return ydl.urlopen('http://httpbin.org/ip').status == 200
    except Exception:
        return False

# Contenedores donde yt-dlp puede incrustar carátula (wav y webm no lo soportan)
THUMBNAIL_EXTS = {'mp3', 'm4a', 'mp4', 'mkv'}

# "(Official Video)", "[Lyrics]", "(Video Oficial)", "(4K Remaster)"... al final de títulos de canciones
_TITLE_JUNK = re.compile(
    r'\s*[\(\[][^\)\]]*\b(official|oficial|video|v[ií]deo|audio|lyrics?|letra|visuali[sz]er|'
    r'remaster(ed)?|hd|hq|4k|mv|videoclip|clip)\b[^\)\]]*[\)\]]', re.IGNORECASE)

def music_tags(info, force=False):
    """Artista y título limpios para canciones. Solo actúa si es música (categoría Music,
    datos de pista del sitio) o si force=True (descarga de solo audio)."""
    artist = info.get('artist') or ', '.join(info.get('artists') or [])
    track = info.get('track')
    if not (force or track or artist or 'Music' in (info.get('categories') or [])):
        return {}
    title = info.get('title') or ''
    parsed = re.match(r'(.+?)\s+[-–—]\s+(.+)', title)  # "Artista - Canción"
    if not artist:
        channel = info.get('uploader') or info.get('channel') or ''
        channel = re.sub(r'(\s*-\s*Topic|VEVO|\s+Official)$', '', channel, flags=re.IGNORECASE).strip()
        artist = parsed.group(1).strip() if parsed else channel
    if not track:
        track = _TITLE_JUNK.sub('', parsed.group(2) if parsed else title).strip() or title
    # Los campos meta_* tienen prioridad en FFmpegMetadata sobre los que genera yt-dlp
    return {k: v for k, v in (('meta_title', track), ('meta_artist', artist)) if v}

class MusicTagsPP(PostProcessor):
    def __init__(self, force=False):
        super().__init__()
        self.force = force

    def run(self, info):
        info.update(music_tags(info, self.force))
        return [], info

def build_media_opts(v_res, v_fmt, a_fmt, embed_metadata):
    """Opciones de yt-dlp (format, merge, postprocesadores) para que el archivo final
    quede exactamente en el formato elegido. Sin formato elegido, solo añade metadatos."""
    opts = {}
    pps = []
    if a_fmt != "none" and v_fmt == "none":
        opts['format'] = 'bestaudio/best'
        pps.append({'key': 'FFmpegExtractAudio', 'preferredcodec': a_fmt, 'preferredquality': '192'})
        final_ext = a_fmt
    elif v_fmt != "none":
        h = '' if v_res in ("mejor", "none") else f'[height<={v_res.rstrip("p")}]'
        # Primero streams nativos del contenedor (sin recodificar); mkv acepta cualquiera
        a_ext = {'mp4': '[ext=m4a]', 'webm': '[ext=webm]'}.get(v_fmt, '')
        opts['format'] = (f'bestvideo{h}[ext={v_fmt}]+bestaudio{a_ext}/best{h}[ext={v_fmt}]'
                          f'/bestvideo{h}+bestaudio/best{h}/best')
        if v_fmt == 'webm':
            # webm solo admite VP8/VP9/AV1 + Opus/Vorbis: si el respaldo trae h264/aac hay que
            # recodificar; se usa el modo rápido de libvpx (el modo por defecto es muy lento)
            opts['merge_output_format'] = 'webm/mkv'
            pps.append({'key': 'FFmpegVideoConvertor', 'preferedformat': 'webm'})
            opts['postprocessor_args'] = {'videoconvertor': [
                '-c:v', 'libvpx-vp9', '-deadline', 'realtime', '-cpu-used', '8', '-row-mt', '1',
                '-b:v', '0', '-crf', '32', '-c:a', 'libopus']}
        else:
            # mp4/mkv admiten h264, vp9, av1, opus y aac: se copian los streams (remux),
            # sin recodificar. yt-dlp omite el paso si el archivo ya está en el formato pedido
            # shortcut: códecs muy antiguos (p. ej. Vorbis) no caben en mp4 y el remux falla; se reporta como error
            opts['merge_output_format'] = v_fmt
            pps.append({'key': 'FFmpegVideoRemuxer', 'preferedformat': v_fmt})
        final_ext = v_fmt
    else:
        # Sin formato elegido el contenedor final no se conoce: solo metadatos, sin carátula
        final_ext = None

    if embed_metadata:
        # Título, artista, fecha, género, descripción, URL y capítulos
        pps.append({'key': 'FFmpegMetadata', 'add_metadata': True, 'add_chapters': True})
        if final_ext in THUMBNAIL_EXTS:
            # Las miniaturas webp no se incrustan bien en mp3/m4a: se pasan a jpg
            pps.append({'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg', 'when': 'before_dl'})
            pps.append({'key': 'EmbedThumbnail'})
            opts['writethumbnail'] = True
            if final_ext in ('mp3', 'm4a'):
                # Portada cuadrada (recorte centrado) como en los reproductores de música
                opts.setdefault('postprocessor_args', {})['thumbnailsconvertor+ffmpeg_o'] = [
                    '-vf', "crop='min(iw,ih)':'min(iw,ih)'", '-q:v', '2']

    opts['postprocessors'] = pps
    return opts


def remove_partial_files(download_paths, thumb_paths):
    """Tras cancelar, borra solo temporales: .part/.ytdl, streams sueltos antes de unir
    ("titulo.f401.mp4") y la miniatura recién escrita. Nunca un archivo final, que yt-dlp
    también reporta en el progreso si ya existía de antes."""
    candidates = set(filter(None, thumb_paths))
    for p in filter(None, download_paths):
        candidates.update((p + '.part', p + '.ytdl'))
        if p.endswith(('.part', '.ytdl')) or re.search(r'\.f[\w-]+\.\w+$', p):
            candidates.add(p)
    for p in candidates:
        try:
            if os.path.isfile(p):
                os.remove(p)
        except OSError:
            pass


# ========== CLASE PRINCIPAL DE INTERFAZ ==========

# Texto del menú para "sin formato elegido" (internamente es "none")
ORIGINAL = "Original"

class MultiDownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi Downloader Pro v4.0")
        # Que quepa en pantallas de 768 px (el contenido central tiene scroll)
        height = min(900, master.winfo_screenheight() - 80)
        master.geometry(f"850x{height}")
        master.minsize(780, min(750, height))
        self.master.configure(fg_color=BG_COLOR)

        # Variables de estado
        self.video_resolution = ctk.StringVar(value="mejor")
        self.video_format = ctk.StringVar(value=ORIGINAL)
        self.audio_format = ctk.StringVar(value=ORIGINAL)
        self.cancel_event = threading.Event()
        self.output_path = ctk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.ffmpeg_custom_path = ctk.StringVar(value="") 
        self.use_proxy = ctk.BooleanVar(value=False)
        self.proxy_type = ctk.StringVar(value="http")
        self.auto_retry_proxy = ctk.BooleanVar(value=True)
        self.auto_fetch_proxies = ctk.BooleanVar(value=True)
        
        # Variables de cookies mejoradas
        self.use_cookies = ctk.BooleanVar(value=False)
        self.cookie_type = ctk.StringVar(value="archivo")  # "archivo", "navegador"
        self.selected_browser = ctk.StringVar(value="ninguno")
        self.embed_metadata = ctk.BooleanVar(value=True)
        
        self.installed_browsers = detect_installed_browsers()
        if self.installed_browsers:
            self.selected_browser.set(self.installed_browsers[0])
        
        # Verificar si existen cookies guardadas
        self.has_cookie_file = os.path.exists(get_cookie_file_path())

        # --- CABECERA (HEADER CON LOGO) ---
        self.header_frame = ctk.CTkFrame(master, fg_color="transparent")
        self.header_frame.pack(fill=ctk.X, padx=25, pady=(15, 5))

        # Intentar cargar la imagen del logo desde 'assets/youtubemp3.png'
        logo_path = os.path.join(get_base_path(), "assets", "logo.jpg")
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

        # Al ocultar el panel de cookies el scroll queda desplazado: empezar arriba
        master.after(150, lambda: self.scroll_container._parent_canvas.yview_moveto(0))

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
        
        ctk.CTkLabel(sub_header, text="Pega las URLs (una por línea):", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side=ctk.LEFT)
        self.url_count_label = ctk.CTkLabel(sub_header, text="", font=ctk.CTkFont(size=11, weight="bold"), text_color=ACCENT_BLUE)
        self.url_count_label.pack(side=ctk.LEFT, padx=8)

        small = dict(height=24, fg_color=CARD_BORDER, hover_color="#475569", font=ctk.CTkFont(size=11))
        ctk.CTkButton(sub_header, text="📂 Importar .txt", command=self.load_txt_file, width=110, **small).pack(side=ctk.RIGHT)
        ctk.CTkButton(sub_header, text="🗑 Limpiar", command=self.clear_urls, width=80, **small).pack(side=ctk.RIGHT, padx=4)
        ctk.CTkButton(sub_header, text="📋 Pegar", command=self.paste_urls, width=80, **small).pack(side=ctk.RIGHT)

        self.url_textbox = ctk.CTkTextbox(card, height=110, corner_radius=8, font=('Consolas', 11),
                                          fg_color=BG_COLOR, border_color=CARD_BORDER, border_width=1)
        self.url_textbox.pack(fill=ctk.X)
        self.url_textbox.bind("<KeyRelease>", lambda _: self.update_url_count())
        self.update_url_count()

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
        ctk.CTkEntry(row2, textvariable=self.ffmpeg_custom_path, state='readonly').pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=5)
        ctk.CTkButton(row2, text="Seleccionar", command=self.browse_ffmpeg_path, width=80, fg_color=CARD_BORDER).pack(side=ctk.LEFT, padx=2)

        self.ffmpeg_status_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=10), anchor="w")
        self.ffmpeg_status_label.pack(fill=ctk.X, padx=(85, 0))
        self.update_ffmpeg_status()

    def update_ffmpeg_status(self):
        """FFmpeg es necesario para unir audio+video, convertir y añadir metadatos"""
        custom = self.ffmpeg_custom_path.get()
        if custom and os.path.exists(custom):
            text, color = "✅ Usando el FFmpeg seleccionado", ACCENT_GREEN
        elif shutil.which("ffmpeg"):
            text, color = "✅ FFmpeg detectado en el sistema (opcional elegir otro)", ACCENT_GREEN
        else:
            text, color = "⚠️ FFmpeg no encontrado: sin él no se pueden convertir formatos ni añadir metadatos", ACCENT_ORANGE
        self.ffmpeg_status_label.configure(text=text, text_color=color)

    def update_url_count(self):
        n = len(self.get_urls_from_textbox())
        self.url_count_label.configure(text=f"{n} URL{'s' if n != 1 else ''} en cola" if n else "")

    def paste_urls(self):
        try:
            text = self.master.clipboard_get().strip()
        except tk.TclError:
            return  # portapapeles vacío o sin texto
        if text:
            current = self.url_textbox.get("1.0", "end-1c")
            self.url_textbox.insert("end", ("\n" if current.strip() else "") + text)
            self.update_url_count()

    def clear_urls(self):
        self.url_textbox.delete("1.0", "end")
        self.update_url_count()

    def build_options_card(self):
        card = self.build_card("⚙️ Formato y Calidad")
        
        opts_frame = ctk.CTkFrame(card, fg_color="transparent")
        opts_frame.pack(fill=ctk.X)
        opts_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Res
        f1 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f1.grid(row=0, column=0, sticky="ew", padx=5)
        ctk.CTkLabel(f1, text="Resolución Video", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f1, variable=self.video_resolution, values=["mejor", "2160p", "1440p", "1080p", "720p", "480p"]).pack(fill=ctk.X, pady=2)

        # Formato Video
        f2 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f2.grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkLabel(f2, text="Formato Video", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f2, variable=self.video_format, values=[ORIGINAL, "mp4", "webm", "mkv"]).pack(fill=ctk.X, pady=2)

        # Formato Audio
        f3 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        f3.grid(row=0, column=2, sticky="ew", padx=5)
        ctk.CTkLabel(f3, text="Formato Audio", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(anchor="w")
        ctk.CTkOptionMenu(f3, variable=self.audio_format, values=[ORIGINAL, "mp3", "wav", "m4a"]).pack(fill=ctk.X, pady=2)

        ctk.CTkCheckBox(
            card, text="Incrustar carátula y metadatos (título, artista, capítulos) en audio y video",
            variable=self.embed_metadata, font=ctk.CTkFont(size=11)
        ).pack(anchor="w", pady=(10, 0))

    def build_advanced_card(self):
        card = self.build_card("🛡️ Red y Autenticación")

        # ===== SECCIÓN DE COOKIES MEJORADA =====
        self.cookie_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.cookie_frame.pack(fill=ctk.X, pady=(0, 8))

        # Checkbox principal de cookies
        ctk.CTkCheckBox(
            self.cookie_frame,
            text="🔐 Usar autenticación (cookies)", 
            variable=self.use_cookies, 
            command=self.on_cookie_toggle,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w")

        # Sub-frame para opciones de cookies
        self.cookie_options_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.cookie_options_frame.pack(fill=ctk.X, padx=20, pady=(5, 0))
        
        # Método de autenticación
        method_frame = ctk.CTkFrame(self.cookie_options_frame, fg_color="transparent")
        method_frame.pack(fill=ctk.X, pady=2)
        
        ctk.CTkLabel(method_frame, text="Método:", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side=ctk.LEFT, padx=(0, 10))
        
        ctk.CTkOptionMenu(
            method_frame, 
            variable=self.cookie_type,
            values=["archivo", "navegador"],
            width=120,
            command=self.on_cookie_type_change
        ).pack(side=ctk.LEFT)

        # Botones según método
        self.method_buttons_frame = ctk.CTkFrame(self.cookie_options_frame, fg_color="transparent")
        self.method_buttons_frame.pack(fill=ctk.X, pady=5)
        
        self.update_cookie_buttons()

        # Información de estado
        self.cookie_status_label = ctk.CTkLabel(
            self.cookie_options_frame, 
            text="", 
            font=ctk.CTkFont(size=10),
            text_color=TEXT_MUTED
        )
        self.cookie_status_label.pack(anchor="w", pady=(2, 0))
        
        self.update_cookie_status()
        self.on_cookie_toggle()  # oculto mientras la autenticación esté desactivada

        # Separador
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

    def update_cookie_buttons(self):
        """Actualiza los botones según el método seleccionado"""
        # Limpiar frame
        for widget in self.method_buttons_frame.winfo_children():
            widget.destroy()
            
        method = self.cookie_type.get()
        
        if method == "archivo":
            ctk.CTkButton(
                self.method_buttons_frame, 
                text="📂 Seleccionar cookies.txt", 
                command=self.select_cookie_file,
                width=180, height=26, fg_color=ACCENT_ORANGE
            ).pack(side=ctk.LEFT, padx=2)
            
            ctk.CTkButton(
                self.method_buttons_frame, 
                text="📋 Ayuda", 
                command=self.show_cookie_help,
                width=100, height=26, fg_color=CARD_BORDER
            ).pack(side=ctk.LEFT, padx=2)
            
        elif method == "navegador":
            browser_values = self.installed_browsers if self.installed_browsers else ["ninguno"]
            ctk.CTkOptionMenu(
                self.method_buttons_frame,
                variable=self.selected_browser,
                values=browser_values,
                width=120, height=26,
                command=lambda _: self.update_dpapi_warning()
            ).pack(side=ctk.LEFT, padx=2)

            ctk.CTkButton(
                self.method_buttons_frame,
                text="🔄 Detectar",
                command=self.refresh_browsers,
                width=100, height=26, fg_color=CARD_BORDER
            ).pack(side=ctk.LEFT, padx=2)

            self.dpapi_label = ctk.CTkLabel(
                self.method_buttons_frame,
                text="",
                font=ctk.CTkFont(size=10),
                text_color="#EF4444"
            )
            self.dpapi_label.pack(side=ctk.LEFT, padx=5)
            self.update_dpapi_warning()

    def update_dpapi_warning(self):
        """Muestra el aviso DPAPI según el navegador seleccionado"""
        risky = browser_has_dpapi_issue(self.selected_browser.get())
        self.dpapi_label.configure(text="⚠️ Chrome/Edge pueden fallar. Usa Firefox o archivo." if risky else "")

    def update_cookie_status(self):
        """Actualiza el estado de las cookies"""
        status_text = ""
        method = self.cookie_type.get()
        
        if method == "archivo":
            if self.has_cookie_file and validate_cookie_file(get_cookie_file_path()):
                status_text = "✅ cookies.txt válido"
            else:
                status_text = "❌ No hay cookies.txt válido. Selecciona uno."
        elif method == "navegador":
            if self.installed_browsers:
                status_text = f"✅ Navegadores: {', '.join(self.installed_browsers)}"
            else:
                status_text = "❌ No hay navegadores detectados"

        self.cookie_status_label.configure(text=status_text)

    def on_cookie_toggle(self):
        """Muestra las opciones de cookies solo cuando la autenticación está activada"""
        if self.use_cookies.get():
            self.cookie_options_frame.pack(fill=ctk.X, padx=20, pady=(0, 4), after=self.cookie_frame)
            self.update_cookie_buttons()
            self.update_cookie_status()
        else:
            self.cookie_options_frame.pack_forget()

    def on_cookie_type_change(self, choice):
        """Maneja el cambio de método de cookies"""
        self.update_cookie_buttons()
        self.update_cookie_status()

    def select_cookie_file(self):
        """Selecciona un archivo de cookies"""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo de cookies",
            filetypes=[("Cookies files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            dest_path = get_cookie_file_path()
            try:
                shutil.copy2(filepath, dest_path)
                self.has_cookie_file = True
                self.update_cookie_status()
                MessageBox.showinfo("Éxito", f"Cookies guardadas en:\n{dest_path}")
            except Exception as e:
                MessageBox.showerror("Error", f"No se pudo copiar:\n{e}")
    
    def show_cookie_help(self):
        """Muestra ayuda sobre el formato de cookies"""
        help_text = """📖 FORMATO COOKIES.TXT

El archivo debe estar en formato Netscape:

# Netscape HTTP Cookie File
.youtube.com\tTRUE\t/\tFALSE\t1234567890\tVISITOR_INFO1_LIVE\tvalor...
.youtube.com\tTRUE\t/\tFALSE\t1234567890\tCONSENT\tvalor...

📌 CÓMO EXPORTAR:

1. Instala "Get cookies.txt LOCALLY" en Chrome
   https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

2. Ve a YouTube, haz clic en la extensión

3. Haz clic en "Export" y guarda como cookies.txt

4. Selecciona el archivo con el botón "Seleccionar cookies.txt"

✅ FORMATO VÁLIDO:
- Columnas separadas por TAB
- Encabezado # Netscape HTTP Cookie File
- Líneas con: dominio, flag, ruta, seguro, expiración, nombre, valor
"""
        MessageBox.showinfo("Formato de Cookies", help_text)

    def build_footer_actions(self, master):
        footer = ctk.CTkFrame(master, fg_color=CARD_BG, corner_radius=0, border_color=CARD_BORDER, border_width=1)
        footer.pack(fill=ctk.X, side=ctk.BOTTOM)

        # Progresos y Estado
        status_container = ctk.CTkFrame(footer, fg_color="transparent")
        status_container.pack(fill=ctk.X, padx=20, pady=(10, 5))

        status_row = ctk.CTkFrame(status_container, fg_color="transparent")
        status_row.pack(fill=ctk.X)
        self.status_label = ctk.CTkLabel(status_row, text="Listo para iniciar descargas", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED, anchor="w")
        self.status_label.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        self.queue_label = ctk.CTkLabel(status_row, text="", font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT_MAIN)
        self.queue_label.pack(side=ctk.RIGHT)

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

        self.audio_button = ctk.CTkButton(
            btn_container, text="🎵 Solo Audio", command=self.download_audio_only,
            width=110, height=38, fg_color=ACCENT_GREEN, hover_color="#059669", text_color="white"
        )
        self.audio_button.pack(side=ctk.LEFT, padx=2)

        self.video_button = ctk.CTkButton(
            btn_container, text="🎬 Solo Video", command=self.download_video_only,
            width=110, height=38, fg_color=ACCENT_GREEN, hover_color="#059669", text_color="white"
        )
        self.video_button.pack(side=ctk.LEFT, padx=2)

        self.cancel_button = ctk.CTkButton(
            btn_container, text="⏹ Cancelar", command=self.cancel_download, state="disabled",
            width=100, height=38, fg_color="#EF4444", hover_color="#DC2626", text_color="white"
        )
        self.cancel_button.pack(side=ctk.LEFT, padx=(2, 0))


    # ---------- LÓGICA DE NEGOCIO Y FUNCIONES DE EVENTOS ----------

    def load_txt_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.url_textbox.insert("end", f"\n{content}")
            self.update_url_count()

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
        self.update_cookie_status()
        self.update_cookie_buttons()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def browse_ffmpeg_path(self): 
        filepath = filedialog.askopenfilename(defaultextension=".exe", filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
        if filepath:
            self.ffmpeg_custom_path.set(filepath)
            self.update_ffmpeg_status()

    def fetch_proxies_now(self):
        def fetch_thread():
            self.set_status("Consultando APIs de proxies...")
            h_p = get_proxies_from_api('http')
            s_p = get_proxies_from_api('socks5')
            if h_p or s_p:
                save_proxy_list(h_p, s_p)
                total = len(h_p) + len(s_p)
                self.set_status(f"✅ Obtenidos {total} proxies")
                self.ui(MessageBox.showinfo, "Éxito", f"Se guardaron {total} proxies actualizados.")
            else:
                self.set_status("❌ Error consultando proxies")
        threading.Thread(target=fetch_thread, daemon=True).start()

    def test_proxies(self):
        def test_thread():
            self.set_status("Probando conexión de proxies...")
            h_p, s_p = load_proxy_list()
            w_h = [p for p in h_p[:5] if test_proxy(p, 'http')]
            w_s = [p for p in s_p[:5] if test_proxy(p, 'socks5')]
            self.set_status(f"✅ Test finalizado: {len(w_h) + len(w_s)} activos")
            self.ui(MessageBox.showinfo, "Resultado", f"Proxies funcionales detectados:\nHTTP: {len(w_h)}\nSOCKS5: {len(w_s)}")
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

    # Respetan el formato elegido en el menú; mp3/mp4 solo si está en "Original"
    def download_audio_only(self):
        a_fmt = self.audio_format.get()
        self.start_download(a_fmt=a_fmt if a_fmt != ORIGINAL else "mp3", v_fmt="none")

    def download_video_only(self):
        v_fmt = self.video_format.get()
        self.start_download(a_fmt="none", v_fmt=v_fmt if v_fmt != ORIGINAL else "mp4")

    def cancel_download(self):
        self.cancel_event.set()
        self.cancel_button.configure(state="disabled")
        self.status_label.configure(text="⏹ Cancelando... (se detiene al terminar el paso actual)")

    # Tk no es thread-safe: los hilos de trabajo solo tocan widgets a través de after()
    def ui(self, fn, *args, **kwargs):
        self.master.after(0, lambda: fn(*args, **kwargs))

    def set_status(self, text):
        self.ui(self.status_label.configure, text=text)

    def set_download_buttons(self, state):
        for btn in (self.download_button, self.audio_button, self.video_button):
            btn.configure(state=state)
        self.cancel_button.configure(state="normal" if state == "disabled" else "disabled")

    def start_download(self, a_fmt=None, v_fmt=None):
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

        # Leer las variables de Tk aquí (hilo principal), no dentro del hilo de descarga
        v_res = self.video_resolution.get()
        v_fmt = v_fmt or self.video_format.get()
        a_fmt = a_fmt or self.audio_format.get()
        v_fmt, a_fmt = ("none" if f == ORIGINAL else f for f in (v_fmt, a_fmt))
        ffmpeg_path = self.ffmpeg_custom_path.get()
        use_cookies, cookie_method, browser = self.use_cookies.get(), self.cookie_type.get(), self.selected_browser.get()
        use_proxy, proxy_type = self.use_proxy.get(), self.proxy_type.get()
        embed_metadata = self.embed_metadata.get()

        self.cancel_event.clear()
        self.set_download_buttons("disabled")

        def download_thread():
            total = len(urls)
            failed = []
            done = 0

            for idx, url in enumerate(urls, 1):
                if self.cancel_event.is_set():
                    break
                self.ui(self.queue_label.configure, text=f"Cola {idx}/{total}")
                self.partial_files, self.thumb_files = set(), set()
                self.set_status(f"Preparando: {url[:60]}")
                self.ui(self.progress_bar.set, 0)

                ydl_opts = {
                    'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.ydl_progress_hook],
                    'ignoreerrors': True,
                }

                if ffmpeg_path and os.path.exists(ffmpeg_path):
                    ydl_opts['ffmpeg_location'] = ffmpeg_path

                # ========== CONFIGURACIÓN DE COOKIES ==========
                if use_cookies:
                    if cookie_method == "archivo":
                        cookie_file = get_cookie_file_path()
                        if validate_cookie_file(cookie_file):
                            ydl_opts['cookiefile'] = cookie_file
                            self.set_status("🍪 Usando cookies desde archivo")
                        else:
                            self.set_status("⚠️ cookies.txt no válido")
                    elif cookie_method == "navegador":
                        if browser != "ninguno":
                            ydl_opts['cookiesfrombrowser'] = (browser,)
                            self.set_status(f"🔄 Usando cookies de {browser.title()}")
                        else:
                            self.set_status("⚠️ Sin navegador seleccionado")

                if use_proxy:
                    p_addr = get_random_proxy(proxy_type)
                    if p_addr:
                        ydl_opts['proxy'] = f"{proxy_type}://{p_addr}"

                ydl_opts.update(build_media_opts(v_res, v_fmt, a_fmt, embed_metadata))

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        if embed_metadata:
                            ydl.add_post_processor(MusicTagsPP(force=a_fmt != "none" and v_fmt == "none"),
                                                   when='pre_process')
                        # con ignoreerrors, los fallos no lanzan excepción: se reflejan en el código de retorno
                        if ydl.download([url]) != 0:
                            failed.append(url)
                        else:
                            done += 1
                except DownloadCancelled:
                    remove_partial_files(self.partial_files, self.thumb_files)
                    break
                except Exception as e:
                    print(f"Error descargando {url}: {e}")
                    failed.append(url)

            if self.cancel_event.is_set():
                summary = f"⏹ Cancelado: {done}/{total} descargas completadas."
                detail = summary
                show = MessageBox.showinfo
            elif failed:
                summary = f"⚠️ {done}/{total} descargas completadas, {len(failed)} con errores."
                detail = summary + "\n\nFallaron:\n" + "\n".join(u[:80] for u in failed)
                show = MessageBox.showwarning
            else:
                summary = "✅ Todas las descargas completadas con éxito."
                detail = summary
                show = MessageBox.showinfo

            self.set_status(summary)
            self.ui(self.queue_label.configure, text="")
            self.ui(self.progress_bar.set, 1.0 if not self.cancel_event.is_set() else 0)
            self.ui(self.set_download_buttons, "normal")
            send_notification("Multi Downloader Pro", summary)
            self.ui(show, "Finalizado", detail)

        threading.Thread(target=download_thread, daemon=True).start()

    def ydl_progress_hook(self, d):
        # Archivos a medias del elemento actual, para borrarlos si se cancela
        self.partial_files.update((d.get('tmpfilename'), d.get('filename')))
        self.thumb_files.update(t.get('filepath') for t in (d.get('info_dict') or {}).get('thumbnails') or [])
        if self.cancel_event.is_set():
            raise DownloadCancelled("Cancelado por el usuario")
        title = (d.get('info_dict') or {}).get('title') or ''
        title = title if len(title) <= 45 else title[:44] + "…"
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes') or 0
            if total_bytes > 0:
                pct = downloaded / total_bytes
                self.ui(self.progress_bar.set, pct)
                # yt-dlp añade colores ANSI si se lanzó desde una consola
                speed = remove_terminal_sequences(d.get('_speed_str') or 'N/A').strip()
                eta = remove_terminal_sequences(d.get('_eta_str') or 'N/A').strip()
                self.set_status(f"⬇️ {title} — {int(pct*100)}% · {speed} · quedan {eta}")
        elif d['status'] == 'finished':
            self.set_status(f"⚙️ {title} — procesando (unir / convertir / metadatos)...")


if __name__ == "__main__":
    root = ctk.CTk()
    app = MultiDownloaderGUI(root)
    root.mainloop()
