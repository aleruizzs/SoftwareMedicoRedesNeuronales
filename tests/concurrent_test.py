import asyncio
import aiohttp
import time

URL = "http://localhost:8001/predict/"
IMAGE_PATH = "prueba.jpeg"  # ⚠️ Asegúrate de tener esta imagen lista
MODEL_NAME = "columna"         # Cambia a "torax" o "fake" si prefieres

async def send_request(session, i):
    with open(IMAGE_PATH, "rb") as f:
        data = aiohttp.FormData()
        data.add_field("model", MODEL_NAME)
        data.add_field("image", f, filename="test.jpg", content_type="image/jpeg")

        start = time.perf_counter()
        async with session.post(URL, data=data) as resp:
            end = time.perf_counter()
            print(f"🧵 Petición {i} - Estado: {resp.status} - Tiempo: {end - start:.2f}s")
            return await resp.read()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, i) for i in range(1, 6)]  # 🔁 5 peticiones simultáneas
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
