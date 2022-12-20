from fault_prediction.sensor.entity import config_entity,artifact_entity
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor.logger import logging
import os,sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from fault_prediction.sensor.config import Target_column
import pandas as pd
import numpy as np
from fault_prediction.sensor import utils
from imblearn.combine import SMOTETomek


class DataTransformation:
    def __init__(self,data_transformation_config,data_ingestion_artifact):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)


    @classmethod
    def get_data_transformation_object(cls):
        try:
            simple_imputer  = SimpleImputer(strategy='constant',fill_value= 0)
            robust_scaler = RobustScaler()
            step = [("imputer",simple_imputer),
            ("robustscaler",robust_scaler)]
            pipeline = Pipeline(steps = step)
            return pipeline
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_transformation(self):
        try:
            ### reading traing and testing file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            ##selecting input features for train and test dataset
            train_df_input_feature = train_df.drop(Target_column,axis =1)
            test_df_input_feature = test_df.drop(Target_column,axis = 1)
            ### selecting target feature for train and test data
            train_df_target_feature = train_df[Target_column]
            test_df_target_feature = test_df[Target_column]
            ## label encoding
            label_encoder = LabelEncoder()
            label_encoder.fit(train_df_target_feature)
            ### transformation of the target column
            target_feature_train_arr = label_encoder.transform(train_df_target_feature)
            target_feature_test_arr = label_encoder.transform(test_df_target_feature)

            transformation_pipeline = DataTransformation.get_data_transformation_object()
            transformation_pipeline.fit(train_df_input_feature)
            ### transformation of the input features
            input_feature_train_arr = transformation_pipeline.transform(train_df_input_feature)
            input_feature_test_arr = transformation_pipeline.transform(test_df_input_feature)
            
            ### resampling of the data
            smt = SMOTETomek(random_state = 42)
            logging.info(f"before resampling we have Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr}")
            input_feature_train_arr,target_feature_train_arr  = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling we have Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr}")
             
            logging.info(f"before resampling we have Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr}")
            input_feature_test_arr,target_feature_test_arr  = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling we have Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr}")

            ### target encoing
            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]

            ### save the model
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_path,array=train_arr)
            utils.save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_path,array= test_arr)


            utils.save_object(file_path=self.data_transformation_config.transformed_object,object=transformation_pipeline)
            utils.save_object(file_path= self.data_transformation_config.target_encoder_file_path,object=label_encoder)


            data_transformation_artifact = artifact_entity.datattransformation_artifact(
                transform_object_path=self.data_transformation_config.transformed_object,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_file_path

            )

            logging.info(f"Data transformation object {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)


