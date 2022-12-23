from dataclasses import dataclass


@dataclass
class dataingestion_artifact:
    train_file_path:str
    test_file_path :str
    feature_store_path:str

@dataclass
class datavalidation_artifact:
     report_file_path:str

@dataclass
class datattransformation_artifact:
    transform_object_path:str
    transformed_train_path:str
    transformed_test_path:str
    target_encoder_path:str


@dataclass
class modeltraining_artifact:
    model_path:str
    f1_train_score:float 
    f1_test_score:float

@dataclass
class modelevaluation_artifact:
    is_model_accepted:bool
    improved_accuracy:float

@dataclass
class modelpusher_artifact:
    pusher_model_dir:str 
    saved_model_dir:str

