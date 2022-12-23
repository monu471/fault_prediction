import os,sys
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
from datetime import datetime
FILE = "sensor.csv"
Train_file = 'train.csv'
Test_file = "test.csv"
Transformer_object_file = 'transformer.pkl'
Target_encoder_object_file = "target_encoder.pkl"
model_file = "model.pkl"


class Trainingconfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e :
            raise(e,sys)

class dataingestionconfig :
    def __init__(self,train_config):
        try :
            self.database = "aps"
            self.collection = "sensor"
            self.test_size = 0.2
            self.dataingestation_dir = os.path.join(train_config.artifact_dir,"data_ingestion")
            self.feature_store_path = os.path.join(self.dataingestation_dir,"feature_store",FILE )
            self.train_file_path = os.path.join(self.dataingestation_dir,"dataset",Train_file)
            self.test_file_path = os.path.join(self.dataingestation_dir,"dataset",Test_file)

        
        except Exception as e :
           raise SensorException(e,sys)

    def to_dict(self):
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e,sys)         


class datavalidationconfig :
    def __init__(self,train_config):
        self.datavalidation_dir = os.path.join(train_config.artifact_dir,"data_validation")
        self.report_file_path = os.path.join(self.datavalidation_dir,"report.yaml")
        self.missing_threshold = 0.2
        self.base_file_path = r"E:\aps sensor\fault_prediction\sensor\aps_failure_training_set1.csv"


class datatransformationconfig :
    def __init__(self,train_config):
        self.datatransformation_dir = os.path.join(train_config.artifact_dir,"data_transformation" )
        self.transformed_object = os.path.join(self.datatransformation_dir,"transformer",Transformer_object_file)
        self.transformed_train_path  = os.path.join(self.datatransformation_dir,"transformed",Train_file.replace("csv","npz"))
        self.transformed_test_path = os.path.join(self.datatransformation_dir,"transformed",Test_file.replace("csv","npz"))
        self.target_encoder_file_path = os.path.join(self.datatransformation_dir,"target_encoder",Target_encoder_object_file)
      
class modeltraningconfig:
    def __init__(self,train_config):
        self.modeltraining_dir = os.path.join(train_config.artifact_dir,"model_trainer")
        self.model_path = os.path.join(self.modeltraining_dir,"model",model_file)
        self.expected_score = 0.7
        self.overfitting_threshold = 0.1
              
class modelevaluationconfig:
    def __init__(self,train_config):
        self.change_threshold = 0.01


class ModelPusherConfig:

    def __init__(self,train_config):
        self.model_pusher_dir = os.path.join(train_config.artifact_dir , "model_pusher")
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,model_file)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,Transformer_object_file)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,Target_encoder_object_file)
        
