# helpers/coursera_downloader.py
import os
import yt_dlp
from colorama import Fore
from tqdm import tqdm

def handle_coursera(link: str) -> str:
    path = os.getenv('VIDEO_OUTPUT_PATH', '.')
    quality = os.getenv('VIDEO_QUALITY', 'best')
    cookies_path = "coursera_cookies.txt"

    if not os.path.exists(cookies_path):
        return "❌ 'coursera_cookies.txt' file not found. Please export cookies and place in project root."

    opts = {
        'format': quality,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'quiet': True,
        'cookiefile': cookies_path,
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([link])

    return Fore.GREEN + "✅ Coursera download completed."

# Progress bar
pbar = None
def progress_hook(d):
    global pbar
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if pbar is None and total:
            pbar = tqdm(total=total, unit='B', unit_scale=True, desc="Downloading Coursera")
        if pbar:
            pbar.n = downloaded
            pbar.refresh()
    elif d['status'] == 'finished' and pbar:
        pbar.close()
        pbar = None
