from dataclasses import dataclass


@dataclass
class dataingestion_artifact:
    train_file_path:str
    test_file_path :str
    feature_store_path:str