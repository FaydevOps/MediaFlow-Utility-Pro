import os
import sys
import time
import json
import random
import shutil
import tempfile
import requests
import urllib.request
from urllib.parse import urlparse
from yt_dlp import YoutubeDL

# --- LIBRERÍA RICH PARA INTERFAZ VISUAL ---
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich import print as rprint

console = Console()

# Manejo seguro de browser_cookie3
try:
    import browser_cookie3
    COOKIES_AVAILABLE = True
except ImportError:
    COOKIES_AVAILABLE = False

# --- FUNCIONES AUXILIARES ---

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.101 Mobile Safari/537.36',
    ]
    return random.choice(user_agents)

def get_proxy_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "proxies.json")

def load_proxy_list():
    proxy_file = get_proxy_file_path()
    if os.path.exists(proxy_file):
        try:
            with open(proxy_file, 'r') as f:
                proxies = json.load(f)
                return proxies.get('http', []), proxies.get('socks5', [])
        except Exception:
            pass
    return [], []

def save_proxy_list(http_proxies, socks5_proxies):
    proxy_file = get_proxy_file_path()
    proxy_data = {'http': http_proxies, 'socks5': socks5_proxies}
    try:
        with open(proxy_file, 'w') as f:
            json.dump(proxy_data, f, indent=2)
        return True
    except Exception:
        return False

def get_proxies_from_api(proxy_type='http', timeout=10000):
    try:
        params = {
            'request': 'display_proxies',
            'proxy_format': 'protocolipport',
            'format': 'text',
            'timeout': timeout,
        }
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get"
        headers = {'User-Agent': get_random_user_agent()}
        
        console.print("[cyan]🔍 Obteniendo proxies de la API...[/cyan]")
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            proxies_text = response.text.strip()
            if proxies_text:
                proxies = [p.strip() for p in proxies_text.split('\n') if p.strip()]
                console.print(f"[bold green]✅ Obtenidos {len(proxies)} proxies de la API[/bold green]")
                return proxies
    except requests.RequestException as e:
        console.print(f"[bold red]❌ Error de conexión con la API: {e}[/bold red]")
    
    return []

def get_random_proxy(proxy_type='http'):
    http_proxies, socks5_proxies = load_proxy_list()
    if proxy_type == 'http' and http_proxies:
        return random.choice(http_proxies)
    elif proxy_type == 'socks5' and socks5_proxies:
        return random.choice(socks5_proxies)
    
    api_proxies = get_proxies_from_api(proxy_type)
    if api_proxies:
        if proxy_type == 'http':
            save_proxy_list(api_proxies, socks5_proxies)
        else:
            save_proxy_list(http_proxies, api_proxies)
        return random.choice(api_proxies)
    return None

# --- CLASE PRINCIPAL CON INTERFAZ RICH ---

