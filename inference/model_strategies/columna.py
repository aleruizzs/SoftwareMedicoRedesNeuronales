import importlib
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import numpy as np
from .base import BaseModelStrategy
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from huggingface_hub import hf_hub_download
import os 

class ColumnaStrategy(BaseModelStrategy):
    def configure(self):
        cfg = get_cfg()
        cfg.merge_from_file(
            model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        )
        cfg.MODEL.WEIGHTS = "/app/modelos/columna.pth"
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        cfg.MODEL.DEVICE = "cpu"
        self.cfg = cfg
        self.predictor = DefaultPredictor(cfg)

    def predict(self, image):
        outputs = self.predictor(image)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu")).get_image()
        return out[:, :, ::-1]