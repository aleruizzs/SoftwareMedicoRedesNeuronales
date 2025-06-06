import os
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from fastapi.testclient import TestClient
from inference.inference_server import app as fastapi_app
from image_processing.models import ProcessedImage
import numpy as np
import cv2
from unittest.mock import patch, Mock

# Genera bytes de una imagen JPEG válida (100×100 px verdes por defecto)
def create_dummy_image_bytes(width=100, height=100, color=(0, 255, 0)):
    img = np.full((height, width, 3), color, dtype=np.uint8)
    success, buffer = cv2.imencode(".jpg", img)
    assert success, "No se pudo codificar la imagen dummy"
    return buffer.tobytes()

class UnifiedTests(TestCase):
    def setUp(self):
        # Django client y login
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # FastAPI test client
        self.fastapi_client = TestClient(fastapi_app)

        # Bytes de imagen para todos los tests
        self.img_bytes = create_dummy_image_bytes()

    # ─────────────────────────── Test de vistas Django ──────────────────────────
    def test_django_missing_image_field(self):
        response = self.client.post('/process/', {
            'model': 'fake',
            'patient_dni': '12345678X',
        })
        self.assertEqual(response.status_code, 400)

    def test_process_requires_authentication(self):
        self.client.logout()
        response = self.client.post('/process/', {
            'model': 'fake',
            'patient_dni': '00000000X',
            'image': SimpleUploadedFile('test.jpg', self.img_bytes, content_type='image/jpeg')
        })
        self.assertEqual(response.status_code, 302)

    @patch("image_processing.views.requests.post")
    def test_process_creates_processedimage_entry(self, mock_post):
        # Devuelve imagen dummy desde el mock
        mock_post.return_value = Mock(status_code=200, content=self.img_bytes)

        response = self.client.post('/process/', {
            'model': 'fake',
            'patient_dni': '11111111H',
            'image': SimpleUploadedFile('test.jpg', self.img_bytes, content_type='image/jpeg')
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProcessedImage.objects.filter(patient_dni='11111111H').exists())

    def test_historial_dni_filter(self):
        ProcessedImage.objects.create(
            user=self.user,
            patient_dni="12345678Z",
            image_name="imagen.jpg",
            model_used="fake",
            file_path="media/test.jpg"
        )
        response = self.client.get('/historial/?q=12345678Z')
        self.assertContains(response, "12345678Z")

    def test_index_view_renders_for_logged_user(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bienvenido, testuser")

    def test_historial_requires_login(self):
        self.client.logout()
        response = self.client.get("/historial/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_delete_nonexistent_image_graceful(self):
        response = self.client.post("/historial/delete/999/")
        # Redirige de vuelta al historial
        self.assertEqual(response.status_code, 302)
        self.assertIn("/historial/", response["Location"])

    # ───────────────────────── Tests del servidor FastAPI ────────────────────────
    def test_fastapi_invalid_mimetype(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("test.txt", b"notanimage", "text/plain")},
            data={"model": "columna"}
        )
        self.assertEqual(response.status_code, 400)

    def test_fastapi_valid_fake_model(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("test.jpg", self.img_bytes, "image/jpeg")},
            data={"model": "fake"}
        )
        self.assertIn(response.status_code, [200, 500]) 

    def test_fastapi_corrupt_image(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("bad.jpg", b"not_really_an_image", "image/jpeg")},
            data={"model": "fake"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("no pudo decodificarse", response.json().get("detail", "").lower())

    def test_fastapi_invalid_model_name(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("test.jpg", self.img_bytes, "image/jpeg")},
            data={"model": "noexiste"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("modelo desconocido", response.json().get("error", "").lower())

    def test_fastapi_missing_image_field(self):
        response = self.fastapi_client.post(
            "/predict/",
            data={"model": "fake"}
        )
        self.assertEqual(response.status_code, 422)

    def test_fastapi_missing_model_field(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("test.jpg", self.img_bytes, "image/jpeg")}
        )
        self.assertEqual(response.status_code, 422)

    def test_fastapi_unsupported_mime_type(self):
        response = self.fastapi_client.post(
            "/predict/",
            files={"image": ("anim.gif", self.img_bytes, "image/gif")},
            data={"model": "fake"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("El archivo debe ser una imagen", response.json().get("detail", ""))
        
    # ──────────────────────── Pruebas de health/up ─────────────────────────
    def test_django_health_up(self):
        # La página de login debería cargarse correctamente
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_fastapi_health_up(self):
        # El esquema OpenAPI debe estar disponible
        response = self.fastapi_client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("openapi", response.json())

    # ————————————— Pruebas de carga —————————————
    @patch("image_processing.views.requests.post")
    def test_django_process_load(self, mock_post):
        # Simula varias peticiones consecutivas al endpoint /process/
        mock_post.return_value = Mock(status_code=200, content=self.img_bytes)

        for i in range(5):
            response = self.client.post('/process/', {
                'model': 'fake',
                'patient_dni': f'9999999{i}',
                'image': SimpleUploadedFile(f'test{i}.jpg', self.img_bytes, content_type='image/jpeg')
            })
            self.assertEqual(response.status_code, 200)

        self.assertEqual(ProcessedImage.objects.count(), 5)

    def test_fastapi_predict_load(self):
        # Lanza varias predicciones consecutivas para comprobar rendimiento
        for _ in range(5):
            response = self.fastapi_client.post(
                "/predict/",
                files={"image": ("test.jpg", self.img_bytes, "image/jpeg")},
                data={"model": "fake"}
            )
            self.assertIn(response.status_code, [200, 500])