import os
import requests

# Diccionario de modelos con IDs de Google Drive
MODELOS = {
    "columna": "1KmTkWBdeB693WgotCtsNoZLYEoXcPTrE",
    "torax": "14lDHMPvnlfJ5oklv8jbxpn1JNaqK7mai"
}

def descargar_de_drive(file_id, destino):
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={"id": file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        response = session.get(URL, params={"id": file_id, "confirm": token}, stream=True)

    guardar_contenido(response, destino)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def guardar_contenido(response, destino):
    CHUNK_SIZE = 32768

    with open(destino, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

def descargar_modelos():
    os.makedirs("modelos", exist_ok=True)
    for nombre, file_id in MODELOS.items():
        ruta_local = os.path.join("modelos", f"{nombre}.pth")
        if not os.path.exists(ruta_local):
            print(f"📥 Descargando {nombre} desde Google Drive...")
            descargar_de_drive(file_id, ruta_local)
            print(f"✅ Guardado en {ruta_local}")
        else:
            print(f"✔ {nombre} ya existe.")

if __name__ == "__main__":
    descargar_modelos()
