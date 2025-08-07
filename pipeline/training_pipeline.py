from src.data_processing import DataProcessing
from src.model_training import ModelTraining




if  __name__ == '__main__':
    DataProcessor = DataProcessing("artifacts/raw/data.csv")        
    DataProcessor.run()

    trainer =  ModelTraining()
    trainer.run()