import os,sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongoclient
import pandas as pd



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



