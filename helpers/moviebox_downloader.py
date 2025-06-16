import os
import requests
from tqdm import tqdm
from colorama import Fore

def handle_moviebox(link: str) -> str:
    path = os.getenv('VIDEO_OUTPUT_PATH', '.')
    filename = os.path.join(path, link.split('/')[-1])

    try:
        response = requests.get(link, stream=True)
        total = int(response.headers.get('content-length', 0))
        with open(filename, 'wb') as f, tqdm(
            desc=f"Downloading {filename}",
            total=total,
            unit='B',
            unit_scale=True
        ) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        return f"MovieBox download complete: {filename}"
    except Exception as e:
        return f"MovieBox download failed: {e}"