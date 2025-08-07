import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
import os
from src.logger import get_logger
from src.custom_exception import CustomException


logger = get_logger(__name__)


class DataProcessing():
    def __init__(self,file_path):
        self.file_path = file_path
        self.df = None
        self.processed_data_path = 'artifacts/processed'
        os.makedirs(self.processed_data_path, exist_ok=True)

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)
            logger.info("read the data sucessfully")

        except Exception as e:
            logger.error("error while reading the data")
            raise CustomException("Failed to read data", e)        
        
    def handle_outliers(self, column):
        try:
            logger.info("starting handling outlier information")

            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3-Q1

            Lower_value = Q1-1.5*IQR
            Upper_value = Q1+1.5*IQR

            sepal_median = np.median(self.df[column])    


            for i in self.df[column]:
                if i> Upper_value or i<Lower_value:
                   self.df[column] = self.df[column].replace(i,sepal_median)

            logger.info("Handled outliers sucessfully....")   

        except Exception as e:
            logger.error("error while handling outliers")
            raise CustomException("Failed to handle outliers", e)

    def split_data(self):
        try:
            X = self.df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
            Y = self.df['Species']   
            X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size=0.2, random_state=42)

            logger.info("data splitting done sucessfully")   

            joblib.dump(X_train, os.path.join(self.processed_data_path, 'X_train.pkl'))   
            joblib.dump(X_test, os.path.join(self.processed_data_path, 'X_test.pkl'))
            joblib.dump(Y_train, os.path.join(self.processed_data_path, 'Y_train.pkl'))
            joblib.dump(Y_test, os.path.join(self.processed_data_path, 'Y_test.pkl'))   

            logger.info("File saved successully for data processing steps")


        except Exception as e:
            logger.error("error while splitting data")
            raise CustomException("Failed to split data", e)   
        

    def run(self):
        self.load_data()
        self.handle_outliers('SepalWidthCm')
        self.split_data()   



if  __name__ == '__main__':
    DataProcessor = DataProcessing("artifacts/raw/data.csv")        
    DataProcessor.run()

                