def get_model_strategy(model_name: str):
    if model_name == "Columna":
        from .columna import ColumnaStrategy
        return ColumnaStrategy()
    elif model_name == "Fake":
        from .fake import FakeStrategy
        return FakeStrategy()
    elif model_name == "SAM-Med2D":
        from .sammed2d import SamMed2DStrategy
        return SamMed2DStrategy()

    else:
        raise ValueError(f"Modelo desconocido: {model_name}")
