import pytest
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert "Iniciar sesión" in response.content.decode()

@pytest.mark.django_db
def test_historial_requires_authentication(client):
    response = client.get(reverse('historial'))
    assert response.status_code in (302, 403)

@pytest.mark.django_db
def test_index_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(username="testuser", password="12345")
    client.login(username="testuser", password="12345")
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert "Analizar Imagen" in response.content.decode()

@pytest.mark.django_db
def test_upload_and_access_historial(client, django_user_model):
    user = django_user_model.objects.create_user(username="testuser2", password="12345")
    client.force_login(user)

    with open("media/prueba.jpg", "rb") as f:
        test_file = SimpleUploadedFile("test.jpg", f.read(), content_type="image/jpeg")

    response = client.post(
        reverse('process_image'),
        data={
            'model': 'fake',
            'patient_dni': '12345678X',
            'image': test_file
        },
        format='multipart'  # importante para que Django lo trate como multipart/form-data
    )

    print("❗ Respuesta:", response.content.decode())
    assert response.status_code in (200, 302)


