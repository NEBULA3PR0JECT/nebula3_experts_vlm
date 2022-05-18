# from typing import Optional
from fastapi import FastAPI

from typing import Optional

from nebula3_experts.experts.service.base_expert import BaseExpert
from nebula3_experts.experts.app import ExpertApp
from nebula3_experts.experts.common.defines import *

import sys
sys.path.insert(0, 'nebula3_vlm/')
sys.path.insert(0, 'nebula3_experts/')
sys.path.insert(0, 'nebula3_experts/experts/')
from nebula3_vlm.models.clip_ms.clip_ms import Model

class VlmExpert(BaseExpert):
    def __init__(self):
        super().__init__()
        # after init all
        self.set_active()

    def get_name(self):
        return "VlmExpert"
    def get_cfg(self) -> str:
        return {}
    def get_dependency(self) -> str:
        return "VlmExpert"


    def get_cfg(self):
        """return expert's name
        """
        pass

    def get_dependency(self):
        pass
    def get_status(self):   
        pass

    def get_tasks(self):   
        pass

    def handle_exit(self):   
        pass

    def handle_msg(self):   
        pass

    def add_expert_apis(self, app: FastAPI):
        @app.get("/my-expert")
        def get_my_expert(q: Optional[str] = None):
            return {"expert": "my-expert" }

    def predict(self, movie_id, scene_element, output: OutputStyle):
        """ handle new movie """
        pass
    
    def predict_on_txt(self, app: FastAPI):
        """ Prediction on text """
        @app.get("/predict-on-txt/{txt}")
        def get_my_expert(txt: Optional[str] = 'test'):
            clip_model = Model()
            data = {}
            data['text'] = txt
            result = clip_model.encode_text(data)
            return { 'result': result}
    
    def predict_on_video(self, app: FastAPI):
        """ Prediction on video """
        @app.get("/predict-on-video/{movie_id}/{scene_element}")
        def get_my_expert(movie_id: Optional[str] = '114208777', scene_element: Optional[int] = 0):
            clip_model = Model()
            data = {}
            full_movie_id = "Movies/" + movie_id
            data['movie_id'] = full_movie_id
            data['scene_element'] = scene_element
            result = clip_model.encode_video(data)
            return { 'result': result}

my_expert = VlmExpert()
expert_app = ExpertApp(expert=my_expert)
app = expert_app.get_app()
expert_app.run()
