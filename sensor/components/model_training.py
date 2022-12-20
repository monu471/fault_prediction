from fault_prediction.sensor.entity import config_entity,artifact_entity
from fault_prediction.sensor.logger import logging
from fault_prediction.sensor.exception import SensorException
from fault_prediction.sensor import utils
from xgboost import XGBClassifier
import os,sys
from sklearn.metrics import f1_score


class ModelTraining:
    def __init__(self,model_training_config,data_transformation_artifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_training_config
            self.data_transformation_artifact=data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)  



    
    def train_model(self,x,y):
        try:
            xgb_clf =  XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)
    

    def initiate_model_trainer(self):
        try:
            logging.info("loading test and train array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            logging.info(f"Splitting input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]
            logging.info("training the model")
            model = self.train_model(x = x_train,y = y_train)

            logging.info("calculating f1 score")
            yhat_train = model.predict(x_train)
            f1_train_score  =f1_score(y_true=y_train, y_pred=yhat_train)

            logging.info(f"Calculating f1 test score")
            yhat_test = model.predict(x_test)
            f1_test_score  =f1_score(y_true=y_test, y_pred=yhat_test)
            logging.info(f"train score:{f1_train_score} and tests score {f1_test_score}")

            #check for overfitting or underfiiting or expected score
            logging.info(f"Checking if our model is underfitting or not")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it is not able to give \
                expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            logging.info(f"Checking if our model is overfiiting or not")
            diff = abs(f1_train_score-f1_test_score)

            
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            #save the trained model
            logging.info(f"Saving mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path, object=model)

            #prepare artifact
            logging.info(f"Prepare the artifact")
            model_trainer_artifact  = artifact_entity.modeltraining_artifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)
