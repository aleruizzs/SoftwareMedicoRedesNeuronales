
# tests/test_caja_negra.py

import pytest
from fastapi.testclient import TestClient
from inference_server import app

client = TestClient(app)

def get_test_image(path="media/prueba.jpg"):
    return open(path, "rb")

def test_tc01_jpg():
    with get_test_image() as img:
        response = client.post("/predict/", files={"image": ("test.jpg", img, "image/jpeg")}, data={"model": "fake"})
        assert response.status_code == 200

def test_tc02_png():
    with open("media/prueba.png", "rb") as img:
        response = client.post("/predict/", files={"image": ("test.png", img, "image/png")}, data={"model": "fake"})
        assert response.status_code == 200

def test_tc03_jpeg():
    with open("media/prueba.jpeg", "rb") as img:
        response = client.post("/predict/", files={"image": ("test.jpeg", img, "image/jpeg")}, data={"model": "fake"})
        assert response.status_code == 200

def test_tc04_invalid_format_pdf():
    with open("media/prueba.pdf", "rb") as file:
        response = client.post("/predict/", files={"image": ("test.pdf", file, "application/pdf")}, data={"model": "columna"})
        assert response.status_code == 400
        assert "imagen" in response.json().get("detail", "").lower()


def test_tc05_oversize_image():
    # Simula una imagen de más de 50MB
    big_content = b"\xff" * (51 * 1024 * 1024)
    response = client.post("/predict/", files={"image": ("big.jpg", big_content, "image/jpeg")}, data={"model": "columna"})
    assert response.status_code in (400, 413)

def test_tc06_columna_model():
    with get_test_image() as img:
        response = client.post("/predict/", files={"image": ("test.jpg", img, "image/jpeg")}, data={"model": "columna"})
        assert response.status_code == 200

def test_tc07_torax_model():
    with get_test_image() as img:
        response = client.post("/predict/", files={"image": ("test.jpg", img, "image/jpeg")}, data={"model": "torax"})
        assert response.status_code == 200

def test_tc08_no_image_sent():
    response = client.post("/predict/", data={"model": "fake"})
    assert response.status_code == 422  # Unprocessable Entity
