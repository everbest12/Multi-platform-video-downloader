import os
import yt_dlp
from tqdm import tqdm
from colorama import Fore, Style

pbar = None

def progress_hook(d):
    global pbar
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if pbar is None and total:
            bar_format = f"{Fore.GREEN}{{l_bar}}{{bar}}{Style.RESET_ALL} {{n_fmt}}/{{total_fmt}} [{{elapsed}}<{{remaining}}, {{rate_fmt}}]"
            pbar = tqdm(total=total, unit='B', unit_scale=True, desc="Downloading", ncols=80, bar_format=bar_format)
        if pbar:
            pbar.n = downloaded
            pbar.refresh()
    elif d['status'] == 'finished':
        if pbar:
            pbar.n = pbar.total
            pbar.refresh()
            pbar.close()
            print(Fore.GREEN + "DOWNLOAD COMPLETE!")
            pbar = None

def get_opts():
    quality = os.getenv('VIDEO_QUALITY', 'best')
    path = os.getenv('VIDEO_OUTPUT_PATH', '.')
    return {
        'format': quality,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True
    }

def handle_facebook(link: str) -> str:
    opts = get_opts()
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([link])
    return "Facebook download completed."