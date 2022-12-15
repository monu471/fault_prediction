import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from datetime import datetime
FILE = "sensor.csv"
Train_file = 'train.csv'
Test_file = "test.csv"
class Trainingconfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e :
            raise(e,sys)

class dataingestion_config :
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
