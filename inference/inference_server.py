from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
import cv2
import numpy as np
from .model_strategies.factory import get_model_strategy
import time
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

app = FastAPI()
loaded_strategies = {}

ALLOWED_EXTENSIONS = ["image/jpeg", "image/png"]

def validate_image_type(file: UploadFile):

    if file.content_type not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser una imagen en formato JPG, JPEG o PNG"
        )

@app.post("/predict/")
async def predict(model: str = Form(...), image: UploadFile = File(...)):
    print("Modelo recibido:", model)
    print("Tipo de archivo recibido:", image.content_type)
    print(f"Recibida petición {uuid.uuid4().hex[:5]} en {time.time()}")
    try:
        start_time = time.time()

        validate_image_type(image)
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="La imagen no pudo decodificarse. ¿Formato o tamaño incorrecto?")

        # Usa modelo cacheado si ya existe
        if model in loaded_strategies:
            strategy = loaded_strategies[model]
        else:
            strategy = get_model_strategy(model)
            strategy.configure()
            loaded_strategies[model] = strategy

        out_img = strategy.predict(img)

        filename = f"output_{uuid.uuid4().hex}.png"
        output_path = os.path.join("outputs", filename)
        os.makedirs("outputs", exist_ok=True)
        cv2.imwrite(output_path, out_img)

        total_time = time.time() - start_time
        print(f"Tiempo total de procesamiento: {total_time:.2f} segundos")

        return FileResponse(output_path, media_type="image/png")

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()  
        print("ERROR:", repr(e)) 
        return JSONResponse(
            status_code=500,
            content={"error": "Error interno en el servidor de inferencia"}
        )

