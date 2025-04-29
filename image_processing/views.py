import cv2
import numpy as np
import os
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ProcessedImage

import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


@api_view(['POST'])
@login_required
def process_image(request):
    if 'image' not in request.FILES or 'model' not in request.POST:
        return Response({"error": "Faltan campos"}, status=400)

    image_file = request.FILES['image']
    model_name = request.POST['model']

    # Enviar la imagen al servidor FastAPI
    response = requests.post(
        "http://inference:8001/predict/",
        data={'model': model_name},
        files={'image': (image_file.name, image_file.read(), image_file.content_type)}
    )


    if response.status_code != 200:
        return Response({"error": "Error desde el servidor de inferencia"}, status=500)

    # Guardar la imagen procesada recibida desde FastAPI
    output_filename = f"processed_{image_file.name}"
    output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
    with open(output_path, "wb") as f:
        f.write(response.content)

    ProcessedImage.objects.create(
        user=request.user,
        patient_dni=request.POST['patient_dni'],
        image_name=image_file.name,
        model_used=model_name,
        file_path=f"media/{output_filename}"
    )

    return Response({"processed_image": f"media/{output_filename}"})

@login_required
def index(request): 
    return render(request, 'index.html', {'user': request.user})

@login_required
def historial(request):
    imagenes = ProcessedImage.objects.filter(user=request.user)

    q = request.GET.get("q")
    if q:
        imagenes = imagenes.filter(patient_dni__icontains=q)

    return render(request, 'historial.html', {'imagenes': imagenes})


def custom_logout(request):
    django_logout(request)
    return redirect('login')

@csrf_protect
@login_required
def delete_image(request, image_id):
    if request.method == 'POST':
        try:
            imagen = ProcessedImage.objects.get(pk=image_id)
            imagen.delete()
            messages.success(request, "Imagen eliminada correctamente.")
        except ProcessedImage.DoesNotExist:
            messages.error(request, "La imagen ya no existe en la base de datos.")
        return redirect("historial")

    return redirect('historial')