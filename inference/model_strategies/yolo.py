from ultralytics import YOLO
import cv2
import numpy as np
from .base import BaseModelStrategy

class YoloStrategy(BaseModelStrategy):
    def configure(self):
        self.model = YOLO("/app/modelos/yolov8n.pt")
        self.model.fuse()

    def predict(self, image):
        results = self.model(image)[0]
        output = image.copy()

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            label = self.model.names[cls_id]

            # Dibujar caja
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Etiqueta
            text = f"{label} {conf:.2f}"
            cv2.putText(output, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return output
