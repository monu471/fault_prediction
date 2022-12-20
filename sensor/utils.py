import os,sys
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor.config import mongoclient
import pandas as pd
import pymongo
import yaml
import dill
import numpy as np




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


def save_object(file_path,object):
   try:
      logging.info("Enrtered the save object of utils")
      os.makedirs(os.path.dirname(file_path),exist_ok=True)
      with open(file_path,"wb") as file_obj:
          dill.dump(object,file_obj)
   except Exception as e:
      raise SensorException(e,sys)


def load_object(file_path):
   try:
      if not os.path.exists(file_path):
         raise Exception (f" path {file_path} is not exsist")
      with open(file_path,"rb") as file_obj:
         return dill.load(file_obj)
   except Exception as e:
      raise SensorException(e,sys) 

         

def save_numpy_array_data(file_path,array):
   try:
      dir_path = os.path.dirname(file_path)
      os.makedirs(dir_path,exist_ok=True)
      with open(file_path,"wb") as file_obj:
            return np.save(file_obj,array)
   except Exception as e:
      raise SensorException(e,sys)



def load_numpy_array_data(file_path):

   try:
      with open(file_path,"rb") as file_obj :
         return np.load(file_obj)
   except Exception as e:
      raise SensorException(e,sys)
      
