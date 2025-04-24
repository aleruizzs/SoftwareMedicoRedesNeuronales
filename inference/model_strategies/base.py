class BaseModelStrategy:
    def __init__(self):
        self.predictor = None
        self.cfg = None

    def configure(self):
        """Configura el modelo (cargar pesos, etc.)"""
        raise NotImplementedError()

    def predict(self, image):
        """Aplica la predicción a la imagen."""
        raise NotImplementedError()
