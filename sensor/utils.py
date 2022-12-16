import os,sys
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor.config import mongoclient
import pandas as pd
import pymongo



def get_data(database,collection):
    try:
       logging.info(f"we are reading {collection} from {database} ")
       df = pd.DataFrame(list(mongoclient[database][collection].find()))
       logging.info(f"we have column name{df.columns}")
       if "_id" in df.columns:
          logging.info("we are dropping id column from the dataset")
          df = df.drop(columns=["_id"])
       logging.info(f"we have the row and columnd{df.shape}")  
       return df

    except Exception as e :
        raise SensorException(e,sys)






