from fault_prediction.sensor.components import data_ingestion
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
import os,sys
import pandas  as pd
from fault_prediction.sensor.entity import artifact_entity,config_entity
from fault_prediction.sensor.utils import get_data
from fault_prediction.sensor.config import mongoclient
from fault_prediction.sensor.components.data_ingestion import DataIngesation
from fault_prediction.sensor.components import data_validation
from fault_prediction.sensor.components.data_validation import  DataValidation
import yaml
if __name__ == "__main__":
    try:


        train_config = config_entity.Trainingconfig()
        data_ingestion_config = config_entity.dataingestionconfig(train_config=train_config)
        
        print(data_ingestion_config.to_dict())

        dataIngestation = DataIngesation(data_ingestion_config)
        data_ingestion_artifact=dataIngestation.initiate_dataingesation()
        data_validation_config = config_entity.datavalidationconfig(train_config=train_config)
        data_validate = data_validation.DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validate.initiate_data_validation()
    
    except Exception as e:
        raise SensorException(e,sys)