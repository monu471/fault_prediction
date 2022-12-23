import os,sys
from fault_prediction.sensor.entity import  config_entity,artifact_entity
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor.logger import logging
from typing import Optional
from fault_prediction.sensor.entity.config_entity import Transformer_object_file,model_file,Target_encoder_object_file

class ModelResolver:
    def __init__(self,model_registry= "saved_models",
                 tranformer_dir_name = "transformer",
                target_encoder_dir_name = "target_encoder",
                  model_dir_name = "model"):


    
        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = tranformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name


    def get_latest_dir_path(self):
        try:
            dir_name = os.listdir(self.model_registry)
            if len(dir_name)==0:
                return None
            dir_name = list(map(int,dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registry,f"{latest_dir_name}")
        except Exception as e:
            raise SensorException(e,sys)


    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise ("model is not available")
            return os.path.join(latest_dir,self.model_dir_name,model_file)
        except Exception as e:
            raise e





    def get_latest_transformer_path(self):
        try:
            latest_dir  = self.get_latest_dir_path()
            if latest_dir is None:
                raise ("transformer is not available")
            return os.path.join(latest_dir,self.transformer_dir_name,Transformer_object_file)
        except Exception as e:
            raise e


    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None :
                raise Exception ("Target encoder is not available")
            return os.path.join(latest_dir,self.target_encoder_dir_name,Target_encoder_object_file)
        except Exception as e:
            raise e

    def get_latest_save_dir_path(self):
            try:
                latest_dir = self.get_latest_dir_path()
                if latest_dir==None:
                    return os.path.join(self.model_registry,f"{0}")
                latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
                return os.path.join(self.model_registry,f"{latest_dir_num+1}")
            except Exception as e:
                raise e
    def get_latest_save_model_path(self):
            try:
                latest_dir = self.get_latest_save_dir_path()
                return os.path.join(latest_dir,self.model_dir_name,model_file)
            except Exception as e:
                raise e

    def get_latest_save_transformer_path(self):
            try:
                latest_dir = self.get_latest_save_dir_path()
                return os.path.join(latest_dir,self.transformer_dir_name,Transformer_object_file)
            except Exception as e:
                raise e
    def get_latest_save_target_encoder_path(self):
            try:
                latest_dir = self.get_latest_save_dir_path()
                return os.path.join(latest_dir,self.target_encoder_dir_name,Target_encoder_object_file)
            except Exception as e:
                raise e

