import os
import requests

def download_file_from_gdrive(url, dest_path):
    if os.path.exists(dest_path):
        return

    print(f"Descargando modelo desde: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Modelo guardado en: {dest_path}")