class DownloaderCLI:
    def __init__(self):
        self.url = ""
        self.video_resolution = "720p"
        self.video_format = "mp4"
        self.audio_format = "mp3"
        
        termux_storage = os.path.expanduser("~/storage/downloads")
        if os.path.exists(termux_storage):
            self.output_path = termux_storage
        else:
            self.output_path = os.path.expanduser("~")
            
        self.use_proxy = False
        self.proxy_type = "http"

    def print_header(self):
        banner = """
[bold cyan]⚡ TERMUX MULTI-DOWNLOADER ⚡[/bold cyan]
[dim]Descarga videos y audio con alta velocidad y soporte de proxies[/dim]
        """
        console.print(Panel(banner.strip(), border_style="cyan", expand=False))

    def render_dashboard(self):
        console.clear()
        self.print_header()

        # Tabla de Configuración Actual
        table = Table(title="📌 Configuración Actual", show_header=True, header_style="bold magenta")
        table.add_column("Parámetro", style="bold white", width=20)
        table.add_column("Valor", style="yellow")

        url_display = self.url if len(self.url) <= 45 else f"{self.url[:42]}..."
        proxy_status = f"[bold green]SÍ ({self.proxy_type.upper()})[/bold green]" if self.use_proxy else "[bold red]NO[/bold red]"

        table.add_row("🔗 URL", url_display or "[dim]No ingresada[/dim]")
        table.add_row("📁 Carpeta", self.output_path)
        table.add_row("🎬 Calidad / Formato", f"{self.video_resolution} | {self.video_format.upper()}")
        table.add_row("🔊 Formato Audio", self.audio_format.upper())
        table.add_row("🛡️ Proxy", proxy_status)

        console.print(table)

        # Menú de Opciones
        menu_table = Table(show_header=False, box=None)
        menu_table.add_column("Opción", style="bold cyan")
        menu_table.add_column("Descripción", style="bold white")

        menu_table.add_row("[1]", "Modificar URL")
        menu_table.add_row("[2]", "Cambiar Carpeta Destino")
        menu_table.add_row("[3]", "Configurar Calidad y Formatos")
        menu_table.add_row("[4]", "Ajustes de Proxy")
        menu_table.add_row("-----------------", "-----------------")
        menu_table.add_row("[D]", "[bold green]⬇️  Descargar Video + Audio[/bold green]")
        menu_table.add_row("[A]", "[bold blue]🔊  Descargar Solo Audio[/bold blue]")
        menu_table.add_row("[V]", "[bold purple]🎥  Descargar Solo Video[/bold purple]")
        menu_table.add_row("[Q]", "[bold red]❌  Salir[/bold red]")

        console.print(Panel(menu_table, title="[bold yellow]Opciones[/bold yellow]", border_style="yellow"))

    def handle_menu_choice(self, choice):
        choice = choice.upper().strip()
        
        if choice == '1':
            self.url = Prompt.ask("[bold cyan]Ingresa la URL del video[/bold cyan]", default=self.url)
        elif choice == '2':
            new_path = Prompt.ask("[bold cyan]Ruta de destino[/bold cyan]", default=self.output_path)
            expanded = os.path.expanduser(new_path)
            if os.path.isdir(expanded):
                self.output_path = expanded
            else:
                console.print("[bold red]❌ La ruta no existe. Ejecuta 'termux-setup-storage' si usas la SD.[/bold red]")
                time.sleep(2)
        elif choice == '3':
            self.configure_formats()
        elif choice == '4':
            self.manage_proxies()
        elif choice == 'D':
            self.start_download(audio_only=False, video_only=False)
        elif choice == 'A':
            self.start_download(audio_only=True, video_only=False)
        elif choice == 'V':
            self.start_download(audio_only=False, video_only=True)
        elif choice == 'Q':
            console.print("[bold yellow]👋 ¡Hasta luego![/bold yellow]")
            sys.exit(0)

    def configure_formats(self):
        console.clear()
        self.print_header()
        
        console.print("[bold yellow]--- CONFIGURACIÓN DE FORMATOS ---[/bold yellow]\n")
        self.video_resolution = Prompt.ask(
            "Selecciona la resolución de video",
            choices=["2160p", "1440p", "1080p", "720p", "480p", "360p", "mejor"],
            default=self.video_resolution
        )
        self.video_format = Prompt.ask(
            "Selecciona el formato del video",
            choices=["mp4", "mkv", "webm"],
            default=self.video_format
        )
        self.audio_format = Prompt.ask(
            "Selecciona el formato del audio",
            choices=["mp3", "m4a", "wav"],
            default=self.audio_format
        )

    def manage_proxies(self):
        console.clear()
        self.print_header()
        
        self.use_proxy = Confirm.ask("¿Deseas activar el uso de proxies?", default=self.use_proxy)
        if self.use_proxy:
            self.proxy_type = Prompt.ask("Tipo de proxy", choices=["http", "socks5"], default=self.proxy_type)
            if Confirm.ask("¿Obtener una lista nueva de proxies ahora?"):
                get_proxies_from_api(self.proxy_type)
                Prompt.ask("\nPresiona [enter] para continuar")

    def start_download(self, audio_only, video_only):
        if not self.url:
            console.print("[bold red]❌ Por favor ingresa una URL primero.[/bold red]")
            time.sleep(1.5)
            return

        console.clear()
        self.print_header()

        temp_dir = tempfile.mkdtemp()
        try:
            final_output_path = os.path.abspath(self.output_path)
            os.makedirs(final_output_path, exist_ok=True)

            ydl_opts = {
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'socket_timeout': 30,
                'retries': 5,
                'nocheckcertificate': True,
                'quiet': True,
            }

            if self.use_proxy:
                proxy = get_random_proxy(self.proxy_type)
                if proxy:
                    ydl_opts['proxy'] = f'{self.proxy_type}://{proxy}'
                    console.print(f"[cyan]🛡️ Usando Proxy: {proxy}[/cyan]")

            ydl_opts['http_headers'] = {'User-Agent': get_random_user_agent()}

            if audio_only:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': self.audio_format,
                        'preferredquality': '192',
                    }],
                })
            elif video_only:
                fmt_res = self.video_resolution.replace('p', '')
                ydl_opts['format'] = f'bestvideo[height<={fmt_res}]/bestvideo' if fmt_res.isdigit() else 'bestvideo'
            else:
                fmt_res = self.video_resolution.replace('p', '')
                if fmt_res.isdigit():
                    ydl_opts['format'] = f'bestvideo[height<={fmt_res}]+bestaudio/best[height<={fmt_res}]/best'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = self.video_format

            console.print("[bold yellow]⏳ Obteniendo información e iniciando descarga...[/bold yellow]")

            # Barra de progreso con Rich
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(bar_width=None, style="black", complete_style="green"),
                "[progress.percentage]{task.percentage:>3.0f}%",
                "•",
                TransferSpeedColumn(),
                "•",
                TimeRemainingColumn(),
                console=console
            ) as progress:

                task_id = progress.add_task("Descargando...", total=100)

                def custom_hook(d):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        downloaded = d.get('downloaded_bytes', 0)
                        if total > 0:
                            percentage = (downloaded / total) * 100
                            progress.update(task_id, completed=percentage)
                    elif d['status'] == 'finished':
                        progress.update(task_id, completed=100, description="[bold green]Procesando archivo...")

                ydl_opts['progress_hooks'] = [custom_hook]

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])

            # Mover archivo al directorio final
            for filename in os.listdir(temp_dir):
                source_path = os.path.join(temp_dir, filename)
                if os.path.isfile(source_path) and not filename.endswith('.part'):
                    destination_path = os.path.join(final_output_path, filename)
                    shutil.move(source_path, destination_path)

            console.print(f"\n[bold green]🎉 ¡Descarga completada con éxito![/bold green]")
            console.print(f"[bold cyan]📁 Guardado en: {final_output_path}[/bold cyan]\n")

        except Exception as e:
            console.print(f"\n[bold red]❌ Error durante la descarga: {e}[/bold red]\n")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            Prompt.ask("Presiona [enter] para volver al menú")

    def run(self):
        while True:
            self.render_dashboard()
            choice = Prompt.ask("\n[bold cyan]Selecciona una opción[/bold cyan]")
            self.handle_menu_choice(choice)

if __name__ == '__main__':
    try:
        app = DownloaderCLI()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]¡Proceso cancelado por el usuario![/bold yellow]")
        sys.exit(0)
