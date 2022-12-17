import os,sys
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor.config import mongoclient
import pandas as pd
import pymongo
import yaml



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


def write_yaml_file(file_path,data):
   try:
      file_dir = os.path.dirname(file_path)
      os.makedirs(file_dir,exist_ok=True)
      with open(file_path,"w") as file_writer :
         yaml.dump(data,file_writer)

   except Exception as e:
      raise SensorException(e,sys)   



def convert_to_float(df,exclude_column):
   try:
      for column in df.columns:
         if column not in exclude_column:
            df[column] = df[column].astype(float)
      return df
   except Exception as e :
      raise SensorException(e,sys)    





