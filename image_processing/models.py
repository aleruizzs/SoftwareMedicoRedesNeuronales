from django.db import models
from django.contrib.auth.models import User

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_dni = models.CharField(max_length=20)
    image_name = models.CharField(max_length=255)
    model_used = models.CharField(max_length=50)
    file_path = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_dni} - {self.image_name} ({self.model_used})"