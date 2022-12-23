from fault_prediction.sensor.pipeline.batch_prediction import start_batch_prediction
from fault_prediction.sensor.pipeline.training_pipeline import start_training_pipeline

path = r"E:\aps sensor\fault_prediction\sensor\aps_failure_training_set1.csv"
if __name__ == "__main__":
    try:
       output_file =  start_batch_prediction(input_file_path=path)
       print(output_file)
    except Exception as e:
        raise(e)