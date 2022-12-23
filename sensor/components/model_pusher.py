from fault_prediction.sensor.predictor import ModelResolver
from fault_prediction.sensor.entity.config_entity import ModelPusherConfig
from fault_prediction.sensor.exception import SensorException
import os,sys
from fault_prediction.sensor.utils import load_object,save_object
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.entity.artifact_entity import datattransformation_artifact,modeltraining_artifact,modelpusher_artifact
class ModelPusher:

    def __init__(self,model_pusher_config,data_transformation_artifact,model_trainer_artifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.model_pusher_config=model_pusher_config
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_pusher(self,):
        try:
            #load object
            logging.info(f"Loading transformer model and target encoder")
            transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            model = load_object(file_path=self.model_trainer_artifact.model_path)
            target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            #model pusher dir
            logging.info(f"Saving model into model pusher directory")
            save_object(file_path=self.model_pusher_config.pusher_transformer_path, object=transformer)
            save_object(file_path=self.model_pusher_config.pusher_model_path, object=model)
            save_object(file_path=self.model_pusher_config.pusher_target_encoder_path, object=target_encoder)


            #saved model dir
            logging.info(f"Saving model in saved model dir")
            transformer_path=self.model_resolver.get_latest_save_transformer_path()
            model_path=self.model_resolver.get_latest_save_model_path()
            target_encoder_path=self.model_resolver.get_latest_save_target_encoder_path()

            save_object(file_path=transformer_path, object=transformer)
            save_object(file_path=model_path, object=model)
            save_object(file_path=target_encoder_path, object=target_encoder)

            model_pusher_artifact = modelpusher_artifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
            saved_model_dir=self.model_pusher_config.saved_model_dir)
            logging.info(f"Model pusher artifact: {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise SensorException(e, sys)
