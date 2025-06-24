# model_strategies/sammed2d.py
import os
import sys
import numpy as np
import cv2
from .base import BaseModelStrategy

class SamMed2DStrategy(BaseModelStrategy):
    def configure(self):
        repo_path = os.path.join(os.path.dirname(__file__), "SAM-Med2D")
        sys.path.append(repo_path)
        from segment_anything import sam_model_registry
        from segment_anything.predictor_sammed import SammedPredictor
        from argparse import Namespace

        checkpoint = os.path.join(repo_path, "pretrain_model", "sam-med2d_b.pth")
        args = Namespace(image_size=256, encoder_adapter=True, sam_checkpoint=checkpoint)
        device = "cpu"  # Cambia a "cuda" si hay GPU disponible/configurada
        self.model = sam_model_registry["vit_b"](args).to(device)
        self.predictor = SammedPredictor(self.model)

    def predict(self, image, points=None):
        """Realiza la predicción permitiendo especificar puntos de entrada.

        Parameters
        ----------
        image : np.ndarray
            Imagen sobre la que realizar la segmentación.
        points : list or np.ndarray, optional
            Lista de coordenadas ``[[x1, y1], [x2, y2], ...]``. Si no se
            proporciona se usará el centro de la imagen.
        """

        if points is None:
            # Si no se indican puntos, usar el centro de la imagen como ejemplo
            h, w = image.shape[:2]
            input_point = np.array([[w // 2, h // 2]])
        else:
            input_point = np.array(points, dtype=np.int32)

        # Cada punto se etiqueta con '1' para indicar que es un punto positivo
        input_label = np.ones(len(input_point), dtype=np.int32)

        self.predictor.set_image(image)
        masks, scores, logits = self.predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=False
        )
        mask = masks[0].astype(np.uint8)
        output = image.copy()
        output[mask == 1] = [255, 0, 0]  # Pinta la máscara en rojo
        return output
