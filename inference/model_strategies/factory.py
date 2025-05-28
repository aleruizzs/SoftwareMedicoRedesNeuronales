def get_model_strategy(model_name: str):
    if model_name == "columna":
        from .columna import ColumnaStrategy
        return ColumnaStrategy()
    elif model_name == "torax":
        from .torax import ToraxStrategy
        return ToraxStrategy()
    elif model_name == "fake":
        from .fake import FakeStrategy
        return FakeStrategy()
    elif model_name == "yolo":
        from .yolo import YoloStrategy
        return YoloStrategy()

    else:
        raise ValueError(f"Modelo desconocido: {model_name}")
