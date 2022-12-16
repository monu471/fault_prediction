from fault_prediction.sensor.components import data_ingestion
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
import os,sys
import pandas  as pd
from fault_prediction.sensor.entity import artifact_entity,config_entity
from fault_prediction.sensor.utils import get_data
if __name__ == "__main__":
    try:


        train_config = config_entity.Trainingconfig()
        data_ingestion_config = config_entity.dataingestionconfig(train_config=train_config)
        print(data_ingestion_config.to_dict())
    
    except Exception as e:
        raise SensorException(e,sys)