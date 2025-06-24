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
    
def parse_points(points_str: str):
    """Convierte una cadena "x1,y1;x2,y2" en un array de puntos."""
    try:
        points = []
        for pair in points_str.split(';'):
            if not pair.strip():
                continue
            x_str, y_str = pair.split(',')
            points.append([int(x_str), int(y_str)])
        return np.array(points, dtype=np.int32)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de puntos inválido")


@app.post("/predict/")
async def predict(model: str = Form(...), image: UploadFile = File(...), points: str = Form(None)):
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

        parsed_points = parse_points(points) if points else None

        if model == "SAM-Med2D":
            out_img = strategy.predict(img, points=parsed_points)
        else:
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

