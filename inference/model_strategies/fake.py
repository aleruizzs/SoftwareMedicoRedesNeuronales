import cv2
from .base import BaseModelStrategy

class FakeStrategy(BaseModelStrategy):
    def configure(self):
        pass  # No necesita configuración real

    def predict(self, image):
        output = image.copy()
        height, width = output.shape[:2]

        # Dibujar rectángulo
        cv2.rectangle(output, (int(width*0.2), int(height*0.2)), (int(width*0.8), int(height*0.8)), (0, 255, 0), 4)

        # Añadir texto de demo
        cv2.putText(output, "Procesada (demo)", (50, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        return output
